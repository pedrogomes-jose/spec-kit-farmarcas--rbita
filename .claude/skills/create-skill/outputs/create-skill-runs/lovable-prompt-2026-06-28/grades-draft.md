# Draft Grades

## Input 01 — Direct invocation `/lovable-prompt`

| Criterion | Score (/20) | Evidence |
|-----------|-------------|----------|
| Routing quality | 20 | Direct invocation fires; description 500+ chars, 8 trigger phrases |
| Output specificity | 16 | Principled-decline anchor: asks all 6 questions specifically, no fabrication. Ceiling ~16 with no context. |
| Output format consistency | 18 | Consistent single-message format. Risk: no explicit template in skill body so minor variability possible. |
| Prompt completeness | 16 | Principled-decline: names all 6 missing pieces, suggests next step. No preview of what the final 7-section prompt looks like. |
| Scope containment | 16 | Questions include scope exclusions and integrations feeding into DO NOT. But doesn't explicitly gate on "what Lovable should NEVER add." |
| **Total** | **86/100 (A)** | Below A+ threshold. |

**Lowest criterion:** Format consistency (18) — no deterministic template means slight output variability across runs.
**Second lowest:** Scope containment (16) — discovery questions don't explicitly surface DO NOT constraints.

---

## Input 02 — Partial context (freelancer management)

| Criterion | Score (/20) | Evidence |
|-----------|-------------|----------|
| Routing quality | 20 | Explicit Lovable mention in input; skill fires |
| Output specificity | 18 | Acknowledges specific features (project list, freelancer task panel), asks targeted missing questions |
| Output format consistency | 18 | Consistent "what I understood / what I need" structure; not fully templated |
| Prompt completeness | 18 | Identifies 3 missing questions precisely; asks auth clarification that has architecture impact |
| Scope containment | 16 | Asks about integrations but doesn't explicitly ask "what should Lovable never add beyond scope?" |
| **Total** | **90/100 (A+)** | |

---

## Input 03 — Full context (personal training app)

| Criterion | Score (/20) | Evidence |
|-----------|-------------|----------|
| Routing quality | 20 | Explicit Lovable mention; natural language matches description |
| Output specificity | 19 | Specific hex colors, specific RLS rules per table, context-specific DO NOT rules, correct "no self-registration" constraint |
| Output format consistency | 20 | All 7 sections in order, code block, Portuguese usage note |
| Prompt completeness | 19 | All sections filled; scope items specific (exercise name, sets, reps, rest); Out of v1 comprehensive |
| Scope containment | 19 | 7 DO NOT rules including 2 context-specific; explicit out-of-v1; design system written with exact hex values |
| **Total** | **97/100 (A+)** | |

---

## Summary

| Input | Score | Grade |
|-------|-------|-------|
| 01 (direct invocation) | 86/100 | A |
| 02 (partial context) | 90/100 | A+ |
| 03 (full context) | 97/100 | A+ |
| **Average** | **91/100** | **A+** |

**Problem:** Input 01 is below A+ threshold (86/100). Structural ceiling applies (no-context invocation) but can be improved.

**Highest-leverage fix:** Add a deterministic discovery message template to Step 1 that (a) previews the 7 sections the final prompt will have, (b) includes prompt-in-English reminder. This raises format consistency to 20 and prompt completeness to 18 on Input 01.

**Secondary fix:** Strengthen discovery Question 3 to explicitly ask "what should Lovable NEVER add beyond the listed scope?" — this raises scope containment to 17 on Inputs 01 and 02.

Projected post-fix scores for Input 01: 20+16+20+18+17 = 91/100 (A+).
