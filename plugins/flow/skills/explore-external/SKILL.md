---
name: explore-external
description: >-
  Discover how an external system behaves — a CLI, a third-party API, a closed
  library — by probing it directly. Use when the user says "figure out how X
  works", "explore this API", "what does this CLI actually do", "write learning
  tests for Y", "/explore-external", or when a feature depends on an external
  system whose behavior isn't documented well enough to design against.
argument-hint: "[the external system to explore — a CLI, API, or library]"
---

# Explore External

Discover how an external system behaves by probing it — not by reading docs alone. The evidence is emphatic: in the Mini-SWE-Agent ablation (2025), dynamic exploration via probe scripts gained +60 points of task success vs +4–5 for static code analysis. Docs describe intent; probes reveal behavior.

**Output:** `<repo-root>/kb/external/<system-name>.md` — permanent knowledge, not a thoughts/ transactional doc.

## Iron Law

```
NO DESIGN ASSUMPTION ABOUT EXTERNAL BEHAVIOR WITHOUT A PROBE THAT DEMONSTRATES IT
```

## Process

### 1. Classify the system

| Source available? | Approach |
|-------------------|----------|
| **Public repo** | Shallow-clone to a scratch dir, run codebase research on it via subagents. Faster and more reliable than docs. |
| **No source (closed API, service, CLI)** | Write **learning tests**: scripted probes that map behavior empirically. |

Ask the user if unclear: "Is the source for X public, or should I probe the live system?"

### 2a. Public source — clone and research

```bash
git clone --depth 1 <repo-url> /tmp/<system-name>
```

Dispatch subagents (codebase-locator, codebase-analyzer) against the clone. Focus on:
- The interface surface the user's code will call
- Edge cases, error modes, undocumented behavior
- Defaults and configuration that affect behavior

The clone is throwaway — only the learned answers survive into `kb/external/`.

### 2b. Closed system — learning tests

Write a battery of small, scripted probes — each one tests a single question about the system's behavior. Run them in a scratch directory, never inside the feature branch.

A good probe:
```bash
# probe: does the refund API return refund_id on success?
curl -s -X POST "$BASE_URL/refunds" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"charge_id": "ch_test", "amount": 100}' \
  | jq '{status: .status, has_refund_id: (.refund_id != null)}'
# expected: {"status": "succeeded", "has_refund_id": true}
```

A bad probe:
```bash
# "test the API" — tests nothing specific, learns nothing
curl "$BASE_URL/refunds"
```

Each probe:
- States the question it answers as a comment
- Has a concrete expected output
- Records actual output for comparison
- Is idempotent and safe to re-run

**Keep the probes runnable.** Save them at `<repo-root>/probes/<system-name>/` (or a scratch dir if the user prefers). They double as regression detectors when the external system changes.

### 3. Distill findings

Write `kb/external/<system-name>.md`:

```markdown
---
date: YYYY-MM-DDTHH:MM:SS+TZ
author: agent (model-id)
git_commit: <short hash>
last_verified_commit: <short hash>
status: active
---

# External: [System Name]

**What it is:** one-line description.
**Version/endpoint tested:** [version, URL, or commit hash of the source clone]

## Behavior (verified by probes)

Each finding states what was observed, not what docs claim. Cite the probe.

- Refund API returns `refund_id` on success — `probes/stripe/refund_success.sh`
- Refund of a fully-refunded charge returns 400, not idempotent success — `probes/stripe/refund_duplicate.sh`
- ...

## Failure Modes

How the system fails — timeouts, error shapes, retry behavior. Graveyard-style
negative knowledge: what looks like it should work but doesn't.

## Gotchas

Undocumented behavior, surprising defaults, things the docs get wrong.

## Configuration

Settings that affect behavior in ways the feature cares about. Defaults stated.
```

### 4. Deliver

Present in chat: key findings (3–5 bullets, each citing a probe or source file), any surprises, and the file path.

Tell the user: "External behavior documented. The probes are runnable at `probes/<system>/` — re-run them if the system updates. This feeds `/flow:design`."

## Rules

- **Probes run in scratch, never the feature branch.** They're exploration, not integration.
- **Record failures as knowledge.** A probe that fails teaches you something — document the failure mode, don't just retry and move on.
- **Docs are hypotheses, probes are evidence.** When docs and probes disagree, the probe wins. Note the discrepancy.
- **Keep probes alive.** A one-shot script you delete is a lesson you'll have to relearn. Save it.
- **kb/, not thoughts/.** Learned external behavior is permanent knowledge — it's about the system, not this task. It lives in `kb/external/` and gets updated by `/flow:kb-sync` when the system changes.
