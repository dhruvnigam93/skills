# Deep-Modules Reference

Extends the vocabulary table and three tests in SKILL.md — this file adds only what they don't cover.

## Term Nuances

- **Module** — deliberately scale-agnostic: a function, class, package, or tier-spanning slice.
- **Interface** — also covers required configuration and performance characteristics, not just the type-level surface.
- **Implementation vs Adapter** — a module can be a small adapter with a large implementation (a Postgres repo) or a large adapter with a small implementation (an in-memory fake). Say "adapter" when the seam is the topic; "implementation" otherwise.
- **Depth** — a property of the interface, not the implementation. A deep module can be internally composed of small, swappable parts that never surface to callers.
- **Seam** — where to put the seam is its own design decision, distinct from what goes behind it.
- **Adapter** — describes role (what slot it fills), not substance (what is inside).
- **Leverage** — one implementation pays back across N call sites and M tests.
- **Locality** — change, bugs, knowledge, and verification concentrate in one place. Fix once, fixed everywhere.

## Internal vs External Seams

A deep module can have internal seams (private to its implementation, used by its own tests) and an external seam (its interface). Do not expose internal seams through the external interface just because tests use them.

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
