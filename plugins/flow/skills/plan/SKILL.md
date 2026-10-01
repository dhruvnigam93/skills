---
name: plan
description: >-
  Write the implementation plan for one software feature — after design, before
  any code. Use when the user says "plan this", "write the plan", "break this into
  steps", "create an implementation plan", "turn the design into steps", "/plan",
  or right after a design doc is signed off.
argument-hint: "[path to design doc, or a feature description]"
---

# Plan Phase

Turn one feature's design into a plan of small, commit-sized steps. The plan is what `/flow:implement` executes and fills in as it goes. `/plan` never writes code.

Write every step for an implementer that is a **cheap model with no context**: it reads the plan header and its one step — not the design doc, not the other steps, not this conversation. A step that only makes sense with that wider context gets guessed at, and guesses fail review.

**Output:** exactly one file at `<repo-root>/thoughts/shared/plans/YYYY-MM-DD-<kebab-desc>.md`
- `<repo-root>` = `git rev-parse --show-toplevel` (the worktree root if you are in one)
- `YYYY-MM-DD` = today; `<kebab-desc>` = the design doc's slug, which is also the branch slug
- Example: `thoughts/shared/plans/2026-10-01-order-cancellation.md` for `designs/2026-10-01-order-cancellation.md` on `feat/order-cancellation`
- Create the directories if missing. If a plan with this slug already exists, ask before touching it.

## Iron Law

```
EVERY STEP MUST BE BUILDABLE AND VERIFIABLE FROM THE PLAN HEADER + THAT STEP ALONE
```

## Process

### 1. Find the design, isolate, check scope

- **Signed design doc** — the path passed in, or the doc in `thoughts/shared/designs/` matching the current branch's slug, with `status: signed-off`. Read it fully, plus its `references:`. Its Interface Spec is the source of every signature in the plan.
- **No design, or only a draft** — recommend it in one line, then follow the user's call. Never block on it:
  > "There's no signed design for this. I'd run `/flow:design` first — or I can plan straight from what you've described. Which?"

  If they choose to plan, what they described (plus the draft, if any) is the design. Any signature the plan introduces gets approved with the plan at sign-off.
- **Branch** — if you are on the default branch, propose `feat/<kebab-desc>` off main and create it on confirm. Never commit the plan to the default branch. (If `/flow:design` ran, you are already on its branch.)
- **One feature** — if the input describes more than one feature, plan the first and name the others as separate plans. Test: if X could ship and be useful without Y, they are two features.

### 2. Ground every step in the repo

Read the code the steps will touch, plus `kb/architecture.md` and `kb/domain.md` if they exist. Subagents are optional — use them for a large feature, read directly for a small one. Collect:
- exact paths to modify, and where new files belong (follow the existing layout)
- the project's real commands — from the Makefile, `package.json`, `pyproject.toml`, or CI config. Never guess a command.
- existing tests the new ones should mirror

If something blocks a step and neither the design nor the code answers it, ask — one batched round of 3–5 questions, each with a recommended answer. Never write an open question into the plan. If the user says "enough", use your recommendations and list them under **Assumptions** in the plan header.

If a step needs an interface the signed design lacks or contradicts, stop and raise it. That is a design change, and design belongs to the user.

### 3. Draft success criteria, then steps

**Success criteria first:** what must be true when the whole feature is done, each line with its own check. The steps exist to make these pass.

**A step is a commit:** a small lift that does one thing, has an automated check that proves it, and is easy to review and understand on its own.
- If naming the step needs "and", split it.
- If two changes would always be approved or rejected together, merge them.
- Every step leaves the repo working and its tests green.

**Order:** the thinnest end-to-end path first, then widen — so each step is verifiable on its own. A wide mechanical change (rename, retype) goes expand → migrate in batches → contract, green at each step.

**Phases:** group steps into phases. End a phase where the user should look by hand; `/flow:implement` pauses there.

Write the plan from [templates/plan.md](templates/plan.md). Each step carries:

