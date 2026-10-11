---
date: 2026-07-02
author: claude-fable-5 (Explore subagent)
status: active
references:
  - ../inspiration/superpowers/
purpose: Primary research for the AI coding workflow — study of obra/superpowers skill system
---

# obra/superpowers — Study Report

## 1. Overall Philosophy & Architecture

Superpowers is a complete software development methodology encoded as composable, auto-triggering "skills" (markdown documents). The core bet: AI agents are skilled developers with poor taste and no discipline — they need process guardrails, not capability upgrades. Four pillars: TDD, systematic-over-ad-hoc, complexity reduction, evidence over claims.

Skills are markdown files with YAML frontmatter (`name` + `description`) in `skills/<skill-name>/SKILL.md`. A session-start hook injects the `using-superpowers` bootstrap skill, which acts as a dispatcher forcing skill checks before any action. Skills reference each other (`**REQUIRED SUB-SKILL:** Use superpowers:writing-plans`).

Canonical pipeline: `brainstorming → writing-plans → subagent-driven-development (or executing-plans) → finishing-a-development-branch`. Human must approve at every transition.

Enforcement language from the bootstrap:
```
If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill.
IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.
This is not negotiable. You cannot rationalize your way out of this.
```

Plus an 11-entry "Red Flags" rationalization table ("This is just a simple question" → "Questions are tasks. Check for skills.").

## 2. Key Skills

### brainstorming
- Hard gate: `Do NOT invoke any implementation skill, write any code, scaffold any project, or take any implementation action until you have presented a design and the user has approved it. This applies to EVERY project regardless of perceived simplicity.`
- Anti-simplicity bias: `"Simple" projects are where unexamined assumptions cause the most wasted work.`
- One question at a time, prefer multiple choice; 2-3 approaches with trade-offs + recommendation; design presented in sections with approval after each; spec to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`; self-review (placeholder scan, consistency, scope, ambiguity); terminal state ONLY `writing-plans`.

### writing-plans
- Plans target "an enthusiastic junior engineer with poor taste, no judgement, no project context, and an aversion to testing".
- Each task 2–5 minutes. Every step shows actual code, exact paths, exact commands with expected output.
- **No Placeholders rule** — plan failures: "TBD", "TODO", "Add appropriate error handling", "Write tests for the above" (without test code), "Similar to Task N".
- Task structure has `Interfaces:` with `Consumes:` / `Produces:` (exact signatures).

### subagent-driven-development (SDD)
- One fresh subagent per task; `"They should never inherit your session's context or history — you construct exactly what they need."`
- `"Do not pause to check in with your human partner between tasks."` (conflicts with Dhruv's T1 — he resolved it: auto-commit per step but he picks track)
- Pre-flight plan review before Task 1; findings presented as ONE batched question.
- Model selection: cheapest model that fits; `"Turn count beats token price... cheapest models routinely take 2-3x the turns"`.
- **File handoffs**: task briefs, reports, review packages via files, never pasted into controller context.
- **Durable progress ledger** at `.superpowers/sdd/progress.md` — survives compaction; `"Controllers that lost their place have re-dispatched entire completed task sequences — the single most expensive failure observed."`
- Statuses: DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, BLOCKED.
- Two-stage review per task: spec compliance + code quality; final whole-branch review.
- Reviewer instructions: `"Do not trust the report. Treat the implementer's report as unverified claims about the code."` and `"Do not pre-judge findings for the reviewer — never instruct a reviewer to ignore or not flag a specific issue."`

### test-driven-development
- Iron Law: `NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST`
- Delete rule: `Write code before the test? Delete it. Start over.` + loophole closures (`Don't keep it as "reference" / Don't "adapt" it / Delete means delete`)
- `"Violating the letter of the rules is violating the spirit of the rules."`
- 11-entry rationalization table; 13 red-flag thoughts.

### systematic-debugging
- Iron Law: `NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST`
- Phases: Root Cause → Pattern Analysis → Hypothesis & Testing → Implementation.
- 3-fix escalation: `"If >= 3: STOP and question the architecture"`.

### verification-before-completion
- Iron Law: `NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE`
- Gate: IDENTIFY what proves the claim → RUN → READ output → VERIFY → ONLY THEN claim.
- Forbids: "should", "probably", "seems to", "Great!", "Done!".
- `"Claiming work is complete without verification is dishonesty, not efficiency."`

### requesting/receiving-code-review
- Reviewer: fresh context, read-only, Critical/Important/Minor, verdict required.
- Receiving: forbidden `"You're absolutely right!"`; READ→UNDERSTAND→VERIFY→EVALUATE→RESPOND→IMPLEMENT; `"External feedback = suggestions to evaluate, not orders to follow."`

### others
- dispatching-parallel-agents (one agent per independent problem; parallel dispatch in one response)
- executing-plans (inline fallback with checkpoints)
- using-git-worktrees (isolation, consent gate)
- finishing-a-development-branch (tests-pass gate; 4 options; typed "discard" confirmation)

## 3. Prompt-Engineering Tricks Worth Stealing

1. **Rationalization prevention tables** — enumerate every excuse, counter each with a one-liner. Discovered via adversarial testing, not invented.
2. **"Violating the letter of the rules is violating the spirit of the rules."** — closes a whole class of rationalization.
3. **Red flags as self-check triggers** — "if you catch yourself thinking X, STOP".
4. **SDO insight**: skill *descriptions* that summarize workflow cause agents to follow the description instead of reading the skill. Description should say WHEN to use, not HOW it works.
5. **Match form to failure**: skips-rule → prohibition + rationalization table; wrong-shape output → positive recipe; omits element → REQUIRED template field; conditional behavior → conditional keyed to observable predicate. `"prohibitions backfire on shaping problems"`.
6. **No nuance clauses**: `"Don't X unless it matters" reopens the negotiation.` Express exceptions as separate conditionals on observable predicates.
7. **Iron Laws** as single-line code-block anchors: `NO X WITHOUT Y FIRST`.
8. **Persuasion stack**: Authority + Commitment + Social Proof; cited compliance jump 33%→72% (Meincke et al., 2025).
9. **Micro-test wording**: 5+ reps per variant; always include a no-guidance control.
10. **File handoffs** to keep controller context clean.
11. **Durable progress ledger** for compaction survival.
12. **Meta-testing failed skills**: ask the violating agent "how could the skill have been written so Option A was clearly the only answer?" — reveals documentation vs organization vs willfulness.
13. **`<SUBAGENT-STOP>` tag** so meta-skills don't hijack subagent work.

## 4. Gaps vs Dhruv's Tenets

1. No automated feedback beyond unit tests — no deploy/API/Playwright verification (his T7 is stronger).
2. Human excluded during execution (explicit no-pause rule) — Dhruv keeps phase-boundary pauses + track control.
3. Plan contains AI-authored code detail — Dhruv wants Interface Spec sign-off first (T3).
4. Review is task-scoped, not intent-scoped until the very end.
5. No pre-agreed success-criteria negotiation step.
6. TDD absolutism awkward for integration-heavy work (LiveKit/Gemini) — Dhruv chose "red-capable check first" generalization (T8).
7. Heavy ceremony for small changes — Dhruv added quick track.
