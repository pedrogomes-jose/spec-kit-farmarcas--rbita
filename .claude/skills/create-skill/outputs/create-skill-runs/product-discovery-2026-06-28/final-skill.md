---
name: product-discovery
description: Guia um processo conversacional de discovery de produto, fazendo perguntas progressivas por fase até construir uma Matriz CSD (Certezas, Suposições, Dúvidas) e uma Árvore de Oportunidades estruturadas a partir do contexto real fornecido. Use quando o usuário disser 'vamos fazer um discovery', 'quero entender esse problema', 'me ajuda com a árvore de oportunidades', 'fazer uma CSD', 'discovery de produto', 'mapear dores dos usuários', 'explorar oportunidades', 'entender as oportunidades do produto', 'investigar esse problema', ou apresentar qualquer dor, métrica, hipótese ou problema de produto para investigar. Do NOT use para escrever PRDs → faça em conversa; do NOT use para criar prompts de Lovable → use /lovable-prompt; do NOT use para criar sistemas → use /claude-system-builder; do NOT use para planejar roteiros de pesquisa com usuários → trate em conversa separada.
---

# product-discovery

Conduz um discovery de produto estruturado por quatro fases — Ancoragem, CSD, Mapeamento de Oportunidades, Saída — fazendo perguntas progressivas a cada turno até que a Matriz CSD e a Árvore de Oportunidades estejam populadas com o contexto real do produto. O output é sempre derivado das respostas do usuário, nunca de suposições genéricas.

## Critical

- **Nunca pule para soluções.** A Árvore de Oportunidades mapeia dores, desejos e contextos de usuários — não features, não wireframes, não ideias de produto. Soluções são exploradas DEPOIS do discovery.
- **Frameworks derivados do contexto real.** Nenhum item na CSD ou na Árvore pode ser inventado. Se não veio do usuário, marque como `[SUPOR: confirmar]`.
- **Perguntas progressivas, não em bloco.** Faça 1–3 perguntas por turno, construindo sobre a resposta anterior. Não entregue um formulário de 10 perguntas.
- **Mostre o estado atual dos frameworks.** Após cada fase completada, exiba a CSD e/ou Árvore no estado parcial para que o usuário veja o progresso e corrija antes de avançar.
- **A CSD é viva.** Items podem migrar entre colunas conforme a conversa avança. Dúvidas viram certezas. Suposições são confirmadas ou descartadas.
- **Convergência explícita por fase.** Avance de fase só quando os critérios de convergência da fase atual estiverem satisfeitos.
- **Output final sempre vai para o Miro.** Na Fase D, crie a CSD como tabela e a Árvore como diagrama no Miro. Se o Miro MCP não estiver disponível, entregue o output em texto na conversa e avise o usuário.

## Frameworks Referência (embutido)

### Matriz CSD (Livework)
| ✅ Certezas | ❓ Suposições | 🔍 Dúvidas |
|-------------|--------------|------------|
| O que sabemos com evidência (dados, pesquisa, citações diretas de usuários) | O que ACHAMOS que é verdade — hipóteses e crenças da equipe sem validação formal | O que não sabemos e precisamos descobrir — perguntas abertas críticas |

**Regra de separação:** Uma certeza requer evidência citável (dado, estudo, N usuários disseram). Uma suposição é "acreditamos que...". Uma dúvida é "precisamos descobrir se...".

### Árvore de Oportunidades (Teresa Torres)
```
🎯 Outcome desejado (raiz) — métrica ou comportamento de usuário mensurável
│
├── 📌 Espaço de oportunidade 1 — cluster de dores/desejos relacionados
│   ├── Sub-oportunidade 1.1 — dor ou desejo específico de usuário
│   └── Sub-oportunidade 1.2 — dor ou desejo específico de usuário
│
├── 📌 Espaço de oportunidade 2
│   └── Sub-oportunidade 2.1
│
└── 📌 Espaço de oportunidade 3
    └── Sub-oportunidade 3.1
```

**Regras da Árvore:**
- O outcome é o que O NEGÓCIO precisa (métrica, OKR), não uma feature.
- Oportunidades são problemas ou desejos dos USUÁRIOS — não soluções.
- Sub-oportunidades são dores mais específicas dentro de um espaço de oportunidade.
- Nunca colocar soluções ou features na árvore — elas ficam em um passo posterior.

## Step 0: Leia Antes de Responder

