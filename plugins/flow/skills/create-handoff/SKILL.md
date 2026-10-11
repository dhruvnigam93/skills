---
name: create-handoff
description: >-
  Compact the current session into a handoff doc so a fresh session can continue.
  Use when the user says "hand off", "write a handoff", "create handoff",
  "/create-handoff", or when you hit ~60% context utilization during /flow:implement.
  The dumb-zone rule in /flow:implement triggers this automatically.
argument-hint: "[optional: what the next session should focus on]"
---

# Create Handoff

Write a handoff document so a fresh session can continue exactly where this one stopped. The handoff is a pointer document — it references artifacts, not duplicates them. A fresh agent reads it plus the linked files and resumes without asking "where were we?"

**Output:** `<repo-root>/thoughts/shared/handoffs/YYYY-MM-DD-<kebab-desc>.md`
- `<repo-root>` = `git rev-parse --show-toplevel`
- `<kebab-desc>` = current branch slug or task description
- Create the directories if missing.

## Iron Law

```
NO HANDOFF WITHOUT LINKING THE PLAN AND ITS EXACT POSITION
```

A handoff that says "continue the work" without naming the plan file and the step number forces the next agent to re-derive your progress. That is the single most expensive failure in multi-session work — controllers that lost their place have re-dispatched entire completed task sequences.

## When to trigger

- **User asks** — explicit request.
- **Dumb-zone rule** — at ~60% context utilization during `/flow:implement`, the implement skill finishes the current step, commits, and invokes this skill. Never mid-step.
- **End of session** — if you've made progress worth preserving and the user is wrapping up.

## Process

### 1. Gather state

- `git log --oneline -20` — recent commits (what's done)
- `git status` — uncommitted work (stash or commit before handing off)
- `git diff --stat` — what's changed
- Current plan file — read it for checked/unchecked steps
- Current branch name and base

**Uncommitted work:** if there are uncommitted changes, stash them with a descriptive message (`git stash push -u -m "handoff: <description>"`). Note the stash in the handoff. Never hand off with dirty state — the next agent won't know what's committed and what's not.

### 2. Write the handoff

```markdown
---
date: YYYY-MM-DDTHH:MM:SS+TZ
author: agent (model-id)
git_commit: <current HEAD hash>
branch: <current branch>
status: active
references:
  - <plan file path>
  - <design doc path>
---

# Handoff: [concise description]

## Resume command

`/flow:implement <plan-path>` — or `/flow:resume-handoff <this-file-path>`

## Position

- **Plan:** `<path>` — Step N of M complete, next is Step N+1
- **Branch:** `<branch>` at commit `<hash>`
- **Base for next step:** `<commit hash>`
- **Stashed work:** [none, or: `git stash pop` to recover — describe what's in it]

## What's done

[2-3 bullets: what was accomplished, referencing committed steps]

## What's next

[The next step(s) from the plan, and any context the next agent needs beyond
what the plan says — a gotcha you discovered, a deviation you made, a ruling
the plan doesn't capture]

## Learnings

[Things discovered during implementation that aren't in the plan or design doc
— edge cases, surprising behavior, patterns. Include file:line references.
Skip if nothing surprising.]

## Critical references

[2-3 most important files the next agent should read, beyond the plan itself.
Only files that carry context the plan doesn't.]
```

### 3. Commit and tell the user

Commit the handoff doc. Tell the user:

> "Handoff written. Resume in a fresh session with:
> `/flow:resume-handoff <handoff-path>`
> or just `/flow:implement <plan-path>` (it picks up from the plan's checkmarks)."

## Rules

- **Pointers, not copies.** Reference artifacts by path — don't paste plan contents, design docs, or code into the handoff. The next agent reads the files.
- **No secrets.** Redact API keys, passwords, tokens. Reference them by name ("the Stripe test key in `.env`"), not value.
- **Commit before handing off.** Dirty state is invisible to the next session. Stash if you can't commit cleanly.
- **Link the plan.** The plan is the durable ledger. The handoff is a shortcut into it, not a replacement for it.
