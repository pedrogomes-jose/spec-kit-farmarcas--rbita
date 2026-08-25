---
name: create-skill
description: Creates a new Claude skill from scratch — for any domain (PM, job-search, content, engineering, finance, fitness, personal, ops, anything). Drafts a v0 SKILL.md that bakes in the 12 tips by default (frontmatter with triggers + boundary, Step-0 read-first table, imperative body, worked example, anti-rationalization table, exit checklist, cross-skill routing), then runs an evaluation loop on its own draft — builds a custom rubric, generates 3 realistic test inputs, scores the draft's outputs, edits in place to fix the lowest criteria, and loops until the new skill scores A+ across the rubric. Produces full proof-of-work in `outputs/`. Use when the user types 'create skill', 'new skill', 'build me a skill', 'scaffold a skill', 'make this into a skill', 'turn this into a skill', 'turn this into a thing I can re-run', 'make this re-runnable', 'I do this every week — automate it', '/create-skill', or describes a recurring task they want turned into a skill. Do NOT use for editing or upgrading an existing SKILL.md → use /improve-skill instead. Do NOT use for tuning CLAUDE.md or hooks → use /update-config. Do NOT use for one-off scripts or single prompts — a skill is for tasks reused across sessions.
---

# create-skill

Creates a new Claude skill from scratch and ships it at A+ quality. The deliverable is not a draft; it is a SKILL.md whose own evaluation loop has converged.

The principle: a "rule-applied" skill is a hypothesis. A re-run on three real inputs with grades over 90/100 is proof. Same loop as `/improve-skill`, but starting from `name + 1-line spec` instead of an existing file.

## Critical

- **Build → eval → fix → loop.** Never ship a v0 draft. The last 25 evaluation runs in `references/learnings.md` show drafts that "look right" routinely score F on first eval. The eval is the verification.
- **Read sibling skills BEFORE writing cross-skill links.** Unverified pointers (`→ use /retention-analysis`) cap routing at 18/20 and break worse than no link. Verify the folder exists.
- **Verify YAML name == folder name.** Mismatch is silent — `/skill-name` invocation hits nothing. Always check before declaring done.
- **No `${CLAUDE_SKILL_DIR}` or other unguaranteed env vars.** If a skill must reference external files, use a project-relative path or embed inline.
- **Apply the safety override.** For health/safety/medical/financial domains, safety-critical rules go in the FIRST `## block` of the body — before Step 0, regardless of body length. Not later. Not buried.
- **One skill, one job.** If the spec names 3+ output formats or 3+ verbs ("creates posts AND tweets AND newsletters"), STOP and split before drafting. Multi-job skills route badly and the eval will not save them.
- **--draft mode does not skip the loop by default.** If the user did not explicitly type `--draft`, run the full eval loop. `--draft` is documented in Step 9 only as an escape hatch with a logged warning.

## Step 0: Read Before You Write

Read these in order. Do not draft until all are read.

| Source | Path | What to extract |
|--------|------|-----------------|
| Twelve tips | `references/twelve-tips.md` | The 12 rule shapes — pattern-match the draft against the *good* example shape, not the rule paraphrase |
| Audit checklist | `references/audit-checklist.md` | The P0–P3 pre-flight items (frontmatter present, name == folder, refs resolve, no unguaranteed env vars) and items 1–11 + B1–B8 |
| Worked examples | `references/examples.md` | Before/after shapes for description, context routing, output format |
| Past learnings | `references/learnings.md` | 25 prior runs across PM/job-search/content/engineering/finance/fitness/cooking/education/founder. Read before drafting — every entry names a failure mode that cost real iteration time |
| Creation patterns | `references/creation-patterns.md` | Distilled "build it right the first time" defaults by domain — frontmatter shape, Step-0 shape, output-format shape, common ceilings |
| Sibling skills | `<skills-dir>/*/SKILL.md` (frontmatter only) | Names + descriptions of nearby skills, for verified cross-skill routing pointers |
| User prompt | conversation | The skill name, one-line job, who it's for, what it should NOT do |

