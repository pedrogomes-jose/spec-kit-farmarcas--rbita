---
name: orbita-user-stories
description: Gera e atualiza cards de história de usuário no template oficial do board Jira SQO, a partir de PRD, spec, estudo, transcrição de reunião ou descrição verbal, revisando cada card com o subagente de clareza júnior. Use quando o usuário disser 'cria os cards do Órbita', 'quebra essa feature em cards', 'história de usuário pro board SQO', 'card pro Jira do Órbita', 'atualiza o card SQO-xxxx', 'transforma essa ata/transcrição em card', ou pedir para transformar um PRD, estudo ou reunião em backlog do board SQO. Cobre o board SQO inteiro: features do produto Órbita (onde confere os 3 repositórios de código antes de citar caminho/endpoint) e features de outros produtos da Farmarcas que usam o mesmo board, como Gestão de Lojas do Radar (onde declara 'fora dos repositórios do Órbita' em vez de inventar caminho). Do NOT use para cards que não vão para o board SQO → use /user-stories; do NOT use para escrever o PRD em si → use /claude-system-builder ou /lovable-prompt; do NOT use para discovery de produto → use /product-discovery; do NOT use para validar uma hipótese de problema → use /problem-validation.
---

# orbita-user-stories

Transforma um PRD, spec técnica ou descrição verbal de feature do **Órbita**
(ferramenta de viabilidade de pontos comerciais da Farmarcas) em cards de
backlog no formato exato do template oficial do board Jira **SQO - ÓRBITA**.
O escopo desta skill é o **board SQO**, não só o produto Órbita. O board
recebe cards de dois tipos de origem, e a diferença muda só o Step 3:
- **Feature do produto Órbita** → confere os 3 repositórios de código antes de
  citar qualquer caminho/endpoint.
- **Feature de outro produto da Farmarcas no mesmo board** (ex.: Gestão de
  Lojas do Radar) → pula a verificação de repositório e declara
  "Não aplicável — fora dos repositórios do Órbita", sem inventar caminho.

Nos dois casos a skill (1) emite o template do board e (2) passa cada card
pelo subagente `(?_?) revisor-clareza-junior` antes de considerá-lo pronto.

## Critical

- **Motivação de negócio**: o time do Órbita agora tem devs júnior. Um card
  com jargão de domínio não definido (score de viabilidade, camada, raio de
  análise), caso de borda implícito, ou nenhuma pista de onde mexer no código
  gera retrabalho e dependência de interromper um sênior. Esta skill existe
  para fechar esse gap antes do card chegar ao board.
- Todo card DEVE seguir exatamente as 8 seções do template Jira SQO, nesta
  ordem — nunca o formato solto "Como/Eu quero/Para que" da skill genérica:
  **Contexto, Referências visuais, Caminho/rota, Escopo do card, Regras de
  negócio, Pontos em aberto, Critérios de aceite, Figma** (ver Output Format).
- A seção **"Pontos em aberto" é obrigatória e nunca pode ser omitida**. Toda
  ambiguidade, contradição ou lacuna da fonte vira um item ali, **citando o
  trecho literal** que gerou a dúvida — nunca uma regra inventada em
  "Regras de negócio". Se não houver nenhuma, escrever literalmente "Nenhum",
  para distinguir "não há" de "não verifiquei".
- A seção **"Contexto" DEVE trazer os três**: (a) o comportamento ATUAL, (b)
  por que ele está errado, (c) o impacto concreto de negócio de deixar como
  está. Só o "o quê" não basta.
- Quando a fonte mostrar uma **alternativa que foi sugerida e rebatida**,
  registrá-la em "Contexto" com o motivo da rejeição. Sem esse registro, o
  próximo dev "simplifica" de volta a decisão que o time já descartou.
- "Regras de negócio" DEVE ser **lista numerada e atômica** — uma regra por
  item, cada uma verificável isoladamente — e DEVE incluir explicitamente as
  regras que **NÃO mudam** com este card. Sem isso o júnior assume que precisa
  mexer e mexe.
