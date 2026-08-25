# Iterations Log — product-discovery

## Iteration 1

**Inputs abaixo de 90:** 01 (85) e 02 (89)

**Root cause comum:** sem template de abertura determinístico e sem instrução de contexto parcial → format consistency 17-18 (não 20) e discovery depth 16 (não 18).

**Fix #1 (template + contexto parcial):** Adicionado à Fase A.
- Input 01: format 17→20 (+3), discovery depth 16→18 (+2) → 85→90
- Input 02: format 18→19 (+1), specificity 17→18 (+1), discovery depth 16→17 (+1) → 89→92

**Fix #2 (Miro integration):** Requisito inserido pelo usuário durante o eval. Fase D reescrita com D1–D7 (ToolSearch + context_get + board_create + table_create + diagram_create + doc_create + fallback). Impacto: exit checklist mais específico e verificável.

**Sem regressões.** Input 03 permanece 97.

## Stop condition
Todos os inputs ≥ 90 após 1 iteração. Shipped.
