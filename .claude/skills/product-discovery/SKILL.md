---
name: product-discovery
description: Guia um processo conversacional de discovery de produto, fazendo perguntas progressivas por fase até construir uma Matriz CSD (Certezas, Suposições, Dúvidas) e uma Árvore de Oportunidades estruturadas a partir do contexto real fornecido. Use quando o usuário disser 'vamos fazer um discovery', 'quero entender esse problema', 'me ajuda com a árvore de oportunidades', 'fazer uma CSD', 'discovery de produto', 'mapear dores dos usuários', 'explorar oportunidades', 'entender as oportunidades do produto', 'investigar esse problema', ou apresentar qualquer dor, métrica, hipótese ou problema de produto para investigar. Do NOT use para escrever PRDs → faça em conversa; do NOT use para criar prompts de Lovable → use /lovable-prompt; do NOT use para criar sistemas → use /claude-system-builder; do NOT use para planejar roteiros de pesquisa com usuários → trate em conversa separada; do NOT use para validar uma hipótese de problema única com JTBD, roteiro Mom Test e critério Go/No-Go de entrevistas → use /problem-validation.
---

# product-discovery

Conduz um discovery de produto estruturado por quatro fases — Ancoragem, CSD, Mapeamento de Oportunidades, Saída — fazendo perguntas progressivas a cada turno até que a Matriz CSD e a Árvore de Oportunidades estejam populadas com o contexto real do produto. O output é sempre derivado das respostas do usuário, nunca de suposições genéricas.

## Critical

- **Nunca pule para soluções.** A Árvore de Oportunidades mapeia dores, desejos e contextos de usuários — não features, não wireframes, não ideias de produto. Soluções são exploradas DEPOIS do discovery.
- **Frameworks derivados do contexto real.** Nenhum item na CSD ou na Árvore pode ser inventado. Se não veio do usuário, marque como `[SUPOR: confirmar]`.
- **Postura cética, não validadora.** Nunca aceite a formulação do outcome, do problema, ou uma "certeza" do usuário de primeira. Ao identificar um pressuposto não comprovado — especialmente uma causa raiz já assumida ("achamos que é X") — questione-o explicitamente e ofereça ao menos uma hipótese alternativa antes de registrá-lo na CSD. Uma "certeza" sem categoria de evidência (ver Fase B) é uma opinião disfarçada de fato: marque para aprofundar, não aceite de primeira.
- **Perguntas progressivas, não em bloco.** Faça 1–3 perguntas por turno, construindo sobre a resposta anterior. Não entregue um formulário de 10 perguntas.
- **Mostre o estado atual dos frameworks.** Após cada fase completada, exiba a CSD e/ou Árvore no estado parcial para que o usuário veja o progresso e corrija antes de avançar.
- **A CSD é viva.** Items podem migrar entre colunas conforme a conversa avança. Dúvidas viram certezas. Suposições são confirmadas ou descartadas.
- **Convergência explícita por fase.** Avance de fase só quando os critérios de convergência da fase atual estiverem satisfeitos.
- **Output final sempre vai para o Miro.** Na Fase D, crie a CSD como tabela e a Árvore como diagrama no Miro. Se o Miro MCP não estiver disponível, entregue o output em texto na conversa e avise o usuário.
- **Nunca invoque o subagente `ux-researcher` automaticamente.** A oferta ao final da Fase B é sempre uma pergunta ao usuário, nunca uma invocação implícita — mesmo padrão de confirmação explícita usado para ativar `/problem-validation` em D6.

## Frameworks Referência (embutido)

### Matriz CSD (Livework)
| ✅ Certezas | ❓ Suposições | 🔍 Dúvidas |
|-------------|--------------|------------|
| O que sabemos com evidência (dados, pesquisa, citações diretas de usuários) | O que ACHAMOS que é verdade — hipóteses e crenças da equipe sem validação formal | O que não sabemos e precisamos descobrir — perguntas abertas críticas |

**Regra de separação:** Uma certeza requer evidência citável (dado, estudo, N usuários disseram). Uma suposição é "acreditamos que...". Uma dúvida é "precisamos descobrir se...".

