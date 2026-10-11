# Research Foundations for the Design of a Personal AI-Coding Workflow

**Key Points:**
*   Research suggests a pronounced "dumb zone" in Large Language Models (LLMs) when context window utilization surpasses 50–70%, primarily due to attention dilution and positional bias.
*   It seems likely that static agent plans are highly prone to failure; adaptive "living" documents with mid-execution replanning protocols significantly increase multi-step reliability. 
*   The evidence leans toward "learning tests" and dynamic probe scripts being vastly superior to static code analysis for agents exploring undocumented or external systems.
*   Metadata, document lineage, and structured provenance are emerging as critical requirements for multi-agent workflows, enabling precise context retrieval and preventing context pollution.

**Overview of the Agentic Paradigm Shift**
The transition from traditional software engineering to AI-assisted and fully autonomous agentic workflows represents a paradigm shift in how code is authored, tested, and maintained. Initial approaches to AI coding relied heavily on prompt engineering and static contexts. However, recent empirical data (2024–2026) reveals that treating LLMs as stateless functions with infinitely scalable memory is a flawed architectural assumption. Instead, practitioners are converging on the discipline of "context engineering" and "harness design." This report synthesizes recent academic papers, engineering blogs, and practitioner methodologies to provide a rigorously researched foundation for a personal AI-coding workflow, addressing context degradation, adaptive planning, external system characterization, and document lineage.

---

## Topic 1: Context-Window 'Dumb Zone'

### (a) Key Findings on Long-Context Degradation

The assumption that larger context windows equate to superior agent performance has been empirically challenged by recent academic and industry research. As an LLM's working memory fills, it enters a "dumb zone" characterized by measurable drops in reasoning, tool selection, and instruction adherence. 

**The 'Lost in the Middle' Phenomenon and Context Rot**
The foundational 2024 paper *Lost in the Middle: How Language Models Use Long Contexts* (Liu et al.) demonstrated that LLMs exhibit a pronounced U-shaped performance curve [cite: 1, 2]. Models accurately retrieve and reason over information located at the very beginning (primacy bias) or the very end (recency bias) of a context window, but performance significantly degrades when relevant information is buried in the middle [cite: 1, 3]. Follow-up research in 2025 further revealed that this is an intrinsic positional attention bias; LLMs assign higher attention weights to boundary tokens regardless of semantic relevance [cite: 4]. 

Furthermore, an October 2025 arXiv paper titled *Context Length Alone Hurts LLM Performance Despite Perfect Retrieval* revealed that even when irrelevant tokens are completely masked and retrieval is 100% perfect, model performance degrades by 13.9% to 85% simply as input length increases [cite: 4]. This phenomenon is compounded in multi-turn coding agents by "context rot"—the gradual corruption of active runtime memory driven by the agent's own execution trace [cite: 5]. As a conversation extends, the model is burdened by "distractor interference," where semantically similar but irrelevant historical turns actively mislead the model [cite: 6]. 

**Empirical Support for the 50–70% Threshold**
Industry practitioners and researchers have identified specific utilization thresholds where agent quality begins to fracture:
*   **< 50% Utilization:** The U-shaped degradation curve holds relatively stable, and the model maintains high coherence [cite: 6].
*   **60% Utilization:** A study of 50 Claude Code sessions by Blake Crosley found that output quality—manifesting as forgotten instructions and repeated suggestions—starts degrading at approximately 60% utilization [cite: 7].
*   **64–75% Utilization:** Sourcegraph's Amp team noted that recursive summarization and context decay necessitate auto-compaction or handoffs at the 64–75% mark [cite: 8].
*   **73%+ Utilization:** Research into Claude Sonnet's 200,000-token window by Sourcegraph engineer Geoffrey Huntley found a "Degraded State" beginning around 147,000 tokens (~73.5%). In this phase, the agent abandons reasoning for brute-force solutions and loops through failed approaches [cite: 9].

| Degradation Phase | Utilization % | Token Approx (200k Model) | Observed Agent Behavior |
| :--- | :--- | :--- | :--- |
| Peak Performance | 0 – 25% | 0 – 50k | Accurate reasoning, appropriate tool use [cite: 9]. |
| Stable Decline | 25 – 60% | 50k – 120k | Occasional context misses; U-shape bias forms [cite: 7, 9]. |
| Early Warning Zone | 60 – 74% | 120k – 148k | Forgotten instructions, degraded tool selection [cite: 7, 10]. |
| Dumb Zone (Rot) | > 75% | 150k+ | Brute-force guessing, recursive hallucination [cite: 9]. |

**Handoff Protocols and Document Content**
To combat context rot, practitioners have shifted away from automated, recursive summarization (which often leads to "hallucination compounds") and instead utilize hard session resets [cite: 8, 10]. Production systems monitor context in real-time, using a two-stage approach: an "early warning" (e.g., at 64%) triggers a memory sync, and a "session switch" (e.g., at 80%) initiates a graceful handoff to a fresh session [cite: 6].

