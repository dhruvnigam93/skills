---
name: implement
description: >-
  Execute a signed implementation plan step by step — implement, verify, get
  independent review, auto-commit. Use when the user says "implement this",
  "start building", "execute the plan", "run the steps", "/implement", or
  right after a plan is signed off.
argument-hint: "[path to plan]"
---

# Implement Phase

Work through a signed `/flow:plan` plan one step at a time. Each step: implement → verify green → review gate (independent review if >3 files or >200 lines) → auto-commit. The plan file is the durable progress ledger — fill it in as you go.

## Iron Law

```
NO LARGE-STEP COMMIT WITHOUT A PASSING INDEPENDENT REVIEW
```

"Large" is mechanical, not a judgement call — see 2f. Small steps skip the reviewer and commit after green verify.

## Process

### 1. Find the plan, check state

- **Plan file** — the path passed in, or the most recent `thoughts/shared/plans/*.md` on the current branch with `status: signed-off` or `status: implementing`.
- **No signed plan** — say: "No signed plan found. Run `/flow:plan` first." Stop.
- **Resume** — if `status: implementing` and some steps are checked (`[x]`), pick up from the first unchecked step. Read the last `Review note:` and any `> **Handoff:**` block to understand where things stand. Trust checked steps and `git log` over your own recollection — after context compaction, the plan is the record.
- Set `status: implementing` in the frontmatter if it isn't already. This change rides with the first step's commit — never commit it alone.
- Read the **plan header** (everything above Phase 1) — this is your context for every step. Read the **design doc** in `references:` if it exists — its Interface Spec is the authority on signatures.

### 2. Step loop

For each unchecked step (`### [ ] Step N`), in order:

#### 2a. Read the step

Read the plan header + this one step. The step-reviewer will judge against exactly this, so build from exactly this.

#### 2b. Red-capable check

Run the step's `Verify:` command(s) **before writing any code**.

- `MANUAL:` — skip this substep.
- Test file doesn't exist yet — red-capable by definition.
- `Verify:` already passes before any change — **ESCALATE**: "Step N's Verify passes before any change — the check can't prove this step. Your call." Do not proceed.

#### 2c. Implement

Write the code. Build from `Do:`, `Files:`, `Interfaces:`, and `Scope:`.

- Touch only the files in `Files:`. The plan file is the one exception (checkbox + notes).
- Match every `Adds:` signature exactly — name, parameters, types, return type.
- Respect `Must NOT change:`.
- Need something the step doesn't cover — a file not in `Files:`, a signature not in `Adds:`? **Don't do it.** Note the gap in `Impl note:`. If it's clearly plan-level (missing file, wrong signature in the design), ESCALATE immediately rather than working around it.

#### 2d. Verify green

Run the step's `Verify:` command(s). All must pass with the expected output.

- Failures: fix your code and re-run. The test and the Verify command are the step's contract — don't rewrite them.
- If the Verify itself is wrong (typo in expected output, wrong path), note it in `Impl note:` and ESCALATE. Never silently rewrite a step's Verify.

#### 2e. Fill the plan

1. Check the box: `### [ ] Step N` → `### [x] Step N`
2. Write a one-line `**Impl note:**` — what you did, anything surprising, or "as planned".

If the step has a `Decision:` field: run the observation command, record what you observed in `Impl note:`, follow the matching fork. If the observation matches no named fork — ESCALATE. If following a fork would change a signature in the signed design's Interface Spec — **hard stop**, that is a design change.

#### 2f. Review gate (deterministic)

Measure the step's change, excluding the plan file:

```
git add -N <files from Files:>
git diff --numstat <base> -- . ':!<plan-path>'
```

- **files** = number of rows; **lines** = sum of added + deleted (binary rows count as 0 lines, 1 file).
- **files > 3 OR lines > 200** → review required (below).
- Otherwise → **skip the reviewer**. Add `**Review note:** skipped — N files, M lines (under threshold)` to the step, then commit as in 2g.
- A `Decision:` step, or one that touches a signature in the design's Interface Spec, is reviewed regardless of size.

Do not override the gate by feel in either direction. Re-measure after any BLOCK fix; if a step first reviewed then shrinks, it stays reviewed.

#### 2f-i. Independent review

