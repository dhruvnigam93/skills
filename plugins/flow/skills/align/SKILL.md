---
name: align
description: >-
  Ask N sequential questions to align on what the user actually wants before
  producing a permanent artifact or taking a concrete action. Use when the user
  says "align", "ask me N questions", "check my assumptions", "make sure we're
  on the same page", "/align", or when you're about to produce something
  permanent and sense there are untested assumptions.
argument-hint: "<number of questions, e.g. 3 or 5>"
---

# Align

Ask N sequential questions — each one chosen to maximally reduce the gap between what the user wants and what you would execute. This is not a survey; it is a search. Each question targets the assumption whose wrongness would cost the most.

**No output file.** The alignment lives in the conversation. Other skills (`/flow:design`, `/flow:prd`, `/flow:plan`) consume it by being invoked after.

## Iron Law

```
ONE QUESTION AT A TIME, THROUGH THE QUESTION TOOL, WITH NO RECOMMENDED OPTION
```

## Process

### 1. Set N

The user passes N as the argument (e.g. `/flow:align 5`). If no number, ask once, through the question tool: "How many questions?" with options 3, 5 and 7 and no suggestion (the user can type another number). Accept their number. No negotiation.

### 2. Before asking anything

Gather what you already know — the user's description, the codebase context, any prior docs. **Facts are your job.** Never spend a question on something the code or environment can answer. Read files, grep, dispatch a subagent if needed. Every question you burn on a fact you could have looked up is a wasted question.

Then check for the question tool (see **Asking the user** below) and load it if it is deferred.

### 3. Ask question 1

Pick the single question whose answer would change the most about what you'd build or do. This is the question where, if your default assumption is wrong, the cost is highest.

Ask it as one call to the question tool:

```
header:   "Q1/N <topic>"   (12 characters at most, e.g. "Q1/5 Scope")
question: [one to three sentences. Concrete, not abstract.]
options:  2–4 concrete answers. Each label is short; each description says what
          choosing it would mean for the work — what changes, what it costs,
          what it rules out. None is marked recommended.
```

Wait for the user's answer. A click on an option is a complete answer; so is their own words under "Other".

### 4. Ask questions 2 through N

Each question is chosen **after** hearing the previous answer. Do not pre-plan the full list — the user's answers reshape what matters most.

Selection heuristic for each question, in priority order:

1. **Test the riskiest unsaid assumption.** What are you assuming that the user hasn't confirmed, where being wrong would waste the most work?
2. **Resolve ambiguity.** Where does the user's description permit two interpretations that lead to meaningfully different implementations?
3. **Surface scope boundaries.** What might the user expect that isn't in their description, or not expect that you'd include by default?
4. **Expose hidden constraints.** Timeline, compatibility, audience, dependencies — things that change the shape of the solution but aren't stated.

After each answer, mentally re-rank the remaining candidates. The question that was #2 before the last answer may no longer matter; a new question may have emerged from what the user just said.

### 5. Close

After question N, summarize the alignment in a compact block:

```
**Aligned on:**
- [decision 1]
- [decision 2]
- ...

**Assumptions (not asked, using safe defaults):**
- [anything material you're still assuming]
```

Then state what you'd do next and let the user confirm or redirect.

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

- **Sequential, not batched.** Each question depends on the previous answer. Asking 5 at once confuses the user and defeats the purpose — you can't adapt question 3 based on the answer to question 2.
- **No recommended option.** A recommendation anchors the user, and their own judgment is what alignment is testing. The options' descriptions carry the trade-offs instead, so the user can still answer with one click.
- **No filler questions.** N is the user's budget. A question that doesn't change what you'd build is a waste. If you've run out of high-value questions before N, say so: "I'm aligned after Q3 — the remaining questions wouldn't change the approach. Ready to proceed."
- **No facts as questions.** "What framework does this project use?" is a lookup, not a question. Do the lookup.
- **No leading questions.** "Don't you think we should use X?" is not alignment — it's lobbying. Ask the genuine decision: "X or Y?", each option with what it costs.
- **Stop means stop.** If the user says "enough" or "just go" before question N, proceed immediately. List the remaining assumptions with safe defaults in the close block.
