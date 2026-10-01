# Dhruv's AI Coding Workflow

**Version**: 1.7 — 2026-10-01
**Built from**: stated tenets + analysis of ~1,300 prompts of real usage + study of humanlayer, obra/superpowers, mattpocock/skills + KB research (web + Gemini) + Ralph-technique research from the source (Geoffrey Huntley, ghuntley.com).
**Structure**: Tenets → Workflow → Skills → Skill-authoring tenets. Everything downstream must trace back to a tenet.

---

## Part 1 — Tenets

### T1. Alignment over speed by default; autonomy is a dial I control
AI is trigger-happy. It earns autonomy through explicit checkpoints. I select the operating track for every task — the AI never self-selects. Speed is available on demand (one-shot track), never by default.

### T2. Every material assumption is surfaced and verified by me
The AI asks questions in **batched rounds of 3–5**, most important first, each with a recommended answer I can accept with one word. An **assumption ledger** tracks every assumption as `VERIFIED` / `UNVERIFIED`. I can say **"enough"** at any point — the AI then proceeds, resolving remaining items with safe assumptions, but they stay visible in the ledger. Five boring confirmations are worth one catch.

### T3. I own design at both altitudes; AI owns implementation
Architecture down to components, classes, method signatures, and data schemas is mine. The mechanism: **AI drafts, I sign off** — the design phase produces a mandatory **Interface Spec** (every new/changed class, signature, schema; 2–3 deliberately different variants for load-bearing interfaces). AI has full autonomy only *inside* approved interfaces. ("Design the interface, delegate the implementation" — Ousterhout via Pocock.)

### T4. One plan = one feature; steps are atomic and self-verifying
Each plan delivers exactly one feature's functionality. Each step declares: **files touched, scope, and its verification method** — before any code. Success criteria (including deploy/API/UI checks) are agreed at plan time, not discovered at the end.

### T5. Review is independent or it's worthless
After every step passes its checks, a **fresh-context subagent** reviews the diff against the step's intent. It sees only: the step spec, the diff, and verification evidence — never the implementer's narrative or session history. A context-saturated agent reviewing its own work has confirmation bias; that is not review.

### T6. Commit at green, automatically
When a step passes its success criteria **and** independent review, the AI commits on its own and continues. No per-commit ask. The branch is always a sequence of clean, atomic, reviewable increments.

### T7. Process-irrelevant work goes to subagents
Research, codebase exploration, log analysis, external-library study — anywhere only the output matters — runs in subagents. The main context stays clean for the work I care about.

### T8. Verification is a hierarchy, never optional
TDD where possible → some automated check always required (pytest, API hit, Playwright script, deploy + E2E + log grep) → if no automated check is possible, the step is **explicitly flagged for my manual verification** and cannot self-certify. No step begins until its check exists and can go red.

### T9. Trust raw data, not reports
Verification means reading logs, timestamps, transcripts, and diffs — not believing an agent's summary of them. Prefer N=5 runs over N=1 for anything stochastic.

### T10. Knowledge lives in the repo, indexed, and never rots
A repo-resident KB is initialized at project start and **kept fresh at every commit**. Small always-loaded index; deep detail behind progressive disclosure. Stale docs are worse than no docs. Document only what code cannot say: intent, invariants, decisions, domain language, and **negative knowledge** (what was tried and rejected, and why).

### T11. The system improves itself
The AI is *eager* to convert recurring procedures (CLI dances, log-fetch patterns, deploy sequences) into skills — it flags candidates the moment it notices repetition. A retro skill critiques past sessions against these tenets and outputs **patches** (to skills, CLAUDE.md, memory), never prose advice.

### T12. Every mistake becomes a rule
When the AI errs, the correction gets encoded — CLAUDE.md, memory, a skill, or a hook — so the same mistake cannot recur. (Already my habit: "is there any learning — do we need to update claude md?")

