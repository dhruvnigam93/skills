---
name: experiment-design
description: >-
  Design one round of an ML experiment before any compute is spent: one question, the user's own hypothesis and
  predictions of result, time and cost on record before any forecast, the smallest design that answers, and how
  each outcome will be read; then freeze it. Use whenever the user has an idea or hypothesis to test, says
  "design an experiment", "why not try X", "let's test whether", "what should we run to find out", "the next
  round", "/experiment-design", brings a question from a meeting, or dictates an ablation, fine-tune, benchmark,
  sweep, data or labelling study, even without the word "design". Also brings a hand-written experiment design
  into shape. For experiments it takes the place of /flow:prd and /flow:design, which are for software features.
argument-hint: "[the idea or question, or a path to a study folder or a hand-written design]"
---

# Experiment Design

Turn an idea into one **round design**: one question, the user's own hypothesis and predictions, the smallest design that answers it, and how the result will be read, all written before the run and frozen at sign-off, so the result is read against what was expected, not against what was hoped. `/flow:experiment-plan` turns it into a run plan; `experiment-design` never writes run code or launches anything.

Start the page from [templates/round-design.md](templates/round-design.md) as soon as the study is found (`status: draft`), or take up a design written by hand where it lives (step 1), and fill each section as a step settles it: facts from the record, decisions from the user, predictions from the user alone, the forecast from measured rates.

