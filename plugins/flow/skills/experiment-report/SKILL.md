---
name: experiment-report
description: Write up an ML experiment as a paper-style report, published as a private HTML artifact. It has a title that states the finding, an abstract, and one main table of the best candidates with intervals, paired differences, the bar and cost. Numbered sections follow (problem, data, architecture, training and evaluation, inference and systems, reproducibility), with SVG figures and a sources footer. It gives the final picture of the work, never the journey. Use it whenever the user wants to write up, report or present a study, model comparison, ablation, fine-tune, classifier, data or filter study, labelling study or benchmark ("write up the results", "make a report for the team", "experiment report", "paper-style write-up"), or to add new results to an existing report. Not for Notion team results pages, Slack or email summaries (executive-summary), or repo docs and run logs.
---

# Experiment report

Write the study the way an ML paper reads: the best candidates, how they were compared, and the results. The page is
the culmination of the work, the final and concise picture. It is not a lab notebook: nothing about the order things
were tried in, what failed on the way, or how the infrastructure was set up. A reader who stops after the title, the
abstract and Table 1 has the result; the numbered sections are there for whoever wants to check it.

The output is one HTML page, published as a private artifact. Start from `assets/report-skeleton.html`: its styles,
tables, figure classes and footer are the house style, already approved. Replace every word and number in it.

## Pick the right kind of write-up

| The user wants | Write |
| --- | --- |
| The full study, for the team to read and check | This report: private HTML artifact, infra included |
| A team results page on Notion (data runs, funnels) | Not this skill: that format opens with the funnel and leaves infra out |
| A quick answer for Slack or email | The `executive-summary` skill |
| The project's record of a run | The repo's run log and docs, aggregates only |

If you can't tell which one the user wants, ask.

## A paper, not a journey

Report only the final state:

- **The final candidates**, each in its final setup. Earlier best models show up only as baselines, with a row in a
  table and a pointer to where their numbers come from (a run-log id), never as "last round", "until now" or "we
  first tried".
- **Failed or replaced runs stay out.** They belong in the run log. When an arm uses a different setting because the
  usual one fails, say so in one line, as a fact about the method.
- **Infra as facts, not setup.** Hardware, precision, throughput, memory and cost belong in section 5, written the way
  a paper would. Orchestration does not belong anywhere: cluster names, pods, schedulers, launch scripts, restarts,
  out-of-memory stories, how long things took to set up.
- **No timeline.** No "then", "after debugging", "while the 4B was training", "this round".

| Cut | Write instead |
| --- | --- |
| We first tried lr 5e−5, but one seed collapsed, so we reran at 2e−5. | The 270M encoder uses lr 2e−5; at 5e−5 it does not train. |
| Until now the best model was the 4B decoder reading windows. | The reference is the 4B decoder reading 75-line windows (run log E-63). |
| The 1B and 4B arms ran on one 8-GPU node through SkyPilot, eight at a time. | Each run used one B200 (183 GB) in bf16. |
| After fixing a padding bug, PR AUC went up by 0.02. | (nothing: the bug is part of how the work went, not part of the result) |

## The page, top to bottom

