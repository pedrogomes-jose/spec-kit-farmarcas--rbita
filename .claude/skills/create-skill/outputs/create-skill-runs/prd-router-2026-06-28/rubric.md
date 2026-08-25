# Rubric — prd-router

Domain: Decision (PRD routing — Lovable vs Software)

## Criteria

| # | Criterion | 0 | 10 | 20 |
|---|-----------|---|----|----|
| C1 | **Routing quality** | No frontmatter / <50 chars / no triggers | Frontmatter present, some triggers, partial WHAT+WHEN | 100+ chars, 5+ PT+EN triggers, WHAT+WHEN in first 250, "Do NOT use for" with /pointers, third person |
| C2 | **Output specificity** | Generic output with no PRD evidence / fabricated facts | Partial evidence (some criteria cited, others inferred) | All 5 classification criteria cite specific PRD text OR principled-decline path shows full pipeline preview (14–18 for no-PRD) |
| C3 | **Format consistency** | No classification table / no proposal structure | Table present but missing sections (argumento contrário OR kill criteria OR confirmation question) | All elements present in correct order: classification table → destino + porquê → argumento contrário → kill criteria → confirmation question |
| C4 | **Routing opinion quality** | "Both paths are possible" — no clear recommendation | Recommendation present but weak (no specific PRD evidence, or evidence inferred not quoted) | Recommendation names specific path, backed by 5-criteria table with cited PRD evidence, not paraphrased |
| C5 | **Kill criteria + alternative honesty** | No kill criteria / strawman alternative ("the other option is also fine") | Kill criteria listed but alternative argument is weak or generic | Names strongest real argument for the other path (citing PRD evidence where applicable) + 3 specific conditions that would change decision |

## Principled-decline anchor

Input 01 (no PRD) → correct output = decline template showing full 5-step pipeline.
Score C2 at 14–16 (pipeline preview visible), C4 at 14–16 (correct behavior), C5 at 14–16.
Do NOT penalize at 4/20 for not producing a classification when no PRD exists.

## Test inputs

- Input 01: `/prd-router` with no PRD — tests principled-decline path
- Input 02: "analisa esse PRD e me diz para onde vai" + simple app PRD (Lovable case) — tests trigger phrase + Lovable classification
- Input 03: "preciso saber se esse produto vai para o Lovable ou para o Claude Code" + complex PRD with workers/queues — tests adjacent natural language + Software classification
