# Creation Patterns — distilled from 25 improve-skill runs

Source: `learnings.md` in this folder, summarized into "build it right the first time" defaults. Pattern-match the spec to a row, then bake the row into the v0 draft *before* the eval loop. Each row exists because the corresponding failure cost real iteration time on a past skill.

For full incident detail, read the named slot in `learnings.md`.

---

## A. Frontmatter shape (all skills)

| Slot inspired | Pattern | Apply to v0 |
|---------------|---------|-------------|
| 01-daily-plan, 02-activation-analysis, 03-prd-draft, 04-create-tickets | "Gold-standard" body, 36–86 char description, zero trigger phrases — routing 4–8/20 | Always 100+ chars, 5+ user-typed trigger phrases, WHAT+WHEN in first 250 chars |
| 17-budget-helper, 14-li-post-guide, 15-li-skill-rough | No YAML frontmatter at all — routing 0/20 regardless of body | Frontmatter is non-negotiable; verify YAML name matches folder name |
| 21-first-person-tutor | First-person description ("I help you...") — routing 6/20 | Third person: "Generates X..." not "I help with X" |
| 24-status-update | Body has `## Out of Scope` but description has no `Do NOT use for X` boundary — out-of-scope input scores 8/100 | Negative triggers go in the description with `→ use /Y` pointers, not only in the body |

## B. Step 0 read-first shape (all skills with file/context dependencies)

| Slot inspired | Pattern | Apply to v0 |
|---------------|---------|-------------|
| 22-no-step-zero-debugger | No read-first step — Claude invents file paths (app.js, server.js) not in user input | Step 0 with Source/Path/What-to-extract table, even when context is "the user's prompt" |
| 04-create-tickets | "Context Routing Strategy" buried at line 402 in narrative form | Step 0 must be a TABLE near the top, not narrative buried in a long body |
| 10-aakash-second-brain, 11-pm-second-brain | References `${CLAUDE_SKILL_DIR}/...` files — silent failure every run | Never reference unguaranteed env vars; embed inline or use project-relative paths |

## C. Domain-specific defaults

### Outreach (cover letter, referral, recruiter, intro, cold email)

From slot 07 (referral-request).

- Step 0 extracts: user's name, current employer, current role, target company, target role, relationship tier (A/B/C).
- Output template: copy-paste-ready — no `[Your Name]`, `[Company]`, `[Their Role]` placeholders.
- Exit gate: regex scan output for `\[[A-Z][^\]]*\]`; if any match, regenerate.
- HM/recruiter-name suggestion: prefer titles ("Director of Product, Growth") over fabricated names. If MCP-less, never invent a name.

### Multi-step provisioning / setup (5+ steps creating named resources)

From slot 13 (arize-evaluator).

- Top-of-workflow scaffold:
  ```
  ## Track these as you go
  INTEGRATION_ID: ___
  EVALUATOR_ID: ___
  TASK_ID: ___
  RUN_ID: ___
  ```
- Each subsequent step references the ID by name.
- Move troubleshooting tables to `references/<skill>-troubleshooting.md`; replace with 4–5 line quick-fix guide + pointer.

### Constraint-collecting skills (recipes, training plans, schedules)

From slot 16 (recipe-from-pantry), slot 20 (fitness-coach).

- Critical-section rule: "If a user-stated constraint conflicts with the input/inventory, state the contradiction explicitly before proceeding. Do not silently resolve."
- Example trigger: "chicken, rice, pepper — what should I make? I'm vegetarian."
- For fitness/health domains, this rule is safety-critical and lives in the FIRST `## block`, not buried.

### Health / safety / medical / financial

From slot 20 (fitness-coach — safety rules at line 700 of 724 were actively violated).

- Safety/non-negotiable rules go in the FIRST `## block` of the body. Before Step 0. Before workflow.
- If the user wrote "I keep forgetting to add these at the top," the rules ARE being violated. Move them.
- Bloat in these domains is not a quality issue — it's a harm vector.

### Config-producing skills (RFC, infra, ticket specs, salary numbers, training reps, recipe scaling, investor metrics)

From slot 12 (rfc-author).

- Step 0 rule: "Any value not in user input or in the read-first files must carry the `[DEFAULT: X — confirm with Y]` marker."
- Bad: "p95 latency must stay under 200ms during cutover." (Looks great. Came from training data.)
- Good: "p95 latency [DEFAULT: < 200ms — confirm with @sre]"
- The marker is ugly on purpose — it forces a confirm step that quiet defaults skip.

### Persona-style domains (tutor, coach, mentor, advisor)

From slot 21 (first-person-tutor).

- Description must be third person. Routing fails on first-person descriptions.
- Body restructure: Mode-Step format (Mode A: Step A1/A2/A3) — preserves the teaching/coaching logic while making instructions imperative and auditable.
- Do not rewrite every "I'll" line in isolation; restructure the modes.
- Verify any cross-skill pointer (e.g., "/essay-writer") exists in the skill folder. Unverified pointers cost 2 routing points each.

### Content / writing skills with worked examples in body

From slot 08 (linkedin-post-mastery, 631 lines, 350+ lines worked examples).

- The 500-line guideline relaxes when excess lines are worked examples (Tip 10 gold pattern).
- Worked examples are the specificity driver — do NOT trim.
- Move only reference-data tables (performance reference, archive of past output) to `references/`, not the examples.

### Reference-guide-masquerading-as-skill (over 800 lines, advisory prose, no imperative steps)

From slot 14 (li-post-guide, 1224 lines), slot 15 (li-skill-rough, 1475 lines).

