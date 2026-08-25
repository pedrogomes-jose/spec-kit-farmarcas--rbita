# Final Grades — after Iteration 1

## Input 01 — Direct invocation `/lovable-prompt`

| Criterion | Score (/20) | Evidence |
|-----------|-------------|----------|
| Routing quality | 20 | Direct invocation; 8 trigger phrases, 500+ char description |
| Output specificity | 16 | Principled-decline ceiling: asks all 6 questions, no fabrication |
| Output format consistency | 20 | Deterministic discovery message template added → same output every run |
| Prompt completeness | 18 | Template previews all 7 final sections → principled-decline path is now fully informative |
| Scope containment | 17 | Q3 updated: "what Lovable should NEVER add" explicitly surfaces DO NOT constraints at discovery |
| **Total** | **91/100 (A+)** | |

## Input 02 — Partial context (freelancer management)

| Criterion | Score (/20) | Evidence |
|-----------|-------------|----------|
| Routing quality | 20 | Explicit Lovable mention |
| Output specificity | 18 | Acknowledges specific features; asks targeted questions for missing answers |
| Output format consistency | 18 | Consistent "understood / need" structure |
| Prompt completeness | 18 | Identifies missing pieces precisely; asks auth model clarification with architecture rationale |
| Scope containment | 18 | Updated Q3 now explicitly asks "what should Lovable NEVER add?" in partial-context discovery |
| **Total** | **92/100 (A+)** | |

## Input 03 — Full context (personal training app)

| Criterion | Score (/20) | Evidence |
|-----------|-------------|----------|
| Routing quality | 20 | Explicit Lovable mention |
| Output specificity | 19 | Specific hex colors, specific per-table RLS rules, context-specific DO NOT rules |
| Output format consistency | 20 | All 7 sections in order, code block, Portuguese usage note |
| Prompt completeness | 19 | All sections filled, scope items granular, Out of v1 comprehensive |
| Scope containment | 19 | 7 DO NOT rules (2 context-specific), explicit exclusions, design system with exact hex values |
| **Total** | **97/100 (A+)** | |

---

## Summary

| Input | Draft | Final | Delta |
|-------|-------|-------|-------|
| 01 | 86 (A) | 91 (A+) | +5 |
| 02 | 90 (A+) | 92 (A+) | +2 |
| 03 | 97 (A+) | 97 (A+) | 0 |
| **Average** | **91** | **93.3** | **+2.3** |

All inputs ≥ 90. Stop condition met.
