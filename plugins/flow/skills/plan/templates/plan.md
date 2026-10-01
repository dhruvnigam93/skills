# Plan Template

Every /plan invocation produces one file with this structure. All sections are required — if a section has nothing to say, write "None" rather than omitting it.

The header (everything above Phase 1) is read by the implementer at every step, so keep it short and include only what every step needs.

```markdown
---
date: YYYY-MM-DDTHH:MM:SS+TZ       # ISO-8601 with timezone
author: agent (model-id)            # e.g. "agent (claude-opus-5-5)" or "user"
git_commit: abc1234                 # git rev-parse --short HEAD
branch: feat/order-cancellation     # current branch
status: draft                       # draft | signed-off | implementing | done | superseded
references:
  - thoughts/shared/designs/2026-10-01-order-cancellation.md   # or: none — planned from the user's description
---

# Plan: [Feature Name]

**Goal:** One sentence — what works when this plan is done.

## Success Criteria

What must be true when the whole feature is done. Each line carries its own check.

- [ ] Cancelling a pending order returns a receipt — `curl -s -X POST localhost:8000/orders/123/cancel | jq -r .status` → `cancelled`
- [ ] No regressions — `make test` → exit 0
- [ ] MANUAL: the refund appears in the Stripe test dashboard within a minute

## Context for Every Step

- **Stack:** [language, framework, test runner]
- **Commands:** test `[exact command]` · lint `[exact command]` · typecheck `[exact command]`
- **Conventions:** [only the repo rules a step could get wrong — where errors live, test layout, naming]
- **Design:** `[path]` — background only; no step requires reading it

## Out of Scope

- [From the design's Out of Scope, plus anything this plan deliberately defers]

## Assumptions

- [Anything assumed rather than confirmed — the user said "enough", or there is no design. Otherwise "None".]

## Phase 1: [Name] — [what works at the end of this phase]

### [ ] Step 1 — [does one thing]

**Do:**
**Files:**
**Interfaces:**
- Uses:
- Adds:
**Scope:** … Must NOT change: …
**Verify:**
**Impl note:**
**Review note:**

### [ ] Step 2 — [does one thing]

…

> **Phase 1 checkpoint** — MANUAL: [what the user looks at before Phase 2], or "none — automated checks cover it".

## Phase 2: [Name] — [what works at the end of this phase]

…
```

Conventions:
- `[ ]` → `[x]` when a step is done, so `grep -n '^### \[ \]'` finds the next step.
- Fork steps are numbered from their decision point: Step 5B, 6B.
- `Decision:` sits between `Verify:` and `Impl note:` in the step that makes the observation.
