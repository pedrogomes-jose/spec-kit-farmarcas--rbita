# Iteration log — user-stories

## Iteration 0 (draft v0)
Average across inputs 01–03: 92.7/100 (91/93/94, all A+). Input 04 (out-of-scope) PASS at 94/100.

Lowest-scoring single criterion: Output format consistency on Input 02 (13/20). Root cause: when the skill saves stories to markdown (no Linear/Jira MCP), the draft's Step 4 said to save the file and show a summary table, but never explicitly required the full story text to also appear in the chat response. The agent running Input 02 produced a summary + file pointer instead of inline story text — inconsistent with Input 03's behavior (which did show full inline text) and with the SKILL.md's own Worked Example (which shows full inline stories). Verified the underlying saved file was actually excellent (read it directly) — the defect was purely in what reached the user in the response, not in the generation logic itself.

## Iteration 1
Fix applied — three additions to SKILL.md:
1. `## Critical` rule: "Sempre incluir o texto completo de todas as histórias... diretamente na resposta ao usuário. Salvar em markdown ou criar tickets... é adicional — nunca substitui mostrar o conteúdo completo na resposta."
2. Anti-rationalization table row naming the exact shortcut: "Já vou salvar em markdown ou criar os tickets, então posso só resumir na resposta ao usuário."
3. Exit checklist item: "O texto completo de todas as histórias apareceu na resposta ao usuário — não apenas um resumo apontando para o arquivo salvo."

Re-ran Input 02 only (the sole failing criterion). Result: format consistency 13→20, traceability/default discipline 20→20 (with a bonus improvement — Prioridade now also gets `[DEFAULT]` marker, applying the Critical rule more strictly than draft). Input 02 total: 93→100.

Inputs 01, 03, 04 were not re-run — they were already A+ on the draft and the fix does not touch their code paths (01 and 04 never reach story generation; 03 already showed full inline content).

## Final average (inputs 01–03)
(91 + 100 + 94) / 3 = **95.0/100 — all A+**

## Stop condition
All inputs ≥ 90 after iteration 1. Shipped.

## Structural ceilings noted (not iterated against)
- Input 01 (direct invocation, no context): specificity/format capped ~17-18/20 per the principled-decline anchor — correct behavior, not a defect.
- Live MCP connectivity (Linear/Jira) could not be verified beyond confirming `ToolSearch` returns no matching tools in this environment — this is a methodology gap for MCP-dependent skills evaluated offline, consistent with prior runs (arize-evaluator, salary-research).
