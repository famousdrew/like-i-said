# Like I Said

Build a voice bible: a short document that teaches an AI to write like you.

**Start here:** open [prompts/1-interview.md](prompts/1-interview.md), copy all of it and paste it into a new chat with any AI assistant. It takes 20 to 30 minutes. You finish with a transcript of how you actually talk, and everything else is built from that.

## Why

AI writing is easy to spot. (Not that there's anything wrong with it.) It's clean and competent and it sounds like everybody, which is a problem if you wanted to sound like you.

Asking for "my voice" doesn't work. The AI has never read you, and almost nobody can describe their own voice well enough to brief it.

So this kit collects evidence. You get interviewed, you fix a few AI drafts by hand and you hand over things you've written. Out comes a voice bible: what you never do, what you do that an editor would wrongly fix, and how your sentences get built, with the numbers. You give it to Claude, ChatGPT, Gemini or whatever you use before it writes for you.

The name is the test every line has to pass: would you actually say this out loud?

## What it changes

Same notes, two drafts. The bookkeeper is made up and so are both drafts.

**Her notes**

> 11 clients sent crumpled receipt photos AGAIN, could read maybe half. third month i've asked. be nice but they need to actually do it: lay it flat, whole receipt in the photo, one photo per receipt. if i can't read one i have to email them about it and that costs us both time. parking receipts too. thank the ones who do it right. need the rest by the 3rd.

**A default draft**

> Hello everyone! I hope this month is treating you well. I wanted to take a moment to talk about something small but incredibly important: receipt photos. Clear records aren't just about staying organized. They're about saving all of us valuable time. This month, several of you sent photos that were difficult to read, which means extra follow-up emails for everyone. Here's the good news: there's a simple fix! Just lay each receipt flat, capture the whole receipt, and take one photo per receipt (parking receipts included). A huge thank you to those of you who already do this. Please send any outstanding receipts by the 3rd. As always, don't hesitate to reach out with any questions!

**The same notes, drafted with her voice bible**

> Eleven of you sent me crumpled receipt photos again this month. I could read about half of them.
>
> Right. This is the third month I've asked, so I'm asking nicely one more time.
>
> 1. Lay the receipt flat.
> 2. Get the whole receipt in the photo.
> 3. Take one photo per receipt.
>
> That's all. When I can't read one I have to email you about it, and that costs us both time. (Yes, parking receipts too.)
>
> Thank you to everyone who already does this. Everyone else, I need yours by the 3rd.

Nothing's wrong with the first one, but anybody could have sent it. The second is hers: the number first, no greeting, numbered steps, one aside, the deadline last. Her bible lists each of those habits with a line of her own writing behind it.

## The four steps

About an hour in total. Any AI chat assistant works and there's nothing to install.

1. **Get interviewed (20 to 30 min).** Paste [1-interview.md](prompts/1-interview.md) into a new chat. Talk your answers out loud if you can and don't clean them up. You get `interview.md`.
2. **Fix three AI drafts (15 min).** In the same chat, paste [2-edit-exercise.md](prompts/2-edit-exercise.md). Rewrite each passage the way you'd say it. You get `edits.md`.
3. **Build the bible (10 min).** In a new chat, paste [3-build-bible.md](prompts/3-build-bible.md), then your interview, your edits and anything you've written. Answer its questions. You get `voice-bible.md`.
4. **Make the short version (2 min).** Say "card" in that chat. You get `voice-card.md`, sized for a small instruction box.

Short on time? Stop after step 1 and you still get a starter bible. Step 2 adds the most, because what you change in a draft is the strongest evidence there is.

No writing samples? Your side of old chats with an AI counts. You typed it and nobody polished it.

Rather answer the interview on your own? The questions are in [reference/interview-questions.md](reference/interview-questions.md).

## Use it

| When | Prompt |
|---|---|
| You want something drafted from your notes | [use-draft.md](prompts/use-draft.md) |
| You want a draft checked | [use-check.md](prompts/use-check.md) |
| You've edited a few AI drafts and want the bible to learn from them | [use-refresh.md](prompts/use-refresh.md) |

Where to put the bible in each app, and how to tell if it's working: [docs/using-your-bible.md](docs/using-your-bible.md).

## What's in a voice bible

Five sections matter most.

1. **The test.** Would you actually say this out loud?
2. **Hard no's.** AI habits you've rejected, by cutting them or by saying so.
3. **Leave these alone.** Habits an editor would "fix" that are yours.
4. **Use sparingly.** Things you really do, with a ceiling so the AI doesn't do them in every paragraph.
5. **Before and after.** Your real edits to AI drafts.

It also covers how you build sentences, your numbers, your words, what changes by context, and how an AI may edit your own drafts. The blank version is [templates/voice-bible.template.md](templates/voice-bible.template.md).

Every rule is short and carries its evidence. Two entries from the made-up bookkeeper's bible:

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
  "Right. This is the third month I've asked, so I'm asking nicely one more time."
```

## Why it's built this way

Each of these came from getting it wrong first. More in [docs/how-it-works.md](docs/how-it-works.md).

**Nobody inherits a ban.** Most tools strip every habit on a [list of things AI does](reference/ai-tells.md). This kit asks which of those are YOURS. If you've used em dashes for twenty years, they stay. The one exception is invented stories and numbers, which are out for everybody.

**Protected habits count as much as banned ones.** Give an AI only a list of don'ts and it removes your habits along with its own.

**Your edits beat your opinions.** What you change in a draft is better evidence than what you say you like. You still get the final word on every rule.

**Written-down habits get overdone.** Tell an AI you sometimes open with a question and every draft opens with a question. So occasional habits come with limits.

**You bring the material.** The bible shapes what you give it and can't supply it. Hand the AI only a topic and the prompts make it ask you questions first.

Tested so far: the build prompt, once, on a real person's writing. Not yet tested on a real person: the interview and the edit exercise. Details are at the bottom of [docs/how-it-works.md](docs/how-it-works.md).

## Claude Code and the Claude apps

```bash
cp -r skill/voice-bible ~/.claude/skills/
```

Then ask Claude to help you build your voice bible. The skill runs the same prompts, counts with a script instead of estimating, and checks every quote in the finished bible against your material. For the Claude apps, zip the `voice-bible` folder and add it wherever your settings list skills.

## The scripts

Python 3.8 or newer, nothing to install.

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

The counts are approximate and can't tell you if something sounds like you. They tell you where to look.

## Privacy

1. Check how your AI service handles what you paste into it.
2. Change names and take out private details about other people before you paste.
3. Treat your finished bible as a personal document. It quotes you at length.
4. If you work inside a copy of this repo, keep your files in `my-voice/`. Git ignores it.

## Related projects

Some of what's here follows other people's ideas.

- [write-like-me](https://github.com/Hiro-Inagawa/write-like-me) measures a large body of your writing and enforces the result with a tested checker. With 20,000 words of your own and Claude Code, it checks more strictly than this kit does. The check for invented details follows its idea.
- [inside-lago-voice-skill](https://github.com/getlago/inside-lago-voice-skill) is a short template you fill in yourself. The section on editing your own drafts follows it, and so does the note on non-native English.
- [mydamnvoice](https://github.com/rangrot/mydamnvoice) runs a quick multiple-choice interview. The "this or that" sentence pairs follow its idea.
- [writing-style-skill](https://github.com/jzOcb/writing-style-skill) pulls rules out of your edits automatically. Its documentation is in Chinese.

Only want the common AI habits removed? [humanizer](https://github.com/blader/humanizer) and [stop-slop](https://github.com/hardikpandya/stop-slop) do that. This kit assumes the habits worth removing depend on who's writing.

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

Edit `src/`, `reference/`, `templates/` or `tools/`. The files in `prompts/` and `skill/` are assembled from those. Then rebuild and run the tests:

```bash
python3 tools/build.py
python3 -m unittest discover -s tools -p "test_*.py"
```

## License

MIT. See [LICENSE](LICENSE).

**Next:** open [prompts/1-interview.md](prompts/1-interview.md) and paste it into a new chat.