| Fonte | Onde | O que extrair |
|-------|------|---------------|
| Contexto inicial do usuário | conversa | Outcome candidato, usuários mencionados, dados citados, dores relatadas |
| Respostas anteriores | conversa | Items já confirmados para CSD e Árvore |
| Contexto Miro atual | `mcp__claude_ai_Miro__context_get` | Board ativo — usar se existir; criar novo se não existir |
| Aprendizados passados | references/learnings.md | Padrões e erros anteriores a evitar |

Se `references/learnings.md` não existir, prossiga sem ele.

**Verificação Miro (somente na Fase D):** Antes de criar artefatos no Miro, use ToolSearch com `"select:mcp__claude_ai_Miro__context_get,mcp__claude_ai_Miro__board_create,mcp__claude_ai_Miro__table_create,mcp__claude_ai_Miro__diagram_create"` para carregar os schemas. Se qualquer chamada Miro falhar por ausência de MCP, entregue o output em texto na conversa.

Ao receber o input inicial, identifique imediatamente quais fases já estão parcialmente respondidas pelo contexto fornecido. Não pergunte o que já foi dado.

## Fase A: Ancoragem

**Objetivo:** Definir o outcome desejado e o(s) usuário(s) alvo.

**Convergência da Fase A:** Outcome articulado como métrica ou comportamento mensurável + persona de usuário nomeada.

**Quando invocado sem contexto,** use esta abertura determinística:

> Vamos montar o discovery juntos. O processo tem 4 fases:
>
> **Fase A** — Ancoragem (outcome + usuários) → **Fase B** — Matriz CSD (o que sabemos, achamos e não sabemos) → **Fase C** — Árvore de Oportunidades (dores e desejos dos usuários) → **Fase D** — Output final com os dois frameworks estruturados.
>
> Para começar:
>
> 1. **Outcome:** Qual é o resultado de negócio que queremos mover? (ex: aumentar ativação de X% para Y%, reduzir churn de 12 para 20 dias de trial, aumentar NPS de 32 para 50)
> 2. **Usuários:** Quem são os usuários afetados por esse problema? (ex: gestores, usuários novos no trial, admins, freelancers)

**Quando contexto parcial for fornecido,** abra reconhecendo o que já foi dado antes de perguntar:

> Aqui está o que já entendi do contexto:
> - [listar o que foi extraído do input inicial]
>
> Para avançar, preciso completar:
> - [perguntas apenas sobre o que ainda falta]

Se o contexto inicial já responde A1 e A2, vá direto para a Fase B sem perguntar.

**Ao concluir a Fase A:** Confirme com o usuário antes de avançar:
> "Entendido. Vou trabalhar com:
> - **Outcome:** [X]
> - **Usuários:** [Y]
> Podemos avançar para mapear o que sabemos, achamos e não sabemos sobre esse problema?"

## Fase B: Construção da CSD

**Objetivo:** Popular as três colunas da Matriz CSD com o contexto real do produto.

**Convergência da Fase B:** CSD com ≥ 3 itens em cada coluna, todos derivados do usuário ou marcados como `[SUPOR: confirmar]`.

Faça 1–3 perguntas por turno, na ordem abaixo. Avance para a próxima coluna assim que a atual tiver ≥ 3 itens.

**Certezas:**
- O que você sabe com certeza sobre esse problema? (dados de analytics, pesquisa com usuários, suporte/CS, métricas)
- Alguma citação direta de usuários que confirme esse problema?
- Que comportamentos você já mediu que são fatos?

**Suposições:**
- O que o time acredita ser verdade mas nunca validou formalmente?
- Que hipóteses guiam as decisões hoje?
- Se você fosse fazer uma aposta, qual seria?

**Dúvidas:**
- O que você mais precisa descobrir antes de agir?
- O que te impede de ter certeza?
- Que pergunta, se respondida, mudaria completamente a direção?

**Após cada bloco de respostas,** exiba a CSD no estado atual:

```
📊 Matriz CSD — estado atual

| ✅ Certezas | ❓ Suposições | 🔍 Dúvidas |
|-------------|--------------|------------|
| [itens]     | [itens]      | [itens]    |
```

## Fase C: Mapeamento de Oportunidades

**Objetivo:** Estruturar os espaços de oportunidade e sub-oportunidades da Árvore a partir das dores e desejos reais dos usuários.

**Convergência da Fase C:** ≥ 3 espaços de oportunidade, cada um com ≥ 1 sub-oportunidade, todos derivados de dores/desejos dos usuários (não de soluções).

Pergunte 1–2 questões por turno:

- Que dores os usuários expressaram diretamente? (citações, tickets de suporte, entrevistas)
- Em que momentos da jornada a dor acontece? (onboarding, uso recorrente, momento de conversão)
- Diferentes segmentos de usuários têm dores diferentes? Como elas se agrupam?
- O que os usuários tentaram fazer e não conseguiram? O que eles desejam mas ainda não existe?
- Há padrões nos churn interviews, NPS detractors, ou tickets de CS?

**Após cada bloco,** exiba a Árvore no estado atual:

```
🌳 Árvore de Oportunidades — estado atual

🎯 Outcome: [X]

📌 [Espaço 1]
  └── [Sub-oportunidade]

📌 [Espaço 2]
  └── [Sub-oportunidade]
```

## Fase D: Output Final no Miro

Quando a Fase C convergir, execute nesta ordem:

### D1 — Carregar ferramentas Miro

Use ToolSearch com `"select:mcp__claude_ai_Miro__context_get,mcp__claude_ai_Miro__board_create,mcp__claude_ai_Miro__table_create,mcp__claude_ai_Miro__diagram_create"`.

### D2 — Verificar ou criar board

1. Chame `mcp__claude_ai_Miro__context_get` para verificar se há board ativo.
2. Se houver board ativo: use-o.
3. Se não houver: chame `mcp__claude_ai_Miro__board_create` com nome `"Product Discovery — [produto/problema] — [data]"`.

### D3 — Criar Matriz CSD como tabela no Miro

Chame `mcp__claude_ai_Miro__table_create` com:
- Título: `📊 Matriz CSD — [produto/problema]`
- 3 colunas: `✅ Certezas`, `❓ Suposições`, `🔍 Dúvidas`
- Linhas: uma por item descoberto na Fase B

### D4 — Criar Árvore de Oportunidades como diagrama no Miro

Chame `mcp__claude_ai_Miro__diagram_create` representando:
- Nó raiz: `🎯 Outcome: [métrica mensurável]`
- Nós filhos: cada espaço de oportunidade (`📌 Oportunidade N: [espaço]`)
- Nós netos: sub-oportunidades de cada espaço (`[dor/desejo específico]`)

### D5 — Criar documento de Próximos Passos no Miro

Chame `mcp__claude_ai_Miro__doc_create` com:
- Título: `🔬 Próximos Passos de Validação`
- Conteúdo: lista das 3 principais perguntas a validar, derivadas das Dúvidas e Suposições de maior prioridade, com método sugerido para cada uma (entrevista, analytics, teste A/B, etc.)

### D6 — Confirmar com o usuário

Após criar os artefatos, responda na conversa:
> "Frameworks criados no Miro ✓
> - 📊 Matriz CSD com [N] itens
> - 🌳 Árvore de Oportunidades com [N] espaços e [M] sub-oportunidades
> - 🔬 [N] próximos passos de validação
>
> [Link do board ou nome do board]"

### D7 — Fallback (Miro não disponível)

Se qualquer chamada Miro falhar, entregue o output em texto na conversa neste formato:

```
📊 MATRIZ CSD — [produto/problema]

| ✅ Certezas | ❓ Suposições | 🔍 Dúvidas |
|-------------|--------------|------------|
| [item]      | [item]       | [item]     |

🌳 ÁRVORE DE OPORTUNIDADES

🎯 Outcome: [métrica mensurável]
📌 Oportunidade 1: [espaço]
  └── 1.1 [sub-oportunidade]
📌 Oportunidade 2: [espaço]
  └── 2.1 [sub-oportunidade]

🔬 PRÓXIMOS PASSOS DE VALIDAÇÃO
1. [Pergunta + método]
2. [Pergunta + método]
```

E avise: *"Miro não está conectado. Cole o output acima manualmente ou conecte o Miro MCP e rode novamente."*

## Exemplo Trabalhado

**Input (rico, com contexto):**
> Somos um SaaS B2B para gestão de freelancers. Quero aumentar ativação de 20% para 35% em 60 dias. Sabemos: usuários que criam o primeiro projeto no dia 1 têm 3x mais retenção; 60% não criam nenhum projeto na semana 1. Achamos que o onboarding é longo demais. Maiores dúvidas: é UX ou produto? Gestores ou freelancers têm mais dificuldade? Dores relatadas: "não sei por onde começar", "convidei freelancers mas não sei criar tarefas", "desisti depois de 30 minutos."

**Resposta do skill (Fase A+B já respondidas, Fase C a completar):**

