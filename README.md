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
| `/flow:design` | Design phase for one feature: batched question rounds with recommended answers, a visible assumption ledger, a full interface spec, Design-It-Twice variants for load-bearing interfaces, and a hard sign-off gate. Writes `thoughts/shared/designs/YYYY-MM-DD-<slug>.md` on a feature branch. | ✅ v0.1 |
| `/flow:plan` | Plan phase for one feature: commit-sized steps, each buildable and verifiable from the plan header plus that step alone — exact files, signatures, scope (including what must not change), and a literal verify command. Design is recommended, not required. One sign-off. Writes `thoughts/shared/plans/YYYY-MM-DD-<slug>.md`. | ✅ v0.2 |
| `step-reviewer` | Fresh-context subagent that reviews each step's diff against its spec | Planned |
| `/flow:implement` | Step loop: check → implement → independent review → auto-commit | Planned |

The full roadmap (15 skills) is in [Part 3 of the spec](docs/ai-coding-workflow.md#part-3--skills-to-build).

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
docs/                             # the workflow spec
```

## License

[MIT](LICENSE)
