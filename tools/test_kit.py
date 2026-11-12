"""Tests for the build script, the quote checker, and the kit's own files.

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
import build  # noqa: E402
import check_quotes as cq  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class Build(unittest.TestCase):
    def test_generated_files_are_current(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = build.main(["--check"])
        self.assertEqual(code, 0, out.getvalue())

    def test_includes_are_expanded(self):
        built = build.outputs()
        prompt = built[ROOT / "prompts" / "3-build-bible.md"]
        self.assertNotIn("{{include", prompt)
        self.assertIn("### `em-dash`", prompt)
        self.assertIn("## Leave these alone", prompt)
        interview = built[ROOT / "prompts" / "1-interview.md"]
        self.assertIn("## Part 7: Preferences", interview)
        self.assertNotIn("## How to answer", interview, "the partial include starts at Part 1")

    def test_skill_is_self_contained(self):
        skill = build.outputs()[build.SKILL / "SKILL.md"]
        for mentioned in set(re.findall(r"`((?:references|scripts)/[\w.-]+)`", skill)):
            self.assertIn(build.SKILL / mentioned, build.outputs(), mentioned)
        self.assertTrue(skill.startswith("---\nname: voice-bible\n"))


class QuoteChecker(unittest.TestCase):
    SOURCES = ("I only took the job for the parking, honestly. Most quit. Marta stayed. Be like Marta.\n"
               "It’s more of a patchwork quilt than a five-year plan, and that suits me fine.")

    def problems(self, bible):
        return [quote for _, quote, _ in cq.check(bible, self.SOURCES)]

    def test_real_quotes_pass(self):
        bible = ('- ✅ "I only took the job for the parking, honestly."\n'
                 '> "Most quit. Marta stayed. Be like Marta."\n'
                 '- "it\'s more of a patchwork quilt" as a self-description `[moderate]`\n')
        self.assertEqual(self.problems(bible), [])

    def test_invented_quote_is_caught(self):
        self.assertEqual(self.problems('- ✅ "I took the job for the free parking."\n'),
                         ["I took the job for the free parking."])

    def test_tidied_quote_is_caught(self):
        self.assertEqual(self.problems('> "Most of them quit. Marta stayed."\n'), ["Most of them quit. Marta stayed."])

    def test_cross_marked_examples_are_skipped(self):
        self.assertEqual(self.problems('- ❌ "Support is a rich tapestry of journeys."\n'), [])

    def test_elided_quote_checks_each_part(self):
        self.assertEqual(self.problems('"I only took the job... Be like Marta."\n'), [])
        found = cq.check('"I only took the job... Be like Greta."\n', self.SOURCES)
        self.assertEqual(found[0][2], ["be like greta"])

    def test_ellipsis_character_at_either_end(self):
        bible = ('> "Most quit. Marta stayed…"\n'
                 '- "…patchwork quilt than a five-year plan"\n')
        self.assertEqual(self.problems(bible), [])

    def test_headings_and_never_lists_are_skipped(self):
        bible = ('### 2. "It\'s not just X, it\'s Y" `[said]`\n'
                 '**Words and phrases Sam never uses:** "delve", "tapestry"\n')
        self.assertEqual(self.problems(bible), [])

    def test_references_to_its_own_sections_are_skipped(self):
        bible = ('## Leave these alone\n\n### 3. Stiff setup lines `[strong]`\n\n'
                 '**Raw versus finished.** Filler goes.\n\n'
                 'See "Leave these alone," "Raw versus finished" and "Stiff setup lines."\n')
        self.assertEqual(self.problems(bible), [])

    def test_unquoted_blockquote_is_checked(self):
        self.assertEqual(self.problems("> Most quit. Marta stayed.\n> Be like Marta.\n"), [])
        self.assertEqual(len(self.problems("> Most quit. Greta stayed.\n")), 1)

    def test_template_wording_is_not_treated_as_a_quote(self):
        # A finished bible keeps the template's fixed wording and loses the bracketed guidance.
        template = (ROOT / "templates" / "voice-bible.template.md").read_text(encoding="utf-8")
        fixed, previous = template, None
        while fixed != previous:
            previous, fixed = fixed, re.sub(r"\[[^\[\]]*\]", "", fixed)
        self.assertEqual(cq.check(fixed, "nothing relevant here"), [])

    def test_command_line(self):
        with tempfile.TemporaryDirectory() as folder:
            bible = Path(folder) / "voice-bible.md"
            source = Path(folder) / "interview.md"
            source.write_text(self.SOURCES, encoding="utf-8")
            bible.write_text('> "Be like Marta."\n', encoding="utf-8")
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(cq.main([str(bible), folder]), 0)
            bible.write_text('> "Be like Greta."\n', encoding="utf-8")
            with redirect_stdout(out):
                self.assertEqual(cq.main([str(bible), folder]), 1)
            self.assertIn('line 1: "Be like Greta."', out.getvalue())


class KitProse(unittest.TestCase):
    """The kit should not be written in the style it helps people avoid."""

    def test_no_em_dashes_outside_examples(self):
        allowed = {
            # These files show em dashes on purpose, as examples of the tell.
            ROOT / "reference" / "ai-tells.md": 1,
            ROOT / "prompts" / "3-build-bible.md": 1,
            build.SKILL / "references" / "3-build-bible.md": 1,
        }
        folders = ("README.md", "docs", "prompts", "reference", "templates", "src", "skill")
        files = []
        for name in folders:
            path = ROOT / name
            files += [path] if path.is_file() else sorted(path.rglob("*.md")) if path.exists() else []
        self.assertGreater(len(files), 10)
        for path in files:
            count = path.read_text(encoding="utf-8").count("—")
            self.assertLessEqual(count, allowed.get(path, 0), "%s has %d em dashes" % (path, count))


if __name__ == "__main__":
    unittest.main()
