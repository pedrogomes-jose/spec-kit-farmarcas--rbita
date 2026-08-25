# Rubric — claude-agent-flow
Date: 2026-06-28

## Overview
This skill is a two-phase discovery + brief skill. Scoring accounts for Phase 1 (discovery) outputs vs. Phase 2 (brief produced) outputs. Phase 1 outputs are scored at a principled-decline ceiling of ~84-88/100 on C3/C4/C5 — the brief hasn't been produced yet, so those criteria are evaluated on the quality of the discovery message structure.

---

## Criterion 1 — Routing Quality (20 pts)
**Primary signal:** Does the skill fire on the right natural-language inputs and stay silent on out-of-scope ones?

| Score | Anchor |
|-------|--------|
| 20 | Fires immediately; no hesitation; description WHAT+WHEN+triggers all present |
| 17–19 | Fires but requires mild context or an exact skill name |
| 12–16 | Fires inconsistently — some natural-language phrasings miss |
| 6–11 | Fires only on exact command, misses most adjacent phrasing |
| 0–5 | Doesn't fire or fires on clearly wrong inputs |

**Test:** Would `/claude-agent-flow`, `"quero automatizar isso com Claude"`, and `"multi-agent flow"` all route to this skill? Would `"prompt para o Lovable"` route away?

---

## Criterion 2 — Discovery Completeness (20 pts)
**Primary signal:** Does the skill ask all 6 required questions before building the brief? Are they asked in a single message? Is the deterministic template used on no-context invocations?

| Score | Anchor |
|-------|--------|
| 20 | All 6 questions in one message; exact deterministic template on no-context; 7-section preview included; correctly identifies partial context and asks only unanswered questions |
| 17–19 | All 6 questions but minor deviation from template OR partial context not handled perfectly |
| 12–16 | Some questions missing OR questions dripped one at a time |
| 6–11 | Fewer than 4 questions OR discovery skipped in partial-context case |
| 0–5 | Discovery skipped entirely; proceeds directly to brief without confirmation |

**Test:** Does the skill ask about trigger, goal, tools, data flow, error handling, AND guardrails before producing a brief? On partial context, does it correctly identify which questions are already answered?

---

## Criterion 3 — Brief Section Completeness (20 pts)
**Primary signal:** Are all 7 sections present and correctly structured in the brief?

| Score | Anchor |
|-------|--------|
| 20 | All 7 sections present; none empty; format exactly as specified; expected outputs per flow step |
| 17–19 | 6/7 sections or one section slightly malformed |
| 14–16 | Phase 1 (discovery) output: 7-section preview clearly shown in opening message OR 5/7 sections in Phase 2 brief |
| 10–13 | Phase 1 with partial context but no skeleton shown; OR fewer than 5 sections in brief |
| 0–9 | Fewer than 5 sections; major structural gaps |

**Phase 1 anchor:** Skill in discovery mode — 7-section preview in opening message earns 16/20. No preview earns 12/20.

---

## Criterion 4 — Agent Architecture Completeness (20 pts) [PRIMARY]
**Primary signal:** Trigger, goal, tools, agent flow steps with expected outputs, error handling — all specified and internally consistent.

| Score | Anchor |
|-------|--------|
| 20 | All elements present; every flow step has expected output; tools in Step 3 match steps in Step 4; error table covers all failure-prone steps; DEFAULT markers on inferred values |
| 17–19 | All elements but 1 minor inconsistency (tool listed but not used in flow; or 1 step missing expected output) |
| 14–16 | Phase 1: all 6 discovery questions map directly to architecture concerns (trigger→Q1, tools→Q3, flow→Q4, errors→Q5); OR 2+ elements missing from Phase 2 brief |
| 8–13 | Missing trigger or missing error table; OR flow steps lack expected outputs throughout |
| 0–7 | Too vague to implement; no step-level detail |

**Phase 1 anchor:** Questions directly address all 5 architecture elements → 16/20.

---

## Criterion 5 — Scope Guardrails (20 pts) [SECONDARY]
**Primary signal:** NEVER rules are explicit, human-in-the-loop gates are specified, scope is closed, DEFAULT markers present.

| Score | Anchor |
|-------|--------|
| 20 | At least 2 explicit NEVER rules; HiL gate(s) specified with trigger condition; all inferred values carry [DEFAULT: X — confirm]; no implied capabilities |
| 17–19 | 2+ NEVER rules but missing DEFAULT markers; OR HiL gate present but condition vague |
| 14–16 | Phase 1: Q6 explicitly asks for NEVER rules; OR 1 NEVER rule in brief with HiL gate |
| 8–13 | Guardrails section present but generic ("be careful with X"); OR no HiL gate |
| 0–7 | No guardrails section; or scope implied beyond what user confirmed |

**Phase 1 anchor:** Q6 (NEVER rules) prominently asked in discovery → 15/20.

---

## Aggregate scoring thresholds
- A+ (≥90): All criteria strong; any Phase 1 ceiling acknowledged
- A (85–89): Strong but one criterion hitting Phase 1 principled ceiling
- F (<85): Meaningful gap in one or more criteria requiring fix

## Known ceilings (do not iterate against)
| Input type | Ceiling | Reason |
|------------|---------|--------|
| No-context invocation (Input 01) | ~88-91/100 | Phase 1 only; C3/C4/C5 capped until brief is produced |
| Partial-context (Input 02) | ~86-90/100 | Phase 1 with partial info; ceiling depends on partial-context handling quality |
