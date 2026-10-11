---
name: resume-handoff
description: >-
  Resume work from a handoff document written by a previous session. Use when the
  user says "resume", "pick up where we left off", "continue from the handoff",
  "/resume-handoff", or provides a path to a handoff doc.
argument-hint: "<path to handoff doc>"
---

# Resume from Handoff

Pick up work from a handoff document. Validate that the world matches what the handoff describes, then continue — usually via `/flow:implement`.

## Process

### 1. Find the handoff

- **Path provided** — read it.
- **No path** — look in `thoughts/shared/handoffs/` for the most recent file on the current branch. If multiple exist, use the one with the latest date in the filename.
- **Nothing found** — ask: "I can't find a handoff doc. Do you have a path, or should I check the plan directly?"

### 2. Read and validate

Read the handoff fully. Then validate current state against what it describes:

| Check | How |
|-------|-----|
| Branch exists and is current | `git branch --show-current` |
| HEAD matches or is ahead of handoff's commit | `git log --oneline <handoff-commit>..HEAD` |
| Plan file exists and has the expected checkmarks | Read the plan, compare checked steps |
| Stashed work (if noted) | `git stash list` — pop if the handoff says to |
| Referenced files still exist | Spot-check the critical references |

**If state diverged** (commits after the handoff, plan modified, branch rebased):
- Tell the user what changed since the handoff
- Propose how to proceed: usually, trust the plan's checkmarks + git log over the handoff's description
- Get a one-word confirmation before continuing

**If state matches:** proceed without asking.

### 3. Ingest context

Read, in order:
1. The **plan file** — the plan is the durable ledger; the handoff is a shortcut into it
2. The **design doc** referenced in the plan's frontmatter (if it exists)
3. The **critical references** listed in the handoff
4. The **learnings** section — gotchas and discoveries to carry forward

Do NOT dispatch subagents for this. Read the files yourself — this is intake, not research. You need this context in your own window.

### 4. Resume

If the handoff points to a plan mid-implementation:
- Run `/flow:implement <plan-path>` — it resumes from the first unchecked step automatically
- The handoff's "Base for next step" is the base commit for the step-reviewer

If the handoff points to a different phase (design, research):
- Tell the user which skill to invoke and with what arguments
- Or invoke it directly if the handoff is clear about what's next

### 5. Report

Before starting work, give a one-line status:
> "Resuming from Step N+1 of `<plan>` on branch `<branch>`. Last committed step: N. Continuing."

Then start. Don't present a lengthy analysis or ask "shall I proceed?" — the user resumed for a reason.

## Rules

- **Trust the plan over the handoff.** The plan has checkmarks updated at commit time. The handoff is a snapshot that may be slightly stale.
- **Trust git over memory.** `git log` is the record. The handoff is a pointer into it. If they disagree, git wins.
- **Validate before acting.** Never assume the handoff state matches current state — check first. But don't turn validation into a ceremony. Three quick checks, then go.
- **Don't re-research.** The handoff's Learnings section carries what the previous agent discovered. Read it, don't re-derive it. If it seems wrong, verify the specific claim — don't re-explore the whole area.
- **Pop stashed work.** If the handoff notes a stash, pop it before starting. Stashed changes are invisible otherwise and the next commit will miss them.
