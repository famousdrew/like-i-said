#!/usr/bin/env python3
"""check_quotes: find quotes in a voice bible that are not in the source material.

    python3 check_quotes.py voice-bible.md SOURCES...

SOURCES are the files or folders the bible was built from: the interview, the
edit pairs and the writing samples. Every quoted passage in the bible should
appear in them word for word. This lists the ones that do not, so they can be
corrected or removed. Lines that start with a cross mark are skipped, because
those examples are invented on purpose. Headings and "never uses" lists are
skipped too.

Exit code 0 means every quote was found. Exit code 1 means some were not.
Standard library only. Python 3.8 or newer.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

TEXT_SUFFIXES = {".md", ".markdown", ".txt", ".text"}

# Quoted words that belong to the template's own wording, not to the writer.
# Stored the way check() sees them: lowercase, with edge punctuation trimmed.
# A bible's own section names and bold labels are skipped automatically.
TEMPLATE_PHRASES = {"est", "fix"}
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(?:\d+\.\s*)?(.*)$")
BOLD_LABEL = re.compile(r"\*\*(.+?)\*\*")
CODE_SPAN = re.compile(r"`[^`]*`")
INVENTED = re.compile(r"^\s*(?:[-*+]\s+)?(?:❌|✗|✘|✖)")
# Headings name patterns, and "never uses" lists name words that are absent by design.
NOT_QUOTING = re.compile(r"^\s{0,3}#{1,6}\s|never uses?\b", re.I)
QUOTED = re.compile(r'"([^"\n]{2,}?)"')
BLOCKQUOTE = re.compile(r"^\s{0,3}>\s?(.*)$")
PLACEHOLDER = re.compile(r"^\[.*\]$")
ELISION = re.compile(r"\s*(?:\.{3,}|\[\.\.\.\]|\[…\])\s*")


def normalize(text: str) -> str:
    """Flatten the differences that do not change what was said."""
    text = (text.replace("’", "'").replace("‘", "'")
            .replace("“", '"').replace("”", '"').replace("…", "..."))
    text = re.sub(r"(\*\*|__|(?<!\w)[*_]|[*_](?!\w)|`)", "", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def trim(quote: str) -> str:
    return quote.strip().strip(".,;:!?").strip()


def collect(paths: "list[str]") -> "list[Path]":
    files: "list[Path]" = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            files += sorted(p for p in path.rglob("*")
                            if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES)
        elif path.is_file():
            files.append(path)
        else:
            raise SystemExit("Not found: %s" % raw)
    return files


def quotes_in(bible: str) -> "list[tuple[int, str]]":
    """Every quoted passage worth checking, with its line number."""
    found: "list[tuple[int, str]]" = []
    block: "list[str]" = []
    block_start = 0

    def flush() -> None:
        text = " ".join(block).strip()
        block.clear()
        if text and not QUOTED.search(text):
            found.append((block_start, text))

    for number, line in enumerate(bible.split("\n"), 1):
        quote_line = BLOCKQUOTE.match(line)
        if quote_line and quote_line.group(1).strip():
            if not block:
                block_start = number
            block.append(quote_line.group(1).strip())
        else:
            flush()
        if INVENTED.match(line) or NOT_QUOTING.search(line):
            continue
        for match in QUOTED.finditer(line.replace("“", '"').replace("”", '"')):
            found.append((number, match.group(1)))
    flush()
    return [(number, quote) for number, quote in found if re.search(r"\w", quote)]


def missing_parts(quote: str, haystack: str) -> "list[str]":
    """The pieces of a quote that are not in the sources. Empty means it was found."""
    quote = quote.replace("…", "...")
    whole = normalize(trim(quote))
    if not whole or whole in haystack:
        return []
    # A quote may skip over words with an ellipsis, so check each stretch on its own.
    parts = [normalize(trim(p)) for p in ELISION.split(quote)]
    return [p for p in parts if p and p not in haystack]


def own_labels(bible: str) -> "set[str]":
    """The bible's section names and bold labels, which it may refer to in quotes."""
    labels = set()
    for line in bible.split("\n"):
        line = CODE_SPAN.sub("", line)
        heading = HEADING.match(line)
        found = [heading.group(1)] if heading else BOLD_LABEL.findall(line)
        labels.update(normalize(trim(text)) for text in found)
    return labels - {""}


def is_quote_of_writer(quote: str, labels: "set[str]") -> bool:
    cleaned = normalize(trim(quote))
    return not (cleaned in TEMPLATE_PHRASES or cleaned in labels or PLACEHOLDER.match(quote.strip()))


def check(bible: str, sources: str) -> "list[tuple[int, str, list[str]]]":
    haystack = normalize(sources)
    labels = own_labels(bible)
    problems = []
    for number, quote in quotes_in(bible):
        if not is_quote_of_writer(quote, labels):
            continue
        missing = missing_parts(quote, haystack)
        if missing:
            problems.append((number, quote, missing))
    return problems


def main(argv: "list[str] | None" = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) < 2 or args[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if args and args[0] in ("-h", "--help") else 2
    bible_path = Path(args[0])
    if not bible_path.is_file():
        raise SystemExit("Not found: %s" % args[0])
    bible = bible_path.read_text(encoding="utf-8", errors="replace")
    files = [p for p in collect(args[1:]) if p.resolve() != bible_path.resolve()]
    if not files:
        raise SystemExit("No source files found in: %s" % ", ".join(args[1:]))
    sources = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in files)
    labels = own_labels(bible)
    total = len([q for _, q in quotes_in(bible) if is_quote_of_writer(q, labels)])
    problems = check(bible, sources)
    print("Checked %d quoted passages against %d source file%s." % (
        total, len(files), "" if len(files) == 1 else "s"))
    if not problems:
        print("All of them appear word for word in the sources.")
        return 0
    print("%d not found word for word. Copy the real text, or remove them:" % len(problems))
    for number, quote, missing in problems:
        print('\nline %d: "%s"' % (number, quote if len(quote) <= 160 else quote[:157] + "..."))
        if [normalize(trim(quote))] != missing:
            for part in missing:
                print('    missing part: "%s"' % part)
    return 1


if __name__ == "__main__":
    sys.exit(main())
