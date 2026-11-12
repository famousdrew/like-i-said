"""Tests for check_invented.py.

    python3 -m unittest discover -s tools -p "test_*.py"
"""
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_invented as ci  # noqa: E402

NOTES = ("11 clients sent receipt photos this month, crumpled, can read maybe half. "
         "what to do: find the card statement, circle the charge, write what it was for. "
         "applies to parking too. next note goes out on the 3rd. marta said keep every receipt.")


def found(draft, notes=NOTES):
    return [(kind, text) for _, kind, text in ci.check(draft, notes)]


class Numbers(unittest.TestCase):
    def test_words_and_digits_are_the_same_figure(self):
        self.assertEqual(found("Eleven of you sent photos. The next one lands on the 3rd."), [])

    def test_a_new_figure_is_flagged(self):
        self.assertEqual(found("That cost my clients $340 last year, about 23% more."),
                         [("number", "$340"), ("number", "23%")])

    def test_commas_and_trailing_zeros_do_not_matter(self):
        self.assertEqual(found("It came to $2,150.00.", "they owe 2150 in total"), [])

    def test_hyphenated_number_words(self):
        self.assertEqual(found("Twenty-five of them replied.", "25 replied"), [])
        self.assertEqual(found("Twenty-five of them replied.", "some replied"),
                         [("number", "twenty-five")])

    def test_one_and_two_are_left_alone(self):
        self.assertEqual(found("One thing matters, and two people know it."), [])

    def test_list_numbering_is_not_a_figure(self):
        self.assertEqual(found("1. Find the card statement.\n2. Circle the charge."), [])

    def test_a_figure_is_reported_once(self):
        self.assertEqual(len(found("It was 40. Still 40. Always 40.")), 1)


class Names(unittest.TestCase):
    def test_a_name_from_the_notes_is_fine(self):
        self.assertEqual(found("As Marta said, keep it. Marta's rule is simple."), [])

    def test_an_unknown_name_is_flagged(self):
        self.assertEqual(found("I asked Tomas about it on Thursday."),
                         [("name", "Tomas"), ("name", "Thursday")])

    def test_the_first_word_of_a_sentence_is_not_a_name(self):
        self.assertEqual(found("Right. Here is what to do. Most of you will ignore this."), [])

    def test_a_two_word_name_at_the_start_of_a_sentence_is_caught(self):
        self.assertEqual(found("Hurricane Zeta closed the office."),
                         [("name", "Hurricane"), ("name", "Zeta")])

    def test_capitals_for_stress_are_not_names(self):
        self.assertEqual(found("You can NOT read half of them."), [("name", "NOT")])
        self.assertEqual(found("You can NOT read half.", NOTES + " not readable"), [])


class Quotations(unittest.TestCase):
    def test_a_quotation_from_the_notes_is_fine(self):
        self.assertEqual(found('She told them to "keep every receipt."'), [])

    def test_an_invented_quotation_is_flagged(self):
        self.assertEqual(found('She said "paper never lies to you" and left.'),
                         [("quotation", "paper never lies to you")])

    def test_short_quoted_words_are_ignored(self):
        self.assertEqual(found('It was "fine" and "not urgent."'), [])


class Skipped(unittest.TestCase):
    def test_gaps_headings_and_code_are_skipped(self):
        draft = ("# March Update From Nadia\n\n[NEED: the date for Tomas]\n\n"
                 "```\nTomas owes 999\n```\n")
        self.assertEqual(found(draft), [])


class CommandLine(unittest.TestCase):
    def test_exit_codes_and_report(self):
        with tempfile.TemporaryDirectory() as folder:
            notes = Path(folder) / "notes.md"
            notes.write_text(NOTES, encoding="utf-8")
            draft = Path(folder) / "draft.md"
            draft.write_text("Eleven of you sent photos.", encoding="utf-8")
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(ci.main([str(draft), str(notes)]), 0)
            draft.write_text("Eleven of you sent photos.\n\nTomas sent 14.", encoding="utf-8")
            with redirect_stdout(out):
                self.assertEqual(ci.main([str(draft), str(notes)]), 1)
            self.assertIn("line 3, number: 14", out.getvalue())

    def test_missing_file_stops_with_a_message(self):
        with self.assertRaises(SystemExit) as stop:
            ci.main(["/no/such/draft.md", "/no/such/notes.md"])
        self.assertIn("Not found", str(stop.exception))


if __name__ == "__main__":
    unittest.main()
