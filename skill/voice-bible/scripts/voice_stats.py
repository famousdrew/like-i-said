#!/usr/bin/env python3
"""voice_stats: count the countable parts of a writing voice.

    python3 voice_stats.py SAMPLES...                   report on your own writing
    python3 voice_stats.py --compare DRAFT SAMPLES...   compare a draft with your writing

SAMPLES and DRAFT are .md or .txt files, or folders of them. Add --json for
machine-readable output. Standard library only. Python 3.8 or newer.

The numbers are approximate. Sentence splitting is rule-based and the tell
patterns are rough matches. Use them to decide where to look, not as a verdict.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

TEXT_SUFFIXES = {".md", ".markdown", ".txt", ".text"}
SHORT_SENTENCE = 5      # words or fewer
LONG_SENTENCE = 25      # words or more
VERY_LONG_SENTENCE = 35
FRAGMENT = 4            # words or fewer, for fragment clusters
SHORT_PIECE = 400       # words; a piece this short rarely needs headers
SMALL_SAMPLE = 1500     # words; below this the numbers are rough

# ---------------------------------------------------------------- cleaning

FRONT_MATTER = re.compile(r"\A---\n.*?\n---\n", re.S)
FENCE = re.compile(r"^(```|~~~)[^\n]*\n.*?^\1[^\n]*$", re.S | re.M)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
LINK = re.compile(r"\[([^\]]+)\]\([^)]*\)")
URL = re.compile(r"https?://\S+")
INLINE_CODE = re.compile(r"`([^`\n]*)`")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+\S")
RULE = re.compile(r"^\s{0,3}([-*_])(?:\s*\1){2,}\s*$")
BULLET = re.compile(r"^\s*(?:[-*+•]|\d{1,3}[.)])\s+")
TABLE = re.compile(r"^\s*\|.*\|\s*$")
QUOTE_MARK = re.compile(r"^\s{0,3}(?:>\s?)+")
BOLD = re.compile(r"(\*\*|__)(?=\S)(.+?)(?<=\S)\1")
ITALIC = re.compile(r"(?<![\w*_])([*_])(?=\S)([^*_\n]+?)(?<=\S)\1(?![\w*_])")
EMOJI = "[\U0001F300-\U0001FAFF☀-➿⬀-⯿]"
BOLD_LEAD = re.compile(
    r"^\s*(?:(?:[-*+•]|\d{1,3}[.)])\s+)?(\*\*|__)[^*_\n]{1,60}(?::\1|\1\s?:)"
)
EMOJI_LEAD = re.compile(r"^\s*(?:(?:[-*+•]|\d{1,3}[.)])\s+)?" + EMOJI)


def normalize(text: str) -> str:
    """Make quotes and ellipses uniform so the patterns below can stay simple."""
    return (
        text.replace("’", "'").replace("‘", "'")
        .replace("“", '"').replace("”", '"')
        .replace("…", "...").replace("\r\n", "\n")
    )


class Doc:
    """One file, split into prose paragraphs and list items, with markup counted."""

    def __init__(self, name: str, raw: str):
        self.name = name
        self.paragraphs: list[str] = []
        self.list_items: list[str] = []
        self.counts: Counter = Counter()
        self._parse(raw)

    def _inline(self, text: str) -> str:
        text = IMAGE.sub("", text)
        text = LINK.sub(r"\1", text)
        text = URL.sub("", text)
        text = INLINE_CODE.sub(r"\1", text)
        self.counts["bold"] += len(BOLD.findall(text))
        text = BOLD.sub(r"\2", text)
        self.counts["italic"] += len(ITALIC.findall(text))
        text = ITALIC.sub(r"\2", text)
        return re.sub(r"[ \t]+", " ", text).strip()

    def _parse(self, raw: str) -> None:
        text = normalize(raw)
        text = FRONT_MATTER.sub("", text)
        text = FENCE.sub("", text)
        text = HTML_COMMENT.sub("", text)
        current: list[str] = []
        in_list = False

        def flush() -> None:
            if current:
                block = self._inline(" ".join(current))
                if block:
                    self.paragraphs.append(block)
                current.clear()

        for line in text.split("\n"):
            if not line.strip():
                flush()
                in_list = False
                continue
            if RULE.match(line):
                flush()
                in_list = False
                continue
            if HEADING.match(line):
                flush()
                in_list = False
                self.counts["headings"] += 1
                continue
            if TABLE.match(line):
                flush()
                in_list = False
                self.counts["table_rows"] += 1
                continue
            line = QUOTE_MARK.sub("", line)
            if BOLD_LEAD.match(line):
                self.counts["bold_lead_in"] += 1
            if EMOJI_LEAD.match(line):
                self.counts["emoji_lead"] += 1
            if BULLET.match(line):
                flush()
                in_list = True
                self.counts["bullets"] += 1
                item = self._inline(BULLET.sub("", line, count=1))
                if item:
                    self.list_items.append(item)
                continue
            if in_list and self.list_items and line[:1] in " \t":
                self.list_items[-1] += " " + self._inline(line)
                continue
            in_list = False
            current.append(line.strip())
        flush()

    @property
    def text(self) -> str:
        return "\n".join(self.paragraphs + self.list_items)


# --------------------------------------------------------------- sentences

DOT = "\x00"   # a period that does not end a sentence
ELL = "\x01"   # an ellipsis
TITLES = re.compile(r"\b(Mr|Mrs|Ms|Dr|Prof|Sr|Jr|vs|Inc|Ltd)\.", re.I)
LATIN = re.compile(r"\b(e\.g|i\.e)\.", re.I)
SOFT_ABBREV = re.compile(r"\b(etc|a\.m|p\.m|U\.S|U\.K)\.(?=\s+[a-z]|[,;:)])")
DOTTED = re.compile(r"\b([A-Za-z])\.(?=[A-Za-z]\.)")
DECIMAL = re.compile(r"(?<=\d)\.(?=\d)")
SENT_END = re.compile(
    r"(?:[.!?]+|" + ELL + r"(?=[\"')\]]*\s+[\"'(\[]?[A-Z]))[\"')\]]*(?=\s|$)"
)
WORD = re.compile(r"\d[\d,]*(?:\.\d+)?%?|[A-Za-z0-9]+(?:'[A-Za-z]+)*(?:-[A-Za-z0-9]+(?:'[A-Za-z]+)*)*")


def split_sentences(paragraph: str) -> list[str]:
    text = re.sub(r"\.{3,}", ELL, paragraph)
    text = DECIMAL.sub(DOT, text)
    text = TITLES.sub(lambda m: m.group(1) + DOT, text)
    text = LATIN.sub(lambda m: m.group(1).replace(".", DOT) + DOT, text)
    text = SOFT_ABBREV.sub(lambda m: m.group(1).replace(".", DOT) + DOT, text)
    text = DOTTED.sub(lambda m: m.group(1) + DOT, text)
    out, start = [], 0
    for match in SENT_END.finditer(text):
        end = match.end()
        closer = match.group(0)[-1]
        rest = text[end:].lstrip()
        # '"Why?" he asked.' is one sentence: a closing quote followed by lowercase.
        if closer in "\"')" and rest[:1].islower() and not match.group(0).startswith("."):
            continue
        out.append(text[start:end])
        start = end
    out.append(text[start:])
    cleaned = []
    for sentence in out:
        sentence = sentence.replace(DOT, ".").replace(ELL, "...").strip()
        if WORD.search(sentence):
            cleaned.append(sentence)
    return cleaned


def words(text: str) -> list[str]:
    return WORD.findall(text)


# ------------------------------------------------------------- word habits

CONTRACTED = re.compile(
    r"\b(?:\w+n't|\w+'(?:re|ve|ll|d|m)|"
    r"(?:it|that|there|here|what|he|she|who|let|how|where|when|why)'s)\b", re.I)
EXPANDABLE = re.compile(
    r"\b(?:(?:do|does|did|is|are|was|were|would|could|should|have|has|had|will|must) not|"
    r"cannot|can not|I (?:am|will|have|would)|(?:it|that|there|here|what|he|she) is|"
    r"(?:you|we|they) (?:are|will|have|would)|let us)\b", re.I)
FIRST_SINGULAR = re.compile(r"\b(?:I|me|my|mine|myself)\b")
FIRST_SINGULAR_LOWER = re.compile(r"\b(?:i|me|my|mine|myself)\b")
FIRST_PLURAL = re.compile(r"\b(?:we|us|our|ours|ourselves)\b", re.I)
SECOND = re.compile(r"\b(?:you|your|yours|yourself|y'all)\b", re.I)
CONJUNCTION_OPENERS = {"and", "but", "so", "or", "because", "yet", "plus"}

PUNCTUATION = {
    "em_dash": re.compile(r"—|(?<=\w) ?-- ?(?=\w)"),
    "spaced_en_dash": re.compile(r"(?<=\S) – (?=\S)"),
    "spaced_hyphen": re.compile(r"(?<=\S) - (?=\S)"),
    "semicolon": re.compile(r";"),
    "colon": re.compile(r":(?=\s|$)", re.M),
    "ellipsis": re.compile(r"\.{3,}"),
    "exclamation": re.compile(r"!+"),
    "question": re.compile(r"\?+"),
    "parenthetical": re.compile(r"\([^()\n]*\w[^()\n]*\)"),
}
PUNCTUATION_LABELS = {
    "em_dash": "Em dashes (— or --)",
    "spaced_en_dash": "Spaced en dashes ( – )",
    "spaced_hyphen": "Spaced hyphens ( - )",
    "semicolon": "Semicolons",
    "colon": "Colons",
    "ellipsis": "Ellipses",
    "exclamation": "Exclamation points",
    "question": "Question marks",
    "parenthetical": "Parenthetical asides",
}

STOPWORDS = set("""
a about after again all also am an and any are as at be because been before being but by can
could did do does doing down each even for from had has have having he her here hers him his
how i if in into is it its just like may me might more most my no nor not now of off on once
one only or other our out over own same she should so some such than that the their them then
there these they this those through to too under until up us very was we were what when where
which while who whom why will with would you your it's i'm don't that's
""".split())

# ------------------------------------------------------------------ tells
# Keys match the ids in reference/ai-tells.md that are marked countable.


def _phrases(*alternatives: str, flags: int = re.I) -> "re.Pattern[str]":
    return re.compile(r"\b(?:" + "|".join(alternatives) + r")\b", flags)


START = r"(?:^|(?<=[.!?]\s)|(?<=[.!?][\"')]\s))"

PATTERN_TELLS = {
    "colon-reveal": re.compile(
        START + r"(?:(?:Here's|Here is|That's|This is) (?:the|my|what|where|why|how)\b[^.!?:\n]{0,40}"
        r"|(?:The|My) (?:result|catch|problem|truth|upshot|takeaway|bottom line|reality|answer|"
        r"lesson|point|kicker|twist|difference|good news|bad news|short version|short answer|"
        r"advice|verdict|fix|goal))\s*:", re.I | re.M),
    "not-x-but-y": re.compile(
        r"\bnot (?:just|only|merely|simply)\b[^.!?\n]{1,80}?[,;.]\s+(?:but|it's|it is|they're|that's)\b"
        r"|\b(?:isn't|is not|aren't|are not|wasn't|was not|it's not|that's not|this is not)\b"
        r"[^.!?\n]{1,70}[.,;]\s+(?:it|that|this|they)(?:'s|'re| is| are| was)\b"
        r"|\bnot because\b[^.!?\n]{1,80}\bbut because\b", re.I),
    "triplets": re.compile(
        r"\b(?:[\w'-]+ )?[\w'-]+, (?:[\w'-]+ ){0,2}[\w'-]+,? (?:and|or) (?:[\w'-]+ ){0,2}?[\w'-]+", re.I),
    "announcing": _phrases(
        r"let's dive in", r"let's dig in", r"dive into", r"here's the thing", r"here's the deal",
        r"let me be (?:honest|clear|real)", r"to be (?:honest|clear|fair)", r"i'll be honest",
        r"i want to be (?:honest|clear)", r"it's worth (?:noting|mentioning|remembering)",
        r"it is worth (?:noting|mentioning|remembering)", r"the truth is", r"the reality is",
        r"what nobody tells you", r"let that sink in", r"make no mistake", r"the bottom line is",
        r"at the end of the day", r"needless to say", r"it goes without saying"),
    "significance-tail": re.compile(
        r",\s+(?:highlighting|underscoring|emphasizing|reflecting|showcasing|demonstrating|"
        r"illustrating|signaling|cementing|reinforcing|ensuring|paving the way|"
        r"making (?:it|them|this))\b", re.I),
    "range-frames": re.compile(
        r"\bwhether you(?:'re| are)\b|" + START + r"From [^.,;!?\n]{2,40} to [^.,;!?\n]{2,40},",
        re.I | re.M),
    "hedge-stack": re.compile(
        r"\b(?:can|could|may|might)\s+(?:often|sometimes|potentially|possibly|perhaps|generally|typically)\b"
        r"|\b(?:often|sometimes|generally|typically)\s+(?:can|could|may|might)\b"
        r"|\bhelps? to potentially\b", re.I),
    "ai-vocabulary": _phrases(
        r"delv(?:e|es|ed|ing)", "tapestry", "realm", "testament", r"underscor(?:e|es|ed|ing)",
        "pivotal", "crucial", "robust", r"seamless(?:ly)?", r"leverag(?:e|es|ed|ing)",
        r"harness(?:es|ed|ing)?", r"unlock(?:s|ed|ing)?", r"elevat(?:e|es|ed|ing)",
        r"foster(?:s|ed|ing)?", "nuanced", "multifaceted", "intricate", "vibrant",
        r"meticulous(?:ly)?", "comprehensive", "holistic", r"streamlin(?:e|es|ed|ing)",
        r"empower(?:s|ed|ing|ment)?", "game-changer", "cutting-edge", "ever-evolving",
        "ever-changing", r"embark(?:s|ed|ing)?", r"showcas(?:e|es|ed|ing)",
        r"bolster(?:s|ed|ing)?", r"resonat(?:e|es|ed|ing)", "landscape",
        r"navigat(?:e|es|ed|ing)", "journey"),
    "stock-transitions": re.compile(
        START + r"(?:Moreover|Furthermore|Additionally|That said|In essence|Ultimately|At its core|"
        r"In conclusion|In summary|Overall|Notably|Importantly|Interestingly|Consequently|"
        r"When it comes to)\b|\bin today's [\w-]+(?: [\w-]+)? world\b", re.I | re.M),
    "sincerity-markers": _phrases(
        "truly", "genuinely", "incredibly", "deeply", "frankly",
        r"i(?:'m| am) (?:thrilled|excited|honored|humbled|delighted)",
        r"excited to (?:share|announce)"),
    "corporate-abstraction": _phrases(
        r"driv(?:e|es|ing) results", r"actionable insights?", r"best practices?", "value-add",
        r"stakeholders?", r"synerg(?:y|ies|istic)", "meaningful impact",
        r"thought leader(?:ship|s)?", "move the needle", "circle back", "deep dive",
        r"paradigm(?: shift)?", r"core competenc(?:y|ies)", "mission-critical", "best-in-class"),
    "stock-metaphor": _phrases(
        "symphony", "double-edged sword", "north star", "roadmap", "tip of the iceberg",
        "perfect storm", "secret sauce", "silver bullet", "rollercoaster", "game of chess"),
    "vague-authority": _phrases(
        r"studies (?:show|suggest|have shown)", r"research (?:shows|suggests|has shown)",
        r"experts (?:agree|say|suggest)", r"it is widely (?:known|accepted)",
        r"many (?:experts|people) (?:believe|say)"),
    "signposting": _phrases(
        r"in this (?:post|article|piece|guide|chapter|essay|section),? (?:we|i)(?:'ll| will)",
        r"let's break (?:it|this) down", r"let's (?:explore|unpack|take a (?:closer )?look)",
        r"here are (?:\d+|three|four|five|six|seven|ten|some|a few) "
        r"(?:ways|things|tips|reasons|steps|lessons|strategies)",
        r"we'll (?:explore|cover|look at)", r"read on to"),
    "moral-bow": re.compile(
        START + r"(?:In the end|When all is said and done)\b|\band that's okay\b"
        r"|\b(?:it's|it is|that's what it's) all about\b"
        r"|\bthat's the whole (?:point|game|thing|story|trick)\b", re.I | re.M),
    "toast-and-ask": re.compile(
        r"\b(?:here's to (?:the|all|every|those|you)|let me know in the comments"
        r"|i'd love to hear your (?:thoughts|take|story|stories)|drop a comment"
        r"|share your thoughts|let's keep (?:building|the conversation going))\b"
        r"|\bwhat do you think\?", re.I),
    "relentless-positivity": _phrases(
        "amazing", "incredible", "powerful", "exciting", "invaluable", "remarkable",
        "transformative", "game-changing", "revolutionary", "unparalleled", "exceptional"),
}

# Tells measured from the text's shape instead of matched as a phrase.
METRIC_TELLS = (
    "em-dash", "bold-lead-in", "structure-on-short", "emoji-markers", "fragment-recap",
    "chopped-pairs", "question-answer", "even-rhythm", "paragraph-capstone",
)
TELL_IDS = tuple(PATTERN_TELLS) + METRIC_TELLS

TELL_NAMES = {
    "em-dash": "Em dashes", "bold-lead-in": "Bold lead-in labels",
    "structure-on-short": "Headers or bullets on short pieces", "emoji-markers": "Emoji-led lines",
    "fragment-recap": "Fragment clusters", "chopped-pairs": "Very short sentences",
    "question-answer": "Question answered at once", "even-rhythm": "Even sentence rhythm",
    "paragraph-capstone": "Short capstone closing a paragraph", "colon-reveal": "Colon reveal",
    "not-x-but-y": "Negate, then restate", "triplets": "Lists of three",
    "announcing": "Announcing", "significance-tail": "Trailing significance clause",
    "range-frames": "Range frames", "hedge-stack": "Stacked hedges",
    "ai-vocabulary": "Familiar AI vocabulary", "stock-transitions": "Stock transitions",
    "sincerity-markers": "Sincerity markers", "corporate-abstraction": "Corporate abstraction",
    "stock-metaphor": "Stock metaphors", "vague-authority": "Authority with no source",
    "signposting": "Signposting", "moral-bow": "Moral or recap ending",
    "toast-and-ask": "Toast or comment request", "relentless-positivity": "Positivity words",
}


# --------------------------------------------------------------- analysis

def per_thousand(count: float, total_words: int) -> float:
    return round(count * 1000.0 / total_words, 2) if total_words else 0.0


def share(part: float, whole: float) -> float:
    return round(100.0 * part / whole, 1) if whole else 0.0


def snippet(text: str, start: int, end: int, width: int = 90) -> str:
    left = max(0, start - (width - (end - start)) // 2)
    piece = text[left:left + width].replace("\n", " ").strip()
    return ("..." if left > 0 else "") + piece + ("..." if left + width < len(text) else "")


def recurring_phrases(sentences: list[str], total_words: int, top: int) -> list[tuple[str, int]]:
    grams: Counter = Counter()
    for sentence in sentences:
        tokens = [w.lower() for w in words(sentence)]
        for size in (2, 3, 4):
            for i in range(len(tokens) - size + 1):
                gram = tokens[i:i + size]
                content = [w for w in gram if w not in STOPWORDS and not w[0].isdigit()]
                if not content or (size == 2 and len(content) < 2):
                    continue
                grams[" ".join(gram)] += 1
    floor = 3 if total_words >= 2500 else 2
    kept = [(g, c) for g, c in grams.items() if c >= floor]
    kept.sort(key=lambda gc: (-gc[1], -len(gc[0].split()), gc[0]))
    out: list[tuple[str, int]] = []
    for gram, count in kept:
        # Skip a phrase already covered by a longer or equal one we kept.
        if any(gram in other and count <= other_count for other, other_count in out):
            continue
        out = [(o, oc) for o, oc in out if not (o in gram and oc <= count)]
        out.append((gram, count))
    out.sort(key=lambda gc: (-gc[1], gc[0]))
    return out[:top]


def analyze(docs: list[Doc], top: int = 12) -> dict:
    paragraphs = [split_sentences(p) for d in docs for p in d.paragraphs]
    paragraphs = [p for p in paragraphs if p]
    sentences = [s for p in paragraphs for s in p]
    text = "\n".join(d.text for d in docs)
    all_words = words(text)
    n_words = len(all_words)
    counts: Counter = Counter()
    for d in docs:
        counts.update(d.counts)

    lengths = [len(words(s)) for s in sentences]
    n_sent = len(lengths)
    mean = statistics.mean(lengths) if lengths else 0.0
    spread = statistics.pstdev(lengths) if n_sent > 1 else 0.0

    clusters, cluster_examples = 0, []
    answered, answered_examples = 0, []
    capstones, eligible, capstone_examples = 0, 0, []
    for para in paragraphs:
        run: list[str] = []
        for sentence in para + [""]:
            if sentence and len(words(sentence)) <= FRAGMENT:
                run.append(sentence)
                continue
            if len(run) >= 3:
                clusters += 1
                cluster_examples.append(" ".join(run))
            run = []
        for first, second in zip(para, para[1:]):
            if (first.rstrip("\"')").endswith("?") and len(words(first)) <= 8
                    and len(words(second)) <= 8 and "?" not in second):
                answered += 1
                answered_examples.append(first + " " + second)
        if len(para) >= 3:
            eligible += 1
            if len(words(para[-1])) <= 6:
                capstones += 1
                capstone_examples.append(para[-1])

    punctuation = {}
    for key, pattern in PUNCTUATION.items():
        found = len(pattern.findall(text))
        punctuation[key] = {"count": found, "per_1000": per_thousand(found, n_words)}

    contracted = len(CONTRACTED.findall(text))
    expandable = len(EXPANDABLE.findall(text))
    lower_i = text == text.lower() or len(re.findall(r"\bi\b", text)) > len(re.findall(r"\bI\b", text))
    first_singular = len((FIRST_SINGULAR_LOWER if lower_i else FIRST_SINGULAR).findall(text))

    openers: Counter = Counter()
    for sentence in sentences:
        tokens = words(sentence)
        if tokens:
            openers[tokens[0].lower()] += 1
    conjunction_starts = sum(openers[w] for w in CONJUNCTION_OPENERS)

    lowered = Counter(w for w in all_words if not w.isupper())
    lowered_set = {w.lower() for w in lowered}
    shouted = Counter(
        w for w in all_words
        if len(w) >= 2 and w.isalpha() and w.isupper() and w.lower() in lowered_set)

    short_pieces = [d for d in docs if 0 < len(words(d.text)) < SHORT_PIECE]
    structured_short = [
        d.name for d in short_pieces if d.counts["headings"] >= 2 or d.counts["bullets"] >= 3]

    tells: dict = {}
    for tell_id, pattern in PATTERN_TELLS.items():
        matches = list(pattern.finditer(text))
        tells[tell_id] = {
            "count": len(matches), "value": per_thousand(len(matches), n_words),
            "unit": "per 1,000 words",
            "examples": [snippet(text, m.start(), m.end()) for m in matches[:3]],
        }
    tells["em-dash"] = {
        "count": punctuation["em_dash"]["count"], "value": punctuation["em_dash"]["per_1000"],
        "unit": "per 1,000 words",
        "examples": [snippet(text, m.start(), m.end()) for m in
                     list(PUNCTUATION["em_dash"].finditer(text))[:3]]}
    tells["bold-lead-in"] = {
        "count": counts["bold_lead_in"], "value": per_thousand(counts["bold_lead_in"], n_words),
        "unit": "per 1,000 words", "examples": []}
    tells["emoji-markers"] = {
        "count": counts["emoji_lead"], "value": per_thousand(counts["emoji_lead"], n_words),
        "unit": "per 1,000 words", "examples": []}
    tells["structure-on-short"] = {
        "count": len(structured_short), "value": share(len(structured_short), len(short_pieces)),
        "unit": "% of short pieces", "examples": structured_short[:3]}
    tells["fragment-recap"] = {
        "count": clusters, "value": per_thousand(clusters, n_words),
        "unit": "per 1,000 words", "examples": cluster_examples[:3]}
    tells["chopped-pairs"] = {
        "count": sum(1 for n in lengths if n <= SHORT_SENTENCE),
        "value": share(sum(1 for n in lengths if n <= SHORT_SENTENCE), n_sent),
        "unit": "% of sentences", "examples": []}
    tells["question-answer"] = {
        "count": answered, "value": per_thousand(answered, n_words),
        "unit": "per 1,000 words", "examples": answered_examples[:3]}
    tells["even-rhythm"] = {
        "count": n_sent, "value": round(spread / mean, 2) if mean else 0.0,
        "unit": "spread / average (lower is more even)", "examples": []}
    tells["paragraph-capstone"] = {
        "count": capstones, "value": share(capstones, eligible),
        "unit": "% of paragraphs with 3+ sentences", "examples": capstone_examples[:3]}

    para_sizes = [len(p) for p in paragraphs]
    return {
        "files": [d.name for d in docs],
        "words": n_words,
        "sentences": {
            "count": n_sent,
            "mean_words": round(mean, 1),
            "median_words": statistics.median(lengths) if lengths else 0,
            "spread_words": round(spread, 1),
            "short_pct": share(sum(1 for n in lengths if n <= SHORT_SENTENCE), n_sent),
            "long_pct": share(sum(1 for n in lengths if n >= LONG_SENTENCE), n_sent),
            "very_long_pct": share(sum(1 for n in lengths if n >= VERY_LONG_SENTENCE), n_sent),
            "longest_words": max(lengths) if lengths else 0,
            "fragment_clusters": clusters,
        },
        "paragraphs": {
            "count": len(paragraphs),
            "median_sentences": statistics.median(para_sizes) if para_sizes else 0,
            "single_sentence_pct": share(sum(1 for n in para_sizes if n == 1), len(para_sizes)),
            "short_closer_pct": share(capstones, eligible),
        },
        "punctuation": punctuation,
        "habits": {
            "contraction_pct": share(contracted, contracted + expandable),
            "contractions": contracted,
            "uncontracted": expandable,
            "first_singular_per_1000": per_thousand(first_singular, n_words),
            "first_plural_per_1000": per_thousand(len(FIRST_PLURAL.findall(text)), n_words),
            "second_person_per_1000": per_thousand(len(SECOND.findall(text)), n_words),
            "conjunction_opener_pct": share(conjunction_starts, n_sent),
            "top_openers": openers.most_common(top),
            "shouted_words": shouted.most_common(top),
            "shouted_per_1000": per_thousand(sum(shouted.values()), n_words),
        },
        "formatting": {
            "headings": counts["headings"], "bullet_lines": counts["bullets"],
            "table_rows": counts["table_rows"], "bold_spans": counts["bold"],
            "italic_spans": counts["italic"], "bold_lead_ins": counts["bold_lead_in"],
            "emoji_led_lines": counts["emoji_lead"],
            "bullet_pct": share(counts["bullets"], counts["bullets"] + len(paragraphs)),
        },
        "phrases": recurring_phrases(sentences, n_words, max(top, 20)),
        "tells": tells,
    }


# -------------------------------------------------------------- comparing

def compare(base: dict, draft: dict) -> dict:
    """Find where a draft departs from the writer's own numbers."""
    differs, tells, missing = [], [], []
    bs, ds = base["sentences"], draft["sentences"]

    def row(label: str, yours, theirs, note: str) -> None:
        differs.append({"measure": label, "you": yours, "draft": theirs, "note": note})

    if bs["mean_words"] and abs(ds["mean_words"] - bs["mean_words"]) / bs["mean_words"] > 0.25:
        longer = ds["mean_words"] > bs["mean_words"]
        row("Average sentence length (words)", bs["mean_words"], ds["mean_words"],
            "longer than yours" if longer else "shorter than yours")
    if ds["short_pct"] - bs["short_pct"] >= 8:
        row("Very short sentences (%)", bs["short_pct"], ds["short_pct"],
            "choppier than you; try joining pairs with and, but or so")
    elif bs["short_pct"] - ds["short_pct"] >= 8:
        row("Very short sentences (%)", bs["short_pct"], ds["short_pct"], "fewer short beats than you")
    if bs["long_pct"] - ds["long_pct"] >= 8:
        row("Long sentences (%)", bs["long_pct"], ds["long_pct"], "fewer long sentences than you")
    elif ds["long_pct"] - bs["long_pct"] >= 8:
        row("Long sentences (%)", bs["long_pct"], ds["long_pct"], "more long sentences than you")
    bp, dp = base["paragraphs"], draft["paragraphs"]
    if abs(dp["single_sentence_pct"] - bp["single_sentence_pct"]) >= 15:
        row("One-sentence paragraphs (%)", bp["single_sentence_pct"], dp["single_sentence_pct"],
            "more than you" if dp["single_sentence_pct"] > bp["single_sentence_pct"] else "fewer than you")
    bh, dh = base["habits"], draft["habits"]
    if bh["contraction_pct"] - dh["contraction_pct"] >= 20:
        row("Contractions (% of chances taken)", bh["contraction_pct"], dh["contraction_pct"],
            "stiffer than you")
    bf, df = base["formatting"], draft["formatting"]
    if df["bullet_pct"] - bf["bullet_pct"] >= 15:
        row("Bullet lines (% of blocks)", bf["bullet_pct"], df["bullet_pct"], "more bullets than you")

    for key, label in PUNCTUATION_LABELS.items():
        yours, theirs = base["punctuation"][key]["per_1000"], draft["punctuation"][key]["per_1000"]
        if key == "em_dash":
            continue  # reported with the tells
        if yours == 0 and theirs > 0 and draft["punctuation"][key]["count"] >= 2:
            row(label + " per 1,000 words", yours, theirs, "not in your writing")
        elif yours > 0 and theirs >= 2 * yours and theirs - yours >= 1.5:
            row(label + " per 1,000 words", yours, theirs, "more than you")

    for tell_id in TELL_IDS:
        yours, theirs = base["tells"][tell_id], draft["tells"][tell_id]
        if tell_id == "chopped-pairs":
            continue  # covered by the short-sentence row above
        if tell_id == "even-rhythm":
            if yours["value"] and theirs["value"] and theirs["value"] < 0.8 * yours["value"] \
                    and ds["count"] >= 10:
                tells.append({"tell": tell_id, "name": TELL_NAMES[tell_id], "you": yours["value"],
                              "draft": theirs["value"], "unit": theirs["unit"],
                              "note": "more even than you", "examples": []})
            continue
        if theirs["count"] == 0:
            continue
        if yours["value"] == 0:
            note = "not in your writing"
        elif theirs["value"] >= 2 * yours["value"] and theirs["count"] >= 2:
            note = "more than you"
        else:
            continue
        tells.append({"tell": tell_id, "name": TELL_NAMES[tell_id], "you": yours["value"],
                      "draft": theirs["value"], "unit": theirs["unit"], "note": note,
                      "examples": theirs["examples"]})

    if draft["words"] >= 300:
        def habit(label: str, yours: float, theirs: float, floor: float) -> None:
            if yours >= floor and theirs <= yours * 0.25:
                missing.append({"habit": label, "you": yours, "draft": theirs})
        for key in ("spaced_hyphen", "semicolon", "ellipsis", "parenthetical", "question",
                    "exclamation"):
            habit(PUNCTUATION_LABELS[key] + " per 1,000 words",
                  base["punctuation"][key]["per_1000"], draft["punctuation"][key]["per_1000"], 1.0)
        habit("Sentences starting with And, But, So (%)", bh["conjunction_opener_pct"],
              dh["conjunction_opener_pct"], 4.0)
        habit("ALL CAPS for stress, per 1,000 words", bh["shouted_per_1000"],
              dh["shouted_per_1000"], 0.5)
        habit("I, me, my per 1,000 words", bh["first_singular_per_1000"],
              dh["first_singular_per_1000"], 10.0)
        habit("You, your per 1,000 words", bh["second_person_per_1000"],
              dh["second_person_per_1000"], 10.0)
    return {"baseline_words": base["words"], "draft_words": draft["words"],
            "differs": differs, "tells": tells, "missing": missing}


