---
name: research
description: >-
  Research the codebase or domain for a feature — before design, before code.
  Use when the user says "research this", "explore the codebase", "how does X
  work in our code", "what do we have for Y", "investigate", "/research", or
  when the codebase or domain is unfamiliar before designing.
argument-hint: "[what to research — a feature area, question, or domain topic]"
---

# Research Phase

Fan out subagents to explore the codebase and domain, then synthesize findings into a research doc. Research runs entirely in subagents (T7) — the main context stays clean for synthesis. The output feeds `/flow:design`.

**Output:** exactly one file at `<repo-root>/thoughts/shared/research/YYYY-MM-DD-<kebab-desc>.md`
- `<repo-root>` = `git rev-parse --show-toplevel`
- Create the directories if missing.

## Iron Law

```
EVERY FINDING CITES file:line OR RAW OUTPUT — NEVER A SUMMARIZED NUMBER WITHOUT ITS SOURCE
```

## Process

### 1. Read what the user gave you

If the user mentioned specific files, tickets, or docs — read them FULLY yourself, in the main context, before spawning anything. You need complete context to decompose the research well.

### 2. Sharpen the question

State the research question in one line. If the request is vague, sharpen it:
> "I'll research how order cancellation works — the flow, the edge cases, and what would need to change. That right?"

One word from the user ("yes", "go") is enough to proceed.

### 3. Fan out subagents

Dispatch subagents for parallel exploration. Pick from these based on what the question needs — not all are required for every research:

| Subagent | When |
|----------|------|
| **codebase-locator** | Find all files related to the area |
| **codebase-analyzer** | Understand how specific components work |
| **codebase-pattern-finder** | Find similar patterns or implementations to learn from |
| **thoughts-locator** | Find prior research, designs, or decisions |
| **thoughts-analyzer** | Deep-dive into a specific prior doc's reasoning |

Also read these yourself if they exist (skip silently if not):
- `kb/architecture.md` — system boundaries and invariants
- `kb/domain.md` — project glossary
- `kb/graveyard.md` — what was tried and rejected

Start with locators to find what exists, then dispatch analyzers on the most promising findings. Run multiple agents in parallel when they're searching for different things. Each agent knows its job — tell it what you're looking for, not how to search.

**Wait for ALL subagents to complete before synthesizing.** Do not write the doc from partial results.

### 4. Synthesize

Write the research doc. Every claim cites `file:line` or raw output. Opinions are welcome but labeled.

```markdown
---
date: YYYY-MM-DDTHH:MM:SS+TZ
author: agent (model-id)
git_commit: <short hash>
branch: <current branch>
status: active
references:
  - <any PRD or prior doc that prompted this>
---

# Research: [Topic]

**Question:** [the sharpened research question]

## Current State

How it works today — modules, data flow, key interfaces. Cite `file:line`.

## Patterns and Precedents

Similar implementations in the codebase. Conventions they follow. Cite paths.

## Constraints and Gotchas

Edge cases, invariants, surprising behavior the code reveals. Include raw evidence
(error messages, log lines, test assertions).

## Prior Decisions

Anything from `kb/graveyard.md`, ADRs, or prior research that's relevant. What was
tried, what was rejected, and why. Cite the source doc.

## Open Questions

Questions the codebase couldn't answer — these feed into `/flow:design`'s batched
rounds. Each with a recommended answer if you have one.

## Opinion

Your assessment: what's straightforward, what's risky, what deserves attention during
design. This section is judgment, not fact — labeled as such.
```

### 5. Deliver

Present in chat: the key findings (3–5 bullets, each citing a file or evidence), the open questions, and the file path. The doc has the detail — don't repeat it all.

Tell the user: "Research written. Next step is `/flow:design` to turn this into an interface spec, or ask follow-up questions."

**Follow-ups:** if the user has more questions, append a `## Follow-up: [topic]` section to the same doc rather than creating a new one. Dispatch new subagents as needed.

## Rules

- **Cite or cut.** A finding without `file:line` or raw output is a claim. Claims don't survive into design.
- **Opinions are welcome, labeled.** "I think X because Y" in the Opinion section is useful. "X" presented as fact when it's judgment is not.
- **No derived numbers without source.** "There are 47 callers" includes the grep output that produced 47.
- **No code changes.** Research is read-only. If you find a bug, note it.
- **No design, no steps.** This runs before design. Surface facts and questions — don't write interface specs or plan steps.
- **Keep the main context clean.** Subagents do the reading. You do the synthesis. Long file contents stay in the subagents, not pasted into the controller context.
