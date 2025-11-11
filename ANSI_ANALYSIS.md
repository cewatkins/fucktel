# ANSI Compatibility Analysis for fucktel

## Executive Summary
The current ANSI implementation handles basic CSI sequences but has gaps in:
1. **CR/LF handling** - Mixed CR/LF modes not fully supported
2. **Cursor positioning edge cases** - Some absolute positioning forms missing
3. **Binary/8-bit sequences** - Not all control bytes preserved correctly
4. **Extended ANSI features** - Limited SGR (Select Graphic Rendition) support

---

## 1. CURRENT ANSI SEQUENCE SUPPORT

### ✅ IMPLEMENTED
- **CSI sequences** (ESC[...): Color, cursor movement, screen clear
  - Format: `ESC [ <params> <command>`
  - Terminators: Letters A-Z, a-z (@-~)
  - Examples: `ESC[2J` (clear), `ESC[1;1H` (home), `ESC[31m` (red)

- **OSC sequences** (ESC]...): Operating System Command
  - Format: `ESC ] <text> <terminator>`
  - Terminators: BEL (0x07) or ESC\ (0x1B\)
  - Example: `ESC]0;Title BEL`

- **Character set selection** (ESC(...): Graphics mode
  - Formats: `ESC(0`, `ESC)A`, `ESC*U`, `ESC+B`
  - Enables line drawing characters

- **CP437 low ASCII graphical** (0x01-0x1F, 0x7F)
  - Currently mapped but may have binary encoding issues

### ⚠️ PARTIALLY IMPLEMENTED
- **Cursor positioning**:
  - ✅ `ESC[<row>;<col>H` - Absolute positioning
  - ✅ `ESC[H` - Home (cursor to 0,0)
  - ✅ `ESC[0;0H` - Home (alternate form)
  - ❌ `ESC[<row>;<col>f` - Absolute positioning (alternate form - NOT detected)
  - ❌ `ESC[<n>A` - Cursor up (relative)
  - ❌ `ESC[<n>B` - Cursor down (relative)
  - ❌ `ESC[<n>C` - Cursor forward (relative)
  - ❌ `ESC[<n>D` - Cursor backward (relative)
  - ❌ `ESC[<n>E` - Cursor to next line
  - ❌ `ESC[<n>F` - Cursor to previous line

- **Line drawing modes**:
  - ✅ Detected (ESC(0, etc.)
  - ❌ Not actively handled/preserved

### ❌ NOT IMPLEMENTED
- **Relative cursor movement** (most common in games)
- **SGR parameters** (colors, bold, etc.) - Passed through but not parsed
- **Save/restore cursor** (`ESC7`, `ESC8`)
- **Alternate screen buffer** (`ESC[?1049h/l`)
- **Mouse reporting** (`ESC[?1000h` etc.)
- **Window title** (OSC 0, 1, 2)
- **Delete/Insert lines** (`ESC[<n>M`, `ESC[<n>L`)
- **Erase in line** (`ESC[K`, `ESC[0K`, `ESC[1K`, `ESC[2K`)

---

## 2. CR/LF HANDLING ISSUES

### Current Behavior
- CR (0x0D) passed through as-is
- LF (0x0A) passed through as-is
- No special handling for different line ending modes

### Problems
1. **Unix mode (LF only)**: Works correctly
2. **DOS mode (CR+LF)**: 
   - When received as separate packets, cursor may move incorrectly
   - Terminal may interpret CR+LF as move-to-column + newline
   - Could cause 2-character offset if packets split between CR and LF

3. **Mac mode (CR only)**: 
   - Moves cursor to column 0 but doesn't advance line
   - Server may rely on this behavior

### Root Cause
Telnetlib3 may normalize line endings before we see them, or packets may fragment between CR and LF.

### Recommended Fix
```python
# Option A: Preserve exact sequence
# Don't modify CR/LF - pass through as-is (current behavior, but may need buffering)

# Option B: Normalize to LF + cursor home
# Convert CR to newline, add cursor positioning

# Option C: Binary mode passthrough
# Ensure bytes are NOT interpreted as text by terminal
```

---

## 3. BINARY/8-BIT DATA ISSUES

### Current Issues
1. **CP437 low characters** (0x01-0x1F):
   - Mapped to Unicode symbols ✅
   - But terminal may interpret raw bytes as control codes before we decode them
   - Need to ensure they arrive as binary, not text

2. **Encoding layer**:
   - Using `encoding='latin-1', force_binary=True` in telnetlib3 ✅
   - But Python's stdout may interpret 0x0D/0x0A as line endings

3. **Output handling**:
   - `sys.stdout.write(decoded)` may convert `\r` → `\r\n` on Windows/text mode
   - Need binary output channel for true 8-bit data

---

## 4. CURSOR POSITIONING EDGE CASES

### Missing Forms
```
Current recognizes:  ESC[<row>;<col>H
Should also handle:  
  - ESC[<row>;<col>f  (alternate form)
  - ESC[;<col>H       (row defaults to 1)
  - ESC[<row>;H       (col defaults to 1)
  - ESC[H             (no params = home to 0,0)
```

### Relative Movement Not Detected
```
Missing patterns:
  ESC[<n>A - cursor up n lines
  ESC[<n>B - cursor down n lines  
  ESC[<n>C - cursor forward n chars
  ESC[<n>D - cursor backward n chars
```

### Line Operations Not Implemented
```
Missing patterns:
  ESC[<n>M - delete n lines
  ESC[<n>L - insert n lines
  ESC[K    - erase line from cursor to end
  ESC[0K   - erase from cursor to end
  ESC[1K   - erase from start to cursor
  ESC[2K   - erase entire line
```

---

## 5. SGR (COLOR/FORMATTING) HANDLING

### Current Status
- Sequences like `ESC[31m` (red) are detected and passed through
- But parameters are not parsed/validated
- Terminal interprets them (works by accident)

### Potential Issues
- Malformed SGR codes might break sequence detection
- Multiple parameters: `ESC[1;31;40m` (bold red on black) 
  - Correctly detected (0x40-0x7E range includes 'm')
  - But we're not validating parameters

---

## 6. INCOMPLETE SEQUENCE BUFFERING

### Current Implementation
- Buffers incomplete sequences across read() calls ✅
- Maximum 100 bytes for CSI sequences
- Maximum 200 bytes for OSC sequences
- Works for typical cases

### Potential Issues
- Very long OSC sequences (e.g., 24-bit RGB palette changes) might exceed limits
- Some edge cases with charset sequences (ESC(...) may not buffer correctly

### Code Location
Lines 125-150 in cp437_telnet.py - handles ESC detection and buffering

---

## 7. RECOMMENDED PRIORITY FIXES

### HIGH PRIORITY (Affects display correctness)
1. **Add relative cursor movement** (ESC[nA/B/C/D)
   - Impact: Game graphics with fine cursor control
   - Effort: Low - just add 4 new sequence patterns

2. **Add erase-in-line** (ESC[K variants)
   - Impact: Clearing partial lines before drawing
   - Effort: Low - detect and pass-through

3. **Ensure binary output mode**
   - Impact: CP437 low bytes not interpreted as control codes
   - Effort: Medium - may need os.write() instead of sys.stdout

4. **Fix CR/LF handling**
   - Impact: Line offsets during rapid updates
   - Effort: Medium - need packet buffering for CR+LF pairs

### MEDIUM PRIORITY (Enhanced compatibility)
5. Add save/restore cursor (ESC7, ESC8)
6. Add delete/insert lines (ESC[nM, ESC[nL)
7. Add alternate screen buffer (ESC[?1049h/l)

### LOW PRIORITY (Nice-to-have)
8. SGR parameter validation
9. Mouse reporting support
10. Window title handling

---

## 8. TESTING RECOMMENDATIONS

### Test Cases to Add
```python
# Test relative cursor movement
def test_cursor_up():
    data = b'\x1b[5A'  # Move up 5 lines
    result, _ = decode_cp437_graphical_buffered(data)
    assert '\x1b[5A' in result

# Test erase line
def test_erase_line():
    data = b'\x1b[2K'  # Erase entire line
    result, _ = decode_cp437_graphical_buffered(data)
    assert '\x1b[2K' in result

# Test CR/LF handling
def test_crlf_sequence():
    data = b'text\r\nmore'
    result, _ = decode_cp437_graphical_buffered(data)
    assert result == 'text\r\nmore'

# Test CP437 low chars with binary
def test_cp437_low_binary():
    data = bytes([0x01, 0x02, 0x03])  # Smiley faces
    result, _ = decode_cp437_graphical_buffered(data)
    assert '☺' in result
    assert '☻' in result
```

---

## 9. IMPLEMENTATION ROADMAP

### Phase 1: Relative Cursor Movement (1 hour)
Add detection for ESC[nA, ESC[nB, ESC[nC, ESC[nD in decode_cp437_graphical_buffered()

### Phase 2: Erase Commands (30 min)
Add detection for ESC[K variants

### Phase 3: Binary Output (2 hours)
- Switch sys.stdout.write() to os.write() for binary channel
- Test CP437 low bytes aren't eaten by terminal

### Phase 4: CR/LF Buffering (2 hours)
- Detect CR+LF pairs across packet boundaries
- Ensure proper cursor positioning

### Phase 5: Advanced Features (Optional)
- Save/restore cursor
- Line operations
- Alternate screen

---

## 10. CODE CHANGES NEEDED

### File: cp437_telnet.py

#### Change 1: Extend CSI sequence detection (Lines ~130)
```python
# After checking for normal CSI terminator (0x40-0x7E)
# Add specific handling for movement and erase commands
if remaining[1:2] == b'[':
    # Existing code handles generic CSI...
    # Add specific checks for:
    # - 0x41-0x44 (A/B/C/D) = cursor movement
    # - 0x4B (K) = erase in line
    # - 0x4D/0x4C (M/L) = delete/insert lines
```

#### Change 2: Binary output mode (Lines ~368)
```python
# Current: sys.stdout.write(decoded)
# Change to: os.write(sys.stdout.fileno(), decoded.encode('utf-8'))
```

#### Change 3: CR/LF detection (Lines ~365)
```python
# Before writing, check for incomplete CR at end of buffer
# If ends with \r and next read would give \n, buffer the \r
```

---

## Summary Table

| Feature | Status | Impact | Effort |
|---------|--------|--------|--------|
| CSI Basic | ✅ | High | Done |
| Cursor absolute | ✅ | High | Done |
| Cursor relative | ❌ | High | 1hr |
| Erase line | ❌ | Medium | 0.5hr |
| Save/restore cursor | ❌ | Medium | 1hr |
| Line operations | ❌ | Low | 1.5hr |
| Binary output | ⚠️ | High | 2hr |
| CR/LF handling | ⚠️ | Medium | 2hr |
| SGR parsing | ⚠️ | Low | 1hr |
| Mouse support | ❌ | Low | 2hr |

