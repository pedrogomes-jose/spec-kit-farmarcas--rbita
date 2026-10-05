---
name: orbita-user-stories
description: Gera cards de história de usuário do Órbita no template oficial do board Jira SQO, sempre verificando os 3 repositórios de código do produto antes de citar caminho/endpoint e revisando cada card com o subagente de clareza júnior. Use quando o usuário disser 'cria os cards do Órbita', 'quebra essa feature do Órbita em cards', 'história de usuário pro board SQO', 'card pro Jira do Órbita', 'gera o card no formato do Órbita', ou pedir para transformar um PRD/spec do Órbita em backlog. Do NOT use para projetos fora do Órbita → use /user-stories; do NOT use para escrever o PRD em si → use /claude-system-builder ou /lovable-prompt; do NOT use para discovery de produto → use /product-discovery; do NOT use para validar uma hipótese de problema → use /problem-validation.
---

# orbita-user-stories

Transforma um PRD, spec técnica ou descrição verbal de feature do **Órbita**
(ferramenta de viabilidade de pontos comerciais da Farmarcas) em cards de
backlog no formato exato do template oficial do board Jira **SQO - ÓRBITA**.
Diferente da skill genérica `/user-stories`, esta skill (1) sempre confere os
3 repositórios de código do Órbita antes de citar qualquer caminho/endpoint,
e (2) sempre passa cada card pelo subagente `(?_?) revisor-clareza-junior`
antes de considerá-lo pronto.

## Critical

- **Motivação de negócio**: o time do Órbita agora tem devs júnior. Um card
  com jargão de domínio não definido (score de viabilidade, camada, raio de
  análise), caso de borda implícito, ou nenhuma pista de onde mexer no código
  gera retrabalho e dependência de interromper um sênior. Esta skill existe
  para fechar esse gap antes do card chegar ao board.
- Todo card DEVE seguir exatamente as 7 seções do template Jira SQO, nesta
  ordem — nunca o formato solto "Como/Eu quero/Para que" da skill genérica:
  **Contexto, Referências visuais, Caminho/rota, Escopo do card, Regras de
  negócio, Critérios de aceite, Figma** (ver Output Format).
- Toda pista de caminho/endpoint/componente citada em "Caminho/rota" ou
  "Escopo do card" DEVE ser conferida com Grep/Glob/Read nos 3 repositórios
  **nesta mesma sessão** antes de aparecer no card. Nunca citar um caminho
  plausível sem checar. Se não encontrar correspondência real, escrever
  literalmente "Não localizado no código — confirmar com o time" em vez de
  inventar.
- Todo card, antes de ser apresentado como final ao usuário, DEVE passar pelo
  subagente `(?_?) revisor-clareza-junior` (Agent tool). Se o veredito for
  "precisa de ajuste", incorporar a reescrita sugerida e reapresentar o card
  completo ajustado — nunca colar o feedback bruto do subagente como se fosse
  a entrega, e nunca marcar um card como pronto sem o veredito "pronto para o
  júnior".
- Toda história DEVE ter Critérios de Aceite em Gherkin (Dado/Quando/Então)
  dentro da seção "Critérios de aceite", cobrindo caminho feliz + pelo menos
  um caso de borda — nunca bullets soltos.
