#!/usr/bin/env python3
"""
CP437 Translation Helper - Provides CP437 encoding/decoding functions.

This module sets up CP437 graphical character support and makes it available
in an interactive Python shell for testing telnetlib3 connections.

Usage:
    python3 cp437_translator.py
    Then use decode_cp437() and encode_cp437() functions in the shell.
"""

import asyncio
import sys

# Dynamically build CP437 graphical map (standard + low symbol overrides)
raw = bytes(range(256))
standard_decoded = raw.decode("cp437")
graphical_low = {
    0x01: "\u263a",  # ☺
    0x02: "\u263b",  # ☻
    0x03: "\u2665",  # ♥
    0x04: "\u2666",  # ♦
    0x05: "\u2663",  # ♣
    0x06: "\u2660",  # ♠
    0x07: "\u2022",  # •
    0x08: "\u25d8",  # ◘
    0x09: "\u25cb",  # ○ (TAB)
    0x0A: "\u25d9",  # ▹ (LF)
    0x0B: "\u2642",  # ♂
    0x0C: "\u2640",  # ♀
    0x0D: "\u266a",  # ♪ (CR)
    0x0E: "\u25ba",  # ►
    0x0F: "\u25c4",  # ◄
    0x10: "\u2195",  # ↕
    0x11: "\u203c",  # ‼
    0x12: "\u00b6",  # ¶
    0x13: "\u00a7",  # §
    0x14: "\u25ac",  # ▬
    0x15: "\u21a8",  # ↨
    0x16: "\u2191",  # ↑
    0x17: "\u2193",  # ↓
    0x18: "\u2192",  # →
    0x19: "\u2190",  # ←
    0x1A: "\u221f",  # ∟
    0x1B: "\u2194",  # ↔
    0x1C: "\u25b2",  # ▲
    0x1D: "\u25bc",  # ▼
    0x1E: "\u2320",  # ⌠
    0x1F: "\u2321",  # ⌡
    0x7F: "\u2302",  # ⌂
}

CP437_MAP = {}
for i in range(256):
    if i in graphical_low:
        CP437_MAP[i] = graphical_low[i]
    else:
        CP437_MAP[i] = standard_decoded[i]

# Inverse map for encoding (Unicode to CP437; first match wins)
UNICODE_TO_CP437 = {}
for k, v in CP437_MAP.items():
    if v not in UNICODE_TO_CP437:
        UNICODE_TO_CP437[v] = k


def decode_cp437(data: bytes) -> str:
    """Decode CP437 bytes to Unicode string with graphical characters."""
    if isinstance(data, str):
        return data
    return "".join(CP437_MAP.get(b, "?") for b in data)


def encode_cp437(text: str) -> bytes:
    """Encode Unicode string to CP437 bytes."""
    if isinstance(text, bytes):
        return text
    result = bytearray()
    for char in text:
        if char in UNICODE_TO_CP437:
            result.append(UNICODE_TO_CP437[char])
        else:
            try:
                result.append(char.encode("latin-1")[0])
            except Exception:
                result.append(ord("?"))  # Safe fallback
    return bytes(result)


def print_cp437(data: bytes) -> None:
    """Print CP437 bytes as decoded Unicode."""
    print(decode_cp437(data))


def show_cp437_map() -> None:
    """Display the CP437 character mapping."""
    print("\nCP437 Graphical Character Map:")
    print("=" * 60)
    print(f"{'Byte':<8} {'Char':<6} {'Unicode':<12} {'Description':<20}")
    print("-" * 60)

    mappings = [
        (0x01, "Smiley Face"),
        (0x02, "Reverse Smiley"),
        (0x03, "Heart"),
        (0x04, "Diamond"),
        (0x05, "Club"),
        (0x06, "Spade"),
        (0x07, "Bullet"),
        (0x08, "Inverse Bullet"),
        (0x09, "Hollow Circle"),
        (0x0A, "Inverse Circle"),
        (0x0B, "Male Symbol"),
        (0x0C, "Female Symbol"),
        (0x0D, "Musical Note"),
        (0x0E, "Play/Right Triangle"),
        (0x0F, "Pause/Left Triangle"),
        (0x10, "Up/Down Arrows"),
        (0x11, "Double Exclamation"),
        (0x12, "Pilcrow"),
        (0x13, "Section Sign"),
        (0x14, "Horizontal Bar"),
        (0x15, "Up/Down Arrow Tall"),
        (0x16, "Up Arrow"),
        (0x17, "Down Arrow"),
        (0x18, "Right Arrow"),
        (0x19, "Left Arrow"),
        (0x1A, "Right Angle"),
        (0x1B, "Left/Right Arrow"),
        (0x1C, "Up Triangle"),
        (0x1D, "Down Triangle"),
        (0x1E, "Top Half Integral"),
        (0x1F, "Bottom Half Integral"),
        (0x7F, "House Symbol"),
    ]

    for byte_val, desc in mappings:
        char = CP437_MAP[byte_val]
        unicode_val = f"U+{ord(char):04X}"
        print(f"0x{byte_val:02X}     {char:<6} {unicode_val:<12} {desc:<20}")
    print("=" * 60)


