#!/usr/bin/env python3
"""
CP437 Telnet Client - Telnetlib3 client with CP437 graphical support.

This module provides a telnet client that properly decodes and displays
CP437 (Code Page 437) graphical characters, including low ASCII symbols
that are typically lost in standard UTF-8 telnet.
"""

import argparse
import asyncio
import codecs
import sys
import tty
import termios
import time
from datetime import datetime
from typing import Optional, Dict

import telnetlib3

# Patch telnetlib3 TTYPE handler to prevent crashes on problematic servers
# Some servers send malformed TTYPE subnegotiations that cause AssertionErrors
try:
    from telnetlib3.stream_writer import StreamWriter
    
    # Replace the problematic TTYPE handler with a no-op
    def _patched_handle_sb_ttype(self, buf):
        """Handle TTYPE subnegotiation safely by doing nothing."""
        # Don't process TTYPE at all - just ignore it
        pass
    
    StreamWriter._handle_sb_ttype = _patched_handle_sb_ttype
except Exception:
    pass  # If we can't patch, continue anyway

# Dynamically build CP437 graphical map (standard + low symbol overrides)
raw = bytes(range(256))
standard_decoded = raw.decode("cp437")
# Only override printable graphical characters from low ASCII range
# Include ALL low ASCII characters that have graphical representations in CP437
graphical_low = {
    0x01: "\u263a",  # ☺
    0x02: "\u263b",  # ☻
    0x03: "\u2665",  # ♥
    0x04: "\u2666",  # ♦
    0x05: "\u2663",  # ♣
    0x06: "\u2660",  # ♠
    0x07: "\u2022",  # •
    # 0x08: BS - keep as-is (backspace control)
    # 0x09: TAB - keep as-is (tab control)
    # 0x0A: LF - keep as-is (line feed control)
    0x0B: "\u2642",  # ♂
    0x0C: "\u2640",  # ♀
    # 0x0D: CR - keep as-is (carriage return control)
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


def decode_cp437_graphical(data: bytes) -> str:
    """Custom decoder: Maps CP437 bytes to graphical Unicode, preserving ANSI codes."""
    result, _ = decode_cp437_graphical_buffered(data)
    return result


def decode_cp437_graphical_buffered(data: bytes) -> tuple:
    """
    Custom decoder: Maps CP437 bytes to graphical Unicode, preserving ANSI codes.
    Returns (decoded_string, incomplete_sequence_bytes).
    Incomplete sequences are returned for buffering across read boundaries.
    """
    result = []
    incomplete = b''
    i = 0
    
    while i < len(data):
        byte = data[i]
        
        # Check for ANSI escape sequence FIRST (ESC = 0x1B)
        # This must be checked BEFORE we map 0x1B to a character
        if byte == 0x1B:
            # We found the start of a potential escape sequence
            # Check if we have enough data to complete it
            remaining = data[i:]
            
            if len(remaining) < 2:
                # Not enough data - buffer this for next read
                incomplete = remaining
                break
            
            found_sequence = False
            
            # Check for CSI sequence (ESC [)
            if remaining[1:2] == b'[':
                # Start of ANSI CSI sequence: ESC [
                # Find the end (letter in range @-~)
                j = 2
                found_terminator = False
                while j < len(remaining) and j < 100:
                    if 0x40 <= remaining[j] <= 0x7E:
                        found_terminator = True
                        break
                    j += 1
                
                if found_terminator:
                    # Complete sequence found
                    seq = remaining[0:j+1]
                    result.append(seq.decode('latin-1', errors='replace'))
                    i += j + 1
                    found_sequence = True
                else:
                    # Incomplete CSI sequence
                    if j >= 100:
                        # Sequence is too long, assume it's malformed and skip ESC
                        result.append(CP437_MAP.get(byte, '?'))
                        i += 1
                    else:
                        # Not enough data - buffer it
                        incomplete = remaining
                        break
            
            # Check for OSC sequences: ESC ] ... (terminated by BEL or ESC \)
            elif len(remaining) > 1 and remaining[1:2] == b']':
                j = 2
                found_terminator = False
                while j < len(remaining) and j < 200:
                    if remaining[j:j+1] == b'\x07':  # BEL terminator
                        result.append(remaining[0:j+1].decode('latin-1', errors='replace'))
                        i += j + 1
                        found_sequence = True
                        found_terminator = True
                        break
                    elif remaining[j:j+2] == b'\x1b\\':  # ESC \ terminator
                        result.append(remaining[0:j+2].decode('latin-1', errors='replace'))
                        i += j + 2
                        found_sequence = True
                        found_terminator = True
                        break
                    j += 1
                
                if not found_terminator:
                    if j >= 200:
                        # Sequence too long, skip ESC
                        result.append(CP437_MAP.get(byte, '?'))
                        i += 1
                    else:
                        # Not enough data - buffer it
                        incomplete = remaining
                        break
            
            # Check for character set sequences: ESC ( or ESC ) or ESC * or ESC +
            elif len(remaining) > 2 and remaining[1:2] in (b'(', b')', b'*', b'+'):
                if remaining[2:3] in b'0ABU':
                    result.append(remaining[0:3].decode('latin-1', errors='replace'))
                    i += 3
                    found_sequence = True
                else:
                    # Invalid charset sequence, skip ESC
                    result.append(CP437_MAP.get(byte, '?'))
                    i += 1
            
            # If we get here, ESC is not part of a recognized sequence
            if not found_sequence:
                # Check if we might be at the start of something incomplete
                if len(remaining) > 1 and remaining[1:2] in b'([)*+':
                    # Could be a charset sequence but incomplete
                    if len(remaining) < 3:
                        incomplete = remaining
                        break
                
                # Not a recognized sequence pattern, map ESC as CP437
                result.append(CP437_MAP.get(byte, '?'))
                i += 1
        
        elif byte in CP437_MAP:
            # Regular CP437 byte - decode using our map
            result.append(CP437_MAP[byte])
            i += 1
        else:
            # Unknown byte - use ? as fallback
            result.append('?')
            i += 1
    
    return "".join(result), incomplete


def encode_to_cp437(text: str) -> bytes:
    """Encode UTF-8 input back to CP437 (inverse map; latin-1 fallback)."""
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


# Register custom CP437 codec
class CP437Codec(codecs.Codec):
    """Custom CP437 codec that preserves graphical characters."""

    def encode(self, input_str: str, errors: str = "strict") -> tuple:
        return encode_to_cp437(input_str), len(input_str)

    def decode(self, input_bytes: bytes, errors: str = "strict") -> tuple:
        return decode_cp437_graphical(input_bytes), len(input_bytes)


class CP437IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input_str: str, final: bool = False) -> str:
        return encode_to_cp437(input_str).decode("latin-1", errors="replace")


