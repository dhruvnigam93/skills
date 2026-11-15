# Craft principles

Use these to judge the spine, the storyboard and every revision. Each one comes with a test, so that you check it rather than claim it.

## Shape

**A journey, not a list.** A talk that moves people is one argument, where each part causes the next. A list of tips is forgotten by the coffee break.
- *Shuffle test:* reorder the sections. If nothing breaks, it's a list.
- *Transition test:* each link between sections reads as "but" or "therefore" ("fixing X revealed Y"), never "and next".

**Threes.** People hold about three things.
- At most three sections.
- At most three criteria in a yardstick.
- At most three beats on a slide.
- *Test:* count them.

**A promise early, kept at the end.** Within the first two minutes, say what the audience will be able to do, see or decide by the end. The ending pays that promise off explicitly.
- *Test:* quote the promise and the payoff side by side. The payoff must answer the promise.

**Stated against a belief.** The thesis is sharper when it contradicts something the audience already believes ("the usual advice is X; here's why it failed us").
- *Test:* name the belief in one sentence.

## Slides

**One point per slide, and the title states it.** Write the title as a claim ("Retries doubled our load"), not a topic ("Retries"). The slide shows. The speaker tells.
- *Test:* reading the titles alone, in order, tells the story.

**Beats are cues, not a script.** At most three bullets, each at most ten words. They remind the speaker what to say. They are not what the speaker reads.
- *Test:* count the bullets and the words.

**Describe visuals, don't design them.** The storyboard says what the audience should see and notice. The style lives in `talk.yaml` and the style sheet.

## Memory

**Recall over novelty.** Reuse a small set of recurring elements so the audience recognises them and builds on them. Examples are a map of the journey, a yardstick applied to each attempt, or a diagram that returns crossed out. A new visual on every slide makes the audience start over each time.
- *Test:* every recurring element is set up before its first payoff, and returns at least twice.

**The human stakes before the mechanism.** Open each section with the problem as a person feels it. Only then show how it works.
- *Test:* the first slide of each section names a person, a moment or a cost.

**An emotional beat in each section.** This can be surprise, frustration, relief or a laugh. Without one, the section is a lecture.

## Truth

**Every claim has a source.** Every number, quote or named result on a slide is in `facts.md`, and is cleared to share.
- *Test:* look up each one.

**The speaker's words win.** When the speaker says something better in a talk-through than the plan had it, the plan changes to match.

## Length

**Plan for less than the slot.** Aim for about 90% of the talk time. A live talk runs longer than a rehearsal, because of applause, clicker trouble and a question nobody planned for.
- *Test:* the storyboard's planned total is at or under `slot.target_minutes`.