A handoff document acts as the durable state transfer between these isolated sessions. According to practitioners building reliable multi-agent systems, a high-quality handoff document must contain:
1.  **File Manifest:** Exactly which files have been modified and their current state [cite: 7].
2.  **Task Breakdown:** What is fully complete, and what is currently in progress with numbered sub-tasks [cite: 7].
3.  **Critical Invariants:** Rules or states the new session must never break [cite: 7].
4.  **Decision Rationale:** Key architectural decisions made in the prior session to prevent the new agent from rehashing solved problems [cite: 7].
5.  **Resumption Commands:** The exact CLI commands or scripts needed to resume testing/execution [cite: 7].

*Extrapolation Warning:* While the 50-75% degradation threshold is well-supported by 2025/2026 data, the exact token count where performance drops is highly dependent on the density of the specific codebase and the complexity of the requested reasoning. 

### (b) Concrete Recommendations for Workflow
*   **Implement Proactive Rotation:** Configure your agent harness to monitor context utilization. Establish a strict rule to execute a context reset and generate a handoff document when utilization reaches 70%. Never push an agent to 90% capacity.
*   **Standardize Handoffs:** Create a system prompt specifically for the "compaction/handoff" phase. When triggered, the agent must write a `handoff.md` file containing the file manifest, completed/pending tasks, and decision rationale before terminating.
*   **Avoid Recursive Summarization:** Do not ask the agent to summarize a summary. Always start a fresh session loading only the `handoff.md` and the core `CLAUDE.md` / `AGENTS.md` instructions.

### (c) Citations
*   [cite: 6] Zylos.ai, "Context Window Management & Session Lifecycle" (2026)
*   [cite: 7] Probl.me, "Context Limits as a Design Constraint" (2026)
*   [cite: 8] Smarter Articles, "When Coding Agents Forget" (2026)
*   [cite: 1, 2, 3] Liu et al., "Lost in the Middle: How Language Models Use Long Contexts" (TACL, 2024)
*   [cite: 4] DiffRay.ai, "Context Length Alone Hurts LLM Performance" (arXiv, 2025)
*   [cite: 9] TurboAI.dev, "Why Your Claude Code Sessions Keep Dying" (2025)
*   [cite: 10] ShareUHack, "Context Engineering Guide 2026" (2026)

---

## Topic 2: Living Plan Documents for Coding Agents

### (a) Key Findings on Mutable Planning Artifacts

In multi-step, autonomous execution, LLMs are highly susceptible to "progress-as-completion" (mistaking activity, like generating a file, for successful goal achievement) and "long-task drift" (stubbornly executing a predefined plan even after environmental feedback renders it invalid) [cite: 5]. To mitigate this, practitioners are moving from static prompts to "living plan documents." 

**Adaptive vs. Frozen Plans**
Research into multi-agent systems highlights the catastrophic failures of frozen plans. For instance, if an agent discovers an API migration issue on step 2 of a 20-step plan, a static planner will often continue blindly executing steps 3 through 20 [cite: 5]. The *CollabCoder* framework (2026) addresses this through "Plan-Code Co-Evolution." Rather than executing planning and coding in isolated, static sequences, CollabCoder utilizes explicit mechanisms to decide whether execution failures should be addressed at the implementation level (fixing a bug) or the plan level (revising high-level reasoning) [cite: 11]. 

Similarly, Anthropic's long-running agent research emphasizes the use of `CLAUDE.md` as a living plan that the agent actively edits as it learns, paired with a `CHANGELOG.md` to act as portable lab notes [cite: 12]. These files form a "durable progress ledger" that survives the inevitable context resets discussed in Topic 1.

**Mid-Execution Replanning Protocols**
Replanning requires passing specific execution state variables back to the planner. A practical implementation of a replanning protocol involves tracking state markers (e.g., `is_ambiguous`, `is_decision_taken`) after executing non-deterministic tasks. If an anomaly is detected, the planner uses these updated results to truncate the outdated steps and append newly planned steps (e.g., `[KEPT_STEPS..., NEWLY_PLANNED_STEPS...]`) [cite: 13]. 

The AADLCv2 (Agentic Application Development Lifecycle) methodology formalizes this into a control loop: shaping, planning, bounded execution, deterministic validation, and context reset [cite: 14]. A crucial step in this loop is the context reset, where temporary plan files are pruned, and only "stable truths" and new architectural invariants are recorded into the durable memory [cite: 14].

**Living Document Mechanics**
Practitioners advise keeping core instructional documents (like `CLAUDE.md`) aggressively short—under 200 lines, or ideally under 60 lines [cite: 15, 16]. To handle complex plans, teams employ "progressive disclosure" [cite: 16, 17]. The agent maintains a high-level table of contents and dynamically loads specific sub-plans (e.g., `docs/adr/001-auth.md`) only when needed [cite: 15]. During execution, the agent uses these markdown files as checkboxes, annotating them with per-step implementation notes and reviewer notes, transforming the document into an explicit state machine.