Record the base commit (`git rev-parse HEAD` before this step's changes — or the base from a handoff note on resume).

Dispatch the `flow:step-reviewer` agent:

```
Plan: <plan-path>
Step: <N>
Base: <base-commit>
```

On a re-review after BLOCK, add:
```
Previous BLOCK reasons:
<the reviewer's reasons from the last verdict>
```

Wait for the verdict. Parse the first line of the report: `VERDICT: APPROVE`, `VERDICT: BLOCK`, or `VERDICT: ESCALATE`.

#### 2g. Act on verdict

| Verdict | Action |
|---------|--------|
| **APPROVE** (or gate skipped review) | Commit and continue to next step. |
| **BLOCK** | Fix your code (not the step spec). Re-dispatch the reviewer. Max **3 review cycles** — after 3 BLOCKs, pause: "Step N blocked 3 times. Reviewer keeps finding: [reasons]. Your call." |
| **ESCALATE** | Pause. Show the user the reviewer's full report — the decision, options, and recommendation. Wait. |

**Commit on APPROVE or a skipped review (and every other commit in this skill: the `status: done` commit, the handoff note):** always invoke the `commit` skill via the Skill tool. Never run a bare `git commit`, because the harness adds a `Co-Authored-By: Claude` trailer to commits made without the skill, and the skill's attribution rules (no `Co-Authored-By`, no "Generated with", no AI metadata) are what strip it. The plan sign-off plus the reviewer's APPROVE (or the gate's skip) counts as the user's approval, so skip the skill's "Shall I proceed?" prompt and commit straight away. Stage only the files in `Files:` plus the plan file. Never `git add -A`. Message:

```
feat(<scope>): step N — <step title>

<one-line what changed>
```

The reviewer's non-blocking notes ride along in the plan's `Review note:` — the reviewer already wrote them there.

### 3. Phase boundaries

At each `> **Phase N checkpoint**` line:
- `MANUAL:` — pause, show the user what to check, wait for confirmation before Phase N+1.
- "none — automated checks cover it" — continue.

If the user asked to run multiple phases consecutively, skip the pause until the last requested phase.

### 4. Completion

After the last step:
1. Re-verify every **Success Criterion** in the plan header. Run each check and record the output.
2. Any criterion fails → identify which step's work is insufficient. Don't invent new steps — that's a plan change.
3. Set `status: done` in the frontmatter. Commit.
4. Tell the user: "Plan complete. All success criteria pass. Next: final review + PR."

### 5. Dumb-zone rule

At ~60% context utilization: finish the current step through its commit, then stop. Write a handoff in the plan under the next unchecked step:

```
> **Handoff:** session ended at ~60% context. Last committed step: N. Resume from Step N+1. Base commit: <hash>.
```

Commit this note. Tell the user:
> "Context getting full — committed through Step N, noted the resume point. Run `/flow:implement <plan-path>` in a fresh session to continue."

Never push through. A degraded agent makes mistakes that waste more time than a clean restart.

## Red Flags

| Thought | Reality |
|---------|---------|
| "The reviewer will be fine with this extra file." | If it's not in `Files:`, don't touch it. |
| "This test is wrong, let me fix it." | The test is the step's contract. ESCALATE. |
| "I'll just adjust the signature slightly." | If it's in `Adds:`, match it exactly. If the design is wrong, ESCALATE. |
| "The reviewer blocked on something trivial, I'll skip re-review." | If a review was required, no commit without a passing one. The iron law. |
| "This small step feels risky, I'll review it anyway" / "This big one is simple, skip." | The gate is files > 3 or lines > 200. Follow the numbers. |
| "I can finish one more step before handing off." | If you're at 60%, you can't. Commit and stop. |
| "A quick `git commit` is faster than the commit skill." | Bare commits get a Claude co-author trailer. Always use the `commit` skill. |
| "I'll commit all the steps together at the end." | Each step is a commit. Atomic, reviewable increments. |
| "I'll just work around the missing file." | Note it in Impl note, ESCALATE. The plan missed something — that's plan-level, not implementation-level. |
| "I remember what Step N says from reading it earlier." | You remember a summary. The step has the exact values, signatures, and test cases. Read it. |
| "Should I check in before the next step?" | No. Execute continuously. Pause only at phase boundaries, MANUAL steps, 3x BLOCK, ESCALATE, and the dumb zone. |
