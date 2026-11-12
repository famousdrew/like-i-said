---
name: voice-bible
description: Build, use and maintain a personal "voice bible" so that AI-assisted writing sounds like the person and not like an AI. Use this skill whenever someone wants AI drafts to sound like them, wants to capture or document their writing voice or style, says a draft "sounds like AI" or "sounds like ChatGPT," asks for a draft to be checked against their voice, wants something written in their own voice from notes or a voice memo, or wants to update their voice bible after editing a draft. It covers the interview, the edit exercise, analysis of writing samples, the finished bible and short voice card, draft checks, and refreshes.
---

# Voice Bible

A voice bible is a reference document that tells an AI how one particular person writes: what they never do, what they do that an editor would wrongly fix, how their sentences and arguments are built, and the numbers behind it. This skill builds one from evidence and then uses it.

Four ideas run through everything here, and they explain most of the instructions below.

- **Evidence over taste.** Every rule comes from the person's own words: an interview, their writing, or their edits to an AI draft. Your sense of good writing is not evidence. If their writing has a habit you would normally fix, the habit wins.
- **Their exact words.** Quotes are copied character for character. An invented or tidied quote poisons the bible, because later drafts will imitate a sentence the person never wrote.
- **Voice is their call.** Fix typos without asking. Flag anything about voice and let them decide, even when the bible says they are wrong. People overrule their own rules on purpose.
- **Rules get performed.** Once a habit is written down, a drafting model tends to use it in every paragraph. That is why occasional habits get ceilings, and why drafting starts from the person's raw material and never from an earlier AI draft.

## Where things live

Keep one working folder per person. Default to `my-voice/` in the current directory unless they name another place or one already exists. Check for it first and pick up where they left off.

```
my-voice/
  interview.md          the interview transcript, word for word
  edits.md              AI drafts with the person's rewrites
  samples/finished/     things they typed, edited and sent or published, with no AI help
  samples/ai-assisted/  pieces an AI helped draft, which they then edited
  samples/raw/          notes, voice memo transcripts, quick messages
  samples/notes.md      one line per sample that needs explaining, such as "dictated"
  stats.md              output of the stats script
  voice-bible.md        the bible
  voice-card.md         the short version
```

This folder holds personal writing. Do not send its contents to any outside service, and if the directory is a git repository, suggest adding the folder to `.gitignore` before anything is committed.

## The reference files

`references/` holds one file per job. Each is written as a message from the person to an AI ("You are going to interview me..."), because the same files are published as copy-paste prompts for people who use a chat app. Read the file for the job and treat it as the person's instructions to you. Where this document differs from a reference file, this document wins, because you have a file system and a script and a chat app does not.

| Job | Read | When |
|---|---|---|
| Interview | `references/1-interview.md` | No `interview.md` yet |
| Edit exercise | `references/2-edit-exercise.md` | After the interview, or any time for stronger evidence |
| Build the bible | `references/3-build-bible.md` | There is material and no bible, or they ask to rebuild |
| Voice card | `references/4-voice-card.md` | A bible exists and they want the short version |
| Draft | `references/use-draft.md` | They want something written in their voice |
| Check | `references/use-check.md` | They want a draft checked |
| Refresh | `references/use-refresh.md` | They have new edits or new writing |

If the person says only "help me sound like myself" and has no bible, explain the path in three or four lines (interview, edit exercise, samples, build), say it takes about an hour end to end, and start the interview.

## Building a bible

### 1. Gather what exists

Ask what they already have: emails, posts, messages, old documents, voice memos. Their side of old conversations with an AI assistant is a good source too, since they typed it themselves and nobody polished it. Have them drop files into the three `samples/` folders. Which folder matters, because the sources are not equally trustworthy. Something they typed alone shows how they write. A piece an AI drafted and they edited shows only what they will accept. Dictated material shows how they talk, and its punctuation belongs to the transcription software. Ask about anything unclear and record the answer in `samples/notes.md`.

Writing from before they started using AI is the cleanest. Even three or four pieces help, and nothing at all is fine too, since the interview can carry a starter bible.

