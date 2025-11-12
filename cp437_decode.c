/*
 * CP437 decoding library - Character mapping and decoding functions
 */

#define _POSIX_C_SOURCE 200112L

#include <string.h>
#include "cp437_decode.h"

/* CP437 graphical character mapping to Unicode UTF-8 */
typedef struct {
    unsigned char cp437_byte;
    const char *utf8_char;
} CP437Mapping;

/* CP437 special characters (low ASCII) mapping to UTF-8 */
static const CP437Mapping cp437_graphical_map[] = {
    {0x01, "☺"},  // Smiley Face
    {0x02, "☻"},  // Reverse Smiley
    {0x03, "♥"},  // Heart
    {0x04, "♦"},  // Diamond
    {0x05, "♣"},  // Club
    {0x06, "♠"},  // Spade
    {0x07, "•"},  // Bullet
    {0x0B, "♂"},  // Male
    {0x0C, "♀"},  // Female
    {0x0E, "►"},  // Play/Triangle Right
    {0x0F, "◄"},  // Pause/Triangle Left
    {0x10, "↕"},  // Up/Down Arrows
    {0x11, "‼"},  // Double Exclamation
    {0x12, "¶"},  // Pilcrow
    {0x13, "§"},  // Section Sign
    {0x14, "▬"},  // Rectangle
    {0x15, "↨"},  // Up/Down Arrow with Base
    {0x16, "↑"},  // Up Arrow
    {0x17, "↓"},  // Down Arrow
    {0x18, "→"},  // Right Arrow
    {0x19, "←"},  // Left Arrow
    {0x1A, "∟"},  // Right Angle
    {0x1B, "↔"},  // Left/Right Arrow
    {0x1C, "▲"},  // Up Triangle
    {0x1D, "▼"},  // Down Triangle
    {0x1E, "⌠"},  // Top Half Integral
    {0x1F, "⌡"},  // Bottom Half Integral
    {0x7F, "⌂"},  // House
    {0x00, NULL}  // Sentinel
};

/* Look up UTF-8 string for a CP437 byte */
const char* cp437_to_utf8(unsigned char byte) {
    /* Check special graphical characters first */
    for (int i = 0; cp437_graphical_map[i].utf8_char != NULL; i++) {
        if (cp437_graphical_map[i].cp437_byte == byte) {
            return cp437_graphical_map[i].utf8_char;
        }
    }
    
    /* For standard ASCII (0x20-0x7E), return as-is */
    /* For control characters we want to preserve (BS, TAB, LF, CR), return as-is */
    static char single_byte[2] = {0, 0};
    
    if (byte == 0x08 || byte == 0x09 || byte == 0x0A || byte == 0x0D ||
        (byte >= 0x20 && byte <= 0x7E)) {
        single_byte[0] = byte;
        return single_byte;
    }
    
    /* For other characters, we'd need full CP437 table */
    /* For now, return as-is for simplicity */
    single_byte[0] = byte;
    return single_byte;
}

/* Decode CP437 bytes to UTF-8, handling ANSI escape sequences */
void decode_cp437_graphical(const unsigned char *data, size_t len, char *output, size_t output_size) {
    size_t out_idx = 0;
    size_t i = 0;
    
    while (i < len && out_idx < output_size - 10) {
        unsigned char byte = data[i];
        
        /* Check for ANSI escape sequence (ESC = 0x1B) */
        if (byte == 0x1B && i + 1 < len) {
            /* Start of potential escape sequence */
            if (data[i + 1] == '[') {
                /* CSI sequence: ESC [ ... */
                output[out_idx++] = 0x1B;
                output[out_idx++] = '[';
                i += 2;
                
                /* Copy until we find the terminator (letter in range @-~) */
                while (i < len && out_idx < output_size - 1) {
                    unsigned char c = data[i];
                    output[out_idx++] = c;
                    i++;
                    if (c >= 0x40 && c <= 0x7E) {
                        break;
                    }
                }
                continue;
            } else if (data[i + 1] == ']') {
                /* OSC sequence: ESC ] ... (terminated by BEL or ESC \) */
                output[out_idx++] = 0x1B;
                output[out_idx++] = ']';
                i += 2;
                
                /* Copy until BEL or ESC \ */
                while (i < len && out_idx < output_size - 2) {
                    unsigned char c = data[i];
                    output[out_idx++] = c;
                    i++;
                    if (c == 0x07) {  /* BEL */
                        break;
                    }
                    if (c == 0x1B && i < len && data[i] == '\\') {
                        output[out_idx++] = '\\';
                        i++;
                        break;
                    }
                }
                continue;
            }
        }
        
        /* Regular CP437 character */
        const char *utf8_str = cp437_to_utf8(byte);
        size_t utf8_len = strlen(utf8_str);
        
        if (out_idx + utf8_len < output_size) {
            memcpy(output + out_idx, utf8_str, utf8_len);
            out_idx += utf8_len;
        }
        i++;
    }
    
    output[out_idx] = '\0';
}
