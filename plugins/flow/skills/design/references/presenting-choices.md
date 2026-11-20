# Presenting Design Choices

Use this format whenever the user picks between designs: the variants of Design-It-Twice, and any Phase 2 question whose options are different designs (where a seam goes, the shape of an interface, a data layout, which module owns a piece of work). A question that only confirms a fact or a value needs no more than the question tool's option descriptions.

Write for a reader who knows the repo only at a high level and has not followed this conversation. Someone who opens only this message must be able to choose. Restate what earlier answers settled instead of pointing back to them ("as agreed above").

## The Sections, in Order

### 1. Background

The core of the problem, for that reader:
- what the module is, where it sits and what calls it;
- what it does today and what is changing;
- why the choice has to be made now;
- the decisions already made that constrain it.

Name the real modules, files and data. Define any term a newcomer would not know.

### 2. Key Considerations

The trade-offs every option has to settle, stated before the options so each is judged against the same list:
- **Scale:** the sizes and rates involved, and what grows.
- **Complexity:** the new concepts, modules and moving parts, and who has to learn them.
- **Simplicity:** what the most common caller writes.
- **Fit with existing practice:** the repo's conventions, seams and rules that the choice follows or bends.

Cover each briefly, and say where the options are equal.

### 3. One Section per Option

Every option gets the same three parts and runs the same worked example, so the options compare like for like:
- **How it solves the problem:** its key choices and the idea behind them, in a few sentences.
- **What it looks like:** the interface as a caller meets it. Show usage snippets with this codebase's real names and data, then the signatures. Add one or two corner cases (an error, an empty input, a rare caller, a second adapter) and what comes back.
- **Strengths and weaknesses:** concrete, each tied to a consideration from section 2.

### 4. Comparison Table

Last, a table with one column per option and one row per consideration, plus rows for whatever differs most (entry points, what crosses the seam, cost). The table sums up the sections above and adds no fact they lack.

### 5. The Question

Then ask one question through the question tool, following SKILL.md, **Asking the user**, including its preview rules. No option is recommended, here or anywhere above.

Size the sections to the choice: a small choice may need two lines each.