If `references/learnings.md` does not exist in this folder, fall back to `../improve-skill/references/learnings.md`. Do not invent learnings.

## Step 1: Intake the Spec

Get these five fields from the user. If any is missing, ask once before proceeding — do not invent.

| Field | Example |
|-------|---------|
| **Skill name** (kebab-case, matches folder) | `cover-letter-writer` |
| **One-line job** (WHAT it does, in one verb-led sentence) | "Generate an ATS-optimized cover letter tailored to a JD." |
| **Domain class** (used to pick rubric) | content / outreach / analysis / planning / code / decision / education / health / finance / scaffolding / synthesis / research |
| **WHEN it should fire** (3+ user-typed phrases) | "write a cover letter", "applying to X for Y", "help me apply" |
| **Out-of-scope + pointer** (what it should NOT do, with `→ use /Y`) | "resume rewrites → use /resume-tailor; salary negotiation → use /salary-research" |

For any value the user did not supply, mark it with `[NEED: from user]`. Do not silently default. (See learnings: "inferred defaults masquerading as user-supplied facts" — Tip 13.)

**Trigger-phrase floor.** If the user supplies fewer than 5 trigger phrases, do not infer to fill the gap silently. Surface candidates extracted from the user's prompt verbatim ("you wrote 'every Monday' and 'kickoff doc' — should those be triggers?") and ask once. Inferring without flagging is the routing-failure pattern from learnings (status-update Iter-2 had to add 2 phrases post-hoc).

**Prefill from conversation, then confirm.** If prior conversation gave the skill name, voice samples, file paths, or domain class — list them as candidates with the source ("from your earlier message: name=`sprint-kickoff`, sources=Linear+Slack+PRD backlog") and ask once. Never silently use prior context as user-confirmed.

**Loop preview.** When you stop to ask, tell the user what the loop *will* do once they reply: "Once confirmed, I'll classify the domain, draft v0, build the rubric, run 3 inputs, score, and loop until A+. Expect ~5–8 minutes." This sets the expectation that creation is a loop, not a one-shot draft.

## Step 2: Classify and Pick the Domain Rubric

Map the spec to a domain row, which determines two domain-specific criteria (4 and 5) added on top of the universal three. Defaults below; override only with reason.

| Domain | Primary criterion | Secondary criterion |
|--------|-------------------|---------------------|
| Analysis (activation, retention, funnel) | evidence trail | actionability |
| Outreach (cover letter, referral, recruiter, intro) | personalization | call-to-action / placeholder scrubbing |
| Content (LinkedIn, tweet, newsletter, infographic) | voice match | hook strength / visual clarity |
| Professional writing (status update, investor update) | signal density | honesty flagging |
| Planning (daily plan, sprint, training block) | prioritization | graceful degradation |
| Code review / debugging | file:line precision | severity tagging |
| Code authoring (RFC, commit msg, refactor) | correctness | risk flagging / alternatives-not-strawmen |
| Research / market data | primary-source ratio | triangulation |
| Synthesis / summary | coverage | signal/noise |
| Decision (build vs buy, PRD vs no-PRD) | opinion | kill criteria |
| Education / tutoring | checkpoints | progression |
| Health / fitness / safety / medical | safety-first application | individualization |
| Finance / budget | math correctness | category completeness |
| Multi-step provisioning / setup | step completeness | id-tracking |
| Cooking / recipes | constraint respect | substitution / contradiction flagging |
| Scaffolding (second brain, repo init) | idempotency | starter completeness |

If the spec doesn't fit, write your own two criteria. The table is a starting point.

## Step 3: Generate Draft v0

Write the file at `<skills-dir>/<skill-name>/SKILL.md`. Use this skeleton and fill every section. Skip none — Step 4 will eval whether they're load-bearing.

