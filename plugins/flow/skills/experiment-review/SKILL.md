---
name: experiment-review
description: >-
  Get an independent review of an ML experiment: a neutral brief that gives the reviewer the evidence and never
  our conclusion, every finding checked before anyone acts, and a disposition table kept with the study. Three
  kinds: pre-launch (a round design and its run plan, before compute is spent), result (the claims, recomputed)
  and directions (several models rank what to run next). Required before launch only when the round design says
  so. Use when the user says "review the experiment", "get a review of this design", "ask Codex about these
  results", "adversarial review", "second opinion", "poke holes in this", "double-check these results", "ask
  other models what to try next", "/experiment-review", or when a study is stuck. For a code change, the review
  is part of /flow:pr.
argument-hint: "[prelaunch | result | directions, or two of them] [path to a round design, a report or a study folder]"
---

# Experiment Review

Get a cold read of a round, its results or a whole study from a model that did not design or run it. This is `/flow:pr`'s review (a cold reviewer, every finding verified, then act) applied to an experiment. It hands back to wherever the round stands: `/flow:experiment-plan` or `/flow:experiment-run` before launch, `/flow:experiment-close` after a result, `/flow:experiment-design` for a new round.

**Required:** a pre-launch review, before the first billed launch, when the round design's Forecast ends "Review before launch: required". `/flow:experiment-design` writes that line against the review threshold (the project's or the user's instructions set it; default 200k in the currency the project budgets in); a design without the line needs no review. The user can waive a required review in one line, under **Amendments**. Otherwise a review is the user's call: offer it at most once.

**Output:** `<repo-root>/thoughts/studies/<study>/reviews/<YYYY-MM-DD>-<round-slug>-<mode>.md`, dated today, from [templates/review.md](templates/review.md): the disposition table, and the paths of the brief and of each answer, kept as files beside it. `<mode>` is `prelaunch`, `result` or `directions`; two in one request make one review record, named with both (`-result-directions`).

## Iron Law

```
THE REVIEWER GETS THE EVIDENCE, NEVER OUR CONCLUSION. NO FINDING IS ACTED ON UNTIL IT IS CHECKED.
```

Only the user can lift the first half, by saying to send a document as it is (step 2). Everything else scales with the spend, and the user can waive any of it in one line, noted in the review record: a second opinion on a cheap round can be one reviewer and a three-row table.

## Process

### 1. The round, the mode, the reviewer

- **The round:** the path passed in, or the study's latest round. Read its round design and run plan (for directions, every round in the study) and the project's data rules. A design written by hand, a report, or results with no round design: review what exists, where it lives. The review record goes in the study's `reviews/`; with no study, in a new `thoughts/studies/<YYYY-MM-DD>-<study-slug>/reviews/`.
- **The mode:** from the request; else from the round's status: `frozen` with nothing run is pre-launch, `answered` is result, a stuck study or "what next" is directions. Ask only if neither settles it. Modes combine: a request for a result review and directions is one brief in two parts, run once per reviewer, with one review record.
- **The reviewer:** the project's or the user's instructions name it and say how to run it; if they do not, ask once. Directions normally takes several models, the same brief to each.

### 2. Write the brief

Write it to a file, from the brief skeleton in the template.
- **Send:** the question and the decision it feeds; the design, with its bar and the Answer written before the run; factual amendments; the measured results, with the files, code and commands that made them; what the reviewer cannot reach (a remote store, a tracker), pasted as facts; the user's settled decisions from **Aligned**, marked "do not reopen", with leave to say what each costs; on a re-review, the findings already checked and declined, with the reason.
- **Withhold, wherever it occurs** (the design, Amendments, Results, a report, the index's Next): hypotheses, predictions, the outcome we read and other interpretations, proposed next rounds, and any request to confirm. A reviewer handed our reading checks the reading, not the evidence. Paste what is sent, or name the files and sections to read and those to leave; copy the evidence to a folder of its own only when the two cannot be told apart.
- **The user's instruction wins.** If they say to send the report or the design as it is, send it (in result mode, in place of the numbered claims), say so in the brief's header, and ask also for its sentences to be checked against its own tables.
- **Data rules:** a reviewer sends what it reads to its provider. Point it only at what the project's data rules allow out, with examples stripped.

| Mode | Also gets | Asked to |
| --- | --- | --- |
| pre-launch | the run plan, if written; the measured rates behind the forecast; the project's instructions | find confounds and missing or needless arms; say whether the evaluation can decide the bar, whether the forecast is realistic, what fails first, and what breaks the project's rules |
| result | the claims, numbered, each a plain sentence with its number and its source | assume something is wrong; recompute each claim from the files; say which claims the design's measures and bar support |
| directions | each round's question, design and measured results; the budget | critique the study; rank next rounds, each with what it would tell and its cost; say what not to do |

✅ "3. Final validation loss, wu-2000 minus wu-500, paired by seed: −0.011 (90% interval −0.016 to −0.006). `results/compare.json`, from `analysis/compare.py`."
❌ "The longer warmup clearly helps. Can you confirm the analysis is sound?" It hands over the conclusion and asks for agreement.

### 3. Run it

Run each reviewer in the background, with the instructions' settings or through the tool the user names (for a command-line reviewer: read-only, the brief from its file, the answer to a file), and read each answer when it lands. Where the settings assume a diff and there is none (an effort set by its size), choose, and say which in one line. If a named reviewer fails to start, tell the user: another model is their call.

### 4. Check every finding (forced)

Before anyone acts on a finding, check it against the evidence: open the file and line it cites, rerun the number, read the code. Verdict: valid; or partly wrong, wrong or not verifiable, each with its reason (for the last, what would verify it). Agreement between reviewers is not verification: models share misreadings, and a fix built on a wrong finding can break the run. The same finding from several reviewers is one row with all their letters.

### 5. Write the review record

From the template. Keep the brief and each answer as files beside the review record, or where the project's data rules keep files that quote data, and give their paths; never paste long answers in. Directions mode adds the directions merged and ranked, who backs each, and a **Not to do** list. A wrong finding keeps its row and its reason, so a re-review can list it as declined.

### 6. Act on what holds

- **An error** (a number computed wrong, a claim the files do not support): in Results, correct it through `/flow:experiment-analyse`, as a new entry that names the review. In the project record or a report, correct it where it is written.
- **Changes to the design** (an arm, the data, a measure, the budget): the user's call. Put them all as one question, a multi-select with each change's cost (past four, a numbered list answered in one reply). For each yes: one line under **Amendments** (date, what, why: the review's finding, and what had been seen), and the run plan edited to match.
- **A change to the question or the bar:** a new round, through `/flow:experiment-design`.
- **Not acted on now:** status open, with what would close it.

Then fill in each row's status, and if `thoughts/` is tracked by git, commit through the `commit` skill, with no AI attribution.

### 7. Tell the user

Blockers first: each finding that held and what was done about it; then the wrong ones, a line each on why; then what is open. End with the next skill: after a pre-launch review, `/flow:experiment-plan`, or `/flow:experiment-run` if the run plan is signed; after result mode, `/flow:experiment-close`; after directions, `/flow:experiment-design` for the round the user picks.

## Asking the user

- One question per message, through the question tool (`AskUserQuestion`; load it with ToolSearch if deferred). With none, ask in plain text with lettered options.
- No recommended option. Each option's description says what choosing it means for the round: what it changes, costs or rules out. If the user asks what you would pick, answer.
- Ask only what the files and the request cannot answer: the reviewer when none is named, the mode when nothing settles it, and the design changes a review proposes, all in one question (step 6).