### Job Statement (JTBD)
```
Quando [situação/contexto], quero [progresso/motivação], para que eu possa [resultado esperado].
```
- **Job funcional:** a tarefa prática que o usuário está tentando completar.
- **Job emocional:** como o usuário quer se sentir (ou parar de sentir) ao completar o job.
- **Job social:** como o usuário quer ser percebido por outros ao completar o job.

**Regra:** o Job Statement é sobre o USUÁRIO, não sobre o produto. Nunca inclua o nome do produto ou uma feature na declaração.

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

**Objetivo:** Definir o outcome desejado, o(s) usuário(s) alvo e o Job Statement (JTBD) que os move.

**Convergência da Fase A:** Outcome articulado como métrica ou comportamento mensurável + persona de usuário nomeada + Job Statement com jobs funcional, emocional e social identificados.

**Quando invocado sem contexto,** use esta abertura determinística:

> Vamos montar o discovery juntos. O processo tem 4 fases:
>
> **Fase A** — Ancoragem (outcome + usuários + job a ser feito) → **Fase B** — Matriz CSD, com cada Certeza categorizada por evidência a favor/contra e uma postura cética sobre pressupostos (ao final, você pode pedir uma segunda opinião ao subagente **ux-researcher** sobre a evidência levantada) → **Fase C** — Árvore de Oportunidades (dores e desejos dos usuários) → **Fase D** — Output final com sinais de Go/No-Go, regra de parada e nível de confiança para a oportunidade priorizada.
>
> Para começar:
>
> 1. **Outcome:** Qual é o resultado de negócio que queremos mover? (ex: aumentar ativação de X% para Y%, reduzir churn de 12 para 20 dias de trial, aumentar NPS de 32 para 50)
> 2. **Usuários:** Quem são os usuários afetados por esse problema? (ex: gestores, usuários novos no trial, admins, freelancers)
> 3. **Job a ser feito:** Quando esse usuário enfrenta essa situação, o que ele está tentando progredir? Que resultado prático ele busca (job funcional), como quer se sentir (job emocional), e como quer ser percebido (job social)?

**Quando contexto parcial for fornecido,** abra reconhecendo o que já foi dado antes de perguntar:

> Aqui está o que já entendi do contexto:
> - [listar o que foi extraído do input inicial, incluindo Job Statement se dedutível]
>
> Antes de seguir, aponto um ponto que vale questionar: [pressuposto não comprovado ou hipótese alternativa — aplicar a postura cética do bloco Critical]
>
> Para avançar, preciso completar:
> - [perguntas apenas sobre o que ainda falta, incluindo Job Statement se não estiver claro no input]

Se o contexto inicial já responde outcome, usuários e Job Statement, vá direto para a Fase B sem perguntar — mas ainda assim aplique o desafio cético antes de confirmar.

**ANTES de confirmar,** aplique a postura cética (bloco Critical): questione ativamente pelo menos um pressuposto do outcome, do problema ou de uma causa-raiz já assumida pelo usuário, e ofereça uma hipótese alternativa. Não pule esta etapa mesmo quando o contexto parecer completo.

**Ao concluir a Fase A:** Confirme com o usuário antes de avançar:
> "Entendido. Vou trabalhar com:
> - **Outcome:** [X]
> - **Usuários:** [Y]
> - **Job Statement:** Quando [situação], quero [progresso], para que eu possa [resultado]. (funcional: [Z] · emocional: [W] · social: [V])
> Podemos avançar para mapear o que sabemos, achamos e não sabemos sobre esse problema?"

## Fase B: Construção da CSD

**Objetivo:** Popular as três colunas da Matriz CSD com o contexto real do produto.

**Convergência da Fase B:** CSD com ≥ 3 itens em cada coluna, todos derivados do usuário ou marcados como `[SUPOR: confirmar]`.

Faça 1–3 perguntas por turno, na ordem abaixo. Avance para a próxima coluna assim que a atual tiver ≥ 3 itens.

**Certezas — evidência categorizada, nos dois sentidos:**

Para cada item candidato a Certeza, sonde ativamente evidência a favor E evidência que enfraquece — não pare na primeira resposta positiva:

- **A favor (força o problema):** frequência (quantos usuários / com que frequência?), impacto (o que isso custa em conversão, retenção, receita, tempo?), tempo ou dinheiro que o usuário já gasta tentando resolver, gambiarras ou processos manuais que já existem como tentativa de solução.
- **Contra (enfraquece a hipótese):** o problema é raro? o impacto é baixo? a solução atual já é suficiente para a maioria? isso é uma preferência do time sendo confundida com um problema do usuário?

