---
name: writing-review
description: >-
  Review technical writing for AI-writing habits and fix what fails: sentences that carry no fact,
  stock contrast ("X, not Y"), adjectives with no evidence behind them, claims that no longer match
  the code, rotating terms, and LLM cadence (Additionally, delve, em-dash asides, bold labels). Durable
  docs also go to a cold reader who sees only the text. Each finding comes with a plain rewrite, and
  rewrites never invent a number. Use when the user says "review this writing", "review the docs",
  "does this read like AI", "deslop this", "tighten this doc", "make this less AI-sounding", "cold read
  this", "/writing-review", or wants a README, design doc, plan, PR description, report, docstring or
  any other prose an agent wrote checked before it is committed, posted or published, even if they
  don't say "review". For technical prose; blog and social posts have their own voice rules.
argument-hint: "[files, folder, --since <git ref>, or pasted text] [fix]"
---

# Writing Review

Find and remove the habits that make agent-written prose longer and vaguer than the facts behind it.
The rules, with examples, are in [references/rules.md](references/rules.md). Read it at the start of
every review. Scope for now is technical writing: docs, READMEs, design and plan docs, PR descriptions,
reports, docstrings, comments, and messages about technical work.

## Iron Law

```
DELETE FIRST. A REWRITE USES ONLY FACTS YOU CAN POINT TO.
```

Most findings are fixed by deleting. When a rewrite needs a number or a name, take it from the text,
the repo, or a file the text cites. If there is none, the fix is "We have not measured X", a narrower
claim, or a deletion, plus a question to the author. An invented "latency fell 18%" is worse than the
adjective it replaced: it reads as evidence.

## Process

### 1. Scope

- The text: the files or folder named; `--since <ref>` for the prose changed on a branch (review the
  changed lines, read the rest for context); pasted text; or, with nothing named, the prose this
  session just wrote. A folder means its prose files (`.md`, `.rst`, `.txt` and similar). Docstrings
  and comments are in scope when the user names code files.
- The reader: who reads it and what they already know. Take it from the request or from where the
  file lives (a README: someone new to the repo; a design doc: the team; a dev guide: contributors).
  Ask only when neither settles it.
- Durable or passing: a doc, README, design doc, report, PR description or public docstring must
  stand alone and gets every step. A chat reply, Slack message or commit message skips the cold
  reader (step 5) unless the user asks for it.
- Review or fix: review is the default. Fix when the user says "fix", "clean up", "rewrite",
  "deslop", or passes `fix`.

### 2. Scan

Run the bundled scanner. The path is relative to this skill's base directory:

```bash
uv run --no-project python <skill-dir>/scripts/scan.py <files or folder>
uv run --no-project python <skill-dir>/scripts/scan.py --since origin/main
```

The second form scans only lines added or changed since the ref, in every changed or untracked prose
file. For pasted text, write it to a scratch file and scan that, so findings have line numbers. The
script needs only the standard library, so `python3` works where `uv` is missing.

Each hit is a candidate. Judge it in context: "has not run" states a fact, "significant" next to a
p-value is evidence, an em-dash inside a quoted error message is not the author's. The scanner sees
words only. Steps 3 and 4 find the rest.

### 3. Read

Read the whole text once against the rules. Then go paragraph by paragraph:
- Name the result, setup, decision, constraint or caveat it carries. If there is none, delete the
  paragraph or rewrite it around one.
- Put each sentence through the four sentence questions in the rules.
- Track the term used for each object. Flag rotation (`term`).
- Look for what the scanner can't see: adjective trios, forced lists of three, paragraphs that restate
  a table or heading, future-work sections with no owner.

### 4. Check claims against the source

This step catches text that is wrong, which matters more than text that is long. For each concrete
claim:
- A function, class, flag, config key, path or command: search the repo. Confirm it exists and does
  what the text says.
- A number: find it in the table, results file or log the text cites. No source: tag it `evidence`.
- A described behaviour (a default, an ordering, what runs when): read the code path.

A claim the repo can't confirm (no code for it, or a system you can't reach) is tagged `evidence`,
with what you searched. Don't guess.

### 5. Cold reader (durable text only)

A reader who gets the text and nothing else: no conversation, notes, diff or author intent. You and
the author both know things the text never says, so neither of you can find those gaps.

- Reviewer: if the user's or project's instructions name a model or command for independent reviews,
  use it, and where they size the effort by a diff, use the draft's line count. Otherwise spawn a
  fresh general-purpose subagent.
