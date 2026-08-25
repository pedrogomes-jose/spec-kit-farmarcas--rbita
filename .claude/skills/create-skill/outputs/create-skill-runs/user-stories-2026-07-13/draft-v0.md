---
name: user-stories
description: Gera histórias de usuário em formato Gherkin (Dado/Quando/Então) com critérios de aceite testáveis, a partir de um PRD/spec já existente na conversa ou em outputs/, ou de uma feature descrita verbalmente quando não há PRD, criando os tickets no Linear/Jira se a integração MCP estiver conectada ou salvando em markdown. Use quando o usuário disser 'criar histórias de usuário', 'escreve as user stories', 'quebra essa feature em histórias', 'gera os critérios de aceite', 'user stories dessa PRD', 'backlog de histórias', 'criar as stories no Linear', 'transforma esse PRD em stories', ou 'write user stories'. Do NOT use para escrever PRDs → use /claude-system-builder ou /lovable-prompt; do NOT use para discovery de produto → use /product-discovery; do NOT use para validar hipótese de problema → use /problem-validation; do NOT use para rotear PRD entre Lovable e Claude Code → use /prd-router.
---

# user-stories

Transforma um PRD, spec técnica ou descrição verbal de feature em histórias de usuário prontas para o backlog — cada uma com formato INVEST, critérios de aceite em Gherkin e rastreabilidade explícita até a fonte. O objetivo é entregar algo que o time de engenharia possa pegar e implementar sem precisar voltar para perguntar "o que isso quer dizer".

## Critical

- Toda história DEVE ter critérios de aceite em Gherkin (Dado/Quando/Então) — não aceitar bullets soltos como critério de aceite.
- Toda história DEVE citar a seção do PRD/spec de onde veio, ou "descrito verbalmente pelo usuário em [data]" se não houver PRD. Nunca inventar requisito sem fonte.
- Story points, prioridade ou qualquer estimativa que não veio do usuário nem do PRD/spec DEVE levar o marcador `[DEFAULT: X — confirmar com o usuário]`. Nunca apresentar uma estimativa inferida como se fosse decisão do time.
- Se o PRD/spec contiver requisitos contraditórios (ex.: um trecho diz "aprovação automática", outro diz "aprovação manual obrigatória"), declarar a contradição explicitamente na história e perguntar qual prevalece — nunca resolver silenciosamente escolhendo um dos dois.

## Step 0: Read Before You Write

| Fonte | Caminho | O que extrair |
|---|---|---|
| PRD/spec na conversa | mensagens anteriores desta conversa | Feature, requisitos funcionais, regras de negócio, critérios de sucesso |
| PRDs salvos | `outputs/prds/*.md` | PRDs existentes relacionados à feature pedida |
| Specs técnicas | `outputs/claude-system-builder-runs/*/spec.md` ou similar | Componentes, modelos de dados, endpoints que viram histórias técnicas |
| Decisões documentadas | `outputs/build-decisions-runs/*.md` (se existir) | Regras de negócio e guardrails já registrados, para não contradizer na história |
| Integração de backlog | Linear/Jira MCP — checar com `ToolSearch` antes de tentar chamar | Projeto/board de destino, esquema de campos (tipo, prioridade, estimativa) |
| Aprendizados anteriores | `references/learnings.md` | Padrões de quebra de história e falhas a evitar em rodadas passadas |

Só gerar histórias depois de completar o Step 0. Se nenhuma fonte de PRD/spec existir, ir para o Step 1 Caso B.

## Step 1: Localizar ou Coletar o Conteúdo da Feature

**Caso A — PRD/spec encontrado (na conversa ou em outputs/):** Extrair a feature, os requisitos funcionais, as regras de negócio e os critérios de sucesso. Citar de qual arquivo ou trecho da conversa cada requisito veio.

**Caso B — Nenhum PRD/spec encontrado:** Não inventar a feature. Responder com este template:

```
Não encontrei um PRD ou spec para esta feature nesta conversa nem em outputs/prds/ ou outputs/claude-system-builder-runs/.

Para gerar as histórias de usuário preciso de uma das duas coisas:
1. Um PRD ou spec — cole aqui, ou aponte o caminho do arquivo.
2. Uma descrição da feature — em 3-5 frases: quem usa, o que ela faz, e qual problema resolve.

Se quiser, também posso rodar /claude-system-builder ou /lovable-prompt primeiro para gerar a spec, e depois quebrar em histórias.

Assim que eu tiver isso, gero as histórias com:
- Formato INVEST (Independente, Negociável, Valiosa, Estimável, Pequena, Testável)
- Critérios de aceite em Gherkin (Dado/Quando/Então)
- Rastreabilidade — cada história cita a origem do requisito
- Estimativa de story points marcada como [DEFAULT] até você confirmar
```

