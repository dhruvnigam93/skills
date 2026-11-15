---
name: storyboard
description: >-
  Write and revise a talk's storyboard: one entry per slide, each with a stable
  ID, a title that states the point, the time it takes, a description of what
  the audience sees, beats as speaker cues, and any lines that must land.
  Checks it against the craft principles and the time budget. Every structural
  change to the talk goes through this skill, including changes that come from
  rehearsals and reviewer feedback. Use whenever someone wants to turn a talk
  narrative or outline into slides-to-be, plan slide by slide, "storyboard my
  talk", "outline the slides", "apply these changes to the storyboard", "is my
  talk too long", "cut two minutes", or "/talk:storyboard". Use it before
  building any slides.
argument-hint: "[draft | revise | check]"
---

# Storyboard

`storyboard.md` is the talk's structure in text: the cheapest form it will ever take. Every change made here costs minutes; the same change made to built slides costs hours. That is why visuals and slides wait until the structure freezes.

The format and its checks are in `../../references/storyboard-format.md`. The craft principles are in `../../references/craft.md`. Read both before writing.

## Rules

- Align first: ask questions one at a time, as multiple choice, with the recommended answer first.
- Structure, don't invent. The spine and keep lines in `narrative.md`, plus `facts.md`, are the only sources.
- Slide IDs are stable for life.
- Once slides have been handed off (`Slides owner: slides` in `STATE.md`), stop editing the storyboard directly. Changes go into the slides, and `talk:build` syncs them back.
- Update `STATE.md` at the end.

## Draft

1. **Read** `talk.yaml`, `narrative.md` (the spine first), `facts.md`, and any `feedback.md`.

2. **Align** on up to three questions:
   - **Tone:** show three sample titles for the same slide in different registers (plain, wry, bold) and let the speaker pick.
   - **Density:** roughly how many slides per minute. One to two is typical; demos and diagrams run slower.
   - **Recurring elements:** which one to three devices will return through the talk. Propose candidates from the spine, such as a map of the journey, the yardstick, or a diagram that comes back changed.

3. **Lay out the sections** from the spine, in order. Each one should:
   - open with the human problem;
   - make the promise near the start of the talk and pay it off at the end;
   - give each recurring element a set-up before its first payoff.

4. **Write the slides** in the format:
   - a title that states the point;
   - a visual that is described, not designed;
   - one to three beats;
   - Lines taken from the keep lines;
   - an estimated time.

   Then compute the section totals and the **Planned** total.

5. **Check coverage against the spine.** List every keep line, section point and link from `narrative.md` that has no slide yet. Ask the speaker about each one: place it, or move it to the cut list.

6. **Run the checks** in the format reference and fix what fails. When **Planned** is over target, propose specific cuts, ranked by how little each one costs the argument. Don't squeeze the timings to make the sum fit.

7. **Do a titles-only read.** Show the titles in order, with nothing else. If they don't tell the story on their own, fix the titles before anything else.

8. **Approve.** Once the speaker signs off:
   - set the stage to `loop-a`;
   - log the approval and check in;
   - tell the speaker what Loop A involves: talk it through out loud (`talk:rehearse` in structure mode) and send the storyboard to an outside reviewer (`talk:feedback`).

   Reviewing a storyboard is quick, which makes it the cheapest point to hear "this part loses me".

## Revise

Use this for changes that come from `talk:rehearse`, from `talk:feedback`, or from the speaker directly.

1. Take the approved changes one at a time. Tag each one with its source ID, for example `F12` or `R3-7`.
2. Apply it, following these rules:
   - Keep IDs.
   - A new slide gets a new ID.
   - A removed slide moves to the cut list with its reason. Nothing is deleted silently.
   - A rename keeps the ID.
3. Recompute the times. If the structure changed (a section's point, its order or a link between sections), update the spine in `narrative.md` too.
4. Log each change in the **Changes** table.
5. Run the checks. Report the new **Planned** time and what moved.

**After the structure freeze**, a structural change needs explicit agreement. Say that it breaks the freeze, and name the visuals and slides that would have to be redone.

**Within `freeze.content_hours_before` of the talk**, accept only cuts and changes to wording.

## Check

Run the checks in the format reference on their own and report the result, without changing anything.
