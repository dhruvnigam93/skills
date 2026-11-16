# Study Index Template

`/flow:experiment-design` creates `thoughts/studies/<YYYY-MM-DD>-<study-slug>/README.md` with the first round it designs in a study, and adds each round's row at sign-off; `/flow:experiment-close` fills in Answer and Decision and keeps "Where we stand" current. It answers one question for anyone who opens the folder: where does this study stand? Keep it to one screen; the history lives in the round designs and the project record.

```markdown
# <Study name>

**Serves:** the question the whole study answers, and the decision it feeds.
**Where we stand (YYYY-MM-DD):** two to four lines: the current answer, the current candidate, what is unproven.

| Round | Question | Answer | Decision | Records |
| --- | --- | --- | --- | --- |
| [YYYY-MM-DD <round name>](<path to the round design>) | one line | — | — | ids in the project record |

**Next (the user's call):** candidate rounds, one line each.
**Earlier work:** links to documents and record ids from before this index, if any.
```

Conventions:
- One row per round, oldest first, linked where its design lives. A new row has "—" in Answer and Decision until `/flow:experiment-close` fills them: the index keeps no status of its own.
- An index created for a study that already has work lists that work under "Earlier work", as plain links; its rows are not reconstructed unless the user asks.
- Questions split off a dump, and candidate rounds from analysis, go under Next, each with what it would tell us and roughly what it costs. The user picks; nothing under Next runs on its own.

## Example

```markdown
# Small-model recipe

**Serves:** which training settings the 7B run takes from 1B ablations.
**Where we stand (2026-01-12):** peak lr 3e-4 holds at 1B. A 2,000-step warmup round is frozen.

| Round | Question | Answer | Decision | Records |
| --- | --- | --- | --- | --- |
| [2026-01-06 peak lr](rounds/2026-01-06-peak-lr.md) | Does 6e-4 beat 3e-4 at 1B? | No: 0.011 higher (90% interval +0.006 to +0.016) | Keep 3e-4 (user, 2026-01-09) | R-1 to R-4 |
| [2026-01-12 warmup length](rounds/2026-01-12-warmup-length.md) | Does a 2,000-step warmup beat 500 at 1B? | — | — | — |

**Next (the user's call):** a 1,000-step warmup, only if 2,000 clears (about 160 GPU-h).
```
