---
name: design
description: >-
  Run the DESIGN PHASE for a software feature — architecture decisions, interface
  shapes, and schema definitions — before any planning or coding begins. Use when
  the user says "design this", "let's think through the interface", "how should we
  structure this", "what should the API look like", "design before we plan",
  "design the architecture", or "/design". Also trigger when a user is about to
  start /plan or implementation for a nontrivial feature and no design doc exists
  yet — the design phase always precedes planning. If the user wants to skip
  design for speed, that is what /oneshot is for; /design is never skipped by
  default.
user_invocable: true
---

# Design Phase

Produce a **Design Doc** for a single feature — problem framing, architecture, and every new or changed interface and schema — before any planning or coding begins. The downstream `/plan` skill consumes this doc. `/design` never invokes `/plan` itself.

Output: one file at `thoughts/shared/designs/YYYY-MM-DD-<kebab-desc>.md` (create directory if needed; fall back to `docs/designs/` if no `thoughts/` directory exists).

## Hard Gate

**No planning and no code until the user signs off on the design.**

This applies to EVERY feature regardless of perceived simplicity. A trivial feature gets a trivial design (three sentences, one interface) but it still gets written and signed. The cost of a boring confirmation is near zero; the cost of a missed assumption is an entire plan rebuilt on a false foundation.

If the user wants speed, that is the `/oneshot` track and only the user selects it.

### Rationalization Table

You will feel the pull to skip this. Recognize the thought and override it.

| Rationalization | Why it is wrong |
|----------------|----------------|
| "This is too simple to need a design" | Simple features have the most hidden assumptions. A trivial design is 3 sentences — write them. |
| "I already know the interface" | You know your guess. The user has not confirmed it, and the codebase may contradict it. |
| "The user seems in a hurry" | Then write a short design fast. Hurry is not a reason to skip; it is a reason to be concise. |
| "I'll design while I plan" | Design and planning are different altitudes. Mixing them produces a plan built on unverified assumptions. |
| "The research already answered everything" | Research answers how the codebase IS. Design answers how it SHOULD CHANGE. Different question. |
| "The user didn't say /design" | The gate is on the WORK, not the command. Nontrivial features need design regardless of how the user phrased the request. |

### Red-Flags Self-Check

Before producing ANY plan step or code, stop and verify:

- Am I about to write an implementation step? That is /plan territory.
- Am I choosing between approaches without documenting the trade-off? That is design work — do it here first.
- Am I defining a new function, class, or schema inside a plan? That signature belongs in the design doc.
- Have I written the assumption ledger? If not, I have not done the design.
- Has the user said "looks good" / "approved" / "sign off"? If not, the design is not done.

## Process

### Phase 1: Self-Research

Before asking the user ANYTHING, answer everything the codebase can answer. Never ask the user what the code can tell you — that is wasting their time on work a subagent can do in seconds.

Spawn these read-only subagents in parallel:

| Subagent | Task |
|----------|------|
| **codebase-locator** | Find all files related to the feature area |
| **codebase-analyzer** | Understand how the current implementation works |
| **codebase-pattern-finder** | Find similar interfaces and patterns to model after |
| **thoughts-locator** | Find existing research, designs, or decisions about this area |

Also read these files if they exist (skip silently if not):
- `kb/domain.md` — project glossary and domain terms
- `kb/architecture.md` — system architecture overview

If the user linked a prior `/research` doc, read it fully before proceeding.

Wait for ALL subagents to complete before moving to Phase 2.

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

Document EVERY new or changed interface and schema. This is the central section of the design doc — if you skip it, the downstream /plan inherits guesses instead of decisions.

For each interface, specify:
- **Signatures** with types
- **Invariants** (what must always be true)
- **Error modes** (what can go wrong and how it surfaces)
- **Ordering constraints** (what must happen before/after)
- **Dependencies** (what the module takes as input or injection)

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
Missing: return type, invariants, errors, ordering, dependencies. This is a sketch, not a spec.