def test_roundtrip(text: str) -> bool:
    """Test encoding/decoding roundtrip."""
    encoded = encode_cp437(text)
    decoded = decode_cp437(encoded)
    match = text == decoded
    print(f"Original:  {text}")
    print(f"Encoded:   {encoded}")
    print(f"Decoded:   {decoded}")
    print(f"Match:     {match} ✓" if match else f"Match:     {match} ✗")
    return match


async def test_bbs_connection(host: str = "lol.ddial.com", port: int = 2300):
    """Test CP437 translation with actual BBS connection."""
    import telnetlib3

    print(f"\nConnecting to {host}:{port}...")
    print("=" * 60)

    try:
        reader, writer = await telnetlib3.open_connection(
            host, port, force_binary=True
        )

        # Read initial server message
        print("Reading initial server response...")
        data = await asyncio.wait_for(reader.read(2048), timeout=2.0)
        decoded = decode_cp437(data)
        print("\nServer Response (decoded from CP437):")
        print("-" * 60)
        print(decoded)
        print("-" * 60)

        # Send test command (telnetlib3 expects strings, not bytes)
        test_cmd = "l"
        print(f"\nSending command: {repr(test_cmd)}")
        print(f"Encoded as CP437: {encode_cp437(test_cmd)}")
        writer.write(test_cmd + "\r\n")
        await writer.drain()

        # Read response
        print("\nWaiting for server response...")
        data = await asyncio.wait_for(reader.read(2048), timeout=2.0)
        decoded = decode_cp437(data)
        print("\nServer Response (decoded from CP437):")
        print("-" * 60)
        print(decoded)
        print("-" * 60)

        # Disconnect
        writer.close()
        await writer.wait_closed()
        print("\n✓ Connection test completed successfully!")

    except asyncio.TimeoutError:
        print("✗ Timeout waiting for server response")
    except Exception as e:
        print(f"✗ Connection error: {e}")


def run_bbs_test():
    """Run the BBS connection test in event loop."""
    import asyncio

    print("\n╔════════════════════════════════════════════════════════════════╗")
    print("║         CP437 BBS Connection Test - lol.ddial.com            ║")
    print("╚════════════════════════════════════════════════════════════════╝")

    try:
        asyncio.run(test_bbs_connection())
    except KeyboardInterrupt:
        print("\n✗ Test interrupted by user")


if __name__ == "__main__":
    import code

    banner = """
╔════════════════════════════════════════════════════════════════╗
║          CP437 Translation Helper - Interactive Shell          ║
╚════════════════════════════════════════════════════════════════╝

Available functions:
  • decode_cp437(data)       - Convert CP437 bytes to Unicode string
  • encode_cp437(text)       - Convert Unicode string to CP437 bytes
  • print_cp437(data)        - Print CP437 bytes as Unicode
  • show_cp437_map()         - Display CP437 character mapping
  • test_roundtrip(text)     - Test encoding/decoding roundtrip
  • run_bbs_test()           - Test connection to lol.ddial.com BBS

Available variables:
  • CP437_MAP                - Complete CP437 character mapping (256 chars)
  • UNICODE_TO_CP437         - Reverse mapping (Unicode → CP437 byte)

Quick test examples:
  >>> decode_cp437(b'\\x01\\x02\\x03')  # ☺☻♥
  >>> encode_cp437('Hello ☺')
  >>> test_roundtrip('Test♥♦♣♠')
  >>> show_cp437_map()
  >>> run_bbs_test()          # Test actual BBS connection!

Interactive telnetlib3 example:
  >>> import asyncio
  >>> async def connect():
  ...     import telnetlib3
  ...     reader, writer = await telnetlib3.open_connection(
  ...         'lol.ddial.com', 2300, force_binary=True)
  ...     data = await reader.read(1024)
  ...     print(decode_cp437(data))
  ...     writer.close()
  >>> asyncio.run(connect())

Type 'exit()' or Ctrl-D to quit.
"""

    # Start interactive shell with available functions
    local_vars = {
        "decode_cp437": decode_cp437,
        "encode_cp437": encode_cp437,
        "print_cp437": print_cp437,
        "show_cp437_map": show_cp437_map,
        "test_roundtrip": test_roundtrip,
        "run_bbs_test": run_bbs_test,
        "CP437_MAP": CP437_MAP,
        "UNICODE_TO_CP437": UNICODE_TO_CP437,
        "telnetlib3": __import__("telnetlib3"),
        "asyncio": __import__("asyncio"),
    }

    code.interact(banner=banner, local=local_vars)