# -------------------------------------------------------------- reporting

def _pairs(items: list) -> str:
    return ", ".join("%s (%d)" % (word, count) for word, count in items) or "none"


def render_report(stats: dict) -> str:
    s, p, h, f = stats["sentences"], stats["paragraphs"], stats["habits"], stats["formatting"]
    out = ["# Voice stats", ""]
    out.append("%d words, %d sentences and %d paragraphs in %d file%s." % (
        stats["words"], s["count"], p["count"], len(stats["files"]),
        "" if len(stats["files"]) == 1 else "s"))
    if stats["words"] < SMALL_SAMPLE:
        out.append("")
        out.append("**Small sample.** Under %d words, so treat every number here as rough." % SMALL_SAMPLE)
    out += ["", "## Sentences", ""]
    out.append("- Average length: %s words (median %s)" % (s["mean_words"], s["median_words"]))
    out.append("- Short, %d words or fewer: %s%%" % (SHORT_SENTENCE, s["short_pct"]))
    out.append("- Long, %d words or more: %s%% (%s%% run to %d or more)" % (
        LONG_SENTENCE, s["long_pct"], s["very_long_pct"], VERY_LONG_SENTENCE))
    out.append("- Longest: %s words" % s["longest_words"])
    out.append("- Spread: %s words (standard deviation)" % s["spread_words"])
    out.append("- Fragment clusters, 3 or more very short sentences in a row: %s" % s["fragment_clusters"])
    out += ["", "## Paragraphs", ""]
    out.append("- Typical length: %s sentences (median)" % p["median_sentences"])
    out.append("- One-sentence paragraphs: %s%%" % p["single_sentence_pct"])
    out.append("- Paragraphs of 3 or more sentences that end on a very short one: %s%%" % p["short_closer_pct"])
    out += ["", "## Punctuation", "", "| Mark | Count | Per 1,000 words |", "|---|---|---|"]
    for key, label in PUNCTUATION_LABELS.items():
        out.append("| %s | %d | %s |" % (label, stats["punctuation"][key]["count"],
                                         stats["punctuation"][key]["per_1000"]))
    out += ["", "## Word habits", ""]
    out.append("- Contractions: used in %s%% of the places one was possible (%d contracted, %d not)" % (
        h["contraction_pct"], h["contractions"], h["uncontracted"]))
    out.append("- Per 1,000 words: I/me/my %s, we/us/our %s, you/your %s" % (
        h["first_singular_per_1000"], h["first_plural_per_1000"], h["second_person_per_1000"]))
    out.append("- Sentences starting with And, But, So, Or, Because: %s%%" % h["conjunction_opener_pct"])
    out.append("- Most common sentence openers: %s" % _pairs(h["top_openers"]))
    out.append("- ALL CAPS used for stress: %s" % _pairs(h["shouted_words"]))
    out += ["", "## Formatting", ""]
    out.append("- Headings: %d. Bullet or numbered lines: %d (%s%% of blocks). Table rows: %d." % (
        f["headings"], f["bullet_lines"], f["bullet_pct"], f["table_rows"]))
    out.append("- Bold spans: %d. Italic spans: %d. Bold lead-in labels: %d. Emoji-led lines: %d." % (
        f["bold_spans"], f["italic_spans"], f["bold_lead_ins"], f["emoji_led_lines"]))
    out += ["", "## Recurring phrases", ""]
    out.append(_pairs(stats["phrases"]))
    out += ["", "## Common AI tells found in this writing", ""]
    out.append("A hit is not a verdict. If one of these shows up in writing you did yourself, it is yours.")
    out += ["", "| Tell | Hits | Value | Example |", "|---|---|---|---|"]
    for tell_id in TELL_IDS:
        tell = stats["tells"][tell_id]
        if not tell["count"] and tell_id not in ("chopped-pairs", "even-rhythm"):
            continue
        example = tell["examples"][0].replace("|", "/") if tell["examples"] else ""
        out.append("| %s (`%s`) | %d | %s %s | %s |" % (
            TELL_NAMES[tell_id], tell_id, tell["count"], tell["value"], tell["unit"], example))
    return "\n".join(out) + "\n"


