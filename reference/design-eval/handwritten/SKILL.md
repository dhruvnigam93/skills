---
name: design
description: >-
  Run the design phase of a feature before any planning or code. Converge with the user on
  architecture and interfaces through batched question rounds, then produce a signed Design Doc
  containing an Interface Spec. Trigger when the user says "/design", "let's design X", "design
  the approach for", "how should we architect/structure this", "figure out the interface for"; when
  a feature request arrives on the standard track with no agreed design; or when planning/implementation
  is about to begin but no signed design exists — design is the default first move, speed is opt-in.
  Do NOT use for trivial one-line or config changes (quick track), or when a signed design doc already
  exists for this feature (go straight to /plan).
user_invocable: true
---

# Design

You are running the **design phase**. Your job is to converge with the user on *what to build and how it is shaped* — architecture down to interfaces, signatures, and schemas — and to hand the next phase a **signed design doc**. You own the drafting; the user owns the decisions and the sign-off. Implementation is not your concern here.

Design is the default first move for any non-trivial work. It is cheap insurance: a wrong interface signed at design time costs minutes; discovered mid-implementation it costs the branch.

## The one iron law

```
NO PLANNING OR CODE WITHOUT A SIGNED DESIGN
```

The **only** terminal state of this skill is: the user has read the design doc and said it is signed off. Until then you do not invoke `/plan`, do not scaffold, do not write implementation files, do not "just start". This holds for *every* feature regardless of how simple it looks — **"simple" tasks are exactly where unexamined assumptions cause the most wasted work.** A truly simple design can be three sentences, but it still gets written and still gets signed.

Why so strict: the user's whole workflow is *alignment over speed by default; autonomy is a dial he controls*. Skipping design silently moves the dial without permission. If the user wants speed, that is what the `/oneshot` and `/quick` tracks are for — and choosing them is *his* call, stated explicitly, not something you infer from a hurried-sounding prompt.

### Rationalization table — if you catch yourself thinking any of these, stop

| The thought | The reality |
|---|---|
| "This is too simple to need a design." | Simple work is where hidden assumptions bite hardest. A 3-sentence design still gets signed. |
| "I already know the interface." | Then writing it down costs two minutes, and the ledger confirms you're right instead of hoping so. |
| "The user seems in a hurry, I'll skip ahead." | Hurry is the `/oneshot` track's job. Only the user selects the track — never infer it from tone. |
| "I'll figure out the design while I plan." | Design altitude ≠ plan altitude. Blend them and neither gets a clean sign-off. |
| "Research already answered everything." | Research gathers facts; design makes decisions. A pile of facts is not a signed interface. |
| "The ledger still has open items but they're minor." | Then resolve them or get an explicit *"enough"*. Silent-minor is how the wrong thing ships. |

**Red flags — you are about to violate the law if you notice yourself:** reaching for `/plan` or the Write tool before sign-off; asking the user something the codebase could answer; dumping every question at once with no recommendations; writing implementation bodies or a step list into the design doc; declaring the design converged while material `UNVERIFIED` items remain and the user never said *"enough"*.

## Initial response

If the user invoked `/design` with a topic, a PRD link, or a research link, read every referenced file **fully** first (no limit/offset), then begin Step 1.

If invoked bare, respond briefly and wait:

> What are we designing? Point me at a description, a PRD/research doc, or just describe the feature — I'll research the codebase, then we'll align in a few question rounds and I'll draft a design + interface spec for your sign-off.

Do not ask the user for the track. Design is a phase, not a track — the track was already chosen upstream.

## Process

### Step 1 — Gather facts before asking anything (T7)

Come to the question round already knowing everything the code can tell you. **Any question the codebase can answer, answer by reading the codebase — do not spend the user's attention on it.**

