---
name: experiment-run
description: >-
  Run one round of an ML experiment from its run plan: /flow:implement's loop for the scripts, and for the
  runs a preflight, the user's go before anything billed, launches through the project's own launchers, watching
  that only observes, and actual time and cost beside each forecast. Use when the user says "run the experiment",
  "launch the runs", "start the runs", "kick off the experiment", "/experiment-run", right after
  /flow:experiment-plan signs off, when a session resumes a round with runs in flight, or when the user asks
  "eta?", "sup" or "what's left" about running experiments. For a software plan with nothing to launch, use
  /flow:implement.
argument-hint: "[path to the run plan]"
---

# Experiment Run

Work through one signed **run plan**: build steps exactly as `/flow:implement` builds them, run steps launched and watched through the project's own tools. The plan is the ledger, so a resumed or compacted session finds the live runs and `/flow:experiment-analyse` finds what they left.

Load `flow:implement` through the Skill tool and follow it; this skill lists only what changes for a round, and where the two disagree, it wins. Read its "plan" as the run plan and its "design doc" as the round design in `references:`.

**Output:**
- The run plan, filled in: run ids and actuals in the Impl notes, every arm's disposition, `status: done` at the end.
- The measured numbers in the project record (wherever the project's instructions put them), as each run ends.
- One line under the round design's **Amendments** per change to the frozen design.

## Iron Law

```
NO BILLED LAUNCH WITHOUT A GO FROM THE USER THAT NAMED IT
```

A billed launch starts paid compute or paid API calls. A go covers the launches it named: the plan's sign-off covers those it lists with their forecast, and "start Step 3" covers Step 3. Anything else billed (a relaunch, a diagnostic run, an added arm) needs its own. The gates are the plan's `MANUAL:` checkpoints; by default, before the first billed launch no go has named, between pilot and scale-up, and before a sealed test set is scored. flow:implement's iron law still holds for build steps. Beyond the go, what this skill adds is guidance: scale it to the spend, and the user can waive any of it in one line, noted in the plan.

## Process

### 1. Find the plan; check what is live

- **The plan:** the path passed in, or the most recent `thoughts/shared/plans/*-run.md` on the current branch with `status: signed-off` or `implementing`. None: "No signed run plan found. Run `/flow:experiment-plan` first." Stop.
- **Written by hand** (no frontmatter, checkboxes or `Verify:`, any name): a plan the user points to counts as signed, though not as a go for its launches. Its numbered steps are the steps: add in place only what each needs to be executed (a checkbox, ticked where its notes show the step done; for a step still to run, the check that shows it is done) and `MANUAL:` checkpoints at the default gates it lacks, with no new sign-off; then carry on.
- **Runs live with no plan:** watch and report them (step 4); launch nothing until there is a plan.
- **Resume:** before the first unchecked step, check every run named in the Impl notes or a `Handoff:` block from the runs themselves (running, finished, failed or gone), and land the ones that ended unseen (step 4).
- **The round design:** its arms table, **Saved**, **Forecast** and **Amendments** say what each run must be and leave. With none, the plan header stands in.
- **Project specifics** come from the project's instructions and skills: the launchers and guardrails, the record, the budget unit and any rate, and the data rules (what may be written into the plan and the record).

### 2. flow:implement's loop, read for a run step

Build steps (a script and its test, a fix) go through the loop unchanged. A run step launches a run and moves on, or waits on one; it changes no code and reads the loop like this:

| flow:implement | For a run step |
| --- | --- |
| 2b red-capable check | A launch step: as flow:implement says; its Verify passing before the launch means an earlier attempt's outputs are in the way: ESCALATE, never launch over them. A wait step: none. If its Verify already passes for the run id the launch step recorded, the run has finished: carry on. |
| 2c touch only `Files:` | Holds for code. A run step may also write the project record and the round design's **Amendments**. |
| 2d Verify fails: fix and re-run | Not for a run: a failed run goes to step 5. A Verify that is itself wrong still escalates. |
| 2e fill the plan | A launch step is checked at launch, its Impl note giving the run id, where it runs, its log and how to check it. When the run ends, its actuals go in that note beside the step's `Forecast:`. An arm not run: `not run — fork B` or `dropped — <why> (user, <date>)`, box checked so a resume skips it. |
| 2f review gate | Skipped, `Decision:` or not: `Review note: skipped — run step, no code`. |
| 3 phases straight through | A gate still stops, unless a go named what it launches. |
| 5 dumb zone | A wait step can't finish first: hand off with the runs live. The handoff names each live run (where, its id, its log, how to check it, when it should end), and the resume command is `/flow:experiment-run <plan-path>`. |

Every commit flow:implement makes (a step, completion, a handoff) stages only the tracked files it changed, so a plan in an ignored `thoughts/` is never staged; with nothing tracked changed, there is no commit.

### 3. Preflight, then the gate

- **Preflight** before the first launch, and again after a resume or a gap of hours (credentials expire mid-round), through the project's launch skills and rules: auth, capacity and limits, and what other sessions run on the same resources. Never bypass a guardrail; if one refuses, stop and tell the user.
- **Review:** read the "Review before launch" line at the end of the round design's **Forecast**. If it says required, this round's pre-launch review record in the study's `reviews/` or a waiver line under **Amendments** must exist before the first billed launch; with neither, stop and point to `/flow:experiment-review`. No such line: not required.
- **What a run leaves:** if neither the design nor the plan says what a run must leave, and its compute is released at its end, say before the launch what will be lost (models, checkpoints, per-item scores).
- **At a gate:** stop and say in one line what launches, its forecast (wall, compute, and money where the project states a rate) at the latest measured rates, and the round's spend so far against its budget; for a sealed test, what is scored (the model, checkpoint and threshold frozen beforehand). Then ask for the go. If it no longer fits the budget, say so: more budget is an amendment (step 6). A go given earlier that named what the gate launches is the go: say what launches and go on.

```
✅ Gate, pilot → scale-up: wu-1000 and wu-2000, seeds 1–2, two at a time: ~20 h, ~317 GPU-h at the pilot's
   71k tokens/s per GPU (forecast 70k). Spent: 16 of 400 GPU-h. Checkpoints saved and reloaded. Go?
❌ "The pilot looks good. Shall I start the main runs?" A yes approves a spend nobody has stated.
```

### 4. Launch, watch, land

- Launch only through the project's launchers. The project's instructions decide how runs are watched; by default, observe and report: no retries, watchdogs or recovery. Waits end with the session or expire; re-arming one or re-attaching to a log is observing, not recovery.
- Report the events that matter (a milestone a Verify names, a failure, a saved output, the end), not every log line.
- A run past 1.5x its forecast: report it with its progress and a new expected end. Do not kill it.
- **Status** ("eta?", "sup", "what's left"), from a fresh check of the runs, not memory: the step, each live run's elapsed time against its forecast and its expected end, and what is waiting on the user. An early number is labelled early, with its source; reading it against the bar is `/flow:experiment-analyse`'s job.
- **When a run ends:** everything the design's **Saved** line names is in the durable store before its compute is released, by a teardown or an idle shutdown, since what is left on the machine is lost. Then the actuals in the launch step's Impl note, and the project record now, not later.

### 5. When a run fails

- Check the run itself first. A dropped log stream or a dead launcher is not a failed run, and relaunching it would run it twice.
- Stop launching; leave the other runs going. Collect the evidence: logs, config, exit state, what was saved. Diagnose; a fresh subagent given the problem in one line and the logs, with no hypothesis of yours, is a good second opinion. A diagnostic launch needs a go like any other: ask in the same message as the diagnosis.
- Propose the fix: a build step, added to the plan before the relaunch, with a check that fails without it. Relaunch on the user's go by reopening the launch step under a new run name, so the failed attempt's outputs cannot pass its check. If the user declines the fix, note it in the launch step's Impl note and go on.
- If the fix changes code an arm already ran, the arms no longer differ in one thing: say so. Rerunning that arm is the user's call, and an amendment.

### 6. Changes to the frozen design

- A change above the round design's freeze line (an arm, the data, a measure, what is saved, the budget), whoever asks for it: one line under **Amendments** (date, what changed, why, and what had been seen when it changed), and the plan edited to match. The message that asked for it is the go if it named what launches. For an added arm, the user's predicted result goes in the line: from that message if it gave one, else asked in one plain-text line before you show its forecast. With no round design file, the plan edit alone carries the change. A new compute shape or order that leaves the design alone is only a plan edit.
- A change to the question or the bar is a new round, through `/flow:experiment-design`.

### 7. Completion

Completion comes when every arm has a disposition in the plan (done with its run ids, not run, or dropped and why), even if a clean-up step still waits on the user: leave that step unchecked with `pending (user)` in its Impl note, for `/flow:experiment-close` to pick up. Then flow:implement's completion, with the actual total beside the forecast total, and tell the user: "Runs complete: <arms done and dropped>; <actual> against a forecast of <forecast>. Next is `/flow:experiment-analyse`, which reads them against the round design." If the user's request already asked for the analysis, go straight on.