**Regra:** uma Certeza sem nenhuma categoria de evidência identificável (nenhuma frequência, impacto, tempo/dinheiro ou gambiarra citados) é uma opinião disfarçada de fato. Marque como `[APROFUNDAR: evidência fraca]` em vez de aceitar como Certeza — e pergunte de novo antes de contar para a convergência de 3 itens.

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

**Ao atingir a convergência da Fase B** (≥ 3 itens por coluna), antes de avançar para a Fase C, ofereça — nunca invoque automaticamente — uma segunda camada de revisão:

> "A CSD está com [N] Certezas, [N] Suposições e [N] Dúvidas. Quer que eu peça uma segunda opinião ao subagente **ux-researcher** antes de avançarmos? Ele revisa especificamente: (a) se alguma Certeza ainda carrega evidência fraca demais para ter saído do `[APROFUNDAR: evidência fraca]`, (b) se alguma causa-raiz assumida escapou sem uma hipótese alternativa, e (c) se a categorização entre Certeza/Suposição/Dúvida está consistente com a regra de evidência citável."

Se o usuário confirmar, invoque o subagente `ux-researcher` passando a CSD completa como contexto — não peça para o usuário repeti-la. Se o usuário recusar ou não responder, avance normalmente para a Fase C. A oferta é sempre opcional e nunca bloqueia o avanço de fase.

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

### D5 — Criar documento de Próximos Passos e Decisão de Investimento no Miro

Antes de tudo, identifique a **oportunidade priorizada**: a sub-oportunidade da Árvore com maior potencial de impacto no outcome OU maior incerteza (a que, se validada ou refutada, mais mudaria a direção).

Chame `mcp__claude_ai_Miro__doc_create` com:
- Título: `🔬 Próximos Passos e Decisão de Investimento`
- Conteúdo:
  1. As 3 principais perguntas a validar, derivadas das Dúvidas e Suposições de maior prioridade, com método sugerido para cada uma (entrevista, analytics, teste A/B, etc.)
  2. **✅ Sinais de confirmação (Go):** 2–3 sinais que, se aparecerem, confirmam que vale investir na oportunidade priorizada — derivados da evidência a favor coletada na Fase B.
  3. **⛔ Sinais de descarte (No-Go/Pivô):** 1–2 sinais que indicariam pivotar ou descartar a oportunidade — derivados da evidência que enfraquece a hipótese, coletada na Fase B.
  4. **🛑 Regra de parada:** uma regra objetiva e verificável (ex.: "se [sinal esperado] não aparecer espontaneamente em N conversas/fontes, a oportunidade não tem densidade suficiente para avançar").
  5. **📶 Nível de confiança** na oportunidade priorizada, em duas dimensões, cada uma com uma frase justificando: **qualidade da evidência coletada** (Alta/Média/Baixa) e **robustez frente a hipóteses alternativas** (Alta/Média/Baixa — ou seja, o quanto a Fase A já considerou e descartou explicações concorrentes).

### D6 — Confirmar com o usuário e propor validação da oportunidade priorizada

Após criar os artefatos, responda na conversa:
> "Frameworks criados no Miro ✓
> - 📊 Matriz CSD com [N] itens
> - 🌳 Árvore de Oportunidades com [N] espaços e [M] sub-oportunidades
> - 🔬 [N] próximos passos + sinais de Go/No-Go + nível de confiança ([Alta/Média/Baixa] evidência, [Alta/Média/Baixa] robustez)
>
> [Link do board ou nome do board]
>
> Quer que eu já valide a oportunidade prioritária — **[nome da sub-oportunidade priorizada]** — com JTBD completo e roteiro de entrevista (The Mom Test)? Se sim, eu chamo a skill `/problem-validation` já com o outcome, essa oportunidade e as suposições/dúvidas relacionadas que levantamos aqui, pra você não repetir contexto."

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

✅ SINAIS DE CONFIRMAÇÃO (GO)
1. [sinal]
2. [sinal]

⛔ SINAIS DE DESCARTE (NO-GO/PIVÔ)
1. [sinal]

🛑 REGRA DE PARADA
[regra objetiva]

