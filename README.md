# Like I Said

A kit for building a voice bible: a reference document that teaches an AI to write like you.

AI assistants have a house style. It is competent and easy to spot, and there is nothing wrong with it except that it is not yours. Asking for "my voice" does not help much, because the assistant has never read you, and almost nobody can describe their own voice well enough to brief it.

A voice bible closes that gap with evidence. It is a few pages built from your own words: what you never do, what you do that an editor would wrongly fix, how your sentences and arguments are put together, and the numbers behind it. You hand it to Claude, ChatGPT, Gemini or any other assistant before it drafts or edits for you. The name comes from the one test every line has to pass: would you actually say this out loud?

## What it changes

Both drafts below came from the same few lines of notes, for a made-up bookkeeper writing her monthly note to clients. The pair was written for this page as an illustration. A real one comes from your notes and your bible.

**Her notes**

> 11 clients sent receipt photos this month, crumpled, can read maybe half. what to do: find the card statement, circle the charge, write what it was for, four words is plenty. that's all i need and all anyone who asks later needs. applies to parking too. next note goes out on the 3rd.

**A default draft**

> Hello everyone! I hope this month is treating you well. Let's talk about a topic that may not be exciting but is incredibly important: receipts. Keeping clear records isn't just about staying organized. It's about protecting your business. This month, several of you sent photos that were difficult to read, which can create unnecessary stress down the road. Here's the good news: there's a simple fix! Whether you're a seasoned business owner or just starting out, a little preparation goes a long way. As always, don't hesitate to reach out with any questions.

**The same notes, drafted with her voice bible**

> Eleven of you sent receipts as photos of crumpled paper this month. I can read about half of them.
>
> Right. Here is what to do with the ones I cannot read.
>
> 1. Find the card statement for that week.
> 2. Circle the charge.
> 3. Write what it was for next to it. Four words is plenty.
>
> That is enough for me, and it is enough for anyone who asks later. (Yes, even the parking ones.)
>
> Next one of these lands on the 3rd.

Nothing is wrong with the first draft, and it could have been written for anyone. The second is hers. The number comes first, there is no greeting, the procedure is numbered, there is one dry aside, and the next date sits where a sign-off would go. Her bible lists each of those habits, with a line of her own writing behind it.

## What you need

- About an hour
- Any AI chat assistant
- Optional, and worth it: a few things you wrote yourself, such as emails, posts or messages. Writing you did with no AI help is the most useful. If you have little of it, your own side of old chats with an AI counts, since you typed it and nobody polished it.

No installation and no code. Everything is a prompt you copy and paste.

## Build yours

| Step | Prompt | Time | You save |
|---|---|---|---|
| 1. Get interviewed | [1-interview.md](prompts/1-interview.md) | 20 to 30 min | `interview.md` |
| 2. Fix three AI drafts | [2-edit-exercise.md](prompts/2-edit-exercise.md) | 15 min | `edits.md` |
| 3. Build the bible | [3-build-bible.md](prompts/3-build-bible.md) | 10 min | `voice-bible.md` |
| 4. Make the short version | [4-voice-card.md](prompts/4-voice-card.md) | 2 min | `voice-card.md` |

**Step 1.** Open the interview prompt, copy all of it, and paste it into a new chat. The AI asks about your work, your stories and your opinions, one question at a time. It will not ask you to describe your style. Near the end it shows you a few pairs of sentences and asks which sounds more like you. Answer out loud with dictation if you can, and do not tidy what comes out. At the end it hands you a transcript to save. If you would sooner answer on your own, the questions are in [reference/interview-questions.md](reference/interview-questions.md).

**Step 2.** In the same chat, paste the edit exercise prompt. The AI writes three short passages about things you said, in its own style, and you rewrite each one the way you would say it. What you change is the strongest evidence in the whole process, so do not skip this if you can spare the time.

**Step 3.** Open a new chat. Paste the build prompt, then your interview, your edits, and any writing samples you have. If you ran the stats script described below, paste its report too. For each sample, say whether you typed or dictated it, whether it is finished or rough, and whether an AI helped draft it. Before it writes anything, the AI shows you what it plans to ban and protect and asks a few questions. Then it gives you the bible.

**Step 4.** In the same chat, say "card" to get a version short enough for a small instruction box.

You can stop after step 1 and still get a starter bible. Each extra kind of evidence makes it sharper.

## Use it

| When | Prompt |
|---|---|
| You want something drafted from your notes | [use-draft.md](prompts/use-draft.md) |
| You want a draft checked | [use-check.md](prompts/use-check.md) |
| You have edited a few AI drafts and want the bible to learn from them | [use-refresh.md](prompts/use-refresh.md) |

[docs/using-your-bible.md](docs/using-your-bible.md) covers where to put the bible in each kind of app, the routine that keeps it improving, and how to tell whether it is working.

## What is in a voice bible

- **The test.** One question to ask of every line: would you actually say this out loud?
- **Hard no's.** AI habits you have rejected, in your edits or in so many words.
- **Use sparingly.** Things you really do, with a ceiling so the AI does not do them in every paragraph.
- **Leave these alone.** Habits an editor would fix that are yours.
- **How you build sentences, paragraphs and whole pieces,** shown in your own quoted words.
- **Mechanics.** Sentence length, punctuation and other numbers.
- **Lexicon.** Words that are yours.
- **By context.** What changes between a post, an email and a how-to.
- **When editing your own drafts.** How much an AI may change, and what it must leave alone.
- **Before and after.** Your real edits to AI drafts.