- **Para card do produto Órbita:** toda pista de caminho/endpoint/componente
  citada em "Caminho/rota" ou "Escopo do card" DEVE ser conferida com
  Grep/Glob/Read nos 3 repositórios **nesta mesma sessão** antes de aparecer
  no card. Nunca citar um caminho plausível sem checar. Se não encontrar
  correspondência real, escrever literalmente "Não localizado no código —
  confirmar com o time" em vez de inventar.
- **Para card do board SQO fora do produto Órbita** (ex.: Gestão de Lojas do
  Radar): não existe repositório local para conferir. Escrever "Não aplicável
  — fora dos repositórios do Órbita" em "Caminho/rota"/"Escopo do card", e
  colocar a rota de navegação informada pelo usuário em "Pontos em aberto"
  marcada como "a confirmar". **Nunca** rotear esses cards para
  `/user-stories`: ela não emite o template do board SQO.
- Toda afirmação de ausência DEVE ser qualificada como "não encontrado **nestes
  3 repositórios**" — nunca como fato sobre o produto ou a empresa inteira.
  Existe ao menos um 4º repositório do Órbita não mapeado aqui, e o Radar é
  outro produto fora de alcance.
- Todo card, antes de ser apresentado como final ao usuário, DEVE passar pelo
  subagente `(?_?) revisor-clareza-junior` (Agent tool). Se o veredito for
  "precisa de ajuste", incorporar a reescrita sugerida e reapresentar o card
  completo ajustado — nunca colar o feedback bruto do subagente como se fosse
  a entrega, e nunca marcar um card como pronto sem o veredito "pronto para o
  júnior".
- "Critérios de aceite" admite **duas formas, nunca bullets soltos**:
  - **Forma A (padrão):** Gherkin (Dado/Quando/Então) cobrindo caminho feliz +
    pelo menos um caso de borda, seguido dos 4 critérios fixos do board.
  - **Forma B:** apenas os 4 critérios fixos do board, permitida **somente**
    quando cada item de "Regras de negócio" for isoladamente verificável por
    QA. Nessa forma, a cobertura de caso de borda DEVE aparecer entre as regras
    numeradas ou em "Pontos em aberto".
  Usar a Forma A quando o card descreve comportamento observável de UI/API.
  Usar a Forma B quando a especificação verificável já são as próprias regras
  numeradas. O `(?_?) revisor-clareza-junior` checa essa escolha no Step 5.
- Rastreabilidade é obrigatória dentro da seção "Contexto", **sempre com
  localizador específico** — nome de arquivo sozinho não é rastreabilidade:
  PRD/spec → a seção; estudo → arquivo + seção; transcrição/ata → link +
  timestamps (ex.: "00:41:16 a 00:55:05"); conversa → a data. Nunca inventar
  requisito sem fonte.
- Estimativa/prioridade sem confirmação do usuário ou do PRD/spec DEVE levar
  o marcador `[DEFAULT: X — confirmar com o time]`.
- Se a fonte contiver requisitos contraditórios, declarar a contradição em
  **"Pontos em aberto"** com o trecho literal dos dois lados — nunca resolver
  em silêncio e nunca misturar com o que já está decidido em "Regras de
  negócio".
- **Efeitos de segunda ordem são obrigatórios** (Step 3B): o que a mudança
  altera FORA da tela pedida — relatórios, extrações, integrações, outros
  times, documentos, contratos. Se o raio de impacto ultrapassar o escopo
  pedido, o card declara e a resposta avisa o usuário, **sem ampliar o escopo
  por conta própria**.
- Sempre incluir o texto completo de cada card (as 7 seções inteiras) na
  resposta ao usuário. Criar o ticket no Jira ou salvar em markdown é
  adicional — nunca substitui mostrar o card completo.

## Step 0: Read Before You Write

