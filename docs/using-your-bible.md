# Using your voice bible

You have `voice-bible.md` and maybe `voice-card.md`. This page covers where to put them, the routine that keeps them improving, and how to tell whether they are working.

## Where to put it

The names and menus in these apps change often, and so do their size limits, so this section describes the kinds of places to look. Use whichever your assistant has.

**A project or workspace.** Most assistants let you create a space with its own instructions and attached files, and every chat started inside it sees both. Claude and ChatGPT both call these Projects. This is the best home for the full bible. Attach `voice-bible.md` as a file, and put one line in the project's instructions: "Before drafting or editing anything for me, read voice-bible.md and follow it."

**A custom assistant.** Some apps let you build a saved assistant with instructions and reference files, such as a GPT in ChatGPT or a Gem in Gemini. Set it up the same way: the bible as a file and a one-line instruction pointing at it.

**A custom instructions box.** This is the setting that applies to every chat. These boxes are small, in some cases 1,500 characters, and the full bible will not fit. Paste the voice card, which is built for that size. The card covers the most important points and nothing else, so expect less from it than from the full bible.

**Pasted into the chat.** This works everywhere. The drafting, checking and refresh prompts each end with a place for the bible. Paste it there or attach the file.

**A coding assistant.** If you write in an editor with an AI assistant that reads a project instructions file, point that file at the bible. With Claude Code, the [skill](../skill/voice-bible/) handles this.

Two things apply everywhere:

- **Start a new chat for each piece.** In a long conversation, the assistant starts imitating its own earlier drafts and the bible fades.
- **Do not hand it an earlier AI draft as the style to copy.** Give it the bible and your notes every time.

## The routine

1. **Collect your raw material.** Talk into a voice memo, jot notes, or paste a rough outline. Rough is fine. The stories, numbers and opinions have to come from you.
2. **Draft** with [use-draft.md](../prompts/use-draft.md). If you give it only a topic, it will ask you questions first. Answer them.
3. **Edit by hand.** Change whatever is wrong. This is where the piece becomes yours.
4. **Save the before and after.** Paste the AI's draft and your version into a running file. This takes a minute and it is the step people skip.
5. **Check** with [use-check.md](../prompts/use-check.md) if you want a second look. It fixes typos, and it flags voice issues as a numbered list for you to answer.
6. **Refresh** with [use-refresh.md](../prompts/use-refresh.md) once you have three or four saved pairs. It proposes changes to the bible and you say yes or no to each.

The first few refreshes change the most. After that the bible settles and you can refresh every month or two.

## Is it working?

**Read the draft out loud.** This is the test at the top of every bible, and it is the best one. Where you stumble or wince, the draft has left your voice.

**Run the same notes twice.** Give the assistant your notes with the bible, then in a fresh chat without it. If you cannot tell which is which, the bible is not being read, or it is too thin to matter.

**Count your edits.** If you are changing less in each new draft than you did a month ago, it is working. If you keep making the same change, that change belongs in the bible. Run a refresh.

**Ask someone who knows your writing.** Give them three paragraphs you wrote and three the AI drafted with your bible, mixed up, and see whether they can sort them.

**Compare the numbers,** if you are comfortable in a terminal:

```bash
python3 tools/voice_stats.py --compare draft.md my-writing/
```

This shows where a draft's sentence lengths, punctuation and habits depart from yours. It cannot judge whether the draft sounds like you.

**Check for invented details.** A second script lists every number, name and quotation in a draft that is not in the notes you gave the AI:

```bash
python3 tools/check_invented.py draft.md notes.md
```

It is a rough filter and will sometimes flag an ordinary capitalized word. Anything it lists that you did not say is something the AI made up.

## When something is off

**The drafts still sound like AI.** Check that the assistant can see the bible: ask it to quote your first hard no. If it can, start a new chat, since long chats drift. If you are using only the voice card, move to the full bible in a project.

**The drafts sound like an impression of me.** The assistant is performing your habits. Run a refresh with the drafts and your edits, and it will add or lower the ceilings in "Use sparingly." Also check that you gave it enough raw material. With little to say, it fills space with your mannerisms.

**It keeps fixing something I do on purpose.** Add that habit to "Leave these alone," with an example. The refresh prompt calls this "Protect."

**The check flags a rule I broke on purpose.** Keep your line. The bible describes your habits and does not outrank you. If you overrule the same rule several times, the rule is wrong, and the next refresh should loosen it.

**The draft is fluent and says nothing.** The draft needed more of your material, and the bible cannot supply it. Answer the drafting prompt's questions at more length, with a real example.

**My bible is short.** That is correct for the evidence you gave it. Add finished writing and saved edits, then refresh. A short bible that is true is more use than a long one padded with guesses.

**Different kinds of writing come out the same.** Fill in "By context." Give the build or refresh prompt samples of each kind and say which is which.

## Privacy

Your bible quotes you at length and may mention people you work with. Treat it as a personal document, and use names you are comfortable sharing. Before you paste writing samples into an AI service, check how that service handles what you give it, and remove private details about other people.
