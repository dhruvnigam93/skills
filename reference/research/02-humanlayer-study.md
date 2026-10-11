---
date: 2026-07-02
author: claude-fable-5 (Explore subagent)
status: active
references:
  - ../inspiration/humanlayer/
  - ~/.claude/skills/ (Dhruv's local adaptations)
  - ~/.claude/commands/ (Dhruv's local adaptations)
purpose: Primary research — humanlayer workflow system + where Dhruv's local copies diverge (high-signal for his preferences)
---

# humanlayer/humanlayer — Study Report (+ Dhruv's local divergences)

## 1. Philosophy

- **Research → Plan → Implement with human gates.** 12 Linear statuses. Key line from `linear.md`: "Review and alignment happen at the plan stage (not PR stage) to move faster and avoid rework."
- **Frequent intentional context compaction.** Orchestrator (Opus) synthesizes; subagents (Sonnet) do output-only work. Research outputs → `thoughts/` (git-tracked knowledge layer). Locator-then-analyzer pattern minimizes context.
- **Documentarians, not critics** (subagents): "CRITICAL: YOUR ONLY JOB IS TO DOCUMENT AND EXPLAIN THE CODEBASE AS IT EXISTS TODAY" / "You are a documentarian, not a critic or consultant".

## 2. Phase commands

### research_codebase.md (opus)
Read mentioned files FULLY first → decompose into parallel subagents → wait for ALL → synthesize with file:line refs → write `thoughts/shared/research/YYYY-MM-DD-ENG-XXXX-description.md` → permalinks → sync.

### create_plan.md (opus)
5 steps: Context, Research & Discovery, Plan Structure, Detailed Writing, Sync & Review.
Key lines: "Don't write the full plan in one shot" / "Get buy-in at each major step" / "If you encounter open questions during planning, STOP. Research or ask for clarification immediately."
Also: "Question vague requirements"; if user corrects a misunderstanding — "DO NOT just accept the correction - Spawn new research tasks to verify".

### implement_plan.md (default model)
"After completing all automated verification for a phase, pause and inform the human that the phase is ready for manual testing." / "do not check off items in the manual testing steps until confirmed by the user." Mismatch protocol: STOP and present Expected/Found/Why it matters/How to proceed.

### iterate_plan.md — surgical edits, not rewrites. validate_plan.md — post-hoc validation report.

## 3. Plan template (verbatim skeleton — Dhruv's creating-plan uses the same)

```markdown
# [Feature] Implementation Plan
## Overview
## Current State Analysis
## Desired End State
### Key Discoveries: [file:line refs]
## What We're NOT Doing
## Implementation Approach
## Phase 1: [Name]
### Overview
### Changes Required:
#### 1. [Component/File Group]
**File**: `path/to/file.ext`
**Changes**: [Summary]
### Success Criteria:
#### Automated Verification:
- [ ] Unit tests pass: `make test-component`
#### Manual Verification:
- [ ] Feature works as expected when tested via UI
**Implementation Note**: pause here for manual confirmation
```

## 4. Dhruv's local divergences (HIGH SIGNAL — his revealed preferences)

- **creating-plan/**: template externalized to `templates/plan-template.md` + `references/` (success-criteria.md, patterns.md, sub-task-guide.md) — he modularizes.
- **research_codebase_generic.md**: **REMOVED the "documentarian, not critic" block** — he wants opinionated research. Removed humanlayer-specific paths/sync.
- **implementing-plan/**: kept nearly verbatim — he agrees with strict human gates at implementation.
- **create-handoff / resume-handoff**: heavily reworked/original. resume-handoff has: 3 input modes, state validation ("Never assume handoff state matches current state" — git log from handoff commit to HEAD), 5 scenario handlers (clean/diverged/incomplete/stale/missing-refs), confirmation before proceeding.
- **prd-development/**: entirely his own. 3 interaction modes (Guided / Context dump / Best guess), 8 phases, anti-patterns ("Solution too prescriptive").
- Carried verbatim: describe_pr, linear, ralph_*, oneshot*, founder_mode, create_worktree, local_review, debug, validate_plan, iterate_plan.
- Pattern: genericize, modularize, add product layer, preserve control points, drop dogma that constrains (documentarian).

## 5. Subagent architecture (all sonnet)

| Agent | Tools | Role |
|-------|-------|------|
| codebase-locator | Grep, Glob, LS | find WHERE (no Read!) |
| codebase-analyzer | +Read | explain HOW, file:line refs |
| codebase-pattern-finder | +Read | similar implementations w/ snippets |
| thoughts-locator / thoughts-analyzer | | same split for thoughts/ |
| web-search-researcher | WebSearch etc. | external, must return links |

Spawning guidance: "Don't write detailed prompts about HOW to search - the agents already know" / "Just tell it what you're looking for". Tool restrictions enforce separation (locators can't Read).

Ralph pipeline: `humanlayer-nightly launch --dangerously-skip-permissions ... "/implement_plan and when done ... commit ... describe_pr ... comment on Linear"` — fully autonomous chain; zero checkpoints once launched (the inspiration for Dhruv's oneshot track, but his version keeps reviewer gates).

## 6. Gaps vs Dhruv's tenets

| Tenet | Gap |
|-------|-----|
| Alignment checkpoints | Ralph bypasses all gates |
| Surface assumptions | No pre-implementation interpretation checkpoint |
| Human owns design | Plan stops at file-level; NO class/method signature spec |
| Atomic steps w/ own tests | Phase-level granularity only |
| Independent diff-vs-intent review | **Not implemented at all — biggest gap** |
| Deploy+verify feedback | Success criteria = build/test/lint only; no deploy-then-verify pattern |
| Subagents for research | Well implemented ✓ |