| Fonte | Caminho | O que extrair |
|---|---|---|
| PRD/spec na conversa | mensagens anteriores desta conversa | Feature, requisitos funcionais, regras de negócio |
| **Transcrição/ata de reunião** | link do Google Docs, notas do Gemini, gravação transcrita — fornecido pelo usuário | **Fonte primária de requisito, no mesmo nível de um PRD.** Decisões fechadas, alternativas rebatidas, ambiguidades, e os timestamps de cada uma |
| **Card já existente no Jira** | `getJiraIssue` na chave citada pelo usuário (ex.: SQO-1323) | Conteúdo atual do card, para atualizar sem apagar o que já estava certo (ver Step 6B) |
| PRDs salvos | `outputs/prds/*.md` (se existir) | PRDs existentes relacionados à feature pedida |
| Specs técnicas | `outputs/claude-system-builder-runs/*/spec.md` (se existir) | Componentes, endpoints que viram cards técnicos |
| Decisões documentadas | `outputs/build-decisions-runs/*.md` (se existir) | Regras de negócio e guardrails já registrados |
| Estudos de domínio | `docs/confluence/ia/analises/*.md`, `docs/confluence/2025/evolucao-camadas/*.md` | Como o score/camadas funcionam hoje, para não contradizer na Regra de negócio |
| **Backend agente/IA** | `C:\Users\zequi\projetos\api-agent-orbita\src` (`routes/`, `controllers/`, `services/analysisAgent/`) | Endpoints reais (ex.: `POST /analysis`, `GET /layers/radius`), lógica de score (`services/analysisAgent/scoring.ts`), nomes de controller/service |
| **Backend legado** | `C:\Users\zequi\projetos\api-orbita-nodejs\src` (`controllers/`, `services/`) | Endpoints reais (ex.: `GET /available/radius` em `sourceController.js`), controllers de fonte/arquivo/agrupamento |
| **Frontend** | `C:\Users\zequi\projetos\webapp-orbita-angular\src\app\modules` | Módulos/componentes reais (ex.: `modules/analysis/pages/dashboard/components/...`), rotas Angular |
| Template oficial do card | Jira SQO-1060 (já extraído — ver Output Format abaixo, não precisa reconsultar a cada card) | As 7 seções e sua ordem exata |
| Aprendizados anteriores | `references/learnings.md` (desta skill) | Padrões de card e falhas a evitar em rodadas passadas |
| Integração de backlog | Jira MCP — checar com `ToolSearch` antes de tentar chamar | Projeto SQO - ÓRBITA, tipo de issue "História" |

**Primeira decisão do Step 0 — de qual produto é este card?**
- **Produto Órbita** → as 3 linhas de repositório acima são obrigatórias.
- **Outro produto no board SQO** (Gestão de Lojas do Radar, etc.) → pular as 3
  linhas de repositório e registrar "Não aplicável — fora dos repositórios do
  Órbita". Seguir normalmente para o Step 1. **Não** rotear para
  `/user-stories`: o card vai para o board SQO e precisa deste template.

Regra dura (card do Órbita): nunca escrever "Caminho/rota" ou uma pista de
código em "Escopo do card"/"Regras de negócio" sem ter rodado Grep/Glob real
nos 3 repositórios acima **na sessão atual**. Um caminho lembrado de uma
rodada anterior deve ser reconferido — código muda.

