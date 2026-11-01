---
name: prd
description: >-
  Define what a feature should achieve — the product outcome, not the technical
  design. Use when the user says "write a PRD", "define the product requirements",
  "what should this feature do", "spec out the product", "/prd", or when the
  product outcome needs defining before technical design begins.
argument-hint: "[feature name or product goal]"
---

# PRD Phase

Define what a feature should achieve and why — the product outcome, iterated with the same rigor as `/flow:design`. A PRD is non-technical: it says what the user/customer gets, not how it's built. The downstream `/flow:design` consumes this doc.

**Output:** exactly one file at `<repo-root>/thoughts/shared/prds/YYYY-MM-DD-<kebab-desc>.md`
- `<repo-root>` = `git rev-parse --show-toplevel`
- Create the directories if missing.

## Process

### 1. Scope and isolate

- **One feature.** If the input describes more than one, scope the first and name the others. Test: if X could ship and be useful without Y, they are two features.
- **Branch** — if on the default branch, propose `feat/<kebab-desc>` off main and create on confirm. The PRD is the first artifact on the feature branch — never commit it to the default branch.

### 2. Self-research

Before asking the user anything, answer what the codebase can answer. Read relevant code, `kb/domain.md`, any existing PRDs or research docs. Dispatch subagents for large scopes. Never ask the user what the code can tell you.

### 3. Questions, one at a time

Ask questions **one at a time**, most important first, following **Asking the user** below. Choose each question after hearing the last answer.

Questions target **product decisions** the codebase can't answer:
- Who is this for?
- What does success look like from the user's perspective?
- What's explicitly out of scope?
- What are the constraints (timeline, compatibility, dependencies)?

✅ Good: one question through the question tool — "Should cancelled orders still appear in the user's order history?" — with options **Shown, greyed out** (users can find past orders for returns and disputes; the history page needs a cancelled state) and **Hidden** (the history stays simple; users lose the record of what they cancelled). Neither is marked recommended.

❌ Bad: the same question with "Recommended: yes, greyed out" — it anchors the user's answer.

❌ Bad: five questions in one message — the user answers the first and skims the rest.

❌ Bad: "What database should we use?" — that's technical design, not product.

❌ Bad: "What does the current order model look like?" — the codebase told you.

**Keep the assumption ledger current after every answer.** Show it in full before the first question and again when the questions end; between questions, one line on what the last answer changed is enough.

**The "enough" stop-gap.** When the user says "enough" or "just go":
1. Mark remaining assumptions as ASSUMED with safe defaults
2. State each default explicitly
3. Keep them visible in the ledger
4. Proceed

### 4. Write the PRD

Use [templates/prd.md](templates/prd.md). Every frontmatter field is required.

**Self-review before presenting:**
1. Placeholder scan — any TBD, TODO, or empty sections? Fill them.
2. Scope — exactly one feature? Nothing technical crept in?
3. Success criteria — each one observable from the user's perspective?
4. Assumptions — all accounted for in the ledger?

### 5. Sign-off

Present the PRD, then ask for sign-off as one question through the question tool. Revise until the user signs off — sign-off is the only exit.

On sign-off:
1. Set `status: signed-off` in the frontmatter
2. Commit the PRD
3. Tell the user: "PRD signed off. Next step is `/flow:design` (or `/flow:research` first if the domain is unfamiliar), which consumes this doc."

## Asking the user

Every question this skill asks — clarifying questions, picks between options, confirmations, sign-off — follows these rules.

1. **Use the question tool.** Before the first question, check for a tool that asks the user (`AskUserQuestion` in Claude Code; if it is listed only as a deferred tool, load it with ToolSearch first) and ask through it. With no such tool, ask in plain text in the same shape: the question, then its options lettered (a), (b), … each with what it means.
2. **One question at a time.** One question per message and per tool call, even though the tool takes four. Wait for the answer, then choose the next question in its light.
3. **No recommended option.** Never label an option "Recommended" or "default", never put your favorite first, and never say which you would pick — not in the question, the options or the text around them. If the user asks what you would pick, answer.
4. **Use the tool well.**
   - `question`: one to three concrete sentences. What the user needs to decide goes here, not in a wall of text before the call.
   - `header`: a chip of 12 characters at most naming the topic.
   - `options`: 2–4 real, mutually exclusive answers with short labels. Each `description` says what choosing it means for the work — what it changes, what it costs, what it rules out — so the user can decide without a recommendation.
   - `multiSelect: true` when several answers can hold at once (for example, which items apply).
   - `preview` when the options are concrete things to compare: a signature, a schema, a snippet, a layout.
   - No "Other" option: the tool adds one for the user's own words.

## Rules

- **Non-technical.** No database choices, no API shapes, no implementation details. If you catch yourself writing a signature or a file path, stop — that belongs in `/flow:design`.
- **User-facing language.** Success criteria describe what the user sees or experiences, not what the system does internally.
- **Same T2 mechanics as /design.** One question at a time through the question tool, no recommended options, assumption ledger, "enough" stop-gap. The rigor is the same; the altitude is different.