class CP437IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input_bytes: bytes, final: bool = False) -> str:
        return decode_cp437_graphical(input_bytes)


def cp437_codec_info(name: str) -> codecs.CodecInfo:
    return codecs.CodecInfo(
        name="cp437_graphical",
        encode=CP437Codec().encode,
        decode=CP437Codec().decode,
        incrementalencoder=CP437IncrementalEncoder,
        incrementaldecoder=CP437IncrementalDecoder,
    )


# Register the codec
codecs.register(lambda name: cp437_codec_info(name) if name == "cp437_graphical" else None)


class SessionLogger:
    """Logs telnet session to file."""
    
    def __init__(self, log_file: Optional[str] = None):
        self.log_file = log_file
        self.file_handle = None
        
        if log_file:
            self.file_handle = open(log_file, 'w', encoding='utf-8')
            self.log(f"=== Session started at {datetime.now().isoformat()} ===\n")
    
    def log(self, data: str):
        """Write data to log file."""
        if self.file_handle:
            self.file_handle.write(data)
            self.file_handle.flush()
    
    def close(self):
        """Close the log file."""
        if self.file_handle:
            self.log(f"\n=== Session ended at {datetime.now().isoformat()} ===\n")
            self.file_handle.close()


def parse_macro_keys(macro_text: str) -> list:
    """
    Parse macro text converting vim-style keys to escape sequences.
    - h -> left arrow (ESC[D)
    - j -> down arrow (ESC[B)
    - k -> up arrow (ESC[A)
    - l -> right arrow (ESC[C)
    All other characters passed through as-is.
    
    Returns list of strings/characters to send.
    """
    key_map = {
        'h': '\x1b[D',  # left arrow
        'j': '\x1b[B',  # down arrow
        'k': '\x1b[A',  # up arrow
        'l': '\x1b[C',  # right arrow
    }
    
    result = []
    for char in macro_text:
        if char in key_map:
            result.append(key_map[char])
        else:
            result.append(char)
    
    return result


