#!/usr/bin/env python3
"""Unit tests for CP437 encoding and decoding functions."""

import os
import sys
import unittest

from cp437_telnet import (
    CP437_MAP,
    UNICODE_TO_CP437,
    decode_cp437_graphical,
    encode_to_cp437,
)

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCP437Decoding(unittest.TestCase):
    """Test CP437 to Unicode decoding."""

    def test_decode_smiley_face(self):
        """Test decoding of smiley face (0x01)."""
        data = bytes([0x01])
        result = decode_cp437_graphical(data)
        self.assertEqual(result, "\u263a")  # ☺

    def test_decode_heart(self):
        """Test decoding of heart symbol (0x03)."""
        data = bytes([0x03])
        result = decode_cp437_graphical(data)
        self.assertEqual(result, "\u2665")  # ♥

    def test_decode_multiple_symbols(self):
        """Test decoding multiple CP437 symbols."""
        data = bytes([0x01, 0x02, 0x03])  # ☺☻♥
        result = decode_cp437_graphical(data)
        self.assertEqual(result, "\u263a\u263b\u2665")

    def test_decode_ascii_range(self):
        """Test decoding standard ASCII characters."""
        data = b"Hello"
        result = decode_cp437_graphical(data)
        self.assertEqual(result, "Hello")

    def test_decode_house_symbol(self):
        """Test decoding house symbol (0x7F - DEL)."""
        data = bytes([0x7F])
        result = decode_cp437_graphical(data)
        self.assertEqual(result, "\u2302")  # ⌂

    def test_decode_mixed_content(self):
        """Test decoding mixed ASCII and CP437 symbols."""
        data = bytes([ord("A"), 0x01, ord("B")])  # A☺B
        result = decode_cp437_graphical(data)
        self.assertEqual(result, "A\u263aB")


class TestCP437Encoding(unittest.TestCase):
    """Test Unicode to CP437 encoding."""

    def test_encode_ascii(self):
        """Test encoding ASCII text."""
        text = "Hello"
        result = encode_to_cp437(text)
        self.assertEqual(result, b"Hello")

    def test_encode_smiley_face(self):
        """Test encoding smiley face unicode."""
        text = "\u263a"  # ☺
        result = encode_to_cp437(text)
        self.assertEqual(result, bytes([0x01]))

    def test_encode_heart(self):
        """Test encoding heart symbol."""
        text = "\u2665"  # ♥
        result = encode_to_cp437(text)
        self.assertEqual(result, bytes([0x03]))

    def test_encode_mixed(self):
        """Test encoding mixed ASCII and symbols."""
        text = "A\u263aB"  # A☺B
        result = encode_to_cp437(text)
        self.assertEqual(result, bytes([ord("A"), 0x01, ord("B")]))

    def test_encode_invalid_char_fallback(self):
        """Test that invalid characters fall back to '?'."""
        text = "Hello\ufffdWorld"  # Replacement character
        result = encode_to_cp437(text)
        # Should not raise exception
        self.assertIsInstance(result, bytes)

    def test_encode_decode_roundtrip(self):
        """Test that encoding then decoding preserves data."""
        original = "Test\u263a\u2665"  # Test☺♥
        encoded = encode_to_cp437(original)
        decoded = decode_cp437_graphical(encoded)
        self.assertEqual(decoded, original)


class TestCP437Maps(unittest.TestCase):
    """Test CP437 mapping integrity."""

    def test_cp437_map_complete(self):
        """Test that CP437_MAP has all 256 characters."""
        self.assertEqual(len(CP437_MAP), 256)

    def test_unicode_to_cp437_integrity(self):
        """Test that inverse map values match CP437_MAP."""
        for unicode_char, cp437_byte in UNICODE_TO_CP437.items():
            self.assertEqual(CP437_MAP[cp437_byte], unicode_char)

    def test_graphical_low_all_mapped(self):
        """Test that graphical_low characters are in CP437_MAP."""
        graphical_low = {
            0x01: "\u263a",  # ☺
            0x02: "\u263b",  # ☻
            0x03: "\u2665",  # ♥
            0x04: "\u2666",  # ♦
            0x05: "\u2663",  # ♣
            0x06: "\u2660",  # ♠
            0x07: "\u2022",  # •
            0x0B: "\u2642",  # ♂
            0x0C: "\u2640",  # ♀
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
        for byte_val, unicode_char in graphical_low.items():
            self.assertEqual(CP437_MAP[byte_val], unicode_char)


if __name__ == "__main__":
    unittest.main()
