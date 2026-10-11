# Interface design — vocabulary, the load-bearing test, and Design-It-Twice

Read this before shaping any interface in Step 3. It gives you the language to reason about interface *shape*
(not implementation), a falsifiable test for which interfaces deserve real exploration, and the parallel-subagent
mechanic for exploring them.

## 1. Vocabulary (deep modules)

Use these terms exactly. Consistent language is the point — don't substitute "component", "service", "API", or
"boundary".

- **Module** — anything with an interface and an implementation. Scale-agnostic: a function, class, package, or
  tier-spanning slice.
- **Interface** — *everything a caller must know to use the module correctly*: the type signature, but also
  invariants, ordering constraints, error modes, required config, and performance characteristics. Broader than
  "signature" (which is only the type-level surface).
- **Implementation** — what's inside the module. Never appears in the design doc.
- **Depth** — leverage at the interface: how much behavior a caller (or test) exercises per unit of interface it
  has to learn. **Deep** = a lot of behavior behind a small interface (good). **Shallow** = the interface is nearly
  as complex as the implementation (a pass-through; usually a mistake).
- **Seam** *(Feathers)* — a place where you can alter behavior without editing in that place. *Where* the seam sits
  is its own design decision, separate from *what* goes behind it.
- **Adapter** — a concrete thing that satisfies an interface at a seam (a Postgres repo; an in-memory fake).
- **Leverage** (what callers get) / **Locality** (what maintainers get): depth pays back as more capability per unit
  learned, and as change/bugs/knowledge concentrating in one place instead of spreading across callers.

**Two heuristics that keep interfaces honest:**
- **The deletion test.** Imagine deleting the module. If complexity vanishes, it was a pass-through (delete it for
  real). If complexity reappears across N callers, it was earning its keep.
- **The interface is the test surface.** Callers and tests cross the same seam. If you find yourself wanting to test
  *past* the interface, the module is probably the wrong shape.

## 2. Which interfaces are "load-bearing"?

Document *every* new/changed interface and schema. But only spend Design-It-Twice on the load-bearing ones. An
interface is load-bearing when **all three** hold (same bar as an ADR):

1. **Multiple callers or adapters** — two adapters mean a real seam; one means a hypothetical one. If nothing
   varies across it, it isn't load-bearing yet.
2. **Hard to reverse** — a persisted schema, a public/cross-module contract, anything whose change ripples.
3. **A real trade-off exists** — there are genuinely different shapes and picking one closes off others.

If any of the three is missing, propose a single interface and move on — variant exploration would be ceremony.
Present your load-bearing flags to the user and let him confirm before you spin up subagents.

## 3. Design-It-Twice — parallel variant exploration

*Your first idea is unlikely to be the best (Ousterhout). For each confirmed load-bearing interface, generate
radically different shapes in parallel, then choose deliberately.*

### Spawn

Spawn **3+ subagents in parallel** (Agent tool, one message). Give each a **separate technical brief** — the file
paths, the coupling details, what sits behind the seam — and **a different divergence constraint** so they can't
converge:

- **Agent 1 — minimize the interface:** aim for 1–3 entry points, maximum leverage per entry point.
- **Agent 2 — maximize flexibility:** support many use cases and future extension.
- **Agent 3 — optimize the common caller:** make the default case trivial, even at the cost of edge-case ergonomics.
- **Agent 4 (only if cross-seam dependencies matter) — ports & adapters:** design around swappable adapters.

Each subagent returns:
1. The interface — types, methods, params, plus **invariants, ordering, error modes**.
2. A usage example showing how a caller uses it.
3. What the implementation hides behind the seam.
4. Dependency/adapter strategy.
5. Trade-offs — where leverage is high, where it's thin.

### Present and choose

- Present the designs **sequentially** so the user can absorb each before the next — don't dump them side by side.
- Compare them **in prose** (not a table) by **depth** (leverage at the interface), **locality** (where change
  concentrates), and **seam placement**. Also weigh ease of *correct* use vs ease of *mis*use.
- Give **an opinionated recommendation** — which is strongest and why. If elements from different designs combine
  well, propose a hybrid. The user wants a strong read, not a menu.
- Do **not** evaluate on implementation effort — this is about interface shape. The chosen interface goes into the
  Interface Spec; each rejected one gets a one-line "considered because…" in the doc.

### Anti-patterns

- Letting subagents produce similar designs — enforce radical difference via the constraints.
- Skipping the comparison — the value is in the contrast, not the options.
- Slipping into implementation — you are choosing a *shape*, not writing the body.
