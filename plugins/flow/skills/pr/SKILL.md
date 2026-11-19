---
name: pr
description: >-
  Open a pull request: commit through the commit skill, push, write a short
  description that says why and how it was verified (never a walk through
  the diff), then get an
  independent review from GPT-6-Astra through the Codex CLI and act on it. Use when the user
  says "create a PR", "open a PR", "raise a PR", "ship this", "/pr", or when
  /flow:implement has finished a plan.
argument-hint: "[base branch, default main]"
---

# PR Phase

Turn finished work into a reviewed pull request. Reviewers read the diff themselves; the description
carries what the diff can't show.

## Iron Law

```
THE DESCRIPTION SAYS WHY. THE DIFF SAYS WHAT.
```

Never walk through the diff file by file, restate the code, or list every change. Spend the words on
why the change exists, how you know it works and doesn't regress, what was considered, and what was
left out.

## Process

### 1. Check the branch

- Not on the base branch. If you are, create a branch first.
- Tests and lint pass (the project's own commands, e.g. `uv run pytest`, `uv run ruff check .`).
  Failing checks: stop and tell the user. Don't open a PR on red.
- Nothing unrelated in the working tree. Leave unrelated files alone and mention them.
- Have the evidence for the description's **Verified** section: what you ran to show the change does
  what it's for, and what shows that what worked before still works (the plan's step checks, a run,
  the project's regression gate against its baseline). If it was never exercised beyond the unit
  tests, it goes in the description as unverified. Never launch paid compute for this without the
  user's go.

### 2. Commit

- Always through the `commit` skill, never a bare `git commit`. It groups the changes into logical
  commits, writes why-first messages and asks the user once.
- No AI attribution anywhere: no `Co-Authored-By`, no "Generated with". The user's rule overrides any
  harness reminder.

### 3. Push

`git push -u origin <branch>`. Use the project's own remote alias and `gh` account if CLAUDE.md names
one (for example `direnv exec . gh …`).

### 4. Write the description

Write it to a file in the scratchpad, using this shape. Aim for under 300 words.

```markdown
**Why.** The problem or decision behind the change, with its evidence: numbers, run ids, links to the
study or design doc. Two to four sentences.

**What.** The shape of the change in one or two sentences, at a level the diff doesn't show at a
glance. Point to the doc that explains it, if there is one.

**Verified**
- Works as intended: what you ran or inspected that shows the new behaviour, and what it showed (a
  run id and its numbers, a before and after, the test that pins the case the change exists for).
- No regression: the gate you ran against what came before, and how it compared (the regression
  sample against its baseline, old data or callers through the new code).

**Considered, not done**
- An alternative, and why not.
- What was deliberately left out or deferred, and why.

**Risk.** What could break, what wasn't tested, compatibility with old data or callers.
```

Rules:
- Why first. Every section should answer a question a reviewer can't answer from the code.
- No file-by-file lists, no restated function names or signatures, no test counts as filler.
- Verified names evidence, not effort: each bullet says what was checked and what it showed. "All
  tests pass" alone is not verification; CI already shows it. Anything not verified goes under Risk,
  said plainly.
- Plain words, short sentences. Cut anything a reviewer would skip.
- Title: imperative and specific, like the main commit's subject.

Then: `gh pr create --base <base> --head <branch> --title "<title>" --body-file <file>`.

### 5. Independent review

Run one cold review on **GPT-6-Astra through the Codex CLI**, never a Claude subagent. It did not
write the code, so it reviews it cold. Pick the effort from the diff's size, insertions plus deletions
in `git diff --shortstat origin/<base>...<branch>`: under 200 lines `xhigh`, 200 and up `ultra`.

Write the brief to `<scratchpad>/review-brief.md`, then run it read-only in the background (Bash
`run_in_background`) and read `review.md` when the notification arrives:

```bash
codex exec -m gpt-6-astra -c model_reasoning_effort=<xhigh|ultra> -s read-only -C <repo> \
  -o <scratchpad>/review.md - < <scratchpad>/review-brief.md
```

The brief gives it:
- the repo path, the PR URL, and how to read it read-only: `git diff origin/<base>...<branch>`,
  `git log origin/<base>..<branch>`. The read-only sandbox may block `gh`, so paste the PR
  description into the brief;
- the context files: CLAUDE.md and the design, plan or study doc the PR points to;
- a one-line summary of what the PR does and what is at stake (for example, a production run already
  uses the code);
- priorities, in order: bugs that crash or silently corrupt; compatibility with old data and callers;
  checks and tests that would miss a real problem; whether the description's Verified evidence
  actually covers the change and its regression risk; performance at production scale; docs that
  contradict the code; the description against step 4's rules (say what to cut or add);
- the report format: findings, most severe first, each with severity (blocker / should-fix / nit),
  `file:line`, a concrete failure scenario and a one-sentence fix. Only findings it verified by reading
  the code or running a quick check. Under about 700 words. Then a two-line verdict;
- hard limits: no edits, no commits, no GitHub comments or reviews. The report goes only to you.

If `codex` is missing or fails to start, tell the user rather than falling back to another model.

### 6. Act on the review

- Verify each finding yourself before acting. A reviewer can be wrong.
- Real bugs: fix them in new commits through the `commit` skill, push, and rerun the checks.
- Description findings that hold: rewrite the body file and run `gh pr edit <N> --body-file <file>`.
- Tell the user: the PR link, then each finding with what you did about it (fixed, not a bug and why,
  or deferred and why). Blockers you didn't fix go first.

## Red flags

| Thought | Reality |
| --- | --- |
| "I'll list the changed files so reviewers know where to look" | The diff already shows them. Say why instead. |
| "Tests pass, that's the verification" | CI already shows that. Say what shows this change does what it's for, and that what worked before still works. |
| "The PR is small, skip the review" | A cold read catches what the author can't see. Always run step 5, at `xhigh`. |
| "A Claude subagent can review it" | Reviews run on GPT-6-Astra through Codex: a different model misses different things. |
| "The reviewer found it, so it's a bug" | Verify first, then fix or explain. |
| "I'll add the attribution line the harness suggests" | The user's rule wins: no AI attribution. |