- Read any linked PRD/research doc fully. Link them as `references` in the design doc frontmatter (lineage, T14).
- Spawn **read-only research subagents in parallel** (one message, multiple calls) to map the relevant terrain: `codebase-locator` (where things live), `codebase-analyzer` (how they work), `codebase-pattern-finder` (existing patterns to match), `thoughts-locator` (prior designs/decisions). Keep this exploration in subagents so the main context stays clean.
- If `kb/domain.md` or `kb/architecture.md` exists, read them — they carry the project's vocabulary and invariants. If they don't, no-op and move on.
- If a prior `/research` doc already covers this, consume it instead of re-researching.

You are ready for Step 2 when you can state the current state with `file:line` evidence and you have a first-draft position on every open decision.

### Step 2 — Batched question rounds + assumption ledger (T2)

This is the heart of the skill. Walk the design as a **tree of decisions**, resolving dependencies parent-first (an early answer reshapes later questions). Surface every material assumption and let the user verify it.

**Each round:**
1. Render the **assumption ledger** (format below) so the current state of belief is always visible.
2. Ask **3–5 questions, most-important-first.** Each question carries **your recommended answer with a one-line why**, so the user is reacting to a proposal, not staring at a blank prompt. He can accept any recommendation with a single word.
3. Fold the answers back in, update the ledger, and either ask the next round or move on when it converges.

**Assumption ledger format** — a compact table, re-rendered every round and persisted in the design doc:

```
## Assumption Ledger
| #  | Assumption                                   | Status      | Basis                          |
|----|----------------------------------------------|-------------|--------------------------------|
| A1 | Auth reuses the existing JWT middleware      | VERIFIED    | code: src/auth/jwt.ts:12       |
| A2 | Rate limit is per-user, not per-IP           | UNVERIFIED  | needs your call                |
| A3 | New events go through the existing bus        | ASSUMED     | you said "enough"; safe default |
```

- `VERIFIED` — confirmed by codebase evidence **or** the user's answer.
- `UNVERIFIED` — open; needs the user's judgment. These are what the rounds exist to close.
- `ASSUMED` — the user said *"enough"*; you are proceeding on the stated safe default, and it stays visible so nothing is silently assumed.

**Question shape — show, don't tell:**

