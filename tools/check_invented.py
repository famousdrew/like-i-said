#!/usr/bin/env python3
"""check_invented: find specifics in a draft that are not in your notes.

    python3 check_invented.py DRAFT NOTES...

DRAFT is something an AI drafted for you. NOTES are what you gave it to work
from: your notes, a voice memo transcript, your interview, anything in your own
words. This lists every number, name and quotation in the draft that does not
appear in the notes, so you can see whether the AI made it up.

It is a rough filter. It takes a capital letter in the middle of a sentence as
the sign of a name, so it misses names typed in lowercase and it will sometimes
flag an ordinary capitalized word. A hit means "look at this line."

Exit code 0 means nothing was flagged. Exit code 1 means something was.
Standard library only. Python 3.8 or newer.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

TEXT_SUFFIXES = {".md", ".markdown", ".txt", ".text"}

UNITS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
         "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
         "eighteen", "nineteen", "twenty"]
TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
        "eighty": 80, "ninety": 90}
ORDINALS = {"third": 3, "fourth": 4, "fifth": 5, "sixth": 6, "seventh": 7, "eighth": 8,
            "ninth": 9, "tenth": 10, "eleventh": 11, "twelfth": 12, "twentieth": 20,
            "thirtieth": 30}
NUMBER_WORDS = dict({word: value for value, word in enumerate(UNITS)}, **TENS)
NUMBER_WORDS.update(ORDINALS)
# "One" and "two" are ordinary words far more often than they are figures, so a
# draft is only held to the number words from "three" up.
CHECKED_WORDS = {word for word, value in NUMBER_WORDS.items() if value >= 3}

DIGITS = re.compile(r"\$?(\d+(?:,\d{3})*(?:\.\d+)?)(?:%|(?:st|nd|rd|th)\b)?")
WORD_NUMBER = re.compile(r"\b([a-z]+)(?:-([a-z]+))?\b")
CAPITALIZED = re.compile(r"\b[A-Z][A-Za-z]*(?:'[A-Za-z]+)?(?:-[A-Z][A-Za-z]*)*\b")
QUOTED = re.compile(r'"([^"\n]{3,}?)"')
SENTENCE_START = re.compile(r'(?:^|[.!?:]["\')\]]*\s+|^\s*(?:[-*+>]|\d{1,3}[.)])\s+)["\'(\[]*$')
LIST_MARKER = re.compile(r"^\s*\d{1,3}[.)]\s+")
NEED = re.compile(r"\[NEED:[^\]]*\]", re.I)
FENCE = re.compile(r"^(```|~~~)")
NOT_NAMES = {"I", "OK", "Okay"}
# Ordinary words that often open a sentence just before a name ("As Marta said").
OPENERS = set("""
a about after all although an and any as at because before but by dear each every for from
he hello her here hi his how if in it last many most mr mrs ms my next no not now of on once
or our she since so some thanks that the their then there these they this those to we what
when where while who why with yes you your
""".split())


def normalize(text: str) -> str:
    return (text.replace("’", "'").replace("‘", "'").replace("“", '"')
            .replace("”", '"').replace("…", "..."))


def canonical(number: str) -> str:
    """'2,150', '$2150' and '2150.0' are the same figure."""
    number = number.replace(",", "")
    if "." in number:
        number = number.rstrip("0").rstrip(".")
    return number


def numbers_in(text: str, words_from: "set[str]") -> "list[tuple[str, str]]":
    """Figures in the text as (canonical value, as written)."""
    found = [(canonical(m.group(1)), m.group(0)) for m in DIGITS.finditer(text)]
    for match in WORD_NUMBER.finditer(text.lower()):
        first, second = match.group(1), match.group(2)
        if first in TENS and second in UNITS[1:10]:
            found.append((str(TENS[first] + UNITS.index(second)), match.group(0)))
        elif first in words_from and not second:
            found.append((str(NUMBER_WORDS[first]), match.group(0)))
    return found


def names_in(line: str) -> "list[str]":
    """Capitalized words that are not just the start of a sentence."""
    matches = list(CAPITALIZED.finditer(line))
    names = []
    for index, match in enumerate(matches):
        word = match.group(0)
        if word in NOT_NAMES or word.split("'")[0] in NOT_NAMES:
            continue
        starts_sentence = bool(SENTENCE_START.search(line[:match.start()]))
        following = matches[index + 1] if index + 1 < len(matches) else None
        part_of_a_name = following is not None and line[match.end():following.start()] == " "
        if starts_sentence and (not part_of_a_name or word.lower() in OPENERS):
            continue
        names.append(word)
    return names


def squash(text: str) -> str:
    text = re.sub(r"(\*\*|__|(?<!\w)[*_]|[*_](?!\w)|`)", "", normalize(text))
    return re.sub(r"\s+", " ", text).strip().strip(".,;:!?").lower()


def check(draft: str, notes: str) -> "list[tuple[int, str, str]]":
    """Each finding is (line number, kind, the text in question)."""
    notes = normalize(notes)
    known_numbers = {value for value, _ in numbers_in(notes, set(NUMBER_WORDS))}
    known_words = set(re.findall(r"[a-z0-9]+", notes.lower()))
    notes_flat = squash(notes)
    findings: "list[tuple[int, str, str]]" = []
    seen = set()
    in_code = False
    for number, raw in enumerate(normalize(draft).split("\n"), 1):
        if FENCE.match(raw.strip()):
            in_code = not in_code
            continue
        if in_code or raw.lstrip().startswith("#"):
            continue
        line = NEED.sub("", LIST_MARKER.sub("", raw))
        for match in QUOTED.finditer(line):
            quote = match.group(1)
            if len(quote.split()) >= 3 and squash(quote) not in notes_flat:
                findings.append((number, "quotation", quote))
        for value, written in numbers_in(line, CHECKED_WORDS):
            if value not in known_numbers and ("number", value) not in seen:
                seen.add(("number", value))
                findings.append((number, "number", written))
        for name in names_in(line):
            key = name.split("'")[0].lower()
            parts = [part for part in re.findall(r"[a-z0-9]+", key)]
            if any(part not in known_words for part in parts) and ("name", key) not in seen:
                seen.add(("name", key))
                findings.append((number, "name", name))
    return findings


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


def main(argv: "list[str] | None" = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) < 2 or args[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if args and args[0] in ("-h", "--help") else 2
    draft_path = Path(args[0])
    if not draft_path.is_file():
        raise SystemExit("Not found: %s" % args[0])
    files = [p for p in collect(args[1:]) if p.resolve() != draft_path.resolve()]
    if not files:
        raise SystemExit("No notes found in: %s" % ", ".join(args[1:]))
    draft = draft_path.read_text(encoding="utf-8", errors="replace")
    notes = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in files)
    findings = check(draft, notes)
    if not findings:
        print("Every number, name and quotation in the draft appears in your notes.")
        return 0
    print("%d thing%s in the draft that your notes do not contain. Check each one:" % (
        len(findings), "" if len(findings) == 1 else "s"))
    for number, kind, text in findings:
        shown = text if len(text) <= 120 else text[:117] + "..."
        print('  line %d, %s: %s' % (number, kind, shown))
    return 1


if __name__ == "__main__":
    sys.exit(main())