```markdown
---
name: <skill-name>
description: <WHAT in one sentence — third person, pushy: "Generates X..." not "I help with X". Then WHEN: "Use when the user types 'phrase 1', 'phrase 2', 'phrase 3', 'phrase 4', or 'phrase 5'." Then boundary: "Do NOT use for X → use /Y. Do NOT use for Z → use /W.">
---

# <skill-name>

<One-paragraph what + why this skill exists. Imperative, not narrative.>

## Critical

<3–6 bullets of non-negotiable rules. For health/safety/finance: safety rules go HERE, in the first ## block, regardless of body length.>

## Step 0: Read Before You Write

| Source | Path | What to extract |
|--------|------|-----------------|
| <named source 1> | <real path> | <real fields> |
| <named source 2> | <real path> | <real fields> |
| <learnings, if applicable> | references/learnings.md | prior patterns to apply / avoid |

<For inferred-default risk (config-like outputs): add line — "Any value not in user input or in the read-first files must carry the `[DEFAULT: X — confirm with Y]` marker."

For outreach/copy-paste artifacts: add line — "Extract user's name, current employer, current role for placeholder substitution.">

## Step 1: <First imperative step>

<Imperative verbs throughout. Numbered if multi-step. No softening — no "could you", "maybe", "if you'd like".>

## Step N: ...

## Output Format

<Exact template OR worked input/output example. For skills with multiple valid sub-shapes (bullets vs prose, body vs no body), include 2–3 worked examples — rules alone never resolve those choices.>

## Worked Example

Input: <realistic user prompt>
Output:
<full output the skill produces — what good looks like>

## Out of Scope

This skill does NOT handle:
- <X> → use /<verified-sibling-skill>
- <Y> → use /<verified-sibling-skill>
- <Z> → write manually / use a different tool

## Cross-Skill Routing

<Only include verified sibling skills. After completing this skill: if X detected → recommend /Y. Verify each pointer's folder exists in Step 0.>

## Common Shortcuts — Do Not Take These

| What Claude might think | Why it's wrong |
|---|---|
| <specific shortcut for THIS skill> | <why it fails> |
| <specific shortcut for THIS skill> | <why it fails> |

<Include only if the skill has 3+ steps. For 2-step skills, skip — adding it adds noise without rubric payoff (cf. learnings: status-update, commit-message).>

## Before Marking Complete

- [ ] Step 0 files were read — list which ones
- [ ] Output references specific data from those files (or explicitly states none existed)
- [ ] Output format matches the template / worked example
- [ ] <skill-specific verifiable item>
- [ ] <skill-specific verifiable item>
- [ ] If output contains placeholders like `[Your Name]`, `[Company]`, regenerate or stop

<Skip checklist only if partial output is harmless (rare). Default: include.>

## After Completing: Log Learning

Append to `references/learnings.md`:
Date / What worked / What didn't / Edge case
```

**Mandatory defaults to bake in regardless of domain:**

1. Frontmatter description: 100+ chars, 3+ user-typed trigger phrases, "Do NOT use for X → use /Y" boundary, third person.
2. Step 0 with named files (not "check the context library").
3. At least one worked input/output example in the body.
4. Imperative verbs only — read the body aloud; if it sounds like a Slack ask, rewrite as a rundown (see learnings: conversational-codereview, where softening propagates 1:1 into output).
5. Exit checklist with verifiable items, not Claude's judgment.

**Domain-specific defaults — bake these into v0 directly. Do not defer to the eval loop.** (See `references/creation-patterns.md` for the canonical body of each. The intent is a v0 that converges in 0–1 iterations, not 3.)

