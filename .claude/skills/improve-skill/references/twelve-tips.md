# The 12 Tips — Reference

Source: Aakash Gupta, "How to build 10/10 Claude Skills" (May 2026).

Each tip below has: **rule**, **why it matters**, **bad pattern**, **good pattern**. Pattern-match the target skill against these. When applying a tip, copy the *good* shape — don't paraphrase the tip.

---

## Tip 1: The description answers two questions — what does it do, when should Claude use it.

**Rule.** Description must contain WHAT + WHEN in the first 250 characters. Third person. Pushy ("Use when..." / "Make sure to use..." not "Use for...").

**Why.** Claude pre-loads only `name` + `description` at startup. Body, references, and scripts load only after description triggers a match. Descriptions under 50 chars get invoked 3–5x less often. Inconsistent POV (first person "I can help with X") breaks routing.

**Bad:**
```yaml
name: daily-plan
description: Generate PM daily plan with context
```
36 chars. No trigger phrases. No boundaries. Claude has nothing to route on.

**Good:**
```yaml
name: daily-plan
description: Generates a prioritized daily plan for product managers by pulling from PRDs, meeting notes, stakeholder profiles, and connected MCPs. Use when starting your workday, planning tomorrow, or when the user types 'daily plan', 'what should I work on today', 'my schedule', 'plan my day', or 'what's on my plate'. Do not use for weekly planning, OKR reviews, or roadmap prioritization.
```

---

## Tip 2: Add negative triggers, not just positive ones.

**Rule.** Every description ends with "Do NOT use for X → use /Y instead." Tells Claude where to route the request, not just where not to.

**Why.** Claude over-triggers on adjacent requests. A ticket-creation skill fires when the user asks about experiment design. An activation analysis skill fires when someone asks about retention. Negative triggers turn a collection of skills into a routing system.

**Bad:**
```
description: Creates engineering tickets from PRDs and feature specs.
```

**Good:**
```
description: Creates engineering tickets from PRDs, feature specs, or meeting notes. Use when the user says 'create tickets', 'break into tasks', 'sprint planning', or references a PRD and wants implementation tasks. Do NOT use for PRD writing, experiment design, milestone planning, or roadmap prioritization — use /prd-draft, /experiment-metrics, or /milestone-plan instead.
```

The pointer (`→ use /X`) is the part 70% of skills miss. It closes the loop.

---

## Tip 3: Instructions are commands. Not conversations. Not suggestions.

**Rule.** Every line in the body is imperative. "Read the target file. Check for X. Output as Y." Not "Could you take a look and maybe check for any issues?"

**Why.** Vague input produces vague output. "It would be great if you could suggest improvements" sounds like a Slack message asking a colleague for a favor — Claude treats it that way. Numbered steps + direct verbs + no softening language.

Also: **consistent terminology**. Pick one word per concept and never vary it. Always "API endpoint" not "URL" in one step, "route" in another, "path" in a third. Always "ticket" not alternating with "task" then "item". Claude tracks the term and treats synonyms as potentially different things.

**Bad:**
```
Could you please review the code? Maybe check if there are any bugs?
It would be great if you could suggest improvements too.
```

**Good:**
```
Review the current diff. Check for:
1. Security vulnerabilities (OWASP Top 10)
2. Performance issues (N+1 queries, blocking calls)
3. Code style violations

Output as a checklist with severity ratings: Critical / High / Medium / Low.
Flag each finding with the specific line number and the recommended fix.
```

The test: read your skill out loud. If it sounds like a request, rewrite it as a rundown.

---

## Tip 4: Build a context routing table, not just a read-first step.

**Rule.** Use a structured table that maps **Source | Path | What to extract**. Claude reads the right files, in the right order, looking for the right information.

**Why.** "Check the context library before writing" lets Claude read whatever looks relevant — sometimes right, often not. The table forces consistency.

**Bad:**
```
## Step 0
Check the context library before writing.
```

**Good:**
```
## Step 0: Read Before You Write

Check these files in this order before generating anything:

| Source         | Path                              | What to extract                |
|----------------|-----------------------------------|--------------------------------|
| Metrics        | context-library/metrics/*.md      | D7/D30, setup completion %, Aha rate |
| User research  | context-library/research/*.md     | Onboarding confusion points    |
| PRDs           | context-library/prds/*.md         | Past activation work, shipped changes |
| Stakeholders   | context-library/stakeholders/*.md | Decision makers, recent concerns |
| Business info  | context-library/business-info-template.md | Target user, core value prop |

Only generate output after completing Step 0.
```