### T13. Never work in the dumb zone
Past ~60% context utilization, agent quality degrades — the evidence: the U-shaped attention curve ("Lost in the Middle", Liu et al., TACL 2024), degradation with input length *even under perfect retrieval* (arXiv 2025), and practitioner thresholds converging on 60–75% (Sourcegraph's Amp compacts at 64–75%; a 50-session Claude Code study saw forgotten instructions from ~60%; >73% shows brute-force looping). Protocol: **~60% = warning** — finish the current step, sync state; **75% = hard stop** — write a handoff (create-handoff) and resume fresh (resume-handoff). Never recursive summarization — hard resets with a handoff doc containing: file manifest, done/in-progress breakdown, critical invariants, decision rationale, resumption commands. The plan file is the durable ledger, so nothing is lost. Pushing on with a saturated context is a tenet violation, not diligence.

### T14. Every document carries provenance and lineage
All docs (thoughts/ and kb/) get frontmatter: date, author (me / agent+model), git commit, branch — the humanlayer convention. And every doc links its upstream sources: plan → the research and design it consumed, design → the PRD, PR → the plan. Any artifact's full ancestry is traceable in one hop per level. Thoughts are **transactional** (what happened, when); the KB is **current state** (what is true now) — lineage is what connects the two.

---

## Part 2 — Workflow

### 2.1 Tracks (I pick, always)

| Track | When | Ceremony |
|-------|------|----------|
| **quick** | Small, low-blast-radius changes (UI copy, config tweak, one-liner) | State intent + verify method in one line → do → verify → commit. No plan. |
| **standard** | Normal feature work | Full pipeline below, auto-commits per step, pauses at phase boundaries + manual-verify steps. |
| **oneshot** | Speed matters; I trust the design | Align once on design + plan, then AI runs everything → reviews → commits → PR. Review failures: auto-fix loop (max 3), then stop and report. |
| **ralph** | Greenfield bootstrap; throwaway / eventual-consistency work I'll supervise at loop boundaries, not per step | Write + sign the spec, then a bash loop restarts a **fresh headless agent every iteration** — each does the single most important next thing — until done, capped, or I stop it. Max position of the autonomy dial. Mechanics in §2.6. |

At intake I say the track. If I don't, the AI asks in one line — it never assumes.

### 2.2 Standard-track pipeline

```
[prd]* → [research]* → design → plan → implement (step loop) → final review → kb-sync → PR
                         │                    │
                 assumption ledger      per step: check exists (red-capable)
                 interface spec          → implement → checks green
                 my sign-off             → independent step-review (fresh subagent)
                                         → auto-commit → next step → update plan form
```
\* Both entry stages are optional. **PRD first when the product outcome needs defining** — what we want to achieve, non-technical, iterated as rigorously as design (batched rounds, same T2 mechanics). When the feature is clear and the work is technical, enter directly at research or design. Research is needed only when the codebase/domain is unfamiliar; it runs entirely in subagents (T7). Every stage links its upstream artifact (T14).

**Design phase** (T2, T3): research subagents gather facts → batched question rounds (3–5, most-important-first, each with a recommendation) → assumption ledger converges → AI drafts Interface Spec (variants for load-bearing interfaces) → **I sign off**. Exit gate: ledger has no major UNVERIFIED items, or I said "enough".

**Plan phase** (T4, T8, T14): consumes design doc + interface spec (linked in frontmatter). One feature. Atomic steps, each with:
- `Files:` exact paths
- `Scope:` what changes and what must NOT change (blast-radius line)
- `Verify:` the literal command(s) + expected output — pytest / API call / Playwright / deploy + E2E + log grep — or `MANUAL: <what I check>`
- `[ ]` checkbox + empty `Impl note:` and `Review note:` fields — filled during execution
- Plan header: success criteria for the whole feature, agreed before step 1.

**The plan is a living form, not a frozen script:**
- The implementer *fills it in* as it goes: checks boxes, writes a one-line `Impl note:` per step (what was actually done, anything surprising), and the step-reviewer's verdict lands in `Review note:`. The plan file doubles as the durable progress ledger (T13) — a fresh session can resume from it alone.
- **Decision points and forks are first-class**: a step may declare `Decision: observe <X> → if A, continue; if B, take fork B1–B3`. When a step reveals something un-planned-for, the implementer first classifies the failure: **implementation-level** (fix the code, plan stands) or **plan-level** (the plan's reasoning is invalidated — "plan–code co-evolution", ACL 2026). Plan-level findings get recorded in the plan and become a proposed fork — minor forks (no interface change, within scope) proceed after logging; anything touching the signed Interface Spec or feature scope comes back to me (T3). Frozen plans that keep executing after the environment contradicts them are a known agent failure mode ("long-task drift").

**Implement phase** (T5, T6, T8): per step — verify the check exists and can go red → implement (TDD where the code is unit-testable) → run checks → spawn **step-reviewer** subagent → on APPROVE: commit, continue (non-blocking notes ride along in the plan); on BLOCK: fix and re-review (max 3 cycles, then pause for me); on ESCALATE: pause for me. Pauses: phase boundaries, `MANUAL:` steps, and any interface change not in the signed spec (hard stop — that's a design change, back to me).

**Close** (T10): completion challenge — before claiming done, the implementer re-verifies every feature-level success criterion against the plan's invariants (counters "progress-as-completion" bias: agents mistake activity for achievement) → final whole-feature review (fresh subagent, full branch diff vs feature intent) → kb-sync → PR (linked to plan, T14).

**Dumb-zone rule (T13), all phases**: at ~60% context utilization the AI stops at the next clean boundary, writes a handoff (linking plan + position in it), and work resumes fresh. Never mid-step.

### 2.3 Knowledge base (T10)

Synthesis of the KB research (Anthropic guidance, Cline Memory Bank, agents.md, llms.txt, HumanLayer thoughts/, ADRs):

```
CLAUDE.md                  # ALWAYS LOADED. <200 lines. Rules + gotchas + pointer to kb/_index.md
kb/
  _index.md                # Routing map, ~600 tokens. One line per doc: "read X if touching Y"
  architecture.md          # System boundaries, invariants ("A must never call B synchronously")
  domain.md                # Ubiquitous language: glossary of terms as THIS project uses them
  graveyard.md             # Negative knowledge: approaches tried & rejected, with why
  adrs/NNN-*.md            # Decisions: context, decision, status (accepted/superseded)
  external/<system>.md     # Learned behavior of external systems (CLIs, APIs, closed libs) — see 2.5
thoughts/                  # TRANSACTIONAL working memory: prd, research, plans, handoffs
```

**thoughts/ vs kb/** (T10, T14): thoughts/ is the transaction log — PRDs, research, plans, handoffs, timestamped, never edited after the fact. kb/ is current state — always true *now*, updated by kb-sync. A fact graduates from thoughts/ to kb/ when it stops being about *this task* and starts being about *the system*.

**Version control — both git-tracked, never gitignored** (T10, T14): kb/ and thoughts/ live *in* the repo and flow through branches, **merging to main like code**. This is what T10's "repo-resident" and T14's provenance require — gitignoring them loses lineage and breaks worktrees (a fresh worktree or clone carries none of the untracked files). A feature branch's PR is then one coherent unit: design → plan → code → the kb/ updates it made true. kb/ = current truth converging on main; thoughts/ = append-only history with uniquely-dated filenames, so merges are conflict-free in practice. **Always branch from main** so every feature starts from current knowledge; an in-flight doc on another branch is *proposed* truth, visible everywhere once merged. (Alternative considered: humanlayer's separate synced-thoughts repo — valid, but two repos and split provenance; we keep a single history.)

**Doc conventions (T14)** — every doc in thoughts/ and kb/ carries frontmatter:

```yaml
date: 2026-07-03T14:30:00+05:30
author: dhruv | claude-fable-5 | <human or agent+model — provenance matters>
git_commit: <hash at creation>
last_verified_commit: <hash>      # kb docs only: when this doc was last known accurate
status: draft | active | superseded by <doc>   # ADR-style lifecycle, agents skip superseded
branch: feat/...
references:                       # lineage (depends_on graph), one hop per level
  - thoughts/shared/research/2026-07-02-....md
  - thoughts/shared/designs/2026-07-03-....md
```

Key principles from research:
- **Working memory ≠ semantic memory**: task state (thoughts/) stays separate from structural knowledge (kb/) — mixing them degrades agent attention.
- **Unindexed lore doesn't exist**: everything must be reachable from `_index.md` in one hop.
- **Freshness = commit-workflow step, not blind hook**: kb-sync runs inside the commit skill — reads the diff + `_index.md`, updates only conceptually-affected docs, no-ops on mechanical diffs. Avoids both rot (never skipped) and churn (no paraphrasing every diff). Optional later: CI drift-check with a cheap model ("does this diff make any KB doc factually wrong?").
- **Anti-patterns**: unbounded always-loaded files; duplicated truth (state each fact once); docs that paraphrase code; missing negative knowledge (agents re-try dead ends unless told).

### 2.4 External-system discovery (T7, T8, T10)

Research isn't only codebase research. When the work depends on an external system — a CLI, a third-party API, a library interface:

- **Public source available** → temp-clone the repo (shallow) and run normal codebase research on it via subagents.
- **No source (closed API, service, CLI)** → write **learning tests**: small scripted probes (a battery of commands / API calls with recorded inputs → outputs) that empirically map the system's behavior. Run them, keep them runnable (they double as regression detectors when the external system changes), and distill findings into `kb/external/<system>.md` — including surprises and failure modes (graveyard-style negative knowledge).

Learned external behavior is permanent knowledge → it lives in kb/, not thoughts/.

The evidence is emphatic: in the Mini-SWE-Agent ablation (2025), dynamic exploration via probe scripts gained **+60 points** of task success vs **+4–5** for static code analysis. Simon Willison calls this the "scout" pattern — a throwaway proof-of-concept whose only job is to uncover the sticky bits; only the learned answer survives. Probes are exploration, not integration: they run in a scratch dir against the real system, never inside the feature branch.

### 2.5 Self-improvement loop (T11, T12)

- **In-session**: the moment a multi-step procedure repeats, AI flags "skill-ify this?" — one line, costless to dismiss.
- **On demand / after painful sessions**: `/retro` analyzes transcripts against the tenets — assumptions not surfaced, scope creep, wrong tools, missed skill opportunities — and proposes concrete patches.
- Every correction I make lands somewhere durable (CLAUDE.md / memory / skill / hook).

### 2.6 The Ralph loop (track 4 — max-autonomy bootstrap)

Ralph (Geoffrey Huntley's technique, named after Ralph Wiggum) is a bash `while` loop that restarts a **fresh headless agent every iteration** — each one reads the same spec + plan from disk and does the single most important next thing. It exists because a single agent, even on a perfectly specified task, degrades as its context fills and eventually stalls or loops; a fresh agent per iteration keeps every loop in the high-quality zone. This is not a workaround around a tenet — it is the purest expression of **T13**: the filesystem (spec, plan, code, git history) is the durable ledger, and no iteration ever runs in the dumb zone.

**Ralph is the MAX position of T1's autonomy dial, not a suspension of the tenets:**
- **T3 (I own design)** → the **spec is the design gate**. Ralph does not start until I've written and signed `specs/*` (one concern per file). The spec *is* Ralph's interface spec; a wrong spec is the most expensive failure, so it is iterated with the same rigor as §2.2 design.
- **T5 / T8 (independent review / verification)** → the **build + tests + type-checker are the reviewer**. Every loop must end green; back-pressure tools (strong types, static analysis, tests) are the fresh-context review no self-narrating agent can fake. I checkpoint at **loop boundaries** (every N iterations / on the circuit-breaker), not per step.
- **T1 / T2 (alignment, I control autonomy)** → I consciously set the dial to max for this class of work, cap the loop, and can stop it at any iteration. Alignment is front-loaded into the spec.
- **T9 (raw data)** → I judge Ralph by the git log, the passing tests, and the diff — never by a summary.

**When**: greenfield bootstrap — Huntley's expectation is ~90% done, then a human finishes. **Not** on an existing codebase by default: *"there's no way in heck I'd use Ralph in an existing codebase."* On an existing repo, Ralph runs only inside an **isolated new package/subtree with explicit opt-in**, and that warning is surfaced loudly.

**The harness** (produced by `/ralph`, Part 3 row 15):
- `specs/*` — the signed specification, one concern per file.
- `fix_plan.md` — priority-ordered checklist of what's not yet built; Ralph works the top item(s) and updates it every loop. Regenerable from scratch in planning mode.
- `AGENT.md` — how to build/test/run; Ralph self-updates it with build learnings (never status reports).
- `PROMPT.md` — the loop's instruction, tuned over time (Huntley's "signs on the playground"). Core directives: study `specs/*` + `fix_plan.md`; **do the single most important next item** (relax to N as the project matures; narrow back to 1 the moment quality drops); **search before implementing** — don't assume it's missing (the ripgrep false-negative → duplicate implementation is Ralph's Achilles heel); **no placeholder implementations**; run the changed unit's tests; on green, update `fix_plan.md`, `git add -A` + commit + push, tag semver on zero errors; delegate expensive search/test work to subagents to keep the main context lean (the orchestrator is a scheduler).
- `ralph.sh` — the loop, at its core `while :; do cat PROMPT.md | claude -p --dangerously-skip-permissions; done`, wrapped with a `--max-iterations` cap, a **circuit-breaker** (stop after K consecutive loops with no new commit or a failing build), per-loop logging, and clean human interrupt. Planning mode and build mode use different prompts.

**Sharp edges carried as guardrails** (from Huntley): duplicate implementations from incomplete searches; placeholder bias from the model's reward function (run dedicated cleanup loops); a wedged codebase on wakeup (`git reset --hard` + a rescue prompt); wrong specs waste the most time — fix the spec, not the loop. Ralph is *"deterministically bad in an undeterministic world"* and works by eventual consistency; a senior engineer steering the spec is non-negotiable (*"anyone claiming engineers are no longer required… is peddling horseshit"*).

---

## Part 3 — Skills to build

Ordered by implementation priority. Existing skills kept as-is: `commit`. Existing skills kept but upgraded (see rows 12–14): `create-handoff`, `resume-handoff`, `prd-development`.

| # | Skill | Replaces | Core tenets | Key mechanics |
|---|-------|----------|-------------|---------------|
| 1 | **`/design`** | (new) | T1 T2 T3 | Batched rounds of 3–5 questions w/ recommended answers, most-important-first; assumption ledger (VERIFIED/UNVERIFIED) rendered every round; "enough" stop-gap; produces Design Doc + **Interface Spec** (signatures, schemas; 2–3 variants for load-bearing interfaces); hard gate: no planning until I sign off. |
| 2 | **`/plan`** | creating-plan | T3 T4 T8 T14 | Consumes design doc + interface spec (lineage frontmatter); design is recommended, not required — without one, plans from the user's description. One step = one commit. Every step is buildable and verifiable from the plan header + that step alone (the implementer is a low-context model). Step template: Files / Interfaces (uses + adds, full signatures) / Scope (incl. must-NOT-change) / Verify (literal command + expected output, or `MANUAL:`) / `[ ]` + `Impl note:` + `Review note:`. Signatures, paths, sequences, commands — no code. Supports `Decision:` points with named forks. Feature-level success criteria at top. One sign-off on the full plan (criteria + steps + checks). One feature per plan — refuses to plan more. |
| 3 | **`step-reviewer`** (subagent def) | (new) | T5 T9 | Fresh context, Sonnet; ships as plugin agent `flow:step-reviewer`. Input: plan header + its one step + the diff since base, never the implementer's narrative (`Impl note:` is an unverified claim). **Runs the step's Verify itself**: no verdict without it. Blocks only on real violations: Verify fails, step intent missing or exceeded, a file outside `Files:`, `Must NOT change` touched, signature ≠ `Adds:`, a test that can't fail, a real bug. Style/naming/judgement calls → non-blocking notes. Verdict: APPROVE (with notes) / BLOCK (implementer can fix) / ESCALATE (needs my decision; gives options + recommendation). Read-only except it appends its own line to the step's `Review note:`. |
| 4 | **`/implement`** | implementing-plan | T5 T6 T8 T13 | Step loop: red-capable check first → implement → checks green → dispatch step-reviewer → APPROVE ⇒ auto-commit (via commit skill) + continue; BLOCK ⇒ fix, re-review, max 3 then pause. **Fills the plan form as it goes**: checkboxes, `Impl note:` per step, reviewer verdict into `Review note:`. Handles `Decision:` forks — minor: log + proceed; interface/scope-touching: back to me. Hard stop on any interface deviation from signed spec. Pauses at phase boundaries + MANUAL steps. At ~60% context: handoff + resume (T13). |
| 5 | **`/kb-init`** | (new) | T10 | One-time at project init: scans repo, interviews me briefly (batched, per T2), scaffolds **both `kb/` and `thoughts/`** skeletons + `_index.md` + seeds architecture.md/domain.md from code + my answers; **ensures both dirs are git-tracked (removes any gitignore entry) and commits the scaffold to main**; trims CLAUDE.md to rules-only with index pointer. |
| 6 | **`/kb-sync`** | (new) | T10 T12 | Called by commit skill (and manually). Reads diff + `_index.md`; updates only conceptually-affected docs; appends to graveyard.md when an approach was reverted/rejected; no-op on mechanical diffs; keeps `_index.md` complete. |
| 7 | **`/oneshot`** | oneshot | T1 T6 | Track 3: compressed design (one round unless I say "enough" immediately) → plan → runs all steps with reviewer-gated auto-commits → PR + summary w/ assumption ledger + evidence links. Never pauses except reviewer 3-strike. |
| 8 | **`/quick`** | (new) | T1 T8 | Track 1: restates intent + verify method in one line, does it, verifies (evidence shown raw), commits. Refuses silently growing scope — if a second file type or interface gets touched, escalates: "this is standard-track work". |
| 9 | **`/retro`** | (new) | T11 T12 | Input: one or more session transcripts (`~/.claude/projects/.../*.jsonl`). Grades the session against T1–T12; finds: unsurfaced assumptions, scope creep, wrong tools, repeated manual procedures. Output: **patches only** — diffs to skills/CLAUDE.md/memory + skill-extraction candidates. |
| 10 | **`/skillify`** | skill-creator (wraps) | T11 | Takes a procedure (from flag, retro, or me), interviews me minimally, writes the skill with: trigger description (no workflow summary — superpowers SDO insight), rationalization table if it's a discipline skill, verify section. Global for meta-workflow, project-level for operational (deploy/logs) skills. |
| 11 | **`/research`** | researching-codebase | T7 T9 T14 | Keep humanlayer subagent fan-out; drop "documentarian only" (opinions allowed, labeled); findings must cite file:line / raw log lines, never summarized numbers without source. Lineage frontmatter. |
| 12 | **`/explore-external`** | (new) | T7 T8 T10 | External-system discovery: public source ⇒ temp-clone + codebase research; closed ⇒ **learning tests** (scripted probes, inputs→outputs recorded), kept runnable as regression detectors. Findings distilled into `kb/external/<system>.md` incl. failure modes. |
| 13 | **`/prd`** | prd-development | T1 T2 T14 | Optional entry point when the product outcome needs defining. Non-technical: what we want to achieve and why. Iterated with the same batched-round + ledger mechanics as design (T2). Feeds /design via lineage link. |
| 14 | **`create-handoff` / `resume-handoff`** | (upgrade existing) | T13 T14 | Add the dumb-zone trigger: at ~60% context, stop at next clean boundary and hand off; never mid-step. Handoff links the plan + exact position in its form. Resume validates state against git before continuing (already built). |
| 15 | **`/ralph`** | ralph_plan / ralph_impl / ralph_research | T1 T3 T8 T13 | Track 4 (§2.6). Interviews me to write + sign `specs/*` (one concern per file), then generates the harness: `fix_plan.md`, `AGENT.md`, `PROMPT.md`, `ralph.sh` (loop with `--max-iterations`, circuit-breaker on K no-progress/failing loops, per-loop commit + push + semver tag, clean interrupt). **Two modes**: *planning* — regenerate `fix_plan.md` from a spec-vs-code diff via subagents; *build* — fresh agent per loop does the top item, searches before writing, no placeholders, green-gated commit, self-updates `fix_plan.md`/`AGENT.md`. Greenfield-default; existing repo ⇒ isolated subtree + explicit opt-in + loud warning. I checkpoint at loop boundaries and judge by git log + tests (T9), never a summary. |

**Cross-cutting rules** (go into global `~/.claude/CLAUDE.md`, not a skill):
- Track ritual: never start work without a track; ask in one line if unstated.
- Assumption rule: any material assumption gets stated before acting, always.
- Eager skill-flagging: repeated procedure ⇒ one-line "skill-ify?" flag.
- Raw-data rule: never present derived numbers without the raw source line.
- Dumb-zone rule: at ~60% context utilization, hand off and resume fresh — never push through.
- Lineage rule: every doc written gets frontmatter (date, author, commit, branch, references).
- Isolation rule: feature work starts on its own **branch** (worktree opt-in — branch by default; worktree for parallel work or greenfield/ralph). Whichever phase runs first (usually /design) ensures it exists — **never commit a feature artifact to the default branch**; always branch from main. The quick track is exempt (stays on the current branch).
- KB/thoughts git rule: kb/ and thoughts/ are git-tracked and merge to main like code — never gitignored (see §2.3).

**Prompt techniques to reuse when writing these skills** (from superpowers research): iron laws (`NO X WITHOUT Y`), rationalization tables, "violating the letter is violating the spirit", red-flag self-checks, recipe-over-prohibition for shaping problems, file handoffs to subagents, durable progress ledgers.

---

## Part 4 — Skill-authoring tenets

Skills are built top-down like everything else: these tenets govern how every skill in Part 3 is written. They are a synthesis of Anthropic's `skill-creator` + superpowers (`writing-skills`, `persuasion-principles`, "match the form to the failure") + humanlayer + mattpocock — keeping only what fits our intent. When authoring, they are layered on top of Anthropic's official `skill-creator` skill.

- **SA1. Show, don't tell.** Every non-obvious rule ships with a ✅/❌ example — the contrast is the teacher. Specific ("type hints + a one-line docstring on every public fn"), never vague ("write good code").
- **SA2. Every line precise and non-redundant.** Cut vague or duplicated lines; specificity is the payload. If a line isn't pulling weight, delete it.
- **SA3. Short beats complete.** Long skills get ignored — tight body, heavy detail behind progressive disclosure.
- **SA4. Carry the *why*.** Written for a fresh subagent with no context: state the intent behind each rule so it reasons past the letter instead of gaming it.
- **SA5. Description = when to trigger, never the workflow.** A workflow-summary description gets followed *instead of* the skill body (superpowers SDO).
- **SA6. Match the form to the failure.** Discipline failure (knows the rule, skips it) → iron law + rationalization table + red flags; wrong-shaped output → positive recipe; missing element → a required template slot. No MUSTs by default; reserve authority for genuine discipline/safety gates.
- **SA7. Study the analogues first.** Read the closest existing skills and take the best of what fits before writing a line.
- **SA8. One at a time, baseline-tested.** Never batch; watch an agent fail without the skill, confirm it complies with it, finish one before the next.

---

## Evidence base (deep research, 2026-07-03)

Key anchors:

- **T13 dumb zone**: Liu et al., *Lost in the Middle* (TACL 2024) — U-shaped attention; *Context Length Alone Hurts LLM Performance Despite Perfect Retrieval* (arXiv 2025) — 13.9–85% degradation from length alone; Sourcegraph Amp compaction at 64–75%; 50-session Claude Code study: quality drop from ~60%. Caveat: exact threshold varies with codebase density — 60/75 is practitioner consensus, not law.
- **Living plans (2.2)**: plan–code co-evolution (CollabCoder, ACL 2026) — failures classified as implementation-level vs plan-level; "long-task drift" and "progress-as-completion" as documented agent failure modes (EPAM 2026); Addy Osmani on plan files as durable lab notes across resets.
- **Learning tests (2.4)**: Mini-SWE-Agent ablation (2025) — probe scripts +60 points vs +4–5 for static analysis; Willison's "scout" pattern (2025/2026); read-only probe agents (arXiv 2025).
- **Lineage (T14)**: ADR supersedes-links; `depends_on` frontmatter graphs (ContextNest, arXiv 2026 — spec adoption thin, principle validated); HumanLayer 12-Factor Agents Factor 3 (own your context window).

## Open items
- CI drift-check for KB (cheap-model "did this diff invalidate any doc?") — later, once kb-sync proves itself.
- Decide `/quick` vs just doing it inline with the cross-cutting rules — may not need a skill.