| Domain | Mandatory v0 ingredient | Where in the SKILL.md it goes |
|--------|--------------------------|-------------------------------|
| Outreach | Step 0 extracts user's name + employer + role + target company + target role; exit-gate regex `\[[A-Z][^\]]*\]` blocks output if any `[Bracket]` placeholder remains | Step 0 + Exit checklist |
| Multi-step provisioning (5+ resources) | "Track these as you go" scaffold with blank lines per ID (INTEGRATION_ID, EVAL_ID, TASK_ID, RUN_ID, etc.) | Top of workflow, before Step 1 |
| Constraint-collecting (recipes, training plans, schedules) | Critical-section rule: "If a user-stated constraint conflicts with the inventory/input, state the contradiction explicitly before proceeding. Do not silently resolve." | First `## Critical` block |
| Health / safety / medical / financial | Safety/non-negotiable rules in FIRST `## block`, before Step 0, regardless of body length. If user wrote "I keep forgetting these," they ARE being violated — move them. | First `## block` |
| Config-producing (RFC, infra, ticket specs, salary numbers, training reps, recipe scaling, investor metrics) | Step 0 rule: "Any value not in user input or in the read-first files must carry the `[DEFAULT: X — confirm with Y]` marker." | Step 0 |
| Professional writing (status update, investor update) | Critical rule: "If user input or recent activity contains 'missed', 'delayed', 'blocked', 'rough', 'slipped', 'churned', surface in Blockers/Asks/Risks before Wins/Highlights. Burying bad news is a trust failure." | First `## Critical` block |
| Persona-style (tutor, coach, mentor) | Description third person; body restructured to Mode-Step format (Mode A: Step A1/A2/A3) — preserves teaching logic while making instructions imperative | Frontmatter + body skeleton |
| Content/writing with worked examples in body | Relax 500-line limit; embed 3+ annotated worked examples; worked examples are the specificity driver | Body |
| Scaffolding (second brain, repo init) | Explicit Step 1 existence check with 4-option user choice (Skip / Merge / Overwrite / Cancel) before any file writes; embed all "starter prompts" inline (no `${CLAUDE_SKILL_DIR}` refs) | Step 1 |
| Multi-job (3+ output formats) | STOP at intake — flag as split candidate. If unavoidable: rewrite as router with Step 1 channel-identification table | Pre-draft check |
| Synthesis (sprint kickoff, weekly digest, doc summary) | Step 0 names every input source explicitly (Linear, Slack, PRDs, meeting notes, etc.) with graceful-degradation per source — "if Linear MCP not connected, ask user to paste recent ticket activity" | Step 0 |
| Decision (build vs buy, PRD vs no-PRD) | Output template requires explicit recommendation + kill criteria ("what would change this decision"). Strawman-floor ban — alternatives must name strongest argument or advocate. | Output Format |

Save the draft to `<skills-dir>/<skill-name>/SKILL.md`. Snapshot a copy to `outputs/create-skill-runs/<skill-name>-<YYYY-MM-DD>/draft-v0.md`.

## Step 4: Build the Rubric (5 criteria, 0–20 each, /100 total)

Universal criteria (always include, ordered):
1. **Routing quality** — would Claude invoke this skill on relevant prompts? Score against: 100+ chars, WHAT+WHEN in first 250, 3+ trigger phrases, "Do NOT use for" boundary, third person, pushy phrasing.
2. **Output specificity** — uses real context (named files, real numbers, named stakeholders, user input) or generic training-data filler. Principled-decline path scores 14–18, not 4 — see anchor below.
3. **Output format consistency** — would three runs produce the same shape?

Domain criteria (4 and 5): from the table in Step 2.

**Principled-decline anchor.** When a test input has no required context (`/skill` with no args, or read-first files missing), the *correct* output is "stop, name what's missing, suggest a next step." Score 14–18 on specificity and 14–18 on the domain primary, not 4. To make the full pipeline rubric-visible, the worked-example section in the SKILL.md should show both the decline path and the full-context path.

Save to `outputs/create-skill-runs/<skill-name>-<YYYY-MM-DD>/rubric.md`.

## Step 5: Generate 3 Test Inputs

| # | Type | Example shape |
|---|------|---------------|
| 01 | Direct invocation | `/skill-name` or "use the skill-name skill" |
| 02 | Trigger phrase from description | a phrase quoted from the description that should fire the skill |
| 03 | Adjacent natural language | a request that *should* fire but doesn't quote any trigger verbatim — tests latent surface |
| 04 (optional) | Out-of-scope | a request that should NOT fire — score 0 if the skill answers it, 20 if it correctly declines or routes |

Save to `outputs/create-skill-runs/<skill-name>-<YYYY-MM-DD>/inputs/01.md`, `02.md`, `03.md` (and `04.md` if used).

