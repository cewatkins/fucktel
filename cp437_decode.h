/*
 * CP437 decoding library - Header file
 */

#ifndef CP437_DECODE_H
#define CP437_DECODE_H

#include <stddef.h>

/* Look up UTF-8 string for a CP437 byte */
const char* cp437_to_utf8(unsigned char byte);

/* Decode CP437 bytes to UTF-8, handling ANSI escape sequences */
void decode_cp437_graphical(const unsigned char *data, size_t len, 
                           char *output, size_t output_size);

#endif /* CP437_DECODE_H */