Se o usuário responder com a descrição verbal, tratar como fonte primária (equivalente ao Caso A) e prosseguir.

## Step 2: Quebrar em Épicos e Histórias

1. Agrupar requisitos relacionados em épicos quando a feature for grande o suficiente para precisar de mais de 5 histórias.
2. Quebrar cada épico em histórias que passem no teste INVEST — se uma história não for "Pequena" (implementável em menos de um sprint) ou "Testável" (critério de aceite verificável), quebrar mais.
3. Separar histórias de front-end, back-end/API, migração de dados e infraestrutura quando a feature tocar mais de uma camada — não misturar numa única história.
4. Identificar dependências entre histórias (ex.: "história de API precisa existir antes da história de UI que a consome").

## Step 3: Escrever Cada História

Usar o formato exato da seção Output Format para cada história. Toda história tem:
- Título curto no padrão `[Componente] [Ação] [Sujeito]`
- Declaração "Como [persona], eu quero [ação], para que [benefício]"
- Critérios de aceite em Gherkin — no mínimo 2, cobrindo o caminho feliz e pelo menos um caso de borda
- Rastreabilidade — de onde veio o requisito
- Estimativa `[DEFAULT: X pts — confirmar com o time]` a menos que o usuário tenha dado a estimativa
- Dependências (IDs de outras histórias ou "Nenhuma")

## Step 4: Criar os Tickets ou Salvar

1. Rodar `ToolSearch` com query relacionada a Linear/Jira para checar se há integração MCP conectada.
2. Se conectada: criar um ticket por história, usando o tipo "Story", e registrar o ID retornado.
3. Se não conectada: salvar todas as histórias em `outputs/user-stories/[nome-da-feature]-stories.md`, seguindo o Output Format.
4. Ao final, mostrar uma tabela resumo: história, ID do ticket (ou "salvo em markdown"), estimativa, dependências.

## Output Format

Cada história segue exatamente este template:

```
### [Componente] [Ação] [Sujeito]

**Como** [persona],
**eu quero** [ação],
**para que** [benefício].

**Critérios de Aceite:**
- Dado [contexto], quando [ação], então [resultado esperado]
- Dado [contexto de borda], quando [ação], então [resultado esperado]

**Rastreabilidade:** [seção do PRD/spec ou "descrito verbalmente em 2026-07-13"]
**Estimativa:** [DEFAULT: 3 pts — confirmar com o time] (ou valor confirmado pelo usuário)
**Prioridade:** P0 / P1 / P2
**Dependências:** [IDs de outras histórias ou "Nenhuma"]
```

Ao final de todas as histórias, incluir a **Tabela Resumo** (história | ID do ticket ou local salvo | estimativa | dependências).

## Worked Example

**Input:** "Aqui está o PRD: usuários podem favoritar produtos na lista de busca. Um ícone de coração no card do produto. Ao clicar, o produto vai para uma aba 'Favoritos' no perfil. Não logado, ao clicar deve pedir login primeiro."

**Output (trecho):**

