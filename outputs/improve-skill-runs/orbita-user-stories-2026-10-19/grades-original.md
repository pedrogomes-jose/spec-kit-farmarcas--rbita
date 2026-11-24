# Notas — SKILL.md ORIGINAL (2026-10-19)

## Input 01 — `/orbita-user-stories` (invocação direta, sem args)

| Critério | Nota | Evidência |
|---|---|---|
| Routing quality | 16 | Disparou corretamente; description tem 3+ gatilhos e boundary com ponteiro. Perde por não cobrir transcrição como fonte nem "atualizar card existente". |
| Output specificity | 16 | Declínio com princípio (âncora da rubrica): nomeou exatamente o que falta e ofereceu 2 caminhos. Listou os 3 diretórios do Step 0 que não existem. |
| Output format consistency | 18 | Usou o texto literal do Step 1 Caso B. |
| Implementabilidade júnior | 16 | Sem card, mas o declínio diz o que o usuário precisa trazer. |
| Honestidade | 18 | Declarou o que não pôde executar e que `learnings.md` mudou no disco durante o run. |
| **Total** | **84** | **A** |

## Input 02 — "Cria os cards do Órbita pra essa melhoria..." (frase-gatilho)

| Critério | Nota | Evidência |
|---|---|---|
| Routing quality | 18 | Frase-gatilho literal da description. |
| Output specificity | 20 | `arquivo:linha` em toda pista: `scoring.ts:94-99`, `index.ts:40-49`, `analysis.routes.ts:7`, `economicClass.ts:7-35`. Usou os 3 níveis de confirmação do Step 3. |
| Output format consistency | 18 | 7 seções na ordem. Perde porque as ambiguidades reais ficaram no Step 3 do relatório, fora do card — quem lê só o card no Jira não as vê. |
| Implementabilidade júnior | 15 | Define "dimensão" vs "camada", dá o porquê, diz o que não entra. Perde por: regras em bullet não numerado, "o que NÃO muda" só dentro de Escopo, nenhuma alternativa descartada registrada. |
| Honestidade | 16 | Excelente qualificação de ausência ("apenas nestes 3 repositórios", aviso do 4º repo). Perde por não ter seção própria de pontos em aberto nem efeito de segunda ordem. |
| **Total** | **87** | **A** |

## Input 03 — transcrição de reunião, board SQO mas fora do produto Órbita (adjacente)

| Critério | Nota | Evidência |
|---|---|---|
| Routing quality | 8 | A description roteia este caso para FORA (`/user-stories`), que entrega formato errado para o board SQO. O caso real do SQO-1323 não tem skill. |
| Output specificity | 16 | Greps reais comprovando a parada: 0 ocorrências de `bloquead/blocked` nos 3 repos; `navigation.component.ts:81`, `dashboard.component.ts:28`, `environment.ts:34`. |
| Output format consistency | 6 | **Zero cards produzidos.** Para um pedido de card, a forma entregue foi um documento de decisão. |
| Implementabilidade júnior | 4 | O júnior não recebe nada acionável sobre o trabalho pedido. |
| Honestidade | 20 | Recusou-se a fabricar "Caminho/rota", citou o precedente do SQO-1279, expôs a lacuna da própria skill e pediu decisão em vez de escolher sozinho. |
| **Total** | **54** | **C** |

## Input 04 — "Escreve o PRD completo..." (fora de escopo, teste de fronteira)

| Critério | Nota | Evidência |
|---|---|---|
| Routing quality | 20 | Fronteira negativa segurou; roteou para `/claude-system-builder`. |
| Output specificity | 16 | Citou a linha do Out of Scope que decidiu. |
| Output format consistency | 18 | Recusa limpa, sem card parcial. |
| Implementabilidade júnior | 16 | N/A — rota correta. |
| Honestidade | 18 | Não produziu PRD parcial para "ajudar". |
| **Total** | **88** | **A** |

---

## Diagnóstico

**Média: 78,25/100 (B).** Faixa: 54 a 88.

**Critério mais baixo no conjunto: Implementabilidade por júnior** (4 / 15 / 16 / 16).

**Input mais baixo: 03 (54, C)** — e é exatamente o cenário do SQO-1323 que o
usuário aprovou. A skill original **não consegue produzir aquele card**.

**Seção da SKILL.md que causa a nota baixa:** `Out of Scope` + `Cross-Skill
Routing`, que definem o escopo pelo *produto/código* e empurram para fora toda
feature do board SQO que não seja do produto Órbita — sem que a skill de destino
(`/user-stories`) saiba emitir o template do board. É um buraco de roteamento,
não um defeito de redação.

**Segundo alvo:** regras de negócio em parágrafo/bullet corrido e ausência de uma
seção de pontos em aberto dentro do card (derruba júnior e honestidade nos
inputs 02 e 03).
