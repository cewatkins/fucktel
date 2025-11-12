/*
 * Simple test program for CP437 character decoding
 */

#include <stdio.h>
#include <string.h>
#include "cp437_decode.h"

/* Test helper */
int test_decode(const char *test_name, const unsigned char *input, size_t input_len, const char *expected) {
    char output[1024];
    decode_cp437_graphical(input, input_len, output, sizeof(output));
    
    if (strcmp(output, expected) == 0) {
        printf("✓ %s\n", test_name);
        return 1;
    } else {
        printf("✗ %s\n", test_name);
        printf("  Expected: %s\n", expected);
        printf("  Got:      %s\n", output);
        return 0;
    }
}

int main(void) {
    int passed = 0;
    int total = 0;
    
    printf("CP437 Telnet Client - C Version Tests\n");
    printf("======================================\n\n");
    
    /* Test 1: Simple ASCII text */
    {
        unsigned char input[] = "Hello World";
        total++;
        if (test_decode("Simple ASCII text", input, strlen((char*)input), "Hello World")) {
            passed++;
        }
    }
    
    /* Test 2: Smiley face (0x01) */
    {
        unsigned char input[] = {0x01, 0x00};
        total++;
        if (test_decode("Smiley face", input, 1, "☺")) {
            passed++;
        }
    }
    
    /* Test 3: Multiple special chars */
    {
        unsigned char input[] = {0x01, 0x02, 0x03, 0x00};
        total++;
        if (test_decode("Multiple special chars", input, 3, "☺☻♥")) {
            passed++;
        }
    }
    
    /* Test 4: Mixed ASCII and special */
    {
        unsigned char input[] = {'H', 'i', ' ', 0x01, '!', 0x00};
        total++;
        if (test_decode("Mixed ASCII and special", input, 5, "Hi ☺!")) {
            passed++;
        }
    }
    
    /* Test 5: Card suits */
    {
        unsigned char input[] = {0x03, 0x04, 0x05, 0x06, 0x00};
        total++;
        if (test_decode("Card suits", input, 4, "♥♦♣♠")) {
            passed++;
        }
    }
    
    /* Test 6: Arrows */
    {
        unsigned char input[] = {0x18, 0x19, 0x16, 0x17, 0x00};
        total++;
        if (test_decode("Arrows", input, 4, "→←↑↓")) {
            passed++;
        }
    }
    
    /* Test 7: ANSI escape sequence (CSI) */
    {
        unsigned char input[] = {0x1B, '[', '3', '1', 'm', 'R', 'e', 'd', 0x1B, '[', '0', 'm', 0x00};
        total++;
        if (test_decode("ANSI CSI sequence", input, 12, "\x1B[31mRed\x1B[0m")) {
            passed++;
        }
    }
    
    /* Test 8: Control characters (preserved) */
    {
        unsigned char input[] = {'T', 'e', 's', 't', '\n', 0x00};
        total++;
        if (test_decode("Control chars (LF)", input, 5, "Test\n")) {
            passed++;
        }
    }
    
    printf("\n======================================\n");
    printf("Tests passed: %d/%d\n", passed, total);
    
    if (passed == total) {
        printf("All tests passed! ✓\n");
        return 0;
    } else {
        printf("Some tests failed.\n");
        return 1;
    }
}