> Fase A e B já estão bem cobertas pelo contexto. Deixa eu confirmar antes de avançar:
>
> **📊 Matriz CSD — estado atual**
>
> | ✅ Certezas | ❓ Suposições | 🔍 Dúvidas |
> |-------------|--------------|------------|
> | Usuários que criam projeto no dia 1 têm 3x mais retenção | Onboarding é longo demais | É problema de UX ou produto? |
> | 60% não criam nenhum projeto na semana 1 | | Gestores ou freelancers têm mais dificuldade? |
>
> Para completar a CSD e avançar para a Árvore, preciso de mais 2 itens:
> 1. **Certeza:** Tem algum dado de onde exatamente os usuários abandonam? (ex: passo do onboarding, tela específica, tempo médio até sair)
> 2. **Dúvida:** Além do "é UX ou produto" e do segmento, tem mais alguma pergunta que, se respondida, mudaria sua direção?

**Após resposta, entrega o output final completo.**

## Saídas Fora de Escopo

Esta skill NÃO lida com:
- Escrita de PRDs → faça diretamente em conversa
- Criação de prompts para Lovable → use /lovable-prompt
- Especificação de sistemas para Claude Code → use /claude-system-builder
- Planejamento de roteiro de pesquisa com usuários (screener, guia de entrevista) → trate em conversa

## Atalhos Comuns — Não Tome Estes

| O que Claude pode pensar | Por que está errado |
|--------------------------|---------------------|
| "Tenho contexto suficiente para montar a Árvore completa a partir do primeiro input" | A Árvore construída a partir de um único input reflete suposições do modelo, não o contexto real do produto. Perguntas de Fase C surfaceiam dores que não estão no input inicial. |
| "Vou perguntar tudo de uma vez para ser eficiente" | Discovery é um processo de pensamento, não um formulário. Perguntas devem construir sobre respostas anteriores — fazer tudo de uma vez elimina o valor de guiar o raciocínio. |
| "As dúvidas são óbvias, não preciso perguntar" | As dúvidas mais valiosas são as que o time não sabe que tem. A pergunta sobre dúvidas na Fase B é obrigatória. |
| "Vou incluir soluções na Árvore de Oportunidades para ser mais útil" | Soluções na Árvore contaminam o discovery. A Árvore mapeia dores e desejos; soluções são exploradas em um passo posterior explícito. |
| "A CSD está com 2 itens por coluna — boa o suficiente" | O critério de convergência é ≥ 3 por coluna. Com 2, espaços de oportunidade críticos podem ser perdidos. Continue perguntando. |
| "Posso pular a Fase A se o outcome parecer óbvio no input" | O outcome deve ser explicitamente confirmado como métrica mensurável. "Melhorar o onboarding" não é um outcome — "aumentar ativação de 20% para 35%" sim. |
| "O Miro pode falhar — vou só entregar o texto e ignorar o Miro" | Sempre tente o Miro primeiro. O fallback em texto só ocorre se a chamada Miro falhar. Não pule proativamente a tentativa de Miro. |
| "Vou criar um único widget de texto no Miro com tudo junto" | CSD deve ser tabela (`table_create`) e Árvore deve ser diagrama (`diagram_create`). Widgets separados permitem edição independente no Miro. |

## Antes de Marcar Completo

- [ ] Fase A: outcome definido como métrica/comportamento mensurável + usuários nomeados
- [ ] Fase B: CSD com ≥ 3 itens em cada coluna, todos derivados do usuário
- [ ] Fase C: ≥ 3 espaços de oportunidade, cada um com ≥ 1 sub-oportunidade
- [ ] Nenhum item na CSD ou Árvore é genérico ou inventado (todos têm fonte na conversa ou marcação `[SUPOR: confirmar]`)
- [ ] Árvore não contém soluções — apenas dores, desejos e contextos de usuários
- [ ] Próximos passos derivados das dúvidas e suposições de maior prioridade
- [ ] Fase D executada: tabela CSD + diagrama Árvore + doc próximos passos criados no Miro (ou fallback em texto se Miro indisponível, com aviso ao usuário)

## Após Concluir: Registrar Aprendizado

Adicione ao final de `references/learnings.md`:

```
Data: [hoje]
Contexto do produto: [tipo de app, mercado, fase]
Input inicial: [vago / parcial / rico]
Fases puladas (contexto já cobria): [A / B / C / nenhuma]
O que funcionou: [padrão de pergunta ou abordagem que gerou boa resposta]
O que não funcionou: [pergunta que causou confusão ou resposta vaga]
Edge case: [algo inesperado — segmento incomum, dúvida que virou certeza, etc.]
```
