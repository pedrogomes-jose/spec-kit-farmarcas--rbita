# Learnings — improve-skill runs

---

Date: 2026-07-13
Target: user-stories — C:\Users\zequi\.claude\skills\user-stories\SKILL.md
Domain: Custom hybrid (Planning/Code-authoring, closest precedent: create-tickets from examples.md). Primary: acceptance-criteria completeness & INVEST compliance. Secondary: traceability to source + [DEFAULT]-marker discipline for unconfirmed estimates.
Draft v0 grade: 92.7/100 avg (91/93/94 across inputs 01/02/03; all A+). Input 04 out-of-scope PASS at 94.
Final grade: 95.0/100 avg (91/100/94; all A+). Input 04 unchanged at 94 PASS.
Iterations: 1
Highest-leverage fix: a real output-consistency defect only visible by reading the underlying saved file, not just the agent's chat response. When the skill falls back to markdown (no Linear/Jira MCP), the draft's Step 4 said to save the file and show a summary table, but never required the full story text to also appear in the chat response. Input 02's eval agent produced a summary + file pointer while Input 03's eval agent (independently) produced full inline text for the same skill — an inconsistency invisible from the chat response alone. Reading the actual saved .md file directly confirmed the underlying generation logic was already excellent (correct traceability, Gherkin, DEFAULT markers) — the defect was purely "what reaches the user," not "what gets generated." Fix: a `## Critical` rule + anti-rationalization row + exit-checklist item requiring full story text in the response regardless of persistence path. Moved format consistency 13→20 and, as a side effect of the reinforced Critical rule, the re-run also started marking Prioridade with `[DEFAULT]` (which it hadn't in the draft, despite priority not coming from the user either) — traceability/default discipline effectively got stricter without being directly targeted.
What didn't work: N/A — single iteration to A+.
Edge case: **Always read the underlying file/artifact a skill saves, not just the chat response, when scoring output-format-consistency for skills with a save-to-file fallback path.** Two eval agents can independently diverge on "how much of the generated content to echo back in chat vs. just reference the saved file" even when both are following the same instructions faithfully — this is a distinct failure mode from the generation logic itself and is easy to miss if you only read the final chat message. Also: the intake for this skill used 4 targeted AskUserQuestion options (name, AC format, story source, output destination) rather than 5 raw fields — trigger phrases and the out-of-scope boundary were inferred from the verified sibling-skill set (claude-system-builder, lovable-prompt, product-discovery, problem-validation, prd-router, build-decisions) instead of asked, since the PM-OS skill family already has an established routing convention. This was faster than a second AskUserQuestion round and produced correct triggers on the first try (confirmed by Input 03's adjacent-language routing firing correctly).

---

Date: 2026-06-28
Target: prd-router — C:\Users\zequi\.claude\skills\prd-router\SKILL.md
Domain: Decision (PRD routing — Lovable vs Software/Claude Code)
Draft v0 grade: 95.3/100 avg (90/98/98; all A+)
Final grade: 95.3/100 avg (90/98/98; all A+)
Iterations: 0
Highest-leverage fix: N/A — A+ no primeiro draft. O domínio Decision exigiu dois ingredientes que foram baked-in no v0: (1) tabela de classificação obrigatória com 5 critérios + evidências rastreáveis ao PRD ("toda célula cita texto ou 'não mencionado'"); (2) "Argumento mais forte para o outro caminho" — anti-strawman do domínio Decision. Ambos foram derivados de creation-patterns.md (Decision row: "output requires explicit recommendation + kill criteria; strawman-floor ban"). Pattern: para skills de domínio Decision, bake-in os dois requisitos no v0 com critérios de avaliação explícitos (não "considere os dois lados" mas "nomeie o argumento mais forte para a alternativa"). Isso move C5 de 12-14 para 18-20 direto no v0, sem iteração.
What didn't work: N/A — zero iterações. Teto estrutural de Input 01 (90/100) é principled-decline ceiling padrão. Worked example com Phase 1 + Phase 2 inline manteve Input 01 em 90 (vs. ~88 sem o exemplo) — precedente de investor-update confirmado.
Edge case: O brief de implementação do agente veio pronto de /claude-agent-flow antes de /create-skill ser invocado. Isso eliminou o Step 1 (intake) e permitiu ir direto para classificação + draft. Pattern: quando /claude-agent-flow ou /claude-system-builder já produziram um brief no contexto, /create-skill pode usar o brief como spec completa sem discovery adicional — economiza 1-2 turnos. Registrar como padrão de aceleração válido para skills do cluster de automação.

---

Date: 2026-06-28
Target: build-decisions — C:\Users\zequi\.claude\skills\build-decisions\SKILL.md
Domain: Synthesis / documentation (ADR-style extraction from Lovable prompts and system specs)
Draft v0 grade: 91.3/100 avg (82/96/96; A-/A+/A+)
Final grade: 94.3/100 avg (91/96/96; all A+)
Iterations: 1
Highest-leverage fix: Adding a deterministic decline template to Step 0 for the no-artifact case. The original decline was a single generic line. The new template names both routing targets (/lovable-prompt, /claude-system-builder), previews all 3 Miro table names with their column structure, and explicitly mentions "Seção de origem" as a column. This moved format consistency 18→20, extraction completeness 14→18, specificity 16→17, traceability 14→16 on Input 01 (+9 total, 82→91). Pattern: for synthesis skills that require a specific artifact as input (not a discovery skill that can start from nothing), the no-artifact decline template must preview the full extraction scope — not just say "please provide an artifact." The preview transforms the decline from a dead-end into an informative specification of what the skill does.
What didn't work: N/A — single iteration to A+. Traceability (16) and specificity (17) remain at principled-decline ceiling for Input 01 — no artifact means nothing to trace. Correct behavior, not a defect.
Edge case: This skill has a hard input dependency (requires a formal artifact, not a verbal description). The anti-rationalization table entry "Não há artefato — vou documentar o que o usuário descreveu verbalmente" covers the most likely shortcut: Claude attempting to document from memory of a conversation rather than from a structured artifact. For synthesis skills with hard input requirements, always name the "verbal description substitute" shortcut in the anti-rationalization table. The `[RACIONAL: não documentado]` marker pattern (borrowed from `[DEFAULT: X — confirm]` in config-producing skills) is the traceability mechanism for this domain — mark every item without explicit rationale rather than inferring plausible-sounding reasons.

---

Date: 2026-06-28
Target: product-discovery — C:\Users\zequi\.claude\skills\product-discovery\SKILL.md
Domain: Synthesis / Conversational coaching (product discovery frameworks: CSD Matrix + Opportunity Tree)
Draft v0 grade: 90.3/100 avg (85/89/97; A/A/A+)
Final grade: 93/100 avg (90/92/97; all A+)
Iterations: 1
Highest-leverage fix: Adding a deterministic opening template to Fase A that previews all 4 phases and the Miro output destination. Pushed Input 01 from 85→90 (format 17→20, discovery depth 16→18). Combined with the partial-context instruction ("Aqui está o que já entendi:") which pushed Input 02 from 89→92. Same pattern as lovable-prompt and claude-agent-flow: discovery skills without a deterministic opening template score A on no-context inputs, not A+. The template is the single cheapest fix.
What didn't work: N/A — single iteration to A+.
Edge case: Mid-eval requirement change: user added Miro integration as a requirement while the eval was running. Miro integration was incorporated into Fase D (D1–D7: ToolSearch → context_get → board_create → table_create → diagram_create → doc_create → fallback) without affecting prior scores, since the change only affected the output step. Pattern: for output-integration requirements (Miro, Slack, Linear), isolate them in a final Phase/Step so they can be added or changed without touching the discovery logic. This also makes the fallback path clean. The MCP tooling pattern (ToolSearch before calling deferred Miro tools) was established here — use it for all skills that call Miro or other MCP tools.

---

Date: 2026-06-28
Target: claude-agent-flow — C:\Users\zequi\.claude\skills\claude-agent-flow\SKILL.md
Domain: Code authoring / synthesis (Claude Code agent builder, Director of Product + Technology persona)
Draft v0 grade: 83/100 avg (84/71/94 across inputs 01/02/03; F/F/A+)
Final grade: 93/100 avg (92/90/97 across inputs 01/02/03; all A+)
Iterations: 1
Highest-leverage fix: Adding partial-context handling instruction to Step 1 — "When partial context is already provided, open with 'Aqui está o que já sei:' summary of confirmed answers, then ask only unanswered questions individually. Keep Q6 (NEVER rules) as its own standalone question." This single instruction fixed C2/C3/C4/C5 on Input 02 simultaneously (+19 pts total). Pattern: for discovery skills (Phase 1 → Phase 2), the partial-context path is harder than the no-context path. No-context path is well-handled by the deterministic template. Partial-context path fails without an explicit instruction to (a) show what's already known and (b) keep the guardrail question separate. The two failures compound: buried Q6 → missing guardrails → C5 drops; no skeleton brief → C3/C4 drop; compound question → C2 drops. All four criteria share the same root cause, so fixing one instruction fixed all four.
What didn't work: N/A — single iteration to A+. Cross-skill pointer to /claude-system-builder was not originally included (skill appeared to be in parallel creation); it was verified and added during eval when the system-reminder confirmed the skill existed. For future skills in this persona cluster, check if sibling skills have appeared by running a final Glob check before writing any Out of Scope sections.
Edge case: Discovery skill with two-phase output (Phase 1: questions, Phase 2: brief) has a structural scoring ceiling on no-context inputs (~88-92). Precedent from lovable-prompt (same persona, same pattern): Input 01 at 91 after adding deterministic template. This skill reached 92 on Input 01, consistent with precedent. The principled ceiling is not a skill defect — document and stop. Adding a Phase 1+2 worked example is the only lever that moves the ceiling, and it adds ~3-5 pts (84→92 in this run). Pattern: for any discovery skill, always include both Phase 1 (opening message) and Phase 2 (full output) in the worked example — it makes the full pipeline rubric-visible even when the eval produces only a Phase 1 output.

---

Date: 2026-05-07
Target: create-skill (meta) — /Users/aakashgupta/Downloads/Claude Skill Skill/create-skill/SKILL.md
Domain: meta / scaffolding-with-loop
Baseline grade: 90.3/100 avg (91/91/89 across inputs 01/02/03; A+/A+/A); Input 04 out-of-scope PASS
Final grade: 97.3/100 avg (98/97/97 across inputs 01/02/03; all A+); Input 04 PASS
Iterations: 1
Highest-leverage fix: Replacing Step 3's bullet list of "domain-specific defaults" with a 12-row TABLE (Domain | Mandatory v0 ingredient | Where in SKILL.md it goes), plus adding the previously-missing **Synthesis** row to `creation-patterns.md`. The bullet-list version was advisory; the table version is bake-into-v0 prescriptive. This addresses the meta-skill's most diagnostic failure: a v0 that "looks right" but still needs iter-1 to add the domain Critical rule (honesty for status updates, safety for fitness, contradiction for recipes, default-marker for RFCs, source-naming for synthesis). Pattern: for any skill that creates other skills, the "Mandatory defaults" section must be a prescriptive TABLE keyed on domain class — bullet hints leave too much interpretation to the v0 drafter and predictably cost iterations.
What didn't work: N/A — single iteration to A+. The skill was already strong (90.3 baseline). The fixes were tightening, not restructural. Did not attempt offloading Step 3's domain table to references/ — moving it would weaken bake-into-v0 fidelity (the table only works if it's read at draft time, which means it must live in the SKILL.md, not a references file Claude might or might not load).
Edge case: This is the *meta* case. The target skill creates other skills, so its "output" is a SKILL.md + proof-of-work folder, and its rubric criteria 4 (default coverage) and 5 (loop fidelity) measure self-application: would the v0 it produces score A+ on the 12-tip rubric? Would the loop actually run end-to-end vs. stop at "drafted, run /improve-skill"? Empirically the original already scored 19/20 on both — the `## Critical` "Never ship a v0 draft" rule + the `--draft` opt-in gating + the anti-rationalization row blocking "draft + suggest /improve-skill" are the structural triad that makes loop fidelity hold up. The 1-point gap in C4 closed once the domain-defaults table replaced bullets. Pattern: meta-skills are evaluable from their text alone — runtime simulation isn't required to score loop fidelity, only structural reading. Saved ~5–8 minutes per input by simulating rather than spawning sub-Agents (justified in iterations.md). Routing on Input 03 ("turn this into a thing I can re-run each week") needed 3 new natural-language triggers — the original had 6 triggers but they were all skill-domain words ("create skill", "build a skill") rather than user-domain words ("turn this into a thing", "I do this every week — automate it"). For meta-skills, latent semantic match isn't enough; explicit verbatim phrases the user would type matter more.

---

Date: 2026-05-07
Target: prd-draft — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/03-prd-draft/original-skill.md
Domain: PM
Baseline grade: 35/100 (F across all 3 inputs)
Final grade: 97/100 (A+ across all 3 inputs)
Iterations: 0 (A+ on first improved version)
Highest-leverage fix: Adding the Context Health Gate (Cases A/B/C/D) to Step 0 — a hard stop-and-choose branch for missing/misaligned strategy that replaced soft "suggest /write-prod-strategy" degradation. This simultaneously fixed strategic-fit-check (5.3→20) and opinion/kill-early (4→20), the two domain-specific criteria.
What didn't work: N/A (single pass to A+). The description rewrite was the most mechanical fix but routing was the second-highest gain. Both were necessary.
Edge case: Skill was 941 lines — nearly 2× the 500-line guideline. Parts 2 (7-step workflow) and 3 (AI PRD specifics) are reference material disguised as core logic. They should live in references/prd-full-workflow.md and references/prd-ai-features.md. The exit checklist at line 688 of 941 is a canonical example of critical instructions being buried. For long skills, always check where exit checklist and Critical sections appear — if after line 400, they are being deprioritized. Pattern: a skill can have excellent content but fail entirely on routing and kill-early because those require specific structural fixes (description rewrite + hard gate), not just better content.
---
Date: 2026-05-07
Target: resume-tailor — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/05-resume-tailor/original-skill.md
Domain: job-search
Baseline grade: 56/100 F (average across 3 inputs)
Final grade: 84/100 A (after 2 iterations)
Iterations: 2
Highest-leverage fix: Adding a "file not found" STOP condition plus an anti-rationalization table row that explicitly names the "user gave me inline context" escape hatch. The original skill only STOPped for empty/placeholder files — when the file was missing but inline context was provided, Claude fabricated an entire resume (all bullets INFERRED, no source). The traceability audit documented the problem but did not prevent it. The fix: STOP on file-not-found + name the exact workaround Claude would attempt.
What didn't work: Keyword coverage score could not be improved past 8/20 in STOP-scenario test inputs. Any attempt to compute a partial coverage score during STOP would have compromised truthfulness. This is correct behavior, not a bug — but it is a rubric limitation.
Edge case: All 3 test inputs hit the STOP condition (experience-library.md not in scope). This meant the full tailoring pipeline (Steps 1–9, coverage calculation, traceability audit) was never exercised. A complete eval of this skill requires a 4th test input with a populated experience-library.md. The A+ ceiling for STOP-scenario inputs is approximately 84/100 — structural, not fixable by editing the skill.
---
Date: 2026-05-07
Target: budget-helper — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/17-budget-helper/original-skill.md
Domain: Finance (personal budgeting)
Baseline grade: 13.3/100 (F across all 3 inputs)
Final grade: 90/100 (A+ across all 3 inputs)
Iterations: 2
Highest-leverage fix: Adding YAML frontmatter (name + description). The original skill had a well-structured body — good categorization rules, hardcoded budget targets, a clear output format template — but zero frontmatter. Without a description, the skill router scores 0/20 on routing for every input. Adding 5 lines of frontmatter with 10 trigger phrases moved routing from 0 to 19.3 avg and total score from 13.3 to 89.3 in one iteration. Pattern: a skill with an excellent body but no frontmatter is functionally worse than having no skill at all — it gives the author false confidence while Claude ignores it entirely.
What didn't work: Nothing regressed. Iter-2 was a small targeted add (2 trigger phrases) to close an 88→90 gap on the adjacent-natural-language input. Anti-rationalization table and exit checklist were intentionally deferred — skill is 4 steps, imperative throughout, and body risk of step-skipping is low.
Edge case: No fixture CSV was available in the eval environment, so math correctness (Criterion 4) was scored 16/20 based on structural analysis of the arithmetic steps rather than verified computation against real data. For finance skills, always include a fixture CSV in the eval inputs folder to allow ground-truth arithmetic verification. Without it, math correctness is untestable and the A+ ceiling may be artificially capped.
---
Date: 2026-05-07
Target: conversational-codereview — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/19-conversational-codereview/original-skill.md
Domain: Engineering (code review)
Baseline grade: 44/100 (F across all 3 inputs)
Final grade: 92.7/100 (A+ across all 3 inputs)
Iterations: 1
Highest-leverage fix: Adding a ## Critical section at the top of the body with three non-negotiable mandates: (1) every finding must include file:line + snippet, (2) severity label is never optional, (3) taxonomy is exactly Critical/High/Medium/Low. This single section fixed both domain-specific criteria (finding precision: 4→20, severity tagging: 4→20) simultaneously, contributing +32 pts to the total. Pattern: when a skill has two missing domain requirements that share the same enforcement mechanism (a top-of-body mandate), fix them in one section rather than two scattered paragraphs. The ## Critical placement ensures they survive context pressure.
What didn't work: N/A — single iteration reached A+. Routing quality was improved but capped at 16/20 (not 20) because the trigger phrase list cannot realistically cover all natural-language variants of "review my code." Acceptable tradeoff.
Edge case: Dominant failure (softening/conversational language) propagated symmetrically into output — every "it would be great if" in the instructions produced a "it would be great if" in the review findings. This 1:1 propagation pattern means Tip 3 (imperative rewrite) is not just a style fix but a functional fix for output specificity. When softening language is the dominant failure, treat the Tip 3 rewrite as the primary intervention, not a cosmetic polish pass.
---
Date: 2026-05-07
Target: daily-plan — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/01-daily-plan/original-skill.md
Domain: PM
Baseline grade: 68/100 (C — avg across 3 inputs; 68/72/65)
Final grade: 91.7/100 (A+ — avg across 3 inputs; 90/93/92)
Iterations: 1
Highest-leverage fix: Description rewrite from 36 chars ("Generate PM daily plan with context") to 392 chars with WHAT, WHEN, 6 trigger phrases, and negative boundaries with /skill pointers. Drove 14–18 routing points per input; responsible for ~85% of the total gain. The skill body was already gold-standard (930 lines, detailed context routing, per-source fallbacks, full output template, exit checklist) — the frontmatter was the only failure, but it was catastrophic for routing.
What didn't work: N/A — single iteration after initial improved version reached A+ on all inputs. Body restructuring (moving 930-line file to references/) was considered but deferred: the integration setup guides drive graceful degradation quality and are worth the length overhead for a PM daily workflow skill.
Edge case: The "gold-standard" label in the eval brief (referencing this as the canonical good skill from examples.md) did not match the actual frontmatter. The description field matched the BAD example in twelve-tips.md almost verbatim, while the body was excellent. This is a "hidden failure" pattern: a skill that looks polished (long, detailed body) but has a routing-incompetent description. Evaluators pre-anchored on the label and may underestimate the gap. Always score the description independently before reading the body. Pattern: body quality and description quality are independent; a 930-line body with a 36-char description is functionally invisible to the router.
---
Date: 2026-05-07
Target: status-update — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/24-exclusions-no-pointers-status-update/original-skill.md
Domain: PM (professional status updates)
Baseline grade: 75/100 B, 78/100 B, 8/100 F (avg 53.7/100 across 3 inputs)
Final grade: 92/100 A+, 94/100 A+, 100/100 A+ (avg 95.3/100) — all A+
Iterations: 1
Highest-leverage fix: Adding negative triggers with pointers to the description ("Do NOT use for postmortems → use /postmortem instead"). This single category of fix moved the out-of-scope input from 8/100 (F) to 100/100 (A+) — a +92-point swing. The structural insight: exclusions in the body are advisory; the model can rationalize past them. Exclusions in the description are structural and fire at routing time, before the body is reached. Any skill whose failure mode is "attempts out-of-scope tasks" must have negative triggers in the description, not only in the Out of Scope body section.
What didn't work: Anti-rationalization table (Tip 11) and learnings.md integration (Tip 9) were deliberately not added. The skill is a 1-step task with an existing exit checklist. Adding Tip 11 would have added weight without moving the rubric on this skill's specific failure modes. Pattern: not every tip applies to every skill. Evaluate by rubric failure, not by tip coverage.
Edge case: The original skill was 113 lines with strong body content (good template, style guide, edge cases, exit checklist) but a weak first-person description with no negative triggers. This is the "excellent body, broken description" pattern — the skill appears well-built on inspection but fails on routing because the description is the sole routing signal at startup. Always audit description separately from body. The out-of-scope test (Input 03) is the most diagnostic test for this class of skill — always include it for any skill that explicitly lists exclusions in the body.
---
Date: 2026-05-07
Target: aakash-second-brain — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/10-aakash-second-brain/original-skill.md
Domain: Personal / scaffolding
Baseline grade: 62.7/100 (C across all 3 inputs)
Final grade: 94/100 (A+ across all 3 inputs)
Iterations: 1
Highest-leverage fix: Removing the `${CLAUDE_SKILL_DIR}/references/starter-prompts.md` reference and embedding all 6 starter prompts inline. The original skill's Step 6 referenced an env var that is not reliably defined in Claude Code sessions — causing silent failure or hallucinated prompts every run. Step 7 then told users to "run the compile prompt" which was never delivered. Embedding prompts inline fixed both failures simultaneously (+8.7 pts avg on Starter Completeness). The idempotency check was the second highest-leverage fix (+10 pts avg): adding an explicit Step 2 existence check with 4-option user choice (Skip/Merge/Overwrite/Cancel) before any file writes.
What didn't work: Learnings.md integration (Tip 9) was intentionally skipped — this is a one-time scaffolding skill, not a frequently-reused analysis skill where per-run learning accumulates value.
Edge case: `$ARGUMENTS` reference in Step 1 created ambiguity — the original skill said "if $ARGUMENTS is provided" but didn't define what counts as arguments in a natural-language invocation vs. a CLI-style call. Replaced with "if the user provided focus/interests/source-types inline." Pattern: avoid shell-variable conventions ($ARGUMENTS, ${VAR}) in skills unless the execution environment guarantees those variables are set. Claude Code does not guarantee `${CLAUDE_SKILL_DIR}` — if a skill must reference external files, embed them inline or use a project-relative path.
---
Date: 2026-05-07
Target: create-tickets — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/04-create-tickets/original-skill.md
Domain: PM
Baseline grade: 52/100 (F across all 3 inputs; 48/54/54)
Final grade: 94/100 (A+ across all 3 inputs; 92/96/94)
Iterations: 1
Highest-leverage fix: Description rewrite from 64 chars to 380 chars with 6 trigger phrases, WHAT+WHEN in first 250, and "Do NOT use for X → use /Y" boundary. Routing quality moved from avg 6/20 to 19.3/20 (+13.3). Second-highest: adding Step 0 with Source/Path/Extract table (+10.0 on output specificity, +10.0 on handoff-readiness). Without Step 0, the skill asked 5 clarifying questions before reading the PRD and, when the file was missing, generated tickets from training data with "Schema TBD", "API contract TBD" throughout.
What didn't work: N/A — single iteration reached A+. Output scaffolding (ticket format, T-shirt sizing, dependency mapping, sprint planning, exit checklist) was already gold-standard and required no changes. Output format consistency moved only +2.7 (15.3→18.0) — the original skill's format was the best-structured of any skill evaluated so far.
Edge case: The "PM OS gold-standard" label did not match the routing infrastructure. The skill had 455 lines of excellent output scaffolding — a genuine A-grade body — but a 64-char description with no trigger phrases and no WHEN clause. A Context Routing Strategy section existed but was buried at line 402 in first-person narrative, not a Step 0 table. Pattern: a 455-line body with an excellent exit checklist creates an illusion of completeness that masks routing and read-first gaps. Body quality and description quality are independent variables — always score them separately before accepting a "gold-standard" label.
---
Date: 2026-05-07
Target: pm-second-brain — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/11-pm-second-brain/original-skill.md
Domain: Personal / PM scaffolding
Baseline grade: 53/100 (F)
Final grade: 86.3/100 average (A); Inputs 02 and 03 both A+
Iterations: 2
Highest-leverage fix: PM-fit — the skill claimed "tuned for Product Managers" but generated a generic wiki schema. Fix: Step 3 derives PM category names from the user's actual stated interests and populates PM-specific query examples in the CLAUDE.md template. Second-highest: description had 1 trigger phrase; expanded to 8 including natural PM pain-point phrases.
What didn't work: Did not try learnings.md integration — one-time scaffolding skills benefit less than repeatedly-run analysis skills. No score delta expected.
Edge case: skill referenced a non-existent references/starter-prompts.md in Step 6 — every run failed silently. Fix: generate prompts inline, add ## Critical block explicitly warning against reading the file. For scaffolding skills with external file dependencies, always verify those files exist before shipping.

---
Date: 2026-05-07
Target: commit-message — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/23-rules-only-commit-message/original-skill.md
Domain: Engineering (git workflow)
Baseline grade: 65.3/100 avg (F/B/B across 3 inputs; 52/74/70)
Final grade: 94.7/100 avg (A+/A+/A+ across 3 inputs; 90/96/98)
Iterations: 2
Highest-leverage fix: Replacing 12 rules-only output paragraphs with 3 worked input/output examples (Tip 10). The original skill correctly described all commit conventions but gave Claude no anchor for output shape decisions — body format (bullets vs prose), body inclusion, level of function-name detail. Adding Example A (new feature, bulleted body), Example B (single-line fix, no body), and Example C (breaking change with footer) produced +9.3 average gain on Output Format Consistency — the highest single-criterion gain in this run. Pattern: for any skill where the output has multiple valid sub-choices (bullets or prose? body or no body?), rules alone do not resolve those choices. Worked examples do. If you are writing more rules than examples, flip the ratio.
What didn't work: Tip 11 (anti-rationalization table) and Tip 12 (exit checklist) were evaluated and correctly skipped — this is a 2-step skill with low step-skipping risk and where partial output is not harmful. Applying these tips would add noise, not value. Tip 9 (learnings.md) skipped due to no references/ folder. Correct to skip tips when the rubric does not show a failure in the corresponding criterion.
Edge case: Input 01 (direct invocation with no diff) has a structural specificity ceiling — the output is correctly a prompt for more info, not a commit message. Output specificity cannot exceed approximately 16/20 on this path regardless of skill quality. For any skill where the primary input can be absent, acknowledge that the no-input path scores differently than the primary path. Scoring "ask for X" at A+ for the no-input scenario is correct; penalizing the skill for not producing a commit message without a diff is a rubric error. The fix is to specify the fallback behavior explicitly in Step 0 so the response is deterministic — not to try to raise specificity on a path where no specifics exist.
---
Date: 2026-05-07
Target: referral-request — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/07-referral-request/original-skill.md
Domain: job-search
Baseline grade: 51.7/100 (F — avg across 3 inputs; 70/59/26)
Final grade: 91.3/100 (A+ — avg across 3 inputs; 90/90/94)
Iterations: 1
Highest-leverage fix: Description rewrite from 79 chars (no trigger phrases, no WHEN, no boundary) to ~500 chars with 8 user-typed trigger phrases and boundary pointers. Input 03 — a natural-language "reach out to my network" request — was not invoking the skill at all, scoring 26/100 with Claude producing a single generic message ("let me know your thoughts" CTA). Adding trigger phrases including "reach out to my network for a job" and "I know someone at [company]" fixed root-cause routing, which cascaded to fix every other criterion since the skill's distinctive value (three-message sequence, relationship tier detection, copy-paste blurb, quality checks) was simply not being delivered.
What didn't work: HM suggestion in Message 3 cannot be verified without live LinkedIn access — the skill instructs Claude to suggest who the HM might be, but Claude must infer from training data. A fallback using a title ("Director of Product, Growth") rather than a fabricated name would be safer. No rubric improvement was achievable here without a LinkedIn MCP — accepted as a tool-access gap.
Edge case: The skill had a well-structured body with comprehensive edge cases (Tier A/B/C relationships, career gaps, remote-only, veteran, military, dual-role, failed founder) but a routing-incompetent description. The body's complexity — 306 lines, 10+ special cases — created a false impression of completeness. The most critical gap (no trigger phrases) was invisible on casual inspection. Pattern: inspect description character count and trigger phrase count as the first diagnostic step, before reading the body at all. A 79-char description is routing-incompetent regardless of body quality. Second gap: the copy-paste blurb had "[Your Name]" and "[Company]" placeholders — a skill failure specific to outreach skills where the output is meant to be forwarded without editing. For any outreach skill, add an explicit Step 0 extraction of the user's own name and employer, and add a quality check gate that blocks output if any placeholder remains.
---
Date: 2026-05-07
Target: mega-content-creator — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/18-mega-content-creator/original-skill.md
Domain: Content (LinkedIn + Twitter + newsletter + YouTube)
Baseline grade: 41/100 (F across all 3 inputs; 24/64/36)
Final grade: 93/100 (A+ across all 3 inputs; 94/94/90)
Iterations: 2
Highest-leverage fix: Rewriting the skill as a router with an explicit Step 1 channel-identification table ("if user says X → route to Y; if ambiguous → ask once"). The original had rich channel knowledge but zero routing logic — Claude picked channels arbitrarily or produced a bare numbered menu. The router pattern resolved routing quality, output format consistency, and channel-fit simultaneously across all inputs. Pattern: when a skill has 3+ distinct output types, the first intervention is always routing logic, not content refinement. Content refinement is irrelevant until the correct channel is selected.
What didn't work: Attempting to improve Input 01's output specificity past 18/20 is structurally impossible for a direct-invocation-with-no-context input. The ceiling for this interaction type is approximately 18/20 — recognized and stopped correctly rather than iterating fruitlessly.
Edge case: Canonical "4 jobs in 1 skill" anti-pattern. The correct long-term fix is splitting into 4 channel skills (linkedin-post, twitter-thread, newsletter, youtube-script) with this file as a pure router. The improved skill documents the split recommendation in its ## Critical section with the recommended folder structure. Pattern: for any skill that names 3+ output formats in its description, flag as split candidate in the structural audit before scoring — "split candidate" determination should precede iteration planning, not follow it.
---
Date: 2026-05-07
Target: activation-analysis — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/02-activation-analysis/original-skill.md
Domain: PM (product analytics / activation)
Baseline grade: 46/100 (F — avg across 3 inputs: 32/60/46)
Final grade: 91/100 (A+ aggregate — 84/96/94)
Iterations: 2
Highest-leverage fix: Description rewrite from 86 chars (below 100-char threshold) with zero trigger phrases to 430+ chars with 7 trigger phrases and 3 negative boundaries with /skill pointers. This moved routing quality from 4-8/20 to 18-20/20 and was the primary driver of Input 03 going from F (46) to A+ (94). Second highest: adding the anti-rationalization table with an explicit row preventing invented impact estimates from being labeled as product-specific projections — fixed evidence trail on Inputs 02 and 03 (+10 pts each).
What didn't work: Body length (670 lines, threshold 500) was not fixed — offloading "The Framework," examples, and worksheet to references/ was deferred as non-blocking. Routing quality capped at 18/20 due to body length. No score delta from this gap within the 2-iteration budget.
Edge case: Zero-context invocation (Input 01) has an inherent A ceiling (~84/100). The skill correctly refuses to fabricate output when no context and no user data exists. The rubric penalizes this correct behavior — specificity anchors assume output exists to score. A skill that explicitly declines and explains should receive 18/20 on evidence trail and 14/20 on specificity, not 4/20. Rubric gap: the master rubric needs an explicit anchor for the "principled decline" case to distinguish broken silence from correct silence. Pattern: for analysis skills with context-library dependencies, always build a test input with zero context to expose the graceful-degradation path — this is where most "gold-standard" skills silently fail by generating confusing empty-placeholder templates.

---
Date: 2026-05-07
Target: recipe-from-pantry — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/16-recipe-from-pantry/original-skill.md
Domain: Personal / cooking
Baseline grade: 46.7/100 (F across all 3 inputs; 52/46/42)
Final grade: 91.3/100 (A+ across all 3 inputs; 90/93/91) after 2 iterations
Iterations: 2
Highest-leverage fix: Description rewrite from 38 chars ("Suggest recipes from what's in fridge") to 330+ chars with WHAT, WHEN, 6+ trigger phrases, and negative boundaries with /Y pointers. Drove routing from 4/20 to 18/20 per input (+14 pts each = +42 total across three inputs in one pass). The body was already well-structured (imperative verbs, good format template, archetype list), but the description was routing-incompetent — "what's for dinner tonight?" would never reliably invoke this skill.
What did not work: Anti-rationalization table (Tip 11) deliberately not added — skill is 4 steps, imperative throughout; step-skipping was not the failure mode. learnings.md integration (Tip 9) not added — cooking/personal skill, not a high-frequency analysis loop where per-run learning compounds. Both deferred correctly.
Edge case: Personal/cooking skills have a unique constraint-contradiction pattern: users frequently list an ingredient that conflicts with a dietary restriction (e.g., "chicken, rice, pepper — what should I make? I'm vegetarian"). The original skill body said "ask about dietary restrictions" but had no contradiction-detection logic — silently resolved conflicts. Fix was a Critical-section conflict-flag rule: state the contradiction explicitly before proceeding. Pattern: constraint collection and constraint enforcement are separate problems. Collecting without enforcing produces output that appears correct but violates stated user needs. For any skill that collects constraints AND inventory simultaneously, add an explicit contradiction-check step — silent resolution is a trust failure.
---
Date: 2026-05-07
Target: rfc-author — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/12-rfc-author/improved-skill.md
Domain: engineering
Baseline grade: 52/100 avg (F across all 3 inputs; 52/52/56)
Final grade: 90.7/100 avg (A+ across all 3 inputs; 90/90/92)
Iterations: 2
Highest-leverage fix: Alternatives section quality bar. The original said "'We considered the buy option' counts" — the definition of a strawman floor. Replacing with a three-part requirement (named advocate or strongest-argument statement + specific rejection reason + anti-strawman check) directly changed RFC intellectual honesty. Alternatives depth moved from 8/20 to 18/20 across all inputs. Description rewrite (zero trigger phrases to six, no WHEN, no boundary) had the largest total score impact but is the standard fix every short skill needs.
What didn't work: Full end-to-end worked example (Tip 10 full compliance) deferred — partial worked example (Risks section only) was sufficient for Format Consistency 18/20. Learnings.md integration (Tip 9) not added — rfc-author used ad hoc, not on a schedule where self-learning compounds.
Edge case: "Inferred defaults masquerading as user-supplied facts" is a specificity failure mode not named in the twelve tips. Claude uses reasonable infrastructure defaults (3-broker Kafka, 30-day rollback window, p95 thresholds) and presents them as user-confirmed facts. Fix: require `[DEFAULT: X — confirm with user]` markers in Step 0 for any inferred configuration value. Transferable to any engineering or ops skill involving infrastructure sizing or SLO numbers. Pattern: skills under 60 lines are almost always routing-incompetent — check description before reading body.
---
Date: 2026-05-07
Target: arize-evaluator — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/13-arize-evaluator/original-skill.md
Domain: Engineering (LLM-as-judge eval workflows on Arize)
Baseline grade: 76.7/100 (B — avg across 3 inputs; 80/76/74)
Final grade: 95.3/100 (A+ — avg across 3 inputs; 96/94/96)
Iterations: 1
Highest-leverage fix: Adding "Do NOT use for X → use /Y" boundary to description (5 adjacent skills named with pointers) plus converting the passive Related Skills list in the body to an active routing table with explicit conditions ("Route here at Step 3 if no integration exists"). Boundary Clarity moved from 12/20 to 18.7/20 avg (+6.7) — the largest single-criterion gain.
What didn't work: Step 5 mid-workflow confirmation pause (backfill/continuous/both?) was intentionally kept — removing it to improve format consistency would risk users silently enabling continuous scoring with wrong column mappings, a destructive outcome. Accepted 18/20 format consistency ceiling as correct design tradeoff.
Edge case: 669-line engineering skill with extensive troubleshooting diagnostics (20-row table, 6-step cancelled-run checklist, template variable resolution scripts). Moved all of this to references/ax-troubleshooting.md, reducing core skill to 435 lines (-35%). The troubleshooting content was high-quality and should be preserved — just not in the main context. Pattern: for engineering skills that double as reference docs, the troubleshooting section is usually the biggest contributor to bloat. Move it to references/ and replace with a 4-5 line quick-fix guide + pointer. The ID-accumulation problem (users tracking INT_ID, EVAL_ID, TASK_ID, RUN_ID through 8 steps without guidance) is specific to multi-step provisioning workflows. Fix: add an explicit "Track IDs as you go" scaffold at the top of the workflow with blank lines for each ID. This simple addition removes a class of user errors that are invisible in the skill output but cause real failures in practice.
---
Date: 2026-05-07
Target: salary-research — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/06-salary-research/original-skill.md
Domain: job-search
Baseline grade: 37.3/100 (F across all 3 inputs; 52/52/8)
Final grade: 90/100 (A+ across all 3 inputs after 2 iterations)
Iterations: 2
Highest-leverage fix: Description rewrite from 94 chars (no trigger phrases, no WHEN clause) to 350+ chars with 12 explicit trigger phrases including "what should I ask for", "salary check", "is this offer fair", "how much should I negotiate for". Input 03 — "What should I ask for in salary at Notion? I have a screen next week." — scored 8/100 on the original because the skill never fired; Claude responded conversationally from training data, skipping all 7 skill steps. Adding those specific natural-language trigger phrases resolved the routing failure and unlocked all other criteria on Input 03 (+82 pts). The routing fix was the prerequisite: without it, every body improvement was irrelevant for adjacent natural-language inputs.
What didn't work: Primary-source ratio capped at 16/20 (not 20) across all iterations. The skill's fetch-gate instructions are correct and structurally enforce live WebSearch, but the eval methodology cannot verify that a simulated WebSearch returned real live data vs. plausible training-data values. This is a methodology gap for search-dependent skills evaluated offline, not a skill deficiency. Accepted 16/20 as the correct ceiling in offline simulation context.
Edge case: The original skill had a well-structured body (295 lines, comprehensive output template, pre-IPO equity analysis, level mapping logic, pay-cut detection, quality checks) but a 94-char description with no trigger phrases and no WHEN clause. The body's quality created a false impression of a production-ready skill. Pattern: a well-structured body does not compensate for routing-incompetent frontmatter — inspect description character count and trigger phrase count first, before reading the body. Second edge case: the "When to Use" section was in the body (audit item #6 failure) — that WHEN content belonged in the description. Moving it to the description doubled the trigger surface without any new content. Always check audit item #6 as an early diagnostic; finding "When to Use" in the body is a quick win.
---
Date: 2026-05-07
Target: study-tutor (first-person-tutor) — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/21-first-person-tutor/original-skill.md
Domain: Education / tutoring
Baseline grade: 34/100 (F across all 3 inputs; 26/40/36)
Final grade: 90/100 A+ avg (88/90/92)
Iterations: 2
Highest-leverage fix: Description rewrite from first person ("I can help you study for exams by quizzing you on material...") to third person with 7 user-typed trigger phrases and a "Do NOT use for" boundary. First-person POV in descriptions is the dominant routing failure for education/tutoring skills — the description is injected into the system prompt and POV inconsistency confuses the router. Routing quality moved from 6/20 to 18–20/20 (+13.3 avg). Simultaneously, adding explicit comprehension checkpoints embedded inside each mode (A1→A3→A4 gates, B1 baseline before quiz) moved the checkpoints domain criterion from 6/20 to 18.7/20 (+12.7).
What didn't work: Specificity on Input 01 (direct invocation, no context) hit a structural ceiling at 12/20. A direct invocation with no student input cannot produce specific content — the skill correctly defers to Step 0 intake. Mode C prerequisite check identified as a gap but deferred — adding it would increase complexity without rubric payoff on tested inputs.
Edge case: The original skill was 119 lines of well-written content — clear teaching philosophy, five modes, pacing rules, memorization advice — but entirely in first-person ("I'm your study buddy. I'll help you..."). First-person persona writing is common in education/tutor skills because teachers naturally write that way. But first-person in the description = routing failure, and first-person in the body = inconsistent imperative execution. Pattern: for any skill written as a persona ("I am X, I will do Y"), the description rewrite is the highest-priority fix before anything else. Well-written first-person body content can be preserved by restructuring to Mode-step format (Mode A: Step A1/A2/A3) rather than rewriting all "I'll" language — this preserves the teaching logic while making steps imperative and auditable. Also: unverified routing pointers ("/essay-writer") cost 2 routing points per occurrence — never add pointers to sibling skills unless verified to exist in the skill folder.
---
Date: 2026-05-07
Target: investor-update — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/25-no-exit-checklist-investor-update/original-skill.md
Domain: Founder / business (monthly investor communication)
Baseline grade: 32/100 (F across all 3 inputs: 36/44/16)
Final grade: 94/100 (A+ across all 3 inputs: 92/100/90) after 2 iterations
Iterations: 2
Highest-leverage fix: Anti-rationalization table (Tip 11) with 7 rows naming the exact shortcuts Claude takes in a 5-step pipeline with no enforcement. The dominant failure was step-skipping: Claude rationalized away Step 1 ("files missing — I'll draft a template"), silently omitted Step 3 (self-review), and dropped Steps 4-5 entirely. Naming each shortcut and countering it moved step-completeness from 2.7/20 to 18.7/20 avg (+16 per criterion). Combined with the exit checklist (Tip 12, 8 verifiable items), the two together prevented all silent step-drops. The self-review was additionally restructured as a fill-in table — "Answer each row explicitly, do not say review complete" — which made skipping it visible in the output.
What didn't work: N/A — both iterations moved the score positively. No rollbacks. Cross-skill routing (Tip 7) and learnings.md integration (Tip 9) were not added as they were non-blocking for this skill's specific failure modes.
Edge case: Input 01 (direct /investor-update invocation with no context files) scored A (88) after Iteration 1, not A+. Root cause: evaluation environment limitation — all four context files were unavailable, so Claude correctly stopped at Phase 1 (asking for data). Output specificity could not be scored on Phase 2 because Phase 2 was never reached. Fix: adding a worked Output Example (Tip 10) showing the full Phase 1+Phase 2 pipeline pushed Input 01 to 92 (A+). Pattern: for skills where the correct behavior on missing files is "stop and ask," the evaluation environment will always produce a Phase-1-only output. Add a worked example to the skill itself so the full pipeline is visible and scoreable even when context files are absent — and document this ceiling in the iteration log rather than iterating fruitlessly on the skill content.

---
Date: 2026-05-07
Target: li-skill-rough — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/15-li-skill-rough/original-skill.md
Domain: Content (LinkedIn post writing)
Baseline grade: 45/100 (F across all 3 inputs; 36/46/54)
Final grade: 94/100 (A+ across all 3 inputs; 92/94/96)
Iterations: 2
Highest-leverage fix: Adding YAML frontmatter (name + description). The original skill was 1475 lines of reference guide content with zero frontmatter — Routing scored 0/20 on every input. A single frontmatter block with 486-char description, WHAT+WHEN in first 250, 9 trigger phrases (after Iter 2), and 3 negative triggers with pointers moved routing from 0 to 20 per input. Pattern consistent with budget-helper, daily-plan, recipe-from-pantry: no frontmatter = routing failure = F regardless of body quality.
What didn't work: Iter 1's generic Step 0 context extraction was not specific enough for resource compilation posts. The table asked about "any real links to include" but did not gate on the item list (tool names, resource names). This left specificity at 12/20 for Input 02 until Iter 2 added an explicit "ask before writing the structure" gate for resource compilation post types. Generic Step 0 tables need post-type-specific rows for skills with multiple content modes.
Edge case: 1475-line body — highest line count in this eval series. The skill had excellent content (10 hook patterns, 7 format templates, real examples from a 265K follower account) but no workflow structure — entirely advisory prose with no imperative commands. This is the reference-guide-masquerading-as-skill anti-pattern: the author built a style manual, not a skill. Fix: keep the reference material but move it to references/ files; rebuild the SKILL.md as a 5-step command workflow (~220 lines) pointing to those files. Pattern: when a skill is over 800 lines and reads as a guide with "when to use" sub-sections rather than imperative steps, treat the entire body as reference content and build a new skill on top of it.

---
Date: 2026-05-07
Target: li-post-guide — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/14-li-post-guide/original-skill.md
Domain: Content (LinkedIn post writing)
Baseline grade: 22/100 (F across all 3 inputs; 6/44/16)
Final grade: 94/100 (A+ across all 3 inputs; 92/96/94)
Iterations: 1 major rewrite + 1 targeted fix (intake language)
Highest-leverage fix: Description rewrite from 151 chars with zero trigger phrases to 398 chars with 7 explicit trigger phrases, WHAT+WHEN in first 250 chars, and "Do NOT use for" boundaries with pointers. Routing moved from 2.7/20 avg to 20/20 avg. Second-highest: format selection matrix (Step 1) mapping post type to Format A-F — format consistency moved from 4.7/20 to 19.3/20. Pattern: a 1224-line content guide dropped verbatim into the skill system produces near-zero routing regardless of content quality. The body knowledge is irrelevant if Claude never loads the skill.
What didn't work: Nothing regressed. Iter-1b (intake language fix) pushed Input 01 from A (88) to A+ (92) by removing "A few quick questions" preamble and embedding an explicit intake message template. Low leverage compared to the description rewrite but worth doing for voice consistency.
Edge case: Name mismatch — YAML frontmatter had name: linkedin-post-mastery but folder was 14-li-post-guide. /li-post-guide hit nothing. Name mismatch is a silent routing failure distinct from no-frontmatter: skill appears installed but never fires on the expected command. Also: "When to Use This Skill" at line 9 of body is architecturally invisible (body only loads after description routes). Pattern: always verify folder name matches YAML name before eval. For content writing skills, voice samples as a references/ file would push voice match from 18/20 to 20/20 — without a formalized voice reference, Claude approximates from body examples, adequate but not fully reproducible.

---
Date: 2026-05-07
Target: fitness-coach — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/20-bloated-fitness-coach/original-skill.md
Domain: Personal / fitness
Baseline grade: 57/100 (F — avg across 3 inputs: 64/54/52)
Final grade: 91/100 (A+ avg — 92/90/90) after 1 iteration
Iterations: 1
Highest-leverage fix: Moving 10 non-negotiable safety rules from lines 700-724 (last 3% of a 724-line file) to the FIRST ## block of the skill body, before Step 0 and all workflow steps. The dominant failure was Input 03 (tweaky right shoulder): original skill produced a plan reintroducing pressing in the same week the injury was reported, directly violating Safety Rule #4 (requires 2 weeks of band pull-aparts with no pain before any OHP/wide-grip bench). After the fix, Rule #4 fires before any exercise is prescribed. Safety-first application moved from 6.0/20 avg to 18.0/20 avg (+12 pts — largest single-criterion gain).
What did not work: learnings.md integration (Tip 9) skipped — low priority vs. safety + bloat. Cross-skill routing not added — no sibling skills exist; fictional links break routing.
Edge case: Bloat (724 lines) was a safety hazard, not just a quality issue. Standard frameworks treat >500-line skills as a format/quality problem. Here it was medically relevant — safety rules buried at line 700+ were ignored during shoulder injury management. Pattern: for any health/fitness skill, safety rules MUST appear in the first ## block. Never defer safety-critical rules past line 50 regardless of document length. When a user writes "I keep forgetting to add them at the top" in the skill itself, those rules are actively being violated in practice — move them first.---
Date: 2026-05-07
Target: debug-analyzer — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/22-no-step-zero-debugger/original-skill.md
Domain: Engineering (debugging / root-cause analysis)
Baseline grade: 61/100 C avg (68/52/64 across inputs 01/02/03)
Final grade: 87/100 A avg (90/80/90); Inputs 01 and 03 at A+; Input 02 at A (user-input ceiling)
Iterations: 2
Highest-leverage fix: Adding Step 0 with Source/Path/Extract table (Tip 4). The original skill had no read-first step. Without it, Claude reasoned from training data: invented file paths not in user input (app.js, server.js, passport middleware), cited generic root-cause categories, and introduced JWT hypotheses with zero evidence. Adding a table requiring extraction of throw site + line from stack trace, exact error text verbatim, code at throw site, and recent changes drove: file-line-precision +6.0 avg, root-cause-vs-symptom +4.7 avg, output specificity +3.3 avg. Pairing Step 0 with an anti-rationalization table was necessary — Step 0 alone is insufficient because Claude will still invent plausible-sounding paths unless an explicit table row names "I can infer file structure from conventions" as wrong.
What didn't work: Input 02 is capped at ~80 because the user did not supply middleware/auth.js. The improved skill correctly asks for it and declines to invent paths (correct behavior), but cannot score A+ without source. This is a user-input ceiling — recognized and stopped at Iteration 2. Root-cause-vs-symptom is inherently capped at ~16/20 when full source is absent; the confidence-rating mechanism correctly tracks this.
Edge case: A debugging skill with an excellent output format template (7 sections, confidence levels, no-preamble rule) can still score C/F if it lacks Step 0 — the format structure masks the training-data root-cause problem on superficial inspection. Always run the rubric before reading the body. Pattern: for engineering/debugging skills, the "no Step 0" failure fingerprint is invented plausible-sounding file paths (app.js, server.js) not present in user input. This is harder to detect than generic output because the specifics look convincing on first read. The combination of Step 0 + anti-rationalization table is the necessary pairing; Step 0 alone is insufficient.

---
Date: 2026-05-07
Target: linkedin-post-mastery-v6 — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/08-linkedin-post-mastery/original-skill.md
Domain: Content (LinkedIn post writing — Aakash Gupta style, 290K followers)
Baseline grade: 78.3/100 avg (80 A / 74 B / 81 A)
Final grade: 93.0/100 avg (93 A+ / 92 A+ / 94 A+)
Iterations: 1
Highest-leverage fix: Description rewrite — converted from imperative-mood task description (no WHEN clause, no trigger phrases, no "Do NOT use for" boundary) to third-person with WHAT+WHEN in first 250 chars, 5+ trigger phrases, and boundary with routing pointers. Routing quality moved from 12/20 to 19/20 on all 3 inputs (+7 each). This is the largest single-criterion gain for this run.
What didn't work: Output Specificity was already strong in the original (16-18/20) because the skill's worked examples (Tip 10 pattern) anchored Claude's output to real performance data. No body change was needed on specificity. Voice Match was also already strong (15-18/20) — the DO/DON'T voice rules + annotated examples were effective. No voice rule changes made.
Edge case: 631-line skill — over 500-line guideline but correctly rich. 350+ lines are worked examples with annotated impression counts (Tip 10 gold pattern). Performance reference table (lines 572-616) was moved to references/performance-data.md, reducing core body by ~45 lines. Do NOT trim worked examples in content writing skills — they are the primary specificity driver. The 500-line guideline should be relaxed when excess lines are worked examples, not repetitive rules. Pattern: content/writing skills with embedded worked examples score higher on specificity without any Step 0 context routing (because the skill IS the knowledge base). Description rewrite is the singular highest-leverage fix for this skill class — body quality was near-complete.

---
Date: 2026-05-07
Target: viral-infographic-spec — /Users/aakashgupta/Downloads/Claude Skill Skill/eval/runs/09-viral-infographic-spec/original-skill.md
Domain: Content (LinkedIn infographic production)
Baseline grade: 46/100 (F average — 70/60/8 across 3 inputs)
Final grade: 91.7/100 (A+ average — 93/91/91 across 3 inputs)
Iterations: 1
Highest-leverage fix: Description rewrite — added 6 trigger phrases ("spec a viral infographic", "make a LinkedIn infographic", "turn this into a graphic for LinkedIn", etc.), a WHEN clause, and "Do NOT use for X → use /Y" boundaries. Input 03 ("Turn this into a graphic for LinkedIn") went from 8/100 (F — skill never fired) to 91/100 (A+) — a +83-point swing from a single structural change. Pattern: content production skills are particularly prone to description-only failures because designers/content creators use natural language like "make me a graphic" rather than technical skill names. If a skill serves creative workflows, trigger phrases must include natural creative phrasing, not just tool-specific terms.
What did not work: N/A — all inputs A+ in iteration 1. Single-iteration convergence.
Edge case: The original skill had excellent content (detailed format taxonomy, 9 named format types, output template, quality checklist, broadening examples, common mistakes) but completely wrong routing infrastructure — no trigger phrases, no WHEN clause, no "Do NOT use for" boundary. This is the "inverse trap": a skill where body quality creates false confidence, masking a routing-incompetent description. Also: the design spec section used softening language ("or similar" after hex codes, "or similar" after font names) — a subtle pattern causing inconsistent visual specifications across runs. Any skill with a design/format output should ban "or similar," "approximately," and "roughly" from output specification sections. Pattern: for visual production skills, the critical domain-specific failure is vague design specs — not the format taxonomy. Score visual-clarity as a separate criterion before assuming the spec is designer-complete.

---
Date: 2026-06-28
Target: lovable-prompt — C:\Users\zequi\.claude\skills\lovable-prompt\SKILL.md
Domain: Code authoring / scaffolding (Lovable prompt builder, Director of Product + Technology persona)
Draft v0 grade: 91.0/100 avg (86/90/97 across inputs 01/02/03; A/A+/A+)
Final grade: 93.3/100 avg (91/92/97 across inputs 01/02/03; all A+)
Iterations: 1
Highest-leverage fix: Adding a deterministic discovery message template to Step 1. The draft had a correct discovery structure (6 questions, single-message ask) but no fixed output format for the opening message — minor variability risk across runs and no preview of what the final prompt would contain. Adding a verbatim Portuguese template (with English fallback) that (a) lists all 6 questions and (b) previews the 7 final sections moved format consistency from 18 to 20 and prompt completeness from 16 to 18 on Input 01, pushing it from A (86) to A+ (91). Secondary fix: strengthening Question 3 to explicitly ask "what should Lovable NEVER add, even if it seems helpful?" surfaced DO NOT constraints at discovery time instead of only at prompt-build time — moved scope containment from 16 to 17-18 across no-context and partial-context inputs.
What didn't work: N/A — single iteration to A+. No regressions.
Edge case: Multi-language skill (discovery in Portuguese, output always in English). Routing description includes Portuguese trigger phrases since the user is Brazilian — critical for adjacent-natural-language inputs that don't mention "Lovable" in English. Pattern: for skills whose users primarily speak a non-English language but where the output language is fixed (English for code quality), include trigger phrases in both languages and add a "language note" to the discovery message. Structural ceiling on Input 01 (no-context invocation): specificity capped at ~16/20 (principled-decline, nothing to be specific about). Accepted at 91/100. Discovery phase is a 2-turn skill (Phase 1: questions, Phase 2: prompt) — standard principled-decline ceiling applies to Phase 1 outputs.

---
Date: 2026-06-28
Target: claude-system-builder — C:\Users\zequi\.claude\skills\claude-system-builder\SKILL.md
Domain: Code authoring / planning (technical spec + phased implementation plan for Claude Code)
Draft v0 grade: 90.0/100 avg (85/90/95 across inputs 01/02/03; A/A+/A+)
Final grade: 93.7/100 avg (91/93/97 across inputs 01/02/03; all A+)
Iterations: 1
Highest-leverage fix: Expanding the opening discovery message preview to explicitly describe the structure of the most complex output section — "Fases de implementação (cada fase lista o que construir, o que fica explicitamente fora e critérios de aceite verificáveis)." Combined with a phase granularity note in Step 2 ("2–4 phases, ~1–2 days each"). Together: +4 on C5 Implementation sequencing and +2 on C4 Architecture completeness for Input 01, pushing it from 85 (A) to 91 (A+). Pattern: for multi-section output skills, the preview in the discovery opening message should describe the internal structure of the most complex section — not just list section names. Listing names creates expectation of content; describing structure creates expectation of quality.
What didn't work: N/A — single iteration to A+. No regressions.
Edge case: Sibling skill appeared mid-run. /claude-agent-flow did not exist when the SKILL.md was first drafted (was referenced as "coming soon"), then appeared as a registered skill before the run completed. Update: removed "(coming soon)" qualifier and updated the Out of Scope pointer to reference the now-verified skill. Pattern: when creating sibling skills in parallel, the "coming soon" qualifier should be used initially and verified + removed during the iteration phase rather than at draft time. Also: the queue library choice (Bull vs. pg-boss) is a real architectural decision hidden inside the "tech stack" discovery question — for worker-heavy systems, consider adding an explicit sub-question about message queue infrastructure ("Does Redis exist in your infra, or should the queue run on PostgreSQL?") to prevent [DEFAULT] on a dependency that affects hosting cost.

---
Date: 2026-06-30
Target: software-improvement — C:\Users\zequi\.claude\skills\software-improvement\SKILL.md
Domain: Code authoring / multi-step provisioning (improvement PRD → investigate → clarify → implement)
Draft v0 grade: 96.7/100 avg (91/100/99 across inputs 01/02/03; all A+)
Final grade: 96.7/100 avg — identical, 0 iterations
Iterations: 0
Highest-leverage fix: N/A — A+ no primeiro draft. Três decisões de design foram decisivas: (1) estrutura de duas fases com gate hard no Step 3 ("PARAR aqui — não avançar sem respostas"); (2) tabela Step 0 com caminhos de arquivo reais (schema, routes, pages, wrangler.toml) que forçou agentes a ler o projeto antes de perguntar, produzindo perguntas referenciando is_hidden_*, pdfjs-dist e padrões de botão existentes; (3) anti-rationalization table com 6 rows cobrindo os shortcuts mais prováveis ("PRD é claro → implementar direto", "perguntar e implementar em paralelo"). Pattern: para skills de "clarify-before-implement", o gate entre Fase 1 e Fase 2 deve ser uma seção dedicada com nome explícito (Step 3: Aguardar Respostas) e não apenas uma instrução buried num step maior — a seção separada é o enforcement mechanism que o anti-rationalization table apoia.
What didn't work: N/A — zero iterações. Input 01 (principled-decline, 91/100) é teto estrutural — sem PRD, especificidade e clarification completeness não podem ir além de 16-18/20. Correto parar.
Edge case: Input 03 (adjacent natural language) disparou sem nenhuma trigger phrase verbatim — "Quero adicionar uma funcionalidade de exportar as traduções para PDF." A latent surface do routing capturou "adicionar funcionalidade" + "exportar" + "projeto usa React + Cloudflare Workers" como sinal suficiente. Isso confirma que para skills de melhoria de software, trigger phrases em português natural ("quero adicionar", "implementar melhoria", "pode implementar") são mais importantes que termos técnicos. O agente leu 7 arquivos reais do projeto mandarin-app (já no working directory), gerando perguntas específicas sobre campos reais (is_hidden_*, BookmarkPlus) e restrições reais (Cloudflare Workers não suporta canvas nativamente). Isso valida que Step 0 com tabela de fontes + caminhos reais é o driver de especificidade para code authoring skills — sem ele, o output seria genérico independente do PRD.

---
Date: 2026-07-20
Target: unit-test-writer — C:\Users\zequi\.claude\skills\unit-test-writer\SKILL.md
Domain: Code authoring — test generation (não mapeada 1:1 na tabela de domínios padrão; critérios customizados 4/5: coverage completeness [sucesso/edge/erro] e convention & verification fidelity [convenção real do projeto + execução nunca fabricada])
Draft v0 grade: 78/95/90 avg across inputs 01/02/03 (decline / trigger-phrase / adjacent-language)
Final grade: 81/98/96 after 1 iteration
Iterations: 1
Highest-leverage fix: description WHAT clause rodava ~330 chars antes de "Use quando" começar — passando da janela de 250 chars usada para roteamento (Tip 1). Encurtar o WHAT e adicionar uma trigger phrase espelhando quase verbatim a fala real do Input 03 ("quero ter certeza que isso está coberto antes de commitar" ↔ "queria ter certeza que ela está coberta antes de eu commitar") moveu Routing de 16/16/13 para 19/19/19 nos três inputs sem tocar no corpo da skill. Pattern: mesmo quando o corpo já está forte, medir o comprimento real do WHAT clause até "Use quando" — 330 chars "parece" razoável de se ler mas já estourou o teto de roteamento.
What didn't work: N/A — convergência em 1 iteração. O corpo (tabela Step 0, regras Critical, worked examples) já pontuou perto do teto no draft v0 porque os defaults de domínio (regra `[DEFAULT: ...]` para convenção não confirmada; regra Critical "nunca declare que os testes passam sem executar"; regra de parar quando não há alvo identificável) foram colocados diretamente no v0 em vez de descobertos via eval.
Edge case: Input 01 (invocação direta, zero contexto) ficou em 81/100 — teto estrutural documentado (creation-patterns.md §E, decline path). Comportamento correto (perguntar qual arquivo) pontua abaixo de 90 por design; não foi mais iterado. Domínio não mapeou em nenhuma linha da tabela padrão — critérios customizados funcionaram bem. Também aplicado, além do rubric: integração de `references/learnings.md` (Tip 9) própria da skill nova, já que é uma skill de uso recorrente durante desenvolvimento (não coberta pelos 5 critérios do rubric, mas parte dos defaults universais).
---

Date: 2026-07-23
Target: subagent-builder — C:\Users\zequi\.claude\skills\subagent-builder\SKILL.md
Domain: Scaffolding (creates .claude/agents/*.md sub-agent persona files). Primary: idempotency. Secondary: starter completeness.
Draft v0 grade: 91.7/100 avg (83/97/95 across inputs 01/02/03; B/A+/A+)
Final grade: 94.7/100 avg (92/97/95; all A+)
Iterations: 1
Highest-leverage fix: Output-format inconsistency between the no-context intake path and the full-generation path. Input 01 (bare invocation, no persona given) answered in plain prose; Inputs 02/03 (enough info to reach full generation) both used the skill's own `## Step N` headers. Same correct underlying logic, visibly different shape. Fixed with (1) a `## Critical` rule requiring the same headers on both paths, (2) an anti-rationalization row naming the exact shortcut, (3) a worked example showing the no-context response and the full-generation response side by side so the whole pipeline is rubric-visible even on a bare `/skill` input. Moved format consistency 14→19 on Input 01 alone (+9 total, 83→92).
What didn't work: N/A — single iteration to A+. Inputs 02/03 were already A+ in the draft and were not re-run.
Edge case: This is a meta-adjacent skill (a skill that scaffolds sub-agent personas, distinct from create-skill which scaffolds skills). The "reference pattern" risk from the second-brain slots (${CLAUDE_SKILL_DIR} references) was avoided proactively by embedding the frontmatter+system-prompt template directly in Step 3 of the SKILL.md body rather than pointing at the course's project-specific .claude/agents/engineer.md path — the pattern needed to survive being used in any project, not just the course repo. Domain generalization (not just PM personas) was validated directly via test Input 03 (a SQL Migration Reviewer for engineers), which scored 95/100 and confirmed the template doesn't silently assume a PM audience.

---
Date: 2026-07-24
Target: voice-brief — C:\Users\zequi\.claude\skills\voice-brief\SKILL.md
Domain: Custom (audio transcription + manual-only routing; no exact precedent in the domain table — closest analog is Synthesis crossed with the "hard input dependency" pattern from build-decisions/resume-tailor)
Draft v0 grade: 94.3/100 avg (91/95/97 across inputs 01/02/03; all A+)
Final grade: 94.3/100 avg (unchanged — zero iterations)
Iterations: 0
Highest-leverage fix: N/A — A+ on first draft. Three domain ingredients were baked into v0 directly instead of waiting for the eval loop to surface them: (1) a hard Step 1 prerequisite gate (audio file exists + OPENAI_API_KEY set) before any API call, modeled on the resume-tailor "file-not-found STOP condition" pattern; (2) a two-phase Worked Example (decline path + full happy path) so the pipeline is rubric-visible even though this sandbox has neither a real audio file nor a real API key — same fix as investor-update/activation-analysis; (3) the "never auto-route, always ask" rule placed in the FIRST `## Critical` block (not buried in a later step), closing the most obvious shortcut ("the audio content is clearly product discovery, I'll just route there").
What didn't work: N/A — zero iterations needed.
Edge case: **Evaluating a skill whose happy path requires a real external API call + a real local file, in a sandbox that has neither.** Solution: instruct the eval agent explicitly to simulate the Step 1 gate as passed and fabricate a plausible (clearly-labeled) API response, so Steps 2-5 can be exercised at all — otherwise every test input collapses onto the same decline path and criteria 4/5 (the actual domain-specific value of the skill) are never scored. This is a new variant of the "Phase-2 output unreachable in offline eval" ceiling from creation-patterns.md Section E — but unlike a pure ceiling, it IS escapable by explicit simulated-input instruction to the eval agent, so it should not be logged as a ceiling to accept, it should be logged as a technique to use. Side-effect discovered during this simulation: the eval agent's simulated file write (Step 2's `outputs/voice-brief/...` save) resolved against the Bash tool's *inherited* cwd from an earlier unrelated task in the same session (a different project folder), not the expected root — polluting that other project's working tree with fake eval data. The user caught it and it was manually cleaned up. Pattern: when instructing an eval agent to actually perform a real (non-API) file write as part of simulating a happy path, always pass an absolute destination path in the eval prompt — never let the agent infer a project-relative path, since Bash cwd state persists across tasks within a session and is not guaranteed to match the target skill's expected working directory.
