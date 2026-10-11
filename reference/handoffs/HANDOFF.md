---
date: 2026-07-03
author: claude-fable-5
status: active
references:
  - ai-coding-workflow.md
  - research/01-superpowers-study.md
  - research/02-humanlayer-study.md
  - research/03-mattpocock-study.md
  - research/04-dhruv-usage-patterns.md
  - research/05-kb-organization-research.md
  - research/gemini-deep-research-2.md
purpose: Sign-off / handoff from the founding session. START HERE if you are the next agent.
---

# HANDOFF — AI Coding Workflow Project

**To the next agent**: Dhruv is building his personal AI coding workflow, strictly top-down: **tenets → workflow → skills**. The tenets and workflow are DONE and approved (v1.2). Your job is to **build the skills**. This folder (`~/.claude/workflow/`) is the project's working folder — it is NOT a special Claude Code directory; nothing here auto-loads. Read this file, then `ai-coding-workflow.md`, then `research/04-dhruv-usage-patterns.md` before doing anything.

## State

- `ai-coding-workflow.md` **v1.4** — the master document: 14 tenets, **4-track** workflow (quick / standard / oneshot / **ralph**), **15 skills** with per-skill tenets, **Part 4 skill-authoring tenets (SA1–SA8)**. Ralph loop added 2026-07-04 (§2.6, skill row 15), sourced from Geoffrey Huntley (ghuntley.com/ralph/) — research in `research/06-ralph-loop-research.md`. Skill-authoring tenets (SA1–SA8) locked 2026-07-04 and **implemented directly in `~/.claude/skills/skill-creator/SKILL.md`** (Anthropic's official skill, customized: description-caveat patch + a "Skill-authoring tenets" section) so we author with the credible skill. Approved by Dhruv; PDF sent to him on Telegram (regenerate with `tools/md2pdf_workflow.py`, needs `uv run --with reportlab`).
- All research persisted in `research/`. Inspiration repos (shallow clones, studied 2026-07-02) in `inspiration/` — superpowers, humanlayer, mattpocock-skills. Grep them for verbatim prompt text when writing skills.
- Cross-session memory pointer exists: `~/.claude/projects/-Users-dhruvnigam-Projects-ds-ai-companion-rtc/memory/project_ai_coding_workflow.md` (note: memory lives under the RTC project because that's where the founding chats happened; the canonical home is HERE).

## Folder map

```
~/.claude/workflow/
  HANDOFF.md                  ← you are here
  ai-coding-workflow.md       ← THE document (tenets/workflow/skills). Source of truth.
  ai-coding-workflow.pdf
  research/
    01-superpowers-study.md   ← prompt-engineering arsenal (iron laws, rationalization tables, SDO)
    02-humanlayer-study.md    ← plan template + Dhruv's local divergences = his revealed preferences
    03-mattpocock-study.md    ← grilling/seams/deep-modules verbatim excerpts
    04-dhruv-usage-patterns.md← HOW TO WORK WITH DHRUV. Read before interacting.
    05-kb-organization-research.md ← KB design evidence (T10)
    gemini-deep-research-2.md ← citations for T13 dumb zone, living plans, learning tests, T14 lineage
  inspiration/{superpowers, humanlayer, mattpocock-skills}/
  tools/md2pdf_workflow.py
```

## Next task: build the skills, in this order

1. **`/design`** → new skill at `~/.claude/skills/design/SKILL.md`
2. **`/plan`** → rewrite of `~/.claude/skills/creating-plan/` (keep its templates/references structure — he likes modular skills)
3. **`step-reviewer`** → subagent definition (`~/.claude/agents/step-reviewer.md`)
4. **`/implement`** → rewrite of `~/.claude/skills/implementing-plan/`
5. Then: `/kb-init`, `/kb-sync`, `/oneshot`, `/ralph` (track-4 bootstrap harness, §2.6 + row 15), `/quick`(maybe), `/retro`, `/skillify`, `/research` upgrade, `/explore-external`, `/prd` adaptation, handoff-pair upgrade.

Full specs for each are in `ai-coding-workflow.md` Part 3 (mechanics column) — treat those rows as the requirements. Per his own workflow: **before building each skill, run a short batched-question alignment round with him** (3–5 questions, recommended answers, most important first). Do NOT build all skills in one shot without checkpoints — that would violate T1 in the very act of implementing it.

## Decision log (locked — do not re-litigate)

1. Batched question rounds (3–5, most-important-first, each with a recommended answer) + assumption ledger; he can say **"enough"** → proceed on safe assumptions, ledger stays visible.
2. Interface Spec: AI drafts (2–3 variants for load-bearing interfaces), he signs off. Hard gate before planning.
3. **He always picks the track** (quick/standard/oneshot). Never auto-select. Ask in one line if unstated.
4. Auto-commit when a step passes checks + independent review. No per-commit ask. Pauses only at phase boundaries, MANUAL steps, interface deviations.
5. TDD where possible; otherwise any red-capable automated check; otherwise explicit `MANUAL:` flag — never silent.
6. Step review = fresh-context subagent, sees ONLY step spec + diff + verification evidence. 3 BLOCK cycles → pause for him.
7. Plans are living forms: checkboxes, `Impl note:`, `Review note:`, `Decision:` forks; implementation-level vs plan-level failure classification.
8. Dumb zone: warn ~60% context, hard handoff by 75%. No recursive summarization.
9. All docs get frontmatter (date, author human/agent+model, commit, status, references). thoughts/ = transactional; kb/ = current state.
10. kb/ = _index.md, architecture.md, domain.md, graveyard.md, adrs/, external/. kb-sync runs inside the commit workflow.
11. Meta-workflow skills global (`~/.claude/skills/`); operational skills per-project.

## How to work with Dhruv (from research/04 — condensed)

- Typo-heavy, fast prompts; parse intent, never comment on typos. One-word replies ("go", "check", "yes") mean continue.
- Always give a recommendation with every question. Batch questions (3–5). Never one-at-a-time interrogation.
- Never exceed stated scope — he explicitly punishes scope creep and unwanted "improvements". State blast radius before changes.
- Never present derived numbers without raw evidence (he cross-checks timestamps).
- Every correction he gives → offer to encode it (CLAUDE.md/memory/skill). He expects this.
- He wants eager skill-flagging: notice repeated procedures, offer "skill-ify?" in one line.

## Gotchas

- **Gemini MCP** (`~/mcp/gemini_mcp/`): deep research works now (fixed 2026-07-03), but after any server-code change the MCP must be reconnected by Dhruv via `/mcp` — you cannot restart it yourself. Deep research writes to a file async (up to 60 min); watch for an error file appearing within ~seconds (means launch failed). Poll with a background watcher.
- The first deep-research attempt errors looked like success ("started successfully") — always check the output file's first line for `# Deep Research Error`.
- His `~/.claude/skills/` currently holds the humanlayer-derived skills being replaced — do not delete them until replacements are approved; rewrite in place only after his sign-off per skill.
- When writing skill descriptions, apply the SDO insight (research/01 §3.4): description says WHEN to trigger, never a workflow summary — otherwise the model follows the description instead of reading the skill.
- Telegram MCP available for sending him docs/PDFs (`send_telegram` with file_path).

## Prompt-technique arsenal for writing the skills

From superpowers (research/01): iron laws in code blocks, rationalization tables, "violating the letter is violating the spirit", red-flag self-checks, recipe-over-prohibition, file handoffs, durable ledgers, `<SUBAGENT-STOP>` guards. From Pocock (research/03): leading words, recommended answers, falsifiable heuristics (deletion test), "Avoid:" vocabulary lists, `disable-model-invocation: true` for user-only orchestration skills. From humanlayer (research/02): the plan template skeleton, locator/analyzer tool-restriction pattern, "spawn new research to verify corrections".
