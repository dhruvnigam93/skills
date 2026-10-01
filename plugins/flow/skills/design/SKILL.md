---
name: design
description: >-
  Run the DESIGN PHASE for a software feature — architecture decisions, interface
  shapes, and schema definitions — before any planning or coding begins. Use when
  the user says "design this", "let's think through the interface", "how should we
  structure this", "what should the API look like", "design before we plan",
  "design the architecture", or "/design". 
user_invocable: true
---

# Design Phase

Produce a **Design Doc** for a single feature — problem framing, architecture, and every new or changed interface and schema. The downstream `/plan` skill consumes this doc. `/design` never invokes `/plan` itself.

**Output:** exactly one file at `<repo-root>/thoughts/shared/designs/YYYY-MM-DD-<kebab-desc>.md`
- `<repo-root>` = `git rev-parse --show-toplevel` (the worktree root if you are in one)
- `YYYY-MM-DD` = today; `<kebab-desc>` = the same slug as the Phase 0 branch
- Example: `thoughts/shared/designs/2026-10-01-order-cancellation.md` on branch `feat/order-cancellation`
- Create the directories if missing. Never write the doc anywhere else.

## Hard Gate

```
NO PLANNING OR CODE WITHOUT A SIGNED DESIGN
```

## Process

### Phase 0: Isolate (branch/worktree)

Before writing any artifact, isolate the feature. If you are on the default branch (`main`/`master`), do not write the design doc there — propose a branch and create it on confirm:

> "I'll branch `feat/<kebab-desc>` off main for this — or want a worktree (parallel work / greenfield)?"

Default to a **branch**; use a **worktree** when the user wants parallel isolation or it's greenfield/ralph. Always branch from main unless otherwise specified. The whole feature — design doc → plan → code → the kb/ updates it makes true — then lives on this branch and merges to main as one unit (kb/ and thoughts/ are git-tracked, never gitignored). If a signed design doc for this feature already exists on a branch, resume there instead of branching again.

### Phase 1: Self-Research

Before asking the user ANYTHING, answer everything the codebase can answer. Never ask the user what the code can tell you — that wastes their time on work you can do in seconds.

Subagents are optional. For a small ask, read the code yourself; for a larger one, dispatch any of these — your call, based on the request and its assessed complexity:

| Subagent | Task |
|----------|------|
| **codebase-locator** | Find all files related to the feature area |
| **codebase-analyzer** | Understand how the current implementation works |
| **codebase-pattern-finder** | Find similar interfaces and patterns to model after |
| **thoughts-locator** | Find existing research, designs, or decisions about this area |

Also read these files if they exist (skip silently if not):
- `kb/domain.md` — project glossary and domain terms
- `kb/architecture.md` — system architecture overview

If the user linked a prior `/research` doc, read it fully. If you dispatched subagents, wait for all of them before Phase 2.

### Phase 2: Batched Question Rounds

Ask questions in **batched rounds of 3-5**, most important first. This is a deliberate choice over one-question-at-a-time grilling — the user prefers efficient rounds.

Every question carries a **recommended answer** with a one-line rationale. The user can accept the recommendation with one word ("yes", "sounds right", "go with that").

**Render the assumption ledger table at the top of every round** and update it as the user responds.

Good round:
```
## Assumption Ledger

| # | Assumption | Status | Basis |
|---|-----------|--------|-------|
| (first round — ledger empty) |

### Round 1

1. Should cancelled orders be soft-deleted or hard-deleted?
   Recommended: soft-delete (preserves audit trail for compliance).

2. Do refunds route through the original payment gateway?
   Recommended: yes (simplifies reconciliation, avoids dual-gateway complexity).

3. Maximum order age for cancellation?
   Recommended: 30 days (matches industry chargeback window).
```

What makes this good: each question targets a decision the codebase could not answer; recommended answers are grounded in concrete rationale (compliance, reconciliation, industry standard); three questions, not twelve.

Bad questions:
- "What does the current order model look like?" — the codebase told you this in Phase 1.
- "Can you describe the feature?" — the user already did.
- Ten questions in one round — important ones get buried.

**The "enough" stop-gap.** When the user says "enough", "just go", or "I trust your judgment":
1. Mark all remaining unverified assumptions as ASSUMED
2. State the safe default for each (never leave it implicit)
3. Keep them visible in the ledger — never delete an assumption
4. Proceed with the design using those defaults

### Phase 3: Interface Spec

Document EVERY new or changed interface and schema — signature, invariants, error modes, ordering constraints, dependencies (the template has a slot for each). This is the central section of the design doc — if you skip it, the downstream /plan inherits guesses instead of decisions.

The right altitude — show, do not tell:

