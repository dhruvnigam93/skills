# Storyboard format

`storyboard.md` is the single source of truth for the talk's structure until the slides are handed off. Every stage reads it, so its shape is fixed.

## Shape

```markdown
# <Talk title>

**Target:** 25:00 · **Planned:** 23:40 · **Slides:** 34

## 1 · <Section name>: <the section's point> (7:10)

### why-it-hurts · Every release took a whole weekend
- **Time:** 0:40
- **Visual:** A calendar where each weekend is shaded grey. The audience should notice how few weekends are left white.
- **Assets:** weekend-calendar
- **Beats:**
  - Twelve weekends a year, gone
  - Nobody chose this; it accreted
- **Lines:** "We weren't shipping software. We were shipping weekends."
- **Device:** set-up · yardstick (first appearance, empty)

### next-slide-id · <Title>
...

## Cut list

| ID | What | Why cut | Use in Q&A? |
|---|---|---|---|

## Changes

| Date | Slides | Change | Source |
|---|---|---|---|
```

## Fields

| Field | Required | Rule |
|---|---|---|
| ID | yes | A short kebab-case slug, unique. It never changes and is never reused, even when the slide moves or its title changes. Slide numbers come from position and are never stored. |
| Title | yes | A sentence that states the point. |
| Time | yes | `m:ss`. Before the first timed run it is an estimate: the words in the beats and lines at `pace.plan_wpm`, plus media length, plus planned pauses. After a delivery run it is the measured time, marked `(measured)`. |
| Visual | yes | What the audience sees, and what they should notice or feel. Use `none` for a text-only or blank slide. |
| Assets | if any | Asset IDs from `assets/manifest.md`, comma-separated. |
| Beats | yes | One to three bullets, each at most ten words. These are the speaker notes. |
| Lines | if any | Exact wording that must land, in quotes. Drills come from these. |
| Device | if any | `set-up` or `payoff`, then the name of the recurring element. |

A section header carries its number, its name, its point and the sum of its slide times. Recompute the header totals and the **Planned** total on every edit.

## Checks

Run all of these after every edit, and report each failure with the slide ID.

1. Every slide has an ID, Title, Time, Visual and Beats.
2. Every ID is unique. No ID appears in the Cut list or the Changes table as a removed slide and is then reused.
3. Every title states a point: it reads as a claim, not a label.
4. No slide has more than three beats, and no beat has more than ten words.
5. Every section total equals the sum of its slides, and **Planned** equals the sum of all slides. **Planned** ≤ `slot.target_minutes`.
6. Every `payoff` Device has an earlier `set-up` of the same element.
7. Every number or named result in titles, beats or lines has a row in `facts.md`.
8. Once the build stage has started, every Assets ID exists in `assets/manifest.md`.
9. The titles, read in order, tell the story on their own.