- Isolation: copy the draft alone to `draft.md` in an empty scratch folder and run the reviewer there
  (a command-line reviewer read-only, with that folder as its working directory), so it can't read the
  repo. Keep the brief and the answer file outside that folder. The folder is not a git repo, so pass
  the flag that lets the reviewer run outside one (for Codex, `--skip-git-repo-check`).
- Run it in the background and draft the report while it reads. Finish the report once it answers.
- The brief, word for word apart from the brackets:

```
You are reading this document for the first time. Audience: [the reader from step 1].
Read only draft.md. Do not open other files.

List what a reader in that audience cannot work out from the text alone:
- terms used without a definition this reader may need
- unclear referents ("this", "the fix", "the old path")
- claims the text gives no support for
- missing steps or causal links
For each, quote the passage and say in one line what is missing.
Do not suggest style changes. Do not summarise the document. Stay under 300 words.
```

Keep only concrete gaps and tag them `cold`. Each fix is the smallest local edit: define the term,
name the referent, narrow the claim, or link the background. Drop findings that are style
preferences or that ask for history the audience doesn't need.

### 6. Report

One block per file. Order findings by tag, most serious first: `stale` (wrong text misleads),
`evidence`, `cold`, `empty`, `contrast`, `term`, `plain`, `cadence`. One line each, with the rewrite.
When several findings hit the same sentence, merge them into one finding that lists every tag and
gives one rewrite that fixes them all.

```
README.md: 9 findings, 1 needs your facts

1. L41 [stale] "`--dedup` defaults to exact matching" → "`--dedup` defaults to `minhash`." (src/dedup/cli.py:22)
2. L12 [evidence] "significantly faster": no number in the doc or repo. Question 1 below.
3. L5 [cold] "the old path" is never named → "the per-file dedup path (removed in v0.3)"
4. L8 [empty] "It is worth noting that all shards share one tokenizer." → "All shards share one tokenizer."
5. L20-23 [empty] paragraph restates the table below it → delete
6. L30 [contrast] "The bottleneck isn't the GPU, it's the data loader." → "The data loader is the bottleneck."
...

Questions
1. L12: what speedup did you measure, and with what setup? With no answer: "We have not benchmarked the new sampler."
```

Each finding that needs facts gets a fallback for when the author has none. In a doc for users (a
README, a guide), deleting the claim usually serves the reader better. In a design doc, report or
PR description, state the unknown ("We have not measured X").

The report follows the rules too: no praise, no recap, no verdict on the doc as a whole.

The fact questions stay in the report as a numbered list; the user answers them in free text, in any
reply. In review mode, then ask one question through the question tool: apply all (with the answers
given and the fallbacks for the rest); apply all except those that need facts; apply a set the user
names by number; apply none.

### 7. Apply

On the user's yes, or straight after the report in fix mode:
- Make the smallest local edits, in place. Keep the author's structure, headings and terms unless a
  finding targets them. If the doc needs restructuring, say so in one line and do it only on request.
- For findings that need facts, use the user's answer. With no answer, apply the fallback in the
  finding. Leave no placeholders in the file.
- Final sweep: rescan the edited files and reread each edited paragraph. Edits bring in stock
  phrases too.
- Tell the user what was applied, what was skipped and why, word count before and after (`wc -w`),
  and any open questions.
- Don't commit. If the user asks for a commit, go through the `commit` skill.

## Asking the user

- One question per message, through the question tool (`AskUserQuestion`; load it with ToolSearch if
  it is deferred). With no tool, ask in plain text with lettered options.
- No recommended option. Each option's description says what choosing it changes.
- Ask only what the text and the repo can't answer: the reader when nothing settles it, the facts
  behind `evidence` findings (listed in the report, answered in free text), and whether to apply.

## Red flags

| Thought | Reality |
| --- | --- |
| "This rewrite reads better with a number; I'll estimate one" | An invented number reads as evidence. Ask, write the unknown, or delete. |
| "Every 'not' is stock contrast" | A negation that states a fact stays: "The ablation has not run." |
| "The cold reader needs some background to be useful" | Then it is no longer cold. Send the draft and the audience only. |
| "The cold reader wants more context everywhere" | Fix the concrete gaps with small edits or a link. Extra context buries the main claim. |
| "This doc should be restructured" | Findings are local edits. Propose a restructure in one line. |
| "I prefer sentence-case headings" | A personal preference is not a finding. Flag only what the rules cover. |
| "The scanner found nothing, so the text is clean" | The scanner sees words. Empty paragraphs, stale claims and rotating terms need steps 3 and 4. |
| "It's a short doc; skip the claim check" | One wrong default in a README costs more than the check. |