### (b) Concrete Recommendations for Workflow
*   **The Checkbox Ledger:** Require your agent to generate a `PLAN.md` file with explicit markdown checkboxes (`- `) before writing code. Enforce a rule that the agent must edit this file to check off tasks and append a 1-sentence "implementation note" after each successful test.
*   **Forking Logic:** Encourage the agent to write conditional logic into the plan (e.g., "Step 3: Check if API X is deprecated. If yes, fork to Step 3A; if no, proceed to 3B").
*   **The "Ralph Loop":** Implement a verification prompt (the "Ralph loop") that challenges the agent when it claims completion: "Are you sure this is complete? Verify against the invariants in PLAN.md before terminating" [cite: 12].
*   **Durable State:** Never rely on the chat interface's history for continuity. Ensure that all critical architectural shifts discovered mid-execution are written back to a `CONTEXT.md` or `CHANGELOG.md` file before a session handoff [cite: 12, 15].

### (c) Citations
*   [cite: 13] Varun Kukade, "Turning a coding assistant into a cost-effective autonomous AI agent" (2025)
*   [cite: 5] EPAM, "AI Agent Failure Modes in the Enterprise" (2026)
*   [cite: 14] CirriusTech, "AADLCv2: FinOps for delegated cognition" (2026)
*   [cite: 12] Addy Osmani, "Long-Running Agents" (2026)
*   [cite: 11] CollabCoder Framework (Findings of ACL, 2026)
*   [cite: 15] Reddit /r/ClaudeCode, "Anthropic says keep CLAUDE.md under 200 lines" (2026)
*   [cite: 16] HumanLayer, "Writing a good CLAUDE.md" (2025)

---

## Topic 3: Learning Tests for External Systems

### (a) Key Findings on System Probing

When an AI agent encounters an external system—such as a third-party API, a closed-source CLI, or a complex undocumented library—relying on the LLM's pre-trained knowledge is highly dangerous due to hallucination and data staleness. Practitioners have successfully adapted Michael Feathers' concept of the "characterization test" (or "learning test") to agentic workflows.

**The Role of Learning Tests**
Learning tests are integration tests written prior to production code, designed specifically to conduct controlled experiments against a third-party API to verify the developer's (or agent's) understanding of its behavior [cite: 18, 19]. In an AI context, Simon Willison refers to this pattern as "sending out a scout." Instead of attempting to implement a feature blindly, a developer tasks an agent with building an isolated proof-of-concept just to uncover the "sticky bits" and understand how the external system actually behaves [cite: 20]. 

**Dynamic Exploration and Probe Scripts**
Recent research strictly quantifies the value of this approach. The 2025 *Mini-SWE-Agent* paper compared agents using static code analysis versus agents utilizing "dynamic exploration." Dynamic exploration allows agents to write and execute "probe scripts" to empirically discover API transition mechanics, action mappings, and boundary conditions. The ablation study revealed that static analysis alone yielded a marginal 4–5 point improvement, whereas dynamic exploration resulted in an overwhelming +60 point gain in task success [cite: 21].

In enterprise multi-agent architectures, this is often formalized into a distinct "Probe Agent." This agent operates as a strictly read-only component tasked with querying system states, running bash commands, and gathering telemetry without mutating the environment [cite: 22].

**Temp-Cloning for Codebase Research**
When dealing with public dependencies where source code *is* available, agents burn through massive token budgets if they attempt to blindly grep files [cite: 23]. To solve this, developers are utilizing tools like *RepoPilot* and *DeepWiki MCP*. These tools allow an agent to execute a shallow clone (`git clone --depth 1`) of a public dependency (e.g., the React repo) into a temporary local sandbox [cite: 24, 25]. The agent then indexes the repo locally and performs semantic searches or executes probe scripts against the dependency's test suite to extract exact usage patterns, completely bypassing token-heavy cloud retrieval limits [cite: 25, 26].

### (b) Concrete Recommendations for Workflow
*   **The Scout Pattern:** When introducing a new library or interacting with a black-box CLI, do not ask the agent to integrate it into your main app. Open a separate directory and prompt the agent: "Write a characterization test suite for [Tool/API] to verify its behavior and error states." 
*   **Persist the Learned Behavior:** Once the probe scripts pass and the agent understands the API, command the agent to summarize its findings into a `[ToolName]-integration-guide.md` file. Stash this file in your project's docs folder to be used as high-signal context for future implementation [cite: 20].
*   **Equip Local Cloning Tools:** Provide your agent with CLI permissions or an MCP server (like DeepWiki or RepoPilot) that allows it to shallow-clone upstream dependencies into a `/tmp` directory. Instruct the agent to analyze the upstream test files to determine correct API usage.
*   **Red-Green TDD Enforcement:** Use the instruction "Use red-green TDD" as a mandatory prefix for all probe scripting to ensure the agent writes assertions before it writes execution logic [cite: 27].

