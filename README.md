# Like I Said

A kit for building a voice bible, which is a reference document that teaches an AI to write like you.

You can spot AI writing from across the room these days. (Not that there's anything wrong with it.) It's clean and competent and it sounds like everybody, which is a problem if you were hoping to sound like you.

Telling the AI to "write in my voice" doesn't get you very far. It has never read you and, honestly, almost nobody can describe their own voice well enough to brief a stranger on it.

So this kit skips the describing and goes after evidence. You get interviewed about your work, you fix a few AI drafts by hand and you hand over some things you've written. What comes out is a voice bible. It's a few pages on what you never do, what you do that an editor would wrongly fix and how your sentences get built, with the numbers behind all of it. You give that to Claude, ChatGPT, Gemini or whatever you use before it drafts or edits anything for you.

The name comes from the one test every line has to pass: would you actually say this out loud?

## What it changes

Both drafts below came from the same few lines of notes. The bookkeeper is made up and so is the pair, so treat it as an illustration. A real one comes from your notes and your bible.

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
> That is enough for me and anyone else. (Yes, even the parking ones.)
>
> Next one of these is due on the 3rd.

Nothing's wrong with the first draft. It could have been written for anybody. The second one is hers, with the number up front and no greeting, the steps numbered, one dry aside, and the next date sitting where a sign-off would go. Her bible lists every one of those habits and puts a line of her own writing behind each.

## What you need

About an hour and any AI chat assistant. That's it.

It works better if you bring a few things you wrote yourself, like emails or posts. Whatever you wrote with no AI help is the most useful. If you don't have much of that, your side of old chats with an AI counts, since you typed it and nobody polished it.

There's nothing to install and no code to run. Every step is a prompt you copy and paste.

## Build yours

| Step | Prompt | Time | You save |
|---|---|---|---|
| 1. Get interviewed | [1-interview.md](prompts/1-interview.md) | 20 to 30 min | `interview.md` |
| 2. Fix three AI drafts | [2-edit-exercise.md](prompts/2-edit-exercise.md) | 15 min | `edits.md` |
| 3. Build the bible | [3-build-bible.md](prompts/3-build-bible.md) | 10 min | `voice-bible.md` |
| 4. Make the short version | [4-voice-card.md](prompts/4-voice-card.md) | 2 min | `voice-card.md` |

**Step 1.** Open the interview prompt, copy the whole thing and paste it into a new chat. The AI asks about your work and what you actually think, one question at a time. It won't ask you to describe your style (you'd get it wrong, we all do). Talk your answers out loud with dictation if you can, and don't clean up what comes out. Near the end it shows you a few pairs of sentences and asks which one sounds more like you, and then it hands you a transcript to save. If you'd rather answer on your own time, the questions are in [reference/interview-questions.md](reference/interview-questions.md).

**Step 2.** Stay in the same chat and paste the edit exercise prompt. The AI writes three short passages about things you just told it, in its own style, and you rewrite each one the way you'd say it. Don't be polite about it. What you change is the strongest evidence in the whole process, so if you only have time for one extra step then make it this one.

**Step 3.** Open a new chat. Paste the build prompt, then your interview, your edits and whatever writing samples you have. If you ran the stats script described below, paste its report too. Tell it which samples you typed and which you dictated, which are finished and which are rough, and whether an AI helped draft any of them. Before it writes anything it shows you what it plans to ban and what it plans to protect, and it asks a few questions. Then you get your bible.

**Step 4.** Say "card" in that same chat and you get a version short enough for a small instruction box.

You can stop after step 1 and still walk away with a starter bible. Every extra kind of evidence makes it sharper.

## Use it

| When | Prompt |
|---|---|
| You want something drafted from your notes | [use-draft.md](prompts/use-draft.md) |
| You want a draft checked | [use-check.md](prompts/use-check.md) |
| You have edited a few AI drafts and want the bible to learn from them | [use-refresh.md](prompts/use-refresh.md) |

[docs/using-your-bible.md](docs/using-your-bible.md) covers where to put the bible in each kind of app, the routine that keeps it getting better, and how to tell if it's working.

## What is in a voice bible

