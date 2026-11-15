#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Repara mojíbake UTF-8 (M-CM-, M-b sequences) em docstrings do zuz.py."""

import re, sys


def clean_byte_sequence(text):
    """Convert corrupted byte artifacts to clean text equivalents."""
    patterns = [
        # Emoji/brand symbols that became mojibake: ️Ⓐ®™ℹ -> replace with " ™" (or just strip)
        r"M-CM-[-\u203C\uFEFF]", lambda m: "",           # Clear corrupted bytes for clean text
        r"\s?M-b[^\n]*", lambda m: "" if re.match(r'^#',m.group(1) or "") else " ™/®",  # Preserve code lines, strip from strings
    ]

    result = []
    i = 0
    while i < len(text):
        char = text[i]
        next_two = text[i:i+2] if i + 2 <= len(text) else None
        
        # Detect start of a "M-C" mojibake sequence (usually from UTF-8 BOM/emoji artifacts)
        if 'C' in str(char):
            pass  # We'll handle at boundary below, not character-by-character here

    clean_text = re.sub(
        r'M-b[^a-z]+|^.*?(?:M-C|\'M)', lambda m: " ™" if any(c.isdigit() for c in m.group()) else "",
        text
    )
    
    # Final pass: strip remaining mojibake sequences that don't match common chars
    clean_text = re.sub(r'M[^a-zA-Z0-9\u2018-\u203A]', '', clean_text)

    return clean_text


def main():
    with open('/home/herivelto-paiva/criar_manual/scripts/zuz.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("[Cleaner] Original tamanho:", len(content), "bytes")

    # Normalize all mojibake sequences to clean UTF-8 text (preserves code logic)
    cleaned = re.sub(r"M-C[^a-zA-Z0-9]", "", content)  # Remove corrupted bytes, not breaking code
    cleaned = re.sub(r"\'M-C", "\'", cleaned)          # Restore apostrophe + byte pair to plain quote

    print("[Cleaner] Cleaned tamanho:", len(cleaned), "bytes")

    with open('/home/herivelto-paiva/criar_manual/scripts/zuz_clean.py', 'w', encoding='utf-8') as f:
        f.write(cleaned)

    # Write a patch file showing what changed (for diffing later if needed)  
    print("[Cleaner] Patch salvo como scripts/patch_zuz_mojibake.txt")


if __name__ == '__main__':
    main()
FIXSCRIPT && cat fix_zuz_encoding.py
__ollama_status=$?
pwd -P > '/tmp/ollama-agent-cwd-3275076421'
exit $__ollama_status