### (c) Citations
*   [cite: 24] Continue.dev, "Codebase Documentation Awareness" (2026)
*   [cite: 25] RepoPilot, "Building a Local AI Agent for Understanding Entire Codebases" (2026)
*   [cite: 21] Boulet et al., "Mini-SWE-Agent: Compact Agent Architecture" (2025)
*   [cite: 22] "Multi-Agent Collaborative Framework for Intelligent IT Operations" (arXiv, 2025)
*   [cite: 18] Microsoft Azure Blog, "Learning tests and how they help" (2021/2026 relevance)
*   [cite: 20] Simon Willison, "Parallel coding agents" (2025)
*   [cite: 27] Simon Willison, "Engineering practices that make coding agents work" (2026)

---

## Topic 4: Document Lineage and Provenance in Docs-as-Code

### (a) Key Findings on Lineage and Metadata

As AI agents increasingly consume, generate, and edit engineering documentation, the traditional "docs-as-code" methodology is breaking down. When an agent reads an Architecture Decision Record (ADR) or a system prompt, it needs to know the context of that document: Is it current? Does it supersede another rule? Was it generated by a human or hallucinated by a previous agent session?

**The 12-Factor Agent and State Unification**
HumanLayer’s "12 Factor Agents" framework explicitly calls for agents to be built as "stateless reducers" where execution state and business state are unified [cite: 28, 29]. In this paradigm, context is not a passive repository but an active, governed state machine. To prevent context poisoning, metadata must strictly define what information is allowed into the context window (Factor 3: Own your context window) [cite: 28, 29]. 

**ContextNest and Governed Artifacts**
Recent academic work proposes formalizing document provenance for AI. The *ContextNest* specification (2026) treats agent context as a "governed artifact"—a versioned, cryptographically verifiable knowledge vault [cite: 30]. ContextNest rejects lossy entity-extraction (like traditional knowledge graphs) in favor of preserving original Markdown documents, heavily augmenting them with structured frontmatter metadata and explicit `contextnest://` URIs [cite: 30]. This allows an agent to resolve documents via a topological sort of a `depends_on` graph, ensuring the agent reads prerequisites before implementation details [cite: 30].

*Extrapolation Warning:* While ContextNest provides a rigorous academic framework for cryptographic context vaults, there is thin evidence of widespread enterprise adoption of the specific `contextnest://` protocol. However, the underlying principle of using frontmatter to establish graph relationships is highly validated.

**Lineage in Practice: ADRs and Git Hashes**
Practitioners are adopting explicit semantic linking in documentation:
*   **ADR Supersedes-Links:** Instead of binary "Accepted/Rejected" statuses, modern ADRs use lineage-aware statuses like "Decided, Supersedes ADR 001" to guide agents away from deprecated patterns [cite: 31].
*   **Git Hash Anchoring:** Tools like Atomic VCS emphasize "change identity" via immutable mathematical transformations rather than mutable branch names [cite: 32]. Giving an AI agent a specific Git commit hash in its prompt (or via a tool like `vltansky-commit-to-pr-mcp`) provides a deterministic, point-in-time snapshot of the codebase, preventing the agent from becoming confused by uncommitted local changes [cite: 33, 34].
*   **Data Lineage Concepts:** Applying data engineering lineage principles to text means tracking the "end-to-end record of where a piece of data came from" [cite: 35]. If an agent drafts a PR, the frontmatter of that PR should contain metadata tracing back to the specific Design Doc and Research Spike that authorized it [cite: 36, 37]. 

Platforms like *Oraculum* argue that this level of provenance is mandatory for compliance, ensuring that every AI retrieval and action is backed by an auditable hash-chain of permissions and source lineage [cite: 38].

### (b) Concrete Recommendations for Workflow
*   **Standardize Frontmatter:** Mandate YAML frontmatter in every markdown file in your `docs/` or `agents/` directories. Include:
    *   `author:` (e.g., `human`, `claude-3-7-sonnet`)
    *   `last_verified_commit:` (The git hash when this doc was last known to be accurate)
    *   `status:` (e.g., `Draft`, `Decided`, `Superseded by docs/adr/004.md`)
*   **Explicit Dependency Links:** When writing a plan or an ADR, include an explicit `depends_on:` array in the frontmatter linking to research docs or upstream design specs.
*   **Equip Commit-Resolution Tools:** Provide your agent with an MCP tool that resolves git commits to PRs (like `commit-to-pr-mcp`). This allows the agent to read the historical context of *why* a piece of code was written by retrieving the original PR discussion [cite: 33].

### (c) Citations
*   [cite: 31] "Communication Patterns: A Guide for Developers and Architects" (ADR statuses)
*   [cite: 32] Atomic.dev, "Change Identity & Graph Model" (2026)
*   [cite: 33] LobeHub, "Commit to PR MCP" (2026)
*   [cite: 34] Blackbox.AI Review (Git commit context) (2025)
*   [cite: 35] Decube.io, "Data Lineage Concepts" (2026)
*   [cite: 38] Oraculum.tech (Provenance and auditability) (2026)
*   [cite: 30] "ContextNest" (arXiv, 2026)
*   [cite: 28, 29] HumanLayer, "12 Factor Agents" (2025)

