---
name: rehearse
description: >-
  Turn a rehearsal of a talk into decisions. Takes a recording or transcript of
  a run-through, measures time per slide and section, projects the real
  runtime, tracks speaking pace and filler words, compares what was said with
  what was planned, and walks the speaker through each gap: adopt what you
  said, drill the planned line, cut it, or restore it. It has two modes:
  structure, for early talk-throughs without slides, and delivery, for timed
  runs with slides and media. Use whenever someone has practised their talk,
  recorded a dry run, has a rehearsal transcript, or asks "how long is my
  talk", "am I over time", "am I speaking too fast", "review my run-through",
  "what did I miss", "/talk:rehearse".
argument-hint: "[structure | delivery] [path to recording or transcript]"
---

# Rehearse

Saying the talk out loud is how it improves. Each run answers three questions:
- Does the structure hold?
- Does it fit the time?
- Does what the speaker actually says match the plan?

Where speech and plan differ, one of them has to change, and this skill makes that a decision instead of drift.

The measurement method and the report format are in `references/analysis.md`.

## Rules

- **Save before acting.** The recording or its text goes into `raw/` first.
- Structure, don't invent: suggested wording comes from what the speaker said.
- Ask about decisions one at a time, with the recommended option first.
- Changes go through the `talk:storyboard` revise rules. After hand-off, they go into the slides.
- Update `STATE.md` at the end.

## Modes

| | Structure (Loop A) | Delivery (Loop B) |
|---|---|---|
| When | After the storyboard is approved, until the structure freezes. | After the slides are built, until the talk is ready. |
| What the speaker does | Talks through `storyboard.md` out loud, without slides. | Gives the full talk with slides and media, timed, as if live. |
| Focus | Order, missing beats, planned lines never said, places where the speaker got lost or backtracked. | Time per slide and section, projected runtime, pace, fillers, drills. |
| Ignore | Pace, fillers, exact timing. | Nothing. |
| Gate | **Structure freeze:** a run with no structural change. | **Ready:** two runs in a row that pass, as defined in `talk:start`. |

Pick the mode from the stage in `STATE.md`, unless the speaker names one.

## Steps

1. **Collect the run.**
   - Get the recording, or a transcript if one already exists.
   - Turn the recording into **timestamped** text with `tools.transcription`. If that is blank, ask how once and record the answer.
   - For delivery runs, also get the times the slides changed if any source has them: a recording from the presenting app, a clicker log, or marks the speaker made.

   Save everything to `raw/` and make a folder `rehearsals/<date>-<n>-<mode>/`.

2. **Align the transcript to the slides.** Use the slide-change times if there are any. Otherwise match the spoken text to each slide's beats, lines and title, in order. Mark any slide where the match is uncertain.

3. **Measure,** following `references/analysis.md`.
   - Structure mode: time per section and the total only.
   - Delivery mode: everything, including the projected runtime and pace in five-minute windows.

4. **Reconcile, slide by slide.** Compare what was said with the beats and lines, and propose one decision for each gap:
   - **ADOPT:** what was said beats the plan. Take the spoken wording into the beats or lines.
   - **DRILL:** a planned line that matters was missed or garbled. Practise it as written.
   - **CUT:** something planned or ad-libbed that nobody would miss, or that eats time.
   - **RESTORE:** something cut earlier that this run showed is needed.

   In structure mode, also flag:
   - slides the speaker skipped or reordered;
   - places where they had to backtrack to explain something. This usually means a set-up is missing earlier.

5. **Score last run's drills.** For each one, record whether it was said as written: hit or miss.

6. **Decide** with the speaker. Show the measurements first, then the decisions, one slide at a time, with the recommended option first. Each run produces at most seven drills, so the speaker can actually practise them. Pick the lines that carry the argument.

7. **Apply** the decisions through `talk:storyboard` (revise). In delivery mode, replace estimated slide times with measured ones. Add any question raised or anticipated during the run to `qa.md`.

8. **Report and close.** Write `rehearsals/<date>-<n>-<mode>/report.md` and update `STATE.md` with:
   - the run number;
   - the measured and projected times;
   - the number of drills;
   - the gate status.

   Then check in. If `tools.notify` is set and the processing took a while, send a note.

Within `freeze.content_hours_before` of the talk, propose only CUT and DRILL decisions.
