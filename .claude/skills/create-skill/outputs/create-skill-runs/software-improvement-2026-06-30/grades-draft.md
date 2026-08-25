# Grades — Draft v0 — software-improvement — 2026-06-30

## Input 01 — Direct invocation / principled-decline

| Criterion | Score (/20) | Evidence |
|-----------|-------------|----------|
| Routing quality | 18 | Skill disparou corretamente; decline estruturado e informativo com preview de 4 próximos passos. -2 por ser principled-decline ceiling (nenhum trigger phrase para confirmar roteamento em NL) |
| Output specificity | 17 | Decline lista 6 itens concretos do PRD + 4 passos futuros. Não há PRD para ser específico — correto parar. Principled-decline anchor: 14-18 |
| Output format consistency | 20 | Template do decline do Step 0 seguido exatamente |
| Clarification completeness | 16 | Sem PRD, não há como gerar perguntas — comportamento correto. Principled-decline anchor: 14-18 |
| Implementation gate enforcement | 20 | Zero código escrito. Aguarda PRD antes de qualquer ação. |
| **Total** | **91/100** | **A+** |

## Input 02 — Trigger phrase + PRD completo (SM-2)

| Criterion | Score (/20) | Evidence |
|-----------|-------------|----------|
| Routing quality | 20 | Disparou em "Tenho um PRD de melhoria" — trigger phrase exata |
| Output specificity | 20 | Referencia 7 arquivos reais do projeto; menciona StudySessionPage, FlashcardsPage, ease_factor, next_review_at, D1 SQLite restrições de migration, padrão SM-2 em contexto de código existente |
| Output format consistency | 20 | Template Fase 1 seguido: título, 3 categorias, numeração contínua, "Assim que você responder, implemento na ordem X" |
| Clarification completeness | 20 | 9 perguntas em 3 categorias; cada uma com contexto ("o PRD diz X mas o código atual faz Y"); cobre edge cases não mencionados no PRD (cards legados, batch vs card-a-card, ALTER TABLE safety) |
| Implementation gate enforcement | 20 | Nenhuma linha de código escrita na Fase 1; anuncia a ordem de implementação mas não implementa |
| **Total** | **100/100** | **A+** |

## Input 03 — Adjacent natural language (sem trigger phrase verbatim)

| Criterion | Score (/20) | Evidence |
|-----------|-------------|----------|
| Routing quality | 20 | Disparou em "Quero adicionar uma funcionalidade" sem trigger phrase explícita — latent surface funcionou |
| Output specificity | 20 | Leu 7 arquivos reais; identificou pdfjs-dist já instalado (mas para leitura), restrições de canvas no Cloudflare Workers, is_hidden_* fields, padrão BookmarkPlus existente — todos referenciados no output |
| Output format consistency | 20 | Template Fase 1 seguido exatamente, 3 categorias, 7 perguntas numeradas |
| Clarification completeness | 19 | Todas as 3 categorias cobertas com perguntas contextualizadas. -1 pois Q5 (feedback visual) poderia ter sido resolvida por padrão do projeto (Loader2 já usado em botão similar) |
| Implementation gate enforcement | 20 | Zero código escrito; fim da Fase 1 explícito |
| **Total** | **99/100** | **A+** |

## Summary

| Input | Score | Grade |
|-------|-------|-------|
| 01 — principled-decline | 91/100 | A+ |
| 02 — trigger phrase + PRD | 100/100 | A+ |
| 03 — natural language | 99/100 | A+ |
| **Average** | **96.7/100** | **A+** |

**All inputs ≥ 90. Stop condition met: ship.**
No iteration needed.