async def graphical_shell(reader, writer, logger: Optional[SessionLogger] = None, bell_macro: Optional[str] = None):
    """Interactive shell with CP437 character support."""
    # Don't print anything - let the server's display be first
    # print("Connected! Type Ctrl+] to quit.\n")
    # if bell_macro:
    #     print("Bell macro available: Press Ctrl+G\n")
    
    # Save original terminal settings
    if sys.stdin.isatty():
        old_settings = termios.tcgetattr(sys.stdin.fileno())
    else:
        old_settings = None
    
    # Buffer for incomplete ANSI sequences between reads
    incomplete_seq = b''
    
    # Macro delay (configurable via global or args)
    macro_delay = getattr(graphical_shell, 'macro_delay', 0.01)
    
    # Get terminal size info if available
    term_cols = getattr(graphical_shell, 'term_cols', 80)
    term_rows = getattr(graphical_shell, 'term_rows', 24)
    
    try:
        # Set terminal to raw mode for character-by-character input
        if old_settings:
            tty.setraw(sys.stdin.fileno())
        
        async def server_reader():
            """Continuously read and display server output."""
            nonlocal incomplete_seq
            try:
                while True:
                    data = await reader.read(4096)
                    if not data:
                        return
                    
                    # Data comes as string (latin-1 decoded by telnetlib3)
                    # Convert back to bytes to decode as CP437
                    if isinstance(data, str):
                        data_bytes = data.encode('latin-1', errors='replace')
                    else:
                        data_bytes = data
                    
                    # Prepend any incomplete sequence from previous read
                    if incomplete_seq:
                        data_bytes = incomplete_seq + data_bytes
                        incomplete_seq = b''
                    
                    # Decode CP437 - will return incomplete_seq if needed
                    decoded, incomplete_seq = decode_cp437_graphical_buffered(data_bytes)
                    
                    # CRITICAL FIX: When server sends ESC[2J (clear screen) without following
                    # with ESC[H (home cursor), the cursor stays where it was.
                    # Many BBS systems don't send the home cursor after clear, causing first
                    # line to print on wrong line. We fix this by detecting ESC[2J and
                    # ensuring cursor is moved to home.
                    if '\x1b[2J' in decoded and '\x1b[H' not in decoded:
                        # Server cleared screen but didn't move cursor to home
                        # Add home cursor after clear
                        decoded = decoded.replace('\x1b[2J', '\x1b[2J\x1b[H', 1)
                    
                    sys.stdout.write(decoded)
                    # Force immediate flush after every write to prevent buffering issues
                    sys.stdout.flush()
                    
                    # Log to file if logger is active
                    if logger:
                        logger.log(decoded)
            except asyncio.CancelledError:
                pass
        
        async def stdin_reader():
            """Continuously read user input from stdin (character-by-character)."""
            try:
                loop = asyncio.get_event_loop()
                escape_char = "\x1d"  # Ctrl+]
                bell_char = "\x07"    # Ctrl+G (BEL)
                
                while True:
                    # Read one character at a time
                    char = await loop.run_in_executor(None, sys.stdin.read, 1)
                    if not char:
                        return
                    
                    # Check for escape character (Ctrl+])
                    if char == escape_char:
                        return
                    
                    # Check for bell macro trigger (Ctrl+G)
                    if char == bell_char and bell_macro:
                        # Parse macro to handle arrow keys (hjkl -> arrow sequences)
                        macro_keys = parse_macro_keys(bell_macro)
                        
                        # Send Ctrl+G first, then macro text with delays
                        writer.write(bell_char)
                        for key in macro_keys:
                            writer.write(key)
                            await asyncio.sleep(macro_delay)
                        if logger:
                            logger.log(f"[BELL MACRO]: {bell_macro}\n")
                    # Handle escape sequences from terminal (arrow keys, etc.)
                    elif char == '\x1b':  # ESC - start of escape sequence
                        # Read the next characters of the sequence with a short timeout
                        seq = char
                        is_escape_sequence = False
                        
                        # Try to read the next character with a timeout
                        try:
                            next_char = await asyncio.wait_for(
                                loop.run_in_executor(None, sys.stdin.read, 1),
                                timeout=0.05
                            )
                            
                            if next_char:
                                seq += next_char
                                # If it's CSI sequence (ESC[), read until terminator
                                if next_char == '[':
                                    is_escape_sequence = True
                                    for _ in range(10):
                                        term_char = await asyncio.wait_for(
                                            loop.run_in_executor(None, sys.stdin.read, 1),
                                            timeout=0.05
                                        )
                                        if not term_char:
                                            break
                                        seq += term_char
                                        # Check if this completes the sequence
                                        if 0x40 <= ord(term_char) <= 0x7E:
                                            break
                                else:
                                    # Other escape sequences (ESC O, ESC (, etc.)
                                    is_escape_sequence = True
                        except asyncio.TimeoutError:
                            # Standalone ESC
                            is_escape_sequence = False
                        
                        # Send the sequence (or standalone ESC) to the server
                        writer.write(seq)
                    else:
                        # Regular character - send to telnet server
                        writer.write(char)
                        # DON'T log or display what we send - let server echo handle it
                        # if logger:
                        #     logger.log(char)
            except (EOFError, asyncio.CancelledError):
                pass
        
        # Create and run both tasks concurrently
        server_task = asyncio.create_task(server_reader())
        stdin_task = asyncio.create_task(stdin_reader())
        
        try:
            # Wait for either task to complete
            done, pending = await asyncio.wait(
                [server_task, stdin_task],
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Cancel pending tasks
            for task in pending:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        except Exception:
            pass
        
        print("\nDisconnected.")
    
    finally:
        # Close logger
        if logger:
            logger.close()
        
        # Restore original terminal settings
        if old_settings:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old_settings)


