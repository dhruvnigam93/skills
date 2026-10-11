---
date: 2026-07-02
author: claude-fable-5 (analysis subagent)
status: active
references:
  - ~/.claude/history.jsonl (3,181 prompts; ~1,292 in ds-ai-companion-rtc)
  - /Users/dhruvnigam/Projects/ds-ai-companion-rtc/thoughts/
  - /Users/dhruvnigam/Projects/ds-ai-companion-rtc/CLAUDE.md
purpose: How Dhruv ACTUALLY works with Claude Code — style, frustrations, revealed preferences. Essential reading for any agent working with him or building his skills.
---

# Dhruv's Real Usage Patterns (from 3,181 prompts)

## 1. Command frequency (all projects / RTC project)

| Command | All | RTC |
|---------|-----|-----|
| /clear | 191 | 83 |
| /model | 178 | 49 |
| /context | 28 | 8 |
| /mcp | 15 | 12 |
| /creating-plan | 14 | 9 |
| /implementing-plan | 11 | 7 |
| /rewind | 12 | 3 |
| /resume-handoff | 4 | 3 |
| /create_handoff | 2 | 2 |
| /researching-codebase | ~3 | 1 |

/clear + /model = 61% of slash usage — he resets context aggressively and switches models constantly. Structured skills used only for the heavyweight phases. ~85 one-word commands in RTC alone: `go`, `check`, `done`, `yes`, `push`, `deploy`.

## 2. Style (critical for interaction design)

- **Bimodal prompts**: one-word continuations OR 500–3,600-char stream-of-consciousness design dumps. Median 47 chars, mean 104.
- **Typo-heavy speed typing** ("deply", "trasnctip", "debator") — thinking faster than typing; expects intent-parsing, never proofreads.
- **"Ask me N questions before starting"** used ~11 times (N = 2, 3, 5) — his natural alignment ritual, always batched.
- **"commit using commit skill"** (sometimes in caps) — wants the workflow, not raw git.
- Audience-aware outputs: "tables dont do well in slack", "the qre non technical ops peopel so please skip tech stuff".

## 3. Frustration patterns (what to never do)

A. **Wrong project/agent routing** (most frequent, 7+): "there is not room in the ai-deabtor project - wehre have you created the room!" → became CLAUDE.md rules.
B. **Wrong tools**: "never deply with defailt agent - always use the explicit config"; "use cloudwatch isntaedof lk agent logs".
C. **Unwanted changes / rollbacks**: "lets roll bak - i dont like any logginghcanges"; "nah, elt this be, discaRD CHAGNES FOR NOW" (caps = escalation).
D. **Scope creep**: "dont update the xamples json - just say it to generate 10"; "i measn create a github issue with al the detrails - dont raise a PR".
E. **Distrusts AI-reported numbers**: "dont rely on reported numebrs and corss check the numbers yourself using timestamps".

## 4. Design involvement — he specifies:

- Data structures inline: "the reutnr is something like { 'common' : list[ { 'player' , 'reason' } ] }..."
- Component boundaries for swappability: "design it to be a searpate compinenet so we can sweitch out the implentation"
- Blast radius: "only deply the director new nothing esle should be deplyied"; "no agent changes only ui changes"

## 5. Verification habits (RTC prompt mention counts)

deploy 112 · test/E2E 113 · logs/CloudWatch 102 · check 121 · playwright 26 · commit 53.
Loop: change → deploy to cloud (never local) → wait ~2min → E2E / Playwright → CloudWatch → S3 transcript → (sometimes) Gemini-scored eval script → commit or iterate. Statistical validation habit: "run 5 debates", "try 5 more to be sure".

## 6. Planning artifact style (from thoughts/)

Header: date, status (Planned/Implementing/Implemented/Verified), branch. Problem summary as table (Issue|Source|Impact|Root Cause) with quantitative data ("21% of turns"). Phases small (3–7 checkboxed items), ordered by risk. Key design decisions called out with rationale. Testing strategy baked into each phase. "What We're NOT Doing" lists. Research docs separate from plans, data-heavy; plans consume them.

## 7. Inferred tenets he later confirmed

- Meta-learning loop: "why did you not get the right metrics in the first attempt is there any learning - do we need to update claude md for this?" (→ T12)
- Deploy-to-test, never local (→ T7 automated feedback)
- Trust raw data (→ T9)
- Uses Claude Code for personal life too (finance, tax, pregnancy project) — same style everywhere; meta-workflow skills should be global.
