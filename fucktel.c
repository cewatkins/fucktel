/*
 * CP437 Telnet Client - C implementation
 * 
 * A telnet client that properly handles CP437 (Code Page 437) graphical
 * characters, including low ASCII symbols that are typically lost in
 * standard UTF-8 telnet connections.
 */

#define _POSIX_C_SOURCE 200112L

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <termios.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <errno.h>
#include <signal.h>
#include <fcntl.h>
#include "cp437_decode.h"

/* Global state */
static struct termios orig_termios;
static int sockfd = -1;
static volatile sig_atomic_t running = 1;

/* Signal handler for clean exit */
void handle_signal(int sig) {
    (void)sig;  /* Unused parameter */
    running = 0;
}

/* Restore terminal settings */
void restore_terminal(void) {
    if (isatty(STDIN_FILENO)) {
        tcsetattr(STDIN_FILENO, TCSAFLUSH, &orig_termios);
    }
}

/* Set terminal to raw mode */
int set_raw_mode(void) {
    struct termios raw;
    
    if (!isatty(STDIN_FILENO)) {
        return 0;
    }
    
    if (tcgetattr(STDIN_FILENO, &orig_termios) == -1) {
        perror("tcgetattr");
        return -1;
    }
    
    atexit(restore_terminal);
    
    raw = orig_termios;
    raw.c_lflag &= ~(ECHO | ICANON | ISIG | IEXTEN);
    raw.c_iflag &= ~(BRKINT | ICRNL | INPCK | ISTRIP | IXON);
    raw.c_oflag &= ~(OPOST);
    raw.c_cflag |= (CS8);
    raw.c_cc[VMIN] = 0;
    raw.c_cc[VTIME] = 1;
    
    if (tcsetattr(STDIN_FILENO, TCSAFLUSH, &raw) == -1) {
        perror("tcsetattr");
        return -1;
    }
    
    return 0;
}

/* Connect to telnet server */
int connect_telnet(const char *host, int port) {
    struct addrinfo hints, *res, *rp;
    char port_str[16];
    int sock;
    
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    
    snprintf(port_str, sizeof(port_str), "%d", port);
    
    if (getaddrinfo(host, port_str, &hints, &res) != 0) {
        fprintf(stderr, "Error resolving host: %s\n", host);
        return -1;
    }
    
    /* Try each address */
    for (rp = res; rp != NULL; rp = rp->ai_next) {
        sock = socket(rp->ai_family, rp->ai_socktype, rp->ai_protocol);
        if (sock == -1) {
            continue;
        }
        
        if (connect(sock, rp->ai_addr, rp->ai_addrlen) != -1) {
            break;  /* Success */
        }
        
        close(sock);
    }
    
    freeaddrinfo(res);
    
    if (rp == NULL) {
        fprintf(stderr, "Could not connect to %s:%d\n", host, port);
        return -1;
    }
    
    /* Set non-blocking */
    int flags = fcntl(sock, F_GETFL, 0);
    fcntl(sock, F_SETFL, flags | O_NONBLOCK);
    
    return sock;
}

/* Main telnet loop */
void telnet_loop(int sock) {
    char recv_buffer[4096];
    char decoded_buffer[16384];
    char input_buffer[1024];
    fd_set readfds;
    struct timeval tv;
    
    printf("\033[2J\033[H");  /* Clear screen and home cursor */
    fflush(stdout);
    
    while (running) {
        FD_ZERO(&readfds);
        FD_SET(STDIN_FILENO, &readfds);
        FD_SET(sock, &readfds);
        
        tv.tv_sec = 0;
        tv.tv_usec = 100000;  /* 100ms timeout */
        
        int max_fd = (sock > STDIN_FILENO ? sock : STDIN_FILENO) + 1;
        int ret = select(max_fd, &readfds, NULL, NULL, &tv);
        
        if (ret < 0) {
            if (errno == EINTR) {
                continue;
            }
            perror("select");
            break;
        }
        
        /* Handle server data */
        if (FD_ISSET(sock, &readfds)) {
            ssize_t n = recv(sock, recv_buffer, sizeof(recv_buffer) - 1, 0);
            if (n > 0) {
                decode_cp437_graphical((unsigned char *)recv_buffer, n, 
                                      decoded_buffer, sizeof(decoded_buffer));
                printf("%s", decoded_buffer);
                fflush(stdout);
            } else if (n == 0) {
                printf("\nConnection closed by server.\n");
                break;
            } else if (errno != EAGAIN && errno != EWOULDBLOCK) {
                perror("recv");
                break;
            }
        }
        
        /* Handle user input */
        if (FD_ISSET(STDIN_FILENO, &readfds)) {
            ssize_t n = read(STDIN_FILENO, input_buffer, sizeof(input_buffer));
            if (n > 0) {
                /* Check for Ctrl+] (0x1D) to exit */
                for (ssize_t i = 0; i < n; i++) {
                    if (input_buffer[i] == 0x1D) {
                        printf("\n\nDisconnected.\n");
                        running = 0;
                        break;
                    }
                }
                
                if (running && send(sock, input_buffer, n, 0) < 0) {
                    if (errno != EAGAIN && errno != EWOULDBLOCK) {
                        perror("send");
                        break;
                    }
                }
            } else if (n == 0) {
                break;
            }
        }
    }
}

/* Print usage */
void print_usage(const char *prog) {
    fprintf(stderr, "Usage: %s <host> [port]\n", prog);
    fprintf(stderr, "  host: Telnet server hostname or IP address\n");
    fprintf(stderr, "  port: Port number (default: 23)\n");
    fprintf(stderr, "\nPress Ctrl+] to disconnect\n");
}

/* Main entry point */
int main(int argc, char *argv[]) {
    const char *host;
    int port = 23;
    
    if (argc < 2) {
        print_usage(argv[0]);
        return 1;
    }
    
    host = argv[1];
    
    if (argc >= 3) {
        port = atoi(argv[2]);
        if (port <= 0 || port > 65535) {
            fprintf(stderr, "Invalid port number: %s\n", argv[2]);
            return 1;
        }
    }
    
    /* Set up signal handlers */
    signal(SIGINT, handle_signal);
    signal(SIGTERM, handle_signal);
    
    /* Connect to server */
    printf("Connecting to %s:%d...\n", host, port);
    sockfd = connect_telnet(host, port);
    if (sockfd < 0) {
        return 1;
    }
    
    printf("Connected! Press Ctrl+] to quit.\n\n");
    
    /* Set terminal to raw mode */
    if (set_raw_mode() < 0) {
        close(sockfd);
        return 1;
    }
    
    /* Run telnet loop */
    telnet_loop(sockfd);
    
    /* Cleanup */
    close(sockfd);
    restore_terminal();
    
    return 0;
}