**Header.**
- `<title>`: a short name for the study, two to four words ("Review Spam Classifier").
- Eyebrow: "Experiment report · <topic>".
- `h1`: the finding as one sentence, with the comparison in it. It is not the topic. ("A 1B bidirectional encoder
  reading whole documents matches the windowed 4B model and clears the bar.")
- Meta line: date / eval set and its size / what is left out / status (test unscored, runs pending) / seeds.

**Abstract.** One paragraph, about 150 to 300 words, in this order:
1. The task and the bar.
2. The reference.
3. What is new.
4. The same-data comparison with the headline numbers per group, and whether each contender clears the bar.
5. What explains the gain: the ablation that isolates it.
6. Cost.
7. What is not covered yet.

**Table 1: the one table.** It comes right after the abstract and holds the result on its own:
- Rows are the main contenders only, usually the best new model and the reference it has to beat. The new model's
  row is highlighted (`tr.new`). Bold follows the bold rule under Numbers: the best value in each column, whichever
  row holds it.
- Each measure is a row group (`tr.grp`), with the bar's measure first. Add a chance row (`tr.base`) where it gives
  scale, for example a random scorer's PR AUC.
- Columns are the groups the bar is judged on (languages, domains, length buckets), plus a Bar column with a
  pass or fail pill.
- Each cell holds the value, its 90% interval `[lo, hi]`, and the paired difference from the reference as a range,
  "Δ +0.034 to +0.144". The reference cell says "reference" there instead.
- The last row group is cost, one line per contender (throughput, cost for the full workload, multiple of the
  budget), on the same hardware.
- The caption says what is compared, on which data and how much of it, how the intervals were computed, and what
  "clears" means.
- When a study has more than two contenders worth comparing, keep Table 1 to the two that decide the question. Every
  other arm goes in a secondary table in section 4.

**Numbered sections**, following the deep-learning reporting guidelines. Open each subsection with its point.

1. **Study design and problem formulation.**
   - The question, in one or two sentences.
   - The problem type and the output.
   - The bar and the budget, as a definition list.
   - What the target looks like: a table of its kinds, with each kind's share and examples.
   - Easy cases and hard cases (see Examples from the data).
   - The arms: a table of backbone, attention, input and fine-tuning.
2. **Data collection and transformation.**
   - Sources and labels, including the labeller's measured quality.
   - Samples and splits, with counts and how leakage is prevented.
   - How the data is fed to each arm, with a figure when the arms differ in what they read.
   - What is left out and why, with its share of the evaluation weight.
3. **Model architecture.** The new model and the reference in words, then one SVG figure of the two side by side.
4. **Training, optimization and evaluation.**
   - A settings table for the main contenders: fine-tuning, optimizer, learning rate, loss, regularization, batches,
     steps and tokens, final training loss, seeds.
   - The measures as a definition list: weights, each measure, how intervals and paired differences are computed.
   - The results: point to Table 1, add per-seed results if the bar has to hold per seed, then a secondary table with
     every other arm and any pending rows.
   - Results on train, validation and test: training loss in the settings table, dev results in the tables, and test
     scored or stated as held out.
5. **Inference and system considerations.**
   - Hardware, in one or two sentences.
   - A systems table: training throughput, time and peak memory; scoring throughput and peak memory; cost for the
     full workload; multiple of the budget.
   - A figure where one helps, such as accuracy against cost with the budget line.
   - What the cost would be with known engineering (kernels, packing, precision), stated as a measured or cited
     floor, never a guess.
6. **Reproducibility and interpretation.**
   - Software and versions; checkpoints; code (file, branch, the flags for each mode); where runs and data live; what
     cannot be public and why.
   - The interpretation: why the winner wins, in terms of the problem.
   - What these results do not show yet.
   - Next steps, numbered and concrete. Link the tracking issue when there is one.

**Footer.** Name the source file of every table and figure, and the run-log ids if the project keeps a run log. State
plainly whether the page quotes data. If it does, say the page stays private. Never claim it holds no data text when
it does.

## Studies that are not model comparisons

The six sections are a menu. Keep the ones that apply, rename or merge the rest, and keep the numbering consecutive.
Never leave an empty section.

| Study | Main table compares | Section 3 becomes | Notes |
| --- | --- | --- | --- |
| Model comparison, fine-tune, ablation | the best model and the reference | Model architecture | the full structure above |
| Data or filter study (rules, dedup, a pipeline) | the candidate pipelines on the same data: share kept, precision of what is removed, tokens kept, cost | Method, with a figure of the flow | section 5 keeps throughput and cost |
| Throughput or systems benchmark | the configurations: throughput, latency, memory, cost, with intervals over repeats | System setup, with a figure | section 4 becomes Measurement (protocol, repeats, variance); section 5 is the core |
| Labelling or judge study | the labellers: agreement, precision against a consensus, cost per item | Labellers (models, prompts, flow figure) | section 4 holds the agreement measures |

## Figures and charts

- **Architecture.** Put the new model beside the reference, with the same stages top to bottom and real sizes (layers,
  width, heads, parameters, context). Add an attention-mask inset when attention is the difference.
- **How data is fed.** Contrast the inputs when the arms differ in what they read (windows against whole documents,
  one item against its thread).
- **Systems.** Draw a figure wherever it helps: accuracy against cost, throughput by configuration, memory.
- **Result charts.** Chart any result that is a curve or a trade-off: learning curves, cost against accuracy,
  threshold sweeps. Load the `dataviz` skill first. Draw to one scale and write the scale functions in a comment above
  the chart. Show intervals as whiskers or bands, and name every point exactly as the tables do. Tables keep the
  exact numbers.
- **SVG rules.**
  - Keep every figure inline, with a viewBox about 760 wide, inside `figure.fig.wide > .tw`, so it scrolls on a phone.
  - Use only the skeleton's classes, so colours follow the theme.
  - Give each marker a unique id per figure.
  - Write a caption that says what to read from the figure.
- **No collisions.** No text may overlap other text, cross a box edge, sit on a line or arrow, or reach outside the
  drawing. Check this with `scripts/svg-overlaps.js` (see Workflow). Never ship a figure the script flags.

## Examples from the data

Examples give problem context only. They show what the target is, its kinds and easy and hard cases. They make the
problem concrete for a reader who has never seen the data.

- Use real items from the labelled training or dev data, never test.
  - Truncate long lines.
  - Skip anything with personal data: emails, phone numbers, names of private people.
- Show the labeller's label on each row and mark the row being discussed.
- Never compare models with examples. No model scores, no win or lose tags, no "model A cuts this, model B keeps
  it". A model's errors show up only as counts and rates in tables.
- Wrap example blocks in an element with `data-nocheck`, so the number checker skips their text.
- A page that quotes data stays private, and its HTML lives in a folder git ignores (for example `runs/`).
  Never put excerpts in a skill, a commit, a repo doc or a log you paste. The project's own data rules (its
  AGENTS.md or CLAUDE.md) win over this skill.