## Step 6: Run Each Input Through the Draft

Use the Agent tool with `subagent_type=general-purpose`. Agent prompt:

```
You are running a Claude skill in evaluation mode. Read the skill at <path>/SKILL.md and follow its instructions exactly. Do not improve it. Do not skip steps. Do not add commentary. The user input is:

<input text>

Produce the output the skill would produce. If the skill calls for reading files that don't exist, note that in the output rather than fabricating.
```

Save to `outputs/.../outputs-draft/01.md`, `02.md`, `03.md`.

## Step 7: Score the Draft

For each input/output pair, score each criterion 0–20. Total /100. A+ = 90+. Save grades to `outputs/.../grades-draft.md`:

| Criterion | Score (/20) | Evidence |
|-----------|-------------|----------|
| Routing quality | X | [why] |
| Output specificity | X | [why] |
| Output format consistency | X | [why] |
| [Domain criterion 1] | X | [why] |
| [Domain criterion 2] | X | [why] |
| **Total** | **/100** | Grade |

Identify the lowest-scoring criterion across all inputs — that's the highest-leverage fix.

## Step 8: Edit and Loop Until A+

For each low-scoring criterion, identify the failure mode in the draft, then apply the relevant fix from this mapping (use as guide, not script):

| Failure | Likely cause | Fix |
|---------|--------------|-----|
| Routing low | description short / no triggers / no boundary / first person | Tip 1+2 + verify YAML name == folder name |
| Specificity low + zero context output | Step 0 missing or doesn't name files | Tip 4 — Source/Path/Extract table |
| Specificity low + correct decline | principled-decline path; score per anchor | add worked Phase-1 + Phase-2 example so full pipeline is visible |
| Specificity low + plausible defaults as facts | Tip 13 violation | add `[DEFAULT: X — confirm with Y]` marker rule in Step 0 |
| Format inconsistent | rules without worked example | Tip 10 — add worked examples; for skills with multiple valid sub-shapes, include 2–3 |
| Step-skipping observed | no anti-rationalization table | Tip 11 |
| Partial / unfinished output | no exit checklist | Tip 12 |
| Output drifts to adjacent topics | exclusions in body but not description | Tip 6 — move boundaries to description with `→ use /Y` pointer |
| Vague/conversational instructions ↔ vague output (1:1) | softening language in body | Tip 3 + Tip 11 — imperative rewrite is functional, not cosmetic |
| Buried critical rule (safety/medical/finance domain) | placement, not length | move to FIRST `## block`, before Step 0 |
| Outreach output contains `[Your Name]` | no extraction step + no scrub gate | Step 0 user-identity extraction + exit-gate regex `[A-Z][^\]]*\]` |
| Multi-step provisioning loses IDs | no ID scaffold | "Track IDs as you go" block at top |
| Constraint conflict silently resolved | collection without enforcement | Critical-section contradiction-flag rule |
| Persona-style first person | tutor/coach domain | Mode-Step restructure (Mode A: A1/A2/A3) — preserves teaching logic |
| References file doesn't exist | broken-pointer silent failure | embed inline OR create file OR add ## Critical warning |

**First-principles override.** If the rubric reveals a failure none of the above name, fix the failure. The mapping is empirical, not exhaustive.

Edit the SKILL.md in place. Save a snapshot to `outputs/.../iterations/iter-N-skill.md`.

Re-run failing inputs only (no need to re-run inputs already at A+). Re-score. Loop.

**Stop conditions:**
- All inputs ≥ 90 → ship.
- 3 iterations and net score hasn't moved → stop, document the blocker (often a structural ceiling: zero-context invocation, offline-eval methodology cap, missing user input, missing live MCP — see learnings).
- Score regressed → roll back, document what didn't work.

Save the iteration log to `outputs/.../iterations.md`.

## Step 9: Produce the Proof-of-Work Artifact

Folder structure:

```
outputs/create-skill-runs/<skill-name>-<YYYY-MM-DD>/
├── summary.md              ← what was built, before/after grades, total iterations
├── rubric.md
├── draft-v0.md             ← snapshot before any eval-driven edits
├── final-skill.md          ← snapshot of shipped SKILL.md
├── inputs/01.md, 02.md, 03.md
├── outputs-draft/01.md, 02.md, 03.md
├── outputs-final/01.md, 02.md, 03.md
├── grades-draft.md
├── grades-final.md
├── iterations/iter-N-skill.md (only if loops happened)
└── iterations.md
```

The user can audit any link in the chain. The shipped SKILL.md lives at `<skills-dir>/<skill-name>/SKILL.md`; the proof lives in `outputs/`.

**`--draft` escape hatch.** If and only if the user explicitly typed `--draft` in the request, stop after Step 3 and produce only the v0 SKILL.md. In that case:
- Add this line to the top of the file: `<!-- DRAFT — eval loop not run; A+ not verified. Run /improve-skill <path> before relying on this skill. -->`
- Write `summary.md` with status `DRAFT — UNVERIFIED` and a single recommendation: run `/improve-skill <path>`.
- Do NOT mark the task complete without telling the user the loop was skipped.

## Out of Scope

This skill does NOT handle:
- Editing or upgrading an existing SKILL.md → use `/improve-skill`
- Tuning CLAUDE.md project instructions → those are not skills; edit CLAUDE.md directly
- Building hooks or modifying settings.json → use `/update-config`
- Setting up recurring runs of a skill → use `/schedule` or `/loop`
- Reviewing arbitrary code or PRs → use `/review` or `/security-review`
- One-off prompts that won't be reused — a skill is for tasks repeated across sessions; for a single use, just run the prompt
- Renaming or restructuring a multi-skill folder → ask the user first

## Cross-Skill Routing

After creating:
- If the new skill should fire automatically (post-edit, on-stop, on-prompt) → recommend `/update-config` to add a hook
- If the new skill duplicates a sibling in the same folder → recommend merging or splitting
- If the new skill should run on a schedule → recommend `/schedule`
- If the user types "now make it better" pointing at the just-shipped skill → that's `/improve-skill`, not another `/create-skill` pass

## Common Shortcuts — Do Not Take These

| What Claude might think | Why it's wrong |
|---|---|
| "I have the spec from the conversation, I can skip Step 0 references" | The 12 tips and 25-run learnings are in the references. Skipping them means re-discovering failure modes through the eval loop instead of avoiding them in v0. Costs iterations. |
| "Three test inputs is overkill; one is enough" | One input is anecdote. Past learnings show direct-invocation, trigger-phrase, and adjacent-natural-language inputs each fail differently. Three reveals consistency. |
| "I'll add cross-skill links to /retention-analysis and /experiment-metrics — those probably exist" | Read the skills directory first. Unverified pointers cap routing at 18/20 and break worse than no link. |
| "The output format is obvious — I don't need a worked example" | "Obvious" means "I'm filling in the gap." Score it as if a stranger were grading. Skills with multiple valid sub-shapes (bullets vs prose, body vs no body) need 2–3 worked examples. |
| "I'll write the draft, then suggest the user run improve-skill" | The skill rewrites in place. A "draft + suggestion" output makes the user do the work — they won't. Run the eval loop. |
| "The skill only has 2 steps; I'll skip the anti-rationalization table" | Correct for 2-step skills (cf. status-update, commit-message learnings). Recount steps before deciding — numbered lists in the body usually mean 3+. |
| "The user said the skill is for 'PMs and engineers and content creators' — I'll make it general" | That's a multi-job skill. Past learning (mega-content-creator): canonical 4-jobs-in-one anti-pattern. Split before drafting. |
| "First-person body content sounds friendlier" | Routing failure (cf. first-person-tutor learning). Description must be third person. Body must be imperative. Persona-style preserves only by Mode-Step restructure. |
| "I'll log to learnings.md if I remember at the end" | The exit checklist requires it. Don't mark complete until logged. |
| "Iter-1 didn't move the score; the skill must be unfixable" | Read per-criterion deltas, not just totals. Often iter-1 fixed criterion A and broke criterion B. The fix is a targeted second pass, not abandonment. |
| "This is a one-time scaffolding skill; --draft is fine" | --draft requires the user to have typed it. Without that, run the loop — past learnings show "looks right" drafts hit F regularly. |

