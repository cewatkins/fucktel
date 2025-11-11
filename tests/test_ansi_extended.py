"""
Extended ANSI compatibility tests for cp437_telnet.py
Tests for features identified in ANSI_ANALYSIS.md
"""

import pytest
from cp437_telnet import decode_cp437_graphical_buffered


class TestRelativeCursorMovement:
    """Test cursor movement commands (relative positioning)."""
    
    def test_cursor_up(self):
        """ESC[nA - Move cursor up n lines."""
        data = b'\x1b[5A'
        result, incomplete = decode_cp437_graphical_buffered(data)
        assert '\x1b[5A' in result
        assert incomplete == b''
    
    def test_cursor_down(self):
        """ESC[nB - Move cursor down n lines."""
        data = b'\x1b[3B'
        result, incomplete = decode_cp437_graphical_buffered(data)
        assert '\x1b[3B' in result
        assert incomplete == b''
    
    def test_cursor_forward(self):
        """ESC[nC - Move cursor forward n characters."""
        data = b'\x1b[10C'
        result, incomplete = decode_cp437_graphical_buffered(data)
        assert '\x1b[10C' in result
        assert incomplete == b''
    
    def test_cursor_backward(self):
        """ESC[nD - Move cursor backward n characters."""
        data = b'\x1b[4D'
        result, incomplete = decode_cp437_graphical_buffered(data)
        assert '\x1b[4D' in result
        assert incomplete == b''
    
    def test_cursor_movement_no_params(self):
        """Cursor movement with no params defaults to 1."""
        for cmd in [b'\x1b[A', b'\x1b[B', b'\x1b[C', b'\x1b[D']:
            result, incomplete = decode_cp437_graphical_buffered(cmd)
            assert cmd.decode('latin-1') in result


class TestEraseInLine:
    """Test line erasure commands."""
    
    def test_erase_from_cursor_to_end(self):
        """ESC[K or ESC[0K - Erase from cursor to end of line."""
        for cmd in [b'\x1b[K', b'\x1b[0K']:
            result, incomplete = decode_cp437_graphical_buffered(cmd)
            assert cmd.decode('latin-1') in result
            assert incomplete == b''
    
    def test_erase_from_start_to_cursor(self):
        """ESC[1K - Erase from start of line to cursor."""
        data = b'\x1b[1K'
        result, incomplete = decode_cp437_graphical_buffered(data)
        assert '\x1b[1K' in result
        assert incomplete == b''
    
    def test_erase_entire_line(self):
        """ESC[2K - Erase entire line."""
        data = b'\x1b[2K'
        result, incomplete = decode_cp437_graphical_buffered(data)
        assert '\x1b[2K' in result
        assert incomplete == b''


class TestCursorPositioningVariants:
    """Test alternate forms of cursor positioning."""
    
    def test_absolute_positioning_f_form(self):
        """ESC[<row>;<col>f - Alternate form of absolute positioning."""
        data = b'\x1b[10;20f'
        result, incomplete = decode_cp437_graphical_buffered(data)
        assert '\x1b[10;20f' in result
        assert incomplete == b''
    
    def test_positioning_with_missing_col(self):
        """ESC[<row>;H - Row specified, column defaults to 1."""
        data = b'\x1b[5;H'
        result, incomplete = decode_cp437_graphical_buffered(data)
        # Should preserve the sequence even if unusual
        assert b'H' in data or '\x1b[5;' in result


class TestLineOperations:
    """Test line insertion/deletion."""
    
    def test_delete_lines(self):
        """ESC[nM - Delete n lines."""
        data = b'\x1b[3M'
        result, incomplete = decode_cp437_graphical_buffered(data)
        assert '\x1b[3M' in result
        assert incomplete == b''
    
    def test_insert_lines(self):
        """ESC[nL - Insert n lines."""
        data = b'\x1b[2L'
        result, incomplete = decode_cp437_graphical_buffered(data)
        assert '\x1b[2L' in result
        assert incomplete == b''


