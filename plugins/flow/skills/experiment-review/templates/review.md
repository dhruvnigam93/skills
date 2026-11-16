# Review Record Template

`/flow:experiment-review` writes one record per review, at `thoughts/studies/<study>/reviews/<YYYY-MM-DD>-<round-slug>-<mode>.md`, and keeps the brief and each answer as files beside it.

## The record

```markdown
---
date: YYYY-MM-DD
study: <study folder name>
reviewed: <paths: the round design, the run plan, result files or a report>
mode: prelaunch             # prelaunch | result | directions, or two: result, directions
reviewers: A = <model>, B = <model>
---

# <Pre-launch | Result | Directions> review: <the question in a few words>

**Brief:** `<path>`. **Answers:** A `<path>`, B `<path>`.
<One line for anything chosen or waived: a setting the instructions did not cover, one reviewer instead of
several, a document sent as is at the user's request.>

## Disposition

| # | Finding | By | Verdict | Status |
| --- | --- | --- | --- | --- |

## Directions (directions mode only)

1. <a next round>: what it would tell; its cost; backed by <letters>.

**Not to do:** <what the reviewers argue against and you have checked>, each with its reason.
```

- **Verdict:** valid; or partly wrong, wrong or not verifiable, each with its reason (a file and line, a recomputed number; for not verifiable, what would verify it).
- **Status:** fixed (where), amended (date), new round, open (what would close it), or none (the finding was wrong). A status may join two: "fixed in Results; the 7B question open".

## The brief

```markdown
You are reviewing <a frozen experiment design before any compute is spent | the claims of a finished experiment |
a study, to say what to run next>. You did not design or run it. Read only: make no edits and start no runs; this
report is your only output.
<Only when so: Sent as is, at the user's request: <the document>.>

- **Question:** <one sentence>. It decides <the decision it feeds>.
- **Design:** <the design, its bar and its Answer, and factual amendments: pasted, or the files and sections to
  read and those to leave>.
- **Evidence:** <paths and read-only commands; facts you cannot reach, pasted here>.
- **Decided by the user, do not reopen:** <the Aligned bullets>. You may say what each costs, and whether any
  stops the bar from deciding.
- **Declined in an earlier review** (re-reviews only): <finding: reason>.
- **Check:** <the mode's questions; for two modes, Part A and Part B>.
- **Return:** a two-line verdict first. Then findings, worst first, each with its severity (blocker / should-fix /
  nit), where (file:line or section), what is wrong, the concrete failure it causes, and the fix with its cost.
  <Result: each claim holds / partly / does not, with your recomputed number, or why you could not recompute it.
  Directions: next rounds ranked, each with what it would tell and its cost; then what not to do.> Only what you
  checked by reading or recomputing. No praise. Under about 1,500 words.
```

## Example disposition

A result review of a warmup-length ablation, two reviewers:

| # | Finding | By | Verdict | Status |
| --- | --- | --- | --- | --- |
| 1 | Loss is read at the best validation checkpoint, not at the final step the bar names | A | valid | fixed: a Results entry (2026-01-15) replaces 2026-01-14's: −0.009 (90% interval −0.014 to −0.004) at the final step; still clears |
| 2 | Validation documents leak into training | A B | wrong: the split is by site (`data/split.py:30`), and no validation site is in the training manifest | none |
| 3 | A 1B result may not carry to the 7B's 4x batch | A B | valid | open: a short 7B run would close it; the limit is already stated |
