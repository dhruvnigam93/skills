---
date: 2026-07-04
author: claude-opus-4-8
status: active
references:
  - ai-coding-workflow.md
  - HANDOFF.md
purpose: Living progress ledger for building the 15 workflow skills, one per session. Updated as each skill is signed off. The /workflow-build skill points here for "what's next". This is the durable cross-session ledger (T13) — the in-session task list does not survive /clear.
---

# BUILD-STATUS — workflow skill build

**How to use**: after Dhruv signs off a skill, mark it ✅ DONE with the date + path, set the next one 🔨 IN-PROGRESS, and update the "Next up" line. A fresh session resumes from this file alone.

**Next up: #5 `/kb-init`.** #1–3 and #4, #11–14 are ✅ DONE. Skills ship from `~/Projects/skills` (github.com/dhruvnigam93/skills), plugin `flow` — new skills go in `plugins/flow/skills/<name>/`, subagents in `plugins/flow/agents/<name>.md`, bump `plugin.json` version on ship.

## Status

| # | Skill | Type | Status | Path / notes |
|---|-------|------|--------|--------------|
| 1 | `/design` | new | ✅ DONE | `~/Projects/skills/plugins/flow/skills/design/` — 2026-07-04 (published v0.1.0) |
| 2 | `/plan` | rewrite creating-plan | ✅ DONE | `~/Projects/skills/plugins/flow/skills/plan/` — 2026-10-01 (v0.2.0). Local `creating-plan` left untouched. |
| 3 | `step-reviewer` | new subagent | ✅ DONE | `~/Projects/skills/plugins/flow/agents/step-reviewer.md` — 2026-10-01 (v0.3.0), dispatched as `flow:step-reviewer` |
| 4 | `/implement` | rewrite implementing-plan | ✅ DONE | `~/Projects/skills/plugins/flow/skills/implement/` — 2026-10-11 (v0.4.0). Sources: humanlayer implement_plan, superpowers executing-plans + SDD. |
| 5 | `/kb-init` | new | ⬜ TODO | `~/Projects/skills/plugins/flow/skills/kb-init/` — inits **both kb/ + thoughts/** (git-tracked) at project init |
| 6 | `/kb-sync` | new | ⬜ TODO | `~/Projects/skills/plugins/flow/skills/kb-sync/` |
| 7 | `/oneshot` | new | ⬜ TODO | `~/Projects/skills/plugins/flow/skills/oneshot/` |
| 8 | `/quick` | new (maybe) | ⬜ TODO | OPEN: skill vs inline CLAUDE.md cross-cutting rules |
| 9 | `/retro` | new | ⬜ TODO | `~/Projects/skills/plugins/flow/skills/retro/` |
| 10 | `/skillify` | wraps skill-creator | ⬜ TODO | `~/Projects/skills/plugins/flow/skills/skillify/` |
| 11 | `/research` | upgrade researching-codebase | ✅ DONE | `~/Projects/skills/plugins/flow/skills/research/` — 2026-10-11 (v0.4.0). Sources: humanlayer research_codebase, mattpocock research. Dropped documentarian-only; opinions labeled. |
| 12 | `/explore-external` | new | ✅ DONE | `~/Projects/skills/plugins/flow/skills/explore-external/` — 2026-10-11 (v0.4.0). Learning tests + temp-clone approach from spec §2.4. |
| 13 | `/prd` | adapt prd-development | ✅ DONE | `~/Projects/skills/plugins/flow/skills/prd/` — 2026-10-11 (v0.4.0). Reuses T2 mechanics from /design at product altitude. |
| 14 | `create-handoff` / `resume-handoff` | upgrade pair | ✅ DONE | `~/Projects/skills/plugins/flow/skills/{create,resume}-handoff/` — 2026-10-11 (v0.4.0). Sources: humanlayer create/resume_handoff, mattpocock handoff. Added dumb-zone trigger + plan linkage. |
| 15 | `/ralph` | replaces ralph_plan/impl/research | ⬜ TODO | `~/.claude/skills/ralph/` |

Legend: ⬜ TODO · 🔨 IN-PROGRESS · ✅ DONE

## Open items (deferred, non-blocking)
- CI drift-check for KB (cheap-model "did this diff invalidate any doc?") — after kb-sync proves itself.
- #8 `/quick`: decide whether it needs to be a skill at all, or just the cross-cutting rules in CLAUDE.md — decide when we reach it.

- **Central style guide** (Python + general): style/naming rules live there, not in the reviewer. step-reviewer files style issues as non-blocking notes; cite the guide once it exists. Location TBD.
- **At #4 `/implement`:** `/flow:plan` calls the implementer "a cheap model with no context"; Dhruv now wants it "decent and solid". Keep "no context", drop "cheap". `/implement` must also: pass plan path + step + base SHA (+ prior BLOCK reasons) to `flow:step-reviewer`, parse its `VERDICT:` first line, route ESCALATE to the user.

## Log
- 2026-07-04 — Project resumed. Created `/workflow-build` orientation skill + this ledger. No skills built yet. Next: `/design`.
- 2026-07-04 — #1 `/design` ✅ DONE at `~/.claude/skills/design/`. Hand-wrote a version, then ran skill-creator clean-room (blind subagent) to A/B them; the skill-creator version won on merit (3-way altitude example, more complete template w/ required slots, turnkey Design-It-Twice subagent prompt, dependency categories). Promoted it with two grafts from the hand-written (merged description w/ trigger carve-outs; iron-law code-block anchor). Both versions snapshotted in `design-skill-eval/`.
- 2026-07-04 — Process learning encoded into `/workflow-build` ritual: step 3 now authors *with* skill-creator; new step 4 validates by skill type (interactive/discipline skills → subjective or clean-room A/B, not the headless quant loop; description-optimizer is the universal cheap trigger check; Dhruv sets depth). Next: #2 `/plan`.
- 2026-07-04 — Workflow decision (spec → v1.5): **kb/ + thoughts/ are git-tracked and merge to main like code** (not gitignored); kb/ = current truth on main, thoughts/ = append-only history. **Isolation rule**: feature work on its own branch (worktree opt-in), always branch from main, never commit feature artifacts to the default branch; quick track exempt. Encoded in spec §2.3 + cross-cutting rules + global CLAUDE.md; added **Phase 0 (branch)** to live `/design`; `/kb-init` (#5) now scaffolds **both kb/ + thoughts/** at project init. Branch defaults: branch-by-default / quick-exempt.
- 2026-10-01 — Skills moved to a public plugin marketplace: `github.com/dhruvnigam93/skills`, plugin `flow` (`/flow:design`). Repo is now the source of truth; ~/.claude/skills/design is superseded.
- 2026-10-01 — #2 `/plan` ✅ DONE at `~/Projects/skills/plugins/flow/skills/plan/` (v0.2.0). Decisions from Dhruv: step = commit (one thing, automated check, easy review); implementer is a low-context model → iron law: every step buildable + verifiable from plan header + that step alone; signatures/paths/sequences/commands, no code or test code; ONE sign-off on the full plan (criteria + steps + checks); design recommended, never forced (else the user's description is the design). No validation run — Dhruv iterates on real use. Spec row 2 updated (v1.6). Next: #3 step-reviewer.
- 2026-10-01 — #3 `step-reviewer` ✅ DONE at `~/Projects/skills/plugins/flow/agents/step-reviewer.md` (v0.3.0). Decisions from Dhruv: reviewer runs the step's Verify itself (iron law: no verdict without it); blocks only on real violations (failing Verify, plan violated, files outside `Files:`); style/naming/ambiguity → non-blocking notes; verdicts APPROVE (with notes) / BLOCK (implementer can fix) / ESCALATE (needs human; options + recommendation); reviewer appends its own line to the step's `Review note:` (its only edit); model Sonnet. Spec row 3 + implement-phase line updated (v1.7). No validation run. Next: #4 /implement.
- 2026-10-11 — Speed-run batch: #4 `/implement`, #11 `/research`, #12 `/explore-external`, #13 `/prd`, #14 `create-handoff`/`resume-handoff` — all ✅ DONE (v0.4.0). All built from source material: spec Part 3 rows + §2.2–2.4, humanlayer originals (implement_plan, research_codebase, create/resume_handoff), superpowers analogues (executing-plans, SDD), mattpocock analogues (research, handoff). Key choices: `/implement` uses superpowers ledger pattern (plan-as-ledger), SDD reviewer dispatch (3 BLOCK max), continuous execution (pause only at phase boundaries/MANUAL/ESCALATE/dumb-zone); `/research` drops documentarian-only (opinions labeled in Opinion section); `/explore-external` learning tests from spec §2.4 evidence; `/prd` reuses T2 mechanics at product altitude; handoff pair adds dumb-zone trigger + plan position linkage. No validation run — Dhruv iterates on real use. Next: #5 /kb-init.