def render_compare(result: dict) -> str:
    out = ["# Draft compared with your writing", ""]
    out.append("Your writing: %d words. Draft: %d words." % (
        result["baseline_words"], result["draft_words"]))
    if result["baseline_words"] < SMALL_SAMPLE:
        out.append("")
        out.append("**Small baseline.** Under %d words of your own writing, so these are rough." % SMALL_SAMPLE)
    if result["draft_words"] < 150:
        out.append("")
        out.append("**Short draft.** Rates swing a lot on a draft this short.")
    out += ["", "## Where the draft differs from you", ""]
    if result["differs"]:
        out += ["| Measure | You | Draft | Note |", "|---|---|---|---|"]
        for d in result["differs"]:
            out.append("| %s | %s | %s | %s |" % (d["measure"], d["you"], d["draft"], d["note"]))
    else:
        out.append("Nothing stands out in sentence length, paragraphs or punctuation.")
    out += ["", "## Tells in the draft that are not your habit", ""]
    if result["tells"]:
        out += ["| Tell | You | Draft | Note | Example from the draft |", "|---|---|---|---|---|"]
        for t in result["tells"]:
            example = t["examples"][0].replace("|", "/") if t["examples"] else ""
            out.append("| %s (`%s`) | %s | %s | %s | %s |" % (
                t["name"], t["tell"], t["you"], t["draft"], t["note"], example))
    else:
        out.append("None found.")
    out += ["", "## Your habits that are missing from the draft", ""]
    if result["missing"]:
        out.append("Do not add these on purpose. A draft with none of them has usually been smoothed too far, "
                   "so look at where it went flat.")
        out += ["", "| Habit | You | Draft |", "|---|---|---|"]
        for m in result["missing"]:
            out.append("| %s | %s | %s |" % (m["habit"], m["you"], m["draft"]))
    elif result["draft_words"] < 300:
        out.append("Draft is too short to check.")
    else:
        out.append("None missing.")
    out.append("")
    out.append("These counts cannot tell you whether the draft sounds like you. Read it out loud for that.")
    return "\n".join(out) + "\n"


