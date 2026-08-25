# Grades — Draft v0
Date: 2026-06-28

## Scores by input

| Criterion | Input 01 | Input 02 | Input 03 |
|-----------|----------|----------|----------|
| C1 Routing quality | 20 | 19 | 19 |
| C2 Discovery completeness | 20 | 16 | 19 |
| C3 Brief section completeness | 16 | 12 | 19 |
| C4 Agent architecture completeness | 14 | 12 | 18 |
| C5 Scope guardrails | 14 | 12 | 19 |
| **Total** | **84** | **71** | **94** |
| **Grade** | **F** | **F** | **A+** |

**Average: 83/100 (F)**

---

## Analysis

**Input 01 (84/100):** Structural ceiling. Deterministic template fires correctly; all 6 questions asked; 7-section preview present. C4/C5 at 14/20 because no brief is produced — architecture and guardrails can only be inferred from the question structure. Lovable-prompt precedent shows this type of output can reach 91/100 with a Phase 1+2 worked example making the full pipeline visible.

**Input 02 (71/100):** Lowest score. Root causes:
1. No "here's what I know" summary — user doesn't know what was inferred vs. what's missing
2. Q6 (NEVER rules) buried inside compound Q4 — guardrail discovery not prominent
3. No skeleton of the 7-section brief — C3/C4/C5 can't score higher without it

**Input 03 (94/100):** A+. Brief is complete, all 7 sections, 3 NEVER rules, DEFAULT markers, correct flow steps with expected outputs. Minor internal consistency note on "file skip" behavior in error table vs. guardrail 2.

---

## Lowest criterion to fix

**C3/C4/C5 on Input 02** — all at 12/20.

**Root cause:** Step 1 does not tell Claude how to handle partial context. The anti-rationalization table does not address "I'll ask all questions even if some are already answered" OR "I'll embed Q6 into a compound question." 

**Targeted fix for iter-1:**
1. Add to Step 1: partial-context handling instruction — "If partial context is provided, open with 'Aqui está o que já sei:' summary of confirmed answers, then ask only unanswered questions individually. Keep Q6 (NEVER rules) as a standalone question."
2. Extend worked example to show Phase 1 opening message + user's full response + Phase 2 brief as a complete pipeline.
3. Update Out of Scope to add verified pointer → /claude-system-builder.
4. Update description boundary to include → /claude-system-builder.