📶 NÍVEL DE CONFIANÇA — [oportunidade priorizada]
Qualidade da evidência: [Alta/Média/Baixa] — [justificativa]
Robustez frente a hipóteses alternativas: [Alta/Média/Baixa] — [justificativa]
```

E avise: *"Miro não está conectado. Cole o output acima manualmente ou conecte o Miro MCP e rode novamente."*

Mesmo no fallback em texto, ofereça avançar para `/problem-validation` na oportunidade priorizada, conforme D6.

## Exemplo Trabalhado

**Input (rico, com contexto):**
> Somos um SaaS B2B para gestão de freelancers. Quero aumentar ativação de 20% para 35% em 60 dias. Sabemos: usuários que criam o primeiro projeto no dia 1 têm 3x mais retenção; 60% não criam nenhum projeto na semana 1. Achamos que o onboarding é longo demais. Maiores dúvidas: é UX ou produto? Gestores ou freelancers têm mais dificuldade? Dores relatadas: "não sei por onde começar", "convidei freelancers mas não sei criar tarefas", "desisti depois de 30 minutos."

**Resposta do skill (Fase A+B já bem cobertas pelo contexto, com JTBD e desafio cético aplicados):**

> Aqui está o que já entendi do contexto:
> - **Outcome:** aumentar ativação de 20% para 35% em 60 dias
> - **Usuários:** gestores e freelancers no SaaS de gestão de freelancers
>
> **Job Statement (dedutível do contexto):** Quando um gestor convida freelancers para a plataforma, ele quer conseguir organizar o trabalho deles rapidamente, para que possa confiar que nada vai passar despercebido. (funcional: criar e distribuir tarefas · emocional: sentir controle, não ansiedade · social: ser visto como organizado pelo time)
>
> Antes de seguir, um ponto que vale questionar: vocês disseram "achamos que o onboarding é longo demais" — isso é uma Suposição, não uma Certeza. Hipótese alternativa igualmente plausível: o onboarding pode ter a duração certa, mas o problema ser a ORDEM das etapas (ex: pedir para criar tarefa antes de o usuário entender o que é um "projeto" na ferramenta). Vou manter como Suposição até termos evidência específica.
>
> **📊 Matriz CSD — estado atual**
>
> | ✅ Certezas | ❓ Suposições | 🔍 Dúvidas |
> |-------------|--------------|------------|
> | Usuários que criam projeto no dia 1 têm 3x mais retenção *(impacto)* | Onboarding é longo demais | É problema de UX ou produto? |
> | `[APROFUNDAR: evidência fraca]` 60% não criam projeto na semana 1 — falta saber se é falta de interesse, dificuldade de descoberta, ou solução atual já resolver de outro jeito | Ordem das etapas pode ser a causa raiz, não a duração | Gestores ou freelancers têm mais dificuldade? |
>
> Para completar a CSD, preciso primeiro fechar a evidência fraca:
> 1. **Aprofundar a certeza fraca:** dos 60% que não criam projeto na semana 1, existe dado de ONDE eles abandonam, ou é só a taxa agregada? Alguma gambiarra (ex: gestor organizando tarefas fora da ferramenta) que confirme que a dor é real, não falta de interesse?
> 2. **Dúvida:** Além do "é UX ou produto" e do segmento, tem mais alguma pergunta que, se respondida, mudaria sua direção?

**Após resposta, entrega o output final completo** — incluindo, ao final da Fase B (assim que a CSD atingir ≥ 3 itens por coluna), a oferta de revisão pelo subagente `ux-researcher`, e, na Fase D, os sinais de Go/No-Go e o nível de confiança da oportunidade priorizada.

## Saídas Fora de Escopo

Esta skill NÃO lida com:
- Escrita de PRDs → faça diretamente em conversa
- Criação de prompts para Lovable → use /lovable-prompt
- Especificação de sistemas para Claude Code → use /claude-system-builder
- Planejamento de roteiro de pesquisa com usuários (screener, guia de entrevista, logística de recrutamento) → trate em conversa
- Validação de uma hipótese de problema específica com JTBD completo + roteiro Mom Test + critério Go/No-Go de entrevistas → use /problem-validation (ver Cross-Skill Routing abaixo)

## Cross-Skill Routing

- **Ao final da Fase D**, sempre proponha avançar para `/problem-validation` na oportunidade priorizada (ver D6). Passe como contexto: outcome, Job Statement, a sub-oportunidade priorizada, e as Suposições/Dúvidas da CSD relacionadas a ela — `/problem-validation` não deve perguntar de novo o que já foi levantado aqui.
- Se o usuário quiser validar uma oportunidade específica da Árvore ANTES de a Fase D estar completa (ex.: "essa dor aqui parece a mais forte, já quero validar"), ofereça rodar `/problem-validation` nela imediatamente, sem esperar a Fase D — não force o usuário a completar todo o discovery antes de agir sobre um sinal forte.
- **Ao final da Fase B**, sempre ofereça uma segunda opinião do subagente `ux-researcher` sobre a qualidade de evidência da CSD inteira — apenas se o usuário confirmar. Isso é diferente de D6: aqui se audita a CSD completa (todas as Certezas/Suposições), lá se valida em profundidade UMA oportunidade priorizada.

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
| "A certeza já parece sólida, não preciso categorizar a evidência" | Certezas sem frequência, impacto, tempo/dinheiro ou gambiarra citados são opiniões disfarçadas de fato. Categorizar é o que separa fato de crença — marque `[APROFUNDAR: evidência fraca]` se nenhuma categoria aparecer. |
| "O usuário já validou a causa raiz, não preciso questionar" | O usuário trouxe uma Suposição ("achamos que é X"), não uma Certeza. Toda causa-raiz assumida precisa de ao menos 1 desafio cético e 1 hipótese alternativa antes de qualquer coisa virar Certeza. |
| "Posso pular o Job Statement se o outcome já parecer claro" | Outcome é o resultado de negócio; JTBD é o motivo do usuário. Sem JTBD, a Árvore de Oportunidades (Fase C) mapeia dores desconectadas do job real que o usuário está tentando fazer. |
| "A CSD e a Árvore já são suficientes, não preciso do Go/No-Go" | Sem sinais de confirmação/descarte e regra de parada, o usuário não tem critério objetivo para decidir se investe. O discovery vira um mapa sem bússola — a Fase D não converge sem esse bloco. |
| "A CSD convergiu (≥3 por coluna), posso pular a oferta do ux-researcher e ir direto para a Fase C" | A oferta ao final da Fase B é o que audita a qualidade de evidência da CSD inteira antes de construir a Árvore em cima dela — pular a oferta silenciosamente priva o usuário dessa checagem. |
| "O time parece confiante nas Certezas, vou invocar o ux-researcher direto sem perguntar" | Confirmação explícita é obrigatória, nunca inferida do tom da conversa — mesmo padrão de confirmação já usado antes de ativar `/problem-validation` em D6. |

## Antes de Marcar Completo

- [ ] Fase A: outcome definido como métrica/comportamento mensurável + usuários nomeados + Job Statement com jobs funcional, emocional e social
- [ ] Ao menos 1 pressuposto ou causa-raiz assumida pelo usuário foi questionado ativamente (postura cética) com uma hipótese alternativa oferecida
- [ ] Fase B: CSD com ≥ 3 itens em cada coluna, todos derivados do usuário; cada Certeza tem categoria de evidência identificada (frequência/impacto/tempo-dinheiro/gambiarra) ou está marcada `[APROFUNDAR: evidência fraca]`
- [ ] Fase B: oferta explícita de revisão pelo subagente `ux-researcher` feita ao atingir a convergência — sem invocação automática, sem bloquear o avanço para a Fase C
- [ ] Fase C: ≥ 3 espaços de oportunidade, cada um com ≥ 1 sub-oportunidade
- [ ] Nenhum item na CSD ou Árvore é genérico ou inventado (todos têm fonte na conversa ou marcação `[SUPOR: confirmar]`)
- [ ] Árvore não contém soluções — apenas dores, desejos e contextos de usuários
- [ ] Fase D inclui sinais de Go, sinais de No-Go/Pivô, regra de parada, e nível de confiança (2 dimensões) para a oportunidade priorizada
- [ ] D6 propõe explicitamente avançar para `/problem-validation` na oportunidade priorizada, passando outcome + JTBD + Suposições/Dúvidas relacionadas como contexto
- [ ] Fase D executada: tabela CSD + diagrama Árvore + doc próximos passos/Go-No-Go criados no Miro (ou fallback em texto se Miro indisponível, com aviso ao usuário)

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
