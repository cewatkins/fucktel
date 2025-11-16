# CP437 Telnet Client

A Python telnet client that properly handles CP437 (Code Page 437) graphical characters, including low ASCII symbols that are typically lost in standard UTF-8 telnet connections.

## Features

- ✅ Full CP437 graphical character support (including low ASCII 0x01-0x1F and 0x7F)
- ✅ Proper Unicode mapping for all 256 CP437 characters
- ✅ Complete ANSI/VT100 escape sequence support
- ✅ Async/await based for non-blocking I/O
- ✅ Built on `telnetlib3` for robust telnet protocol handling
- ✅ Bidirectional encoding/decoding
- ✅ Interactive terminal shell
- ✅ **Compliant with historical ANSI rendering standards** (16colo.rs guidelines)
- ✅ Customizable key mappings (ANSI, SyncTerm)
- ✅ Session logging support
- ✅ Macro support with configurable delays

## Supported Characters

The client maps all CP437 special characters to Unicode equivalents:

- **Smileys**: ☺ ☻
- **Symbols**: ♥ ♦ ♣ ♠ • ◘ ○ ♂ ♀ ♪ ► ◄ ↕ ‼ ¶ § ▬ ↨
- **Arrows**: ↑ ↓ → ← ↔
- **Shapes**: ▲ ▼ ⌠ ⌡ ⌂
- **And more**: Full 256-character CP437 palette

## Requirements

- Python 3.8+
- `telnetlib3` >= 1.0.4

## Installation

### From source

```bash
# Clone the repository
git clone https://github.com/yourusername/cp437-telnet.git
cd cp437-telnet

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Via pip (when published)

```bash
pip install cp437-telnet
```

## Usage

### Command Line

```bash
# Connect to a telnet host with default port 23
python3 fucktel.py hostname

# Connect to a custom port
python3 fucktel.py hostname 6666

# With session logging
python3 fucktel.py hostname 23 --log session.log

# With SyncTerm key mappings (default)
python3 fucktel.py hostname 23 --syncterm

# With ANSI key mappings
python3 fucktel.py hostname 23 --ansi

# With macro support (Ctrl+G sends commands, use hjkl for arrows)
python3 fucktel.py hostname 23 --bell "vjkl"

# Custom terminal dimensions
python3 fucktel.py hostname 23 --cols 120 --rows 40

# Or use the installed command
fucktel hostname
fucktel hostname 6666
```

### Example

```bash
# Connect to a BBS or retro telnet server
python3 cp437_telnet.py bbs.example.com 23

# Type commands as normal, graphical characters will display correctly
# Type 'exit' to disconnect
```

### Programmatic Usage

```python
import asyncio
from cp437_telnet import decode_cp437_graphical, encode_to_cp437

# Decode CP437 bytes to Unicode
cp437_data = bytes([0x01, 0x02, 0x03])  # ☺☻♥
unicode_text = decode_cp437_graphical(cp437_data)
print(unicode_text)  # Output: ☺☻♥

# Encode Unicode text to CP437 bytes
unicode_text = "Hello ☺"
cp437_bytes = encode_to_cp437(unicode_text)
print(cp437_bytes)  # Output: b'Hello \x01'
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/cp437-telnet.git
cd cp437-telnet

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Running Tests

```bash
# Run all tests
python3 -m pytest tests/ -v

# Or use unittest
python3 -m unittest discover -s tests -p "test_*.py" -v

# Run specific test file
python3 -m unittest tests.test_cp437 -v

# With coverage
pip install coverage
coverage run -m unittest discover -s tests -p "test_*.py"
coverage report -m
coverage html  # generates htmlcov/index.html
```

### Code Quality

```bash
# Format code
pip install black
black cp437_telnet.py tests/

# Lint
pip install flake8
flake8 cp437_telnet.py tests/

# Type checking
pip install mypy
mypy cp437_telnet.py

# All checks
black --check cp437_telnet.py tests/ && flake8 cp437_telnet.py tests/ && mypy cp437_telnet.py
```

## ANSI Rendering Compliance

