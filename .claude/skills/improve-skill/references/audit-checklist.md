# Skill Audit Checklist — 11 Items + Bonus

Source: Aakash Gupta, "How to build 10/10 Claude Skills" — section 4.

Pull up the target SKILL.md. For each item, mark **PASS** / **FAIL** / **N/A** and quote the offending line if FAIL. The benchmark: a well-built skill triggers automatically on **9 out of 10** natural-language requests that should trigger it. If it fires on fewer, the description needs more trigger context. If it fires on requests that *shouldn't* trigger it, add negative boundaries.

---

## Description audit (items 1–6)

**1. Length over 100 characters.**
Under 100 and Claude is almost certainly missing it. Sweet spot is 250–500.

**2. At least 3 user-typed trigger phrases.**
Not what *you'd* name the skill — what *the user would actually type* when they need it. ("plan my day", "what's on my plate", "create tickets", "break this PRD into tasks".)

**3. Third person.**
"Generates X when the user asks Y" works. "I can help you with X" breaks routing because the description is injected into the system prompt and inconsistent POV confuses the router.

**4. WHAT + WHEN both in the first 250 characters.**
Description is loaded into the system prompt at startup. Routing happens against the start of the description. Bury the WHEN clause and Claude won't reach it before deciding.

**5. "Do NOT use for" boundary present.**
Stops over-triggering on adjacent requests. Bonus points if it includes a pointer ("→ use /other-skill instead").

**6. No "When to Use This Skill" section in the body.**
If you wrote when-to-use guidance in the body, move it to the description. The body never gets read until the description has already routed.

## Body audit (items 7–11)

**7. Imperative verbs throughout.**
"Review the diff. Check for X. Output as Y." If body lines read like requests ("Could you...", "Maybe..."), rewrite as commands.

**8. Output format specified.**
A template, a worked input/output example, or both. If Claude produces a different shape every session, this is missing.

**9. Read-first step.**
A `## Step 0` (or equivalent) that names specific files Claude should read before generating. Bonus: a Source/Path/What-to-extract table (Tip 4).

**10. Out-of-scope section uses pointers, not just exclusions.**
"Don't do X" = incomplete. "Don't do X → use /Y instead" = closes the loop.

**11. Body under 500 lines.**
If yes, leave it. If no, move detail to `references/` (one level deep) and scripts to `scripts/`. Keep core logic lean.

## Bonus audit (the four most-skipped patterns)

**B1. Cross-skill links present.**
If the skill produces analysis or branchable output (e.g., activation analysis that might surface a pricing issue), it should route to sibling skills explicitly.

**B2. Anti-rationalization table.**
For any skill with 3+ steps. A two-column table: "What Claude might think | Why it's wrong" — names each shortcut Claude is likely to take and counters it.

**B3. Exit checklist.**
For any skill where partial output is worse than no output. Verifiable items (`- [ ] Step 0 files read`, `- [ ] Output saved to outputs/...`) so Claude can't declare done before the work is actually complete.

**B4. learnings.md integration.**
For any skill used regularly. Step 0 reads `references/learnings.md`; an exit step appends a new entry. The skill teaches itself over time without manual rewrites.

---

## The benchmark

Run **10 natural-language requests** that should trigger the skill. If under 9 fire, the description still needs trigger context. If requests fire that *shouldn't*, add negative boundaries.

## One last thing: treat skills like code

Version control them. When you change the description, note what you changed and why. When a skill produces worse output after an edit, roll back. When you see the same failure three sessions in a row, that's a documented pattern — not a vague memory.

---

## Audit output template

When running this audit, produce this exact table. **Run items P0–P3 FIRST — they are pre-flight checks that make the rest of the audit meaningful.**

