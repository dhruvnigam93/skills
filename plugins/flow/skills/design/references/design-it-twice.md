# Design-It-Twice: Variant Exploration Protocol

Run only for interfaces the user confirmed as load-bearing (SKILL.md Phase 4). Based on Ousterhout's "Design It Twice" — your first idea is unlikely to be the best.

## Step 1: Frame the Problem Space

Before spawning subagents, write a brief for BOTH the user and the subagents:

- The constraints any interface must satisfy
- The dependencies and their categories (in-process / local-substitutable / remote-owned / true-external — see [deep-modules.md](deep-modules.md))
- A rough illustrative sketch to ground the constraints — not a proposal, just something concrete enough to think about

Show this to the user, then spawn subagents immediately. The user reads while the agents work in parallel.

## Step 2: Spawn Subagents

Spawn 3 cheap subagents in parallel using the Agent tool. Each receives the same brief but a different constraint. Add Agent 4 when the module has cross-seam dependencies that genuinely warrant a ports-and-adapters exploration.

- **Agent 1 — Minimize the interface.** Aim for 1-3 entry points max. Maximize leverage per entry point. Hide as much as possible behind the seam.
- **Agent 2 — Maximize flexibility/extension.** Support many use cases and easy adapter addition. Optimize for the unexpected caller.
- **Agent 3 — Optimize the common caller.** Make the default case trivial — one line if possible. Complexity goes into the rare paths.
- **Agent 4 (optional) — Ports and adapters.** Design around cross-seam dependencies. Define ports explicitly, show how production and test adapters slot in.

### Subagent Prompt Template

Fill in the bracketed sections from the brief and Phase 1 research.

```
Design a radically different interface for [module name].

Context:
[Problem-space brief — constraints, current coupling, what callers need]

File paths for reference (read-only):
[Relevant source files from the self-research phase]

Dependency categories:
[Each dependency and its category, from the brief]

Your constraint: [This agent's constraint from the list above, verbatim]

Vocabulary — use these terms precisely, never substitute:
[Paste the Deep-Modules Vocabulary table from SKILL.md]

Domain vocabulary:
[Relevant terms from kb/domain.md or CONTEXT.md, if they exist]

Return exactly these five sections:
1. Interface (types/methods/params + invariants, ordering, error modes)
2. Usage example (most common caller, runnable pseudocode)
3. What the implementation hides behind the seam
4. Dependency/adapter strategy
5. Trade-offs (where leverage is high, where it is thin)
```

## Step 3: Present and Compare

1. **Present each variant sequentially** so the user can absorb one at a time. Use the subagent's own structure — do not reformat or summarize away detail.

2. **Compare in prose** on depth, locality, and seam placement (what varies across the seam, how many adapters are justified).

3. **Give an opinionated recommendation.** A strong read, not a menu. State which design you think is strongest and why. If elements from different designs combine well, propose a hybrid with specifics.

4. **The user picks.** Record the result in the design doc's Load-Bearing Interfaces slot, rejected variants as "considered because..." lines.
