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
EVERY QUESTION MUST HAVE A RECOMMENDED ANSWER — THE USER CAN ACCEPT WITH ONE WORD
```

## Process

### 1. Set N

The user passes N as the argument (e.g. `/flow:align 5`). If no number, ask once: "How many questions? I'd suggest 3–5 for this." Accept their number. No negotiation.

### 2. Before asking anything

Gather what you already know — the user's description, the codebase context, any prior docs. **Facts are your job.** Never spend a question on something the code or environment can answer. Read files, grep, dispatch a subagent if needed. Every question you burn on a fact you could have looked up is a wasted question.

### 3. Ask question 1

Pick the single question whose answer would change the most about what you'd build or do. This is the question where, if your default assumption is wrong, the cost is highest.

Format:

```
**Q1/N — [short title]**

[The question — one to three sentences. Concrete, not abstract.]

Recommended: [your best guess + one-line rationale]
```

Wait for the user's answer. One word ("yes", "go with that", "no, actually X") is a complete answer.

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

## Rules

- **Sequential, not batched.** Each question depends on the previous answer. Asking 5 at once defeats the purpose — you can't adapt question 3 based on the answer to question 2.
- **Recommended answer on every question.** The user should never have to think from scratch. Your recommendation is a draft they edit, not a blank they fill.
- **No filler questions.** N is the user's budget. A question that doesn't change what you'd build is a waste. If you've run out of high-value questions before N, say so: "I'm aligned after Q3 — the remaining questions wouldn't change the approach. Ready to proceed."
- **No facts as questions.** "What framework does this project use?" is a lookup, not a question. Do the lookup.
- **No leading questions.** "Don't you think we should use X?" is not alignment — it's lobbying. Ask the genuine decision: "X or Y? I'd go with X because Z."
- **Stop means stop.** If the user says "enough" or "just go" before question N, proceed immediately. List the remaining assumptions with safe defaults in the close block.