**Transcrição grande:** quando a transcrição não couber numa leitura só, ler
em blocos sequenciais até cobrir **100%** do conteúdo e declarar na resposta
qual porção foi lida. Nunca resumir a partir de leitura parcial sem dizer que
foi parcial. Ao ler, separar três coisas que a ata mistura: o que ficou
**decidido**, o que foi **sugerido e rebatido** (vai para "Contexto" como
alternativa descartada) e o que ficou **em aberto** (vai para "Pontos em
aberto" com o timestamp).

Só gerar cards depois de completar o Step 0. Se nenhuma fonte de PRD/spec
existir, ir para o Step 1 Caso B.

## Step 1: Localizar ou Coletar o Conteúdo da Feature

**Caso A — PRD/spec encontrado:** Extrair a feature, os requisitos
funcionais, as regras de negócio e os critérios de sucesso. Citar de qual
arquivo ou trecho da conversa cada requisito veio.

**Caso B — Nenhum PRD/spec encontrado:** Não inventar a feature. Responder:

```
Não encontrei PRD, spec, estudo nem transcrição para esta feature nesta conversa,
em outputs/prds/, outputs/claude-system-builder-runs/, nem em docs/confluence/.

Para gerar os cards no formato do Órbita preciso de uma das duas coisas:
1. Um PRD ou spec — cole aqui, ou aponte o caminho do arquivo.
2. Uma descrição da feature — em 3-5 frases: quem usa (analista de Expansão?
   time interno?), o que ela faz, e qual problema resolve.

3. Uma transcrição/ata de reunião — cole o link ou o texto; trato como fonte
   primária igual a um PRD.

Assim que eu tiver isso, gero os cards no template do board SQO (Contexto,
Referências visuais, Caminho/rota, Escopo do card, Regras de negócio, Pontos
em aberto, Critérios de aceite, Figma), conferindo caminhos de código reais
nos 3 repositórios quando o card for do produto Órbita, e revisando cada card
com o subagente de clareza júnior antes de entregar.
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

**Aplica-se apenas a card do produto Órbita.** Para card do board SQO de outro
produto, pular este Step inteiro e escrever "Não aplicável — fora dos
repositórios do Órbita" em "Caminho/rota" e "Escopo do card", levando a rota
informada pelo usuário para "Pontos em aberto" como "a confirmar".

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

## Step 3B: Mapear Efeitos de Segunda Ordem (obrigatório)

Antes de redigir, responder as quatro perguntas abaixo **por escrito**. O que
tiver resposta entra no card; o que ultrapassar o escopo pedido vai também na
resposta ao usuário como aviso.

1. **Quem mais consome esse dado ou essa tela?** Relatório, extração, API
   pública, integração com parceiro, post automático, planilha de outro time.
2. **O que deixa de ser verdade em outro ponto do sistema se isso mudar?**
   Especialmente: o **momento** em que um dado passa a valer muda junto?
3. **Qual contagem, total ou indicador se altera?** Número de lojas, de
   análises, de pontos — números que alguém divulga.
4. **Alguém fora do time do card precisa ser avisado?** Jurídico, financeiro,
   sucesso do associado, parceiro externo.

Registrar o resultado no "Escopo do card" (quando for trabalho a fazer) ou em
"Pontos em aberto" (quando for impacto a confirmar). **Nunca ampliar o escopo
por conta própria** — declarar o impacto e deixar a decisão com quem pediu.

Exemplo real (SQO-1323): mudar o momento em que o modal de situação dispara
também muda o momento em que a bandeira vigente é gravada no cadastro, logo
relatórios e contagens por bandeira passam a mostrar a bandeira antiga durante
todo o período da situação. Isso não foi pedido, mas é consequência direta e
entrou no card.

## Step 4: Escrever Cada Card no Template Jira SQO

Usar exatamente este formato — extraído do template oficial (SQO-1060):

```
### [Componente] [Ação] [Sujeito]

**Contexto:**
[Os três, nesta ordem:
(a) COMPORTAMENTO ATUAL — o que o sistema faz hoje;
(b) POR QUE ESTÁ ERRADO — a premissa que não se sustenta;
(c) IMPACTO DE NEGÓCIO — o que quebra concretamente se ficar como está.
Tudo em linguagem que alguém sem conhecimento prévio do domínio entenda. Se o
card depende de um termo de domínio (score de viabilidade, camada, raio de
análise, situação de loja), definir em uma frase.]

[ALTERNATIVAS DESCARTADAS — incluir quando a fonte mostrar algo que foi
sugerido e rebatido: "X foi sugerido e descartado porque Y". Omitir a seção
se não houve nenhuma.]

Rastreabilidade: [localizador específico — seção do PRD/spec; arquivo + seção
do estudo; link + timestamps da transcrição (ex.: "00:41:16 a 00:55:05"); ou
"descrito verbalmente em 2026-09-17"]

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
1. [Uma regra por item, atômica e verificável isoladamente, explicada com o
   "porquê" e não só o "o quê".]
2. [...]
N. [O QUE NÃO MUDA — pelo menos um item declarando o comportamento vizinho
   que permanece como está, ex.: "Montagem → Ativa continua exigindo data de
   inauguração; não muda com este card". Sem isso o júnior mexe no que não
   devia.]

**Pontos em aberto:**
- [Toda ambiguidade, contradição ou lacuna da fonte, **citando o trecho
  literal** e o localizador. Ex.: "Na transcrição (00:55:05) foi dito 'se eu
  vier para transição de CNPJ, ele já me pede o CNPJ novo direto', o que
  contradiz a regra 3. Confirmar qual vale."]
- [Campo herdado de template de outra feature — marcar "confirmar/substituir",
  nunca propagar em silêncio.]
- [Impacto de segunda ordem a confirmar, vindo do Step 3B.]
- [Se não houver nenhum: escrever literalmente "Nenhum".]

**Critérios de aceite:**
[Forma A — padrão, quando o card descreve comportamento observável de UI/API:]
- Dado [contexto], quando [ação], então [resultado esperado]
- Dado [contexto de borda], quando [ação], então [resultado esperado]
[Forma B — só os 4 fixos abaixo, quando cada item de "Regras de negócio" já é
isoladamente verificável por QA e a borda aparece entre as regras numeradas.]
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
   caminhos de código já verificados no Step 3. Pedir explicitamente que ele
   cheque, além da clareza: (a) se "Contexto" traz comportamento atual + por
   que está errado + impacto de negócio; (b) se as regras estão numeradas e
   atômicas e se há ao menos uma dizendo o que NÃO muda; (c) se "Pontos em
   aberto" está preenchido ou marcado "Nenhum"; (d) se a escolha entre Forma A
   e Forma B dos critérios de aceite se sustenta.
   Se o card for de produto fora do Órbita, avisar o subagente de que não há
   repositório para conferir — ele não deve cobrar pista de código nesse caso.
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

## Step 6B: Atualizar um Card que Já Existe

Quando o usuário apontar uma chave existente (ex.: "atualiza o SQO-1323"):

1. **Ler o card atual primeiro** (`getJiraIssue`). Nunca escrever por cima sem
   ter lido o que está lá.
2. Preservar o que já estava correto. Não apagar campo preenchido por outra
   pessoa sem avisar o usuário na resposta.
3. **Campos herdados de template** — um card novo costuma vir com
   "Caminho/rota" e "Figma" copiados de outra feature. Nunca propagar em
   silêncio: conferir e, se não bater com esta feature, levar para "Pontos em
   aberto" como "confirmar/substituir". Precedência real: o SQO-1279 foi ao ar
   com a frase-padrão "Radar → ícone de 4 quadradinhos → Órbita → Órbita IA"
   sem checagem, e a tela não existia; o SQO-1323 chegou com rota de Órbita IA
   e Figma do Órbita sendo card de Gestão de Lojas do Radar.
4. Na resposta, dizer o que foi **alterado**, o que foi **mantido** e o que
   ficou em "Pontos em aberto".

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

## Worked Example 2 — Transcrição como fonte, produto fora do Órbita (SQO-1323)

Caso real. Mostra **só as seções que diferenciam** deste exemplo o anterior —
as demais seguem o mesmo template.

**Input:** "Leia essa transcrição [link do Google Docs] e atualize o card
SQO-1323 com as alterações na parte de troca de situação de loja."

**Step 0:** Gestão de Lojas do Radar → board SQO, **fora do produto Órbita**
→ Step 3 pulado. Transcrição de 84 mil caracteres lida em blocos até 100%;
porção lida declarada na resposta. Card existente lido com `getJiraIssue`
antes de escrever (Step 6B).

**Step 3B — efeitos de segunda ordem:** mudar o momento do modal muda o
momento em que a bandeira vigente é gravada → relatórios e contagem por
bandeira passam a mostrar a bandeira antiga durante toda a situação. Não foi
pedido; entrou no Escopo e foi avisado ao usuário.

```
**Contexto:**
Hoje o modal de campos obrigatórios dispara ao ENTRAR na situação: ao
selecionar "Mudança de bandeira", o sistema já pede a bandeira nova e grava no
cadastro. Isso está errado porque a loja entra na situação quando o processo
começa — ela ainda não mudou de bandeira. Gravar nesse momento tira a loja de
uma bandeira e põe em outra nos relatórios e na postagem do Bitrix antes da
reinauguração; se o associado desistir, o número é mexido duas vezes.
"Situação" é o subestado de uma loja com status Ativa.

Alternativas descartadas: foi sugerido remover o modal por ser burocrático.
Descartado porque o modal existe contra o esquecimento humano, que já quebrou
o número de lojas antes.

Rastreabilidade: transcrição "Mudanças Gestão de Lojas - Radar" (16/10/2026),
https://docs.google.com/document/d/.../edit — 00:41:16 a 00:55:05.

**Caminho/rota:**
Radar → Gestão de Lojas → ficha da loja → Informações gerais → campo Situação.
Não aplicável — fora dos repositórios do Órbita (rota informada pelo usuário,
não verificada em código; ver Pontos em aberto).

**Regras de negócio:**
1. Situação só se aplica a loja com status Ativa. Em Montagem ou Desativada,
   trocar a situação não dispara modal algum.
2. O modal deixa de disparar ao ENTRAR em uma situação.
3. O modal passa a disparar ao SAIR da situação atual para qualquer outra.
4. Os campos exigidos são os da situação de ORIGEM, a que está sendo encerrada.
5. Quando o destino for "Loja ativa", exigir também a data de reinauguração.
6. A gravação no cadastro só ocorre na confirmação do modal de saída — durante
   a situação, relatórios e contagens mantêm a bandeira antiga.
7. Montagem → Ativa continua exigindo data de inauguração. **Não muda com
   este card.**

**Pontos em aberto:**
- Transição de CNPJ: em 00:55:05 foi dito "se eu vier para transição de CNPJ,
  ele já me pede o CNPJ novo direto", o que contradiz a regra 3. Confirmar se
  é exceção ou se foi descrição da tela atual.
- Saída por troca de status (Ativa → Desativada estando em "Mudança de
  bandeira"): não discutido na reunião.
- Caminho/rota e Figma do card vieram do template apontando para Órbita IA e
  para o Handoff do Órbita — **confirmar/substituir**, este card é de Gestão
  de Lojas do Radar.

**Critérios de aceite:** [Forma B — as 7 regras acima são isoladamente
verificáveis por QA e a borda está coberta pelas regras 1 e 7]
- Não se pode fugir da seção Escopo do card
- Estar em conformidade com as regras de negócio
- Passar nos testes definidos por QA
- Estar em conformidade com o Figma
```

## Out of Scope

Esta skill NÃO faz:
- Cards que **não vão para o board SQO** → use `/user-stories`. Card de outro
  produto da Farmarcas que vai para o board SQO (Gestão de Lojas do Radar,
  etc.) **é escopo desta skill** — ver Step 0 e Step 3
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
- Se o card for de outro produto no board SQO (fora dos 3 repositórios do
  Órbita) → **continuar nesta skill**, pulando o Step 3 e declarando "Não
  aplicável — fora dos repositórios do Órbita". Não rotear para
  `/user-stories`: ela emite Gherkin solto, fora do template que o board exige
- Se o card não vai para o board SQO → aí sim recomendar `/user-stories`

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
| "A fonte é ambígua nesse ponto, vou escrever a interpretação mais provável como regra" | Interpretação provável escrita em "Regras de negócio" vira fato para quem implementa. Ambiguidade vai para "Pontos em aberto" com o trecho literal — sempre. |
| "O impacto em relatório/outro time não foi pedido, está fora do escopo do card" | O Step 3B é obrigatório. Declarar o efeito de segunda ordem não é ampliar escopo — esconder é que entrega um card que quebra outra coisa em silêncio. |
| "O card já vinha com Caminho/rota e Figma preenchidos, deixo como está" | Card novo herda campo de template de outra feature. Já aconteceu no SQO-1279 e no SQO-1323. Conferir e, se não bater, mandar para "Pontos em aberto". |
| "Escrevo as regras em parágrafo corrido, fica mais natural de ler" | Parágrafo esconde quantas regras existem e torna cada uma não-verificável isoladamente. Lista numerada e atômica — sempre, inclusive a que diz o que NÃO muda. |
| "A transcrição é enorme, leio o resumo do Gemini e os trechos que parecem relevantes" | O resumo perde a alternativa rebatida e a contradição — exatamente o que alimenta "Contexto" e "Pontos em aberto". Ler 100% em blocos e declarar a porção lida. |
| "Essa feature não é do Órbita, mando pra /user-stories" | Se o card vai para o board SQO, `/user-stories` entrega o template errado. Continuar aqui, pulando o Step 3. |

## Before Marking Complete

- [ ] Step 0 executado — fontes de PRD/spec E os 3 repositórios de código
      foram lidos/grepados nesta sessão (listar quais)
- [ ] Se nenhuma fonte de PRD/spec existia, o Step 1 Caso B foi usado
- [ ] Foi decidido no Step 0 se o card é do produto Órbita ou de outro produto
      do board SQO, e o Step 3 foi aplicado ou pulado conforme essa decisão
- [ ] Todo card segue as 8 seções exatas do template SQO, na ordem certa
- [ ] "Contexto" traz comportamento atual + por que está errado + impacto de
      negócio, e registra alternativa descartada quando a fonte mostrou uma
- [ ] "Regras de negócio" está numerada e atômica, com ao menos um item
      declarando o que NÃO muda com o card
- [ ] "Pontos em aberto" está preenchido citando o trecho literal da fonte, ou
      marcado literalmente "Nenhum"
- [ ] Step 3B executado: as 4 perguntas de efeito de segunda ordem foram
      respondidas, e o que ultrapassa o escopo pedido foi avisado ao usuário
- [ ] Rastreabilidade usa localizador específico (seção, timestamps, data) —
      não só o nome do arquivo
- [ ] Se a fonte foi transcrição longa, 100% foi lido e a porção lida foi
      declarada na resposta
- [ ] Se o card já existia no Jira, foi lido antes de escrever e campos
      herdados de template foram conferidos (Step 6B)
- [ ] Para card do Órbita: toda pista de caminho/endpoint foi confirmada nos
      repositórios (ou marcada "não localizado"), e toda afirmação de ausência
      foi qualificada como "nestes 3 repositórios"
- [ ] Para card fora do Órbita: "Não aplicável — fora dos repositórios do
      Órbita" foi escrito, e nenhum caminho de código foi inventado
- [ ] Critérios de aceite usam Forma A (Gherkin + 4 fixos) ou Forma B (4 fixos
      com regras numeradas verificáveis), e a escolha se sustenta
- [ ] Toda estimativa/prioridade sem confirmação carrega `[DEFAULT: X —
      confirmar com o time]`
- [ ] Contradições da fonte foram declaradas em "Pontos em aberto", não
      resolvidas em silêncio nem escondidas em "Regras de negócio"
- [ ] Todo card foi revisado pelo subagente `(?_?) revisor-clareza-junior` e
      só aparece na resposta final com veredito "pronto para o júnior"
- [ ] O texto completo de cada card apareceu na resposta ao usuário
- [ ] Se Jira MCP estava conectado, os tickets foram criados no projeto SQO;
      se não, o caminho do markdown salvo aparece

## After Completing: Log Learning

Anexar a `references/learnings.md`:
Date / O que funcionou / O que não funcionou / Caso de borda / Quantas
rodadas o revisor-clareza-junior pediu até aprovar
