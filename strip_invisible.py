#!/usr/bin/env python3
"""Strip invisible Unicode characters that chat tools leave in copied text."""
import sys
import unicodedata

INVISIBLE = set("\u200b\u200c\u200d\u2060\ufeff\u00ad\u180e\u2061\u2062\u2063\u2064")
INVISIBLE |= {chr(c) for c in range(0x202A, 0x202F)}    # bidi embedding / override
INVISIBLE |= {chr(c) for c in range(0x2066, 0x206A)}    # bidi isolates
INVISIBLE |= {chr(c) for c in range(0xE0000, 0xE0080)}  # Unicode tag characters
SPACES = {"\u00a0": " ", "\u202f": " ", "\u2009": " ", "\u2007": " "}

def clean(text: str) -> str:
    kept = []
    for ch in text:
        if ch in INVISIBLE:
            continue
        if unicodedata.category(ch) == "Cf" and ch not in "\r\n\t":
            continue
        kept.append(SPACES.get(ch, ch))
    return "".join(kept)

if __name__ == "__main__":
    data = sys.stdin.read() if len(sys.argv) == 1 else open(sys.argv[1], encoding="utf-8").read()
    sys.stdout.write(clean(data))
