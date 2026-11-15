---
name: start
description: >-
  Start or resume a talk built with the talk framework. On a new talk it sets
  up the project: the slot, date, audience, presenting setup, style, tools and
  a schedule. On an existing talk it reads the state, checks the gate for the
  current stage and says what to do next. Use whenever someone is preparing a
  conference talk, meetup talk, internal tech talk or other presentation and wants to
  start, has just had a talk accepted, asks "where am I with my talk", "what's
  next for the talk", "how far along is the talk", or opens a folder that
  contains talk.yaml or STATE.md. Also use for "/talk:start".
argument-hint: "[talk folder]"
---

# Start a talk

This skill is the entry point of the talk framework.
- **New talk:** it sets up the project.
- **Existing talk:** it reads `STATE.md`, checks the gate for the current stage and names the next step.

## The framework

```
 SETUP ─► NARRATIVE ─► STORYBOARD ◄── Loop A: talk-through + outside review
                           │ gate: structure freeze
                           ▼
                         BUILD ◄────── Loop B: timed runs with slides and media
                           │ gate: ready
                           ▼
                         FINAL ─► TALK ─► ARCHIVE
```

| Stage | Skill | Gate to move on |
|---|---|---|
| setup | `talk:start` | `talk.yaml` has the slot, date, audience and presenting app. |
| narrative | `talk:narrative` | The spine passes the shuffle, transition and cold-reader tests. Every claim is in `facts.md`. The speaker approves. |
| storyboard | `talk:storyboard` | Every storyboard check passes, **Planned** ≤ target, and the speaker approves. |
| loop-a | `talk:rehearse` (structure) and `talk:feedback` | **Structure freeze**, which needs both: one full talk-through with no structural change (no slide added, cut or moved between sections), and an outside review triaged with no open blocking item. |
| build | `talk:build` | Every visual is placed and the slides pass verification. |
| loop-b | `talk:rehearse` (delivery) and `talk:feedback` | **Ready**, which needs all of these: two delivery runs in a row with a projected time at or under target, no section off its plan by more than 25%, drills landing 85% of the time or more, and no five-minute stretch above `pace.max_wpm`. |
| final | `talk:final` | Freeze in place, slides and storyboard in sync, checklist done. |

## Rules

These apply to every stage.
- **Align first.** Ask up to three questions, one at a time. Make each multiple choice, with the recommended answer first and a "none of these" option. Never ask what the files can answer.
- **Structure, don't invent.** Content comes from the speaker, from `raw/` or from `facts.md`.
- **Save before acting.** Inputs go into `raw/`, dated and named by source, before anything else happens to them.
- **One owner per thing.**
  - `talk.yaml` owns settings.
  - `facts.md` owns claims.
  - The storyboard owns structure until hand-off.
  - Beats are the only notes.
- **End each stage by updating `STATE.md`**, and check in if the project is under version control.
- **Check the files, not the report.**

## New talk

1. **Gather what exists.** Read everything the speaker points at: an abstract, notes, an earlier talk, the event's speaker guidelines. Work out every answer you can from these before asking anything.
2. **Ask the setup questions** that the files didn't answer, one at a time:
   - the talk time and the Q&A time;
   - the date and time;
   - who the audience is, what they already know and what they believe now;
   - the event's selection or review criteria, if any;
   - where the slides will be presented, and on whose machine (this decides how media gets embedded);
   - the look and feel.

   Leave `tools` blank. Each stage asks for its tool when it first needs one, so the speaker only decides what is actually in use.
3. **Create the project.** Write these from `templates/`:
   - `talk.yaml`;
   - `STATE.md`;
   - `facts.md`;
   - an empty `raw/`.

   Create every other file only when its stage runs.
4. **Save the sources.** Copy them into `raw/` with dated, descriptive names. Never move or edit the originals.
5. **Seed `facts.md`.** Add every number, quote and named result in the sources. Give each its source and mark whether it is cleared to share (`ask` when unsure).
6. **List what needs lead time** under "Needs lead time" in `STATE.md`: demo recordings, permissions to show data or logos, people to interview, reviewers to book.
7. **Propose a schedule.** Add the milestones to `STATE.md` and confirm them with the speaker. A workable default, measured from today to the talk:

   | Milestone | When |
   |---|---|
   | Narrative approved | by the first fifth |
   | Storyboard approved | by the first third |
   | Structure freeze | by the midpoint |
   | Slides built | by two thirds |
   | Delivery runs | at least three, in the last third |
   | Ready | at least three days before the talk |

8. **Hand off.** Set the stage to `narrative`, update `STATE.md`, and offer to run `talk:narrative`.

## Existing talk

1. **Read the state.** Read `talk.yaml` and `STATE.md`, and count the days left.
2. **Check the current stage's gate** against the files themselves, not against what `STATE.md` claims. For example, run the storyboard checks and look for the latest rehearsal folder.
3. **Report in a few lines:**
   - the stage;
   - whether its gate passes, and if not, what is missing;
   - open decisions;
   - the next step;
   - how the schedule looks.

   If a milestone has slipped, say what to drop to recover. Usually that means fewer visuals or fewer slides, not fewer rehearsals.
4. **Offer to run the next skill.**

When a gate passes, move the stage forward in `STATE.md`, add a line to the decisions log, and check in.