This client fully complies with proper ANSI rendering standards as outlined in the [16colo.rs guide on ANSI rendering](https://16colo.rs). Key compliance points:

### ✅ What We Handle Correctly

- **CP437 Codepage**: Full support for IBM PC Code Page 437 (standard for classic BBS ANSI art)
- **Binary 8-bit Clean**: Uses `force_binary=True` to preserve CP437 bytes without telnet protocol interference
- **ANSI Escape Sequences**: Complete support for:
  - CSI sequences (colors, cursor movement, screen operations)
  - OSC sequences (operating system commands)
  - Character set selection (line drawing modes)
  - Cursor save/restore
  - Relative and absolute positioning
  - Screen clearing and line operations
- **Sequence Buffering**: Properly handles incomplete ANSI sequences split across TCP packets
- **Robustness**: Auto-fixes common server bugs (e.g., clear without home cursor)

### ⚠️ Important Limitations (By Design)

- **Pixel Aspect Ratio**: CRT hardware used 35% taller pixels than modern LCD displays
  - Pre-2000 art may appear "squashed"
  - **Solution**: Use terminal fonts designed for retro BBS or research artwork date
- **Character Spacing**: Classic hardware had 9-pixel spacing; modern terminals use 8-pixel
  - Line-drawing characters may have gaps
  - **Solution**: Use fonts like "Perfect DOS VGA 437" or "Terminus"
- **Multiple Codepages**: Only CP437 is fully supported (CP850, etc. not implemented)
  - **Workaround**: Most classic art uses CP437

### 📚 Documentation

See the following for detailed compliance information:
- **[ANSI_RENDERING_COMPLIANCE.md](./ANSI_RENDERING_COMPLIANCE.md)** - Comprehensive compliance documentation
- **[ANSI_COMPLIANCE_QUICK_REFERENCE.md](./ANSI_COMPLIANCE_QUICK_REFERENCE.md)** - Quick reference and troubleshooting

## Project Structure

```
fucktel/
├── fucktel.py                              # Main module
├── tests/
│   ├── __init__.py
│   ├── test_cp437.py                       # CP437 encoding/decoding tests
│   └── test_ansi_extended.py               # ANSI sequence tests
├── ANSI_RENDERING_COMPLIANCE.md            # Comprehensive compliance documentation
├── ANSI_COMPLIANCE_QUICK_REFERENCE.md      # Quick reference guide
├── ANSI_ANALYSIS.md                        # Implementation analysis
├── requirements.txt                        # Python dependencies
├── setup.py                                # Package configuration
├── .gitignore                              # Git ignore rules
├── README.md                               # This file
└── LICENSE                                 # MIT License
```

## CP437 Character Mapping

The client includes a complete mapping of all 256 CP437 characters to Unicode:

| Byte | Unicode | Character |
|------|---------|-----------|
| 0x01 | U+263A  | ☺ (Smiley Face) |
| 0x02 | U+263B  | ☻ (Reverse Smiley) |
| 0x03 | U+2665  | ♥ (Heart) |
| 0x04 | U+2666  | ♦ (Diamond) |
| ... | ... | ... |

See `cp437_telnet.py` for the complete mapping.

## How It Works

1. **Connection**: Establishes a binary telnet connection in 8-bit clean mode
2. **Receiving**: Incoming CP437 bytes are decoded to Unicode using the CP437 character map
3. **Display**: Unicode characters are printed to the terminal
4. **Input**: User input is encoded back to CP437 before sending to the server
5. **Encoding**: UTF-8 text is converted to CP437 with fallback to latin-1

## Technical Details

- Uses `asyncio` for non-blocking I/O
- `telnetlib3` handles telnet protocol negotiation
- Binary mode (`force_binary=True`) ensures 8-bit clean data transfer
- Graphical character overrides for low ASCII (0x01-0x1F, 0x7F)
- Inverse Unicode-to-CP437 mapping for encoding

## Limitations

- Requires Unicode-capable terminal
- Some CP437 characters may not render perfectly depending on terminal font
- Line endings are normalized to CRLF (telnet standard)

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -am 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Testing Requirements

All contributions should:
- Pass existing tests: `python3 -m unittest discover -s tests`
- Have no lint errors: `flake8 cp437_telnet.py`
- Follow code style: `black cp437_telnet.py`

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### ANSI/Rendering Issues

**Art looks "squashed" vertically**
- This is expected for pre-2000 artwork on modern monitors (CRT vs LCD pixel aspect)
- Research the artwork's creation date (check SAUCE metadata)
- Try terminal fonts with non-square pixel ratios

**Line-drawing characters have gaps**
- Modern terminals use 8-pixel character width; classic hardware used 9-pixel
- Try retro-designed terminal fonts like "Perfect DOS VGA 437"

**Colors don't work**
- Set terminal to support 256 colors minimum (or 24-bit RGB preferred)
- Some BBS systems require manual color configuration

**First line of text appears at wrong position after clear**
- This is a known server bug; fucktel auto-fixes it
- If still occurring, try a different BBS

### Connection Issues

**Connection refused**
- Verify the host and port are correct
- Ensure the telnet service is running on the target
- Check firewall rules

**Characters display incorrectly**
- Verify your terminal supports Unicode (UTF-8)
- Try a different terminal emulator
- Ensure your terminal font includes the required Unicode characters
- Check if BBS uses CP850 or other codepage (fucktel uses CP437)

**Keys don't work**
- Try `--ansi` or `--syncterm` key mapping modes
- Some BBS systems use different escape sequences
- Use `--bell` macro feature for common navigation patterns

### Encoding Errors

- Input characters may not have a CP437 equivalent
- The client will fall back to the closest latin-1 equivalent
- Safe fallback to '?' for unmapped characters

## Resources

- [Telnetlib3 Documentation](https://telnetlib3.readthedocs.io/)
- [CP437 Wikipedia](https://en.wikipedia.org/wiki/Code_page_437)
- [Unicode Character Database](https://www.unicode.org/unidata/)

## Author

Your Name (@yourusername)

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.
