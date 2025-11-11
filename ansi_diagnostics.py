#!/usr/bin/env python3
"""
ANSI Compatibility Diagnostic Tool
Analyzes telnet session logs for ANSI sequence issues.
"""

import re
import sys
from collections import defaultdict
from typing import Dict, List, Tuple

class ANSIDiagnostics:
    """Analyze ANSI sequences in logged data."""
    
    def __init__(self, log_file: str):
        self.log_file = log_file
        self.sequences = []
        self.issues = []
        self.stats = defaultdict(int)
    
    def parse_log(self):
        """Parse log file and extract ANSI sequences."""
        try:
            with open(self.log_file, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading log: {e}")
            return
        
        # Find all ANSI sequences
        # CSI sequences: ESC [ ... (letter)
        csi_pattern = r'\x1b\[([^a-zA-Z]*)[a-zA-Z]'
        self.sequences.extend(re.finditer(csi_pattern, content))
        
        # OSC sequences: ESC ] ... (BEL or ESC\)
        osc_pattern = r'\x1b\]([^\x07\x1b]*?)(?:\x07|\x1b\\)'
        self.sequences.extend(re.finditer(osc_pattern, content))
        
        # Charset sequences: ESC ( or ESC ) ... 
        charset_pattern = r'\x1b[\(\)\*\+].'
        self.sequences.extend(re.finditer(charset_pattern, content))
        
        print(f"Found {len(self.sequences)} ANSI sequences")
        
        # Analyze sequence types
        self._analyze_sequences(content)
        self._check_issues(content)
    
    def _analyze_sequences(self, content: str):
        """Analyze types and frequency of sequences."""
        cursor_moves = re.findall(r'\x1b\[[0-9;]*[ABCDEF]', content)
        cursor_pos = re.findall(r'\x1b\[[0-9;]*[Hf]', content)
        clear_screen = re.findall(r'\x1b\[2J', content)
        erase_line = re.findall(r'\x1b\[[0-2]?K', content)
        colors = re.findall(r'\x1b\[[0-9;]*m', content)
        
        self.stats['Relative cursor moves'] = len(cursor_moves)
        self.stats['Absolute positioning'] = len(cursor_pos)
        self.stats['Clear screen'] = len(clear_screen)
        self.stats['Erase line'] = len(erase_line)
        self.stats['Color/SGR'] = len(colors)
    
    def _check_issues(self, content: str):
        """Check for common issues."""
        # Issue 1: CR followed by non-LF
        cr_not_lf = re.findall(r'\r(?![\n\x1b])', content)
        if cr_not_lf:
            self.issues.append(f"Found {len(cr_not_lf)} CR not followed by LF or ESC")
        
        # Issue 2: Incomplete sequences at packet boundaries
        incomplete_csi = re.findall(r'\x1b\[([0-9;]*?)$', content, re.MULTILINE)
        if incomplete_csi:
            self.issues.append(f"Found {len(incomplete_csi)} potentially incomplete CSI sequences")
        
        # Issue 3: Text immediately after control codes (no space)
        control_then_text = re.findall(r'[\x1b\r\n][a-zA-Z]', content)
        if control_then_text:
            self.issues.append(f"Found {len(control_then_text)} control chars directly followed by letters")
        
        # Issue 4: Orphaned ESC characters
        orphaned_esc = re.findall(r'\x1b(?![\[\(\)\]\*\+\x07])', content)
        if orphaned_esc:
            self.issues.append(f"Found {len(orphaned_esc)} orphaned ESC characters")
    
    def print_report(self):
        """Print diagnostic report."""
        print("\n" + "="*60)
        print("ANSI DIAGNOSTICS REPORT")
        print("="*60)
        
        if not self.sequences:
            print("No ANSI sequences found in log")
            return
        
        print("\nSequence Statistics:")
        for seq_type, count in sorted(self.stats.items(), key=lambda x: -x[1]):
            print(f"  {seq_type:.<40} {count:>5}")
        
        if self.issues:
            print("\n⚠️  Issues Found:")
            for issue in self.issues:
                print(f"  - {issue}")
        else:
            print("\n✓ No issues found")
        
        print("\n" + "="*60)


class CursorTracker:
    """Track cursor position changes throughout a session."""
    
    def __init__(self, log_file: str, width: int = 80, height: int = 24):
        self.log_file = log_file
        self.width = width
        self.height = height
        self.x = 1
        self.y = 1
        self.jumps = []
        self.movements = []
    
    def analyze(self):
        """Analyze cursor movements in log."""
        try:
            with open(self.log_file, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading log: {e}")
            return
        
        # Track cursor positioning
        pos_pattern = r'\x1b\[(\d+)?(?:;(\d+))?[Hf]'
        for match in re.finditer(pos_pattern, content):
            row = int(match.group(1)) if match.group(1) else 1
            col = int(match.group(2)) if match.group(2) else 1
            
            # Check if this is a huge jump
            distance = abs((row - self.y) * self.width + (col - self.x))
            if distance > 100:
                self.jumps.append({
                    'from': (self.y, self.x),
                    'to': (row, col),
                    'distance': distance
                })
            
            self.x = col
            self.y = row
        
        # Check for erratic movements
        self._check_patterns(content)
    
    def _check_patterns(self, content: str):
        """Check for suspicious movement patterns."""
        # Pattern: Multiple positioning in close sequence
        rapid_pos = re.findall(r'(?:\x1b\[[0-9;]*[Hf]){3,}', content)
        if rapid_pos:
            print(f"⚠️  Found {len(rapid_pos)} instances of 3+ rapid cursor positions")
        
        # Pattern: Cursor moved, then LF (instead of newline + position)
        pos_then_lf = re.findall(r'\x1b\[[0-9;]*[Hf]\x0a', content)
        if pos_then_lf:
            print(f"ℹ️  Found {len(pos_then_lf)} instances of positioning followed by LF (may be intentional)")
    
    def print_report(self):
        """Print cursor tracking report."""
        print("\n" + "="*60)
        print("CURSOR TRACKING REPORT")
        print("="*60)
        
        if not self.jumps:
            print("No large cursor jumps detected")
        else:
            print(f"Large cursor jumps: {len(self.jumps)}")
            for i, jump in enumerate(self.jumps[:5]):  # Show first 5
                print(f"  Jump {i+1}: ({jump['from'][0]},{jump['from'][1]}) → ({jump['to'][0]},{jump['to'][1]}) [distance: {jump['distance']}]")
        
        print("\n" + "="*60)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ansi_diagnostics.py <log_file> [--cursor]")
        sys.exit(1)
    
    log_file = sys.argv[1]
    
    print(f"Analyzing: {log_file}\n")
    
    # Run ANSI diagnostics
    ansi = ANSIDiagnostics(log_file)
    ansi.parse_log()
    ansi.print_report()
    
    # Run cursor tracking if requested
    if '--cursor' in sys.argv:
        tracker = CursorTracker(log_file)
        tracker.analyze()
        tracker.print_report()


if __name__ == '__main__':
    main()