- Anti-pattern: the author built a style manual, not a skill.
- Fix: keep the reference material as `references/<topic>.md` files; rebuild SKILL.md as a 5-step command workflow (~220 lines) pointing to those files.
- Diagnostic: if every section has "when to use" sub-sections rather than imperative steps, the body is reference content, not skill content.

### Scaffolding skills (second brain, repo init, project bootstrap)

From slot 10 (aakash-second-brain), slot 11 (pm-second-brain).

- Idempotency: explicit Step 1 existence check with 4-option user choice (Skip / Merge / Overwrite / Cancel) before any file writes.
- Embed all "starter prompts" inline. Do not reference `${CLAUDE_SKILL_DIR}/references/starter-prompts.md` or similar — the env var is not guaranteed.
- For one-time scaffolding skills, learnings.md integration (Tip 9) can be skipped — no compounding value.

### Synthesis skills (sprint kickoff, weekly digest, doc summary, multi-source roll-up)

Inferred from slot 04 (create-tickets) and slot 24 (status-update) patterns plus the create-skill eval (Input 03 sprint-kickoff).

- Step 0 names every input source explicitly. Don't write "the team's tools" — write "Linear (recent tickets), Slack (#standup channel last 5 days), PRD backlog (`outputs/prds/`), meeting notes (`outputs/meeting-notes/`)."
- Per-source graceful degradation: "if Linear MCP not connected, ask user to paste recent ticket activity"; "if Slack MCP not connected, ask user to paste standups." Each source needs a fallback so the skill works in MCP-less environments.
- Output format must specify dedup behavior: "If a topic appears in both standups and tickets, list once with both sources cited."
- Coverage criterion = "every named input source is represented in the output." If a source is empty, surface that explicitly ("no PRD activity this week"), don't silently omit.
- Signal/noise criterion = "separate this-week-mattered from this-week-was-trivia." Bake a Critical rule: "Group output as Decisions / Blockers / Routine — do not flatten into one bullet list."

### Multi-job skills (3+ output formats in description)

From slot 18 (mega-content-creator: posts AND tweets AND newsletters AND YouTube scripts).

- STOP at intake. Flag as split candidate before drafting.
- If unavoidable in one file: rewrite as a router with explicit Step 1 channel-identification table ("if user says X → route to Mode Y; if ambiguous → ask once").
- Document the recommended split (folder structure for the N skills) in the ## Critical section.

---

## D. Universal "build it right the first time" defaults (every skill)

1. **Description**: 100+ chars, 3+ user-typed trigger phrases, "Do NOT use for X → use /Y" boundary, third person, pushy phrasing ("Use when..."). The description is the entire routing surface — it loads at startup; the body does not.

2. **Frontmatter integrity**: YAML present, `name:` matches folder name. Mismatch = silent routing failure (slot 14).

3. **Step 0 read-first table**: Source / Path / What to extract. Names specific files. Not "check the context library."

4. **Imperative body**: Every line is a command. "Read the file. Check for X. Output as Y." Not "Could you take a look?" Softening propagates 1:1 into output (slot 19).

5. **Worked example in body**: At least one input → output pair. For skills with multiple valid sub-shapes (bullets vs prose, body vs no body, with-footer vs without), include 2–3 examples. Rules alone never resolve sub-shape choices (slot 23).

6. **Out-of-scope with pointers**: "Don't do X → use /Y" not just "Don't do X." Boundaries in description fire at routing time; in body they're advisory.

7. **Cross-skill links — verified only**: Read sibling skills folder before writing pointers. Unverified pointers cap routing at 18/20 (slot 21).

8. **Anti-rationalization table** for skills with 3+ steps. Skip for 2-step skills (slot 23, slot 24 — adding it adds noise without rubric payoff).

9. **Exit checklist** with verifiable items. Default: include. Skip only if partial output is harmless (rare).

10. **Body under 500 lines**, with one exception: worked-example-driven content/writing skills (slot 08).

11. **No unguaranteed env vars** (`${CLAUDE_SKILL_DIR}`, `$ARGUMENTS` in natural-language contexts). Embed inline or use project-relative paths.

12. **Inferred-default markers** for any config-like output. `[DEFAULT: X — confirm with Y]`.

13. **Placeholder scrubbing gate** for any copy-paste artifact output.

14. **`learnings.md` integration** for skills used regularly. Skip for one-time scaffolding.

---

## E. Known structural ceilings (do not iterate against)

These are not skill defects. Recognize and stop.

| Ceiling | Where it shows up | Score cap |
|---------|-------------------|-----------|
| Direct invocation `/skill` with no args | Input 01 in most evals | Specificity ~12–18/20 — correct decline behavior, scored per principled-decline anchor |
| Required user input absent (e.g., diff, file path, JD) | Input 02 sometimes | Domain primary ~16/20 — skill correctly asks; cannot score A+ on missing input |
| Live data dependencies absent (LinkedIn HM, WebSearch results, real-time pricing) | Various | ~84–88/100 — methodology gap, not skill gap |
| Fixture data absent (CSV for finance, voice samples for content) | Slots 17, 06, 14 | One criterion capped 14–18/20 — log as fixture-needed, do not iterate |
| Phase-2 output unreachable in offline eval | Slot 25 (investor-update Input 01) | Add a worked Phase-1+Phase-2 example in the SKILL.md so the full pipeline is rubric-visible |

If a final score is below 90 because of one of these ceilings, document the ceiling in `iterations.md` and ship. Do not waste iterations chasing them.
