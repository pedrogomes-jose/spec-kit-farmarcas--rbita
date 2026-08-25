# Summary — software-improvement — 2026-06-30

## What was built

New skill: `software-improvement`
Path: C:\Users\zequi\.claude\skills\software-improvement\SKILL.md

One-line job: Analisa um PRD de melhoria em projetos existentes, investiga o código atual, levanta dúvidas categorizadas (regras de negócio, UX, técnicas) e implementa somente após as dúvidas serem respondidas.

Domain: Code authoring / multi-step (Fase 1: investigar + perguntar → Fase 2: implementar)

## Grades

| Input | Type | Score | Grade |
|-------|------|-------|-------|
| 01 | Direct invocation / principled-decline | 91/100 | A+ |
| 02 | Trigger phrase + PRD completo (SM-2 flashcards) | 100/100 | A+ |
| 03 | Adjacent natural language (export PDF) | 99/100 | A+ |
| **Average** | | **96.7/100** | **A+** |

## Iterations

0 — A+ no primeiro draft. Stop condition met immediately.

## What moved the score in v0

The key design decisions that produced A+ without iteration:

1. **Two-phase structure with hard gate** — Fase 1 (perguntas) and Fase 2 (implementação) separated by Step 3 (explicit STOP). Anti-rationalization table explicitly blocks "implementar antes das respostas" and "perguntar e implementar em paralelo".

2. **Three-category question structure** — Regras de Negócio / UX-Usabilidade / Técnicas gives users a clear mental model for answering, and forces the skill to investigate all angles.

3. **Step 0 table with specific file paths** — Agents read actual project files (schema, routes, components, wrangler.toml) before generating questions, enabling Input 03 to produce specific questions about pdfjs-dist, is_hidden_* fields, and Cloudflare Workers canvas restrictions.

4. **Principled-decline with preview** — No-PRD case shows a structured decline that previews all 4 steps the skill will take once PRD arrives. Moved Input 01 from ~86 (generic decline) to 91 (informative decline with routing value).

5. **Worked example shows full two-phase pipeline** — Input 01 (Phase 1 only) scores to principled-decline ceiling; the worked example makes Phase 2 rubric-visible.

## Structural ceilings

Input 01 at 91 is the principled-decline ceiling. Without PRD, Phase 1 specificity cannot exceed 17-18/20. Not a skill defect — document and stop.

## Files in this run

- draft-v0.md — snapshot of initial SKILL.md
- final-skill.md — identical to draft-v0 (no iteration needed)
- rubric.md — 5 criteria with 0-20 anchors
- inputs/01.md, 02.md, 03.md — test inputs
- outputs-draft/01.md, 02.md, 03.md — agent outputs
- grades-draft.md = grades-final.md — all A+