| # | Check | Status | Evidence |
|---|-------|--------|----------|
| **P0** | **YAML frontmatter present** (file starts with `---\nname: ...\ndescription: ...\n---`) | PASS / FAIL | first 5 lines |
| **P1** | **YAML `name:` matches folder name** (`name: foo` ↔ folder `foo` or `NN-foo`) | PASS / FAIL | yaml name vs folder name |
| **P2** | **All `references/*.md` paths in body resolve to actual files** | PASS / FAIL | list any broken refs |
| **P3** | **No `${ENV_VAR}` references unless guaranteed defined in the runtime** (e.g., `${CLAUDE_SKILL_DIR}` is NOT guaranteed) | PASS / FAIL | quoted env-var ref |
| 1 | Description over 100 chars | PASS / FAIL | "<actual desc>" (X chars) |
| 2 | 3+ user-typed trigger phrases | PASS / FAIL | quoted phrases |
| 3 | Third person | PASS / FAIL | quoted opening |
| 4 | WHAT + WHEN in first 250 chars | PASS / FAIL | first 250 chars |
| 5 | "Do NOT use for" boundary in description (not just body) | PASS / FAIL | quoted boundary |
| 6 | No "When to Use" section in body (it belongs in description) | PASS / FAIL | header location |
| 7 | Imperative verbs throughout body | PASS / FAIL | quoted weak line if any |
| 8 | Output format specified — template AND/OR worked example | PASS / FAIL | template/example present |
| 9 | Step 0 read-first — names specific files | PASS / FAIL | quoted Step 0 |
| 10 | Out-of-scope with pointers (`→ use /Y`) | PASS / FAIL | quoted section |
| 11a | Body under 500 lines — for skills with rules/process content | PASS / FAIL / N/A | actual count |
| 11b | Body length nuance — if over 500, are excess lines worked examples (Tip 10 gold pattern)? If yes, Tip-8 doesn't apply | N/A / PASS / FAIL | line ranges of worked examples |
| **11c** | **Safety-critical rules in first `## block`** (for health/fitness/medical/financial domains) | PASS / FAIL / N/A | quoted first `##` header + line number of safety rules |
| B1 | Cross-skill links — and pointers reference VERIFIED sibling skills (folder must exist) | PASS / FAIL / N/A | listed pointers, each verified |
| B2 | Anti-rationalization table for skills with 3+ steps | PASS / FAIL / N/A | quoted table |
| B3 | Exit checklist — verifiable evidence per item, not Claude's judgment | PASS / FAIL / N/A | quoted checklist |
| B4 | learnings.md integration — for repeatedly-used skills | PASS / FAIL / N/A | quoted refs |
| **B5** | **Inferred-defaults markers** (`[DEFAULT: X — confirm with Y]`) — for any skill that produces config-like output | PASS / FAIL / N/A | quoted instruction or "missing" |
| **B6** | **Placeholder scrubbing** — for outreach/copy-paste artifacts: exit gate blocks `[Your Name]` / `[Company]` / `[bracket-placeholders]` | PASS / FAIL / N/A | quoted gate |
| **B7** | **ID-tracking scaffold** — for multi-step provisioning skills (5+ steps creating named resources) | PASS / FAIL / N/A | quoted scaffold |
| **B8** | **Constraint contradiction enforcement** — for skills that collect AND apply constraints (recipes, training plans, schedules) | PASS / FAIL / N/A | quoted contradiction-flag rule |

## Critical-path order

If P0 or P1 fail, fix those FIRST. They make every other improvement irrelevant. A 1500-line skill with no frontmatter scores 0/20 routing on every input regardless of what's in the body. A folder rename costs 30 seconds and is invisible to inspection.

If P2 or P3 fail, fix next. A skill with broken refs fails silently every run and the failure mode is invisible from output (Claude proceeds without the missing content).

After pre-flight, items 1–10 (description + body audit) are the highest-leverage standard fixes. Item 11 (line count) is last.

Bonus items B1–B8 are skill-specific. Apply only when the corresponding rubric criterion fails. Don't cargo-cult.
