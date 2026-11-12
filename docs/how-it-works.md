# How it works

This kit came out of months of using a voice bible for real writing, and most of what follows was learned by getting it wrong first. Each section says what the kit does and what goes wrong without it. The details of that writing are left out, and the examples below are made up to illustrate.

## The interview asks about your work, not your style

Ask someone to describe their writing voice and you get adjectives: conversational, direct, a bit funny. An AI cannot do anything with those, and they are often wrong.

So the interview asks for stories, opinions and explanations, and the transcript becomes the evidence. How you phrase an answer about a bad week at work says more about your voice than anything you could say about your style.

The only style questions come at the end, and they are recorded separately as things you said you want.

## Every rule cites your words

A voice bible written from impressions is a list of guesses, and a guess drawn from a small sample is often wrong. A rule might say you never start a sentence with "And." A look at more of your writing then finds one in every piece.

So each rule carries an exact quote and a tag saying how much evidence is behind it. Things seen only once sit in an "Unconfirmed" section until they show up again. When the bible and your real writing disagree, the writing wins and the rule changes.

Quotes are copied character for character. A tidied quote is a small lie about how you write, and every later draft will imitate it. The quote checker in `tools/` exists because models tidy quotes without meaning to.

## Common AI habits get sorted into three piles

It is tempting to hand an AI a list of things to avoid: no em dashes, no "it's not X, it's Y," no lists of three. That produces writing that avoids a list. It does not produce your writing, and it can remove habits that are yours.

Suppose you never use exclamation points, and where someone else would use one you write a flat one-word sentence. A reviewer who knows only the ban has no reason to protect that short sentence, and may tidy it away. Or suppose a rule against one overused construction is written a little too broadly, and every plain contrast you make gets flagged along with it. A list of bans with nothing protected slowly edits a person out of their own writing.

So each item in the [catalog of tells](../reference/ai-tells.md) is checked against your writing and lands in one pile:

- **Hard no.** You say you do not want it, or you remove it from drafts and never write it yourself.
- **Use sparingly.** You do it, and an AI overdoes it, so it gets a ceiling.
- **Leave alone.** You do it, and an editor would wrongly fix it, so it is protected.

A habit that never appears in a good-sized sample of your writing is listed as absent, with no entry of its own. If there is too little writing to tell, it is left out.

The catalog is a starting list. Wikipedia's editors keep a longer field guide, [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), written for spotting undisclosed AI text in articles. It makes the same caution: each sign is only a possible sign, and people do all of them too.

## Your edits are the best evidence

The edit exercise has an AI write short passages in its default style, and you rewrite them. Nothing else shows the gap as directly.

A typical change is small: two short sentences joined with "but," or a tidy closing line deleted. You would not think to mention either in an interview, because you do not know you have the preference until you see the alternative.

What you change says more than what you say you like.

## Talking and writing are measured separately

Dictated answers run long and loose. The same person's spoken sentences can be nearly twice as long as their written ones, and a bible that took its sentence length from an interview would be far off.

The build prompt takes how you tell stories, how you argue and your humor from everything. It takes sentence length, punctuation and formatting only from things you typed. Rough notes are compared with finished pieces for the same reason: filler words and run-ons show up when you talk and get edited out when you write, and the bible should not put them back.

## Some evidence outranks other evidence

A piece that an AI drafted and you edited is weaker evidence than something you typed alone. It shows what you were willing to accept, and it carries some of the AI's habits along with yours. A bible that treats the two as equal can contradict itself. It bans a habit because you removed it in an edit, and then reports that your writing is full of it.

So the prompt ranks its sources. What you say in the chat comes first, then your edits to AI drafts, then things you typed with no AI help, then pieces an AI helped draft that you edited and published, then dictated material.

It also has a rule for the commonest conflict. If you removed something in an edit and it also shows up in your own writing, you do it and the AI did it too much. That calls for a ceiling.

## Habits you have occasionally get ceilings

Once a habit is written down, a drafting model performs it. If the bible says you sometimes open with a question, every draft opens with a question. The habit is real and the frequency is fake.

Three things in the kit push against this:

