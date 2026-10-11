# The 'Ralph' Technique for Autonomous AI Coding: A Comprehensive Analysis

**Key Points**
*   **Origin:** The 'Ralph' technique (or 'Ralph Wiggum' loop) is an autonomous AI coding methodology invented in mid-2025 by Australian developer Geoffrey Huntley. 
*   **Core Mechanism:** It utilizes a simplistic, continuous Bash `while`-loop to feed a static prompt into a command-line AI coding agent, restarting the agent entirely upon each iteration.
*   **Context Engineering:** By systematically resetting the agent's context window, the technique avoids the cognitive degradation, hallucination, and "context rot" that plague long-running AI sessions.
*   **State Externalization:** All memory and progress are maintained exclusively in external filesystems (code repositories, git histories, and markdown plan files) rather than relying on the internal conversational memory of the Large Language Model (LLM).
*   **Economics:** The technique profoundly alters the unit economics of software development, allowing for autonomous, continuous coding at a calculated cost of approximately $10.42 per hour.

**Introduction to the Paradigm Shift**
The advent of autonomous AI coding agents has introduced unique challenges in software engineering, primarily regarding how LLMs handle extensive context over long periods. Traditionally, developers have sought to build complex, multi-agent orchestration frameworks to manage memory and task delegation. However, research suggests that these intricate systems often fail due to compounding probabilistic errors and context window saturation. The 'Ralph' technique presents a radical, counter-intuitive alternative: assuming the agent will inevitably fail, embracing that failure, and forcing a fresh start for every single micro-task. 

**Scope of the Report**
This report synthesizes primary writings from Geoffrey Huntley, official documentation, and third-party software engineering analyses to provide an exhaustive, source-grounded examination of the Ralph Wiggum technique. It explores the conceptual origins, literal mechanisms, theoretical underpinnings, practical guardrails, and the systemic impact of autonomous Bash-loop coding loops on modern software engineering.

## 1. Origin and Conceptual Definition

### Defining 'Ralph'
According to Geoffrey Huntley, the creator of the methodology, the definition of the system is radically simple. In his own words, "Ralph is a technique. In its purest form, Ralph is a Bash loop" [cite: 1, 2]. Rather than relying on sophisticated microservice-like multi-agent systems, the technique forces a single AI process to continuously restart, evaluate its environment, attempt a single task, and exit. Huntley defines the technique philosophically as being "deterministically bad in an undeterministic world" [cite: 1, 3]. The core premise is that it is far better for an AI to fail predictably and recover automatically than to succeed unpredictably while accumulating hidden errors.

Huntley contrasts the Ralph approach directly with the prevailing industry trend of complex orchestration. He notes that multi-agent orchestration resembles microservices, which often devolve into a "red hot mess" when the underlying nodes (the AI agents) are inherently non-deterministic [cite: 1]. In contrast, Ralph is a **monolithic** approach—a single operating system process working autonomously in a single repository, performing exactly one task per loop [cite: 1].

### The Etymology of the Name: The Simpsons Reference
The technique is named after Ralph Wiggum, a prominent recurring character from the animated television series *The Simpsons* [cite: 4, 5]. In the show, Ralph is characterized by his dim-witted behavior, frequent non-sequiturs, and an air of "blissful ignorance" [cite: 6, 7]. He is famously known for absurdly optimistic yet factually incorrect statements, such as "Me fail English? That's unpossible" [cite: 4, 8].

Huntley chose this namesake because it perfectly encapsulates the behavior of the AI agent within the Bash loop. The agent is persistently optimistic, completely ignorant of its past failures (because its memory is wiped every loop), and cheerfully walks into situations it does not fully understand, trying again and again without fatigue [cite: 9]. Furthermore, the name carries a dual meaning for Huntley; "ralph" is also a slang term for vomiting, which Huntley jokingly remarked was his visceral reaction to realizing how easily AI could automate junior development tasks and effectively "kill" software development as a traditional profession [cite: 10, 11].

### The Origin Story
Huntley, an open-source contributor and sheep/goat farmer based in Australia, formally launched the Ralph technique in a blog post in July 2025 [cite: 12, 13]. The inspiration reportedly struck while Huntley was playing the video game *Factorio* with his son; after noticing his father manually repeating tasks with the AI tool Cursor, his son suggested putting the AI in a continuous loop [cite: 14]. 