- **The test.** One question for every line: would you actually say this out loud?
- **Hard no's.** AI habits you've rejected, in your edits or in so many words.
- **Use sparingly.** Things you really do, with a ceiling so the AI doesn't do them in every paragraph.
- **Leave these alone.** Habits an editor would "fix" that are yours.
- **How you build sentences, paragraphs and whole pieces,** shown in your own words.
- **Mechanics.** Sentence length, punctuation and the rest of the numbers.
- **Lexicon.** Words that are yours.
- **By context.** What changes between a post, an email and a how-to.
- **When editing your own drafts.** How much an AI gets to change, and what it has to leave alone.
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

Every one of these came from getting it wrong first. The longer version is in [docs/how-it-works.md](docs/how-it-works.md).

**Nobody inherits a ban.** Most tools for this hand you a list of things AI does and strip all of them out. This kit treats that [list](reference/ai-tells.md) as questions to ask about YOUR writing. If you've been using em dashes for twenty years then they stay.

There's one exception, though, and it's making things up. An invented story or number is a hard no for everybody. An AI that puts a story in your mouth has done something worse than sound like a robot.

**Protected habits matter as much as banned ones.** Give an AI a list of don'ts and nothing else and it will slowly edit you out of your own writing.

**Your edits say more than your opinions do.** What you change in a draft is better evidence of your habits than what you say you like. But you still get the final word on every rule.

**Every rule cites your actual words.** A rule with no quote behind it is a guess.

**Habits get overdone the minute they're written down.** Tell an AI that you sometimes open with a question and every draft opens with a question. So the occasional stuff comes with limits.

**The bible can't supply the material.** It shapes what you bring. Drafting starts from your notes and your stories. And if you hand the AI nothing but a topic, the prompts tell it to ask you questions first.

This is for people who show up with their own material and want help shaping it. If you don't bring what you know and what you'd change, there's nothing here for the method to work with.

For the record, not all of this has been road-tested. The build prompt has had one full run on a real person's writing. The interview and the edit exercise haven't been tried on a real person yet. The details are at the bottom of [docs/how-it-works.md](docs/how-it-works.md).

## For Claude Code and the Claude apps

[skill/voice-bible](skill/voice-bible/) is the same set of prompts packaged as a Claude skill. It runs the interview, reads your sample files and counts with a script instead of estimating. It also checks every quote in the finished bible against your material and saves everything to a folder.

In Claude Code, copy the folder into your personal skills directory:

```bash
cp -r skill/voice-bible ~/.claude/skills/
```

Then ask Claude to help you build your voice bible. For the Claude apps, zip the `voice-bible` folder and add it wherever your settings list skills.

## The scripts

All three run on plain Python 3.8 or newer, with nothing to install.

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

The counts are approximate and they can't tell you if something sounds like you. They tell you where to look.

## Privacy

You're going to be pasting your own writing into whatever AI service you use, so check how that service handles what you give it. Change names and take out private details about other people before you paste. Your finished bible quotes you at length, so treat it like a personal document. If you build yours inside a copy of this repo, keep it in a folder named `my-voice/`, which git is set to ignore.

## Related projects

Other people are working on the same problem, and some of what's here follows their ideas.

- [write-like-me](https://github.com/Hiro-Inagawa/write-like-me) measures a big pile of your writing and enforces the result with a tested checker. If you've got 20,000 words or more of your own writing and you work in Claude Code, its checking is stricter than anything here. The check for invented numbers and names in this kit follows an idea in its checker.
- [inside-lago-voice-skill](https://github.com/getlago/inside-lago-voice-skill) is a short template you fill in yourself, built around the gap between what an AI drafted and what you actually sent. The section on editing your own drafts and the note on non-native English follow it.
- [mydamnvoice](https://github.com/rangrot/mydamnvoice) runs a quick multiple-choice interview and exports to several chat apps. The "this or that" sentence pairs in the interview follow its idea.
- [writing-style-skill](https://github.com/jzOcb/writing-style-skill) records each AI draft and your final version and pulls rules out of the difference automatically. Its documentation is in Chinese.

If all you want is the common AI habits stripped out and you don't care if the result sounds like one particular person, [humanizer](https://github.com/blader/humanizer) and [stop-slop](https://github.com/hardikpandya/stop-slop) are what most people use. This kit makes the opposite bet - the habits worth stripping depend on who's writing.

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
