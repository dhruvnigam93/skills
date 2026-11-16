# Round Design Template

`/flow:experiment-design` writes one file per round from this template, at `thoughts/studies/<study>/rounds/<YYYY-MM-DD>-<round-slug>.md`, or fills in a design written by hand where it lives. The section names are fixed. Length follows the round: above the freeze line, a section with nothing to say holds one line saying so.

```markdown
---
date: YYYY-MM-DD
study: <study folder name>
status: draft                # draft | frozen | answered | closed
frozen:                      # date of sign-off
follows:                     # the round this one follows, or none
run_plan:                    # set by experiment-plan, or none
---

# <The question in a few words>

## Question
One sentence, one question, on a named measure. Then one line: the decision this answer feeds.

## Hypothesis and predictions (user, YYYY-MM-DD)
- **Hypothesis:** what the user expects to happen, and why.
- **Predicted result:** a number or range per arm on the question's measure (for many arms, the shape and a
  number at the cells that decide), and how sure.
- **Predicted time and cost:** wall-clock and compute, and money if the user thinks in it.
If a result of this round had been seen, one line says what, next to the date.

## Aligned (user, YYYY-MM-DD)
The decisions the alignment questions settled, one bullet each. Settled without a question: "(assumed)" and
the basis. Waived readiness checks: "(waived, user)".

## Context
What is already known, with pointers into the project record. The reference this round has to beat, and
whether it is still the current best.

## Design
- **Bar:** the measure, the number, the groups it is judged on, and what "clears" means.
- **Arms:** a table (arm, what changes, settings), or one line for two arms. One line on what stays fixed.
- **Data and evaluation:** counts, the split rule, what is held out, and why the evaluation can decide the bar.
- **Measures:** each measure, its weighting, how intervals and paired differences are computed.
- **Seeds and repeats:** how many, against the measured run-to-run spread.
- **Order:** the cheapest informative step first; a pilot only if something is unmeasured; arms that run only
  if an earlier result calls for them.
- **Needs** (optional): code or data that must exist before the run.
- **Saved:** models, mid-run checkpoints, per-item scores. What is logged during the run belongs to the run plan.

## Answer
Written before the run: each outcome (clears, misses, can't tell, or the question's own words for them), what
it means, and what we do.

## Forecast
| Step | Wall | Compute | Money | Basis |
| --- | --- | --- | --- | --- |

One row per step that bills real compute; money only where the project states a rate. The total against the
budget. Stop and look: a run past 1.5x its forecast.
Review before launch: required | not required, with the total against the review threshold (or "not required:
no rate to compare against the threshold").

## Limits
Known confounds and which way each biases the answer. The cuts, each with what it would have told us and what
it would have cost. What this round does not cover.

<!-- frozen above this line at sign-off: changes below only -->

## Amendments
## Results
## Decision
```

Rules:
- **Frozen** means: at sign-off, set `status: frozen` and `frozen:`. The freeze covers the body above the freeze line; the frontmatter is bookkeeping and may change. A change to the design is one line under **Amendments**: date, what changed, why, and what had already been seen when it changed.
- A change to the **question** or the **bar** is not an amendment: it is a new round.
- **Results** is appended by `/flow:experiment-analyse`, **Decision** by `/flow:experiment-close`.
- The predictions are the user's own words and figures: record them, never invent them.

## Example: the body of a small round, frozen

```markdown
# Warmup length at 1B

## Question
At 1B and 20B tokens, does a 2,000-step warmup end with lower validation loss than the current 500?
It sets the 7B run's warmup.

## Hypothesis and predictions (user, 2026-01-12)
- **Hypothesis:** the early loss spikes come from a warmup too short for the batch; a longer one ends lower.
- **Predicted result:** 0.005 to 0.02 below the reference's 2.712 and 2.716; 60% sure.
- **Predicted time and cost:** a day; about 200 GPU-hours.

## Aligned (user, 2026-01-12)
- Only the warmup changes; the reference's two seeds; budget 250 GPU-hours.
- Final loss decides, not the spikes (assumed: the 7B run is judged on final loss).

## Context
The peak-lr round's 3e-4 runs (R-3, R-4) used warmup 500 on this trainer commit: the reference, reused.

## Design
- **Bar:** final validation loss, 2,000 minus 500, paired by seed: clears if 0.005 lower or more, with the 90% interval below zero.
- **Arms:** wu-2000 against the reference. Fixed: data and order, batch, peak lr, decay, tokens.
- **Data and evaluation:** 40k held-out documents in the 7B mix, split by site; the ten largest carry under 1% of the loss.
- **Measures:** token-weighted loss; the interval is a bootstrap over documents, pooled over seeds.
- **Seeds and repeats:** two; the reference's seeds ended 0.004 apart, under the bar.
- **Order:** both runs side by side; no pilot: R-3 measured this configuration's rate.
- **Saved:** checkpoints every 2B tokens; per-document validation loss.

## Answer
- **Clears:** the 7B run uses 2,000 steps.
- **Can't tell** (the interval spans zero): keep 500; a third seed only if the 7B start is a week away.
- **Misses** (any other result): keep 500; the gain is not in the warmup.

## Forecast
| Step | Wall | Compute | Basis |
| --- | --- | --- | --- |
| Two runs, side by side | 10 h | 158 GPU-h | 70k tokens/s per GPU (R-3): 9.9 h × 8 GPUs a run |

158 of 250 GPU-h. Stop and look: a run past 15 h.
Review before launch: not required: no rate to compare against the threshold.

## Limits
- 1B, not 7B: the 7B batch is 4x larger and may want a longer warmup still.
- Cut: a 1,000-step arm (would locate the best length; +158 GPU-h).

<!-- frozen above this line at sign-off: changes below only -->
```
