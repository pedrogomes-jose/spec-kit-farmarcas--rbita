# Summary — product-discovery

**Date:** 2026-06-28
**Skill:** C:\Users\zequi\.claude\skills\product-discovery\SKILL.md
**Status:** SHIPPED — A+ verified

## O que foi construído

Skill de discovery de produto conversacional com 4 fases progressivas (Ancoragem → CSD → Oportunidades → Output no Miro). Embutida com conhecimento dos frameworks:
- **Matriz CSD** (Livework): Certezas/Suposições/Dúvidas com regras de separação
- **Árvore de Oportunidades** (Teresa Torres): Outcome → Espaços → Sub-oportunidades, sem soluções

Inputs são variáveis — a skill detecta o que já foi respondido e pergunta apenas as lacunas. Output vai para Miro via table_create (CSD) + diagram_create (Árvore) + doc_create (próximos passos). Fallback em texto se Miro indisponível.

## Grades

| Input | Draft | Final |
|-------|-------|-------|
| 01 — direto, sem contexto | 85 (A) | 90 (A+) |
| 02 — churn parcial | 89 (A) | 92 (A+) |
| 03 — contexto rico | 97 (A+) | 97 (A+) |
| **Avg** | 90.3 | **93 (A+)** |

## Iterações: 1

**Fix de maior impacto:** Template de abertura determinístico (Fase A) + instrução de contexto parcial ("Aqui está o que já entendi") — moveu format consistency de 17→20 e discovery depth de 16→18 no Input 01.

**Fix requisitado no meio do eval:** Integração Miro completa na Fase D (requisito do usuário entregue durante a iteração). Sem impacto negativo no score — só melhorou o exit checklist.

## Teto estrutural

Input 01 specificity (16) e framework accuracy (16) são teto de principled-decline: sem contexto, a skill não pode ser específica sobre o produto. Correto — não iterar.