- Occasional habits live in a "Use sparingly" table with a number attached.
- The lexicon is described as a check. A long draft with none of your words has been smoothed too far, and a draft that uses all of them is doing an impression.
- The drafting prompt tells the AI that the bible describes what happens naturally, and that it should never build a move on purpose.

## Checking looks for what is missing

A draft can avoid every banned habit and still not sound like you, because everything that made it yours has been sanded off. Repeated checking makes this worse, since each pass removes a little more.

So the check prompt also asks what is absent: asides, informal words, opinions, specifics. The stats script lists your habits that a draft lacks. Neither tells the AI to add them. They tell you where the draft went flat.

## The bible cannot supply the substance

This was the most expensive lesson. A draft built from a paragraph of notes and a thorough voice bible comes out fluent and thin. More checking does not fix it, and more of your own material does.

A voice bible shapes material. It has no material of its own. So the drafting prompt refuses to draft from a bare topic and asks three to six questions first: a real moment, a real number, what you actually think. It tells the AI to keep your wording where it can, and to mark gaps instead of filling them. An invented anecdote in your name is the one thing that is a hard no for everyone. `tools/check_invented.py` backs the instruction with a check: it lists every number, name and quotation in a draft that is not in your notes.

## Each draft starts from the source

It is tempting to give an AI last week's approved draft as the style to match. Do that a few times and each piece drifts further from you, the way a photocopy of a photocopy loses detail. Start every drafting session from the bible and your raw material. Earlier AI drafts are never the reference, including good ones.

## Voice changes with the job

Rules drawn from one kind of writing go wrong when they are applied to another. A story-first opening and casual asides suit a public post. They work against a reference document that someone will consult every month, where headings and lists are doing a job.

So a bible has a section on context. Some things hold everywhere, and others change between a public post, a work email and a set of instructions, where voice mostly steps aside and clarity wins.

## You decide

The check prompt fixes typos without asking and flags everything about voice for you to answer. It flags lines that break your own rules even when you wrote them, and you are free to keep them. People overrule their own bibles on purpose all the time. What matters is that the choice is yours and made knowingly.

## It is never finished

A rule that came from a small sample should go when more writing contradicts it. The refresh prompt proposes additions, tighter and looser limits, new protections and removals, each with evidence, and waits for a yes or no on each.

The loop only works while it runs. It is easy to stop saving your edits once the drafts are good enough, and the bible stops improving at that point. Saving a before and after takes a minute, so the kit makes it part of the drafting routine.

## What the numbers can and cannot do

`tools/voice_stats.py` counts sentence lengths, punctuation, contractions, repeated phrases and the tells that can be matched by pattern. Counting by hand is unreliable, and so is a model estimating from a long text. A target such as "sentences average 15 words" is worth little unless something counted it.

The counts are still rough. Sentence splitting is rule-based, and the patterns match loosely. They cannot tell you whether a paragraph sounds like you, and reading it out loud is still the way to find out.

## How the kit has been tested

The scripts have unit tests. The build prompt has had one full run on a real writer's material, by an AI assistant that could not run code. The material was an interview, a few finished pieces, some rough notes and a set of edit pairs.

- The quote checker went through about 270 quoted passages in the bible that came out and found no invented quotes.
- The assistant's hand counts were within a few percent of the script's. It counted every sentence, which most chat sessions will not do.
- It reported about forty places where the prompt was unclear or contradicted itself. The worst are described in the section on ranking evidence above. Those were fixed. A second reader then checked the revised prompt against sixteen specific cases and found a few places where two rules still overlapped, and those were fixed too. The revised prompt has not yet had a second full run.

The interview and edit exercise prompts have not been tested with real people yet. That includes the "this or that" round and the section on editing your own drafts, which were added later.

## Evidence levels

| Level | What went in | What to expect |
|---|---|---|
| Starter | One kind of material, or under 1,500 words that you typed | A short bible. Good on stories, opinions and how you argue, weak on mechanics. |
| Solid | 1,500 words or more that you typed | Rules backed by quotes, with real numbers. |
| Strong | That, plus your edits to AI drafts | A before-and-after table, and rules about things you did not know you cared about. |

Start wherever you are. Each refresh moves it up.
