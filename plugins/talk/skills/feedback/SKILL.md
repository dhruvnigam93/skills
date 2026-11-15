---
name: feedback
description: >-
  Take in feedback on a talk from reviewers, friends, organisers or the
  speaker's own notes, in any form: slide comments, chat messages, call notes,
  voice notes or marked-up exports. Saves it verbatim, splits it into items,
  triages each by kind and weight, finds root causes and contradictions, asks
  the speaker only what needs their call, and applies what's accepted. Use
  whenever someone shares comments or reactions on their talk, storyboard or
  slides: "here's what my reviewer said", "my friend watched the run-through",
  "the organisers sent notes", "go through these comments", "what should I
  change based on this feedback", "/talk:feedback". Also use to write a review
  request to send to a reviewer.
argument-hint: "[path to feedback, or paste it]"
---

# Feedback

Outside eyes catch what the speaker can't: the moment the room gets lost, the jargon nobody else knows, the section that only makes sense with the backstory. This skill turns feedback into decisions and changes, and keeps the original so nothing gets misremembered.

## Rules

- **Save before acting.** The feedback goes into `raw/` exactly as received, named by date and source, before any triage.
- Align first. Ask only about items that need the speaker's judgement.
- Apply structural changes through the `talk:storyboard` revise rules. After hand-off, apply them to the slides.
- Update `STATE.md` at the end.

## Steps

1. **Save it.** Write the feedback to `raw/<date>-<source>-feedback.<ext>`, exactly as received. If it's in a file (comments inside a slide export, a document, a recording), extract the text and save that too. Keep each comment next to the slide it was attached to.

2. **Split it into items**, one per distinct point. Keep the reviewer's words. Link each item to a slide ID wherever you can.

3. **Triage** each item into `feedback.md` (create it on first use):

   ```markdown
   | ID | Date | Source | Slides | Quote | Kind | Weight | Decision | Why | Applied |
   |---|---|---|---|---|---|---|---|---|---|
   ```

   | Column | Values |
   |---|---|
   | ID | `F1`, `F2` and so on. Never reused. |
   | Kind | structure · clarity · content · visual · delivery |
   | Weight | **blocks** (the talk fails without a fix) · **should** · **could** |
   | Decision | accept · adapt · reject · park. Proposed by you, then confirmed by the speaker. |

   While triaging:
   - **Find root causes.** Several comments often share one cause. Propose one fix and link all of them to it.
   - **Surface contradictions.** When two reviewers disagree, show both views side by side for the speaker to decide.
   - **Keep reframings.** When a reviewer phrases the point better than the talk does, record it as a candidate line, credited to them.
   - **Treat a reviewer's question as a likely audience question.** Add it to `qa.md`.

4. **Decide.** Show the proposed decisions grouped by weight.
   - Ask about each **blocks** item and each contradiction one at a time, with the recommended decision first.
   - Offer the rest as one batch to accept or edit.

5. **Apply what's accepted:**
   - structure and wording go through `talk:storyboard` (revise), or into the slides after hand-off;
   - visual changes go to the asset manifest;
   - delivery notes become drills for the next rehearsal.

   Mark each item `Applied` and give the slide IDs it touched.

6. **Close.** Record in `STATE.md` how many **blocks** items are still open. The structure-freeze gate needs zero. Then check in.

## Asking for a review

When the speaker wants feedback, draft the request for them. Keep it short and specific.
- **When:** ask for it on the storyboard during Loop A, while changes are still cheap, and again on the slides during Loop B.
- **Whom:**
  - someone who resembles the audience, to tell you where they got lost;
  - someone who knows the craft of talks, to tell you about structure and pacing.
- **What to ask:**
  - Where did you stop following, or stop caring?
  - What would you cut?
  - What did you expect that never came?
  - Which one line will you remember?
- **Which format:** comments on the slides or the storyboard, a voice note, or a quick call. Anything works, because this skill saves it all as it arrives.