```
### [Busca] Favoritar Produto na Lista

**Como** usuário logado navegando na busca,
**eu quero** clicar no ícone de coração no card do produto,
**para que** eu possa salvá-lo na minha aba de Favoritos.

**Critérios de Aceite:**
- Dado que estou logado e vejo um card de produto na busca, quando clico no ícone de coração, então o produto é adicionado aos meus Favoritos e o ícone muda para preenchido.
- Dado que já favoritei um produto, quando clico no ícone novamente, então o produto é removido dos Favoritos e o ícone volta ao estado vazio.

**Rastreabilidade:** PRD colado na conversa, parágrafo sobre "ícone de coração no card do produto"
**Estimativa:** [DEFAULT: 3 pts — confirmar com o time]
**Prioridade:** P1
**Dependências:** Nenhuma

---

### [Busca] Redirecionar Usuário Não Logado ao Favoritar

**Como** visitante não logado navegando na busca,
**eu quero** ser levado para o login ao clicar no ícone de coração,
**para que** eu não perca a intenção de favoritar depois de entrar.

**Critérios de Aceite:**
- Dado que não estou logado e vejo um card de produto, quando clico no ícone de coração, então sou redirecionado para a tela de login.
- Dado que fiz login após ser redirecionado por essa ação, quando o login é concluído, então o produto original é automaticamente favoritado.

**Rastreabilidade:** PRD colado na conversa, frase "Não logado, ao clicar deve pedir login primeiro"
**Estimativa:** [DEFAULT: 5 pts — confirmar com o time]
**Prioridade:** P1
**Dependências:** [Busca] Favoritar Produto na Lista

---

**Tabela Resumo**

| História | Ticket/Local | Estimativa | Dependências |
|---|---|---|---|
| Favoritar Produto na Lista | salvo em outputs/user-stories/favoritos-stories.md | [DEFAULT] 3 pts | Nenhuma |
| Redirecionar Usuário Não Logado | salvo em outputs/user-stories/favoritos-stories.md | [DEFAULT] 5 pts | Favoritar Produto na Lista |
```

## Out of Scope

Esta skill NÃO faz:
- Escrever ou redigir o PRD em si → use `/claude-system-builder` (sistemas) ou `/lovable-prompt` (apps Lovable)
- Discovery de produto (CSD, árvore de oportunidades) → use `/product-discovery`
- Validar se um problema vale a pena investigar → use `/problem-validation`
- Decidir se a feature vai para Lovable ou Claude Code → use `/prd-router`
- Documentar decisões técnicas/regras de negócio já tomadas → use `/build-decisions`
- Tickets que não são histórias de usuário (bug fix, débito técnico, tarefa de infra sem valor direto ao usuário) → criar diretamente no Linear/Jira sem passar por esta skill

## Cross-Skill Routing

- Se não houver PRD/spec disponível → recomendar `/claude-system-builder` ou `/lovable-prompt` antes de continuar
- Se o usuário pedir para documentar as regras de negócio extraídas → recomendar `/build-decisions`
- Se o usuário ainda não decidiu entre Lovable e Claude Code → recomendar `/prd-router` antes de gerar as histórias

## Common Shortcuts — Do Not Take These

| O que Claude pode pensar | Por que está errado |
|---|---|
| "A feature é simples, dá pra escrever a história sem citar a fonte" | Sem rastreabilidade, ninguém consegue verificar se a história reflete o PRD real ou foi inventada. |
| "Vou estimar os pontos com base em features parecidas que já vi" | Isso é um `[DEFAULT]` disfarçado de decisão do time — precisa do marcador, senão parece confirmado. |
| "O PRD não é tão claro nessa parte, vou escolher a interpretação mais provável" | Contradição ou ambiguidade deve ser declarada explicitamente na história, não resolvida silenciosamente. |
| "Não achei PRD, mas dá pra inferir a feature pelo nome que o usuário deu" | Sem PRD nem descrição verbal, gerar histórias é inventar requisito — sempre parar no Step 1 Caso B. |
| "Vou pular o ToolSearch do Linear/Jira e já salvar em markdown direto" | Se a integração existir e não for checada, o usuário perde a chance de já ter os tickets no board real. |

## Before Marking Complete

Não considerar a tarefa concluída até que todos os itens abaixo sejam verdadeiros:

- [ ] Step 0 foi executado — listar quais fontes foram lidas (PRD na conversa, outputs/prds/, outputs/claude-system-builder-runs/, ToolSearch do Linear/Jira, learnings.md)
- [ ] Se nenhuma fonte existia, o Step 1 Caso B foi usado — não foi inventada uma feature
- [ ] Toda história tem critérios de aceite em Gherkin (Dado/Quando/Então), não bullets soltos
- [ ] Toda história cita a rastreabilidade (seção do PRD ou "descrito verbalmente")
- [ ] Toda estimativa sem confirmação do usuário carrega o marcador `[DEFAULT: X — confirmar com o time]`
- [ ] Contradições no PRD/spec foram declaradas explicitamente, não resolvidas em silêncio
- [ ] A Tabela Resumo foi incluída ao final
- [ ] Se Linear/Jira MCP estava conectado, os tickets foram criados e os IDs aparecem na tabela; se não, o caminho do markdown salvo aparece

## After Completing: Log Learning

Anexar a `references/learnings.md`:
Date / O que funcionou / O que não funcionou / Caso de borda
