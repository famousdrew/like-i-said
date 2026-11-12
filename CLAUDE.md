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
- Each prompt in `prompts/` must work when pasted alone into any chat assistant, so it cannot refer to other files in this repository.

## Nothing personal in published files

The kit is published with its author's name on the LICENSE and nowhere else. Every other file must be free of personal material: no real names, employers, places, quotes, stories, project details or statistics taken from the author's own writing or history. Examples and test fixtures are invented. The bookkeeper in the README's before-and-after is made up and must stay that way.

`_source/` holds the private material the kit was derived from. It is ignored by git. Never copy anything from it into a published file, and never use it as a source of example sentences. `my-voice/` is ignored for the same reason.

If `_source/check_private.py` exists, run it before any commit or publish. It scans the published files for private terms and for passages that match the private material.

Scripts use only the Python standard library and support Python 3.8 or newer.
