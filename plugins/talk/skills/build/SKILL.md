---
name: build
description: >-
  Turn a frozen talk storyboard into visuals and slides using whatever tools
  the speaker brings (a slide-building skill or script, a template, a visual
  generator, a stock library, a designer, or by hand), then verify the result
  against the storyboard rather than trusting the tool. Also keeps slides and
  storyboard in sync after the speaker edits the slides by hand. Use whenever
  someone wants to make the slides or visuals for a planned talk: "build the
  deck", "make the slides from the storyboard", "generate the visuals",
  "rebuild after these changes", "I edited the slides, sync it back", "check
  the deck is right", "/talk:build".
argument-hint: "[visuals | slides | verify | sync]"
---

# Build

Visuals and slides are the most expensive form of the talk, so they come after the structure freezes. This skill makes them from `storyboard.md` and checks that what was made matches it. Each job uses whichever tool the speaker named in `talk.yaml`.

## Rules

- **Bring your own tools.**
  - Use `tools.visuals` for visuals and `tools.slides` for slides.
  - If a slot is blank, ask once with the options a skill or script, a template, a person, or by hand. Record the answer in `talk.yaml`.
  - "By hand" means you produce a build sheet the speaker follows.
- **Generate from the storyboard; never copy it by hand.** If a tool needs its own input file, derive it from `storyboard.md` mechanically on every build, so the storyboard stays the only source.
- **Check the files, not the report.** A tool saying it succeeded proves nothing. Count, read back and look at the output.
- **Respect the owner.** Once `STATE.md` says `Slides owner: slides`, never rebuild over hand edits. Use **sync** instead.
- Update `STATE.md` at the end.

## Before you start

Check that the structure is frozen: the stage is `build` or later. If it isn't, say so, and ask whether to build anyway. Anything built before the freeze will probably be rebuilt.

## Visuals

1. **Write the manifest.** Take every **Assets** ID and every **Visual** that needs more than text, and list them in `assets/manifest.md`:

   ```markdown
   | Asset | Slides | What it shows | Kind | Source | Status | File |
   |---|---|---|---|---|---|---|
   <!-- Kind: image · diagram · chart · screenshot · video · audio
        Source: make · find · record · provided
        Status: todo · draft · approved -->
   ```

2. **Write the style sheet.** Turn `talk.yaml`'s `style` into `assets/style.md`:
   - the palette, with one fixed background colour;
   - how line and type are treated;
   - the framing;
   - how each recurring element looks.

   Every visual is made from this sheet, so the set reads as one family.

3. **Make one first.** Pick the most representative visual, make it, and show it to the speaker. Adjust the style sheet until it's right. Only then make the rest.

4. **Check each visual** against all of these:
   - It shows what the manifest says.
   - It follows the style sheet.
   - It can be read from the back of the room: large type and strong contrast.
   - It has the right aspect ratio for its place on the slide.
   - Each recurring element looks the same every time it appears.

   Allow at most three rounds of redoing a visual. After that, show the best candidates side by side and let the speaker choose.

5. **Check the media.**
   - Video and audio play in `presenting.app` on `presenting.machine`, at consistent levels.
   - Media is embedded, not linked, unless the speaker controls the machine.

   Anything that needs recording goes into "Needs lead time" in `STATE.md`.

## Slides

1. **Map the storyboard onto slides,** whatever the tool:
   - one slide per storyboard slide, in order;
   - the title exactly as written;
   - the visual from the manifest;
   - the beats, and any lines, as speaker notes;
   - **the last line of every slide's notes is `id: <slide-id>`**, so a slide can be matched back to the storyboard after any edit;
   - a section divider wherever the storyboard starts a section, if the speaker wants dividers.

2. **Build** with `tools.slides`. For "by hand", write `slides/build-sheet.md` instead, one block per slide, with every field above, ready to copy.

3. **Verify** and report every failure by slide ID:
   - The slide count equals the storyboard count, plus any dividers.
   - Every slide's notes match its beats and end with its ID.
   - Every asset in the manifest is placed, and none is stretched or awkwardly cropped.
   - Text fits its box on every slide.
   - Media is embedded and plays.
   - Every slide is rendered to an image if the tool allows, and you look at all of them together on one contact sheet. Problems that never show up in a file check jump out on a contact sheet.

   Never quietly drop or weaken a check because the tool makes it awkward. Say which check couldn't run.

4. **Share** a version the speaker can flip through on a phone, so they can review it away from the desk.

5. **Close.** Set the stage to `loop-b` and check in.

## Sync (after hand edits)

At some point the speaker will move into their presenting app for final polish. That is the **hand-off**: set `Slides owner: slides` in `STATE.md`. From then on the slides lead, and the storyboard follows.

After every editing session, or every time the speaker exports a new version:
1. **Read the slides:** order, titles, notes, the `id:` lines and any comments.
2. **Diff them against `storyboard.md`,** matching by ID, or by title where an ID is missing. List the slides that were added, removed, moved or retitled, and any whose notes changed.
3. **Update** `storyboard.md` and the manifest to match, and log each change in **Changes**. Any comments go through `talk:feedback`.
4. **Report** either "in sync" or the differences that remain.

The cue card and the Q&A bank are only generated from an in-sync state.
