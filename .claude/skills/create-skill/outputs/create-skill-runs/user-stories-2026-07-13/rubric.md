# Rubric — user-stories

5 criteria, 0–20 each, /100 total. A+ = 90+.

## 1. Routing quality (0–20)
- 18–20: Description 100+ chars, WHAT+WHEN within first 250 chars, 5+ user-typed trigger phrases (PT + EN), third person, "Do NOT use for X → use /Y" boundary present and verified against real sibling skills.
- 12–17: Most present but boundary missing a pointer, or trigger phrases under 5, or WHEN clause starts after char 250.
- 6–11: Description present but short (<100 chars) or first person or no boundary.
- 0–5: No frontmatter, or name/folder mismatch.

## 2. Output specificity (0–20)
- 18–20: Stories reference real PRD/spec text verbatim or cite the exact conversational source; no invented requirements. For principled-decline (no PRD, no description given): 14–18 if the skill correctly stops and names what's missing with the decline template.
- 10–17: Stories are plausible but generic, loosely tied to input.
- 0–9: Stories invented from training data with no traceability, or skill fabricates a PRD that was never given.

## 3. Output format consistency (0–20)
- 18–20: Every story follows the exact template (title, As a/I want/So that, Gherkin AC ≥2, rastreabilidade, estimativa, prioridade, dependências) plus the Tabela Resumo at the end.
- 10–17: Template mostly followed but missing 1–2 fields consistently (e.g., no dependency field, no summary table).
- 0–9: Free-form list, no Gherkin, no consistent shape across stories.

## 4. Acceptance-criteria completeness & INVEST compliance (domain primary, 0–20)
- 18–20: Every story has ≥2 Gherkin criteria covering happy path + edge case; stories are appropriately sized (INVEST "Small"/"Testable"); large features are split into multiple stories, not one mega-story.
- 10–17: Gherkin present but shallow (only happy path, no edge case) or one story tries to cover too much.
- 0–9: No Gherkin format, or acceptance criteria are vague bullets ("should work correctly").

## 5. Traceability & default-marker discipline (domain secondary, 0–20)
- 18–20: Every story cites its source (PRD section/conversation quote, or "descrito verbalmente"); every unconfirmed estimate carries `[DEFAULT: X — confirmar com o time]`; contradictions in source material are flagged explicitly, not silently resolved.
- 10–17: Traceability present but inconsistent (some stories missing source citation), or estimates given without DEFAULT marker.
- 0–9: No traceability at all, or estimates presented as confirmed facts with no marker.

## Principled-decline anchor
When the test input supplies no PRD/spec and no feature description, the correct output is Step 1 Caso B (stop, explain what's missing, preview what the skill will produce once given input). Score 14–18 on specificity and format (not 4) if the decline template is followed exactly. Score domain criteria 4–5 based on whether the preview of Gherkin/traceability/DEFAULT-marker behavior is accurately described.
