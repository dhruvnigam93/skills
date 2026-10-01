# Design Doc Template

Every /design invocation produces one file following this structure. All sections are required — if a section has nothing to say, state that explicitly (e.g., "No schema changes") rather than omitting it.

---

## Frontmatter

```yaml
---
date: YYYY-MM-DDTHH:MM:SS+TZ       # ISO-8601 with timezone
author: agent (model-id)            # e.g. "agent (claude-opus-4-6)" or "user"
git_commit: abc1234                 # current HEAD sha
branch: feature/order-cancellation  # current branch
status: draft                       # draft | signed-off | superseded
references:
  - path/to/prd-or-research-doc.md  # what prompted this design
---
```

## Sections

### # Design: [Feature Name]

One-line summary of what this design covers.

### ## Problem Framing

1-3 paragraphs. What the feature does, why it matters, what changes in the system. Grounded in the codebase research — reference concrete modules and file paths.

### ## Assumption Ledger

| # | Assumption | Status | Basis |
|---|-----------|--------|-------|
| 1 | Example verified assumption | VERIFIED | User confirmed, round 1 |
| 2 | Example assumed default | ASSUMED | Safe default: X. User said "enough". |
| 3 | Example unresolved item | UNVERIFIED | Awaiting user input |

Status values:
- **VERIFIED** — user explicitly confirmed
- **ASSUMED** — user said "enough"; safe default is stated and visible
- **UNVERIFIED** — still open (should not appear in a signed-off doc)

### ## Architecture

#### Current State
How the relevant modules and interfaces work today. Reference file paths. Use deep-modules vocabulary (module, interface, seam, adapter).

#### Proposed Changes
Which modules change, which are new, how the dependency graph shifts.

### ## Interface Spec

One subsection per new or changed interface:

#### [Interface/Module Name]

```
signature(param: Type, param: Type) -> ReturnType
```

**Invariants:** What must always be true.
**Error modes:** What can go wrong and how it surfaces to the caller.
**Ordering constraints:** What must happen before/after this call.
**Dependencies:** What this module takes as input or injection.

Repeat for every new or changed interface.

#### Load-Bearing Interfaces

List the interfaces confirmed as load-bearing and why each meets the bar.

If Design-It-Twice was run:

##### Variant Comparison
Present each variant, compare by depth/locality/seam placement.

##### Selected Variant
Which variant was chosen and why.

##### Considered Alternatives
One line per rejected variant — why it was explored and why it lost:
```
- Minimal interface (Agent 1): considered because it maximizes leverage, but rejected — the most common caller needs two calls instead of one.
- Flexible interface (Agent 2): considered because it supports future adapter types, but rejected — YAGNI; only two adapters are justified today.
```

### ## Schemas

One subsection per new or changed data schema:

#### [Schema/Type Name]

```
type definition, table DDL, or structured format
```

If no schemas change, state: "No schema changes required."

### ## Design Decisions

| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| Chose X over Y | Because Z | Y was considered but rejected because W |

### ## Out of Scope

What this design explicitly does NOT address. This helps the downstream /plan skill stay focused and prevents scope creep.
