---
name: experiment-analyse
description: >-
  Read an ML experiment round's results against its frozen design: check the arms ran as planned, compute the
  planned measures from saved files by code, set the user's predictions and the forecast beside the actuals, and
  name the outcome of the design's Answer that holds. Use whenever an experiment's runs or pilot have landed, or
  the user says "what did we get", "analyse the results", "analyze the results", "did it clear the bar", "how
  did the runs do", "compare the arms", "/experiment-analyse", "/experiment-analyze", or wants saved results
  re-read.
argument-hint: "[path to the round design, its study folder or its run plan]"
---

# Experiment Analysis

Read what a round produced against what its **round design** said before the run, and name the **Answer** outcome that holds. `/flow:experiment-close` records the user's decision on it; `experiment-analyse` never takes it.

**Output:**
- **Results**, appended below the freeze line of the round design, wherever it lives, from [templates/results.md](templates/results.md).
- A numbers file: every number Results cites, written by the analysis code, with the files it read and the command that wrote it. Aggregates only. By default beside the round design, named after it (`rounds/<YYYY-MM-DD>-<round-slug>.numbers.json`), or where the project's instructions keep results. If the project already writes one for these runs, cite it and write only the numbers it lacks.
- The measured numbers in the project record (wherever the project's instructions put them), under new ids that Results cites. The study index is `/flow:experiment-close`'s.

## Iron Law

```
THE PLANNED MEASURES FIRST, AS THE DESIGN DEFINES THEM, FROM FILES BY CODE. NOTHING CHOSEN AFTER LOOKING DECIDES THIS ROUND'S BAR.
```

A measure picked after seeing the numbers can turn any result into a win, and a number typed from memory cannot be checked. The frozen **Answer** says what "clears" means. The rest, apart from the go before scoring a sealed test, is guidance: scale it to the spend, and let the user waive any item in one line, written into Results.

## Process

### 1. Read the design; check the arms are comparable

- **The round design:** the path passed in (a run plan leads to it through `references:`), else the study's latest round. Read **Hypothesis and predictions**, **Design**, **Answer**, **Forecast** and **Amendments**, then the run plan in `run_plan:`: each arm's disposition, and the `Impl note:` lines with actual time and compute. Take the record and its ids, the budget unit and the data rules from the project's instructions.
- **Entered midway:** a hand-written design, or a run plan made with no round design, stands in where it lives. Append Results to it; stop for nothing it lacks. With no Answer, the outcome is read in the question's own words, with "no Answer on record". With no bar, a bar the project's record already carries may be used, named as such.
- **Before any number,** check each arm against the arms table from the run's own logs and configs, not the plan: code state, settings, data. List the arms missing, failed or changed, and which comparisons each one breaks. Two arms that differ in a second thing are never compared without saying so.

### 2. A pilot or a partial set

If a pilot or some arms have landed with others still to run, write a dated Results entry: what ran, the measured rates against the forecast, the corrected forecast. Leave the status alone, and read nothing against the bar unless the design's **Order** reads this result (then steps 3 to 6 apply to it). Then stop: "Next is `/flow:experiment-run <run plan>`, which carries on."

### 3. The planned measures (forced)

Compute each measure as **Design** defines it (weighting, pairing, interval method) with code that reads the saved outputs (per-item scores, timings, logs). Use the project's analysis helpers where they exist; put new code where the project keeps analysis code, so the numbers can be rerun. Every number in Results comes from that code's output, never from memory, a log tail or the chat. Scoring a sealed test set is a gate: ask for the user's go unless a go already named it, and score only the model, checkpoint and threshold frozen beforehand.

### 4. The checks that fit

Apply the rows that fit this round; skip the rest without a word.

| Check | Fits | Guards against |
| --- | --- | --- |
| Each seed or repeat, their spread, then the average | anything run more than once; a single run whose step is near its own noise (checkpoint swings, earlier seed pairs in the record) | a bar read on an average that one seed misses; a gain no bigger than seed noise. Intervals over items leave out seed variance. Averaging per-item predictions makes an ensemble; averaging per-seed metrics summarises runs: say which |
| Paired intervals over the sampled unit | arms scored on the same items | intervals over rows or tokens when documents, users or prompts are what varies, which come out too narrow |
| Each group, with its count of independent items | the bar or the design names groups | an overall gain that hides a loss in one group, or a group decided by a few items |
| The share of the measure the ten largest items carry | losses, weighted measures, items of very different size | a measure carried by a handful of items |
| The bar at a threshold and checkpoint frozen beforehand | an absolute bar read at an operating point; anything scored on a sealed test. Not a step between arms scored the same way | a threshold picked on the data it is scored on, which overstates |

### 5. Predicted against actual

One table, nothing edited to agree. Rows: the result, wall, compute, and money where the project states a rate. Columns: the user's prediction, the forecast, the actual, and the gap with a one-line reason. One more row: did the round test the hypothesis's reason (held or failed), or only its number. With no prediction on record, one line says so, and the table holds forecast against actual only.

### 6. The outcome

Name the **Answer** outcome that holds, in its words, and what it says to do. "Clears" means what the Answer says: a point estimate, if that is what it set; where it reads an interval, one that spans the bar is "can't tell". An interval that spans zero reads "not distinguishable", never "the same" or "level": say what it rules out.

✅ "20k against 10k, macro-F1 Δ −0.4 to +1.1 points: not distinguishable. A gain above 1.1 points is ruled out; a smaller one is not."
❌ "20k and 10k are level." It claims an equality the interval cannot show, and a gain of up to a point gets dropped on it.

A check does not change what the Answer says, but it can show the planned measure cannot decide (a handful of items carry it). Then say so; a measure the design named alongside may decide, and the outcome names it. A better measure found now is the next round's bar.

### 7. Exploratory findings

Label a finding "(exploratory)" only when it supports a claim and was chosen after the numbers were seen. Say it once, where it is used, with the round that would test it. A diagnostic that explains why a planned measure failed is a check, not a claim. Examples of errors show what an aggregate hides; keep them out of the round design, the record and commits unless the project's data rules allow them there.

### 8. Write

- **Results**, from the template, as a dated entry. Set the design's `status: answered` once every arm is read or dropped, adding the line in place if it has none; a `closed` round stays closed, and a run plan standing in keeps its own status. A later reading (a re-analysis, a review's correction) is a new entry naming what it replaces; the earlier entry and the numbers it cites stay, so a later entry writes its numbers beside them, never over them.
- **The numbers file**, written by the step 3 code.
- **The project record**, now, not later.
- If `thoughts/` or the record is tracked by git, commit through the `commit` skill with no AI attribution, when the project's instructions allow it.

### 9. Tell the user

- The outcome in two lines, with its numbers and intervals.
- What surprised: the biggest gap against the prediction, and any exploratory finding worth a round.
- Candidate next rounds, one line each: what it would tell us and roughly what it costs. They are the user's call.
- "Next is `/flow:experiment-close`, which records your decision." If a claim is about to be adopted (a model frozen, a recipe changed, a number published), offer `/flow:experiment-review` in result mode first, in the same line.

## Asking the user

This skill asks little: the go before scoring a sealed test. A missing or changed arm is reported in Results with the comparisons it breaks, not asked about. Questions go one at a time, through the question tool (`AskUserQuestion`; load it with ToolSearch if deferred; with none, plain text with lettered options). No recommended option: each option says what choosing it means for the reading.
