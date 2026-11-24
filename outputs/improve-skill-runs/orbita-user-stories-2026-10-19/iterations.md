# Log de iterações — orbita-user-stories (2026-10-19)

## Iteração 1 — a única necessária

**Diagnóstico da baseline:** média 75,0 (B). O input 03 (54, C) era o gargalo, e
era exatamente o cenário do card SQO-1323 que o usuário aprovou nesta sessão.
Causa raiz: `Out of Scope` + `Cross-Skill Routing` definiam o escopo da skill
pelo *produto/código*, não pelo *board*, empurrando toda feature não-Órbita para
`/user-stories` — que não sabe emitir o template do board SQO. Buraco de
roteamento, não defeito de redação.

**Edições aplicadas (21 no total, em 3 lotes):**

| # | Mudança | Critério alvo |
|---|---|---|
| 1 | `description` cobre board SQO inteiro, transcrição como fonte e "atualiza card SQO-xxxx" | Routing |
| 2-4 | Escopo por board, não por produto: Step 0 decide produto primeiro; Step 3 condicional; "Não aplicável — fora dos repositórios do Órbita" | Routing, Formato, Júnior |
| 5 | 8ª seção obrigatória "Pontos em aberto" com trecho literal, ou "Nenhum" | Honestidade |
| 6 | Contexto com tríade (atual / por que errado / impacto) + alternativas descartadas | Júnior |
| 7 | Regras numeradas e atômicas, com item obrigatório "o que NÃO muda" | Júnior |
| 8 | Step 3B — 4 perguntas de efeito de segunda ordem, sem ampliar escopo | Honestidade |
| 9 | Conflito do Gherkin resolvido: Forma A (Gherkin + fixos) vs. Forma B (só fixos com regras verificáveis) | Formato |
| 10 | Transcrição como fonte primária + leitura em 100% com porção declarada | Especificidade |
| 11 | Rastreabilidade com localizador (timestamps, seção) | Especificidade |
| 12 | Step 6B — atualizar card existente + guarda contra campo herdado de template | Honestidade |
| 13 | Afirmação de ausência qualificada como "nestes 3 repositórios" | Honestidade |
| 14 | P2 do audit: `outputs/prds/`, `claude-system-builder-runs/` marcados "(se existir)" — não existem no repo | Especificidade |
| 15 | 6 linhas novas na tabela de anti-racionalização | Júnior |
| 16 | 11 itens novos no checklist de saída | Formato |
| 17 | Worked Example 2 compacto, baseado no SQO-1323 | Formato, Júnior |

**Resultado:** 01: 84→90, 02: 87→97, 03: 54→93, 04: PASS→PASS.
Todos A+ na primeira iteração. **Nenhuma iteração 2 foi necessária.**

**O que não foi alterado e por quê:**
- A fronteira negativa do `Out of Scope` para PRD/discovery/validação: já estava
  em 20/20 no baseline (input 04). Mexer só criaria risco de regressão — e o
  re-run confirmou que não regrediu.
- Worked Example 1 (breakdown de score): mantido inteiro. O corpo ficou em 599
  linhas, mas 146 delas são worked examples — o Tip 8 explicitamente não se
  aplica a esse conteúdo ("rich worked examples NOT a Tip-8 failure"). O corpo
  de regras/processo ficou em ~453 linhas, dentro da diretriz.
