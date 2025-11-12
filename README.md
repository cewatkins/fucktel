# CP437 Telnet Client

A telnet client that properly handles CP437 (Code Page 437) graphical characters, including low ASCII symbols that are typically lost in standard UTF-8 telnet connections.

**Available in two implementations:**
- **Python** - Feature-rich with session logging, macros, and advanced telnet support
- **C** - Lightweight, fast, zero dependencies (see [README_C.md](README_C.md))

## Features

- ✅ Full CP437 graphical character support (including low ASCII 0x01-0x1F and 0x7F)
- ✅ Proper Unicode mapping for all 256 CP437 characters
- ✅ Async/await based for non-blocking I/O
- ✅ Built on `telnetlib3` for robust telnet protocol handling
- ✅ Bidirectional encoding/decoding
- ✅ Interactive terminal shell

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
python3 cp437_telnet.py hostname

# Connect to a custom port
python3 cp437_telnet.py hostname 6666

# Or use the installed command
cp437-telnet hostname
cp437-telnet hostname 6666
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

## Project Structure

```
cp437-telnet/
├── cp437_telnet.py          # Main module
├── tests/
│   ├── __init__.py
│   └── test_cp437.py        # Unit tests
├── requirements.txt         # Python dependencies
├── setup.py                 # Package configuration
├── .gitignore              # Git ignore rules
├── README.md               # This file
└── LICENSE                 # MIT License
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

### Connection refused
- Verify the host and port are correct
- Ensure the telnet service is running on the target
- Check firewall rules

### Characters display incorrectly
- Verify your terminal supports Unicode (UTF-8)
- Try a different terminal emulator
- Ensure your terminal font includes the required Unicode characters

### Encoding errors
- Input characters may not have a CP437 equivalent
- The client will fall back to the closest latin-1 equivalent
- Safe fallback to '?' for unmapped characters

## Resources

- [Telnetlib3 Documentation](https://telnetlib3.readthedocs.io/)
- [CP437 Wikipedia](https://en.wikipedia.org/wiki/Code_page_437)
- [Unicode Character Database](https://www.unicode.org/unidata/)
- [C Version Documentation](README_C.md)
- [C Implementation Details](C_IMPLEMENTATION.md)

## Author

Your Name (@yourusername)

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.