### 2. Interview

Follow `references/1-interview.md`. Ask one question at a time in the conversation. Spoken answers are more useful than typed ones for most of it, so suggest they use their system's dictation, or record a voice memo and paste the transcript. They can also answer the questions on their own in a file and come back.

When it ends, write the transcript to `interview.md` yourself instead of asking them to copy it. Mark each answer `[spoken]` or `[typed]`, asking which was which if you cannot tell. Do not fix anything in their answers.

### 3. Edit exercise

Follow `references/2-edit-exercise.md`. Write each passage to a file such as `my-voice/exercise-1.md` so they can edit it in their own editor, then read the file back when they say they are done. Save both versions, word for word, to `edits.md`. This step produces the strongest evidence in the whole process, so encourage it, but let them skip it.

### 4. Measure

Run the stats script on material they typed, because dictated speech runs longer and looser than writing:

```bash
python3 scripts/voice_stats.py my-voice/samples/finished > my-voice/stats.md
```

Use these numbers for the Mechanics table instead of estimating. If `samples/finished/` is empty, fall back to `samples/ai-assisted/`, then to typed interview answers, and say under the table which one the numbers came from. The script also counts common AI tells in their own writing. A hit there means the habit is theirs, which is exactly what the sorting step needs to know.

### 5. Analyze, check in, and write

Read all of `references/3-build-bible.md`, since its principles govern every step, and follow it from Step 3 onward. Read every file in the working folder in full. Do the check-in (its Step 6) in the conversation and wait for answers. Then write `voice-bible.md`.

### 6. Verify the quotes

Run the quote checker before you show them the bible:

```bash
python3 scripts/check_quotes.py my-voice/voice-bible.md my-voice/interview.md my-voice/edits.md my-voice/samples
```

It lists every quoted passage in the bible that does not appear word for word in the source material. Go through the list. Where a quote is attributed to the person, copy the real text or remove it. The checker also flags quoted phrases that were never meant as their words, such as the name of a pattern, and those can stay. The ❌ examples are skipped. Do not hand over a bible with an unverified quote of the person.

### 7. Hand over

Show them where the bible is and name the two or three rules you are least sure of. Offer the voice card. Tell them the bible improves fastest when they save their edits to AI drafts and run a refresh.

## Drafting in their voice

Follow `references/use-draft.md`. Three things matter more than the rest.

- **Start from their material.** If they gave only a topic, ask the three to six questions first. A draft built on nothing but the bible is an impression of them wrapped around generic content, and no amount of checking afterward puts the substance back.
- **Re-read the bible and their raw material at the start of every drafting job.** Never use an earlier AI draft as the style reference, even one they approved. Each copy drifts a little further from the person.
- **Invent nothing.** No anecdotes, numbers, quotes or details they did not supply. Mark gaps as `[NEED: ...]`. Before you show a draft, run `python3 scripts/check_invented.py path/to/draft.md path/to/their-notes.md` and resolve every number, name and quotation it lists, by removing it or asking them.

When they edit your draft, save the before and after to `edits.md` under a dated heading. Those pairs are what the next refresh runs on.

## Checking a draft

Run the comparison first, then follow `references/use-check.md`. If the notes the draft was written from are available, run `scripts/check_invented.py` on the draft against them as well, and list what it finds as questions.

```bash
python3 scripts/voice_stats.py --compare path/to/draft.md my-voice/samples/finished
```

The script shows where the draft's numbers leave theirs. It cannot tell whether the draft sounds like them, so use it to decide where to look and do the reading yourself. Report in the two buckets: mechanical fixes applied and listed, voice issues flagged as a numbered list for them to answer. Leave anything under "Leave these alone" untouched.

## Refreshing

Follow `references/use-refresh.md`, using everything added to `edits.md` and `samples/` since the last entry in the bible's Provenance section. Propose changes as a numbered list and wait. After applying the approved ones, run the quote checker again, and add a dated Provenance line. Pruning is part of the job: a rule the evidence no longer supports should go.
