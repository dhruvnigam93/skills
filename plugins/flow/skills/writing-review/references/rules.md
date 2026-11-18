# Writing rules

The checklist `/flow:writing-review` applies. Each section has a tag; findings and `scripts/scan.py` use
the same tags. Adapted from Marin's [AI-writing don'ts](https://github.com/marin-community/marin/blob/main/docs/dev-guide/writing-style/ai-writing-donts.md),
which builds on Orwell's rules for writers and Simplified Technical English (ASD-STE100).

Every example below is invented. Numbers in a "better" line stand for numbers the author has; a
reviewer never makes them up (see `evidence`).

## The tests

Each paragraph carries at least one of: a result, a setup, a decision, a constraint, a caveat. A
paragraph that only frames importance or eases a transition gets rewritten around its fact or
deleted.

Ask of each sentence:
1. What information is lost if I delete it?
2. Can a number, a named fact, a decision or an explicit unknown replace it?
3. Does it still match the current code and evidence?
4. Could it appear unchanged in any software announcement?

Delete what fails. Start with the fact; stop when the useful information stops. A shorter accurate
document beats a longer one.

Break any rule below when following it would make the text less clear or less accurate. Say which
rule and why in the finding.

## `plain`: plain technical English

- Short sentences in the active voice. One action or claim per sentence.
- Common, concrete words. Keep a specialist term when it is more precise, and define it at first use
  if the audience may not know it.
- No stale metaphors or idioms ("move the needle", "low-hanging fruit", "in the weeds").
- A term the author cannot explain gets defined or dropped. Repeating jargon because a source used it
  hides that nobody here knows what it means.

> ❌ Leveraging the shard-aware sampler, throughput characteristics were materially improved.
> ✅ The sampler reads each shard once per epoch. Throughput rose from 1.1M to 1.8M docs/s.

## `empty`: sentences that carry nothing

Delete on sight:
- bridge prose: "The main change is…", "Stepping back…", "What this means is…", "That said…"
- importance claims: "Importantly", "It is worth noting", "This is the key point"
- stage directions: "Let's dive in", "Here is a summary", "In this section we…"
- effort narration: "After extensive investigation…"
- endings that add nothing: generic conclusions, recaps, future-work sections with no owner or
  decision, chatbot sign-offs ("Hope this helps", "Let me know if…")
- text that restates what the reader can see: a heading, the length of a list, a table, a diff, the
  document's own structure ("The config has three parts:" before a three-item list)

> ❌ It is worth noting that all shards share one tokenizer.
> ✅ All shards share one tokenizer.

> ❌ In this section, we describe how deduplication works. *(under the heading "Deduplication")*
> ✅ *(delete; start with the first fact)*

## `contrast`: stock contrast

Templates that stage an opposition to sound insightful:
- "X, not Y" and "not X, but Y"
- "not just X, but also Y"
- "more than X"
- "the question is no longer X; it is Y"
- "the real story / issue / win is X"
- "what matters is X"
- "rather than Y" when nobody proposed Y

Fix: state X directly. If both sides are real, write two plain claims.

> ❌ The bottleneck isn't the GPU, it's the data loader.
> ✅ The data loader takes 310 ms per batch; forward and backward take 90 ms.
> ✅ *(no timings available)* The data loader is the bottleneck.

> ❌ This is more than a refactor: it changes how shards are assigned.
> ✅ Shards are now assigned by a hash of the document ID. Before, they followed file order.

Not stock contrast: a negation that states a fact ("The ablation has not run."), or a measured
comparison where both sides matter.

## `evidence`: claims need support

- Name the thing: the code path, config key, issue, artifact, measurement, or the unknown.
- Replace an adjective with its evidence. "Robust", "powerful", "seamless", "significant", "crucial",
  "pivotal", "scalable", "comprehensive" survive only with a concrete result right behind them.
  "Statistically significant" with the test and the p-value is evidence.
- Missing evidence is stated: "We have not benchmarked X." It is never filled in by the reviewer.

> ❌ The new sampler is significantly faster.
> ✅ The new sampler processes 1.8M docs/s, up from 1.1M (`bench/sampler.py`, 8 workers).
> ✅ *(not measured)* We have not benchmarked the new sampler.

## `stale`: prose that disagrees with the source of truth

- The text matches the code, the tables and current behavior. Check every named function, flag,
  config key, path and command against the repo, and every number against the table or file it
  came from.
- An explanation of how something used to work is removed after the implementation changes.

> ❌ `--dedup` defaults to exact matching. *(the code default is `minhash`)*
> ✅ `--dedup` defaults to `minhash`.

## `term`: one name per thing

- One term for each technical object, used every time. Rotating "shard", "partition" and "chunk"
  for the same object makes the reader wonder whether there are three objects.

## `cadence`: the LLM rhythm

- No adjective trios or forced lists of three ("fast, scalable, and reliable").
- No transition adverbs: "Additionally", "Furthermore", "Moreover", "Importantly", "Notably".
- No stock vocabulary: landscape, ecosystem, interplay, tapestry, testament, delve, showcase,
  underscore, foster, leverage, realm, holistic, streamline, unlock, empower, harness.
- No em-dash asides. Make the aside its own sentence, or delete it.
- No bold labels at the start of lines, takeaway boxes, TL;DR blocks or decorative headings.

> ❌ The cache (which lives on local NVMe) is cleared on restart — so plan accordingly.
> ✅ The cache lives on local NVMe. A restart clears it.

## `cold`: what a first-time reader cannot recover

Findings from the cold reader (step 5 of the skill): an undefined term, an unclear referent ("this",
"the fix", "the old path"), a claim with no support in the text, a missing causal link. Fix with the
smallest local edit: define the term, name the referent, narrow the claim, or link the background.
Do not paste in conversation history, and do not grow a section to pre-empt every question. More
context can bury the main claim.

## Final sweep

After edits, search the text once more for stock contrast, bridge phrases, unsupported adjectives
and stale claims. Edits introduce them too.
