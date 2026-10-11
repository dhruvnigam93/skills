# Deep-Modules Vocabulary

Use these terms precisely in every design doc and design conversation. Consistent language is the point — the banned substitutes blur distinctions that matter during design.

## Terms

**Module** — anything with an interface and an implementation. Deliberately scale-agnostic: a function, class, package, or tier-spanning slice.
_Avoid_: unit, component, service.

**Interface** — everything a caller must know to use the module correctly. This means signatures AND invariants, ordering constraints, error modes, required configuration, and performance characteristics. Not just the type-level surface.
_Avoid_: API, signature (too narrow — they refer only to types).

**Implementation** — what is inside the module; the body of code. Distinct from Adapter: a module can be a small adapter with a large implementation (a Postgres repo) or a large adapter with a small implementation (an in-memory fake). Use "adapter" when the seam is the topic; "implementation" otherwise.

**Depth** — leverage at the interface. A module is **deep** when large behavior sits behind a small interface; **shallow** when the interface is nearly as complex as the implementation. Depth is a property of the interface, not the implementation — a deep module can be internally composed of small, swappable parts that never surface to callers.

**Seam** _(Michael Feathers)_ — a place where you can alter behavior without editing in that place; the location at which a module's interface lives. Where to put the seam is its own design decision, distinct from what goes behind it.
_Avoid_: boundary (overloaded with DDD bounded context).

**Adapter** — a concrete thing that satisfies an interface at a seam. Describes role (what slot it fills), not substance (what is inside).

**Leverage** — what callers get from depth: more capability per unit of interface they learn. One implementation pays back across N call sites and M tests.

**Locality** — what maintainers get from depth: change, bugs, knowledge, and verification concentrate in one place rather than spreading across callers. Fix once, fixed everywhere.

## Design Principles

- **The deletion test.** Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep.
- **The interface is the test surface.** Callers and tests cross the same seam. If you need to test past the interface, the module is probably the wrong shape.
- **One adapter = a hypothetical seam. Two adapters = a real one.** Do not introduce a seam unless something actually varies across it. A single-adapter seam is just indirection.
- **Internal vs external seams.** A deep module can have internal seams (private to its implementation, used by its own tests) and an external seam (its interface). Do not expose internal seams through the external interface just because tests use them.

## Dependency Categories

When assessing an interface for your design, classify its dependencies. The category determines how the deepened module is tested across its seam.

### 1. In-process
Pure computation, in-memory state, no I/O. Always deepenable — merge modules and test through the new interface directly. No adapter needed.

### 2. Local-substitutable
Dependencies that have local test stand-ins (PGLite for Postgres, in-memory filesystem). Deepenable if the stand-in exists. The seam is internal; no port at the module's external interface.

### 3. Remote but owned (Ports & Adapters)
Your own services across a network boundary. Define a port (interface) at the seam. The deep module owns the logic; transport is injected as an adapter. Tests use an in-memory adapter. Production uses HTTP/gRPC/queue.

### 4. True external (Mock)
Third-party services (Stripe, Twilio) you do not control. The deepened module takes the external dependency as an injected port; tests provide a mock adapter.

## Relationships

```
Module ──has-one──> Interface
  |                    |
Depth <──measured-against──'
  |
  +──> Leverage (for callers)
  +──> Locality (for maintainers)

Seam <──lives-at── Interface
  |
Adapter ──satisfies──> Interface at Seam
```

## Deep vs Shallow — Visual

**Deep module** (aim for this):
```
+-----------------------+
|   Small Interface     |  <-- Few methods, simple params
+-----------------------+
|                       |
|  Large Implementation |  <-- Complex logic hidden
|                       |
+-----------------------+
```

**Shallow module** (avoid this):
```
+-------------------------------+
|       Large Interface         |  <-- Many methods, complex params
+-------------------------------+
|  Thin Implementation          |  <-- Just passes through
+-------------------------------+
```