The table tells Claude exactly which directory, what to look for inside it, and what information to pull. Output stops being generic and starts being about the actual product.

---

## Tip 5: Specify the output format. Match strictness to how badly failure hurts.

**Rule.** Specify format. **Low freedom** for fragile/live-system tasks (exact commands, no interpretation). **High freedom** for analysis where Claude's judgment is the point (sensible default template, room to adapt).

**Why.** Without a format, Claude invents a new one every session. The skill fires correctly and still produces inconsistent output. You can't share with a teammate. You can't rely on it across sessions.

**Bad:**
```
Generate a commit message for these changes.
```
One-liners sometimes. Paragraphs sometimes. Prefixes sometimes. No consistency.

**Good:**
```
Generate a commit message in this exact format:

type(scope): short description under 50 chars

- What changed
- Why it changed (if not obvious)

Type must be one of: feat, fix, refactor, docs, test, chore.
Scope is the affected module name.
Description is lowercase, present tense.
```

---

## Tip 6: Write the out-of-scope section with pointers, not just exclusions.

**Rule.** "Don't do X" is incomplete. "Don't do X → use /Y instead" closes the loop.

**Why.** This pattern appears in 70% of well-built skills and almost never in bad ones. When Claude hits a request outside scope, it routes correctly instead of trying and failing.

**Bad:**
```
## Out of Scope
- Experiment design
- Milestone planning
```

**Good:**
```
## Out of Scope

This skill does NOT handle:
- Writing or drafting PRDs → use /prd-draft
- Designing experiments or defining success metrics → use /experiment-metrics
- Milestone planning or roadmap work → use /milestone-plan
- Retention analysis → use /retention-analysis
```

---

## Tip 7: Add cross-skill links inside the body.

**Rule.** Skills that detect adjacent issues route to the skill that handles them.

**Why.** Without cross-skill links, each skill works in isolation and tries to answer everything it touches. The PM gets partial output on adjacent topics or has to manually switch skills.

**Good:**
```
## Cross-Skill Routing

After completing this analysis:
- If D30 retention drop detected → recommend running /retention-analysis
- If pricing or packaging questions surface → recommend /pricing-analysis
- If expansion revenue opportunity found → recommend /expansion-strategy
- If activation gaps trace to onboarding copy → recommend /brief-review
```

This turns a folder of isolated skills into a system that routes itself.

---

## Tip 8: Keep SKILL.md under 1000 lines (ideally 500). Offload everything else.

**Rule.** SKILL.md = core logic. `references/` = docs and examples (loaded only when accessed). `scripts/` = executables (run, never loaded into context).

**Why.** Every token in SKILL.md competes with conversation history once the skill loads. A 2000-line skill burns 5000+ tokens before doing anything. Instructions on line 300+ get deprioritized.

**Bad:**
```
skill/
└── SKILL.md  ← 1,800 lines with every edge case, all API docs, full examples, historical context
```

**Good:**
```
skill/
├── SKILL.md         ← under 500 lines, core logic only
├── references/
│   ├── schema.md    ← loaded when Claude needs schema detail
│   └── examples.md  ← loaded when Claude needs examples
└── scripts/
    └── validate.py  ← executed, never loaded into context
```

Keep `references/` **one level deep**. Nested references cause partial reads where Claude previews a file and misses the critical part at the bottom.

**One skill, one job.** A skill that creates tickets, drafts PRDs, runs activation analysis, and generates standup updates is four skills. If you can't describe what the skill does in one sentence, split it.

---

## Tip 9: Add a learnings.md file to every skill you care about.

**Rule.** The skill logs its own failures. Step 0 reads `references/learnings.md`; an exit step appends a new entry.

**Why.** Without it, you iterate manually: notice failure → open SKILL.md → rewrite section → test again. Days to find one pattern. With it, thirty days of real use surfaces in one read.

**Setup:**
```
skill/
├── SKILL.md
└── references/
    └── learnings.md   ← Claude writes here after each run
```

**Add to Step 0:**
```
## Step 0: Load Context
Before starting, read references/learnings.md if it exists.
Apply any patterns flagged as successful. Avoid patterns flagged as failures.
```

**Add to exit step:**
```
## After Completing: Log Learning

Append one entry to references/learnings.md:
Date: [today]
What worked: [specific pattern that produced good output]
What didn't: [what failed or needed correction]
Edge case: [anything unexpected]
```

