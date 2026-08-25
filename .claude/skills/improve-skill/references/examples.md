# Worked Examples — Four PM OS Skills, Before and After

Source: Aakash Gupta, "How to build 10/10 Claude Skills" — section 3. These are the canonical before/after rewrites the framework was built against. Pattern-match against them when rewriting.

---

## Example 1: `/daily-plan` — Context Routing vs. Starting from Scratch

### Bad (what most PMs write)
```yaml
---
name: daily-plan
description: Create a daily plan for today's work
---

Create a prioritized daily plan based on my current priorities.
Include meetings, tasks, and focus areas.
```

**What Claude produces:** Generic. Could be any PM, any Tuesday. No meetings named, no PRD context, no stakeholder intelligence. The kind of plan you could have written yourself in two minutes.

### Good
```yaml
---
name: daily-plan
description: Generates a prioritized daily plan for product managers by pulling from PRDs, meeting notes, stakeholder profiles, and connected MCPs. Use when starting your workday, planning tomorrow, or when the user types 'daily plan', 'what should I work on today', 'my schedule', 'plan my day', or 'what's on my plate'. Do not use for weekly planning, OKR reviews, or roadmap prioritization.
---

## Context Routing
Check these first:
1. context-library/strategy/ — Quarter priorities, OKRs, North Star
2. outputs/weekly-plans/ — This week's priorities
3. outputs/prds/ — Active PRDs and their stages
4. context-library/stakeholders/ — Stakeholder profiles
5. outputs/meeting-notes/ — Recent context

## Integration Options
Option 1: MCP Servers (Google Calendar, Gmail, Linear, Amplitude)
Option 2: Direct API access (with setup guide per tool)
Option 3: Export/Import workflow (screenshot → vision analysis)
Option 4: Browser automation via Claude in Chrome MCP
Option 5: Manual input (5-question quick entry, always available)

## Graceful Degradation
If Calendar MCP not connected: "What meetings do you have today?"
If Linear MCP not connected: Scan outputs/meeting-notes/ for unchecked items
If no stakeholder profiles: Generate meeting list without context, suggest creating profiles
```

**What Claude produces now:** Named meetings with stakeholder context. Specific blockers. Open questions with deadlines. Day's priorities tied to the week's north star. Output specific to the actual situation, not a generic PM's situation. Works whether MCPs are connected or not because the skill has five fallback paths built in.

**Lesson:** A skill that asks you to supply context is doing half the work. The context routing table plus graceful degradation paths does the work itself.

---

## Example 2: `/activation-analysis` — Embedded Framework vs. Generic Analysis

### Bad
```yaml
---
name: activation-analysis
description: Analyze product activation and identify areas for improvement
---

Analyze the product's activation funnel.
Identify where users drop off.
Recommend improvements.
```

**What Claude produces:** A blog post. Generic best practices with no knowledge of the actual D7 numbers, onboarding steps, or user research. The PM could have Googled this.

### Good (key structural elements)
```yaml
## Context Routing Logic (Internal — for Claude)

| Source | Files/Folders | Search Terms | What to Extract |
|--------|---------------|--------------|------------------|
| Metrics | context-library/metrics/*.md | "onboarding", D7, D30, "time to value" | Current activation rates by stage |
| User Research | context-library/research/*.md | "first time", "confused", "stuck" | Friction points, success moments |
| Meeting Notes | context-library/meetings/*.md | "activation", "new users", "drop-off" | CS feedback, support patterns |
| PRDs | context-library/prds/*.md | "onboarding", "tutorial" | Past onboarding work, shipped changes |

## Context Priority

1. Internal context FIRST (business info, existing metrics, user research)
2. Analytics MCP SECOND (if connected — query activation funnel by cohort)
3. Framework guidance LAST (generic activation tactics)

## Cross-Skill Links

- Retention issues detected → link to /retention-analysis
- Expansion opportunity found → link to /expansion-strategy
- User struggles identified → link to /user-research-synthesis

## Framework Source
Setup → Aha → Habit framework from Aakash Gupta's activation guides
```

**What Claude produces now:** Specific numbers from the metrics folder. User research findings cross-referenced with CS meeting notes. A single highest-leverage fix ranked by implementation effort, tied to a specific sprint. **Not best practices. Your data.**

**Lesson:** The context priority order is what most people miss. Internal context first, MCPs second, framework last. A skill that jumps straight to generic best practices is just a worse version of asking Claude directly.

---

## Example 3: `/prd-draft` — What Happens When Claude Skips the Strategy Check

