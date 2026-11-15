# skills

Claude Code skills by [Dhruv Nigam](https://github.com/dhruvnigam93), distributed as a plugin marketplace.

## Install

In Claude Code:

```
/plugin marketplace add dhruvnigam93/skills
/plugin install flow@dhruvnigam93
```

Or from your shell:

```bash
claude plugin marketplace add dhruvnigam93/skills
claude plugin install flow@dhruvnigam93
```

Plugin skills are namespaced, so `/design` runs as `/flow:design`. Pull updates with `/plugin marketplace update dhruvnigam93`.

## Plugins

### `flow` — alignment-first AI coding workflow

The agent drafts, you sign off. Design happens at your altitude (module boundaries, signatures, invariants, schemas) before a plan or a line of code exists, and the agent has full autonomy only inside interfaces you approved. The reasoning behind it: [docs/ai-coding-workflow.md](docs/ai-coding-workflow.md).

| Skill | What it does | Status |
|-------|--------------|--------|
| `/flow:design` | Design phase for one feature: questions one at a time through the question tool with no recommended answer, a visible assumption ledger, a full interface spec, Design-It-Twice variants for load-bearing interfaces, and a hard sign-off gate. Writes `thoughts/shared/designs/YYYY-MM-DD-<slug>.md` on a feature branch. | ✅ v0.1 |
| `/flow:plan` | Plan phase for one feature: commit-sized steps, each buildable and verifiable from the plan header plus that step alone — exact files, signatures, scope (including what must not change), and a literal verify command. Design is recommended, not required. One sign-off. Writes `thoughts/shared/plans/YYYY-MM-DD-<slug>.md`. | ✅ v0.2 |
| `flow:step-reviewer` | Fresh-context subagent that `/flow:implement` dispatches after each step. It runs the step's verify command itself, checks the diff against the step (files, must-not-change, signatures), and returns APPROVE (with non-blocking notes), BLOCK (implementer fixes) or ESCALATE (needs your decision). Appends its verdict to the step's review note. | ✅ v0.3 |
| `/flow:implement` | Step loop: implement → verify green → dispatch step-reviewer → APPROVE auto-commits, BLOCK fix-and-retry (max 3), ESCALATE pauses for you. Fills the plan form as it goes (checkboxes, impl notes). Handles decision forks, phase boundaries, and the dumb-zone handoff at ~60% context. | ✅ v0.4 |
| `/flow:research` | Fan out subagents to explore the codebase and domain, synthesize into a research doc with cited findings. Every claim cites `file:line` or raw output. Opinions welcome, labeled. Feeds `/flow:design`. | ✅ v0.4 |
| `/flow:explore-external` | Discover external system behavior by probing it — shallow-clone public repos or write learning tests for closed APIs/CLIs. Findings go to `kb/external/<system>.md` as permanent knowledge. Probes kept runnable as regression detectors. | ✅ v0.4 |
| `/flow:prd` | Define the product outcome before technical design — what the user gets, not how it's built. Same one-question-at-a-time + assumption ledger mechanics as `/flow:design`, at product altitude. Feeds `/flow:design` via lineage link. | ✅ v0.4 |
| `/flow:create-handoff` | Compact the session into a handoff doc linking the plan and its exact position. Triggered manually or by the dumb-zone rule at ~60% context. Pointers, not copies — the plan is the ledger, the handoff is a shortcut into it. | ✅ v0.4 |
| `/flow:resume-handoff` | Resume from a handoff doc: validate state against git, ingest context, and continue via `/flow:implement`. Trusts the plan over the handoff, git over memory. | ✅ v0.4 |

The full roadmap (15 skills) is in [Part 3 of the spec](docs/ai-coding-workflow.md#part-3--skills-to-build).

### `talk` — a framework for building conference talks

Narrative first, storyboard second, slides last. Rehearsal starts before any slide exists, and a structure freeze keeps expensive work from being redone. Bring your own slide, visual and transcription tools. The framework is in [plugins/talk/README.md](plugins/talk/README.md).

```
/plugin install talk@dhruvnigam93
```

| Skill | What it does |
|-------|--------------|
| `/talk:start` | Sets up a talk (slot, audience, presenting setup, tools, schedule). Later, reports the stage, its gate and the next step. |
| `/talk:narrative` | Brain dump and spoken talk-through → a one-page spine → prose, tested as a journey rather than a list. Also writes call-for-papers abstracts from the spine. |
| `/talk:storyboard` | One entry per slide, with stable IDs, point-stating titles, beats and computed time, checked against the craft principles. Every structural change goes through it. |
| `/talk:feedback` | Saves reviewer feedback as received, triages it by kind and weight, finds root causes and contradictions, and applies what's accepted. |
| `/talk:rehearse` | Measures a run (time per slide, projected runtime, pace, fillers), reconciles what was said with the plan, and decides each gap: adopt, drill, cut or restore. |
| `/talk:build` | Visuals and slides from the frozen storyboard with your own tools, verified against it, and synced back after hand edits. |
| `/talk:final` | Freeze times, cue card, Q&A bank, day-of checklist, final runs and archive. |

## Develop locally

Register your clone as a marketplace; edits take effect at the next session start or after `/reload-plugins`:

```bash
claude plugin marketplace add ~/Projects/skills
claude plugin install flow@dhruvnigam93
claude plugin validate .   # run after every edit
```

## Layout

```
.claude-plugin/marketplace.json   # the catalog
plugins/flow/
  .claude-plugin/plugin.json      # plugin manifest (bump "version" to ship an update)
  skills/<skill>/SKILL.md         # one folder per skill, with references/ and templates/
  agents/<agent>.md               # subagents the skills dispatch
docs/                             # the workflow spec
BUILD-STATUS.md                   # build ledger — tracks which skills are done, decisions, next up
reference/
  research/                       # our analogue studies + usage-pattern analysis + deep research
  inspiration/
    humanlayer/                   # HumanLayer's agents + commands (ghuntley/humanlayer)
    superpowers/                  # obra/superpowers skills — SDD, review prompts, writing-plans
    mattpocock/                   # mattpocock/skills — implement, tdd, code-review, retro
  design-eval/                    # A/B test artifacts from the /design skill build
  handoffs/                       # session transition docs
tools/                            # md2pdf and other build-time scripts
```

## License

[MIT](LICENSE)
