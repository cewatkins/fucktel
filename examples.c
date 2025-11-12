/*
 * Example usage of CP437 character decoding in C
 * Run to test CP437 functionality
 */

#include <stdio.h>
#include <string.h>

/* CP437 graphical character mapping to Unicode UTF-8 */
typedef struct {
    unsigned char cp437_byte;
    const char *utf8_char;
    const char *description;
} CP437Example;

/* Sample CP437 special characters */
static const CP437Example cp437_examples[] = {
    {0x01, "☺", "Smiley Face"},
    {0x02, "☻", "Reverse Smiley"},
    {0x03, "♥", "Heart"},
    {0x04, "♦", "Diamond"},
    {0x05, "♣", "Club"},
    {0x06, "♠", "Spade"},
    {0x07, "•", "Bullet"},
    {0x0B, "♂", "Male"},
    {0x0C, "♀", "Female"},
    {0x0E, "►", "Play/Triangle Right"},
    {0x0F, "◄", "Pause/Triangle Left"},
    {0x10, "↕", "Up/Down Arrows"},
    {0x11, "‼", "Double Exclamation"},
    {0x12, "¶", "Pilcrow"},
    {0x13, "§", "Section Sign"},
    {0x14, "▬", "Rectangle"},
    {0x15, "↨", "Up/Down Arrow with Base"},
    {0x16, "↑", "Up Arrow"},
    {0x17, "↓", "Down Arrow"},
    {0x18, "→", "Right Arrow"},
    {0x19, "←", "Left Arrow"},
    {0x1A, "∟", "Right Angle"},
    {0x1B, "↔", "Left/Right Arrow"},
    {0x1C, "▲", "Up Triangle"},
    {0x1D, "▼", "Down Triangle"},
    {0x1E, "⌠", "Top Half Integral"},
    {0x1F, "⌡", "Bottom Half Integral"},
    {0x7F, "⌂", "House"},
    {0x00, NULL, NULL}  // Sentinel
};

void print_separator(void) {
    printf("============================================================\n");
}

void example1_character_display(void) {
    print_separator();
    printf("Example 1: CP437 Character Display\n");
    print_separator();
    printf("\n");
    
    printf("Low ASCII special characters:\n");
    for (int i = 0; cp437_examples[i].utf8_char != NULL; i++) {
        printf("  0x%02X: %s  (%s)\n", 
               cp437_examples[i].cp437_byte,
               cp437_examples[i].utf8_char,
               cp437_examples[i].description);
    }
    printf("\n");
}

void example2_ascii_art(void) {
    print_separator();
    printf("Example 2: ASCII Art with CP437 Characters\n");
    print_separator();
    printf("\n");
    
    printf("╭────────────────────────────────────╮\n");
    printf("│  CP437 Telnet Client (C Version)  │\n");
    printf("│  ☺ Retro BBS Support ♥            │\n");
    printf("│  ► Full Character Coverage ◄       │\n");
    printf("│  ↑ Modern Unicode Display ↓        │\n");
    printf("╰────────────────────────────────────╯\n");
    printf("\n");
}

void example3_sample_bbs_screen(void) {
    print_separator();
    printf("Example 3: Sample BBS-Style Screen\n");
    print_separator();
    printf("\n");
    
    printf("╔════════════════════════════════════════════════════════╗\n");
    printf("║              ☺ WELCOME TO THE BBS ☺                   ║\n");
    printf("╠════════════════════════════════════════════════════════╣\n");
    printf("║                                                        ║\n");
    printf("║  ► Messages                                            ║\n");
    printf("║  ► Files                                               ║\n");
    printf("║  ► Games                                               ║\n");
    printf("║  ► Chat                                                ║\n");
    printf("║                                                        ║\n");
    printf("║  Use arrow keys: ↑ ↓ ← →                              ║\n");
    printf("║  Select with: ►                                        ║\n");
    printf("║                                                        ║\n");
    printf("╚════════════════════════════════════════════════════════╝\n");
    printf("\n");
}

void example4_card_suits(void) {
    print_separator();
    printf("Example 4: Card Suits\n");
    print_separator();
    printf("\n");
    
    printf("Standard playing card suits:\n");
    printf("  Hearts:   ♥\n");
    printf("  Diamonds: ♦\n");
    printf("  Clubs:    ♣\n");
    printf("  Spades:   ♠\n");
    printf("\n");
    
    printf("Sample card display:\n");
    printf("  ╔═══╗ ╔═══╗ ╔═══╗ ╔═══╗\n");
    printf("  ║ A ║ ║ K ║ ║ Q ║ ║ J ║\n");
    printf("  ║ ♥ ║ ║ ♦ ║ ║ ♣ ║ ║ ♠ ║\n");
    printf("  ╚═══╝ ╚═══╝ ╚═══╝ ╚═══╝\n");
    printf("\n");
}

void example5_arrows_and_symbols(void) {
    print_separator();
    printf("Example 5: Arrows and Navigation Symbols\n");
    print_separator();
    printf("\n");
    
    printf("Directional arrows:\n");
    printf("  Up:    ↑\n");
    printf("  Down:  ↓\n");
    printf("  Left:  ←\n");
    printf("  Right: →\n");
    printf("  Both:  ↔ ↕\n");
    printf("\n");
    
    printf("Triangles:\n");
    printf("  Play:  ►\n");
    printf("  Pause: ◄\n");
    printf("  Up:    ▲\n");
    printf("  Down:  ▼\n");
    printf("\n");
}

void example6_smileys_and_faces(void) {
    print_separator();
    printf("Example 6: Smileys and Gender Symbols\n");
    print_separator();
    printf("\n");
    
    printf("Emoticons:\n");
    printf("  Happy:   ☺\n");
    printf("  Inverted: ☻\n");
    printf("\n");
    
    printf("Gender symbols:\n");
    printf("  Male:   ♂\n");
    printf("  Female: ♀\n");
    printf("\n");
}

void example7_usage_info(void) {
    print_separator();
    printf("Example 7: Usage Information\n");
    print_separator();
    printf("\n");
    
    printf("CP437 Telnet Client - C Version\n");
    printf("\n");
    printf("Compilation:\n");
    printf("  make              # Build the client\n");
    printf("  make examples_c   # Build this examples program\n");
    printf("\n");
    printf("Usage:\n");
    printf("  ./fucktel <host> [port]\n");
    printf("  ./fucktel bbs.example.com\n");
    printf("  ./fucktel telnet.server.net 6666\n");
    printf("\n");
    printf("Controls:\n");
    printf("  Ctrl+]  - Disconnect and quit\n");
    printf("\n");
    printf("Features:\n");
    printf("  ☺ Full CP437 graphical character support\n");
    printf("  ☺ Proper Unicode mapping for all 256 CP437 characters\n");
    printf("  ☺ Non-blocking I/O for simultaneous read/write\n");
    printf("  ☺ Raw terminal mode for character-by-character input\n");
    printf("  ☺ ANSI escape sequence preservation\n");
    printf("\n");
}

int main(void) {
    printf("\n");
    printf("╔════════════════════════════════════════════════════════╗\n");
    printf("║     CP437 Telnet Client - C Version Examples          ║\n");
    printf("╚════════════════════════════════════════════════════════╝\n");
    printf("\n");
    
    example1_character_display();
    example2_ascii_art();
    example3_sample_bbs_screen();
    example4_card_suits();
    example5_arrows_and_symbols();
    example6_smileys_and_faces();
    example7_usage_info();
    
    print_separator();
    printf("Examples completed successfully!\n");
    print_separator();
    printf("\n");
    
    return 0;
}
