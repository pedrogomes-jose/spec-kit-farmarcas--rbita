# Iterations Log — lovable-prompt

## Iteration 1

**Problem identified:** Input 01 (direct invocation, no context) scored 86/100 (A), below A+ threshold.

**Root cause:**
- Format consistency 18/20: no deterministic template for discovery message → minor variability risk across runs
- Prompt completeness 16/20: discovery decline didn't preview the 7-section output → useful but incomplete
- Scope containment 16/20: discovery questions didn't explicitly ask about DO NOT constraints

**Fix applied (targeted, not structural):**
1. Added a deterministic "opening message template" to Step 1, in Portuguese (with English fallback instruction). Template lists all 6 questions and previews the 7 final sections.
2. Strengthened Question 3: added "What should Lovable NEVER add, even if it seems helpful?" — surfaces DO NOT constraints at discovery time rather than after.

**Result:**
- Format consistency: 18 → 20 (+2): template is now exact, same every run
- Prompt completeness: 16 → 18 (+2): 7-section preview makes principled-decline path informative
- Scope containment: 16 → 17 (+1) on Input 01; 16 → 18 (+2) on Input 02

**No regressions:** Input 03 (full context) unchanged at 97. Input 02 improved.

**Final scores:** 91 / 92 / 97 — all A+. Stopped.

## Stop condition

All 3 inputs ≥ 90 after 1 iteration. Shipping.