| Field | Carries |
|-------|---------|
| `Do:` | one-sentence goal, plus a short ordered sequence if order matters |
| `Files:` | every path touched, marked create / modify / test |
| `Interfaces:` | `Uses:` what it calls from the repo or earlier steps · `Adds:` what later steps rely on — full signatures |
| `Scope:` | what changes, then `Must NOT change:` the nearby things it leaves alone |
| `Verify:` | tests to add (name + behavior asserted, exact values) and the literal command + expected output — or `MANUAL:` |
| `Decision:` | optional — only when the next step depends on something unknowable until run |
| `Impl note:` / `Review note:` | left empty — filled during implementation and step review |

Signatures, file names, sequences, commands — yes. Function bodies and test code — no. The body is the implementer's job, and code written into a plan is code nobody reviewed against the design.

✅ A step a no-context model can build:
```
### [ ] Step 3 — Reject cancelling a shipped order

**Do:** Guard the top of `cancel_order`: if the order is SHIPPED, raise `OrderAlreadyShipped` before any refund call.
**Files:** `src/orders/cancel.py` (modify) · `src/orders/errors.py` (modify) · `tests/orders/test_cancel.py` (test)
**Interfaces:**
- Uses: `cancel_order(order_id: OrderId, reason: CancelReason) -> CancellationReceipt` (Step 2)
- Adds: `class OrderAlreadyShipped(OrderError)` in `src/orders/errors.py`
**Scope:** Only the guard and the new error. Must NOT change: the refund flow, `CancellationReceipt` fields, `OrderStatus` values.
**Verify:**
- Test `test_cancel_shipped_order_raises`: a SHIPPED order → raises `OrderAlreadyShipped`; status stays SHIPPED; refund gateway not called.
- `uv run pytest tests/orders/test_cancel.py -v` → all pass, including `test_cancel_shipped_order_raises PASSED`
**Impl note:**
**Review note:**
```

❌ Too vague:
```
### Step 3 — Cancellation edge cases
Handle shipped orders and other edge cases in the cancel flow, and add tests.
Verify: run the tests.
```
"Other edge cases" decides nothing; no files; the implementer must read the design to learn what "shipped" means; "run the tests" was green before the change too.

❌ Too deep:
```
**Do:** Add to cancel.py:
    if order.status == OrderStatus.SHIPPED:
        raise OrderAlreadyShipped(order.id)
```
That is the implementation. Give the signature, the rule, and the test.

**Verify** follows the hierarchy in [references/verification.md](references/verification.md): a test where possible, else another automated check, else `MANUAL:`. Every check must fail before the step's change.

**Decision points** — only when the right next step depends on something the plan cannot know (an external API's behavior, a measured number). Name the observation and each fork:
```
**Decision:** run `uv run python scripts/probe_refund.py` → if the response has `refund_id`, continue to Step 5; if it is `404`, take Fork B (Steps 5B–6B: poll the refund webhook instead).
```

### 4. Self-review

Check with fresh eyes before presenting. Fix inline.

1. **Local-context test** — read each step with only the header beside it. Does every name it uses already exist in the repo or appear in an earlier step's `Adds:`? Could you build it and run its Verify without opening anything else?
2. **Coverage** — every interface in the design maps to a step; every success criterion is proven by a step's Verify or its own check.
3. **Checks can fail** — each Verify fails before its change. No bare "run the tests".
4. **Consistency** — names and signatures match across steps and the design. `clear_layers` in Step 3 and `clear_all_layers` in Step 7 is a bug.
5. **No code, no placeholders** — no function bodies; no "TBD", "handle edge cases", "add validation", "similar to Step 4".
6. **Scope** — one feature; nothing from Out of Scope crept in.

### 5. Sign-off

Present the plan in chat: the success criteria, then a compact table (step · what it does · how it is verified), then the file path. This is the one checkpoint — the user approves the steps and their checks together. Revise until they sign off.

On sign-off:
1. Set `status: signed-off` in the frontmatter
2. Commit the plan file
3. Tell the user: "Plan signed off. Next step is `/flow:implement`, which works through it one step at a time."

## Red Flags

| Thought | Reality |
|---------|---------|
| "The implementer can find the right file." | It reads one step. Name the path. |
| "Two small changes, one step is fine." | If a reviewer could approve one and reject the other, they are two steps. |
| "Faster to write the code here." | Then nobody reviews it against the design. Signature + test, not body. |
| "`make test` verifies it." | It was green before the change. Name the check that fails without it. |
| "I'll leave this as an open question in the plan." | Ask now. The plan carries decisions, not questions. |