The skill gets better on its own without you touching the core instructions.

---

## Tip 10: Show Claude what good looks like. Don't just describe it.

**Rule.** Include an actual worked example (input → output) inside the skill. Not a description of what good looks like.

**Why.** Claude pattern-matches exceptionally well. One real example produces better results than three paragraphs of rules describing it.

**Bad:**
```
## Output Rules
- Keep commit messages concise
- Start with a type prefix
- Include a short description of what changed
- Add bullet points explaining why
```
"Concise" means different things to different people. "Short description" is vague.

**Good:**
```
## Output Format

Generate commit messages following this exact example:

Input: Added login with Google OAuth
Output:
feat(auth): add Google OAuth login

- Integrate google-auth-library for token verification
- Store OAuth tokens in existing session middleware
- Redirect to /dashboard on successful auth

---

Input: Fixed date formatting bug in reports
Output:
fix(reports): correct date display in timezone conversion

- Replace local date parsing with UTC-normalized timestamps
- Affects weekly and monthly report exports only
```

If you're writing more rules than examples, flip the ratio. One real example outperforms five rules every time.

---

## Tip 11: Add an anti-rationalization table for any step Claude might skip.

**Rule.** A two-column table: **What Claude might think | Why it's wrong.** Names the specific excuses Claude will make and shuts each one down.

**Why.** Agents take shortcuts. Given a multi-step skill, Claude finds reasons to skip the hard parts: "This is simple enough to skip the spec." "The context is clear, I don't need to read the files." The shortest path to a completed response is always faster than following every step.

**Bad:**
```
## Process
1. Read context files
2. Generate analysis
3. Save to outputs/
```

**Good:**
```
## Process
1. Read context files (see Step 0 table)
2. Generate analysis
3. Save to outputs/

## Common Shortcuts — Do Not Take These

| What Claude might think | Why it's wrong |
|---|---|
| "The conversation has enough context, I can skip Step 0" | Step 0 reads files the conversation doesn't contain. Missing it means working from training data. |
| "The output format is obvious, I don't need the template" | Inconsistent format breaks downstream use. Always use the template. |
| "I'll note the cross-skill recommendation at the end" | If analysis is done first, the recommendation gets buried. Surface it immediately when detected. |
```

Use this on any skill with 3+ steps.

**Also:** instructions buried at the bottom of a long skill get ignored. Critical constraints go at the top, before workflow steps. Use `## Critical` or `## Important` headers. If a rule is non-negotiable, it belongs in the first 100 lines, not the last.

---

## Tip 12: End every complex skill with a non-negotiable exit checklist.

**Rule.** A checklist where each item requires verifiable evidence before Claude considers the task finished.

**Why.** Without exit criteria, Claude decides on its own when work is done — and tends to decide early. Output generated, task complete. No check that files saved. No verification that cross-skill routing flagged. No confirmation that output format matched.

**Bad:**
```
Generate the analysis and save it to outputs/.
```

**Good:**
```
## Before Marking Complete

Do not consider this task finished until all of the following are true:

- [ ] Step 0 context files were read (list which ones in your response)
- [ ] Analysis references specific data from context files, not general knowledge
- [ ] Output saved to outputs/analyses/[skill-name]-[date].md
- [ ] Output format matches the template exactly — run a quick self-check
- [ ] Cross-skill recommendations flagged if any triggers were detected
- [ ] If no context files existed, stated that explicitly rather than proceeding from training data

If any item above is unchecked, complete it before finishing.
```

Combined with the anti-rationalization table: the table stops Claude from skipping steps mid-task, the checklist stops Claude from calling it done before the work is actually complete.

Use on any skill where partial output is worse than no output.

---

## Tip 13: Mark inferred defaults as inferred. Don't let plausible-sounding values masquerade as user-supplied facts.

**Rule.** When the skill needs a value the user didn't supply (Kafka broker count, p95 SLO target, equity-grant level, recommended sprint length), the output marks it explicitly: `[DEFAULT: 3 brokers — confirm with user]`. Never let an inferred value pass as a confirmed one.

**Why.** This is the failure mode the original 12 tips don't name. Specificity ≠ correctness. Claude can produce specific-looking output ("we'll size for 3 Kafka brokers, p95 < 200ms, 30-day rollback window") where every number is a reasonable training-data default rather than a user-confirmed fact. This is more dangerous than generic output because it *looks* tailored — the PM signs off on an RFC where Engineering thought the numbers came from the PM, and the PM thought they came from a strategy doc.

