#!/usr/bin/env python3
"""
Example usage of CP437 Telnet Client
Run individual examples to test functionality
"""

# Example 1: Test CP437 decoding
print("=" * 60)
print("Example 1: CP437 Decoding")
print("=" * 60)

from cp437_telnet import decode_cp437_graphical

# Create some CP437 bytes
cp437_data = bytes([
    0x01,  # ☺
    0x02,  # ☻
    0x03,  # ♥
    0x04,  # ♦
    0x05,  # ♣
    0x06,  # ♠
])

decoded = decode_cp437_graphical(cp437_data)
print(f"Input bytes:  {cp437_data}")
print(f"Decoded text: {decoded}")
print()

# Example 2: Test CP437 encoding
print("=" * 60)
print("Example 2: CP437 Encoding")
print("=" * 60)

from cp437_telnet import encode_to_cp437

text = "Hello ☺ World ♥"
encoded = encode_to_cp437(text)
print(f"Input text:   {text}")
print(f"Encoded bytes: {encoded}")
print()

# Example 3: Roundtrip test
print("=" * 60)
print("Example 3: Encoding/Decoding Roundtrip")
print("=" * 60)

test_string = "Test☺♥♦"
encoded = encode_to_cp437(test_string)
decoded = decode_cp437_graphical(encoded)
print(f"Original:     {test_string}")
print(f"Encoded:      {encoded}")
print(f"Decoded:      {decoded}")
print(f"Match:        {test_string == decoded}")
print()

# Example 4: Display all CP437 special characters
print("=" * 60)
print("Example 4: All CP437 Special Characters")
print("=" * 60)

from cp437_telnet import CP437_MAP

special_chars = range(0x01, 0x20)  # 0x01 to 0x1F (low ASCII)
print("Low ASCII special characters (0x01-0x1F):")
for i in special_chars:
    print(f"  0x{i:02X}: {CP437_MAP[i]}", end="  ")
    if (i - 0x00) % 4 == 0:
        print()
print()

print("High special character (0x7F - house symbol):")
print(f"  0x7F: {CP437_MAP[0x7F]}")
print()

# Example 5: Create ASCII art preview
print("=" * 60)
print("Example 5: ASCII Art with CP437 Characters")
print("=" * 60)

art = """
╭────────────────────────────────────╮
│  CP437 Telnet Client              │
│  ☺ Retro BBS Support ♥           │
│  ► Full Character Coverage ◄       │
│  ↑ Modern Unicode Display ↓        │
╰────────────────────────────────────╯
"""
print(art)
print()

# Example 6: Comparison table
print("=" * 60)
print("Example 6: Character Mapping Reference")
print("=" * 60)

mappings = [
    (0x01, "Smiley Face"),
    (0x02, "Reverse Smiley"),
    (0x03, "Heart"),
    (0x04, "Diamond"),
    (0x05, "Club"),
    (0x06, "Spade"),
    (0x0E, "Play/Triangle Right"),
    (0x0F, "Pause/Triangle Left"),
    (0x10, "Up/Down Arrows"),
    (0x18, "Right Arrow"),
    (0x19, "Left Arrow"),
    (0x1C, "Up Triangle"),
    (0x1D, "Down Triangle"),
    (0x7F, "House"),
]

print(f"{'Byte':<8} {'Char':<6} {'Description':<30}")
print("-" * 50)
for byte_val, desc in mappings:
    char = CP437_MAP[byte_val]
    print(f"0x{byte_val:02X}    {char:<6} {desc:<30}")
print()

print("=" * 60)
print("Examples completed successfully!")
print("=" * 60)
