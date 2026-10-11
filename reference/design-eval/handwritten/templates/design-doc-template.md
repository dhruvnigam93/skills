---
date: <ISO-8601 with timezone, e.g. 2026-07-04T15:30:00+05:30>
author: <you (agent+model, e.g. claude-opus-4-8) or the user>
git_commit: <hash at creation>
branch: <branch>
status: draft            # draft | signed-off | superseded by <doc>
tags: [design, <component>]
references:              # lineage — what this design consumed (one hop per level, T14)
  - thoughts/shared/prd/<...>.md          # if a PRD fed this
  - thoughts/shared/research/<...>.md     # if research fed this
---

# Design: <Feature name>

## Problem & Context
What we're solving and why it matters, in the user's terms. 1–3 short paragraphs. Link the PRD/research
that motivated it (also in frontmatter `references`).

## Goals / Non-Goals
- **Goals:** the outcomes this design must achieve.
- **Non-Goals:** what is explicitly out of scope — the blast-radius boundary. Being explicit here prevents
  scope creep downstream.

## Assumption Ledger
Every material assumption, with its status. Kept live through the question rounds and frozen at sign-off.
`VERIFIED` = confirmed by code evidence or the user's answer · `UNVERIFIED` = still open · `ASSUMED` = user
said "enough", proceeding on the stated safe default.

| #  | Assumption                          | Status     | Basis                          |
|----|-------------------------------------|------------|--------------------------------|
| A1 | <assumption>                        | VERIFIED   | code: path/to/file.ext:LINE    |
| A2 | <assumption>                        | UNVERIFIED | needs your call                |
| A3 | <assumption>                        | ASSUMED    | "enough"; safe default: <what> |

## Design Overview
The architecture at the module level: the deep modules, the seams between them, and how data/control flows.
Prose, plus a diagram if it helps. For each unit, a reader should be able to answer: what does it do, how is
it used, what does it depend on? Name the **seams** — the places where behavior can be substituted or tested.
Use the vocabulary from `references/interface-design.md` (Module / Interface / Seam / Depth), not
"component/service/API/boundary".

## Interface Spec

### All new or changed interfaces & schemas
For each: the signature (types, methods, params), its **invariants / ordering constraints / error modes**, and
one short usage example. Design altitude only — the shape callers depend on, never the implementation body.

```
<signature>
  invariant: <...>; ordering: <...>; errors: <...>
  usage: <one-line caller example>
```

### Load-bearing interfaces — variants considered
Only for interfaces flagged load-bearing (multiple callers/adapters · hard to reverse · a real trade-off) and
confirmed with the user. For each, record the outcome of Design-It-Twice:

- **Chosen:** <variant> — <why it won: depth, seam placement, ease of correct use>.
- **Considered:** <variant B> — <one-line why not>; <variant C> — <one-line why not>.

## Key Decisions
Decisions worth remembering — the ones that are hard to reverse, surprising without context, or the result of a
real trade-off (the ADR bar). One line of rationale each, so future readers don't re-litigate or re-try dead ends.

## Open Questions
Must be **empty** at sign-off — or, if the user said "enough", each remaining item appears here *and* in the
ledger as `ASSUMED` with its safe default. No silent unknowns survive into `/plan`.
