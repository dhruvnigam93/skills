---
date: 2026-07-02
author: claude-fable-5 (Explore subagent)
status: active
references:
  - ../inspiration/mattpocock-skills/
purpose: Primary research — Matt Pocock's skills (grilling, seams, deep modules); Dhruv strongly agrees with Pocock's "software fundamentals" talk
---

# mattpocock/skills — Study Report

## 1. The main flow (from ask-matt router skill)

```
grill-with-docs → [optional: prototype via handoff] → to-prd → to-issues → implement → code-review
```
Context hygiene: steps 1–4 in ONE context window; each /implement in a fresh session per issue; handoff at ~120k tokens ("smart zone" limit).

## 2. Workflow-critical skills (verbatim excerpts)

### grilling (the core primitive — full text)
```
Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.

If a question can be answered by exploring the codebase, explore the codebase instead.
```
(NB: Dhruv chose BATCHED rounds instead of one-at-a-time, but kept "provide your recommended answer" and "explore codebase instead of asking".)

### grill-me = `Run a /grilling session.` | grill-with-docs = `Run a /grilling session, using the /domain-modeling skill.`

### domain-modeling
- "When the user uses a term that conflicts with the existing language in CONTEXT.md, call it out immediately. 'Your glossary defines cancellation as X, but you seem to mean Y — which is it?'"
- "You're saying account — do you mean the Customer or the User? Those are different things."
- Cross-reference with code: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"
- ADR gate (all three must hold): hard to reverse / surprising without context / result of a real trade-off.

### codebase-design (shared vocabulary)
- **Module** — anything with an interface and an implementation (scale-agnostic). *Avoid*: unit, component, service.
- **Depth** — leverage at the interface: behaviour a caller/test can exercise per unit of interface learned.
- **Seam** (Feathers) — where you can alter behaviour without editing in that place.
- **Deletion test**: "Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep."
- "The interface is the test surface." / "One adapter means a hypothetical seam. Two adapters means a real one."

### tdd
- "Test only at pre-agreed seams. Before writing any test, write down the seams under test and confirm them with the user."
- Anti-patterns: implementation-coupled / tautological / horizontal slicing (write vertical slices).
- "Red before green." / "One slice at a time." / "Refactoring is not part of the loop. It belongs to the review stage."

### to-prd
- Step 2: "Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible... The fewer seams across the codebase, the better — the ideal number is one. Check with the user that these seams match their expectations."
- "Do NOT interview the user — just synthesize what you already know."

### to-issues (vertical slices)
- Each slice: narrow but COMPLETE path through every layer; demoable on its own; prefactoring first.

### implement (full text — remarkably thin)
```
Implement the work described by the user in the PRD or issues.
Use /tdd where possible, at pre-agreed seams.
Run typechecking regularly, single test files regularly, and the full test suite once at the end.
Once done, use /code-review to review the work.
Commit your work to the current branch.
```

### code-review (two-axis, parallel subagents)
- **Standards** axis (repo standards + 12 Fowler smells baseline) and **Spec** axis (diff vs originating issue/PRD) — run as parallel subagents "so they don't pollute each other's context"; reports side by side, never merged.

### diagnosing-bugs
- Phase 1 done when the loop is **tight** and **red-capable**: ONE command, already run once, that is: Red-capable / Deterministic / Fast (seconds) / Agent-runnable.
- "If you catch yourself reading code to build a theory before this command exists, stop."

### DESIGN-IT-TWICE (in codebase-design references)
- Spawn 3+ parallel subagents, each a *radically different* interface: (1) minimize interface 1-3 entry points; (2) maximize flexibility; (3) optimize for most common caller; (4) ports & adapters. (Source of Dhruv's Interface Spec variants.)

## 3. Prompt techniques worth stealing

1. **Leading words** — a compact pretrained concept recruits priors with minimal tokens: *tight*, *red*, *fog of war*, *tracer bullets*.
2. **One recommended answer per question** — the AI takes a position, never passive interviewing.
3. **Falsifiable heuristics** — deletion test; "stop if you're theorizing before the command exists".
4. **Anti-pattern enumeration with named smells** next to good patterns.
5. **Completion criteria as checkboxes**, not prose.
6. **Parallel subagents with divergence constraints** (each gets a different design constraint to prevent convergence).
7. **Strategic "Do NOT" gates**: "Do NOT propose interfaces yet." / "Do not proceed until you have reproduced and minimised."
8. **Progressive disclosure via sibling files** (DEEPENING.md, DESIGN-IT-TWICE.md loaded only when the branch fires).
9. **"Avoid:" synonym lists** to enforce vocabulary (Module not component/service).
10. **`disable-model-invocation: true`** for user-only orchestration skills (saves context, prevents auto-firing).

## 4. Gaps vs Dhruv's tenets

1. Code review only at END of /implement, not per step.
2. No deployment feedback — all local (types, tests).
3. Human owns seams/interfaces but NOT per-method signatures below them (Dhruv goes further).
4. No general research-subagent pattern.
5. Issues are feature-level, not step-level with files/verify per step.
6. No AI-uncertainty flagging protocol (grilling challenges the USER's terms, not its own assumptions).
7. implement is 5 lines — no failure/scope-creep/checkpoint handling.
