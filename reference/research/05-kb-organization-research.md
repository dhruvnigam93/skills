---
date: 2026-07-03
author: claude-fable-5 (web-search-researcher subagent) + gemini-3.1-pro (ask mode)
status: active
references:
  - gemini-deep-research-2.md
purpose: Secondary research — how to organize the repo-resident knowledge base (T10). Two independent sources that converged.
---

# KB Organization Research (web + Gemini, merged)

## Source A: Web research synthesis

### Pattern catalog
- **CLAUDE.md** (Anthropic): <200 lines; `@path` imports (still load at launch); `.claude/rules/*.md` with `paths:` frontmatter = truly on-demand; child-dir CLAUDE.md loads lazily. "For each line, ask: Would removing this cause Claude to make mistakes? If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"
- **Agent Skills standard** (agentskills.io): 3-stage progressive disclosure — ~100-token name+description at startup → <5k-token SKILL.md on activation → reference files on demand.
- **Cline Memory Bank**: 6-file cascade (projectBrief → productContext / systemPatterns / techContext → activeContext / progress). ALL loaded every task (controversial: burns context, guarantees completeness). Higher docs change rarely, lower change often.
- **llms.txt**: H1 + blockquote summary + H2 link lists; `## Optional` section for skippable resources.
- **ADRs**: numbered, Status lifecycle (proposed/accepted/deprecated/superseded); index as the always-loaded summary.
- **obra pattern**: date-stamped specs/plans (`YYYY-MM-DD-`) — age = natural deprioritization.
- Practitioner quotes: Breunig "Is everything in this context earning its keep?"; 12-Factor Agents Factor 3 "Own Your Context Window".

### Recommended split (token budgets)
| Layer | Mechanism | Budget |
|-------|-----------|--------|
| CLAUDE.md | always loaded | <3k tokens |
| @-imports (index, glossary) | at session start | <2k combined |
| rules/*.md | on matching file reads | <500 each |
| skills | on activation | <5k each |
| kb deep docs / ADRs / specs | on demand | unlimited |

## Source B: Gemini ask-mode (agreed + added)

### Structure
```
agents.md / CLAUDE.md      # always loaded, <150-200 lines, hard rules + POINTER TO INDEX
kb/ (or .agent/kb/)
  _index.md                # fast-routing map ~600 tokens: "read X if touching Y"
  architecture.md          # boundaries & invariants (~1.5k tokens)
  domain.md                # DDD glossary (~1k)
  adrs/                    # ~500 tokens each
thoughts/                  # ephemeral working memory, flushed/archived on merge
```

### Freshness: "DoD-driven agent updates + CI drift check"
- Blind post-commit hooks that force doc writes = churn + paraphrased garbage. Human-only = rot.
- Instead: `/kb-sync` as a mandatory Definition-of-Done step in the commit workflow — reads branch diff + _index.md, updates only conceptually-altered docs.
- Enforcement (later): CI `kb-drift-check` with a cheap model: "Given this diff and these KB files, did the changes render any KB doc factually incorrect? YES/NO" → fail CI on YES.

### Anti-patterns (both sources agree)
1. God files / context stuffing (Cline activeContext growing unbounded).
2. Auto-generated paraphrasing ("connect() connects to the database").
3. Redundant truth (stack defined in 3 places — define once).
4. **Unindexed deep lore** — "If the agent cannot find it cheaply via progressive disclosure, the knowledge functionally does not exist."

### What belongs in the KB (beyond "what code cannot say")
1. **Negative knowledge / the graveyard**: "If you tried a Redis cache in 2025 and it caused a race condition, the code no longer shows it. The KB must say: Do not introduce Redis for X; see ADR-004." (agents love re-optimizing into known dead ends)
2. **Implicit system boundaries**: "Service A must never synchronously call Service B."
3. **Ubiquitous language**: a "Customer" pays, a "User" logs in → prevents `customer_password` columns.

### Literature notes
- Working memory vs semantic memory separation: mixing task state with structural knowledge degrades attention → thoughts/ vs kb/ split is the right call.
- Graph-style curated indexes (_index.md as a directed graph) outperform naive vector RAG for reasoning tasks.
- agents.md standardization (Linux Foundation, late 2025) — proprietary rule-file fragmentation caused erratic behavior.

## Decision taken for the workflow (v1.2)
kb/ = _index.md + architecture.md + domain.md + graveyard.md + adrs/ + external/<system>.md; CLAUDE.md <200 lines pointing at _index.md; kb-sync inside commit skill; thoughts/ transactional vs kb/ current-state; frontmatter with provenance + lineage (T14).
