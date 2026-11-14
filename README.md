# ChatGPT Watermark Remover

**Free browser-based tool: https://www.textwipes.com/tools/clean-chatgpt-text**

Paste text copied out of ChatGPT, Claude, Gemini or DeepSeek and this tool strips the
invisible Unicode characters those models leave behind. Everything runs in your browser —
nothing is uploaded, nothing is stored, no account is required.

## What ChatGPT actually leaves behind

When you copy a reply out of a chat interface, the text you paste is rarely just the
letters you can see. These invisible code points ride along:

| Character | Codepoint | What it does |
|---|---|---|
| Zero-width space | U+200B | No width, breaks word recognition and search matching |
| Zero-width non-joiner | U+200C | Splits characters that should stay joined |
| Zero-width joiner | U+200D | Invisible, but keeps glyphs stuck together |
| Word joiner | U+2060 | Prevents line breaks at a spot that looks empty |
| Byte order mark | U+FEFF | Shows up mid-text and breaks parsers |
| Soft hyphen | U+00AD | Renders nothing until the line wraps, then shows a hyphen |
| Non-breaking space | U+00A0 | Looks like a space, is not a space |
| Narrow no-break space | U+202F | Same problem, narrower |
| Bidirectional controls | U+202A–U+202E, U+2066–U+2069 | Reorder characters invisibly |
| Unicode tag characters | U+E0000–U+E007F | Invisible payload channel, no visual trace |

Alongside those, AI text tends to carry a typographic fingerprint: curly quotes, em
dashes where a person would type a hyphen, and a handful of stock transitions. None of
it is visible on screen.

## Why it matters

- **Code breaks.** Invisible characters inside a code block cause linter errors that
  point at a line that looks perfectly fine, and syntax highlighters give up.
- **Git diffs go wrong.** A pasted file shows as hundreds of changed lines because the
  characters shifted, not the code.
- **Word and Google Docs reflow.** Non-breaking spaces make paragraphs refuse to wrap,
  and soft hyphens appear in the middle of words.
- **String matching fails.** `if title == "Report"` returns false because one of the two
  strings has a zero-width space in it, and no diff tool will tell you why.
- **Search and CMS filters misfire.** A pasted paragraph can trip a word filter or be
  flagged by a similarity checker over characters no human can see.

## How to clean your text

1. Open https://www.textwipes.com/tools/clean-chatgpt-text
2. Paste the text into the box (free up to 500 characters per run)
3. Hit **Wipe Text Clean** and copy the result

There is no upload step and no signup. For `.docx` files, the Pro plan cleans documents
in place without changing the wording.

## The same problem, one command

If you would rather fix files in a pipeline, this script does what the web tool does —
it drops every invisible format character and normalises the exotic spaces:

```python
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
    sys.stdout.write(clean(data))Find and remove invisible AI watermarks from ChatGPT, Claude and Gemini text.