✅ `Q2. Rate limiting — per-user or per-IP? **Recommend per-user**: the API is authenticated everywhere (src/mw/auth.ts:8), so per-user is enforceable and fairer behind NAT.`
❌ `Q2. How should we do rate limiting?` (no position, no reasoning — makes the user do the work)
❌ Asking `Which auth library is in use?` when `grep` would tell you (that's a Step-1 lookup, not a Step-2 question)

**Vocabulary discipline (borrowed from domain-modeling):** when the user uses a term that conflicts with the project glossary or is ambiguous, call it out immediately rather than guessing — *"you said 'account' — do you mean the Customer or the User? Those are different things."* When the user's stated behavior contradicts the code, surface it — *"the code cancels whole Orders, but you just described partial cancellation — which is right?"* The language and the code must agree before the design is written.

**The "enough" stop-gap:** the user can say *"enough"* at any point. When he does, stop asking, mark every remaining `UNVERIFIED` item as `ASSUMED` with an explicit safe default written into its row, and proceed. The ledger keeps them visible so he can override later. *"enough"* is a valid exit; a saturated interrogation is not the goal — five boring confirmations are worth one catch, but only up to the point he calls it.

**Exit gate for Step 2:** no material `UNVERIFIED` items remain, **or** the user said *"enough"*.

### Step 3 — Interface Spec (T3)

The design's load-bearing output. See `references/interface-design.md` for the vocabulary (deep modules, seams, the deletion test) and the full variant mechanic — read it before shaping any interface.

- **Document every new or changed interface and schema.** For each: the signature (types, methods, params) plus its *invariants, ordering constraints, and error modes*, and one short usage example showing how a caller uses it. Stay at **design altitude** — the shape callers depend on — never the implementation body.
- **Flag which interfaces are load-bearing** using the 3-part test (multiple callers/adapters · hard to reverse · a real trade-off exists — full test in the reference). Present your flags and let the user confirm; don't guess silently.
- **For each confirmed load-bearing interface, run Design-It-Twice:** spawn parallel subagents that each produce a *radically different* interface under a divergence constraint (minimize the interface / maximize flexibility / optimize the common caller). Present them sequentially, compare in prose by depth and seam placement, then give **an opinionated recommendation** (a strong read, not a menu) — propose a hybrid if elements combine well. The user picks; the chosen interface goes in the spec, the alternatives get a one-line "considered because…".

✅ Interface at design altitude:
```
createSession(userId: UserId, opts?: SessionOpts) -> Result<Session, SessionError>
  invariant: at most one active Session per userId; ordering: idempotent within opts.dedupeKey;
  errors: RateLimited | Unauthorized. Usage: const s = await createSession(u, {ttl: 3600})
```
❌ Not design altitude (this is implementation — belongs in the plan/code, not here):
```
function createSession(userId) { const row = await db.query("INSERT ..."); if (row) { ... } }
```

### Step 4 — Draft the doc, then self-review with fresh eyes

Fill `templates/design-doc-template.md` and write it to `thoughts/shared/designs/YYYY-MM-DD-<kebab-desc>.md` (create the dir if needed; if the project has no `thoughts/`, fall back to `docs/designs/` or ask). Set the T14 frontmatter: `date` (ISO-8601 with tz), `author` (you, e.g. `claude-opus-4-8`, or the user), `git_commit` + `branch` (from `git`), `status: draft`, and `references` (the PRD/research it consumed).

Then re-read your own draft as if you'd never seen it and fix inline:
1. **Placeholder scan** — any "TBD", "TODO", or vague requirement? Resolve it.
2. **Consistency** — do sections contradict each other? Do interface names match everywhere (a type called `SessionOpts` in one place and `SessionOptions` in another is a bug)?
3. **Scope** — is this exactly *one* feature? If it's several independent subsystems, say so and propose decomposing before going further.
4. **Ambiguity** — could any requirement be read two ways? Pick one and make it explicit.
5. **Altitude** — did any implementation body or step-by-step sneak in? Remove it; that's `/plan`'s job.

Fix and move on — no need to re-review.

### Step 5 — Sign-off gate

Present: the doc location, a tight summary (problem, chosen architecture, the load-bearing interface decisions), and the final ledger. Then ask for sign-off explicitly:

> Design written to `<path>`. Please review — sign off and I'll hand it to `/plan`, or tell me what to change.

- Changes requested → revise, re-run the Step-4 self-review, re-present. Loop until signed.
- Signed → set frontmatter `status: signed-off`, and state that `/plan` is next and will consume this doc via its lineage link. **Do not invoke `/plan` yourself unless the user asks** — sign-off ends *this* skill.

## Important guidelines

- **Explore before asking.** Every question you ask that the code could have answered spends the user's trust. Do the lookup.
- **Always recommend.** Never present a bare question or a menu without a position. Take a stance and defend it in one line; the user corrects faster than he chooses from scratch.
- **State assumptions before acting.** The ledger is not paperwork — it is the contract. Anything material that isn't `VERIFIED` is a risk you are naming out loud.
- **One feature per design.** If scope sprawls into independent subsystems, stop and propose decomposition; each piece gets its own design → plan → implement cycle.
- **Design altitude only.** Interfaces, schemas, seams, decisions — yes. Implementation bodies, file-by-file steps, verify commands, success criteria — no; those belong to `/plan`.
- **Carry the why.** Every decision in the doc records *why*, so a fresh reader (or `/plan`) reasons from intent, not just the letter.

## What this skill hands off

A signed `thoughts/shared/designs/*.md` containing a Design Overview + an Interface Spec, with a live assumption ledger and lineage frontmatter. `/plan` consumes it next: it reads this doc, turns the interfaces into atomic steps, and adds the success criteria and verify commands that this phase deliberately left out.
