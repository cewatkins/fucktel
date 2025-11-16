# ANSI Rendering Compliance - Quick Reference

## What fucktel Does RIGHT ✅

### 1. CP437 Codepage Support
- Full 256-character CP437 codepage (IBM PC standard)
- Low ASCII graphics preserved (0x01-0x1F, 0x7F → Unicode symbols)
- Proper roundtrip encoding/decoding

### 2. Binary Protocol Handling
- Uses `force_binary=True` in telnetlib3
- Prevents telnet protocol layer from modifying CP437 bytes
- Character at 0x01 stays as graphics, not interpreted as SOH control

### 3. ANSI Escape Sequences
- ✅ CSI sequences (ESC[...color, cursor, erase)
- ✅ OSC sequences (ESC]...for system commands)
- ✅ Character set selection (ESC(0, ESC)B, etc.)
- ✅ Cursor movement (absolute and relative)
- ✅ Screen operations (clear, erase line, insert/delete line)
- ✅ Save/restore cursor position

### 4. Sequence Buffering
- Incomplete ANSI sequences properly buffered across TCP packets
- CSI: up to 100 bytes, OSC: up to 200 bytes
- CR+LF pairs split across packets handled correctly

### 5. Robustness
- Defensive sequence handling (no crashes on malformed input)
- Auto-fix: Adds `ESC[H` after `ESC[2J` when missing
- Graceful fallback for unknown sequences

### 6. Terminal Negotiation
- Sends proper terminal size (NAWS negotiation)
- Safely ignores TTYPE to avoid server crashes
- Waits for server to process before displaying

---

## What fucktel CAN'T Do (By Design)

### 1. Pixel Aspect Ratio Adjustment
**Why:** Terminal/OS/font responsibility, not protocol level
- CRT pixels: rectangular, 35% taller than modern
- Modern pixels: square (LCD era)
- **Workaround:** User selects font with appropriate aspect ratio

### 2. 9-Pixel Character Spacing
**Why:** Would corrupt output, terminal-specific
- Classic BBS hardware: 8px chars + 1px spacing = 9px wide
- Modern terminals: 8px chars, no auto-spacing
- **Impact:** Line-drawing characters may have gaps
- **Workaround:** Use retro-designed terminal fonts

### 3. Multiple Codepages
**Why:** Would require user input per session
- CP437: Full support (IBM PC USA standard)
- CP850: Not implemented (Western Europe variant, rarely used)
- **Workaround:** Most classic art uses CP437

### 4. Alternate Screen Buffer
**Why:** Rarely used in telnet BBS, adds complexity
- Not critical for BBS experience
- Could be added if needed

---

## Display Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Art looks "squashed" vertically | Modern square pixels vs. CRT rectangular pixels | Choose font with non-square aspect, check artwork date |
| Line-drawing gaps | No automatic 9px spacing | Use retro terminal font (e.g., "Perfect DOS VGA 437") |
| First line after clear at wrong position | Server bug (clears without homing) | fucktel auto-fixes this |
| Colors not working | Terminal doesn't support 16/256/RGB colors | Upgrade terminal or disable colors |
| Garbled text | CP850 or other codepage used | Check BBS system setup, use CP437 BBS |
| Split key sequences | Multiple servers, different expectations | Try `--ansi` or `--syncterm` flags |

---

## How to Use Properly

### Standard 80x24 BBS (Classic)
```bash
python fucktel.py bbs.example.com 23
```

### Custom Terminal Size
```bash
python fucktel.py bbs.example.com 23 --cols 120 --rows 40
```

### Use SyncTerm Key Mappings (Default)
```bash
python fucktel.py bbs.example.com 23 --syncterm
```

### Use ANSI Key Mappings
```bash
python fucktel.py bbs.example.com 23 --ansi
```

### With Session Logging
```bash
python fucktel.py bbs.example.com 23 --log session.log
```

### With Macro Support (Ctrl+G sends commands)
```bash
# vjkl = vim-style arrows for menu navigation
python fucktel.py bbs.example.com 23 --bell "vjkl"
```

---

## Terminal Requirements