Wrong (too deep — this is /plan territory):
```
Step 1: Create CancellationService in src/billing/cancellation.ts
Step 2: Add test in src/billing/__tests__/cancellation.test.ts
Step 3: Run `bun test src/billing` to verify
```
File paths, steps, and verify commands belong in /plan, not /design.

### Phase 4: Flag Load-Bearing Interfaces

After documenting all interfaces, flag which ones are **load-bearing**. An interface is load-bearing when ALL of these hold:
- Multiple callers or adapters will use it
- Hard to reverse once implemented
- A genuine trade-off exists between competing designs

This is the same bar as an ADR (Architecture Decision Record). Present your flags to the user for confirmation — the user decides which interfaces are truly load-bearing, not you.

For confirmed load-bearing interfaces, run the **Design-It-Twice** protocol: read [references/design-it-twice.md](references/design-it-twice.md) and spawn parallel subagents to produce radically different variants. Each subagent works under a different constraint (minimize interface, maximize flexibility, optimize common caller, optionally ports-and-adapters). Compare variants by depth, locality, and seam placement. Give an opinionated recommendation — a strong read, not a menu. Propose a hybrid if elements combine well. The user picks; alternatives get a one-line "considered because..." in the design doc.

Non-load-bearing interfaces get documented once and move on. No variant analysis needed — most interfaces are not load-bearing, and running variants for everything wastes time and attention.

### Phase 5: Assemble the Design Doc

Write the design doc using the template at [templates/design-doc.md](templates/design-doc.md).

**Location:** `thoughts/shared/designs/YYYY-MM-DD-<kebab-desc>.md`
- Create the directory if it does not exist
- If there is no `thoughts/` directory, use `docs/designs/` instead
- Example: `thoughts/shared/designs/2025-07-04-order-cancellation.md`

**Lineage frontmatter** (all fields required):

```yaml
---
date: 2025-07-04T14:30:00-07:00
author: agent (claude-opus-4-6)
git_commit: abc1234
branch: feature/order-cancellation
status: draft
references:
  - thoughts/shared/research/2025-07-03-order-system.md
---
```

**Self-review before presenting.** Before showing the doc to the user, check with fresh eyes:

1. **Placeholder scan** — any TBD, TODO, "...", or empty sections? Fill them.
2. **Internal consistency** — do interface names match everywhere? Does the architecture section align with the interface spec?
3. **Scope** — does this cover exactly one feature? If it drifts into a second feature, cut it.
4. **Ambiguity** — could any requirement be read two ways? Pick one and state it.
5. **Altitude** — did any implementation steps, file paths, or verify commands sneak in? Remove them.

Fix issues inline. No separate review cycle — just fix and move on.

### Phase 6: Sign-Off Gate

Present the design doc to the user. The only terminal state is the user signing off.

On sign-off:
1. Update `status: signed-off` in the frontmatter
2. Tell the user: "Design signed off. Next step is `/plan`, which consumes this doc."
3. Do NOT invoke /plan automatically — the user decides when

If the user requests changes, revise the doc and present again. Loop until sign-off.

## Altitude Split

/design and /plan own different altitudes. Mixing them produces a plan built on unverified design assumptions, which is the single most expensive failure mode in a coding workflow.

| /design owns | /plan owns |
|-------------|-----------|
| Problem framing and context | Feature success criteria |
| Module boundaries, seam placement | Atomic implementation steps |
| Signatures, invariants, error modes, schemas | Exact file paths to create/modify |
| Load-bearing variant decision | Verify commands (test, lint, etc.) |

If you catch yourself writing something from the right column, stop. That is /plan work and doing it here means doing it without /plan's discipline.

## Deep-Modules Vocabulary

Use these terms in every design doc. Never substitute "component", "service", "API", or "boundary" — they blur the distinctions that matter during design. Read [references/deep-modules.md](references/deep-modules.md) for the full reference including dependency categories and the visual depth diagram.

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

## References

- [templates/design-doc.md](templates/design-doc.md) — Design doc template with all required sections
- [references/design-it-twice.md](references/design-it-twice.md) — Parallel subagent protocol for load-bearing interface variants
- [references/deep-modules.md](references/deep-modules.md) — Full vocabulary, dependency categories, and design principles