## Numbers

- Every number on the page comes from a file, read by code. Never type a number from memory or copy it from the
  chat.
- Compute numbers that no file holds (ratios, costs, shares, counts) with code, and write them to a `numbers.json`
  next to the report.
- Round the same way everywhere:
  - three decimals for measures between 0 and 1;
  - thousands separators for counts;
  - `k` for throughput and cost.
- Write minus signs as "−" (U+2212). Write intervals as `[0.480, 0.628]` and paired differences as
  "Δ +0.003 to +0.078".
- **Bold marks only the best value in each category, in every table of every report** (user convention). A category
  is one column within one row group: one measure for one group.
  - Bold the highest value, or the lowest where lower is better (cost, time, memory, loss). Bold every value that
    ties.
  - Nothing else in a table is bold: not the new model's row, not the reference, not a value the text stresses.
    Chance rows (`tr.base`), intervals, Δ ranges, text cells and pills are never bold.
  - Table 1's caption says once: "Bold: the best value in each column of each measure."
  - Compute the bold from the numbers when the table is built, never by hand.
- Every comparison carries an interval. If the results don't have intervals yet, compute them with a bootstrap over
  the sampled unit (documents, threads, prompts) before writing.
  - Write "higher" only when the paired interval excludes zero.
  - Write "level" or "about level" when it spans zero, and give the range.
- Run the checker before every publish:

  ```bash
  uv run --no-project python <skill-dir>/scripts/check_numbers.py report.html src1.json src2.json numbers.json
  ```

  It lists each number on the page that matches no source value. Resolve every line: fix the number, or add the
  derived value to `numbers.json` by code. Use `--ignore` only for constants of the method, such as a window size.
  A match only means some source value rounds to the number, so also read Table 1 against its source once by eye.

## Pending results and updates

- A run still going gets a row in its table with `tr.pend` and "pending: <what>, expected <date or time>". The meta
  line, the abstract and "what these results do not show yet" say what is pending.