**Minimum:**
- 256 colors (8-bit)
- Supports VT100/ANSI escape sequences
- Monospace font

**Recommended:**
- 256+ colors (ideally 24-bit RGB)
- Full VT100/ANSI/xterm support
- Monospace font designed for retro BBS (e.g., Terminus, IBM Plex Mono)
- Support for non-square pixel aspect ratio (optional)

**Tested Terminals:**
- ✅ Linux: xterm, GNOME Terminal, Konsole, Alacritty
- ✅ macOS: Terminal.app, iTerm2
- ✅ Windows: Windows Terminal, ConEmu (with proper fonts)

---

## For Authentic ANSI Art Rendering

1. **Check artwork date:**
   - Look for SAUCE metadata (especially post-2012 for font info)
   - Pre-2000: May need aspect adjustment
   - Post-2000: Standard square pixel layout

2. **Select appropriate font:**
   - Pre-2000 art: "Perfect DOS VGA 437", "Terminus", "IBM Plex Mono"
   - Post-2000 art: Any monospace font

3. **Connect with correct settings:**
   ```bash
   # Most classic: 80x24 default
   python fucktel.py bbs.example.com 23
   
   # If art looks cut off or wrapped wrong, adjust cols
   python fucktel.py bbs.example.com 23 --cols 80
   ```

4. **Compare with known renderers:**
   - If still wrong, test with 16c or similar viewer
   - Helps identify if issue is fucktel vs. your terminal/font

---

## Technical Compliance Details

| Standard | Compliance | Notes |
|----------|-----------|-------|
| CP437 Codepage | ✅ Full | IBM PC standard for BBS art |
| ANSI X3.64 (VT100) | ✅ Full | All critical sequences implemented |
| Telnet Protocol | ✅ Full | Binary mode, NAWS, safe TTYPE handling |
| RFC 854 (Telnet) | ✅ Full | Via telnetlib3 library |
| 16colo.rs principles | ✅ Full | As documented in ANSI_RENDERING_COMPLIANCE.md |

---

## Troubleshooting

### Issue: "Characters are garbled"
1. Check terminal encoding is UTF-8
2. Try different font
3. Verify BBS is CP437 (not CP850 or other)
4. Check terminal's 8-bit support

### Issue: "Colors don't work"
1. Set terminal to support 256 colors minimum
2. Some BBS need color negotiation (manual setting on BBS)
3. Try different terminal emulator

### Issue: "Art looks wrong vertically"
1. This is expected for pre-2000 art on modern monitors
2. Research artwork creation date
3. Try font with taller pixels (like DOS fonts)

### Issue: "Keys don't work"
1. Try `--ansi` or `--syncterm` flags
2. Check if BBS has special key mappings
3. Use `--bell` macro for common navigation

### Issue: "Crashes or hangs"
1. Report the BBS host
2. Enable logging: `--log crash.log`
3. Check if TTYPE issue (patched automatically)

---

## Key Compliance Points from 16colo.rs Discussion

✅ **Implemented:**
- CP437 codepage recognition and mapping
- Binary 8-bit data preservation
- ANSI escape sequence passthrough
- Recognition that terminal/font determines final appearance
- Document the limitations (aspect ratio, 9px spacing)

⚠️ **Acknowledged but Not Implemented:**
- Pixel aspect ratio adjustment (terminal/OS job)
- 9-pixel character spacing simulation (would corrupt)
- CP850 and other codepages (rare, would complicate)
- Alternate terminal type detection (auto-handled)

**Bottom Line:** fucktel handles the protocol and encoding correctly. Display quality depends on terminal, font, and OS rendering—exactly as the 16colo.rs discussion explains.

---

## Resources

- **16colo.rs:** https://16colo.rs (ANSI art database with rendering guidance)
- **CP437 Info:** https://en.wikipedia.org/wiki/Code_page_437
- **ANSI Escape:** https://en.wikipedia.org/wiki/ANSI_escape_code
- **SAUCE Metadata:** https://en.wikipedia.org/wiki/SAUCE_(file_format)
- **VT100 Sequences:** https://vt100.net/

---

**Last Updated:** November 15, 2025
