---
name: final
description: >-
  Get a talk ready for the day and close it out afterwards: set content and
  visual freeze times, generate a one-glance cue card with time checkpoints,
  build a Q&A bank with short and long answers in the speaker's own words,
  write a day-of checklist for the room and the machine, run the final timed
  rehearsals, and archive everything once the talk is given. Use whenever a
  talk is a few days out or done: "prep for the talk day", "make me a cue
  card", "what questions will they ask", "Q&A prep", "day-of checklist",
  "freeze the deck", "the talk is done, wrap it up", "/talk:final".
argument-hint: "[freeze | cue-card | qa | checklist | archive]"
---

# Final

The last days are for polish, not for new ideas. This stage:
- freezes the talk;
- gives the speaker what they need on stage;
- prepares the room and the machine;
- after the talk, keeps everything that was learned.

## Rules

- Generate only from an in-sync state. Run `talk:build` sync first, and stop if it reports differences.
- Structure, don't invent. Q&A answers come from the speaker's own words wherever possible.
- Update `STATE.md` at the end.

## 1. Freeze

Compute two times from `date` in `talk.yaml` and the `freeze` settings, and write them into `STATE.md`:
- **Content freeze.** After this, only cuts and changes to wording; no new slides, claims or sections.
- **Visual freeze.** After this, the slides don't change at all.

Tell the speaker both times in their timezone.

## 2. Cue card

Write `cue-card.md`, compact enough to take in at a glance on a phone or a single printed page:

```markdown
# <Talk title>: cue card            Target 22:30 · Slot 25:00

## 1 · <Section>        start 0:00 → by 7:10
- why-it-hurts · Every release took a whole weekend: twelve weekends a year
- ...
  ▶ demo-video (0:45)
  ⏸ pause: let the number land
  ★ "We weren't shipping software. We were shipping weekends."

## 2 · <Section>        by 7:10 → by 15:00
```

- One line per slide: the ID, the title, and its first beat.
- A time checkpoint at each section boundary. Use measured times from the latest delivery run, falling back to planned times.
- ▶ marks a media cue, with its length taken from the actual file.
- ⏸ marks a planned pause.
- ★ marks a line that must land.

## 3. Q&A bank

Build `qa.md` from every source of likely questions:
- questions already collected from feedback and rehearsals;
- reviewers' questions in `feedback.md`;
- the cut lists in `narrative.md` and `storyboard.md`, since cut material is what curious people ask about;
- rows in `facts.md` that are not cleared to share;
- a fresh helper playing the most sceptical expert in the audience, asked for the ten hardest questions.

For each question:

```markdown
### <question>
**Short (≈15 s):** <answer>
**Long (≈60 s):** <answer>
**Don't say:** <anything not cleared to share, if relevant>
**Backup slide:** <ID, if one exists>
```

- Draft the answers from the speaker's transcripts wherever they have already said it.
- Mark which drafts are yours, and confirm them with the speaker.
- Pick the five most likely questions for the speaker to rehearse out loud.

## 4. Day-of checklist

Write `checklist.md` from `presenting`, `assets/manifest.md` and the schedule. Cover at least:
- The final file is on the presenting machine, and there are two backups in different places.
- Every piece of media plays **offline** on the presenting machine.
- Fonts and layouts look right on that machine, not just on yours.
- The display adapter, the clicker with a spare battery, and the presenter view showing the notes all work.
- The cue card is on the phone or printed.
- A visible timer is set to the target.
- The AV check is done with the venue before the slot, at a time agreed in advance.
- Water and a microphone check.

## 5. Final runs

Run two full timed delivery runs through `talk:rehearse` after the content freeze. Only cuts and drills come out of them.

## 6. Archive (after the talk)

1. Save the delivered slides, any recording of the talk, and the last transcripts into the project.
2. Add the questions the audience actually asked to `qa.md`.
3. Write `retro.md`:
   - planned against actual time;
   - what worked;
   - what to change next time;
   - which questions came up that weren't in the bank.
4. Set the stage to `archived` and check in.