**Output:** under `<repo-root>/thoughts/studies/<YYYY-MM-DD>-<study-slug>/` (`<repo-root>` = `git rev-parse --show-toplevel`; the date is the day the study's first round began). Create the directories if missing; leave other files in a study folder alone.
- `rounds/<YYYY-MM-DD>-<round-slug>.md`: the round design, dated today. A design written by hand stays where it is (step 1).
- `README.md`: the study index, from [templates/study-index.md](templates/study-index.md), one row per round.

## Iron Law

```
ONE QUESTION. THE USER'S HYPOTHESIS AND PREDICTIONS BEFORE YOUR FORECAST. THE ANSWER BEFORE THE RUN.
```

Sign-off waits for all three, and "enough" or "just go" waives none of them. Everything else here is guidance: scale it to the spend, and let the user waive any item in one line, written into the design.

## Process

### 1. Read before asking

- **The study:** the folder passed in, or the one under `thoughts/studies/` on the same topic. None matches: a new study. More than one: ask which. Read its index, the earlier rounds (Results and Decision first), the project record (wherever the project's instructions put measured numbers and decisions) and any notes or thread the user points at.
- **What the design will lean on:** the data and intermediates already built, the trainer's schedule and defaults, the evaluation set and its size per group, which runs saved models and per-item scores, the measured rates in the record.
- **Facts are your job.** Never ask what a file, a config or the record can answer.
- **Project specifics come from the project:** the budget unit and any rate that turns it into money, the data rules (what may be written into `thoughts/`), the review threshold, launchers and limits. Invent none of them.
- **Entered midway:** a design written by hand is the round design, where it lives. Keep its words, add the frontmatter and only the sections it lacks, in place, link it from the index, and ask only for what is missing. Move it only if the user asks. One page per round, never a copy.

### 2. Can what exists answer it?

If saved runs, scores or checkpoints answer the question, or a re-analysis of them would, say so with the numbers and where they live, offer the re-analysis through `/flow:experiment-analyse`, and stop. If they answer part of it, the round shrinks to the rest. What is known goes under **Context**, with pointers into the record and the reference to beat.

### 3. One question (forced)

Write the dump back as the separate questions it holds, one sentence each, each naming its measure (when the dump gives one) and the decision it feeds. Test: if answering X would be useful without answering Y, they are two rounds, unless X and Y are arms that share the data, the measure and the decision: those are one question.

✅ Dump: "Get the intent classifier to 20k labelled examples, try the bigger encoder too, and see if label smoothing helps." Three rounds. The first: "On the current encoder, does macro-F1 still rise from 10k to 20k training examples?" It decides whether to buy more labels.
❌ "How do more data, a bigger encoder and label smoothing change the classifier?" No gain can be traced to its cause.

If the dump makes plain which question this round answers, state it back as one sentence and let the user correct it. If not, the user picks: describe each option by what it would decide and what it needs, not by your forecast, which waits for step 9. The other questions are parked under **Next** in the index (step 10).

### 4. The user's hypothesis and predictions, before anything of yours (forced)

Before you show any forecast, estimate or view of the outcome, ask in one plain-text message, with no options (an option with a number in it puts your number in their mouth): the **hypothesis**, what they expect and why; the **predicted result** on the question's measure (in its own terms if it names none), and how sure they are; the **predicted time and cost**, wall-clock and compute, and money if they think in it. Quote what the dump already says and ask only for the rest. Show the numbers the record already holds for the comparison (the current best, earlier rounds) with the ask: they are facts, not your view. For many arms, ask for the shape of the result and a number at the cells that decide.

Write the answers under **Hypothesis and predictions** in their words and figures, dated. A vague answer, "no idea" or "you tell me" gets one follow-up, also one message: the widest range they would bet on, and how sure. A wide range with low confidence is an answer; a blank is not. The rest of the design goes on meanwhile; the forecast and the sign-off wait until the predictions are on record. If alignment adds an arm or changes the measure, ask for their prediction on it too, still before the forecast. If any result of this round has been seen, write what next to the date.

```
✅ "Labels are still the limit, so 20k beats 10k by 1 to 3 points of macro-F1; 60% sure.
   A day, about 8 GPU-hours."
❌ Agent: "Probably +2 points for about 6 GPU-hours?" User: "Sure." That is your forecast
   with their name on it.
```

### 5. Align, costliest wrong guess first

Ask until every part of **Design** is confirmed or marked assumed, choosing each question after the last answer. The usual order, by what a wrong guess wastes:
1. **The comparison:** what differs between arms and what is held fixed. Name the hidden variable: same steps or same epochs, same tokens or same documents, same compute or same data. Leaving it open is the commonest cause of a second study.
2. **The bar:** the measure, the number, the groups it is judged on, and what "clears" means.
3. **The evaluation:** which set, how many independent items per group, held out how.
4. **The reference** to beat, and whether it is still the current best.
5. **Seeds or repeats, the budget, and what is cut.**

✅ header "Fixed", question "The 20k arm has twice the data. Same number of steps, or same number of epochs?", options **Same steps** (equal compute; each example seen half as often; asks whether more data helps at a fixed cost) and **Same epochs** (twice the compute; asks whether more data helps if we pay for it).
❌ "Which learning rate does the trainer use?" A lookup: read the config.

Write each settled point under **Aligned**, dated. What the record or the dump settles without a question goes there too, marked "(assumed)" with its basis. Stop when no remaining question would change an arm, the bar, the evaluation or the budget, and say so. On "enough", fill the rest with safe defaults marked "(assumed)", in plain sight.

**Push back on a wrong premise** before the next question, with the pointer (a file and line, a record entry, a two-line calculation), then ask which holds: "The schedule decays the rate to zero in every run, so any single run flattens at its end; only separate runs at 10k and 20k can show saturation." Never build on the premise silently, and never adopt your side silently either. Define a term the first time you use it (paired interval, effective sample size): the user decides on what they understand.

### 6. Readiness checks

Answer each in the Design line named below, or write the user's waiver under **Aligned** as "(waived, user)". Each exists because, missed, it forced a rerun after the money was spent. A cheap round may answer most with "not checked" and a line under **Limits**.

| Check | Line | It says |
| --- | --- | --- |
| The evaluation can decide the bar | Data and evaluation | enough independent items per group (count the unit that varies: documents, users, sources, not rows); the share the ten largest items carry, computed from saved per-item scores when they exist |
| The effect is larger than noise | Seeds and repeats | the run-to-run spread against the effect expected, and enough seeds or repeats to tell them apart; with no measured spread, the effect this round cannot separate |
| The arms differ in one thing | Arms | the one thing; everything else fixed |
| The evaluation matches where the result is used | Data and evaluation | how the evaluation set was drawn against how the real data is drawn (the unit, length caps, sources), any difference and which way it biases; no leakage at the unit that matters; thresholds and checkpoints chosen before any sealed test is scored |
| The comparison is complete | Arms | the reference is current; the cheapest obvious arm is in, or out on purpose |
| A later question needs no rerun | Saved | models, mid-run checkpoints, per-item scores |

### 7. The smallest design that answers

Cut arms, sizes, seeds and new data to the fewest that still answer the question, keeping the waivers and limits already accepted. Order the work: the cheapest informative step first; a pilot only when something is unmeasured (a new code path or configuration, an unknown rate), else cite the run that measured it; then arms that run only if an earlier result calls for them. Code or data that must exist first goes under **Needs**. List the cuts under **Limits**, each with what it would have told us and what it would have cost, and show the user the ones they did not make themselves: any comes back in a line.

### 8. The Answer (forced)

Before any run, write for each outcome what it means and what we do next: at least clears, misses and can't tell, or the question's own words for them ("still rising", "flat"). Can't tell: the interval spans the bar; where there is no interval, or it leaves out seed noise (one seed), it is a gap smaller than the noise you can measure: name that size, or say it is unmeasured. Plan for it; noise makes it common. Written now, no result can be read as a win after the fact.

### 9. The forecast, only now

Write it only once the predictions are on record; until then, say it waits on them. One row per step that bills real compute: wall, compute, money where the project states a rate (never invent a price), and the basis, a measured rate from the record and the arithmetic. A row with no measured rate says "guess" and names what will measure it. Give the total against the budget and the point to stop and look: a run past 1.5x its forecast.

End with "Review before launch: required" or "not required", with the total against the review threshold (the project's or the user's instructions set it; default 200k in the currency the project budgets in). With no rate to turn the forecast into money: "Review before launch: not required: no rate to compare against the threshold". The user can waive a required review in one line, under **Amendments**.

Show the forecast beside the user's prediction and never edit either to agree. Where they differ widely, say so in one line and ask whether it changes the design: one of the two misses something.

### 10. Self-review, then sign-off

Read the page fresh and fix inline:
1. One question; the Answer gives every outcome an action, "can't tell" included.
2. Hypothesis and predictions in the user's words, with figures for result, time and cost, on record before the forecast.
3. The bar names a measure, a number and groups; the arms differ in one thing, or the departure is under **Limits**.
4. Every Design line is in Aligned or marked assumed; every readiness check has its line or a waiver; every forecast row has a basis; the review line is there.
5. No placeholders and no padding (a small round is as short as the template's example), and nothing the project's data rules keep out of files.

Present the question, the predictions beside the forecast, the arms, the bar, the Answer, the cuts and every "(assumed)" line, so sign-off covers the defaults too, and ask for sign-off as one question through the question tool. Words that approve the page as shown ("ok, let's do it", "go ahead") are the sign-off whenever they come: do not ask again. Revise until it comes; sign-off is the only exit. On sign-off:
1. Set `status: frozen` and `frozen:` to today. From then on a design change is one line under **Amendments** (date, what, why, what had been seen); a new question or bar is a new round.
2. Add the round's row to the index with "—" in Answer and Decision, and park the other questions under Next. A study with no index gets one with this round's row; earlier documents (as plain links) and record ids go under one line, "Earlier work", and their rows are not reconstructed unless the user asks.
3. If `thoughts/` is tracked by git, commit the round design and the index through the `commit` skill, with no AI attribution. If it is ignored, the status alone marks the freeze.
4. Tell the user: "Round design frozen. Review before launch: <required, through a pre-launch `/flow:experiment-review` | not required>. Next is `/flow:experiment-plan`, which turns it into a run plan." If their request already asked for the run, go straight on to `/flow:experiment-plan`.

## Asking the user

- One question per message, through the question tool (`AskUserQuestion`; load it with ToolSearch if deferred). With none, ask in plain text with lettered options.
- No recommended option: never label, order or argue for one. Each option's description says what choosing it means for the round: what it changes, answers or rules out. If the user asks what you would pick, answer.
- Step 4 is the exception: one plain-text message, with no options and no numbers of yours.