- When it lands:
  - Replace the pending rows.
  - Update every sentence the new numbers touch: abstract, meta, interpretation, next steps.
  - Rerun both checks and the consistency review (Workflow step 7).
  - Republish to the same URL. Remove every "pending" that no longer holds.

## Workflow

1. **Gather.** List every source file (compare files, run records, label files) and read them.
   - Establish the main contenders, the reference, the bar, the budget, the groups, and which runs are pending.
   - Ask the user only what the files can't answer. Usually that's which two candidates are the main contenders,
     when more than two are close.
2. **Load the design skills.** The Artifact tool requires `artifact-design` before writing a page. Also load
   `dataviz` if the page will have a chart. The skeleton already meets the page contract (title, theme tokens in
   both themes, gutters, Google Fonts only), so the design pass is to reuse it, not to redesign it.
3. **Copy the skeleton** to the study's gitignored folder (for example `runs/<study>/report/<name>.html`). Keep the
   `<style>` block whole.
4. **Write in this order:**
   1. Table 1.
   2. The abstract and the title, which summarise Table 1.
   3. Sections 1 to 6.
   4. The footer.
   Cut every sentence that only repeats a table.
5. **Check the numbers** with `scripts/check_numbers.py`, as above.
6. **Check the figures.**
   1. The browser pane won't run scripts on a `file://` page, so serve the folder in the background:
      `uv run --no-project python -m http.server 8765 --bind 127.0.0.1 --directory <folder>`.
   2. Open `http://127.0.0.1:8765/<file>`.
   3. Pass the whole text of `scripts/svg-overlaps.js` to the browser's JavaScript tool.
   4. Fix every problem it lists and run it again, until the list is empty.
   5. Take one screenshot at about 1100 px wide and one at phone width, then stop the server.
7. **Consistency review, after every write and every edit** (user, 2026-11-19). No report is published, first or
   again, without an independent adversarial review by a Sonnet subagent (Agent tool, `model: "sonnet"`). The checks
   above confirm that each number has a source; this review confirms that the page tells one story.
   1. Write a review copy: the page's text with every table, and for each figure its caption plus the value of every
      plotted point (the `<title>` of each hover target). Strip data excerpts (example blocks, quoted lines) when the
      reviewer could be outside the user's organization.
   2. Brief the subagent with the copy and the sources (numbers files, run log ids). Ask it to break the page, not
      approve it, on these points:
      - each number is the same everywhere it appears: abstract, tables, figures, captions, text, appendix;
      - every claim in a heading, the abstract or the text is what the tables and figures show. A heading that says a
        trend stopped while its figure still rises is an error;
      - figures and tables that show the same quantity agree, and any two that look comparable but are on different
        sets, measures or model counts (one model against an average or an ensemble) say so;
      - levels compared across sections are on the same evaluation set and the same measure, or the text says why
        they differ;
      - every comparison word ("higher", "level", "within noise") matches its interval.
      It reports each finding with the two places that disagree, which one is right according to the source, and the
      fix.
   3. Fix every error at its source (the builder or the numbers file, not the HTML by hand), rebuild, and rerun steps 5
      and 6. When a fix changed a number, a heading or a figure, run the review once more.
8. **Publish** with the Artifact tool. Artifacts start private. Without the Artifact tool, hand over the HTML file's
   path instead.
   - On the first publish, pass `icon: "chart"` and a one-sentence `description`.
   - Republish from the same file path to keep the URL. A report from another session needs its `url` and a read
     first.
9. **Hand over** the link, what is pending, anything the checks could not cover, and the review's verdict.

## Writing style

- Plain, short sentences in the active voice. "We" for the study.
- Give each arm one name and use it everywhere: tables, figures and prose.
- Name the group order once ("en / es / ja") and keep it.
- Give every number its unit: GPU-hours, tokens/s, GB, documents.
- State findings with their numbers. Leave out filler, hedging, asides set off by em dashes, and stock phrases.
- Be concise. If a sentence tells the reader nothing the tables don't, cut it.
