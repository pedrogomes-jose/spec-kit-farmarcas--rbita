# Notas — SKILL.md MELHORADA (2026-10-19, iteração 1)

## Input 01 — `/orbita-user-stories` (invocação direta)

| Critério | Nota | Evidência |
|---|---|---|
| Routing quality | 18 | Description agora cobre transcrição, "atualiza o card SQO-xxxx" e o board SQO inteiro. |
| Output specificity | 17 | Teto da faixa de declínio: nomeia o que falta e **pergunta de qual produto é o card**, porque isso muda o Step 3 inteiro. |
| Output format consistency | 19 | Texto literal do Caso B + 3 pedidos de informação + ressalva de cobertura. Reproduzível. |
| Implementabilidade júnior | 17 | Teto da faixa de declínio: o usuário sabe exatamente o que trazer. |
| Honestidade | 19 | Declarou os diretórios inexistentes e declarou a decisão de produto como **indeterminada** em vez de chutar. |
| **Total** | **90** | **A+** (no teto da faixa de declínio — ver âncora da rubrica) |

Baseline: 84 → **+6**

## Input 02 — "Cria os cards do Órbita..." (frase-gatilho)

| Critério | Nota | Evidência |
|---|---|---|
| Routing quality | 18 | Frase-gatilho literal. |
| Output specificity | 20 | `scoring.ts`, `classifyEconomicClass`, `VIABILITY_TIERS`, `RECOMMENDED_SCORE_PERCENT`, `radiusSearch/types.ts` — todos reais e grepados na sessão. |
| Output format consistency | 20 | 8 seções, Forma A declarada explicitamente, `[DEFAULT]` em estimativa e prioridade. |
| Implementabilidade júnior | 19 | Regras numeradas com "o porquê"; **dois** itens "O QUE NÃO MUDA"; e a armadilha que mais pegaria júnior documentada: `economicClass` vale 0, 1, 3 ou 5 — não é escala contínua, então barra de progresso "x de 5" mostra valor que o código nunca produz. |
| Honestidade | 20 | "Não foi localizado NESTES 3 REPOSITÓRIOS", ressalva do 4º repo, e a inversão de direção de densidade/renda registrada para não se perder entre cards. |
| **Total** | **97** | **A+** |

Baseline: 87 → **+10**

## Input 03 — transcrição, board SQO fora do produto Órbita (adjacente)

| Critério | Nota | Evidência |
|---|---|---|
| Routing quality | 18 | **Continuou na skill** em vez de rotear para `/user-stories`. Era 8. |
| Output specificity | 17 | Sem pista de código — correto, o produto está fora dos repos. Especificidade vem da fonte: trechos literais com timestamp (00:11:31, 00:12:39, 00:16:20, 00:55:05). |
| Output format consistency | 20 | 8 seções completas nos 2 cards; Forma B justificada. Era 6 (zero cards). |
| Implementabilidade júnior | 18 | Define "status" vs "flag" em uma frase; 7 regras numeradas, duas delas "O QUE NÃO MUDA". Desconto: nenhum ponteiro de código, inerente ao produto estar fora de alcance. |
| Honestidade | 20 | Leitura parcial declarada dentro do card; migração marcada como **bloqueante de deploy**; contradição "legal vs. financeira" citada literalmente. |
| **Total** | **93** | **A+** |

Baseline: 54 → **+39**

## Input 04 — fora de escopo (teste binário de fronteira)

**PASS — 20/20.** Recusou escrever o PRD e roteou para `/claude-system-builder`,
mesmo após a reescrita do `Out of Scope`. Sem regressão. Por ser teste binário de
fronteira, não entra na média /100.

---

## Resultado

| Input | Baseline | Melhorada | Δ |
|---|---|---|---|
| 01 declínio | 84 | 90 | +6 |
| 02 frase-gatilho | 87 | 97 | +10 |
| 03 adjacente/transcrição | 54 | 93 | **+39** |
| 04 fronteira | PASS | PASS | — |
| **Média (01-03)** | **75,0** | **93,3** | **+18,3** |

**Todos os inputs pontuados em A+ (90+). Loop encerrado na iteração 1.**

Critério que mais subiu: **Implementabilidade por júnior** (média 11,7 → 18,0),
puxado pelo input 03, que saiu de 4.