Surfaced empirically in slot 12 (rfc-author): infrastructure defaults presented as user-confirmed facts dropped specificity from 18/20 (visibility-of-source) to 12/20 once the rubric distinguished "specific because user said so" from "specific because Claude guessed plausibly."

**Bad:**
```
## Risks
- p95 latency must stay under 200ms during cutover
- Rollback window: 30 days
- Kafka cluster: 3 brokers, replication factor 3
```
Looks great. None of those numbers came from the user.

**Good:**
```
## Risks
- p95 latency [DEFAULT: < 200ms — confirm with @sre]
- Rollback window [DEFAULT: 30 days — confirm with @platform]
- Kafka cluster [DEFAULT: 3 brokers, RF=3 — confirm with @infra]
```

The marker is ugly on purpose — it forces a confirm step that quiet defaults skip.

**Where this applies:** any skill that produces config-like output (RFCs, infra docs, ticket specs, training plans with weights/reps, salary research with specific numbers, investor updates with metric projections, recipe scaling). Add a Step 0 instruction: "any value not in user input or in the read-first files must carry the `[DEFAULT: X — confirm with Y]` marker."

---

## Reading note: line-count nuance for Tip 8

Tip 8 says "keep SKILL.md under 1000 lines, ideally 500." Empirically that rule needs nuance:

- **Bloat (true Tip-8 failure):** duplicated rules, historical context, narrative explanations. Move to references/. Slot 20 (fitness-coach 724 lines) and slot 03 (prd-draft 941 lines) are this category. Critical rules buried at the bottom is the dangerous pattern.
- **Rich worked examples (NOT a Tip-8 failure):** content/writing skills where the worked examples ARE the specificity driver. Slot 08 (linkedin-post-mastery 631 lines, with 350+ lines of annotated examples) scored 16–18/20 on specificity precisely because the examples were inline. Trimming would have hurt the skill.

Diagnostic: when a skill is over 500 lines, ask "what gets read in line 200, 400, 600?" If duplicated rules → move. If worked input/output pairs → keep.

---

## Reading note: Tip 3 + Tip 11 are a *functional* pair, not just style

Tip 3 (imperative commands) is often described as a style fix. Slot 19 (conversational-codereview) showed it's actually functional: softening language in instructions ("could you maybe check") propagates symmetrically into output ("you could maybe consider..."). Every "would be great if" in the skill produces a "would be great if" in the review findings.

When softening language is the dominant failure, treat the imperative rewrite as the primary intervention, paired with an anti-rationalization table row that names the softening pattern explicitly. The two together close the loop; either alone leaves the propagation channel open.

---

## Reading note: special pattern — health/safety/medical/financial domains

Tip 8's line-count rule meets a hard override here: regardless of body length, **safety-critical rules must appear in the first `## block`** of the skill body. Bloat in these domains is not a quality issue — it's a harm vector. Slot 20 (fitness-coach) had safety rules buried at line 700 of 724; the original author wrote "I keep forgetting to add them at the top," and Claude was actively violating them on injury-related inputs. Move first, condense later.

---

## Reading note: outreach skills with copy-paste artifacts

Outreach skills (referral message, recruiter outreach, intro email) produce output the user is meant to copy-paste-send without editing. If the deliverable contains `[Your Name]`, `[Company]`, `[Their Role]` — the artifact is broken. Surfaced in slot 07 (referral-request).

Fix: Step 0 extracts user's name and current employer/role; exit checklist gates output if any unfilled `[Bracket]` placeholder remains. Treat unfilled placeholders as a hard fail, not a polish issue.

---

## Reading note: multi-step provisioning needs an ID-tracking scaffold

For skills that walk through 5+ steps creating named resources (Arize integrations, infrastructure setup, scaffolding workflows), users lose track of `INTEGRATION_ID`, `EVALUATOR_ID`, `TASK_ID`, `RUN_ID` across steps. Surfaced in slot 13 (arize-evaluator).

Fix: add a "Track IDs as you go" block at the top of the workflow:
```
## Track these as you go
INTEGRATION_ID: ___
EVALUATOR_ID: ___
TASK_ID: ___
RUN_ID: ___
```
Users fill them in; the next step instructions reference them by name. Removes a class of silent failures.