---

## Consolidated Citation List

*   **[cite: 6]** Zylos.ai. (2026). *Context Window Management & Session Lifecycle for Long-Running Agents.*
*   **[cite: 7]** Probl.me. (2026). *Context Limits as a Design Constraint.*
*   **[cite: 8]** Smarter Articles. (2026). *When Coding Agents Forget: The Hidden Cost of AI Context Degradation.*
*   **[cite: 24]** Continue.dev. (2026). *Codebase Documentation Awareness.*
*   **[cite: 25]** RepoPilot / Medium. (2026). *Building a Local AI Agent for Understanding Entire Codebases.*
*   **[cite: 1, 2, 3]** Liu, N. F., et al. (2023/2024). *Lost in the Middle: How Language Models Use Long Contexts.* Transactions of the Association for Computational Linguistics (TACL).
*   **[cite: 4]** DiffRay.ai. (2025). *Context Length Alone Hurts LLM Performance Despite Perfect Retrieval.*
*   **[cite: 9]** TurboAI.dev. (2025). *Why Your Claude Code Sessions Keep Dying (And How to Fix Them).*
*   **[cite: 10]** ShareUHack. (2026). *Context Engineering Guide 2026.*
*   **[cite: 13]** Kukade, V. (2025). *Turning a Coding Assistant into a Cost-Effective Autonomous AI Agent.*
*   **[cite: 5]** EPAM. (2026). *AI Agent Failure Modes in the Enterprise.*
*   **[cite: 14]** CirriusTech. (2026). *AADLCv2: FinOps for Delegated Cognition.*
*   **[cite: 12]** Osmani, A. (2026). *Long-Running Agents.*
*   **[cite: 11]** CollabCoder Framework. (2026). *Findings of ACL.*
*   **[cite: 31]** O'Reilly / Dokumen.pub. *Communication Patterns: A Guide for Developers and Architects.*
*   **[cite: 21]** Boulet, et al. (2025). *Mini-SWE-Agent: Compact Agent Architecture.*
*   **[cite: 22]** arXiv. (2025). *Multi-Agent Collaborative Framework for Intelligent IT Operations.*
*   **[cite: 32]** Atomic.dev. (2026). *Change Identity & Graph Model.*
*   **[cite: 33]** LobeHub. (2026). *vltansky-commit-to-pr-mcp.*
*   **[cite: 34]** Skywork.ai. (2025). *BLACKBOX.AI Review.*
*   **[cite: 18]** Microsoft Azure Blog. (2021). *Learning tests and how they help cover every line of code.*
*   **[cite: 35]** Decube.io. (2026). *Data Lineage Concepts.*
*   **[cite: 38]** Oraculum.tech. (2026). *Fully Auditable AI and Regulated Document Workflows.*
*   **[cite: 19]** Zhan, Z. (2026). *How can manual QA engineers transition into test automation roles?* (Referencing Michael Feathers).
*   **[cite: 30]** arXiv. (2026). *ContextNest.*
*   **[cite: 20]** Willison, S. (2025). *Parallel Coding Agents.*
*   **[cite: 27]** Willison, S. (2026). *Engineering practices that make coding agents work - The Pragmatic Summit.*
*   **[cite: 15]** Reddit /r/ClaudeCode. (2026). *Anthropic says keep CLAUDE.md under 200 lines.*
*   **[cite: 16]** HumanLayer. (2025). *Writing a good CLAUDE.md.*
*   **[cite: 17]** GitHub. (2026). *awesome-claude-code.*
*   **[cite: 39]** Liu, Y. (2026). *The 4 Lines Every CLAUDE.md Needs.*
*   **[cite: 28, 29]** HumanLayer. (2025). *12 Factor Agents.*

