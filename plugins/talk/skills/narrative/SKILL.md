---
name: narrative
description: >-
  Find the story of a talk before any slide exists. Turns source material, a
  brain dump and a spoken talk-through into a one-page spine (the thesis, the
  promise, at most three sections each causing the next, and the ending), then
  into prose in the speaker's own words, and tests that it is a journey rather
  than a list. Also writes call-for-papers abstracts and proposals from the
  spine. Use whenever someone has notes, a project or an idea and wants to work
  out what their talk is about: "what's my talk's story", "help me structure my
  talk", "turn these notes into a talk", "my talk feels like a list", "write my
  CFP abstract", "/talk:narrative". Use it before storyboarding or making
  slides.
argument-hint: "[path to brain dump or talk-through]"
---

# Narrative

A talk is found by saying it, not by outlining it. This stage turns what the speaker knows into an argument they can say from memory. It produces `narrative.md`, which has two parts:
- the **spine**: one page, which stays live for the life of the talk;
- the **prose**: the talk as the speaker would say it, used as a reference once the storyboard exists.

Judge everything here against the craft principles in `../../references/craft.md`.

## Rules

- Align first: ask questions one at a time, as multiple choice, with the recommended answer first.
- Structure, don't invent: every sentence traces back to the speaker, `raw/` or `facts.md`. List anything of the speaker's that you cut or merged, and get it confirmed.
- Save talk-throughs and brain dumps to `raw/` before using them.
- Update `STATE.md` at the end.

## Steps

1. **Read** `talk.yaml`, `facts.md` and everything in `raw/`.

2. **Align** on up to three of these, whichever the files leave open:
   - the one thing the audience should leave with;
   - the belief the talk pushes against;
   - how it ends: the last image or line.

   Offer candidates drawn from the material. Don't ask the speaker to write them from nothing.

3. **Get a talk-through.** Ask the speaker to talk through the talk for 5 to 10 minutes, with no slides and no notes, as if explaining it to a friend. Turn the recording into text with `tools.transcription`; if that is blank, ask how once and record the answer. Save the recording and the text to `raw/`.

   This is the most valuable input in the whole framework. What the speaker says unprompted is the talk. If they can't record one, work from a written brain dump and note in `STATE.md` that a talk-through is still owed.

4. **Keep the good lines.** Pull out the phrases, examples and moments that land, word for word. These are the raw material for the storyboard's Lines.

5. **Write the spine** at the top of `narrative.md`, on one page:

   ```markdown
   ## Spine
   **Thesis:** <one sentence, stated against the belief the audience holds>
   **Why it matters to people:** <the human cost, felt before any mechanism is explained>
   **Promise:** <what the audience will be able to do, see or decide by the end>
   **Yardstick (optional):** <≤3 criteria the audience uses to judge each attempt or idea>
   **Sections:**
   1. <name>: <point>. Link → <how this one causes the next: "fixing X revealed Y">
   2. ...
   3. ...
   **Ending:** <how the promise is paid off; the last line>
   **Keep lines:** <the best verbatim lines from step 4>
   **Cut list:** <what's out, and why; this feeds the Q&A bank>
   ```

6. **Write the prose** under `## Prose`. Use the spoken register: short sentences, the speaker's own phrasing, no new facts. Aim for `slot.target_minutes × pace.plan_wpm` words.

7. **Run the tests** and show the results:
   - **Shuffle:** can the sections be reordered without breaking anything? If yes, rework the links until they can't.
   - **Transition:** is every link a "but" or a "therefore", never an "and next"?
   - **Cold reader:** give only the prose to a fresh helper with no other context, and ask for a three-sentence summary. Compare it with the thesis, promise and ending. A mismatch means the prose doesn't say what the spine intends.
   - **Claims:** every number and named result has a row in `facts.md`.
   - **Length:** the word count is within 10% of the target.

8. **Get a second opinion.** Have a fresh helper read the spine as a sceptical member of the audience. Ask it three things: where did it stop caring, what would it challenge, and what did it expect that never came? Save the critique to `raw/`, then triage it as in `talk:feedback`.

9. **Approve.** The speaker signs off on the spine. Then:
   - set the stage to `storyboard`;
   - add the approval to the decisions log;
   - check in;
   - offer `talk:storyboard`.

From here on, the prose is a reference only. The spine stays live: whenever the storyboard's structure changes, update the spine to match.

## Abstract and proposal mode

When the speaker needs a call-for-papers submission, write it **from the spine**, never the other way round, so the talk and its abstract can't drift apart. Follow `selection_criteria` in `talk.yaml` for length, sections and tone. Map each criterion the event judges on to the part of the spine that answers it, and show the speaker that mapping. Save the submitted text to `raw/` with the date: it is a promise the talk has to keep.