- Rastreabilidade é obrigatória dentro da seção "Contexto": citar de onde veio
  o requisito (PRD, spec, trecho da conversa, ou "descrito verbalmente em
  [data]"). Nunca inventar requisito sem fonte.
- Estimativa/prioridade sem confirmação do usuário ou do PRD/spec DEVE levar
  o marcador `[DEFAULT: X — confirmar com o time]`.
- Se o PRD/spec contiver requisitos contraditórios, declarar a contradição
  explicitamente dentro de "Regras de negócio" — nunca resolver em silêncio.
- Sempre incluir o texto completo de cada card (as 7 seções inteiras) na
  resposta ao usuário. Criar o ticket no Jira ou salvar em markdown é
  adicional — nunca substitui mostrar o card completo.

## Step 0: Read Before You Write

| Fonte | Caminho | O que extrair |
|---|---|---|
| PRD/spec na conversa | mensagens anteriores desta conversa | Feature, requisitos funcionais, regras de negócio |
| PRDs salvos | `outputs/prds/*.md` | PRDs existentes relacionados à feature pedida |
| Specs técnicas | `outputs/claude-system-builder-runs/*/spec.md` | Componentes, endpoints que viram cards técnicos |
| Decisões documentadas | `outputs/build-decisions-runs/*.md` (se existir) | Regras de negócio e guardrails já registrados |
| Estudos de domínio | `docs/confluence/ia/analises/*.md`, `docs/confluence/2025/evolucao-camadas/*.md` | Como o score/camadas funcionam hoje, para não contradizer na Regra de negócio |
| **Backend agente/IA** | `C:\Users\zequi\projetos\api-agent-orbita\src` (`routes/`, `controllers/`, `services/analysisAgent/`) | Endpoints reais (ex.: `POST /analysis`, `GET /layers/radius`), lógica de score (`services/analysisAgent/scoring.ts`), nomes de controller/service |
| **Backend legado** | `C:\Users\zequi\projetos\api-orbita-nodejs\src` (`controllers/`, `services/`) | Endpoints reais (ex.: `GET /available/radius` em `sourceController.js`), controllers de fonte/arquivo/agrupamento |
| **Frontend** | `C:\Users\zequi\projetos\webapp-orbita-angular\src\app\modules` | Módulos/componentes reais (ex.: `modules/analysis/pages/dashboard/components/...`), rotas Angular |
| Template oficial do card | Jira SQO-1060 (já extraído — ver Output Format abaixo, não precisa reconsultar a cada card) | As 7 seções e sua ordem exata |
| Aprendizados anteriores | `references/learnings.md` (desta skill) | Padrões de card e falhas a evitar em rodadas passadas |
| Integração de backlog | Jira MCP — checar com `ToolSearch` antes de tentar chamar | Projeto SQO - ÓRBITA, tipo de issue "História" |

Regra dura: nunca escrever "Caminho/rota" ou uma pista de código em "Escopo
do card"/"Regras de negócio" sem ter rodado Grep/Glob real nos 3 repositórios
acima **na sessão atual**. Um caminho lembrado de uma rodada anterior deve
ser reconferido — código muda.

Só gerar cards depois de completar o Step 0. Se nenhuma fonte de PRD/spec
existir, ir para o Step 1 Caso B.

## Step 1: Localizar ou Coletar o Conteúdo da Feature

**Caso A — PRD/spec encontrado:** Extrair a feature, os requisitos
funcionais, as regras de negócio e os critérios de sucesso. Citar de qual
arquivo ou trecho da conversa cada requisito veio.

**Caso B — Nenhum PRD/spec encontrado:** Não inventar a feature. Responder:

```
Não encontrei um PRD ou spec para esta feature nesta conversa, em outputs/prds/,
outputs/claude-system-builder-runs/, nem nos estudos de docs/confluence/.

Para gerar os cards no formato do Órbita preciso de uma das duas coisas:
1. Um PRD ou spec — cole aqui, ou aponte o caminho do arquivo.
2. Uma descrição da feature — em 3-5 frases: quem usa (analista de Expansão?
   time interno?), o que ela faz, e qual problema resolve.

Assim que eu tiver isso, gero os cards no template do board SQO (Contexto,
Referências visuais, Caminho/rota, Escopo do card, Regras de negócio,
Critérios de aceite, Figma), já conferindo caminhos de código reais nos 3
repositórios do Órbita e revisando cada card com o subagente de clareza
júnior antes de entregar.
```

Se o usuário responder com a descrição verbal, tratar como fonte primária
(equivalente ao Caso A) e prosseguir.

## Step 2: Quebrar em Épicos e Histórias (INVEST)

1. Agrupar requisitos relacionados em épicos quando a feature precisar de
   mais de 5 cards.
2. Quebrar cada épico em cards que passem no teste INVEST — se um card não
   for "Pequeno" (implementável em menos de um sprint) ou "Testável"
   (critério de aceite verificável), quebrar mais.
3. Separar cards de front-end (`webapp-orbita-angular`), backend/API
   (`api-agent-orbita` ou `api-orbita-nodejs`, conforme onde a lógica real
   mora) e infraestrutura quando a feature tocar mais de uma camada — não
   misturar num único card.
4. Identificar dependências entre cards.

## Step 3: Verificar Código Real Antes de Redigir

Para cada pista de implementação que o card vai citar (endpoint, controller,
service, componente Angular, ou nome de campo/variável), rodar Grep/Glob/Read
nos 3 repositórios listados no Step 0. Classificar o que foi encontrado em
um destes três níveis — nunca colapsar o segundo no primeiro:
- **Confirmado**: arquivo/endpoint/campo existe literalmente com esse nome —
  citar arquivo:linha.
- **Lógica confirmada, nome não confirmado**: a funcionalidade existe (ex.:
  agregação de concorrentes), mas o nome exato do campo/variável citado no
  PRD ou pela pessoa que pediu o card não aparece literalmente no código —
  citar o arquivo onde a lógica mora e declarar "nome exato do campo não
  confirmado no código, checar com o time antes de implementar assim".
- **Não localizado**: nenhuma correspondência — escrever literalmente "Não
  localizado no código — confirmar com o time".
Esse levantamento alimenta a seção "Caminho/rota" e "Escopo do card" do
Step 4, e é exatamente o que o `(?_?) revisor-clareza-junior` vai reconferir
no Step 5 — checar antes economiza uma rodada de ajuste.

## Step 4: Escrever Cada Card no Template Jira SQO

Usar exatamente este formato — extraído do template oficial (SQO-1060):

```
### [Componente] [Ação] [Sujeito]

**Contexto:**
[O problema de negócio que este card resolve, em linguagem que alguém sem
conhecimento prévio do domínio Órbita entenda. Se o card depende de um termo
de domínio (score de viabilidade, camada, raio de análise, potencial de
consumo), definir em uma frase.]
Rastreabilidade: [seção do PRD/spec, ou "descrito verbalmente em 2026-09-17"]

**Referências visuais:**
[Prints, links de tela, ou "Não informado — solicitar ao design"]

**Caminho/rota:**
[Caminho de navegação dentro do produto até a funcionalidade, ex.:
"Radar → ícone de 4 quadradinhos → Órbita → ...". Se o card for
back-end puro sem rota de UI, escrever "Não aplicável — card técnico"]

**Escopo do card:**
* [O que entra, com pista de código já verificada nos repositórios: arquivo/
  endpoint/componente real, ex.: "endpoint `POST /analysis` em
  `api-agent-orbita/src/controllers/analysis.controller.ts`"]
* [O que explicitamente NÃO entra neste card, se relevante]

**Regras de negócio:**
[As regras que a implementação deve respeitar, explicadas com o "porquê",
não só o "o quê". Declarar aqui qualquer contradição encontrada no PRD/spec.]

**Critérios de aceite:**
- Dado [contexto], quando [ação], então [resultado esperado]
- Dado [contexto de borda], quando [ação], então [resultado esperado]
- Não se pode fugir da seção Escopo do card
- Estar em conformidade com as regras de negócio
- Passar nos testes definidos por QA
- Estar em conformidade com o Figma

**Figma:** [link, ou "Não informado — solicitar ao design"]

**Estimativa:** [DEFAULT: 3 pts — confirmar com o time] (ou valor confirmado)
**Prioridade:** [DEFAULT: P1 — confirmar com o time] (ou valor confirmado)
**Dependências:** [IDs de outros cards ou "Nenhuma"]
**Revisado por (?_?) revisor-clareza-junior:** [veredito final]
```

## Step 5: Revisão Obrigatória — (?_?) revisor-clareza-junior

1. Para cada card redigido no Step 4, invocar o subagente `(?_?)
   revisor-clareza-junior` (Agent tool), passando o card completo e os
   caminhos de código já verificados no Step 3.
2. Se o veredito for **"precisa de ajuste"**: reescrever o card incorporando
   cada sugestão concreta retornada, e repetir a revisão até obter
   **"pronto para o júnior"**. Nunca mostrar ao usuário um card com veredito
   pendente.
3. Anexar ao final do card a linha `**Revisado por (?_?)
   revisor-clareza-junior:** pronto para o júnior`.
4. Se após 2 rodadas de ajuste o subagente ainda não aprovar (ex.: porque a
   pista de código real não existe e o PRD não dá informação suficiente para
   substituí-la), parar e declarar isso explicitamente ao usuário em vez de
   forçar uma aprovação — é sinal de que falta informação, não de um card mal
   escrito.

## Step 6: Criar os Tickets ou Salvar

1. Rodar `ToolSearch` com query relacionada a Jira para checar integração MCP.
2. Se conectada: criar um ticket por card no projeto **SQO - ÓRBITA**, tipo
   de issue "História", usando a descrição no formato do template acima.
3. Se não conectada: salvar em `outputs/orbita-user-stories/[feature]-cards.md`.
4. Mostrar tabela resumo: card | ID do ticket ou "salvo em markdown" |
   estimativa | veredito do revisor-clareza-junior.

## Worked Example

**Input:** "O estudo de peso de população recomendou expor o breakdown do
score por dimensão na tela de resultado — hoje o analista só vê a nota final,
não sabe quanto veio de população, densidade, consumo e renda. Quebra isso
em cards pro time, temos júnior no time agora."

**Step 0 (trecho):** Lido `docs/confluence/ia/analises/estudo-peso-populacao-score-viabilidade.md`
(recomenda "Alinhar backend, integrando cálculo determinístico (scoring.ts)
ou expor breakdown na resposta de /analysis"). Grep em `api-agent-orbita/src`
confirma `POST /analysis` (`src/routes/analysis.routes.ts` →
`src/controllers/analysis.controller.ts`) e a lógica de pontuação em
`src/services/analysisAgent/scoring.ts` (funções como `scorePopulation`).
Grep em `webapp-orbita-angular/src/app/modules/analysis/pages/dashboard`
confirma existência de `components/general/general.component.ts` como
candidato a exibir o breakdown.

**Output (card 1 de 2, backend):**

```
### [API] Expor Breakdown do Score por Dimensão na Resposta de Análise

**Contexto:**
Hoje o Órbita calcula um score de viabilidade de 0 a 20 pontos somando 4
dimensões (população, densidade, potencial de consumo, renda), mas a API só
devolve a nota final. O analista de Expansão não consegue ver quanto cada
dimensão contribuiu, o que dificulta entender por que um ponto comercial
recebeu determinada nota. "Dimensão" aqui significa cada um dos 4 critérios
somados no score — não confundir com "camada" (fonte de dado geográfica).
Rastreabilidade: docs/confluence/ia/analises/estudo-peso-populacao-score-viabilidade.md,
seção "Recomendações e Backlog Sugerido → Curto prazo".

**Referências visuais:**
Não informado — solicitar ao design.

**Caminho/rota:**
Não aplicável — card técnico (consumido pelo card de frontend abaixo).

**Escopo do card:**
* Alterar o endpoint `POST /analysis` (`api-agent-orbita/src/controllers/analysis.controller.ts`)
  para incluir no payload de resposta um objeto `scoreBreakdown` com a
  pontuação individual de cada dimensão, usando as funções já existentes em
  `src/services/analysisAgent/scoring.ts` (ex.: `scorePopulation`).
* Não entra neste card: mudança na fórmula de pontuação em si, nem no prompt
  da IA (`src/services/analysisAgent/prompt.ts`) — só exposição do dado que
  já é calculado internamente.

**Regras de negócio:**
Cada dimensão vale até 5 pontos, num total de 20. O breakdown deve refletir
exatamente os mesmos valores que hoje entram na soma do score final — se a
soma do `scoreBreakdown` não bater com o score total retornado, é bug, não
arredondamento aceitável.

**Critérios de aceite:**
- Dado um ponto com população de 10.189 habitantes, quando a API `/analysis`
  é chamada, então `scoreBreakdown.population` retorna 1 (faixa 10.000-19.999).
- Dado qualquer ponto avaliado, quando a resposta é montada, então a soma dos
  4 valores de `scoreBreakdown` é sempre igual ao campo de score total já
  existente.
- Não se pode fugir da seção Escopo do card
- Estar em conformidade com as regras de negócio
- Passar nos testes definidos por QA
- Estar em conformidade com o Figma

**Figma:** Não informado — solicitar ao design.

**Estimativa:** [DEFAULT: 3 pts — confirmar com o time]
**Prioridade:** [DEFAULT: P1 — confirmar com o time]
**Dependências:** Nenhuma
**Revisado por (?_?) revisor-clareza-junior:** pronto para o júnior
```

*(o segundo card, de frontend, seguiria o mesmo formato citando
`modules/analysis/pages/dashboard/components/general/general.component.ts`
como ponto de entrada confirmado, com dependência do card acima)*

## Out of Scope

Esta skill NÃO faz:
- Cards de projetos que não são o Órbita → use `/user-stories`
- Escrever ou redigir o PRD em si → use `/claude-system-builder` (sistemas)
  ou `/lovable-prompt` (apps Lovable)
- Discovery de produto (CSD, árvore de oportunidades) → use `/product-discovery`
- Validar se um problema vale a pena investigar → use `/problem-validation`
- Decidir se a feature vai para Lovable ou Claude Code → use `/prd-router`
- Documentar decisões técnicas/regras de negócio já tomadas → use `/build-decisions`
- Avaliar fonte de dado externa para uma camada nova → use o subagente
  `(⚑_⚑) estrategista-fontes-dados`
- Tickets que não são histórias de usuário (bug, débito técnico, tarefa de
  infra sem valor direto ao usuário) → criar diretamente no Jira

## Cross-Skill Routing

- Se não houver PRD/spec disponível → recomendar `/claude-system-builder` ou
  `/lovable-prompt` antes de continuar
- Se o usuário pedir para documentar as regras de negócio extraídas →
  recomendar `/build-decisions`
- Se a feature envolve uma camada de dado nova/frágil (ex.: fluxo de
  pessoas) → recomendar o subagente `(⚑_⚑) estrategista-fontes-dados` antes
  de especificar os cards
- Se o card gerado for para um repositório fora dos 3 do Órbita → parar e
  recomendar `/user-stories` (a skill genérica) em vez de continuar

## Common Shortcuts — Do Not Take These

| O que Claude pode pensar | Por que está errado |
|---|---|
| "O endpoint provavelmente se chama assim, não preciso conferir" | É exatamente esse tipo de suposição plausível que gera retrabalho para um júnior — sempre Grep/Glob real antes de citar. |
| "O card ficou claro pra mim, posso pular o revisor-clareza-junior" | "Claro pra mim" não é o critério — o critério é claro para quem nunca viu o domínio Órbita. Pular a revisão é pular o motivo pelo qual esta skill existe. |
| "O revisor pediu ajuste pequeno, vou só colar o feedback dele no final do card" | O card final deve incorporar a reescrita, não expor o processo de revisão como se fosse a entrega. |
| "Vou usar o formato Como/Eu quero/Para que da skill genérica, é mais rápido" | O board SQO usa um template fixo diferente — um card fora do template não é aceito pelo time como está. |
| "Não achei o arquivo, mas dá pra inferir o nome pela convenção do resto do projeto" | Inferir nome de arquivo por convenção ainda é inventar um caminho de código — declarar "não localizado" é a resposta correta. |
| "Achei a lógica (ex.: agregação de concorrentes), então o nome de campo que a pessoa usou deve estar certo" | Achar a lógica não confirma o nome exato do campo/variável — são dois níveis de confirmação diferentes (ver Step 3); tratar como confirmado sem checar o nome literal é uma suposição disfarçada de fato verificado. |
| "A regra de negócio é intuitiva pra quem manja de Órbita, não preciso explicar o porquê" | O público-alvo do card inclui júnior sem esse contexto — "intuitivo pra mim" nunca é critério de aceite para clareza. |

## Before Marking Complete

- [ ] Step 0 executado — fontes de PRD/spec E os 3 repositórios de código
      foram lidos/grepados nesta sessão (listar quais)
- [ ] Se nenhuma fonte de PRD/spec existia, o Step 1 Caso B foi usado
- [ ] Todo card segue as 7 seções exatas do template SQO, na ordem certa
- [ ] Toda pista de caminho/endpoint no card foi confirmada nos repositórios
      (ou marcada como "não localizado")
- [ ] Todo card tem Critérios de Aceite em Gherkin, cobrindo caminho feliz +
      pelo menos um caso de borda
- [ ] Toda estimativa/prioridade sem confirmação carrega `[DEFAULT: X —
      confirmar com o time]`
- [ ] Contradições no PRD/spec foram declaradas explicitamente
- [ ] Todo card foi revisado pelo subagente `(?_?) revisor-clareza-junior` e
      só aparece na resposta final com veredito "pronto para o júnior"
- [ ] O texto completo de cada card apareceu na resposta ao usuário
- [ ] Se Jira MCP estava conectado, os tickets foram criados no projeto SQO;
      se não, o caminho do markdown salvo aparece

## After Completing: Log Learning

Anexar a `references/learnings.md`:
Date / O que funcionou / O que não funcionou / Caso de borda / Quantas
rodadas o revisor-clareza-junior pediu até aprovar
