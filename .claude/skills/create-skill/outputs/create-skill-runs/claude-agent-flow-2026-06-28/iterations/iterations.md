# Iteration Log — claude-agent-flow
Date: 2026-06-28

## Starting point
Draft v0 average: 83/100 (F)
Breakdown: 84/71/94 across inputs 01/02/03

## Iter-1

**Trigger:** Input 02 scored 71/100 (F). C3/C4/C5 all at 12/20.

**Root cause analysis:**
Draft v0's Step 1 had no instruction for partial-context handling. When the user provided a partial description ("quero automatizar relatórios semanais do Linear para Slack"), the skill:
- (a) Did not show a "here's what I know" summary — so the user couldn't verify what was inferred vs. missing
- (b) Embedded Q5 (error handling) and Q6 (NEVER rules) into a single compound question — Q6 was buried
- (c) Did not preview the 7-section brief structure for this intermediate state

Secondary root cause: No Phase 1+2 worked example in the skill — evaluator couldn't score C3/C4/C5 on Input 01's Phase 1 output because the full pipeline wasn't demonstrated.

**Changes applied to SKILL.md:**
1. **Description:** Added `/claude-system-builder` as a verified negative trigger with pointer (skill appeared and was verified mid-eval)
2. **Step 1, partial-context instruction:** Added paragraph: "When partial context is already provided: Open with 'Aqui está o que já sei:' followed by confirmed answers. Then ask only unanswered questions individually. Keep Q6 (NEVER rules) as its own standalone question."
3. **Worked example:** Added Phase 1 section showing the exact opening message for no-context invocation, transitioning to "User responds with full context → skill proceeds to Phase 2"
4. **Out of Scope:** Updated "Building full multi-component systems → plan separately" to "Full multi-component systems → use /claude-system-builder" (verified sibling)

**Score after iter-1:** 92/90/97 — all A+ — average 93/100

**Verification:**
- Input 02 gain: +19 pts. All from fixing the partial-context handling and Q6 standalone instruction.
- Input 01 gain: +8 pts. From Phase 1+2 worked example making the full pipeline rubric-visible.
- Input 03 gain: +3 pts. Minor refinements in step descriptions.

## Known ceilings (not iterated against)

| Input | Final score | Ceiling type | Reason |
|-------|-------------|--------------|--------|
| 01 | 92 | Phase 1 / no-context | Brief not produced; C3/C4/C5 evaluated on discovery message quality |
| 02 | 90 | Phase 1 / partial-context | Brief not produced; ceiling at 90 based on partial-context handling quality |

Both are within the expected A+ range for discovery-phase outputs. Consistent with lovable-prompt precedent (Input 01 reached 91).

## Decision: ship at iter-1

Average 93/100, all inputs ≥ 90/100. No further iterations needed.
