---
name: experiment-plan
description: >-
  Turn an ML experiment's round design into a run plan: /flow:plan's steps plus the launch and wait steps,
  forecasts and gates that runs on paid compute need. Use when the user says "plan the run", "plan the
  experiment", "create a plan to run this experiment", "write the run plan", "/experiment-plan", or right after
  /flow:experiment-design freezes a round. For a software feature with nothing to launch, use /flow:plan.
argument-hint: "[path to a round design, or the experiment described]"
---

# Experiment Plan

Turn one round design into a run plan that `/flow:experiment-run` executes. This is `flow:plan` with a few differences: load `flow:plan` through the Skill tool, follow it, and apply what follows; where the two disagree, this skill wins. Read its "design doc" as the round design and its "feature" as the round. Apart from the gates, what this skill adds is guidance: scale it to the spend, and the user can waive any of it in one line, under Assumptions.

**Output:** `<repo-root>/thoughts/shared/plans/<YYYY-MM-DD>-<round-slug>-run.md`, in flow:plan's template. `references:` points at the round design, if there is one, and the design's `run_plan:` is set to this path, the line added in place if it has none.

## Process: flow:plan's steps, with these differences

### 1. Find the round design
- **The round design** is the one passed in or pointed to, at any path, else the newest `status: frozen` one under `thoughts/studies/`. One written by hand counts as frozen. What it lacks (a **Saved** line, a budget, the `Review before launch:` line) goes under Assumptions; never stop for it.
- **None, or one with `status: draft`:** flow:plan's choice, with `/flow:experiment-design` in place of `/flow:design`. Planning from the description puts one line under Assumptions: "No round design: no prediction or Answer on record."
- **Runs that already happened** enter as checked steps with their ids in `Impl note:`, so `/flow:experiment-run` resumes after them.

### 2. Ground every step in the project
- Take the launcher, its limits and hazards, the record and the data rules from the project's instructions and launch skills; never guess a launch command. The rules a run step could break go under the header's **Conventions**.
- New code interfaces are specified in this plan and approved at its sign-off: the round design has no Interface Spec to defer to.
- A step the design does not call for (an arm, a measure, a dataset, more budget) is a design change: ask. On a yes it is one line under the design's **Amendments** (with no design file, under the plan's Assumptions); a new question or bar goes back to `/flow:experiment-design`.

### 3. Header, success criteria, steps
`Context for Every Step` also says, as lines or one table: the compute and the project's launcher; one run name per arm and seed, from the design's **Arms**; where each run's outputs land and what is saved there, from the design's **Saved** line; and the record: where results go and how ids are taken.

Success criteria say the round can be read, never how it comes out: every arm has a disposition; the arms that ran have the planned settings and the outputs the **Saved** line names; the record holds their rows. **Out of Scope** is the cuts and what the round does not cover, from the design's **Limits**.

Two kinds of step, both in flow:plan's format:
- **A build step** is unchanged: a script and its test. Code the planned measures need is built here, before any run, so how the result is read is fixed before it is seen.
- **A run step** launches a run by its literal command, or waits on one, and changes no code. A **launch step** moves on once the run starts: its `Verify:` is the config and first log lines showing the planned settings, above all those the comparison turns on, and it fails before the launch. A **wait step** checks the outputs in the durable store (the expected fields and counts) of the run the launch step recorded; it may already pass when reached, since the run may have finished meanwhile, so it needs no check that fails beforehand. Seeds and repeats come from the round design: flow:plan's rule to run a stochastic check five times does not apply to experiment runs or their scoring.

Check a run by the name its step gives it; when the launcher assigns the id, the launch step writes it in its `Impl note:` and later steps read it there. A step that bills real compute carries `Forecast:` (wall · compute · money where the project states a rate · basis) just above `Impl note:`, so the actual lands beside it. Arms that run only if an earlier result calls for them are `Decision:` forks.

✅ A launch step, flow:plan's other fields left out:
```
### [ ] Step 6 — Launch wu-2000, seed 1

**Do:** Launch in the background and move on; Step 7 waits for it. `scripts/train.sh --name wu-2000-s1 --model 1b --data web-20b --tokens 20e9 --batch-tokens 1048576 --lr 3e-4 --warmup 2000 --decay cosine:0.1 --seed 1 --save-every 2e9 --item-loss`
**Interfaces:** Adds: the run id the launcher prints, in the Impl note; Step 7 reads it.
**Verify:** within 20 min the log of `wu-2000-s1` shows `warmup_steps=2000` and `step 10/19073`, and its `config.json` is in the durable store.
**Forecast:** 10 h · 79 GPU-h · 70k tokens/s per GPU, measured in R-3.
```

**Order and gates.** Build (no spend), then the pilot if there is one, then the runs, then collect and clean up, in the design's **Order**.
- **Plan a pilot** only when something is unmeasured (a new code path or configuration, an unknown rate); else cite under Assumptions the run that measured it. The pilot's `Verify:` exercises save and reload where they apply (a resume from a checkpoint, per-item scores read back); its `Impl note:` gives the measured rates and the scale-up forecast they imply.
- **Gates end phases** as `MANUAL:` checkpoints, which flow:implement pauses at: before the first billed launch that is more than a small preparation job, between pilot and scale-up, and before a sealed test set is scored. Preparation jobs before the first gate run on the plan's sign-off, which names them with their forecast. Each gate names what its go launches and its forecast, so nothing billed starts without a go that named it:
  `> **Phase 1 checkpoint** — MANUAL: Gate (user), first billed launch: wu-2000 seeds 1 and 2, side by side, ~10 h, ~158 GPU-h.`
- **The last steps** collect the outputs of every arm that ran where `/flow:experiment-analyse` will read them, then free what the runs held (compute, and data on shared storage), each checked by a listing. Deleting data waits for the user's yes.

### 4. Self-review
flow:plan's checks, plus: every arm and seed has a run step or a fork; every **Saved** item is checked by some `Verify:`; each precondition a run step checks (a clean tree, free space) is made true by an earlier step; the forecasts add up to the design's, or the gap is shown.

### 5. Sign-off
Beside flow:plan's table, name the launches the sign-off itself approves, with their forecasts, and each gate. Words that approve the plan as shown are the sign-off: do not ask again. On sign-off, if `thoughts/` is tracked, commit the plan, and the design's `run_plan:` if set, through the `commit` skill; if not, the status alone marks the sign-off. Then read the design's `Review before launch:` line. Required, with no pre-launch review of this round in the study's `reviews/` and no waiver under **Amendments**: "Run plan signed off. Next is a pre-launch `/flow:experiment-review`, required before any launch." Otherwise, or with no such line: "Run plan signed off. Next is `/flow:experiment-run`, which works through it and stops at each gate." If the request already asked for the runs, go straight on to that next skill.
