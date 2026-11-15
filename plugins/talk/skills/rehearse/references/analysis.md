# Rehearsal analysis

How to measure a run and report on it. The numbers are simple. What matters is that they are computed the same way every time, so that runs can be compared.

## Timing

Start from the slide boundaries: the measured slide-change times, or the alignment of the transcript to the slides.

| Measure | How |
|---|---|
| Slide time | Start of the next slide minus start of this one. |
| Section time | The sum of its slides' times. |
| Run time | From the first word to the last word. |
| Delta | `actual − planned`, for each slide and each section, in seconds and as a percentage. |
| **Projected runtime** | Run time, plus the planned time of anything skipped in this run (media not played, a section passed over, a demo described instead of run), plus 5% for live conditions such as applause, transitions, the clicker and a slower start. |

Judge the gate on the **projected** runtime, never on the raw run time. A run that skipped the media is short by exactly the part that will run long on the day.

Flag:
- any section off its plan by more than 25%;
- a projected runtime over `slot.target_minutes`;
- a projected runtime over `slot.talk_minutes`, which means the talk is over the slot.

## Pace

- **Words per minute:** spoken words divided by speaking minutes, for the whole run.
- **Windows:** words per minute in each five-minute window. Flag any window above `pace.max_wpm`.

Pace usually climbs in the last third, as the speaker senses the clock. The fix is almost always to cut content, not to talk faster.

## Fillers and tics

- Count the common fillers in the speaker's language. In English these are "um", "uh", "like", "so", "you know", "basically", "actually" and a tag "right?".
- Also count any word or phrase this speaker repeats far more often than ordinary speech would.
- Report the top three, with counts and rate per minute.
- Compare them with the last run, so the speaker can see the trend.

## Drills

A drill is an exact line taken from a slide's **Lines**.
- Each run carries at most seven.
- Score each one in the next run: **hit** if it was said substantially as written, otherwise **miss**.
- The drill rate is hits ÷ drills. The ready gate needs 85% or more.
- A line missed twice is a signal: either the line is wrong for the speaker (ADOPT what they actually say, or CUT it), or it needs a stronger cue in the beats.

## Report format

Save this as `rehearsals/<date>-<n>-<mode>/report.md`:

```markdown
# Run <n>: <mode>, <date>

**Run time:** 23:12 · **Projected:** 25:05 · **Target:** 22:30 · **Slot:** 25:00
**Pace:** 158 wpm overall, peak 181 wpm (minutes 15–20)
**Fillers:** "so" 41 (1.8/min) · "right?" 22 · "um" 9
**Drills from last run:** 5/6 hit (83%)

## Sections
| Section | Planned | Actual | Delta |
|---|---|---|---|

## Slides over or under by more than 30 seconds
| Slide | Planned | Actual | Note |
|---|---|---|---|

## Decisions
| ID | Slide | Type | What | Decision |
|---|---|---|---|---|
<!-- ID = R<run>-<n>. Type = ADOPT · DRILL · CUT · RESTORE -->

## Drills for next run
1. <slide-id>: "<exact line>"

## Gate
<what passes, what doesn't, and what would make it pass>
```

Structure-mode reports keep only the section timing, the decisions and the gate.
