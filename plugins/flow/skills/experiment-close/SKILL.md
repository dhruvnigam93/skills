---
name: experiment-close
description: >-
  Close one round of an ML experiment: record the user's decision on it (never inferred from the result), bring
  the study index and the project record up to date, and, only when asked, draft the report or messages and list
  what the round left behind. Use when the user takes a decision on a round or parks it, says "close this out",
  "wrap up the experiment", "record the decision", "we're going with X", "freeze that model", "update the
  tracker with this", "/experiment-close", or right after /flow:experiment-analyse.
argument-hint: "[path to a round design or study folder] [the decision, if taken]"
---

# Experiment Close

Record what the user decided on a round in the round design, the study index and the project record, so the next session finds the study where it stands. Reports, messages and deletions happen only when the user asks, through the skills and tools that already do them. It hands on to `/flow:experiment-design` for the next round.

**Output:**
- **Decision** in the round design, below the freeze line, wherever the design lives; `status: closed` unless pending.
- The study index, `thoughts/studies/<YYYY-MM-DD>-<study-slug>/README.md`: **Where we stand**, the round's row, **Next**.
- The decision entry in the project record, and the drafts the user asked for.

## Iron Law

```
THE DECISION IS THE USER'S. RECORD IT; NEVER INFER IT.
```

The outcome says what the result is; the decision says what we do about it, and the user may depart from the Answer for reasons the round never measured (a deadline, a cost, another study). A decision written from the outcome reads, a month later, exactly like one the user took. Everything else is guidance the user can waive in one line: recording the decision is the whole job when that is all they asked.

## Process

### 1. The round and the decision (forced)

- **The round:** the path passed in, or the study's round with `status: answered`, else its latest round not yet closed. Read its Question, Answer, Amendments and Results, and its reviews in the study's `reviews/`. Take the record, its ids and the data rules from the project's instructions.
- **Written by hand, run by hand or stopped early:** use what exists. A design written by hand is the round design, where it lives; with no design at all, the Decision goes at the end of the run plan, whose status stays as it is. Results come from the design, else from the project record or the run plan's notes; offer `/flow:experiment-analyse` only when no analysis exists anywhere. A decision taken without results (stop, drop) says what it rested on.
- **The decision:** if the user has stated it, take their words. If not, ask once: the Answer's outcomes as the options, each with what it says to do, plus "not decided yet"; give the outcome as Results states it, and mark no option. With no Answer, or one that names no action, ask in plain text, giving only the outcome as Results states it: options would invent the action.
- Write **Decision**: the date and "(user)", the decision in their words, its limits (what it was not shown to hold for; review findings still open), and what is next. If it departs from the Answer, say how and why, so the reading written before the run stays checkable. Set the design's `status: closed`, adding the frontmatter line in place if it has none.
- **Pending** is an answer, and "not now" means pending: do not press. Write "Pending (user, date)" with what it waits on, leave the status as it is, and write no record entry.

```
✅ **2026-01-16 (user):** the 7B run takes a 2,000-step warmup, as "clears" says (R-5, R-6).
   Limits: shown at 1B with two seeds; the 7B batch is 4x larger. Next: the decay shape.
❌ "Decision: adopt 2,000 steps (clears)." Written from the outcome: no date, no owner, no limits.
```

### 2. The study index

Rewrite **Where we stand**, dated: two to four lines on the current answer, the current candidate and what is unproven. Add or fill the round's row: Answer and Decision one line each, the decision marked "(user, date)", and the record ids. A study folder with no index gets one from `/flow:experiment-design`'s [study-index template](../experiment-design/templates/study-index.md), by its conventions, with this round's row. With no study folder at all, the Decision and the record are enough: make a folder and index only if the user wants one.

### 3. The project record

Unless the decision is pending, write its entry where and in the form the project's instructions say: dated, marked as the user's, citing the record ids Results cites, and naming any earlier decision it replaces. Then one check: does the canonical record (the default branch, `git show <default-branch>:<record file>`) hold this round's rows? If not, say so in one line ("rows X to Y are only on branch Z"), and ask only when what to do about it is unclear. Bringing code over is the project's own workflow.

### 4. Reports and messages, when asked

Draft the ones the user asks for, each through the skill the project or user has for it (a report, a short summary for chat or email, the tracker's own tool for a comment); with none, write a short draft yourself.
- The source is the round design and its numbers file (or the project's own results file), never the chat. Carry Results' words unchanged: an interval that spans zero stays "not distinguishable".
- A study that already has a report gets that report updated, at its link (from the record, else ask); write the link under Decision.
- Drafts, not sends: nothing is posted, sent or shared until the user says so. Before anything that quotes data leaves the repo, check the project's data rules and who can see the destination.

### 5. What the round left

List what the round left, from the run plan's last steps and the record: compute still up, files on shared storage, failed or partial outputs, data only in a worktree. Never launch compute to measure it: a size the record lacks stays unknown. Say at once if anything still bills, and name data that exists only in a worktree before the worktree goes.

When clean-up is wanted: confirm first that the results are durable (the numbers file and what the design's **Saved** line names), then ask in one message which to delete, saying it cannot be undone. Delete only what gets an explicit yes, through the project's own tools, and write one line under Decision on what went and what stays. A pending decision keeps what it may still need.

### 6. Next, then hand on

Update **Next** in the index, if there is one: drop the candidates the decision settled; add those from Results, the reviews and the conversation, one line each with what it would tell us and roughly what it costs.

If `thoughts/` or the record is tracked by git, commit through the `commit` skill, with no AI attribution, when the project's instructions allow it. Then tell the user: the decision as recorded and where, the drafts and where they wait, what the round left and what was deleted. End with one of:
- Closed: "Round closed. Next is `/flow:experiment-design`, for the round you pick from Next." If the decision answers the study's **Serves** line, say the study is done instead.
- Pending: "Decision pending: <what it waits on>. Run `/flow:experiment-close` again once it is taken."

## Asking the user

- One question per message, through the question tool (`AskUserQuestion`; load it with ToolSearch if deferred; with none, plain text with lettered options).
- No recommended option: each option says what choosing it means for the study. If the user asks what you would pick, answer.
- Two asks are plain text: the decision when no Answer names an action, and what to delete (one list, so a phrase can answer it).
