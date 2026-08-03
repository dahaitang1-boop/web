---
title: Memoir writer
oneLiner: An interview-first writing workflow with a style spec distilled from a decade of the author's own prose, and no invented details.
role: sole author
period: '2026'
stack:
  - Prose-as-spec
  - Structured interview workflow
  - Style profile with a feedback loop
repoStatus: private
status: published
order: 6
metrics:
  - label: Source corpus
    value: 2014–2026
    note: a decade of the author's own essays and travel writing, used to derive the voice
  - label: Invented details permitted
    value: '0'
    note: every detail must trace to an interview transcript or a source text
  - label: Chapter length
    value: 800–2,500
    note: words. Short over padded, enforced as a check not a suggestion
sanitized: true
reviewed: 2026-07-27
---

## The failure mode this is built against

Ask a language model to write a chapter of someone's life story and you get competent, fluent, generic prose. It will fill gaps you did not tell it about. It will smooth a specific memory into a familiar shape. It will produce something that reads well and is not true, and the person whose life it is will not be able to say precisely what is wrong — only that it is not theirs.

Both halves of that failure have the same root: **the model is being asked to write before it has anything to write from.** So the workflow makes that structurally impossible.

## Interview before drafting, always

Drafting cannot begin until an interview has happened. The interview turns a one-sentence memory into a scene, and it asks for things a model cannot invent:

- **Sensory anchors** — colour, smell, sound, temperature, what was eaten, what it cost, what brand it was
- **Actual words** — who said what, in which dialect, phrased how
- **Gesture** — what were their hands doing; a characteristic tic or catchphrase
- **Place and time** — season, weather, room layout, the route taken
- **The gap** — what you believed then against what you understood later
- **Where it ended up** — what became of that object, that person. The afterwards is very often the ending.

Two rules govern the transcript. **Spoken answers are recorded close to verbatim** — the roughness of speech is the raw material, and "tidying it up" at the recording stage destroys the thing you came for. And **"I don't remember" is recorded as "I don't remember"**, tagged as such. A memoir is allowed to say the author has forgotten. It is not allowed to make something up.

## The style profile, and why it improves

Voice is defined by a separate specification derived from the author's own writing across 2014–2026 — not a description of good prose, but a description of *this* prose: its habits, its tells, its failure modes.

It carries explicit prohibitions, and they are the useful part because each names a specific way this author's writing goes wrong under pressure:

- End on the thing that happened, not on what it means
- No essay register — none of the throat-clearing that precedes an argument
- Empty adjectives get replaced by a noun or an action
- At most one abstract noun per chapter
- Loanwords capped, counted

The mechanism that makes the system improve is the feedback loop. **After every editing pass, what the author changed and why is distilled into one to three new rules and appended to the style profile.** Not a note about the chapter — a rule for the next one. This step is marked as non-skippable, because it is the only reason the output converges on the author's voice instead of hovering near a general-purpose one forever.

That is the transferable idea: a style guide that is *written once* decays, because the interesting corrections are the ones you did not anticipate. A style guide that absorbs each round of edits becomes a genuine model of a specific writer, and it does it using the cheapest possible signal — the diff between what was drafted and what was kept.

## Provenance as a hard constraint

Every detail in a finished chapter must trace to either an interview transcript or a document in the source corpus. When a detail is missing, the instruction is not to write around it — it is to go back and ask.

This is slower. It is also the only version of this tool worth having. A memoir is a claim about what happened, made to the people in it, and a system that produces plausible filler produces something the author cannot honestly sign.

## Why there is nothing to show

The output is a private autobiography and will not be published — not in excerpt, not as a sample. What is portable is the shape: **interview → draft under an explicit voice spec → edit → distil the edit back into the spec.**

I have since reused that pattern for work with nothing to do with memoir. Any task where quality means *matching a particular person's judgement* rather than meeting a general standard has the same structure, and the same answer: stop describing the target, and start harvesting the corrections.
