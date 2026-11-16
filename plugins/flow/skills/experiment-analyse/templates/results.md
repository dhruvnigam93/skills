# Results Template

`/flow:experiment-analyse` appends one entry under the round design's **Results** heading, below the freeze line, for each reading. A later entry names what it replaces and leaves the earlier one, and the numbers it cites, in place. Every number comes from the numbers file. Leave out a line with nothing to say, except the verdict.

```markdown
### YYYY-MM-DD (<ids in the project record>)
- **Ran:** arms, seeds and data counts, as designed or what differed and which comparisons it breaks; arms
  missing or dropped, and why.
- **Bar:** the planned measure per arm and seed, then the average; the paired difference with its interval; each
  group the bar names, with its count of independent items.
- **Checks:** the ones that fit, a clause each; any the user waived.
- **Predicted against actual:**

  | | Predicted (user) | Forecast | Actual | Gap, and why |
  | --- | --- | --- | --- | --- |
  | Result | | — | | |
  | Wall | | | | |
  | Compute | | | | |
  | Money | | | | |
  | Hypothesis | the reason given | — | held, failed, or not tested here | |

- **Outcome:** the Answer's outcome, in its words, and what it says to do.
- **Exploratory:** findings chosen after looking that support a claim, each with the round that would test it.
- **Next (the user's call):** candidate rounds, one line each: what it would tell us and roughly what it costs.
- **Numbers:** the numbers file's path.
```

Conventions:
- A pilot or a partial set: **Ran**, the measured rates against the forecast, and the corrected forecast. No **Bar** or **Outcome** unless the design's **Order** reads that result.
- No prediction on record: one line saying so, then forecast against actual only. A Money row only where the project states a rate.
- Many arms: tabulate the steps between arms (paired differences, per group and seed), not every level.
- Each interval's level and method stated once (for example "90% bootstrap over documents"); differences signed.

## Example: the warmup round, answered

```markdown
### 2026-01-14 (run log R-5, R-6)
- **Ran:** as designed: wu-2000 at seeds 1 and 2 against the reference (R-3, R-4); one commit, frozen settings.
- **Bar:** final validation loss, 2,000 minus 500, paired by seed, 90% bootstrap over documents: seed 1 −0.008
  [−0.011, −0.005], seed 2 −0.010 [−0.013, −0.007], pooled −0.009 [−0.011, −0.007].
- **Checks:** the two seeds' steps differ by 0.002, under the 0.009 effect; the ten largest documents carry 0.9%.
- **Predicted against actual:**

  | | Predicted (user) | Forecast | Actual | Gap, and why |
  | --- | --- | --- | --- | --- |
  | Result | 0.005 to 0.02 lower; 60% sure | — | 0.009 lower | inside the range |
  | Wall | a day | 10 h | 11 h | forecast +1 h: one run queued for GPUs |
  | Compute | ~200 GPU-h | 158 GPU-h | 161 GPU-h | prediction ~25% high; forecast close: R-3's rate held |
  | Hypothesis | warmup too short for the batch | — | not tested here | spikes were not a planned measure |

- **Outcome:** clears. The 7B run uses 2,000 steps.
- **Numbers:** `rounds/2026-01-12-warmup-length.numbers.json`.
```