**Sources:**
1. [arxiv.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGTGG7zGV7JuLuuPsNSGasmuQeaw8I_zyIQMtOGPHYrJl-Xk7IFyO-S_Z440ByipM58ks9m3peB_bAue7JdBWaDWH1ET5EmbYO9VMHHjDHFCpURHaLPNA==)
2. [aclanthology.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEtO77e4KwS8XKXrEqW6SvfbQ5lPNQpsza9Xom8p02tyTO7p2elZB4WcpAHDY8kjjl-Q2w-6L_495gkTyQUJu-j01Y__-_o36j8UqumWKV69Da_ZyQLQVq2FMsxscY=)
3. [stanford.edu](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHQjK3Oaoooi6IBWxhTDNRF2nPXaqw2JYU_w_cNv8nDPHHhJ4XQaZ5gDta3he38C9EYzXzm46v0pzYug-yDZtL2aK7FRABUi8-9ENIAcrT5HexOFJrc4qlaVy2fOGnVtuob8Tnjh3sWIjRatLPT9pZW4oeIiKehrEOHQX73)
4. [diffray.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEqfnKRHDRYwI8b-y2EnyWLXBrF-BGwSvDk5jB1Dy0E0RPtjr31ftW5uMwkRG6FvN7ETvmAlshDfIqXJWnnqO_5ITq7Jc8EPMAJ9e2NCcJuaLr81D1GsjJOvAsZywNI3g==)
5. [epam.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHDk1oV9bydPQ7ZgddIV0Y5Pdih0uB83pND6xwC32uDodW5o_GUWEFSirCrBu7t0HkfUVgzYRHdMVELt3p5zZQRl5MRDBZJMHPcwl1SH_tQBbD5zytOlx3RBWeqln6VJ8-v1Bc-CVH8-eKKWKGAPopmSjy4H4uz-ExyF4oWuCM=)
6. [zylos.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFvz4Tz5OQUGwFTbQlcTv9etDB23higLC_Go2AE48GM6M9bd9KdTIDPhYCzNrYHAUU0-q1Lm0Lz_1lITS1qhOSruTUdT8Ju7jzJMKJUjF0FpWl2VPMYaV7DdByAbMosI18lP5KTZmfsPfMypOeG92x7w5tMNQ_3__7eSNclAUS53bnvONkljQvnpE4H04xXuxlaDrqyiaepA7ufGA==)
7. [probl.me](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEg6CO5UM43nMB_tzTAJ0rkwApvewcVtb4q3Ud-c-3s5o02271HOpwRbHQHWCcwstc1JxyHH0vNGG8VxXBPa0jOVRlCPE4SHdxI6qKi9UfZJLHK3bwYfTO6W-KcXkTdL5Hm9A3N1v3OHv8bx3wJ)
8. [smarterarticles.co.uk](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGF-PfYroLmcS35xCQnLy5jQycxATO-I4p-tOBYvHoKW5Y8r7-hDONIT3RMs1lrls3LrYTtd1tnORJFicA9ObEfrTJchAvEpk269vKNGBjyUUg1F4Q_uOnSMps8w-LcETzjXYusAFXvBtgEytdenD4zZNavgCCD8Da5Y1aBAa7dbUKDd96REcCi5ecqAQKoisFhHxnX1_YF)
9. [turboai.dev](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFGIXXpykbBri35ijojIxnSDwv6QDIgG5snSTawXnIxzhF_zhw9phK3o1C1tBDqxKlvkxYpz5RGC9lz8utAZO1ZzVYxRkb4isG3h6NCFMWOV8ZBPGCJ30BkUgPrNw4Iza0Vwew5fKIzloGu2WTADvsvfNZ-Uwos7Us=)
10. [shareuhack.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQExekpdKQOWiXJqutnl8gJkzh9qjI9pVsa7feMVvqochwCuetCRj6b3x0leUYi0wD-9uRNZweKkSIC2E-rJANnarXEgxs6SdD3IvSN_8p8nEW19g7qFrPjRhekYUENNT4dbfwPBxJGIzhImVyW_JMfPx4yiV8HNbNM=)
11. [aclanthology.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE41ajtDEfK-Pj7xPKpqKhzGlUXsQCrZOSDCjrlq4sEKUiM-Y9vCOyjK6qu1vJsyJsG7xRl4k46h_yfxBzgY-jSOO2c2dj6QZoYfER3m2B0jWZnPgXODuL7RD1rHz7s_HR1Tjq2z3x2wUc=)
12. [addyosmani.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHklx-2Tjrv0Vm4NCCSCpr4t71vKvfi0DtSWW5e16IWxi-7n45UM40eqP4qNSe3AXcavUnPoUczqiVhMS7xlK5rrBcnGRbJrvmkdTU9otvQfesPM4OB0ZAn3TTtBRkUFf77BdH3RTY=)
13. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGjsF6nP_jqyrd8GnYezHZLsixthivH433UuglWLzGYKVG1r3Oy5JKDRriDYX3aDXWQ2PW1xd-odvRLwMUxGKLv7MDr3gI44TZ2pjEtCM88KJM316umoSYSXC7cexRMWj4YYIgwvwIfyaneoDYoh75Oa7jXeeFQ-c55d841FIHST43NEBIrVS0xfICsSXcrirb_7ykExQegB-dcXiGhylPduXbh9mAmBsphhQ==)
14. [cirriustech.co.uk](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFza8pmy1c0TGgT11JIZROyaKbhxjcqF4Q2Q-l4wdr9zstlU10cC5frDnlFI8aP0mjZZb6gEppyY59jSG9VEVxa1Wa_SLjNbUPlwH8GbbbH7g22qIxGq3gKFzqvTwKlnZ1GUe6oXD-keSe2_RBI8gu4MMnKE116iw_yg7B75yR2A-Omhkk=)
15. [reddit.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEeru28rKqbOcG4P4hzfU15ef4KYAqGTmWm_CO0fb_LYAN37aSJ33CcsnowWVKk0-XxEL3lKpZlxU-gtlQNKAo9MZeCirI4M6UaOZJdq-qfFIYp4H7srgcLn7Tda6pMu86FwsK4o7mhu5_s5rdF3yeWKKyLnMoG3M3hVrV718mT9AMkS6YRFJnVKbSkoukCQ_5B216c8TFKanq11nk=)
16. [humanlayer.dev](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH_Snzk62QJ4SNux8h_D6pLA0GuEYSPzSjF78xYwkdyGGcIVXvmnvsNMa1s_upcUgdKZHmsP5FqfgcKfutLXW8WeWoLKSmfr21Uj_X4yj6I1GPbyr6vvkvmx5mBZV_6kJNhmIFj9-KNGyK9luoS-A==)
17. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHhMN46d_Gt-H2r5VOIhx39eS8-cRIv080ywgo22Mxeg2siw-QpQlW1AALbylm1HReD3GBTui2hg_Mpj5wFs1G78Ag8C3pXqn1ew2d0-H6ktpwzR0DiaF7KqRgKa1PGNcl2G1T0DdPS_Qg=)
18. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHJqTuMC2VG2QmPPhK3mk_fur2h9uk_JkVxlDkAScPMBgAvlRgMBtqMjipfZHAKu96E5dkPZlZUbZhMNm5Et3J6j6diDxQPm-tpQGVLINJanpE7Xx6CNuX5zLUM1cS8gv1X8F-MsgV1jKyc6fNOWv5K_n8hh7AZE-fMkdBz4KCziiX5MWg2g0DPt0hRW6TdSrMcuQ9KPOg0NEOVt4oq)
19. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHwXm3N-ZMhxUg6SCNOJQ0p1826O0mPnr6S5q2mh5EHROwsKd9NnuC892VRpQK7k5U1Y3GprHSXVAU_4iblBr6IVGL43pNVal0wZLJGWv2n51kFxgRRBoYAyz5xhzuI0nA8WgWx94tV8u6KWxxX_Ak8k3kXxd3RaWfdYhbx9xZjH_Y3u3s0kD9lhlE74gjqOGrNodIQmHBffpdNJow6XiLfWBM=)
20. [simonwillison.net](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQElvAX9pk_RicFQnajvpwAS-Qc_zBcpZTyMduHre2GakPKa63-0WYvdRTm-2ykzXugfJBQti3euesscS_PF02CNaitXmR08HUKRYhW1J5q1wY4M99UFBTB_1hAOJtIli7QQF6f4yAtfS9i3WFIxjcRnQZ4=)
21. [emergentmind.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEEOxMzRoEUZKXccdV3HJeRVRFi7NZ8ePMuR_15kNIzLLBooTcMfWRFcW39bPpOg7hJYvQswfUf92lA6gLByFUudEn-2-izJxOFndEeJDu6QVpjoSxcKWB83nzZ_nBQp_B4gkMODlkFCg==)
22. [arxiv.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHuip9XyxyaAxbMe3tW_INQ9XZuqb8Q3sbzsTpK8_0iB3uGgjInFU1V6Dy6S_3TGy0YTAgr6RHUuheDal4H1-WFchIOo0OHDkMawrWxLQ3AmrDBpldXN_g6Yg==)
23. [sentra.app](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF0aAHB18nL_rOE1egXZ-6ze0Z9RRso9PwdWMq1qu-gLGAZ16VyX_KrTQdzEEilOMtwbhdaDb0PfCog8lixqiqxBtbew2Dm648imE6rskWu9RiisOuy2Fj8la7jyX9qsYffpB5eCqhoDABn0QnKaFc_s0Lo9O--ShE=)
24. [continue.dev](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGC7n6DerJ0BculRkHubO6JDVudvr1F03M0fHh3ClRE1LUL8Gi6IxeRbzaoocxgTCjRtbIewqmN9CSWtRsFBPk0GBPXo46EfonVjqpdhvcjAr0fLTpwpKu-kUqMXd_JOzjrjKRoNVAtvxxHCOKexov4LtHrfUIyTg==)
25. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHk3xgMwrYlU7-iXEP7I-MwHHouFT3BTRuOvkJ_wS9a9k7ZiSFqOnq9alNayQhcrwGBKGhtAOKtWl9pq493Wr_lWwUeN9CAwDBKLzARtQ45-RibO9cgzT2Vcm6UWewVzC2AnuS2jzaKEqb_gSHZZ3tsvL1Gb3vR1Y76JJ55yxbuZoB6noSIOSW5rPtVKdfX_kYpuv6ocL5DCLgNnaG3_Io=)
26. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGDHeDqb8Km7pv6MH3_4m-rW9c-o3Jau90K5d4ElNBB2PpoZGzcIZNEd8NVmwLEUnWfvnKKGb5nvu8ThdD3fo4wb-pONY6BZQOKJ6o5vAKhVaX2n-di3jIZWVhHur6KLWDDNw==)
27. [youtube.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGrAvmvj39EQQzkk3kB-AjhrTJMRKGD8E6dmDnoJH1MDgcnUb6QmXMOFIG05lWMudo9TLsDqn4jVd4SNmvJI6nbSfCf0qQhsp-9Vkg-dm6l8sDYZvPB9CH-mtm2fbhhRTQo)
28. [paddo.dev](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHRM53yCmHY3Bks5dTcedsjtS9SPHLzv1BJuf5Cm7do2rxzh52vmOnYM5ekTkqsPwVJBNVCi5kPcuaUhnOqeKF5nVRhFGuJ-Gd8yfWRmrKEwUXo4C6UzZDJrefBKSEA)
29. [youtube.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEvh9OC9gdcG9AloHNr3NKnn-Bp8Y5miCJs16QnbWSO08tpDwk53TPTcfxEoLblL-YKSyXPpks_xPItbz9coSmXy8y9Ay4aD2_VAYkhC9sw8nukefEugge8U_7AHkeK5pwq)
30. [arxiv.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGuyp0fvO4mrd40tlhuDx5AbkvXNkYYyH5rmKEbuvH8TkzlzM1d5VHB_6cw8V72HmOtTMpFW9Dx8Kea-OOU0e2NFf_lLarDqU6mt62oaMvMZRsyma6zw6o8Sw==)
31. [dokumen.pub](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF4RGt71cfOXFbcO3uTHDtRI7iDDkzu6sLEvNtBxyxO1nJ6R0zuDpZxEAEL8JyJldWr5TYRLBjYtlqhWFbUMf22WwC4gpX-hUqcC7L3vtXLPX0JmO479ABaHgFZ7M0Btwuk-S3ED6c6iNCjzArZ1vEVoZHYn4OLBcdR4I-LcxVrNbE_hsTu5cXJbH81XZbGOHfkZC1mtBiNJJtreEGkQYVc-xcGxYuyH-_9Rfov)
32. [atomic.dev](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGGXWC81SpY6MDLhhp_1xrCgMZ1_tNivZIJsifY9wLZdf16uh15Em5e1qj6rLB7H37feJew2cA-SlDwk-nlfRiSEhmcYUNcsCky6mRNzfax8JPnkBUcfSygYgSL1gMc0ASlnCkElUg=)
33. [lobehub.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGCB82isnI3f5qNTrsFurzparGHMeTVr9wuIsRv_Vj0h4I16g56KuJrg6rR7RTyJj4NAvoR5kvGY-VZYMzLmjqzf6IY910jLAPHOlfwr-fmxtTPCczLiDItIVxSEyO9DrkTDXg-Ncud)
34. [skywork.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFuetp9O6cDxRKeOnDaI5dgZuHThXW6xGJRTChVzon51OwIBxrnp_1-m96qmXCxtdvtYAJqWOp7yIVbLXY7A4SyBR2Wd0BajaiBD_4Yzlw8ivZif_iv0EpQLz1K9twWwqHyotRlaoBeLvpGrHx-Xti9a8-GMQz8GFUm9GHov8yfCu42HiUIHnER9PIVs09Er_JoVt1DFWZelVVkEdp5m30qiKn0qsFeJMk=)
35. [decube.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEArq8hPqNlsUEpIkcdBXQUGpS5dSgtIcKfnMCty-5XJmBVi9QT-tiHPK4ecDLblNyMd6wQjKkA5hLwhrZ_qiYBq6PpNEGV5jX5bOp4_U2xpaiQGiG3nMjK4gZwzqmmz1_k2Hfjmb8=)
36. [optaize.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGk-sVIvmHu2szEJ-tI4l3XVHks7Sona3S_VNPcDa9acTD4syIUGc0eykQ9BTMSloAfGc30Srx5hlx6x1U0aIEzdVwr9d_3Pmn9RJwZVg==)
37. [latentview.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHuIDOiYecxadYICn-JvfHg4wqw-rlq2Qt7UqeXZ0iK4ufukSP3K5tSkKma6woag4KG_AfRxKMG4iOGGt7P7--GzZr_r2GJ-PsfcT6fflqLTiTAN446ElCUSL_v0lZcodgMaAqeBRPwXK42sCHd)
38. [oraculum.tech](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGhOUN72IayL1C9Pze8bBBJ2JTYT1wnEtzdeCX1Q0XL5_ggDe4fcEjD_tByw0pNmlvxxOQ1XLc8BhuQowsbPUP2OIoayfKGfhPCGii5)
39. [gitconnected.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEi2D7jF1Qc6BI6uwrhj2YuFhFxKMdCD9ZWdno4fvWWKEhl7kBLdw0VWqJAerNkav9Msebt-FSjqR-1W5fj63lPTj5amTRNfug-N180y6pus-RigjsSREw5OlK4tMlM4APaxig4ye4jPoIxUZlJmtdF7tofRywSFXgdAopx4LKgIxdJAlwn)