Each rule is short and carries its evidence. Two entries from the made-up bookkeeper's bible:

```markdown
### 2. Warm-up openers `[strong]`

She cut the first sentence from all three AI drafts in the edit exercise.
Each was a greeting that delayed the point.

- ❌ "I hope this email finds you well and that your month is off to a great start."
- ✅ "Three of your invoices are more than 60 days late."

**What she does instead:** opens on the number or the deadline.
```

```markdown
## Leave these alone

- **Sentences that start with "Right." or "Now,"** `[strong]`
  "Right. Here is what to do with the ones I cannot read."
```

The blank version is [templates/voice-bible.template.md](templates/voice-bible.template.md).

## Why it is built this way

Each of these came from getting it wrong first. [docs/how-it-works.md](docs/how-it-works.md) has the longer account.

- **Nobody inherits a ban.** The list of [common AI tells](reference/ai-tells.md) is a set of questions to ask about your writing. If you have used em dashes for twenty years, they stay.
- **Protected habits matter as much as banned ones.** A list of prohibitions with nothing protected will slowly edit you out of your own writing.
- **Your edits say more than your descriptions.** What you change in a draft is better evidence of your habits than what you say you like. You still get the final word on every rule.
- **Every rule cites your words.** A rule with no quote behind it is a guess.
- **Written-down habits get overdone.** An AI that learns you like a certain move will use it constantly, so occasional habits carry limits.
- **The bible shapes material and cannot supply it.** Drafting starts from your notes, your stories and your numbers. The prompts tell the AI to ask you questions when you give it only a topic, and never to invent an anecdote.

This is for people who bring their own material and want help shaping it. Without what you know and what you change, the method has nothing to work from.

## For Claude Code and the Claude apps

[skill/voice-bible](skill/voice-bible/) packages the same prompts as a Claude skill. It runs the interview, reads your sample files, does the counting with a script instead of estimating, verifies every quote in the finished bible against your material, and saves everything to a folder.

In Claude Code, copy the folder into your personal skills directory:

```bash
cp -r skill/voice-bible ~/.claude/skills/
```

Then ask Claude to help you build your voice bible. For the Claude apps, zip the `voice-bible` folder and add it wherever your settings list skills.

## The scripts

All three need only Python 3.8 or newer.

```bash
# The numbers behind your writing: sentence lengths, punctuation, habits, common AI tells
python3 tools/voice_stats.py my-writing/

# Where a draft's numbers depart from yours
python3 tools/voice_stats.py --compare draft.md my-writing/

# Any quote in your bible that is not in your material word for word
python3 tools/check_quotes.py voice-bible.md interview.md edits.md my-writing/

# Any number, name or quotation in a draft that is not in the notes you gave the AI
python3 tools/check_invented.py draft.md notes.md
```

The counts are approximate, and they cannot tell you whether something sounds like you. They show where to look.

## Privacy

You will be pasting your own writing into whatever AI service you use, so check how that service handles what you give it. Change names and remove private details about other people before you paste. Your finished bible quotes you at length, so treat it as a personal document. If you build yours inside a copy of this repository, keep it in a folder named `my-voice/`, which git is set to ignore.

## Related projects

Other people are working on the same problem, and some of what is here follows their ideas.

- [write-like-me](https://github.com/Hiro-Inagawa/write-like-me) measures a large body of your writing and enforces the result with a tested checker. If you have 20,000 words or more of your own writing and you work in Claude Code, its checking is stricter than anything here. The check for invented numbers and names in this kit follows an idea in its checker.
- [inside-lago-voice-skill](https://github.com/getlago/inside-lago-voice-skill) is a short template you fill in yourself, built around the gap between what an AI drafted and what you sent. The section on editing your own drafts and the note on non-native English follow it.
- [mydamnvoice](https://github.com/rangrot/mydamnvoice) runs a quick multiple-choice interview and exports to several chat apps. The "this or that" sentence pairs in the interview follow its idea.
- [writing-style-skill](https://github.com/jzOcb/writing-style-skill) records each AI draft and your final version and extracts rules from the difference automatically. Its documentation is in Chinese.

If you only want the common AI habits removed and do not need the result to sound like one particular person, [humanizer](https://github.com/blader/humanizer) and [stop-slop](https://github.com/hardikpandya/stop-slop) are the widely used tools for that. This kit starts from the opposite assumption, that which habits to remove depends on who is writing.

## What is here

```
prompts/        the prompts to copy and paste (generated; do not edit)
reference/      the interview questions and the catalog of AI tells
templates/      the blank voice bible and voice card
docs/           how the method works and how to use the result
skill/          the Claude skill (generated; do not edit)
tools/          the three scripts, the build script and the tests
src/            sources for the prompts and the skill
```

## Changing the kit

The files in `prompts/` and `skill/` are assembled from `src/`, `reference/`, `templates/` and `tools/`. Edit those, then rebuild and run the tests:

```bash
python3 tools/build.py
python3 -m unittest discover -s tools -p "test_*.py"
```

## License

MIT. See [LICENSE](LICENSE).
