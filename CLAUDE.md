# Like I Said

The repository is named `like-i-said`. It is an open kit that helps people build a "voice bible" so AI-assisted writing sounds like them. The audience is anyone who writes with AI, including people who are not technical.

## Generated files

`prompts/*.md` (all but `prompts/README.md`) and everything under `skill/voice-bible/` are generated. Never edit them directly.

- Edit `src/prompts/`, `src/skill/SKILL.md`, `reference/`, `templates/` and the three scripts in `tools/` (`voice_stats.py`, `check_quotes.py`, `check_invented.py`).
- Then run `python3 tools/build.py`.
- Then run `python3 -m unittest discover -s tools -p "test_*.py"`. One test fails if generated files are stale.

A source prompt pulls in a shared file with `{{include: path}}` on its own line.

## Things that must stay in sync

- Tell ids in `reference/ai-tells.md` marked "Countable" must match `TELL_IDS` in `tools/voice_stats.py`. A test checks this.
- Fixed wording in `templates/voice-bible.template.md` that appears in double quotes must be a section name, a bold label, or listed in `TEMPLATE_PHRASES` in `tools/check_quotes.py`. A test checks this.
- `templates/voice-bible.template.md` and the steps in `src/prompts/3-build-bible.md` describe the same piles, tags and table rows. Change them together.

## Writing style for the kit itself

The kit must not be written in the style it helps people avoid.

- No em dashes outside lines that show one as an example. A test checks this.
- No "it's not X, it's Y," no reflexive lists of three, no announcing ("here's the thing"), no tidy capstone lines.
- Plain, direct sentences. Prompts are written in the first person, as the user speaking to an AI.
- The README's prose is the exception. It is written in the author's own voice, which allows a few things this list does not, such as a spaced hyphen used as a dash and sentences that start with "So" or "And." Do not tidy it to match the rest of the kit.
- The README is also written for readers who will not read much. The first screen says what to do. Steps are numbered, and each one names its time and what you end up with. No list runs past five items. Figures of speech are replaced with the literal thing. The last line is one next action. Keep to this when you change it.
- The made-up bookkeeper's note in the README should read like a real message from a real person: a friendly but firm request, with nothing in it that her notes do not contain. Run `tools/check_invented.py` on it against her notes after any change.
- Each prompt in `prompts/` must work when pasted alone into any chat assistant, so it cannot refer to other files in this repository.

## Nothing personal in published files

The kit is published with its author's name on the LICENSE and nowhere else. Every other file must be free of personal material: no real names, employers, places, quotes, stories, project details or statistics taken from the author's own writing or history. Examples and test fixtures are invented. The bookkeeper in the README's before-and-after is made up and must stay that way.

`_source/` holds the private material the kit was derived from. It is ignored by git. Never copy anything from it into a published file, and never use it as a source of example sentences. `my-voice/` is ignored for the same reason.

If `_source/check_private.py` exists, run it before any commit or publish. It scans the published files for private terms and for passages that match the private material.

Scripts use only the Python standard library and support Python 3.8 or newer.