### Bad
```yaml
---
name: prd-draft
description: Write a product requirements document
---

Write a PRD for the feature the user describes.
Include problem statement, solution, and success metrics.
```

**What Claude produces:** PM types `/prd-draft for dark mode`. Claude writes the PRD immediately. Problem statement, solution, success metrics, stakeholders — all generic. No check on whether this fits Q3 strategy. No flag that user research doesn't support it. Just output.

### Good (key structural elements)
```yaml
## Context Routing Logic
| Source | Path | Extract |
|--------|------|---------|
| Strategy | strategy/*.md | Pillars, OKRs |
| Research | research/*.md | User validation |
| PRDs | prds/*.md | Dependencies |

## Common Shortcuts — Do Not Take These
| What Claude might think | Why it's wrong |
|---|---|
| "The feature is simple, I can skip Step 0" | Step 0 reads strategy files the conversation lacks. |
| "I have the feature description, that's enough" | Without strategy check, you draft work that won't ship. |
| "I'll flag strategic fit at the end of the PRD" | By then, the PM has already invested in the wrong doc. |
```

**What Claude produces now:** Before writing a word, Claude flags that dark mode isn't in the Q3 strategy pillars. Surfaces the user research gap. Offers to reframe or park the feature. When the PM confirms direction, the PRD is drafted against the actual template, saved with the right naming convention, linked to the relevant OKR.

**It doesn't just write the PRD. It tells you when the PRD shouldn't exist yet.**

**Lesson:** Without the anti-rationalization table, Claude skips Step 0 on multi-step skills because the shortest path to a completed response is always faster than following every step. The table closes that exit.

---

## Example 4: `/create-tickets` — Structured Output vs. Freeform List

### Bad
```yaml
---
name: create-tickets
description: Create engineering tickets from a PRD
---

Read the PRD and create engineering tickets for the engineering team.
Break the work into logical tasks.
```

**What Claude produces:** PM types "Create tickets from the checkout redesign PRD." Four generic tasks. No effort estimates. No acceptance criteria. No dependency map. No component labels. **Not something you can hand to an engineering team without another thirty minutes of work.**

### Good (key structural elements)
```yaml
## Step 1: Gather Context

Read the source PRD and identify:
- User-facing features (frontend work)
- API/Backend work
- Data migrations (data engineering)
- Infrastructure changes (DevOps)
- Testing requirements (QA)
- Documentation needs

## Output Format (per ticket)

Title: [Component] [Action] [Subject]
Type: Story / Task / Bug / Sub-task
Effort: [Fibonacci: 1, 2, 3, 5, 8, 13]
Priority: P0 / P1 / P2
Acceptance Criteria:
  - [ ] Given [context] when [action] then [outcome]
  - [ ] [Additional criteria]
Dependencies: [Ticket IDs or "None"]
Labels: [frontend / backend / data / infra / qa / docs]

## Dependency Summary

After all tickets generated:
- Map dependency chain (what blocks what)
- Flag circular dependencies
- Suggest sprint assignment based on dependencies

## Output

If Linear/Jira MCP connected: Create directly
If not: Save to outputs/analyses/[feature]-tickets.md
```

**What Claude produces now:** Each ticket comes out with a component label, Fibonacci effort estimate, priority level, and acceptance criteria in Given/When/Then format. After all tickets are generated, the skill maps the dependency chain and suggests sprint assignments. If Linear MCP is connected, it pushes directly. If not, it saves to `outputs/analyses/checkout-tickets.md`.

**The PM hands it over. Engineering can start.**

**Lesson:** An output format isn't just about consistency. For tickets, it's the difference between output a PM hands off and output an engineering team can act on without a follow-up conversation. **Specify the format at the level your downstream users need it, not at the level that makes writing the skill easy.**

---

## Pattern summary

Across these four examples, the same set of upgrades show up:
1. **Description**: from <50 chars to 250+ with WHAT, WHEN, trigger phrases, and "Do NOT use for" boundary
2. **Step 0**: a Source/Path/What-to-extract table replaces "check the context library"
3. **Output format**: an explicit template or worked example replaces "create a [thing]"
4. **Anti-rationalization** (for multi-step skills): a Common Shortcuts table closes the exit Claude takes
5. **Cross-skill routing** (for skills that produce branchable output): explicit pointers to sibling skills
6. **Graceful degradation**: explicit fallback paths when MCPs / files / inputs are missing

When rewriting a target skill, copy these *shapes*, not the literal content. The PM's actual strategy files, metrics paths, and ticket schema go in the table — not the daily-plan example's.