## Worked Example (full creation, end-to-end)

User prompt: "create a skill for writing weekly status updates for my manager."

**Step 1 spec:**
- name: `status-update`
- job: "Generate a weekly status update for an individual contributor's manager."
- domain: professional writing → primary: signal density, secondary: honesty flagging
- WHEN: "weekly update", "status update", "what should I send my manager", "Friday update"
- out of scope: "postmortem incident reports → use /postmortem; OKR check-in → use /okr-review"

**Step 3 draft v0** (excerpt) — frontmatter applies Tip 1+2; body has Step 0 (read meeting notes + last week's update + ticket activity), output template (Wins / Blockers / Asks / This Week format), worked example, exit checklist with `[ ] flagged any bad news (honesty)`.

**Step 4 rubric:** universal 3 + signal density + honesty flagging.

**Step 5 inputs:**
- 01: `/status-update`
- 02: "draft my weekly update for my manager"
- 03: "what should I tell my manager this Friday — I had a rough week"

**Step 6 run + Step 7 score:** Suppose 01 scores 88 (A), 02 scores 92 (A+), 03 scores 76 (B — honesty flagging 8/20 because the draft buried "rough week" in a Wins section).

**Step 8 fix:** add a Critical-section rule: "If user input or recent ticket activity contains words like 'missed', 'delayed', 'blocked', 'rough', surface it in Blockers/Asks before Wins. Burying bad news is a trust failure." Re-run input 03 only. Score 94. All inputs A+. Stop.

**Step 9 artifact:** saved to `outputs/create-skill-runs/status-update-2026-05-07/`. Append to `references/learnings.md`.

## Before Marking Complete

Do not consider this task finished until all of the following are true:

- [ ] Step 0 references were read — list which ones in the response (twelve-tips.md, audit-checklist.md, examples.md, learnings.md, creation-patterns.md, sibling skills directory)
- [ ] Spec intake completed — all 5 fields populated, none silently inferred
- [ ] Domain classified and rubric criteria 4 & 5 chosen with reason
- [ ] Draft v0 written to `<skills-dir>/<skill-name>/SKILL.md` AND snapshotted to outputs/
- [ ] YAML `name:` matches folder name (verified)
- [ ] All `references/*.md` paths in the draft body resolve to actual files (verified)
- [ ] No `${CLAUDE_SKILL_DIR}` or other unguaranteed env-var references in the draft (verified)
- [ ] Cross-skill routing pointers reference verified sibling skills (or section is omitted)
- [ ] Rubric written with 5 criteria + 0–20 anchors, saved to outputs/
- [ ] 3 test inputs generated and saved (4th out-of-scope optional)
- [ ] Each input run through draft v0 — outputs saved
- [ ] Draft outputs scored — grades-draft.md saved
- [ ] If any draft input scored under 90, eval loop ran (up to 3 iterations) and is logged
- [ ] All final inputs scored ≥ 90 OR stop-condition documented in iterations.md
- [ ] summary.md written: before/after grades, total iterations, what moved, any structural ceilings
- [ ] One entry appended to `references/learnings.md` for this run
- [ ] If `--draft` was used: drafted file is marked with the DRAFT comment, summary.md says UNVERIFIED, user was told the loop was skipped

If any item above is unchecked, complete it before finishing.

## After Completing: Log Learning

Append to `references/learnings.md` (in `create-skill/references/`, not the new skill's folder):

```
Date: [YYYY-MM-DD]
Target: [new skill name and path]
Domain: [class from Step 2]
Draft v0 grade: [X/100]
Final grade: [Y/100]
Iterations: [N]
Highest-leverage fix: [the one edit that moved the score the most]
What didn't work: [edits that didn't move the score]
Edge case: [anything unexpected — structural ceiling, missing fixture, multi-job spec caught at intake, etc.]
```

Create the file if it doesn't exist.
