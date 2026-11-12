"""Tests for voice_stats.py. Run from the repo root:

    python3 -m unittest discover -s tools -p "test_*.py"
"""
import io
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import voice_stats as vs  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def stats_for(text):
    return vs.analyze([vs.Doc("sample.md", text)])


class SentenceSplitting(unittest.TestCase):
    def check(self, text, expected):
        self.assertEqual(vs.split_sentences(text), expected)

    def test_plain(self):
        self.check("It broke. We fixed it! Did it hold?", ["It broke.", "We fixed it!", "Did it hold?"])

    def test_titles_and_decimals(self):
        self.check("Dr. Lee cut the wait from 9 minutes to 3.5 and left. Nobody argued.",
                   ["Dr. Lee cut the wait from 9 minutes to 3.5 and left.", "Nobody argued."])

    def test_latin_abbreviations(self):
        self.check("Pick a tool, e.g. a wiki, and start. Then stop.",
                   ["Pick a tool, e.g. a wiki, and start.", "Then stop."])

    def test_ellipsis_inside_a_sentence(self):
        self.check("keep it there...for now. Done.", ["keep it there...for now.", "Done."])
        self.check("Wait... what? Yes.", ["Wait... what?", "Yes."])

    def test_ellipsis_ending_a_sentence(self):
        self.check("I thought so... Then it rained.", ["I thought so...", "Then it rained."])

    def test_quoted_question_with_attribution(self):
        self.check('"Why?" he asked. Then he left.', ['"Why?" he asked.', "Then he left."])

    def test_quoted_sentence_then_new_sentence(self):
        self.check('She said "no." Then she left.', ['She said "no."', "Then she left."])

    def test_lowercase_writer(self):
        self.check("ok so i tried it. it broke.", ["ok so i tried it.", "it broke."])

    def test_period_beats(self):
        self.check("Not. One. Word.", ["Not.", "One.", "Word."])


class Parsing(unittest.TestCase):
    def test_markup_is_counted_and_removed(self):
        doc = vs.Doc("a.md", "---\ntitle: x\n---\n# Heading\n\nSome *real* text with a [link](http://x.y).\n\n"
                             "```\ncode. here. no.\n```\n\n- one\n- two\n\n| a | b |\n")
        self.assertEqual(doc.paragraphs, ["Some real text with a link."])
        self.assertEqual(doc.list_items, ["one", "two"])
        self.assertEqual(doc.counts["headings"], 1)
        self.assertEqual(doc.counts["bullets"], 2)
        self.assertEqual(doc.counts["italic"], 1)
        self.assertEqual(doc.counts["table_rows"], 1)

    def test_bold_lead_in_and_emoji_lines(self):
        doc = vs.Doc("a.md", "- **Clarity:** say it.\n- **Speed**: go.\n\n\U0001F680 Launch faster\n")
        self.assertEqual(doc.counts["bold_lead_in"], 2)
        self.assertEqual(doc.counts["emoji_lead"], 1)

    def test_blockquotes_count_as_prose(self):
        doc = vs.Doc("a.md", "> A quoted line.\n> And another.\n")
        self.assertEqual(doc.paragraphs, ["A quoted line. And another."])


class Counting(unittest.TestCase):
    def test_dashes(self):
        s = stats_for("One — two. Three -- four. Five - six.\n\n- a bullet, not a dash\n")
        self.assertEqual(s["punctuation"]["em_dash"]["count"], 2)
        self.assertEqual(s["punctuation"]["spaced_hyphen"]["count"], 1)

    def test_colons_skip_clock_times(self):
        s = stats_for("We met at 3:30 sharp. One rule: show up.")
        self.assertEqual(s["punctuation"]["colon"]["count"], 1)

    def test_curly_quotes_are_normalized(self):
        s = stats_for("I don’t know. It’s fine… really.")
        self.assertEqual(s["habits"]["contractions"], 2)
        self.assertEqual(s["punctuation"]["ellipsis"]["count"], 1)

    def test_contraction_share(self):
        s = stats_for("I don't know. I do not care. It's fine. It is late.")
        self.assertEqual(s["habits"]["contraction_pct"], 50.0)

    def test_sentence_numbers(self):
        s = stats_for("Short one. " + " ".join(["word"] * 30) + ".")
        self.assertEqual(s["sentences"]["count"], 2)
        self.assertEqual(s["sentences"]["short_pct"], 50.0)
        self.assertEqual(s["sentences"]["long_pct"], 50.0)

    def test_fragment_cluster(self):
        s = stats_for("We shipped it on Friday afternoon. No fluff. No jargon. Just results.")
        self.assertEqual(s["tells"]["fragment-recap"]["count"], 1)

    def test_shouted_words_skip_acronyms(self):
        s = stats_for("I LOVE this and I love that. The API is fine.")
        self.assertEqual(dict(s["habits"]["shouted_words"]), {"LOVE": 1})

    def test_recurring_phrases(self):
        s = stats_for("A pile of forms came in. A pile of people left. Nothing else repeats here.")
        self.assertIn(("a pile of", 2), s["phrases"])


