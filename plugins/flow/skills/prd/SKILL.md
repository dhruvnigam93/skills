---
name: prd
description: >-
  Define what a feature should achieve — the product outcome, not the technical
  design. Use when the user says "write a PRD", "define the product requirements",
  "what should this feature do", "spec out the product", "/prd", or when the
  product outcome needs defining before technical design begins.
argument-hint: "[feature name or product goal]"
---

# PRD Phase

Define what a feature should achieve and why — the product outcome, iterated with the same rigor as `/flow:design`. A PRD is non-technical: it says what the user/customer gets, not how it's built. The downstream `/flow:design` consumes this doc.

**Output:** exactly one file at `<repo-root>/thoughts/shared/prds/YYYY-MM-DD-<kebab-desc>.md`
- `<repo-root>` = `git rev-parse --show-toplevel`
- Create the directories if missing.

## Process

### 1. Scope and isolate

- **One feature.** If the input describes more than one, scope the first and name the others. Test: if X could ship and be useful without Y, they are two features.
- **Branch** — if on the default branch, propose `feat/<kebab-desc>` off main and create on confirm. The PRD is the first artifact on the feature branch — never commit it to the default branch.

### 2. Self-research

Before asking the user anything, answer what the codebase can answer. Read relevant code, `kb/domain.md`, any existing PRDs or research docs. Dispatch subagents for large scopes. Never ask the user what the code can tell you.

### 3. Batched question rounds

Ask questions in **batched rounds of 3–5**, most important first. Each question carries a **recommended answer** with a one-line rationale. The user can accept with one word.

Questions target **product decisions** the codebase can't answer:
- Who is this for?
- What does success look like from the user's perspective?
- What's explicitly out of scope?
- What are the constraints (timeline, compatibility, dependencies)?

✅ Good: "Should cancelled orders still appear in the user's order history? Recommended: yes, greyed out (users expect to find past orders for returns/disputes)."

❌ Bad: "What database should we use?" — that's technical design, not product.

❌ Bad: "What does the current order model look like?" — the codebase told you.

**Render the assumption ledger at the top of every round.** Update it as the user responds.

**The "enough" stop-gap.** When the user says "enough" or "just go":
1. Mark remaining assumptions as ASSUMED with safe defaults
2. State each default explicitly
3. Keep them visible in the ledger
4. Proceed

### 4. Write the PRD

Use [templates/prd.md](templates/prd.md). Every frontmatter field is required.

**Self-review before presenting:**
1. Placeholder scan — any TBD, TODO, or empty sections? Fill them.
2. Scope — exactly one feature? Nothing technical crept in?
3. Success criteria — each one observable from the user's perspective?
4. Assumptions — all accounted for in the ledger?

### 5. Sign-off

Present the PRD. Revise until the user signs off — sign-off is the only exit.

On sign-off:
1. Set `status: signed-off` in the frontmatter
2. Commit the PRD
3. Tell the user: "PRD signed off. Next step is `/flow:design` (or `/flow:research` first if the domain is unfamiliar), which consumes this doc."

## Rules

- **Non-technical.** No database choices, no API shapes, no implementation details. If you catch yourself writing a signature or a file path, stop — that belongs in `/flow:design`.
- **User-facing language.** Success criteria describe what the user sees or experiences, not what the system does internally.
- **Same T2 mechanics as /design.** Batched rounds, recommended answers, assumption ledger, "enough" stop-gap. The rigor is the same; the altitude is different.