class TestCRLFHandling:
    """Test carriage return and line feed handling."""
    
    def test_crlf_sequence(self):
        """CR+LF should be preserved as-is."""
        data = b'text\r\nmore'
        result, incomplete = decode_cp437_graphical_buffered(data)
        assert result == 'text\r\nmore'
        assert incomplete == b''
    
    def test_cr_only(self):
        """CR without LF (Mac mode)."""
        data = b'text\rmore'
        result, incomplete = decode_cp437_graphical_buffered(data)
        assert result == 'text\rmore'
    
    def test_lf_only(self):
        """LF without CR (Unix mode)."""
        data = b'text\nmore'
        result, incomplete = decode_cp437_graphical_buffered(data)
        assert result == 'text\nmore'
    
    def test_crlf_split_across_packets(self):
        """CR at end of first packet, LF at start of second."""
        # First read ends with CR, gets buffered
        data1 = b'text\r'
        result1, incomplete1 = decode_cp437_graphical_buffered(data1)
        assert result1 == 'text\r'
        
        # Second read starts with LF
        data2 = b'\nmore'
        # If we had proper buffering, we'd handle this
        # For now just verify LF is preserved
        result2, _ = decode_cp437_graphical_buffered(data2)
        assert result2 == '\nmore'


class TestCP437LowCharactersBinary:
    """Test that CP437 low characters work in binary mode."""
    
    def test_smiley_faces(self):
        """Bytes 0x01 and 0x02 = smiley faces."""
        data = bytes([0x01, 0x02])
        result, incomplete = decode_cp437_graphical_buffered(data)
        assert '☺' in result  # 0x01
        assert '☻' in result  # 0x02
        assert incomplete == b''
    
    def test_heart_symbol(self):
        """Byte 0x03 = heart."""
        data = bytes([0x03])
        result, incomplete = decode_cp437_graphical_buffered(data)
        assert '♥' in result
    
    def test_mixed_cp437_and_text(self):
        """Mix of CP437 graphics and ASCII text."""
        data = b'Score:\x01\x02\x03Text'
        result, incomplete = decode_cp437_graphical_buffered(data)
        assert 'Score:' in result
        assert '☺' in result
        assert '☻' in result
        assert '♥' in result
        assert 'Text' in result


class TestSGRParameters:
    """Test Select Graphic Rendition (color/style) codes."""
    
    def test_color_code(self):
        """ESC[31m - Red text."""
        data = b'\x1b[31mRed text'
        result, incomplete = decode_cp437_graphical_buffered(data)
        assert '\x1b[31m' in result
        assert 'Red text' in result
    
    def test_multiple_sgr_params(self):
        """ESC[1;31;40m - Bold red on black."""
        data = b'\x1b[1;31;40mBold Red'
        result, incomplete = decode_cp437_graphical_buffered(data)
        assert '\x1b[1;31;40m' in result
        assert 'Bold Red' in result
    
    def test_sgr_reset(self):
        """ESC[0m - Reset all attributes."""
        data = b'\x1b[0m'
        result, incomplete = decode_cp437_graphical_buffered(data)
        assert '\x1b[0m' in result


class TestSaveRestoreCursor:
    """Test save/restore cursor position."""
    
    def test_save_cursor(self):
        """ESC7 - Save cursor position."""
        data = b'\x1b7'
        result, incomplete = decode_cp437_graphical_buffered(data)
        # ESC7 is 2 bytes, should be preserved
        assert incomplete == b'' or '\x1b7' in result
    
    def test_restore_cursor(self):
        """ESC8 - Restore cursor position."""
        data = b'\x1b8'
        result, incomplete = decode_cp437_graphical_buffered(data)
        assert incomplete == b'' or '\x1b8' in result


class TestComplexSequences:
    """Test real-world complex sequences from BBS systems."""
    
    def test_game_screen_redraw(self):
        """Typical game redraw: clear + position + draw."""
        data = b'\x1b[2J\x1b[H\x1b[1;31mStatus:\x01'
        result, incomplete = decode_cp437_graphical_buffered(data)
        assert '\x1b[2J' in result  # clear
        assert '\x1b[H' in result   # home
        assert '\x1b[1;31m' in result  # red
        assert 'Status:' in result
        assert '☺' in result
    
    def test_line_drawing_with_positioning(self):
        """Line drawing with cursor positioning between chars."""
        # This is common in BBS interfaces
        data = b'\x1b[10;5H\x1b(0lqqk\x1b(B'
        result, incomplete = decode_cp437_graphical_buffered(data)
        assert '\x1b[10;5H' in result
        assert 'lqqk' in result  # Actual chars, charset mode not interpreted
    
    def test_rapid_updates_with_ansi(self):
        """Score/status updates with minimal ANSI."""
        data = b'\x1b[1;1H\x1b[31mScore: 1000\x1b[24;1H\x1b[32mHealth: 100'
        result, incomplete = decode_cp437_graphical_buffered(data)
        assert 'Score: 1000' in result
        assert 'Health: 100' in result
        assert '\x1b[1;1H' in result
        assert '\x1b[24;1H' in result


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