class Tells(unittest.TestCase):
    def hits(self, tell_id, text):
        return stats_for(text)["tells"][tell_id]["count"]

    def test_negate_then_restate(self):
        self.assertEqual(self.hits("not-x-but-y", "It's not just a budget. It's a statement of values."), 1)
        self.assertEqual(self.hits("not-x-but-y", "This isn't a tooling problem, it's a trust problem."), 1)

    def test_plain_contrast_is_not_flagged(self):
        for line in ("Cheap isn't the goal; reliable is the goal.",
                     "A long report isn't a virtue. A clear report is.",
                     "I am not the one who is worried. You are."):
            self.assertEqual(self.hits("not-x-but-y", line), 0, line)

    def test_phrase_tells(self):
        self.assertEqual(self.hits("announcing", "Here's the thing. Let's dive in."), 2)
        self.assertEqual(self.hits("ai-vocabulary", "We delve into a rich tapestry of robust tools."), 3)
        self.assertEqual(self.hits("significance-tail", "Sales rose 4%, underscoring the need for patience."), 1)
        self.assertEqual(self.hits("colon-reveal", "Here's the thing: nobody reads it. The result: chaos."), 2)
        self.assertEqual(self.hits("toast-and-ask", "Here's to the unsung heroes. What do you think?"), 2)

    def test_question_answered_at_once(self):
        self.assertEqual(self.hits("question-answer", "The result? Total confusion."), 1)

    def test_ids_match_the_catalog(self):
        catalog = (ROOT / "reference" / "ai-tells.md").read_text(encoding="utf-8")
        entries = re.findall(r"^### `([a-z-]+)`.*?\n(.*?)(?=^### |^## |\Z)", catalog, re.S | re.M)
        self.assertGreater(len(entries), 20)
        counted = {i for i, body in entries if "Countable" in body}
        judged = {i for i, body in entries if "Judgment call" in body}
        self.assertEqual(counted | judged, {i for i, _ in entries}, "every entry says how it is checked")
        self.assertEqual(counted, set(vs.TELL_IDS))
        self.assertEqual(set(vs.TELL_NAMES), set(vs.TELL_IDS))


class Comparing(unittest.TestCase):
    MINE = ("I ran the shop for six years and I don't miss the early starts. We fixed what broke, "
            "wrote it down, and moved on to the next thing before lunch. Nobody asked for a report. "
            "So I stopped writing them, and it turns out nobody noticed for about a year. ") * 12
    DRAFT = ("It's not just about tickets — it's about trust. Moreover, robust teams leverage "
             "seamless tools. The result? Happier customers. No fluff. No jargon. Just results. ") * 6

    def test_draft_tells_are_flagged(self):
        result = vs.compare(stats_for(self.MINE), stats_for(self.DRAFT))
        flagged = {t["tell"]: t["note"] for t in result["tells"]}
        for tell_id in ("em-dash", "ai-vocabulary", "stock-transitions", "fragment-recap",
                        "question-answer"):
            self.assertEqual(flagged.get(tell_id), "not in your writing", tell_id)
        measures = {d["measure"] for d in result["differs"]}
        self.assertIn("Very short sentences (%)", measures)

    def test_own_writing_compared_with_itself_is_clean(self):
        base = stats_for(self.MINE)
        result = vs.compare(base, base)
        self.assertEqual((result["differs"], result["tells"], result["missing"]), ([], [], []))


class CommandLine(unittest.TestCase):
    def run_cli(self, *args):
        out = io.StringIO()
        with redirect_stdout(out):
            code = vs.main(list(args))
        return code, out.getvalue()

    def test_report_and_compare(self):
        with tempfile.TemporaryDirectory() as folder:
            mine = Path(folder) / "mine"
            mine.mkdir()
            (mine / "a.md").write_text(Comparing.MINE, encoding="utf-8")
            (mine / "skip.json").write_text("{}", encoding="utf-8")
            draft = Path(folder) / "draft.txt"
            draft.write_text(Comparing.DRAFT, encoding="utf-8")
            code, report = self.run_cli(str(mine))
            self.assertEqual(code, 0)
            self.assertIn("# Voice stats", report)
            self.assertIn("in 1 file.", report)
            code, compared = self.run_cli("--compare", str(draft), str(mine))
            self.assertEqual(code, 0)
            self.assertIn("Em dashes (`em-dash`)", compared)
            code, as_json = self.run_cli("--json", str(mine))
            self.assertIn('"sentences"', as_json)

    def test_missing_path_stops_with_a_message(self):
        with self.assertRaises(SystemExit) as stop:
            vs.main(["/no/such/file.md"])
        self.assertIn("Not found", str(stop.exception))


if __name__ == "__main__":
    unittest.main()
