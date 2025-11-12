# CP437 Telnet Client - C Version

A C implementation of the CP437 telnet client that properly handles CP437 (Code Page 437) graphical characters, including low ASCII symbols that are typically lost in standard UTF-8 telnet connections.

## Features

- ✅ Full CP437 graphical character support (including low ASCII 0x01-0x1F and 0x7F)
- ✅ Proper Unicode mapping for CP437 special characters
- ✅ Non-blocking I/O for simultaneous read/write
- ✅ Raw terminal mode for character-by-character input
- ✅ ANSI escape sequence preservation (CSI, OSC)
- ✅ Minimal dependencies (only standard C libraries)
- ✅ Portable POSIX-compliant code

## Supported Characters

The client maps CP437 special characters to Unicode equivalents:

- **Smileys**: ☺ ☻
- **Card Suits**: ♥ ♦ ♣ ♠
- **Symbols**: • ♂ ♀
- **Arrows**: ↑ ↓ → ← ↔ ↕
- **Triangles**: ► ◄ ▲ ▼
- **Shapes**: ⌠ ⌡ ⌂
- **And more**: Full low ASCII CP437 graphical palette

## Requirements

- C compiler (gcc, clang, or compatible)
- POSIX-compliant system (Linux, macOS, BSD, etc.)
- Standard C libraries (socket, termios)

## Building

### Using Make

```bash
# Build the telnet client
make

# Build the examples program
make examples_c

# Build everything
make all

# Clean build artifacts
make clean
```

### Manual Compilation

```bash
# Compile the telnet client
gcc -Wall -Wextra -O2 -std=c99 -o fucktel fucktel.c

# Compile the examples program
gcc -Wall -Wextra -O2 -std=c99 -o examples_c examples.c
```

## Usage

### Command Line

```bash
# Connect to a telnet host with default port 23
./fucktel hostname

# Connect to a custom port
./fucktel hostname 6666

# Run examples to see CP437 characters
./examples_c
```

### Example Sessions

```bash
# Connect to a BBS or retro telnet server
./fucktel bbs.example.com 23

# Type commands as normal, graphical characters will display correctly
# Press Ctrl+] to disconnect
```

## Controls

- **Ctrl+]** - Disconnect and quit the client

## How It Works

1. **Connection**: Establishes a TCP socket connection to the telnet server
2. **Terminal Setup**: Sets stdin to raw mode for character-by-character input
3. **Receiving**: Incoming CP437 bytes are decoded to UTF-8 using the character map
4. **ANSI Handling**: ANSI escape sequences (ESC[...] and ESC]...) are preserved
5. **Display**: UTF-8 characters are printed to the terminal
6. **Input**: User input is sent directly to the server
7. **Non-blocking I/O**: Uses select() for simultaneous read from stdin and socket

## Project Structure

```
.
├── fucktel.c           # Main C telnet client implementation
├── examples.c          # Example program demonstrating CP437 characters
├── Makefile           # Build configuration
├── README_C.md        # This file
└── (Python files)     # Original Python implementation
```

## CP437 Character Mapping

The C implementation includes mappings for all special CP437 characters:

| Byte | Unicode | Character | Description |
|------|---------|-----------|-------------|
| 0x01 | U+263A  | ☺ | Smiley Face |
| 0x02 | U+263B  | ☻ | Reverse Smiley |
| 0x03 | U+2665  | ♥ | Heart |
| 0x04 | U+2666  | ♦ | Diamond |
| 0x05 | U+2663  | ♣ | Club |
| 0x06 | U+2660  | ♠ | Spade |
| ... | ... | ... | ... |

See `fucktel.c` for the complete mapping table.

## Technical Details

### Non-Blocking I/O
- Uses `select()` system call for multiplexed I/O
- Monitors both stdin and network socket simultaneously
- 100ms timeout for responsive control handling

### Terminal Handling
- Saves original terminal settings at startup
- Sets raw mode (no echo, no canonical, no signals)
- Restores original settings on exit (even after signals)

### Character Decoding
- Static lookup table for CP437 → UTF-8 mapping
- Preserves ANSI escape sequences (CSI and OSC)
- Handles incomplete sequences gracefully
- Control characters (BS, TAB, LF, CR) passed through

### Signal Handling
- Catches SIGINT (Ctrl+C) and SIGTERM
- Ensures clean shutdown and terminal restoration
- Uses volatile sig_atomic_t for safe flag updates

## Differences from Python Version

### Similarities
- Same CP437 character mapping
- Same ANSI escape sequence handling
- Same user interface and controls
- Same basic functionality

### Differences
- **No async/await**: Uses select() instead of asyncio
- **Simpler telnet**: No full telnet protocol negotiation (binary mode only)
- **No logging**: Session logging not implemented in C version
- **No macros**: Bell macro feature not implemented
- **Smaller footprint**: Minimal dependencies, faster startup
- **Portable**: Standard C with POSIX, no external libraries

## Installation

### System-wide Installation (Optional)

```bash
# Install to /usr/local/bin (requires root)
sudo make install

# Uninstall
sudo make uninstall
```

### Local Installation

Just copy the compiled binary to your preferred location:

```bash
cp fucktel ~/bin/
# or
cp fucktel ~/.local/bin/
```

## Limitations

- Requires UTF-8 capable terminal
- Some CP437 characters may not render perfectly depending on terminal font
- No full telnet protocol negotiation (works with most servers)
- No session logging (use `script` command if needed)
- No macro support

## Testing

Run the examples program to verify proper character rendering:

```bash
make examples_c
./examples_c
```

You should see properly rendered CP437 special characters including smileys, card suits, arrows, and box-drawing characters.

## Troubleshooting

### Connection Issues
- Verify the host and port are correct
- Ensure the telnet service is running on the target
- Check firewall rules

### Character Display Issues
- Verify your terminal supports UTF-8
- Try a different terminal emulator (e.g., xterm, gnome-terminal)
- Ensure your terminal font includes Unicode characters
- Test with `./examples_c` first

### Compilation Errors
- Ensure you have a C compiler installed (`gcc` or `clang`)
- Check that you're on a POSIX-compliant system
- Try manual compilation with explicit flags

## Comparison: C vs Python

### When to Use C Version
- **Minimal dependencies**: No Python runtime required
- **Performance**: Faster startup, lower memory usage
- **Embedded systems**: Smaller footprint
- **Learning**: Simple, readable C code
- **Portability**: Standard C works everywhere

### When to Use Python Version
- **Advanced features**: Session logging, macros, key remapping
- **Development speed**: Easier to extend and modify
- **Full telnet protocol**: Complete negotiation support
- **More robust**: Better error handling and edge cases

## Contributing

Contributions are welcome! When contributing to the C version:

1. Follow the existing code style
2. Keep dependencies minimal (standard C/POSIX only)
3. Test on multiple platforms if possible
4. Ensure no memory leaks (use valgrind)
5. Update documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Resources

- [CP437 Wikipedia](https://en.wikipedia.org/wiki/Code_page_437)
- [Unicode Character Database](https://www.unicode.org/unidata/)
- [ANSI Escape Codes](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [Original Python Implementation](README.md)

## Author

C implementation based on the original Python version by cewatkins.

## Support

For issues, questions, or suggestions about the C version, please open an issue on the GitHub repository.
