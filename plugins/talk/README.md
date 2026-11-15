# talk

A framework for building a conference talk with an AI agent.

The speaker decides what the talk says. The agent structures, builds and measures. Outside reviewers audit. A talk is found by saying it out loud, so rehearsal starts before any slide exists. Nothing expensive gets made until speaking out loud stops changing the structure.

## Install

```
/plugin marketplace add dhruvnigam93/skills
/plugin install talk@dhruvnigam93
```

## Workflow

```
 SETUP ─► NARRATIVE ─► STORYBOARD ◄──────────────┐
                           │                     │  Loop A: structure (cheap)
                           │                     │  talk it through, get an outside review,
                           ├─────────────────────┘  revise the storyboard
                           │  gate: structure freeze
                           ▼
                         BUILD ◄─────────────────┐
                     visuals, slides             │  Loop B: delivery (full fidelity)
                           │                     │  timed run with slides and media,
                           ├─────────────────────┘  revise the storyboard, rebuild
                           │  gate: ready
                           ▼
                         FINAL ─► TALK ─► ARCHIVE
          freeze, cue card, Q&A bank, day-of checklist
```

There are two loops, and a gate between them.
- **Loop A** runs on a text storyboard. Changing anything costs minutes.
- **Loop B** runs on real slides with real media. Changing anything costs hours.
- **The structure freeze** sits between them, so visuals are made for slides that are going to survive.

## Skills

| Skill | Stage | What it produces |
|---|---|---|
| `/talk:start` | Setup, then status at any time | The project folder, `talk.yaml` and `STATE.md`. Later it reports the stage, the gate and the next step. |
| `/talk:narrative` | Narrative | The spine (a one-page argument) and the talk in prose. Writes a call-for-papers abstract if you need one. |
| `/talk:storyboard` | Storyboard, and every revision | `storyboard.md`, one entry per slide, checked against the craft principles. |
| `/talk:feedback` | Both loops | Reviewer comments saved, triaged in `feedback.md`, and applied. |
| `/talk:rehearse` | Both loops | Timing, pace and a reconciliation of each run against the plan, with a decision on every gap. |
| `/talk:build` | Build | A visual manifest, the visuals and the slides, made with your own tools and then verified. Keeps the slides and the storyboard in sync after hand edits. |
| `/talk:final` | Final | Freeze times, a cue card, a Q&A bank, a day-of checklist and the archive. |

Start with `/talk:start`. Run it again whenever you return to the talk: it reads `STATE.md` and tells you what comes next.

## A talk project

```
talk.yaml        slot, date, audience, presenting setup, style, pace, freeze times, tools
STATE.md         current stage, what's done, open decisions, next step, decisions log
raw/             every source and every piece of feedback, saved before it is used
facts.md         every number and claim, with its source and whether it can be shared
narrative.md     the spine, then the talk in prose
storyboard.md    slide by slide; owns the structure until hand-off
feedback.md      triaged feedback from reviewers
rehearsals/      one folder per run: transcript, timing, reconciliation
assets/          style sheet, visual manifest, visuals and media
slides/          whatever your slide tool produces
qa.md            likely questions, with short and long answers
cue-card.md      one line per slide, with time checkpoints
checklist.md     day-of checks
```

## Rules every skill follows

- **Align first.** Before producing anything, the skill asks up to three questions, one at a time. Each is multiple choice, with the recommended answer first and a "none of these" option. It never spends a question on something the files can answer.
- **Structure, don't invent.** Content comes from the speaker, from `raw/` or from `facts.md`. Anything of the speaker's that gets cut or merged is listed, and the speaker confirms it.
- **Save before acting.** Every recording, transcript, comment and note goes into `raw/` with a date and a source before anyone triages it.
- **One owner per thing.**
  - `talk.yaml` owns settings.
  - `facts.md` owns claims.
  - `storyboard.md` owns structure until the slides are handed off; after that the slides do.
  - Beats are the only speaker notes.
- **State lives in files.** Each stage ends by updating `STATE.md`. If the project is under version control, the skill also checks it in. Anyone can pick the talk up cold.
- **Check the files, not the report.** A stage is done when its output files pass their checks, not when a tool or helper says it succeeded.

## Bring your own tools

The framework assumes no particular slide app, visual generator, transcription service or notification channel. `talk.yaml` has a `tools` block that starts empty. The first time a stage needs a tool, it asks once and records the answer there. Each tool slot accepts:
- a skill or script;
- a template;
- a person;
- "by hand", in which case the skill produces a build sheet for you to follow.

## Craft principles

[references/craft.md](references/craft.md) is the yardstick for the narrative and the storyboard. In short:
- a journey, not a list;
- one point per slide, with a title that states it;
- threes;
- recurring elements set up and paid off;
- the human stakes before the mechanism;
- a promise made early and kept at the end.