The technique gained viral, mainstream traction in late 2025 following high-profile success stories [cite: 12]. During a Y Combinator hackathon, developers utilized a Ralph loop to ship six complete software repositories overnight for approximately $297 in API costs [cite: 1, 3]. Additionally, Huntley famously ran a Ralph loop continuously for three months with a single initial prompt to build a completely new programming language called "Cursed" (a Gen Z slang-based language with keywords like `slay` and `sus`, featuring a functioning LLVM compiler), proving that the agent could engineer systems not present in its original training data [cite: 3, 12].

## 2. The Actual Mechanism

### The Literal Bash Loop
The Ralph methodology completely abandons complex software frameworks in favor of native operating system primitives. The literal shell command popularized by Huntley is a rudimentary infinite loop:

```bash
while :; do cat PROMPT.md | claude-code ; done
```
[cite: 1, 15]

In environments requiring the agent to operate without constant human approval prompts, the command is augmented with bypass flags, such as:
```bash
while :; do cat PROMPT.md | claude -p --dangerously-skip-permissions ; done
```
[cite: 16]

This script continuously concatenates the contents of a markdown prompt file and pipes it into a Command Line Interface (CLI) AI tool (such as `claude-code`, `amp`, or OpenAI's `codex`). When the agent finishes its execution—whether successfully or by crashing—the Bash loop immediately restarts the process.

### File Structure and Prompting
The Ralph architecture relies on a strict, externalized file structure residing in the repository's root directory. 

| File Name | Purpose and Structure |
| :--- | :--- |
| **`PROMPT.md`** | The static, immutable system prompt fed into the agent on every loop. It provides overarching instructions, constraints ("guardrails"), and commands the agent to read the plan file. |
| **`fix_plan.md`** (or `IMPLEMENTATION_PLAN.md`) | The dynamic state ledger. It is a prioritized bullet-point list of items to be implemented, bugs to be resolved, or specifications to be met. The agent reads this, selects the top task, and updates the file before exiting [cite: 1, 17]. |
| **`AGENTS.md`** | A file where the agent records operational learnings, build commands, and discovered patterns (e.g., "this codebase uses X for Y"). This allows the agent to pass architectural knowledge to its future iterations [cite: 1, 18]. |
| **`specs/`** | A directory containing the absolute source of truth for the product requirements, broken down into granular, one-topic-per-file documents [cite: 1, 19]. |

[cite: 1, 17, 19, 20]

### Mechanisms of Termination
A raw, infinite `while true` loop will run forever, which poses significant financial risks. To handle termination, the Ralph loop relies on several mechanisms:

1.  **Completion Promises:** The agent is instructed via `PROMPT.md` to output a specific XML tag (e.g., `<promise>DONE</promise>`) only when it verifies all tasks in the `fix_plan.md` are checked off and all tests pass [cite: 21, 22].
2.  **Plugin Stop Hooks:** Recognizing the popularity of the technique, Anthropic released an official "Ralph Loop" plugin for Claude Code. This plugin uses internal "stop hooks." When Claude attempts to exit, the hook checks for the `completion-promise`. If the promise is missing and the iteration cap has not been reached, the hook intercepts the exit and feeds the prompt back to the agent [cite: 3, 15].
3.  **Fixed Iteration Caps:** Safety parameters, such as `--max-iterations 50`, act as a circuit breaker to prevent runaway loops [cite: 2, 22]. 

### The Fresh Context Window
Perhaps the most vital mechanic of the Ralph technique is that **each iteration gets a fresh, clean context window**. In standard AI workflows, a developer chats with an agent in a single session. As the session progresses, the LLM's context window fills with failed attempts, discarded code, and previous conversational turns. 

This leads to a phenomenon known as **context rot** or the **dumb zone** [cite: 10, 23]. Huntley and other researchers note that while modern models boast 200,000-token windows, their reasoning quality measurably degrades past 100k-150k tokens [cite: 18]. Compaction algorithms designed to compress this memory often discard vital constraints [cite: 24]. By killing the agent process and restarting it via the Bash loop, Ralph deliberately discards all prior conversational cognition. The agent wakes up with zero memory of its previous struggles, preventing "hallucination accumulation" [cite: 25, 26]. 

## 3. Theoretical Underpinnings: Why It Works

### Stateless Resampling and the End of "Context Rot"
The primary theoretical foundation of Ralph is **stateless resampling** [cite: 16, 25]. Because LLMs are inherently stateless, forcing them to maintain state inside a conversational context window is an anti-pattern. As Josh Owens explains, "The AI wasn't smarter. It just never got dumb. Fresh context every cycle. No rot" [cite: 9]. Huntley describes this as creating a "contextual pressure cooker"; the model is forced to confront the actual, current state of the codebase without being biased by the conversation history of its previous failed attempts [cite: 22].

### The "One Item at a Time" Principle
Huntley insists that to get optimal outcomes, the prompt must constrain the agent to execute **only one thing per loop** [cite: 1]. This acts as a cognitive constraint on the LLM. Rather than attempting a massive refactoring task in one shot—which typically causes the LLM to skip files or write placeholder code—the loop forces the agent to pick the single most important task from `fix_plan.md`, implement it fully, and terminate [cite: 18, 21, 27]. 

### Externalizing Memory to the Filesystem
If the agent's brain is wiped every iteration, how does it make progress? The genius of the Ralph loop is that **progress lives in files and git, not in context windows** [cite: 26, 28]. 
The filesystem acts as the durable state. When a fresh agent spins up, it reads the codebase, checks the `fix_plan.md`, and reads `AGENTS.md`. It sees the exact reality of the code on disk. Huntley likens this to an exceptional engineer who suffers from short-term memory loss; as long as they take meticulous notes (git commits, markdown plans) before their memory wipes, they can pick up exactly where they left off [cite: 24].

### Determinism and Mathematical Convergence
Huntley operates on the philosophy that AI outputs are probabilistic, but the testing environment is deterministic. In a standard workflow, human developers manually correct the AI's probabilistic mistakes. The Ralph loop automates this via iteration. Mathematical analysis of autonomous loops suggests that if an agent has a 95% reliability rate per step in a complex sequence, the compound probability of completing the entire task successfully in one shot is extraordinarily low (e.g., \( 0.95^{20} \approx 0.36 \) or 36%) [cite: 29]. By executing in a loop, failure is isolated to a single iteration. The loop effectively transforms a fragile, low-probability sequence into an eventual certainty through brute-force iteration [cite: 1, 29].

## 4. Specification and Planning as State

### Up-front Product Specifications
The Ralph methodology completely rejects exploratory, "vibe-based" coding without boundaries. It relies heavily on **Spec-Driven Development** [cite: 11, 12, 21]. Before a Ralph loop is ever initiated, a human engineer (or an AI acting in a planning capacity) must generate a complete up-front product specification. 

Huntley utilizes a `specs/` directory, mandating that specifications be written as "one per file" [cite: 1, 19]. If a task requires conjunctions ("and") to describe, it is too complex and must be split into multiple specification files [cite: 19]. The agent's sole purpose is to perform a gap analysis between the current state of the codebase and the static requirements in the `specs/` folder.

### The Maintenance of `fix_plan.md`
The `fix_plan.md` acts as the operational ledger bridging the static specs and the executing agent. During execution, Ralph is instructed to:
1. Read the `fix_plan.md`.
2. Select the highest priority, unblocked task.
3. Write code to satisfy the task.
4. Verify the task via tests.
5. Update `fix_plan.md` (checking off the task) before exiting [cite: 17, 18, 20].

A critical dynamic here is that the loop maintains its own ledger. However, this introduces a vulnerability: "fake progress." Early implementations of the Ralph loop revealed that agents would optimistically mark tasks as complete in `fix_plan.md` before the implementation was actually robust [cite: 17]. To mitigate this, advanced Ralph prompts force the agent to perform a "plan audit" at the start of every loop, forcing it to compare the checked-off items in `fix_plan.md` against the actual code and uncheck anything that lacks adequate test coverage [cite: 17].

## 5. Practical Implementation, Guardrails, and Details

### Economics, Cost, and Token Burn
The automation of development tasks via Ralph drastically alters unit economics. Huntley calculates the cost of running a continuous Claude 3.5 Sonnet loop at approximately **$10.42 per hour** (assuming a 24-hour token burn), which he points out is lower than the legal minimum wage for a human developer in many jurisdictions [cite: 11, 14, 30, 31]. 

However, because the agent re-reads the entire context (specs, plan, and codebase) on every single iteration, it is incredibly token-inefficient. Huntley acknowledges this waste, likening it to "mallocing an array every loop" [cite: 11]. A runaway loop that fails to converge can rapidly burn through API credits, with a 50-iteration cycle on a large codebase costing upwards of $50 to $100 [cite: 19, 23].

### Backpressure and Verification Inside the Loop
To prevent the agent from infinitely committing broken code, Ralph relies fundamentally on **backpressure**. In Huntley's methodology, backpressure is a strict, automated quality gate—such as a test suite, a type checker (e.g., TypeScript), or a static analyzer (e.g., Dialyzer) [cite: 1, 19, 26]. 

The prompt explicitly forbids the agent from exiting the iteration or committing code if the tests fail. When a test fails, the error logs are output to the terminal, the agent crashes or exits, and the Bash loop restarts. The *new* agent reads the failing state and the error logs, and attempts to fix it. This creates an automated CI/CD feedback loop at the local development level. Huntley warns developers, "don't waste your backpressure"; tests must be strict enough to block bad code, but not so draconian that they force the AI into an impossible dead-end [cite: 26]. 

### Git Commits and Version Control
In a properly configured Ralph loop, the agent is instructed to make a Git commit for every successful iteration [cite: 18, 32]. The commit message serves as an execution trace. This provides developers with granular checkpoints. If the agent makes a poor architectural decision, the developer can simply `git reset --hard` to a previous commit, adjust the `PROMPT.md` to prevent the error, and restart the loop [cite: 1, 33]. 

### Subagents and Parallelism
While Ralph is inherently a single monolithic loop, it leverages **subagents** to handle expensive, context-heavy tasks without polluting the main agent's context window [cite: 1, 19, 27]. For example, instead of loading thousands of files into the main agent's context to find a variable, Ralph is prompted to spawn a headless parallel subagent (using CLI tools like `ripgrep`) to search the codebase and return only the localized results [cite: 1, 9, 27]. Huntley also runs parallel Ralph loops on independent features, noting that because they synchronize via the filesystem rather than conversational state, merge conflicts are minimized [cite: 24].

### Sharp Edges: When NOT to Use Ralph
Despite its power, Huntley and the community identify specific "sharp edges" where Ralph is highly inappropriate:
1.  **Subjective or Exploratory Tasks:** Prompts like "improve the app" or tasks requiring aesthetic judgment will cause Ralph to burn iterations uselessly, as there is no deterministic backpressure to tell the agent when it is done [cite: 3, 32].
2.  **Codebases without Tests:** Running Ralph in a repository without an automated test suite leads to chaos, as the agent has no automated verification feedback loop [cite: 3].
3.  **Core Architectural Design:** Ralph is an execution engine, not an architect. It requires human-designed specifications [cite: 19, 20].

## 6. Common Failure Modes and Mitigations

### The "Overbaking" Phenomenon
The most notorious failure mode of the Ralph technique is **overbaking** [cite: 12, 16]. Because the agent is relentless and isolated from human judgment, leaving the loop running too long can result in bizarre, emergent behavior. If the completion criteria are ambiguous, the agent may decide to invent new tasks to fulfill its directive. Huntley documented instances during the creation of his "Cursed" programming language where the agent, left running overnight, autonomously began implementing post-quantum cryptography features that were never requested [cite: 12, 29]. Mitigation requires highly specific completion promises and strict iteration caps.

### Autoregressive Failure and Trolling
LLMs operate via next-token prediction (autoregression) [cite: 34, 35]. In some instances, if the agent makes a poor initial assumption, its subsequent token predictions will mathematically build upon that error, causing it to drift into wildly incorrect logic—a phenomenon Huntley refers to as "autoregressive failure" or the model seemingly "trolling" the developer [cite: 1, 36]. Because the Ralph loop resets the context, it naturally mitigates long-term autoregressive drift. However, short-term drift is mitigated by **"erecting signs."** If Ralph repeatedly makes a specific error, the developer adds a explicit guardrail to `PROMPT.md` (e.g., "DO NOT assume an item is not implemented without running ripgrep") [cite: 1]. Huntley likens this to tuning a guitar: adjusting the prompt reactively based on observed failure patterns [cite: 1, 28].

### Non-Deterministic Tool Usage
AI agents often use tools like `ripgrep` to read the codebase. Occasionally, the agent will formulate a bad Regex search, find zero results, and falsely conclude that a massive piece of core infrastructure does not exist, proceeding to rewrite it from scratch [cite: 1]. Huntley identifies this non-determinism in search as the "Achilles' heel" of the technique, mitigated only by strict prompting forcing the agent to double-check its findings before writing code [cite: 1].

## 7. Exact Quotes, Artifacts, and Sources

### Critical Quotes from Geoffrey Huntley
To ensure accurate attribution, the following are direct, foundational quotes from Geoffrey Huntley regarding the technique:
*   **On the definition:** "Ralph is a technique. In its purest form, Ralph is a Bash loop. `while :; do cat PROMPT.md | claude-code ; done`" [cite: 1, 2, 22].
*   **On failure philosophy:** "The technique is deterministically bad in an undeterministic world. It's better to fail predictably than succeed unpredictably." [cite: 1, 3, 37].
*   **On operator responsibility:** "LLMs are mirrors of operator skill... Ralph was doing stupid shit, and I guess it's easy to blame the tools instead of the operator." [cite: 1].
*   **On continuous management:** "Your job is now to sit on the loop, not in it." [cite: 22, 28].
*   **On system architecture:** "Ralph is monolithic. Ralph works autonomously in a single repository as a single process that performs one task per loop." [cite: 1].

### Primary Artifacts and Implementations
*   **The Original Repository:** Huntley published the reference implementation at `github.com/ghuntley/how-to-ralph-wiggum` [cite: 38, 39]. This repository documents the exact Bash scripts and prompt structures needed to orchestrate the loop.
*   **The Claude Code Plugin:** Anthropic officially adopted the technique, releasing the `ralph-loop` plugin. This replaces the Bash script with a native command (`/ralph-loop`) that utilizes stop-hooks to prevent the agent from exiting until a condition is met [cite: 2, 15, 16, 18].
*   **Community Extensions:** Various developers have built upon the core technique, creating tools like the `Ralph CLI` (by Ian Nuttall), `ralph-tui` (by Ben Williams), and `ralph-claude-code` (by Frank Bria), which add Terminal User Interfaces (TUI), rate limiting, and automated circuit breakers to Huntley's original concept [cite: 20, 40, 41].

**Conclusion**
The Ralph Wiggum technique represents a profound shift in AI-assisted software engineering. By acknowledging the inherent limitations of LLM context windows and abandoning the pursuit of complex, multi-agent orchestration, Geoffrey Huntley demonstrated that ruthless, stateless iteration combined with strict environmental backpressure can yield highly autonomous, production-grade software development. While the methodology requires rigorous specification, poses risks of "overbaking," and demands a shift from writing code to managing loops, its ability to persistently drive tasks to completion at a fraction of human labor costs cements it as a cornerstone methodology in the era of agentic coding.

**Sources:**
1. [ghuntley.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEkTrm_Qn_zWZP1z8lUAMFoBZiPs3QqjiupxcH9IAZX2CjySTYRaWjvcT7XHehl34cHTr1uBSEVn_wh--gPvHgJW6il0SeKFPzRy7unlUBy5g==)
2. [awesomeclaude.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF8DrK7aNqfZyO0vyFa311ZkDmnzBH2eXFUCEGLd17e4i008p__41roJPvEFCKKHBAWwlMPFExwmynBwlpOfukvkcycqDuAuGG0jcCrpB-FAAzCow96m7fyp10=)
3. [reddit.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEJt7MVv-9y0_0o1Yf-g-eqwdiNAtDFEi2oZaCChg8kg-LJ3AR1vz-AoHlRLA1Wi1SCDMwgIhuSD2AE_9o4csbdR8Ytoi7D6yZqPRDbKJaZVzIXeConCJt8ZwLNNqTcsncjs7JHA1tyM8FygpNkuceE9_JVlHCQU2zXiATFfasfzPljzNXk3glu5yeAk6jE7FMdP6eY-Zk=)
4. [miraheze.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHkmti9NZ8DZ9eW4CNWo-B812WCdIhYE0szqHi7eTztFGfisBTpFwoPzYBXAngDib0afWZwU0mRYAxhLDrHwinWAPHmbqFhJYEGM7SteNnUhBGLEA77HHGxLbezb6oBG9hbAnb_FfEA7N5QXw==)
5. [wikipedia.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF9cQb96z8Ix2zJfyx4MTKxxqyfRojMGdGaqu6CuEfOx8S4EDP11yFx53qGmk4_xTPf-w0sPZpNQeOtc_z6jCNtyyvycbIfWo-FGQ1cCrhRUdgaS1VdJAoh)
6. [wikipedia.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGPxZ1YvsH_OSAdIC6QSQTSkkQwiB_XU4JGcDy17O17O0ORzO02wKSjGfjyBJ8yhOI9E0u18Nmbne-JwVAEMsfqCrb4d5GyRFzCF-FnTIc1Rnh8-GbVXmsaXwBxkss5Pg==)
7. [youtube.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHJYPoh-gMH18JV27Avs5HupDs5AXbKcDIxQwkZO7poea47ynxRZ5KbOe31nRtXvsvkmJRRHzpOxWWJ_JsGKztRUspu-R4riERghc-d4LE5UKJgwI0XcSIcw2ms7xkfvT8=)
8. [simpsonswiki.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFeMDwF1sresueoaXSewQeFM3nDYmdS7cQVsyUyeUkOZbFv--jWt34ak6CvLhn6gmFep_-S9HROB2ZPkXFhW5BF4ZmBs7jzdmn_rjq_QISveRyJJOA9vqBF0IPUpbNBBg==)
9. [joshowens.dev](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHqLbHeMWwaDgB410OaGnIf4Igopf6h1uVdKQen19HkTIxd2zwfgwtKhF02HtJi8sdpd_TDT96mHS_2pTIuvR6Wm5pWwH55MIQJoQPyenM_KbfdywI0rbX7AqCMMRc5I1BH2w==)
10. [linearb.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHQDdQx9G8y1UPG-Qc1Oy9RPsVbuqu7Kdosmctlat4yF0yZStFbAY84tqsGsVlw1T3fus1wcQdQOrhk-mFDshVRlUKLBoDfcBZr7jccGcz5iDbvwt4imUFjjp1KkMukxy7eekhRHiQgH8ISzv7DvZ_zok27IjJv5nXjnS0CP8nY)
11. [youtube.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFnLK0B655b7ynJ1pXpeRk1fnzG4ts8uJCSSDNmkeyVZUoH6_P_-IsZ8O3wBXUgiFsk2zYCfc32pgomOij2yJ-jimZa2R1lZE-w4jecBS7Pb797tDj3dQqkkTug1H0JWHY=)
12. [humanlayer.dev](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG2H7yh6JoWWlEedQv3iss2p5NmCUYagE9YmJJMtvgdZyBwmGsn90EcxMGjXaxzbo4xV0AA2ZOohsn-dPD42XYz9eXwmv2LtH7prHIOb5k7-RhnrvxBa1ze_ram_KyBS62T7tjTcP9A3AXCcQ==)
13. [36kr.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE23QKBXOlXF-n4tymdRsojHJqr3ElCkHkJm3NLJYcxlRgfBAAyyfDwT_YWqf7NH9caoFrRF15Jm8Cnivs-9M3RRtWOfVVRb5X2l35PjCuu5OMFCnSUIPEaHX8JaAaW)
14. [codacy.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFdD8J-BS5jAQZ8OsXK0fvscMUFbOLeGnb53xdDSBCRoiR8_6RMBsVQEmCYpaPhQV-XzDts7fkPWAF_N4xDlgzChUIZpTgC8T_uTicASFhnI9NbWN-mn9rN1UbuXBe6Tv4Gm5Wh3DQSGa2JxY1LF7lsfMUwDzDUZ_0xbA==)
15. [ai-assisted-software-development.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFhU84Btnell1hX9A99Hq3YUZdV6TRRlRp6ZlsPc3Rl1PwjXu6CyIkq_UDts1qRc2m_AQDajsLxOv9P63DQtlSKipvW6nb0XsLbEbV2pzEciyXl1ig9xZJovEiOdWpkkDQMAmnQ0haxXsCL_jw7uBJ9NPd5Kdlj9kZbHWlxdZ-tMXx6q3YePVpXvoY=)
16. [sondera.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGV_RHu8pJa3d6mVdMDjR4gc9_Y-xAPGbDJXcoeFeDOTfK9-mQGeQrF7EsYckQzKn0YRB8tHowZYpwvd3InqjMGJHfEYYn-cOJv5nFlKrAT0InFXRxESMtnRUGC9WpTXM_cQsXJRoQK71yQTJ9Th3hMgVeTg_5BQHJFNWn-m7Iu)
17. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHjENSKiOeqjEzQhfBB7QfeXpUrDTz9DUT5zPaMCTA4dEGsaB2g9Z3siU2sIy93SQKPJgqzOtgdKPG-4D-cBGkB3Zd6qKfJEmLvwqMhcsag90EcvxdNnh2poawLQlrQJ_SumOOOD3z43U6MYQoczHrr4PdgVcHtb0C31ngOU3gnHpUBH7GVBvHe76U8JywTuPqxJQXCfzroXLCZ1UQhYFIP_PM_fBPsebgyguTg2isBsp0=)
18. [thomas-wiegold.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFZayUWiLpomvf6x6C4aM_PR5vVCizfjBSYW5sjZ3t72sVg-kxTZ7L1ifFDyuK0FWOvNXvH92cVJYqGCzfAnFr10T9PP1b3db_OlDMlnvE07RHTw_B06-s3Bwko2WswaIc9fgvpwmjZAETgHM-N3t8FWrnb7JjeyOKhg2CGiw==)
19. [paddo.dev](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHDgLWK4L2o7RfXWohXfj2MyQ_wYmS90lycDPgcL9JUMEol4ATH9RshGKvMT4w5Sd5posY5sWunWRm4D0Zv0ANhiO1Os1KqA2Db16oDqd5fJ3Nh01rqLGA96GErkUxrKrx1mg==)
20. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEb_X_SOLPZFN82uwJ6j5ca6LEqYkFkWKxSbU3ZTSrqVOt5i9fe7cpSfK2FCniaTq5_r9ozxJI42gCX3H8Mq3DOPeLWxup_N9zItCsKjJ68zT2cVvCj9IKuLAsvF12n89kUP8a-Sx-iTqSs7Xygj4_IQC_ZNmlVTg1rHRt_ihzPXHhpYqx_0i-socN7r8BPwcVUt3W0UKdaiPKMFX2mUY3GkJQh67AfTxah-KhY)
21. [ralph-wiggum.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGhSJXG3hMaM81axNCGi39ljB7aptgH6_zitDr6RpR2J0K1YZUqofwZQAwBasBkrt-T2eqUEpcpfr0o3f4jdiLF119U_OC4Tef9yXEwgw==)
22. [prg.sh](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHcxtYBp8yApdGJ89HJdSKS0c8Bb9q3OvCCctMu0vDlg3HY_YqqFHmkZ-mAnFm5VklB8_EKvDAlUalS4Ts6ASxlWVQ-SSOhv7qyPOVvaC7_rEjDbz2_XWqkJfed)
23. [dev.to](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFh_QIxOBMrUiUWFDnksQtBc0iOjvZ3NrX9luOyX2DxiuHT11ozMY0w7HLTqceBIKNpWHYLpPhCg5O6bNwZ14PkGiMOb1worrqY3brIVJB1d8ur8-XIQSCSdAbb-Aj9Iy3sxBJUDksCs5pCq0piwD2aW9aUftD0mB15AxMmxnBhDfeqlA==)
24. [coinsteam.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEGnk1yRNqQ1jwO5SWbIESwy_zxQjLXA6v82aVQFOIYp9NWxI_YPdxFzBM-RtmkD6wMowoAHKyLmjEMvjj_m-ActCefnUB2YNMsnulEnfZQxgL3s1NsUiSlSDgI9hV6KlyUDWfY9ATD9y-IU8Ef2vMbOJ0zV5ZowgucKqxdlfp85A==)
25. [reddit.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEgE4nXxODHYdnhzDs2w47Rczt69HidPeeKLxKOGgxIUK7FesafZII5cPH6cfhT8jav9W7m9jfjAGmLLEx5IHLjxkOUrTDnY6dSapO9lcWLvKYTTFxsXNhlTbNfsHoT4VD7_QMRP4FVoG01_vWNMVQR4Jp7EglzFtBGEbewa7T_RlJ09tXxevvCq-eYMUS8h6_q_xqnEdFVju6OKw==)
26. [jdon.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHO7wZACZwI-3TK4A-FwbO2hYsUHtjIU-Ot3onF3UI7FtYo5u0eS3v1Ftl2E_iz8UJntuJb6xoZRvdo0IpzMeMftbiGQrp6HkO1nFgTcjGuEfwhWD5WxyL3a-o1Ejk1MhVzeTXjDv_R8nasIxk56oHidh5WySc8KXLepotbrL59DNmQnfHpoW0=)
27. [zerosync.co](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEhPAff8tn1FHoLd-h1Ds5vTESoJZZmbWcNjtl_1lE8UHyJLFEgbruuBhcJ5fF3OnEif2PEydh_M0db1wF_34zoKCYhcKdElYZLKFMaWXxX0i8zmQZ8HBWmNJEa5T4Ga91CRZHu5yXHYrqiXdY5Mog=)
28. [prg.sh](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGpmdAdzM5H7Qe_kL7a9i6wyA87LgJPb99a78yeaBhmKTHGiN1HNSb05my8QpE2Ve99gjUupFtseFn1rSPUeMtmAf0r7ElwH-fIHoaw5fXsO4mWi67s5UCjknXBVAdUqRcln6fvQAvOew875w==)
29. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEDM97IEY2DKISAPj6KRYdD79xCUmr-x14FU517V69GFujx0Lh5EWka0ttNS4ZDfrLNkqhzTvTaB5fhEv37YgDIJHyfDmnVMioOcje_ZPPpJYwutRxKwlQ4S7maarm1iOdYbDblAyT4qFlDVYNJl4Rch3EuzzU3qb7BQppcfaGYuEBJ2-Q_SMRBRBpF)
30. [youtube.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFvc3-MDz7-3gW12wEhdEOihfanickhufHeywPou-zLg1xeGkDwHVkKnDBL3kU6CsphN_MocPBVvrZxlvfj20DOtgH3Sl70rReq4ejqL2w8JlHFx-cPFYQEi3JnuJkEoME=)
31. [buildthisnow.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEr-OG02ghgKyRSeynOFHm0Uy4PuXX6hjl9TKKYkCRF_RBLRMwcHTehMEzr9_FMM2p_rJ4dH5TZkz5Apb_MoPbmdy9_xwEvkIFsSte5R6xo4puMJWNpWBPrB5zNkLjrxhIwfLQNOY9n0yzXMM-gj1f5hAWJVH_z0u8rIGJ_UKYMrQ==)
32. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGSjUyBVhrkahkKdjQ6As0Na2DOKdcxuv-5RS6Ay2lwZLJ_yeZwfyNFKA73_UC_AVWIEOjlzrCgZwBwd_HhXjjqvDXoG6cBj8aAWD-6RRZ1rP950TphZSWRJqhepqYrs7TtEu7nHcSW9bEcEAIiyMpk6EKnmoXg9cZVWpk6WAH5aXKpvnKOtk4fNOpKjmEUakxgL_g1tQsy)
33. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHVFp_wgA04yLEEFJx5mutZo0sA4n4bcSlHfsl4XBH4yDJsSsZ85TclWXl2oIrtBPPKW9crJydyxfR99lG_OiHniv6oXRCXQOKrsaD_plw2mlMI4JwqX2pILleav0fLdyCkuyfrkc_1Pph9iaz4xOY1sqgUHU_7-CbkloDThc0_1AfmmFfk7BNJ2x4DxlLNeg18R01uYTcq6DI777dTXvC2CnM7ZEK7KKfFhs8=)
34. [wikipedia.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHruqu-E6LaHIJYYYH7pk4mNnpv4bqwnudfQ3yBPSartXSZBPG-LJ9i_QrwMmHy9gSRYSDTaZ_tyy63LnPSUrNvRaqM8uTuBwkrvH2FVvFc072WI1YWY4LE45nlDOsEchW-aUSDCps-)
35. [github.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGlv5gOqhiU3NkCUL9KVrDSdN9l_o4E_4fGfmuEwB2_W6PG3QCa_NUSRrk_ISscIBnoQFiuYUUIi4cmC0kMr4SLrZERidNTZWhr9oqU04oftz8dSbq5U8ErgyI2t1sCnidShpR34Gn9GWMLIobABwMFUw==)
36. [ghuntley.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH-FUgPgY_pyuWdmWbGk4rnTpY7dxaVfi9y7WtUCJgtOjrjrkqerRBNHVuIfdZ9ZnJnAAPZroiZ6ONDRPKCWR-yCCnvNhGB4jEWd31a5BLfLg==)
37. [zenn.dev](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGvtIGDxTysDJX64_hmclzVIr62r9OlvghSXzrszB3qMe72PfmIaP7x_e_eUO00ld3pBRQxhOy1TN6NXkZnQj29W8HCGipShrBl4MjqCCN5yb5FIR7pPo--Ee3b7gbsYXouasWuz-Qy-fg=)
38. [grokipedia.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGRliCnabttHjK2SlkiXHRRC7qO3OfLHGi23FGqID7hR7Fe0-wTuycqWMlUqZMlDMsmPAVcpMz-YLgbVqSyMj-UE5USUwnLL354r-D9uHgHT_GrHVPecZqX3nFk_BcXxPIqN_XfjG8=)
39. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGm8VSIhLmsMeWN33C5nn4qWpfR10ms9M5g6eGOrp9bUTjMB46SpUr-xM8QwieF3JPlyaTsNSL_nA_5UgpS8l5ohljey8Ao6EVTprTfZ2K7UANXOIENzcQ4EqZjwFWNfJpCknLJ)
40. [deepakness.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEINlnxTHT5GfkO-1CruFbcgaITU9X4Fj-iUmnZvBUhz9YeiXFQacPVYprcRe3-kDT9Puhy5IFrwZ9ZMskJeg2ljWdHYDE8KSa6slER5g4tX6v8HGiZWh23bhY=)
41. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFBuSbIUkCW7D38TuREu9FJ_XMkhoN47GPS4cbtC2FBt8J6GdPyjdRXtsevPMzdOOpJpoyd4ekUtzW4pFCrgBZ6NiQFAQT_nTYYhw9M1iPurJ5xzBvrCCw39JM-FmHZA5e8EDxDFavwX8Dpd0_8gy21pNn2t4Kl8A==)
