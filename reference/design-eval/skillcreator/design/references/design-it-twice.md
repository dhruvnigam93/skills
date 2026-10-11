# Design-It-Twice: Variant Exploration Protocol

When an interface is flagged as load-bearing and the user confirms, spawn parallel subagents to generate radically different designs. Based on Ousterhout's "Design It Twice" — your first idea is unlikely to be the best.

## When to Run

Only for **load-bearing interfaces** — those that meet ALL of:
- Multiple callers or adapters will use it
- Hard to reverse once implemented
- A genuine trade-off exists between competing designs

This is the same bar as an ADR. If the interface does not meet all three, document it once and move on. No variant analysis needed.

## Step 1: Frame the Problem Space

Before spawning subagents, write a brief for BOTH the user and the subagents:

- The constraints any interface must satisfy
- The dependencies and their categories (in-process / local-substitutable / remote-owned / true-external — see [deep-modules.md](deep-modules.md))
- A rough illustrative sketch to ground the constraints — not a proposal, just something concrete enough to think about

Show this to the user, then spawn subagents immediately. The user reads while the agents work in parallel.

## Step 2: Spawn Subagents

Spawn 3 subagents in parallel using the Agent tool. Each receives the same problem-space brief but a different design constraint. Add Agent 4 when the module has cross-seam dependencies that genuinely warrant a ports-and-adapters exploration.

### Constraint Assignments

- **Agent 1 — Minimize the interface.** Aim for 1-3 entry points max. Maximize leverage per entry point. Hide as much as possible behind the seam.
- **Agent 2 — Maximize flexibility/extension.** Support many use cases and easy adapter addition. Optimize for the unexpected caller.
- **Agent 3 — Optimize the common caller.** Make the default case trivial — one line if possible. Complexity goes into the rare paths.
- **Agent 4 (optional) — Ports and adapters.** Design around cross-seam dependencies. Define ports explicitly, show how production and test adapters slot in.

### Required Output Per Subagent

Each subagent returns exactly:

1. **Interface** — types, methods, params, plus invariants, ordering constraints, error modes
2. **Usage example** — how the most common caller uses this interface (runnable pseudocode)
3. **What it hides** — what implementation sits behind the seam, invisible to callers
4. **Dependency/adapter strategy** — how dependencies are injected, what adapters exist or are needed
5. **Trade-offs** — where leverage is high, where it is thin, what this design gives up

### Subagent Prompt Template

Use this as the base prompt for each subagent. Customize the constraint line and fill in the bracketed sections with specifics from the problem-space brief.

```
Design a radically different interface for [module name].

Context:
[Problem-space brief — constraints, current coupling, what callers need]

File paths for reference (read-only):
[List of relevant source files from the self-research phase]

Dependency categories:
[Classify each dependency as in-process / local-substitutable / remote-owned / true-external]

Your constraint: [INSERT ONE: "Minimize the interface — 1-3 entry points max, maximize leverage" | "Maximize flexibility — support many use cases, easy extension" | "Optimize the common caller — default case trivial, complexity in rare paths" | "Ports and adapters — design around cross-seam dependencies"]

Vocabulary — use these terms precisely, never substitute:
- Module: anything with an interface and an implementation
- Interface: everything a caller must know — signatures, invariants, ordering, error modes
- Seam: where you can alter behavior without editing there (Feathers)
- Adapter: a concrete thing that satisfies an interface at a seam
- Leverage: what callers get — more capability per unit of interface learned
- Locality: what maintainers get — change concentrates in one place

Domain vocabulary:
[Insert relevant terms from kb/domain.md or CONTEXT.md if they exist]

Return exactly these five sections:
1. Interface (types/methods/params + invariants, ordering, error modes)
2. Usage example (most common caller, runnable pseudocode)
3. What the implementation hides behind the seam
4. Dependency/adapter strategy
5. Trade-offs (where leverage is high, where it is thin)
```

## Step 3: Present and Compare

1. **Present each variant sequentially** so the user can absorb one at a time. Use the subagent's own structure — do not reformat or summarize away detail.

2. **Compare in prose** along three axes:
   - **Depth** — leverage at the interface: how much behavior per unit of interface learned
   - **Locality** — where change concentrates when the implementation evolves
   - **Seam placement** — where the seam sits, what varies across it, how many adapters are justified

3. **Give an opinionated recommendation.** A strong read, not a menu. State which design you think is strongest and why. If elements from different designs combine well, propose a hybrid with specifics.

4. **The user picks.** Rejected alternatives get a one-line "considered because..." entry in the design doc's Interface Spec section.

Example of a considered-alternative entry:
```
- Minimal interface (Agent 1): considered because it maximizes leverage, but rejected — the most common caller needs two calls instead of one.
- Flexible interface (Agent 2): considered because it supports future adapter types, but rejected — YAGNI; only two adapters are justified today.
```
