# Prompts

Each file here is one complete prompt. Open it, copy the whole thing, and paste it into a new chat with any AI assistant. On GitHub, the "Copy raw file" button at the top right of the file does this in one click.

## Building your voice bible

| Prompt | What it does | You end up with |
|---|---|---|
| [1-interview.md](1-interview.md) | The AI interviews you for 20 to 30 minutes | `interview.md` |
| [2-edit-exercise.md](2-edit-exercise.md) | The AI writes three short passages and you rewrite them | `edits.md` |
| [3-build-bible.md](3-build-bible.md) | Turns your interview, edits and writing samples into the bible | `voice-bible.md` |
| [4-voice-card.md](4-voice-card.md) | Shrinks the bible to fit a small instruction box | `voice-card.md` |

## Using it

| Prompt | What it does |
|---|---|
| [use-draft.md](use-draft.md) | Drafts something in your voice from your notes |
| [use-check.md](use-check.md) | Checks a draft against your bible and flags what is off |
| [use-refresh.md](use-refresh.md) | Updates the bible from your latest edits |

## If you want to change a prompt

These files are generated. Edit the sources in `src/prompts/`, `reference/` and `templates/`, then run `python3 tools/build.py`. A change made here directly is overwritten by the next build.