# -------------------------------------------------------------------- cli

def collect(paths: list[str]) -> list[Path]:
    files: list[Path] = []
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


def load(paths: list[str]) -> list[Doc]:
    docs = [Doc(str(p), p.read_text(encoding="utf-8", errors="replace")) for p in collect(paths)]
    if not any(words(d.text) for d in docs):
        raise SystemExit("No text found in: %s" % ", ".join(paths))
    return docs


def main(argv: "list[str] | None" = None) -> int:
    parser = argparse.ArgumentParser(
        description="Count the countable parts of a writing voice.",
        epilog="Example: python3 voice_stats.py --compare draft.md my-writing/")
    parser.add_argument("samples", nargs="+", help="your own writing: .md or .txt files, or folders")
    parser.add_argument("--compare", metavar="DRAFT", help="a draft to compare with your writing")
    parser.add_argument("--json", action="store_true", help="print JSON instead of a report")
    parser.add_argument("--top", type=int, default=12, help="how many openers and phrases to list")
    args = parser.parse_args(argv)

    base = analyze(load(args.samples), args.top)
    if args.compare:
        draft = analyze(load([args.compare]), args.top)
        result = compare(base, draft)
        if args.json:
            print(json.dumps({"baseline": base, "draft": draft, "comparison": result}, indent=2))
        else:
            sys.stdout.write(render_compare(result))
    elif args.json:
        print(json.dumps(base, indent=2))
    else:
        sys.stdout.write(render_report(base))
    return 0


if __name__ == "__main__":
    sys.exit(main())
