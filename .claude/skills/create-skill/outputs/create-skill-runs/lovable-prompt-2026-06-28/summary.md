# Summary — lovable-prompt creation run

**Date:** 2026-06-28
**Skill path:** C:\Users\zequi\.claude\skills\lovable-prompt\SKILL.md
**Status:** SHIPPED — A+ verified

## What was built

A skill for acting as Director of Product + Technology when creating prompts for Lovable (AI web app builder). The skill:
1. Runs a 6-question discovery to lock problem, users, MVP scope, stack, design, and integrations
2. Generates a structured 7-section English prompt (Context, Stack, Design System, Scope, Out of v1, Security, DO NOT)
3. Includes 5 universal DO NOT rules + context-specific ones to prevent Lovable from over-helping
4. Delivers the prompt in English (code block) + a usage note in the user's language

Key persona principles baked in:
- All prompts in English (code quality)
- Scope is always closed (Out of v1 section mandatory)
- Security first (Security section mandatory even for non-sensitive data)
- Design system always specified (even "default" must be written out)

## Grades

| Input | Draft | Final |
|-------|-------|-------|
| 01 — direct invocation | 86 (A) | 91 (A+) |
| 02 — partial context (Portuguese) | 90 (A+) | 92 (A+) |
| 03 — full context (Portuguese) | 97 (A+) | 97 (A+) |
| **Average** | **91** | **93.3** |

## Iterations

**1 iteration.** Highest-leverage fix: added a deterministic discovery message template to Step 1 (Portuguese by default, English fallback). Template previews the 7 final sections, making the discovery phase informative even before any answers are given. Secondary fix: strengthened Question 3 to explicitly ask "what Lovable should NEVER add" — surfaces DO NOT constraints at discovery time.

## What moved the score

- Format consistency: 18 → 20 (deterministic template)
- Prompt completeness: 16 → 18 (7-section preview in discovery message)
- Scope containment: 16 → 17–18 (explicit DO NOT question in discovery)

## Structural ceiling

Input 01 (no-context invocation) has a principled-decline ceiling on specificity (~16/20). Accepted per creation patterns. Final score 91 (A+) is above threshold.

## Files

```
outputs/create-skill-runs/lovable-prompt-2026-06-28/
├── summary.md
├── rubric.md
├── draft-v0.md
├── final-skill.md
├── inputs/01.md, 02.md, 03.md
├── outputs-draft/01.md, 02.md, 03.md
├── outputs-final/01.md, 02.md, 03.md
├── grades-draft.md
├── grades-final.md
├── iterations/iter-1-skill.md
└── iterations.md
```