Right (design altitude):
```
cancelSubscription(id: SubscriptionId, reason: CancelReason) -> CancellationReceipt
  Invariant: idempotent — calling twice returns the original receipt.
  Error: SubscriptionNotFound if id does not exist.
  Ordering: must be called after activate(); no-op if already cancelled.
  Dependency: takes BillingGateway as injected adapter.
```

Wrong (too shallow):
```
cancelSubscription(id) — cancels a subscription
```
A sketch, not a spec.

Wrong (too deep — this is /plan territory):
```
Step 1: Create CancellationService in src/billing/cancellation.ts
Step 2: Add test in src/billing/__tests__/cancellation.test.ts
Step 3: Run `bun test src/billing` to verify
```

**Altitude split.** Mixing altitudes produces a plan built on unverified design assumptions — the single most expensive failure mode in a coding workflow. If you catch yourself writing something from the right column, stop; that is /plan work.

| /design owns | /plan owns |
|-------------|-----------|
| Problem framing and context | Feature success criteria |
| Module boundaries, seam placement | Atomic implementation steps |
| Signatures, invariants, error modes, schemas | Exact file paths to create/modify |
| Load-bearing variant decision | Verify commands (test, lint, etc.) |

### Phase 4: Flag Load-Bearing Interfaces

Flag which interfaces are **load-bearing** — ALL of these hold (the same bar as an ADR):
- Multiple callers or adapters will use it
- Hard to reverse once implemented
- A genuine trade-off exists between competing designs

Present your flags; the user decides which are truly load-bearing, not you. For each confirmed one, run the **Design-It-Twice** protocol in [references/design-it-twice.md](references/design-it-twice.md) — cheap parallel subagents, one design constraint each; you recommend, the user picks.

Everything else is documented once and moves on — most interfaces are not load-bearing, and running variants for everything wastes time and attention.

### Phase 5: Assemble the Design Doc

Write the doc to the **Output** path using [templates/design-doc.md](templates/design-doc.md). Every frontmatter field is required (`git_commit` = `git rev-parse --short HEAD`, `branch` = the Phase 0 branch).

**Self-review before presenting.** Check with fresh eyes:

1. **Placeholder scan** — any TBD, TODO, "...", or empty sections? Fill them.
2. **Internal consistency** — do interface names match everywhere? Does the architecture section align with the interface spec?
3. **Scope** — does this cover exactly one feature? If it drifts into a second feature, cut it.
4. **Ambiguity** — could any requirement be read two ways? Pick one and state it.
5. **Altitude** — anything from the /plan column of the altitude split? Remove it.

Fix issues inline. No separate review cycle — just fix and move on.

### Phase 6: Sign-Off Gate

Present the design doc. If the user requests changes, revise and present again — sign-off is the only exit.

On sign-off:
1. Update `status: signed-off` in the frontmatter
2. Commit the design doc
3. Tell the user: "Design signed off. Next step is `/plan`, which consumes this doc."

## Deep-Modules Vocabulary

Use these terms in every design doc. Never substitute "component", "service", "unit", "API", or "boundary" — they blur the distinctions that matter during design ("API" covers only the type surface; "boundary" collides with DDD bounded contexts). Nuances, dependency categories, and the depth diagram: [references/deep-modules.md](references/deep-modules.md).

| Term | Meaning |
|------|---------|
| **Module** | Anything with an interface and an implementation. Scale-agnostic. |
| **Interface** | Everything a caller must know: signatures + invariants + ordering + errors. |
| **Implementation** | What is inside the module; the body of code. |
| **Depth** | Leverage at the interface — behavior per unit of interface learned. |
| **Seam** | Where you can alter behavior without editing there. _(Feathers)_ |
| **Adapter** | A concrete thing that satisfies an interface at a seam. |
| **Leverage** | What callers get from depth — more capability per unit of interface. |
| **Locality** | What maintainers get — change concentrates in one place. |

Three tests that do most of the design work:
- **Deletion test:** imagine deleting the module. If complexity reappears across N callers, it was earning its keep. If it vanishes, it was a pass-through.
- **Interface = test surface:** callers and tests cross the same seam. If you test past the interface, the module shape is wrong.
- **One adapter = hypothetical seam. Two adapters = real one.** Do not cut a seam until something actually varies across it.

## Domain Discipline

When the user's term conflicts with the project glossary (`kb/domain.md` or `CONTEXT.md`), call it out explicitly:

> "You said 'cancellation' but the glossary uses 'termination' — which should we standardize on?"

When the user's stated behavior contradicts what the code actually does, surface the contradiction:

> "You said partial cancellation is possible, but `OrderService.cancel()` deletes the entire order. Which is correct — should we change the code, or was the description inaccurate?"

Never silently adopt either side. The language and the code are forced to agree; the user decides which is right.