async def main(host: str, port: Optional[int] = 23, log_file: Optional[str] = None, bell_macro: Optional[str] = None, macro_delay: float = 0.01, cols: int = 80, rows: int = 24):
    """Connect to telnet host and run graphical shell."""
    # Store macro_delay as a class attribute for use in graphical_shell
    graphical_shell.macro_delay = macro_delay
    graphical_shell.term_cols = cols
    graphical_shell.term_rows = rows
    
    # Create logger if requested
    logger = SessionLogger(log_file) if log_file else None
    
    try:
        # Get actual terminal size only if defaults were used (not explicitly specified)
        # If user specified --cols or --rows, respect those values
        import sys
        if '--cols' not in sys.argv and '--rows' not in sys.argv:
            try:
                import shutil
                term_size = shutil.get_terminal_size((cols, rows))
                cols, rows = term_size.columns, term_size.lines
            except Exception:
                pass
        
        graphical_shell.term_cols = cols
        graphical_shell.term_rows = rows
        
        # Disable TTYPE negotiation to avoid crashes on some servers
        reader, writer = await telnetlib3.open_connection(
            host,
            port,
            encoding='latin-1',  # 8-bit encoding
            force_binary=True,
            connect_minwait=0.0,  # Don't wait for telnet negotiation
        )
        
        # Send terminal size FIRST thing
        try:
            if hasattr(writer.protocol, 'request_naws'):
                await writer.protocol.request_naws(cols, rows)
        except Exception:
            pass
        
        # Wait longer for server to process size and settle before we start displaying
        await asyncio.sleep(0.8)
        
        # Clear telnetlib3's internal buffers to prevent negotiation data from appearing
        try:
            # telnetlib3 buffers data in the protocol object
            if hasattr(writer.protocol, '_stream'):
                # Try to clear the internal stream buffer
                writer.protocol._stream._buffer.clear()
        except Exception:
            pass
        
        # Drain any remaining buffered data
        drained_count = 0
        try:
            while drained_count < 10:  # Max 10 reads to prevent infinite loop
                data = await asyncio.wait_for(reader.read(4096), timeout=0.05)
                if not data:
                    break
                drained_count += 1
        except asyncio.TimeoutError:
            pass  # Expected - no more data
        
        # Clear the screen to wipe any negotiation artifacts before starting the shell
        try:
            sys.stdout.write('\x1b[2J')  # Clear screen
            sys.stdout.write('\x1b[H')   # Home cursor
            sys.stdout.flush()
        except Exception:
            pass
        
        # Run the graphical shell after connection is established
        await graphical_shell(reader, writer, logger=logger, bell_macro=bell_macro)
        await writer.protocol.waiter_closed
    finally:
        if logger:
            logger.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CP437 Telnet Client with full graphical character support"
    )
    parser.add_argument("host", help="Telnet host to connect to")
    parser.add_argument("port", type=int, nargs="?", default=23, help="Telnet port (default: 23)")
    parser.add_argument(
        "-l", "--log",
        dest="log_file",
        help="Log session to file (use timestamp if not specified)"
    )
    parser.add_argument(
        "--bell",
        dest="bell_macro",
        help="Macro text to send when Ctrl+G is pressed (sends Ctrl+G first, then text). Use h/j/k/l for left/down/up/right arrows"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.01,
        help="Delay between macro keystrokes in seconds (default: 0.01)"
    )
    parser.add_argument(
        "--cols",
        type=int,
        default=80,
        help="Terminal width to send to server (default: 80)"
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=24,
        help="Terminal height to send to server (default: 24)"
    )
    
    args = parser.parse_args()
    
    # Generate log filename if --log specified without value
    log_file = args.log_file
    if args.log_file == "":
        # Create timestamped log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"session_{timestamp}.log"
    
    try:
        asyncio.run(main(args.host, args.port, log_file=log_file, bell_macro=args.bell_macro, macro_delay=args.delay, cols=args.cols, rows=args.rows))
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
