# PRD Template

Every /prd invocation produces one file with this structure. All sections are required — if a section has nothing to say, state that explicitly rather than omitting it.

```markdown
---
date: YYYY-MM-DDTHH:MM:SS+TZ
author: agent (model-id)
git_commit: abc1234
branch: feat/order-cancellation
status: draft                       # draft | signed-off | superseded
references:
  - <any prior research or PRD>     # or: none
---

# PRD: [Feature Name]

One-line summary of what this feature delivers to the user.

## Problem

What problem does the user have today? Why does it matter? Ground it in evidence
if available (support tickets, usage data, user feedback). 1–3 paragraphs.

## Assumption Ledger

| # | Assumption | Status | Basis |
|---|-----------|--------|-------|
| 1 | Example | VERIFIED | User confirmed, round 1 |

Status: VERIFIED (user confirmed) · ASSUMED (safe default after "enough") · UNVERIFIED (still open — none in a signed-off doc).

## Users

Who is this for? Be specific — role, context, frequency of use.

## Success Criteria

What must be true when this feature ships, from the user's perspective.
Each criterion is observable and testable.

- [ ] A user can cancel a pending order and sees a confirmation within 3 seconds
- [ ] Cancelled orders appear in order history, greyed out, with the cancellation reason
- [ ] MANUAL: a refund appears in the payment provider dashboard within 5 minutes

## Scope

### In scope
What this feature covers.

### Out of scope
What this feature explicitly does NOT cover. These become the "Out of Scope" for
the downstream /design and /plan.

## Constraints

Timeline, compatibility requirements, regulatory, dependencies on other teams or
systems. "None" if none.

## Open Questions

Questions that remain after the rounds — resolved during /design, not here.
"None" if all questions are resolved.
```
