# Cards — Zoneamento no Órbita

**Fonte:** Confluence "Zoneamento no Órbita (em construção)", espaço SR, página
4545904644, **v14 de 2026-11-18** ("Remove a regra de indicador de zoneamento
verificado"), lida integralmente nesta sessão.
**Fonte de apoio:** `outputs/regras-negocio-zoneamento-orbita.md` (rascunho v3 de
2026-11-17) — usada para rastreabilidade e para alimentar "Pontos em aberto";
onde as duas divergem, **vale a página do Confluence**, que é posterior.
**Épico:** SQO-1331 — "Evitar erros de zoneamento pelo Órbita".
**Data de geração:** 2026-11-23. **Revisado** pelo subagente de clareza júnior
em 2026-11-23 (5 revisões, 1 rodada, todas as correções de código reconferidas
manualmente antes de incorporar).

> **ATUALIZAÇÃO 2026-11-24 — o que foi efetivamente publicado no Jira.**
> Os 12 cards deste documento foram para o board SQO em **versão ENXUTA**, no
> formato puro do template SQO-1060 (Contexto, Referências visuais, Caminho/rota,
> Escopo do card, Regras de negócio, Critérios de aceite, Figma), por decisão do
> PM em 2026-11-24. O que **não** foi para o Jira: a seção "Pontos em aberto"
> como seção própria, o glossário por card, e as pistas de `arquivo:linha`.
> As lacunas **bloqueantes de estimativa** foram dobradas dentro de
> "Escopo do card"/"Regras de negócio" ou num bloco curto de
> "Pendências de negócio" ao final de cada card.
> O glossário virou página única no Confluence:
> https://farmarcas.atlassian.net/wiki/spaces/SR/pages/4555636743
> **O revisor-clareza-junior NÃO foi executado nesta rodada, por ordem explícita
> do usuário.** Os vereditos "pronto para o júnior" registrados abaixo são da
> rodada de 2026-11-23, sobre a versão longa — não sobre o texto publicado.
> Este documento continua sendo o **arquivo da versão longa**, com todo o
> detalhe de código que não cabe no board.

**Pistas de código conferidas em 2026-11-23** contra os clones locais:
`api-agent-orbita` @ `3ca2381` (2026-10-27), `api-orbita-nodejs` @ `3730a4c`
(2026-10-14), `webapp-orbita-angular` @ `733e887` (**2024-05-09**).

> ⚠️ **AVISO QUE VALE PARA TODO CARD DE FRONT-END (Z6, Z7, Z9).** O clone local
> do `webapp-orbita-angular` está em `main` @ `733e887`, de **2024-05-09**, e
> **nenhuma branch remota é mais nova que isso** (`git for-each-ref` sobre
> `refs/remotes`: a mais recente é `origin/main`, 2024-05-09; o último `fetch`
> foi em 2026-11-09). Os dois backends receberam commit em outubro de 2026. Ou
> o front do Órbita não muda há ~18 meses, ou **o desenvolvimento do front
> migrou para outro repositório** — possivelmente o mesmo 4º repositório onde
> vive a tela do Órbita IA. **Isto não foi confirmado.** Antes de qualquer card
> de front entrar em sprint, confirmar com o time qual é o repositório do front
> em produção: se não for este, **toda** pista de front destes cards aponta para
> código que ninguém mais mexe.

> ⚠️ **Número de linha é a parte mais perecível do card.** Ao desenvolver, abrir
> o arquivo e localizar pelo **nome do símbolo** (`analysisIsInvalid`,
> `onSubmit`, `getWarnings`, `findMunicipalIndicators`), não pela linha.

## Glossário mínimo (vale para todos os cards)

| Termo | O que é |
|---|---|
| **Zoneamento** | Conjunto de regras da Farmarcas que decide se um endereço **pode** receber uma loja nova. É **gate**, não nota: ou barra, ou avisa, ou libera. Não confundir com o score de viabilidade 0–20, que mede se o ponto é bom. |
| **Radar** | Outro produto da Farmarcas, onde fica o **cadastro oficial de lojas**. O Órbita hoje não tem esse cadastro. |
| **Carga D-1** | Cópia diária do cadastro do Radar para o Órbita, com os dados de ontem. |
| **Defasagem (da carga)** | Quanto tempo passou desde a última carga bem-sucedida. "Limite de defasagem" é o máximo tolerado antes de o resultado virar `indeterminado`. |
| **Grupo econômico (GE)** | O "dono" de um conjunto de lojas. É a unidade que o teto da cidade conta — não a loja. ⚠️ **Não confundir com o `scoreGroup` do código** (`api-agent-orbita/src/services/analysisAgent/economicClass.ts:3`), que o prompt da IA também chama de "Grupo econômico" (`analysisAgent/prompt.ts:86`) mas significa **faixa de classe socioeconômica** (`A++/A+`, `B1/B2`, `C1/C2`, `D/E`) usada no score. São coisas diferentes. |
| **Teto** | Número máximo de grupos econômicos que podem operar num mesmo município, definido pela faixa de população. Atingido o teto, a cidade está "fechada" **para grupo novo** — mas não para loja nova de quem já está lá. |
| **Faixa de população** | Recorte do município por habitantes que define o teto: até 60.000 / 60.001–120.000 / 120.001–200.000 / acima de 200.000. Cortes **fechados** (60.000 cai na 1ª faixa, 60.001 na 2ª). Definida no Z3 regra 3. |
| **2º grupo da cidade** | O grupo cujo pedido **soma um grupo novo** ao município **e** que entra quando já há exatamente 1 grupo ocupando vaga. **Não é "a 2ª loja"**: a 5ª loja de quem já está na praça continua sendo o 1º grupo. |
| **Ocupar vaga** | Contar para o teto do município. |
| **Status da loja** | `Ativado` = em operação; `Montando` = contratada, em implantação; `Transição` = em troca de dono ou bandeira, ainda operando; `Desativado` = encerrada. Os três primeiros ocupam vaga; o último não. ⚠️ O rascunho de regras marca `Montando` e `Transição` como **"a definir"** — ver Z1, Pontos em aberto. |
| **Distrato** | Encerramento do contrato por acordo entre as partes depois de ele já estar valendo. Para o teto, efeito prático igual ao do cancelamento: o ponto deixa de ocupar vaga. **Não existe como status no modelo atual** — ver Z3, Pontos em aberto. |
| **Bandeira** | A marca sob a qual a loja opera. Nestes cards é sempre **bandeira Farmarcas**, vinda do cadastro de lojas (Z1) ou do `BrandService`. ⚠️ **Não é** o campo `BANDEIRA` da camada Concorrentes (`api-agent-orbita/src/services/radiusSearch/aggregations/competitiveMap.ts:19-29`), que é só uma das chaves para extrair o **nome de um concorrente** — e que não prova que a loja é nossa. |
| **Modelo de negócio** | `Popular` ou `Convencional` — classificação de negócio de uma bandeira Farmarcas. ⚠️ **Esse dado não existe em nenhum contrato do produto hoje:** `BrandModel` tem só `id`, `name` e `assets` (`webapp-orbita-angular/src/app/shared/models/brand.model.ts`), e não há campo de modelo no formulário de análise. **Não confundir com "Tipo de Loja"** (`AnalysisStoreType` = `Nova`/`Conversão`/`Mudança de Ponto`, `shared/models/analysis.model.ts:16-27`), que já existe na tela e é outra coisa. |
| **Endereço da Receita** | Endereço fiscal da loja, com coordenada própria. |
| **Endereço popular** | Endereço onde a loja de fato opera, com coordenada própria. **Pode divergir** do fiscal. |
| **Camada** | Uma fonte/tipo de informação que o Órbita coleta sobre uma área (renda, faixa etária, concorrência). No mapa, é o que o analista liga e desliga. |
| **Camada Concorrentes** | A camada que lista farmácias concorrentes num raio. Traz **nome de bandeira** — inclusive bandeiras Farmarcas —, mas nome de bandeira ali **não prova** que a loja é nossa. |
| **Raio de análise** | O círculo que o analista desenha no mapa para estudar uma região: 300 m a 6.500 m em passos de 100 m, mais três valores-sentinela que **não são metros** (6600 = "Município", 6700 = "Mesoregião", 6800 = "Estado"). **Não tem relação** com os 300/500 m da distância mínima do zoneamento. |
| **Veredito** | O resultado do zoneamento para um ponto, num formato único usado pelas três telas (Z5). Ver a tabela dos **quatro resultados** abaixo. |
| **Lacuna declarada** | Dado que faltou e que o veredito **diz** que faltou, em vez de omitir. Ex.: loja vizinha sem coordenada não vira "não violou" — vira "não checada". |
| **Solicitante** | Quem pede a análise: empresário novo ou empresário que já opera loja Farmarcas. |
| **Órbita IA** | Caminho alternativo do produto em que a análise é montada de uma vez por um agente, sem o analista percorrer mapa → carregar ponto → salvar. A **tela** não está nos 3 repositórios clonados; o **motor** está (`api-agent-orbita`, `POST /analysis`). |
| **Triagem (validação 1)** | Checagem barata que roda ao carregar o ponto no mapa (Z6), com limiar único de 300 m, só para evitar gastar análise cara num ponto que a regra barra. **Não é a regra final:** a final aplica 300/500 m conforme a bandeira (Z2). |

### Os quatro resultados do veredito (contrato único — detalhado no Z5)

| Resultado | Quando sai | O que significa para o analista |
|---|---|---|
| `impedimento` | Alguma regra foi **ferida** | A regra barra o ponto. Não é "atenção": é "não pode" |
| `alerta` | Nenhuma regra ferida, mas há pelo menos um **aviso** | Pode seguir; há um fato a considerar. **`alerta` e "aviso" são a mesma coisa** — `alerta` é o valor no contrato, "aviso" é a palavra em tela |
| `indeterminado` | Faltou dado, ou a checagem não concluiu | A regra **não foi aplicada**. **Nunca** ler como liberação |
| `liberado` | Tudo que se aplicava rodou e nada feriu nem avisou | O ponto passa no zoneamento |

Uma regra que **não se aplica** àquele pedido (ex.: bandeira/modelo num município
de 40 mil habitantes) **não é** `indeterminado`: ela simplesmente não entra.
No nível de cada regra, a saída é `fere` / `avisa` / `nao_avaliada` /
`sem_apontamento`; o Z5 traduz isso para os quatro resultados acima.

## Mapa dos cards

| Épico | Card | Título | Depende de | Jira |
|---|---|---|---|---|
| A — Fundação de dado | **Z1** | [Dados] Camada de lojas do Radar no Órbita | — | **SQO-1333** (existente) |
| A | **Z1b** | [Dados] Rotina de carga diária D-1 da camada de lojas | Z1 | **SQO-1336** (existente) |
| B — Motor de zoneamento | **Z2** | [API] Checagem de distância mínima entre lojas Farmarcas | Z1, Z3 | **SQO-1384** |
| B | **Z3** | [API] Teto de grupos econômicos por município | Z1 | **SQO-1385** |
| B | **Z4** | [API] Regra de bandeira e modelo de negócio por faixa | Z1, Z3 | **SQO-1386** |
| B | **Z5** | [API] Veredito de zoneamento com motivo e rastreabilidade | Z2, Z3, Z4 | **SQO-1387** |
| C — Disparo na interface | **Z6** | [Mapa] Modal de zoneamento ao carregar o ponto | Z2, Z5 | **SQO-1334** (existente) |
| C | **Z7** | [Análise] Aviso de zoneamento ao salvar a análise | Z5 | **SQO-1388** |
| C | **Z8** | [Órbita IA] Modal de zoneamento na tela final da IA | Z2, Z3, Z5 | **SQO-1335** (existente) |
| C | **Z9** | [Análise] Perfil do solicitante obrigatório no início | — (efeito: Z5) | **SQO-1389** |
| C | **Z10** | [Análise] Registro do veredito junto da análise | Z5, Z7, Z8 | **SQO-1390** |

Fora deste conjunto, o épico tem ainda **SQO-1337** ("Dar opção de ajuste do pin
lat e long da loja no Radar"), que é o **pré-requisito de geocodificação** citado
no Z1 — não é um dos 11 cards acima, mas destrava a cobertura de coordenada de
que Z2 depende.

## O que foi conferido no código nesta sessão (Step 3)

### Confirmado (arquivo:linha)

**Fluxo do mapa e o "warnings" que já existe:**
- `POST /sources/search/warnings` — `api-orbita-nodejs/src/controllers/sourceController.js:96`,
  implementado em `src/services/searchService.js:556` (`exports.getWarnings`).
  Devolve **apenas** `{ hasAnalysis: boolean }` (`:566`).
- `const ANALYSIS_RADIUS_SEARCH = 300` — `api-orbita-nodejs/src/services/searchService.js:10`.
  É o 300 m que já existe, usado para **análises próximas**, não para lojas.
- **O serviço ignora qualquer raio enviado:** sobrescreve `search.range = ANALYSIS_RADIUS_SEARCH`
  (`searchService.js:560`). E o cliente nem envia raio — manda só
  `{ latitude, longitude }` no corpo e `?analysisId` na query
  (`webapp-orbita-angular/src/app/shared/services/source.service.ts:91-106`,
  contra `apiBase`). **Sem bandeira, sem município, sem solicitante.**
- Consumidor no front: `checkNearbyAnalysis()` —
  `webapp-orbita-angular/src/app/modules/view/view.component.ts:343`, chamado no
  `ngOnInit` (`:168`) e a cada mudança de `main`/`radius` (`:169-171`). Renderiza
  **toast** (`ToastrService.warning`, `:360-364`) e, em falha, um **segundo toast
  de erro** (`:367-373`) — precedente de "falha não vira silêncio".
- ⚠️ **Guard de saída antecipada:** `checkNearbyAnalysis()` retorna antes de
  chamar a API quando `!map.radiusEnabled` (`view.component.ts:347-353`), e
  `radiusEnabled` é um botão do analista (inicia `true`,
  `shared/models/map.model.ts:88`). O mesmo trecho testa `location.lat` **duas
  vezes** e **nunca testa `lng`** (bug pré-existente).
- `SearchWarningsResponse { hasAnalysis: boolean }` —
  `webapp-orbita-angular/src/app/shared/models/source.model.ts:394-396`.
- Slider de raio: `RANGE_STEP` `:29`, `RANGE_MIN = 300` `:30`, `RANGE_MAX = 6800`
  `:31`, `RANGE_CUSTOM = [6600,6700,6800]` `:33`, `RANGE_CUSTOM_NAME` `:34-38`,
  `RANGE_FREE_MAX` `:43`, `radiusLabel()` `:225-226` — todos em
  `modules/view/view.component.ts`. **6600/6700/6800 não são metros.**
- **Duas entradas chegam em `/view`:** (1) a home navega ao receber um endereço
  escolhido na busca — `onExplore()` seta `map.main` e chama
  `this._router.navigate(['/view'])` (`modules/common/pages/home/home.component.ts:42`);
  (2) "recuperar o mapa" de uma análise existente, que seta `map.analysisId`
  (`modules/analysis/pages/create/components/historic/historic.component.ts:109`)
  antes de navegar (`:118`). A rota `view` está em `app.routes.ts:37`, **fora** do
  `CommonNavigationComponent` — por isso o mapa abre sem menu lateral e não
  aparece nele (itens em `modules/common/components/navigation/navigation.component.ts:57-113`).
- Precedente de **modal** no próprio módulo do mapa: `AuroraModalService` +
  `<rds-modal id="...">` — `modules/view/components/map/map.component.html:27`
  (`id="placeUpdate"`), aberto em `map.component.ts:726`, serviço injetado em
  `map.component.ts:91`. ⚠️ `modules/view/view.component.ts` **não injeta** hoje
  nenhum serviço de modal — só `ToastrService` (`:143`) e `AnalysisModalService`
  (`:148`).

**Fluxo de salvar a análise:**
- `AnalysisService.create()` — `shared/services/analysis.service.ts:71` →
  `POST ${apiExpansion}/analysis`; `update()` — `:79` →
  `PUT ${apiExpansion}/analysis/${analysis.id}`; leitura em
  `GET ${apiExpansion}/analysis/detail/${analysisId}` — `:65`.
  `apiExpansion = environment.api.expansion` (`core/http/http.base.service.ts:9`).
- Ponto de entrada: `AnalysisViewComponent.onSubmit()` —
  `modules/analysis/pages/view/view.component.ts:204`. ⚠️ **O padrão
  "modal antes de concluir" funciona por reentrância com UM booleano:**
  `onSubmit(confirm = false)` abre o modal e dá `return` (`:219-228`); o botão do
  modal chama **`onSubmit(true)`** (`pages/view/view.component.html:116` e `:136`),
  e a 2ª passagem pula o bloco de contrato (`:229-232`) e segue para
  `createAnalysis()`/`updateAnalysis()` (`:235-239`). O botão "Salvar análise"
  chama `onSubmit()` (`view.component.html:146`, com
  `[disabled]="loading || analysisIsInvalid()"`).
- `analysisIsInvalid()` — `modules/analysis/pages/view/view.component.ts:347-353`:
  inválido só quando `isAPointAnalysis() && !lead && !map.main.id`, ou seja,
  **análise de Ponto com `lead` e sem ponto no mapa é salvável hoje**.
- `loading` só é setado dentro de `createAnalysis()`/`updateAnalysis()` (`:243`,
  `:273`) — **durante uma consulta anterior ao salvamento o botão continua
  clicável**.
- **Três caminhos chegam no mesmo `onSubmit()`:** a rota `/analysis/create` e
  `/analysis/view/:analysisId` (`modules/analysis/analysis.routes.ts:15-22`); o
  formulário aberto como **modal do mapa** via `AnalysisModalService.open()`
  (`modules/view/view.component.ts:299`, dentro de `saveAnalysis(type)` `:288`);
  e o **rascunho**, com `MapModel` vazio — `saveDraftAnalysis()`
  (`modules/view/view.component.ts:221-225`) e o atalho do menu lateral
  (`modules/common/components/navigation/navigation.component.ts:50-54`).
- Toda a rota `/analysis` exige a permissão **`ManagamentAnalysis`** no produto
  ORBITA (`app.routes.ts:62-72`) — **a string no código tem esse erro de
  digitação**; é por ela que se procura. `/view` exige `AccessOrbita`
  (`app.routes.ts:20-34`).
- `Analysis.isAssociated?: boolean` — `shared/models/analysis.model.ts:121`;
  select "Associado Farmarcas" em `modules/analysis/pages/view/view.component.html:46-47`
  (`[disabled]="!editable"`), opções em `pages/view/view.component.ts:76-85`.
  ⚠️ A lista de análises imprime
  `{{analysis.isAssociated ? 'ASSOCIADO' : 'NOVO EMPRESÁRIO'}}`
  (`modules/analysis/pages/list/list.component.html:120`) — **hoje toda análise
  com o campo vazio aparece como "NOVO EMPRESÁRIO"**.
- `AnalysisSituation` com 9 valores — `shared/models/analysis.model.ts:52-62`;
  `APPROVED = 4` (`:58`). `AnalysisStatus` — `:82-89`.
- `ContractStatus` = `NOT_STARTED | STARTED | CANCELED` — `:167-171`.
  **Não há status de distrato.**
- `AnalysisType` = `CITY = 0` ("Território") / `POINT = 1` ("Ponto") — `:6-14`.
  O mapa oferece os dois no mesmo fluxo de salvar
  (`modules/view/view.component.html:79` e `:84`, ambos chamando `saveAnalysis()`).
- `Analysis.brand?: number` — `:116` (bandeira é **id numérico**, não texto).
  Lista em `BrandService.getBrands()` (`shared/services/brand.service.ts:15`),
  servida por `${apiCommon}/brand/all` (`:25`, com
  `apiCommon = environment.api.common`, `core/http/http.base.service.ts:10`) —
  **uma quarta API**, fora destes 3 repositórios. Consumida em
  `modules/analysis/pages/view/view.component.ts:175` (`loadBrands()`, `:172-179`,
  chamada no `ngOnInit` `:123`), exibida no select "Bandeira"
  (`pages/view/view.component.html:39`).
- `BrandModel` = `{ id, name, assets }` —
  `shared/models/brand.model.ts`. **Sem campo de modelo de negócio:** não dá para
  derivar `Popular`/`Convencional` da bandeira com o contrato atual.

**Bases e precedentes de backend:**
- Base interna de população: fonte `"População MM 2023"`
  (`SOURCE_NAMES.MUNICIPAL_POPULATION`, `api-agent-orbita/src/constants/collections.ts:14`),
  buscada por `properties.CODMUNIC` (`:27`), **valor em `properties.Populacao2023`**.
  Município resolvido por `$geoIntersects` em `findMunicipality()`
  (`src/services/radiusSearch/aggregations/cityInfluence.ts:12`, **não exportada**),
  pelo campo `properties.CD_MUN` (`collections.ts:21`), convertido para string
  (`cityInfluence.ts:50`). Leitor pronto: `findMunicipalIndicators()`
  (`cityInfluence.ts:40`), que retorna `null` quando não acha município (`:48`).
- 🪤 **ARMADILHA CONFIRMADA:** `findMunicipalIndicators()` devolve
  `population: Number(population?.properties?.Populacao2023 ?? 0)`
  (`cityInfluence.ts:77`). **Município sem população na base vira 0 habitantes**,
  que cai na faixa "até 60.000" e produz **teto 1 grupo** — um veredito
  plausível, restritivo e **falso**, em vez do `indeterminado` que o Z3 exige.
  Como é o único leitor de população do produto, é o que será reusado por
  reflexo, e o bug não aparece em teste.
- **Molde para a checagem de distância (Z2):** `aggregateCompetitiveMapStores()`
  — `api-agent-orbita/src/services/radiusSearch/aggregations/competitiveMap.ts:47`:
  filtra por `geometry: { $geoWithin: { $geometry: searchAreaGeometry } }`
  (`:58-62`), calcula metros com `@turf/distance` (`import distance from "@turf/distance"`,
  `:1`) em `distanceMeters: Math.round(distance(center, point([longitude, latitude]), { units: "meters" }))`
  (`:115-116`), e ordena por distância crescente. Alternativa em Mongo puro:
  `$geoWithin: { $centerSphere: [[lng, lat], range / EARTH_RADIUS] }` com
  `EARTH_RADIUS = 6378100.0` (`api-orbita-nodejs/src/services/searchService.js:6, :62`).
- **Como dado externo entra hoje no Órbita:** `createDataSource()` —
  `api-orbita-nodejs/src/services/sourceService.js:189` grava a configuração da
  fonte na coleção `sources` (`:223`), com
  `config.structure.name = config.name.trim()` (`:218`) apontando para a coleção
  física; o processamento é delegado a uma **Lambda**
  (`AWS_EXCEL_FILE_FUNCTION` `:193`, `AWS_SHAPEL_FILE_FUNCTION` `:195`), que
  **não está nestes 3 repositórios**. Porta de entrada: `POST /imports/:type`
  (`src/controllers/fileController.js:10`), hoje **upload manual de arquivo**.
- Coleção de análises como fonte do mapa: `sources` com
  `structure.name === 'analysis_data'` — `api-orbita-nodejs/src/services/searchService.js:558`.
- Primitiva de busca por raio: `searchService.getLocation({ dataSources, latitude, longitude, range })`
  (`api-orbita-nodejs/src/services/searchService.js:16`). ⚠️ O embrulho
  `sourceService.getAllRadius()` (`sourceService.js:38`) devolve **só os ids das
  fontes com resultado**, não os registros — não serve como está para o Z2.
- **O motor da análise por IA ESTÁ aqui:** `api-agent-orbita` expõe
  `POST /analysis` (`src/routes/analysis.routes.ts:7` →
  `src/controllers/analysis.controller.ts:5` → `analyzeViability()` em
  `src/services/analysisAgent/index.ts:26`), que devolve `viabilityScore`,
  `status`, `classification`, `pros`, `cons` (`index.ts:40-49`) e **não persiste
  nada** — é stateless. O que está fora destes 3 repositórios é a **tela**.
- 🪤 **Não existe agendador em nenhum dos dois backends.**
  `grep -rniE "cron|node-schedule|agenda|setInterval|scheduler"` em
  `api-orbita-nodejs/src`, `api-agent-orbita/src` e nos dois `package.json` →
  **zero ocorrências**. "Carga diária" (Z1b) não tem hoje onde rodar nestes repos.

### Falsos amigos — conferidos, e cada um já custou ou custaria um dia de trabalho

1. **"Grupo econômico" existe no código com outro significado.**
   `api-agent-orbita/src/services/analysisAgent/prompt.ts:86` imprime
   *"Grupo econômico usado para pontuação: ${economicClass.scoreGroup}"*, e
   `scoreGroup` é `"A++/A+" | "B1/B2" | "C1/C2" | "D/E"`
   (`src/services/analysisAgent/economicClass.ts:3`) — **faixa de classe
   socioeconômica do score, não o grupo proprietário de lojas**.
   *(Correção de uma versão anterior deste documento, que afirmava "zero
   ocorrências": a busca não cobria o acento em "econômico".)*
2. **Dois `POST /analysis` diferentes.** O do `api-agent-orbita`
   (`src/routes/analysis.routes.ts:7`) **calcula** viabilidade e não grava nada;
   o `${apiExpansion}/analysis` **grava** a análise e está fora destes 3
   repositórios. Z10 é sobre o segundo. Quem grepar por `POST /analysis` acha o
   primeiro, que está clonado, e perde um dia.
3. **"Modelo de negócio" × "Tipo de Loja".** `AnalysisStoreType` =
   `Nova`/`Conversão`/`Mudança de Ponto` (`analysis.model.ts:16-27`), rotulado
   "Tipo de Loja" na tela (`pages/view/view.component.html:43`). **Não é**
   `Popular`/`Convencional`.
4. **`Popular` aparece no código e não é modelo de negócio.** As 4 ocorrências
   são rótulos de agrupamento de redes **concorrentes** ("Super/Ultra/Maxi/Mega
   Popular") em
   `webapp-orbita-angular/src/app/modules/view/components/manage/components/categorization/components/grouping/new/new.component.ts:85,91,97,151`.
5. **`BANDEIRA` no backend é de concorrente.** `STORE_NAME_PROPERTY_KEYS` inclui
   `"BANDEIRA"`/`"bandeira"` em
   `api-agent-orbita/src/services/radiusSearch/aggregations/competitiveMap.ts:19-29`
   — chaves para extrair o **nome** de um concorrente, não taxonomia de bandeira
   Farmarcas.
6. **Já existe um número chamado "lojas" em tela.** O dashboard de análises
   exibe "N lojas" por bandeira e por UF, e esse número é **contagem de
   contratos**, não de lojas
   (`modules/analysis/pages/dashboard/components/brands/brands.component.ts:118`;
   `.../state-graph/state-graph.component.ts:41`). Com a camada do Z1, o produto
   passa a ter **duas contagens com o mesmo nome e valores diferentes**.

### Não localizado nestes 3 repositórios

A ausência vale **para estes três** (`api-agent-orbita`, `api-orbita-nodejs`,
`webapp-orbita-angular`), nunca como fato sobre o produto inteiro — existe ao
menos um 4º repositório do Órbita, onde vive a **tela** do Órbita IA.

- Qualquer serviço de **zoneamento**, de **teto por faixa de população**, de
  **distância mínima entre lojas Farmarcas** ou de **"ocupar vaga"**
  (`grep -rniE "zonea|zoning|economicGroup|ocupar.?vaga"` → zero).
- **Fonte/base de lojas Farmarcas.** Não existe nenhuma coleção, endpoint ou
  modelo de loja Farmarcas (ver falso amigo nº 6 para o que a palavra "loja"
  acha). Hoje o cadastro existe como planilha estática
  (`relatorio-lojas-23_10_2026.xlsx`), fora do produto.
- Acesso às bases **`contratos_expansao`** e **`all_expansion.analysis_data`**
  para fins de contagem (só `analysis_data` aparece, e como *fonte de mapa*).
- **A API que grava a análise** (`${apiExpansion}/analysis`). O
  `api-orbita-nodejs` monta apenas `/health`, `/imports`, `/sources`,
  `/markers`, `/grouping`, `/graphic` (`api-orbita-nodejs/app.js:52-57`; a linha
  `:58` monta `/api-docs`) — **não serve `/expansion`**. *Pista para achar o
  dono:* em produção a API responde em
  `https://expansion.api.radar.farmarcas.com.br`
  (`webapp-orbita-angular/src/environments/environment.production.ts:25`), host sob
  o domínio do **Radar** — é com o time do Radar que se pergunta.
- **Rota ou tela do Órbita IA** (`grep -rniE "path: *'ai'|orbita/ai|orbita.?ia"`
  → zero; e o webapp não chama o motor da IA — zero referências a
  `api-agent-orbita` em `src/environments`). **A rota em si é desconhecida:**
  qualquer caminho escrito em rascunhos anteriores é suposição.
- **Lista canônica de bandeiras com o modelo de negócio de cada uma** (lacuna
  levantada na geração destes cards, sem registro na página do Confluence nem no
  rascunho de regras — não é decisão numerada).

---

# Épico A — Fundação de dado

> **Nota de mapeamento.** O épico SQO-1331 já tem duas histórias que cobrem este
> épico: **SQO-1333** ("Criar camada de lojas abertas/em montagem do Radar no
> Órbita") e **SQO-1336** ("Criar rotina de atualização da camada de lojas
> abertas"). Por isso a fundação de dado está dividida em **Z1** (a camada e o
> contrato de dado) e **Z1b** (a rotina de carga), em vez de um card único.
> ⚠️ **O título do SQO-1333 diz "abertas/em montagem" e a regra vigente conta
> também `Transição`** — ver Z1, Pontos em aberto.

## Z1 → SQO-1333

### [Dados] Camada de Lojas do Radar no Órbita

**Contexto:**

**Comportamento atual.** O Órbita **não tem** o cadastro de lojas da Farmarcas.
Conferido nesta sessão: não existe **fonte de dado** de lojas nos 3 repositórios
— nenhuma coleção, nenhum endpoint, nenhum modelo de loja Farmarcas. Para saber
se há loja nossa perto de um ponto, o analista olha a camada **Concorrentes** e
procura o nome da bandeira, ou abre uma planilha estática
(`relatorio-lojas-23_10_2026.xlsx`) fora do produto.

**Por que está errado.** Nome de bandeira na camada Concorrentes **não prova que
a loja é nossa**: há registro com nome de bandeira Farmarcas que não existe no
cadastro de lojas (caso verificado e documentado em
`.claude/skills/analise-regiao-farmarcas/references/bases-orbita.md:264`, seção
"Bandeira na camada Concorrentes NÃO prova que a loja é nossa"). E a planilha
envelhece em silêncio: loja aberta ou fechada depois da extração não aparece.
Nenhuma regra de zoneamento pode ser automatizada sobre isso — Z2, Z3 e Z4 todas
contam lojas, grupos e distâncias.

**Impacto de negócio de deixar como está.** Sem este card, **nenhum dos outros
cards roda**. O zoneamento continua sendo contagem manual, o analista continua
precisando saber que a regra existe, e o produto continua liberando pontos que
ferem a regra — que é o problema que a página do Confluence abre descrevendo.

**Alternativa descartada.** Trazer **um único endereço por loja** (nome,
endereço, latitude e longitude) foi a especificação inicial e **foi descartada em
2026-11-17**. O endereço fiscal pode ser o do escritório, de outra unidade do
grupo ou de um imóvel vizinho; usar só ele deixa a regra cega justamente onde a
loja de fato opera. Por isso a camada traz **dois** endereços, com coordenada
própria cada. Consequência aceita pela área de negócio: a regra de zoneamento
fica **mais dura** (Z2) e uma loja pode ocupar vaga em dois municípios (Z3).

Rastreabilidade: Confluence 4545904644 v14, seção "Regras de negócio → Base de
lojas sincronizada do Radar". Contrato de dado e a decisão de 2026-11-17 em
`outputs/regras-negocio-zoneamento-orbita.md`, seção "3.1 Base de lojas —
sincronismo D-1 com o Radar" (RN-DADO-02 e RN-DADO-05).

**Referências visuais:**
Não aplicável — card de dado, sem tela.

**Caminho/ideia de código:**

Sem rota de UI. Mas há caminho de código, conferido em 2026-11-23:

* **Como dado externo entra hoje no Órbita:** `createDataSource()` em
  `api-orbita-nodejs/src/services/sourceService.js:189` grava a configuração da
  fonte na coleção `sources` (`:223`), com `config.structure.name` (`:218`)
  apontando para a coleção física dos dados; o processamento é delegado a uma
  **Lambda** (`AWS_EXCEL_FILE_FUNCTION` `:193`, `AWS_SHAPEL_FILE_FUNCTION`
  `:195`) que **não está nestes 3 repositórios**. A porta de entrada é
  `POST /imports/:type` (`src/controllers/fileController.js:10`), hoje **upload
  manual de arquivo**.
* **Convenção de nome de fonte:** `SOURCE_NAMES` em
  `api-agent-orbita/src/constants/collections.ts:5-18`.
* **Leitura por coordenada (o que o Z2 consome):** a primitiva existe —
  `searchService.getLocation({ dataSources, latitude, longitude, range })` em
  `api-orbita-nodejs/src/services/searchService.js:16`. Cuidado: o embrulho
  `sourceService.getAllRadius()` (`sourceService.js:38`) devolve **só os ids das
  fontes com resultado**, não os registros.
* ⚠️ **Decisão de modelagem a tomar antes de começar:** a camada de lojas vira
  mais uma `source` (seguindo `structure.name`, como `analysis_data` em
  `searchService.js:558`) ou uma coleção própria, fora do mecanismo de fontes?
  Fontes são pensadas para camada de mapa com geometria; a de lojas é consultada
  por **CNPJ**, por **município** e por **coordenada**, e não é (ainda) camada de
  mapa. **Refazer depois custa a carga inteira.**

**Escopo do card:**

1. Criar a camada/base de lojas no Órbita, chaveada por **CNPJ da loja**, com os
   8 itens abaixo (18 campos no total). Cada um existe porque uma regra depende
   dele:
   1. CNPJ, nome e razão social;
   2. **Endereço da Receita** + município + UF;
   3. **Latitude e longitude do endereço da Receita**;
   4. **Endereço popular** + município + UF;
   5. **Latitude e longitude do endereço popular**;
   6. Status;
   7. Bandeira e Modelo de negócio;
   8. Grupo econômico (**identificador próprio**) e responsável pelo grupo.
2. Expor leitura de lojas **por CNPJ**, **por município** (dos dois endereços) e
   **por coordenada** — é o que Z2 e Z3 consomem.
3. Toda leitura devolve junto a **data da última carga bem-sucedida** e o
   sinalizador **`cargaDefasada: true|false`**. Este card entrega **o campo no
   contrato de leitura**; quem o preenche com valor real é o Z1b (regra 3 de lá,
   que é a fonte da verdade desta regra). **Enquanto o Z1b não existir**, a
   camada é alimentada por upload manual (`POST /imports/:type`) e o campo
   carrega a data dessa carga manual com `cargaDefasada: false` — valor
   **provisório por ausência de rotina**, que não deve ser lido como "a carga
   está em dia".
4. **Não entra neste card:** nenhuma regra de zoneamento (distância, teto,
   bandeira) — só o dado.
5. **Não entra neste card:** a rotina de carga diária → é o **Z1b / SQO-1336**.
6. **Não entra neste card:** a geocodificação dos endereços sem coordenada →
   pré-requisito de cronograma, ver **SQO-1337** e Pontos em aberto.
7. **Não entra neste card:** desligar ou alterar a camada Concorrentes. Mas ver
   Pontos em aberto: passam a existir **duas respostas em tela** para "tem loja
   nossa aqui?".

**Regras de negócio:**

1. A chave da camada é o **CNPJ da loja**. É por ela que se evita contar a mesma
   loja duas vezes (ver Z3, regra de deduplicação).
2. **Loja sem CNPJ no Radar não é descartada e não é mesclada com nenhuma
   outra.** Entra sem chave, marcada como `sem_chave`, e sai nas leituras como
   registro que **não pode ser deduplicado**. O rascunho de regras (RN-03.1)
   dedupica por *"CNPJ, quando presente nos registros"* — ou seja, a própria
   especificação admite registro sem CNPJ. Descartar esconde loja do Z2/Z3;
   mesclar funde duas lojas diferentes.
3. **O que conta como "coordenada utilizável":** latitude e longitude existem e
   são numéricas (não nulas, não string vazia); **não** são `0,0`; e caem dentro
   da caixa do território brasileiro (latitude entre −34 e +6, longitude entre
   −74 e −34). Qualquer outro caso é **não utilizável**, marcado **por
   endereço**. Essa definição existe porque `0,0` é o que um cadastro vazio
   costuma gravar, e `0,0` fica no Golfo da Guiné: sem o filtro, o Z2 trataria
   essa loja como "existente e longe de tudo", que é o pior dos dois erros.
4. **Loja sem coordenada utilizável entra na contagem do município** (Z3). Falta
   de coordenada não a tira do teto, que é por município cadastrado.
5. **Loja sem coordenada utilizável não pode ser checada na distância** (Z2) e
   sai nas leituras como **não checável**, nunca como **sem violação**. São
   coisas diferentes: a primeira é lacuna, a segunda é aprovação.
6. **A cobertura de coordenada é medida e reportada por endereço, não por
   loja.** A mesma loja pode ter coordenada da Receita e não a do endereço
   popular, ou o contrário, e cada um é checado separadamente no Z2.
7. O **status** vem como **texto do Radar — não converter para enum fechado
   nesta camada.** Os quatro valores conhecidos são `Ativado`, `Montando`,
   `Transição` e `Desativado`, mas a lista **não está confirmada** (ver Pontos em
   aberto). Valor desconhecido entra como veio e é contabilizado como **não
   classificado**, nunca mapeado "para o mais parecido".
8. O **grupo econômico** vem como **identificador próprio do cadastro do
   Radar**, nunca apurado pelo nome do responsável. Pelo nome, uma grafia
   divergente inventa um grupo novo e barra um pedido que caberia.
9. O campo **"Responsável pelo grupo econômico" é dado pessoal**: entra na
   camada porque é o que liga o solicitante ao grupo (Z3), mas **nunca aparece em
   tela** (LGPD). Quem imprime rótulo anônimo é o Z5.
10. **O que NÃO muda com este card:** a camada **Concorrentes** continua
    existindo exatamente como está, com os mesmos registros e o mesmo
    comportamento no mapa. Este card não a altera, não a substitui e não corrige
    seus falsos positivos de bandeira.
11. **O que NÃO muda com este card:** `POST /sources/search/warnings`
    (`api-orbita-nodejs/src/services/searchService.js:556`) continua checando
    **análises** próximas, com `ANALYSIS_RADIUS_SEARCH = 300` (`:10`), e continua
    devolvendo `{ hasAnalysis }`. Quem mexe nele é o Z6.

**Pontos em aberto:**

- **Os 8 itens existem no Radar?** A página do Confluence diz "A carga precisa
  trazer, por loja: (...) Grupo econômico, como identificador próprio". O
  rascunho registra que *"a especificação inicial previa apenas nome, endereço,
  latitude e longitude de um único endereço"* e marca como **pré-requisito a
  confirmar com o time do Radar**. Confirmar item por item antes de estimar. **Se
  algum campo não existir, a regra que depende dele não pode ser automatizada e
  precisa ser declarada como não avaliada — nunca presumida.**
- **O identificador de grupo econômico é chave de cadastro ou rótulo editável?**
  (`regras-negocio-zoneamento-orbita.md`, seção 3.1: *"Confirmar com o Radar: é
  chave de cadastro ou rótulo editável? Se for editável, a fragilidade continua,
  só muda de campo."*) Se for editável, a regra 8 não entrega o ganho que promete.
- **A lista de valores de Status está fechada?** A página v14 diz apenas
  **"Status;"**, sem enumerar. O rascunho, na seção "2.1 Status de loja —
  definição pendente", enumera quatro e marca **dois como "a definir"**:
  `Montando` (*"a definir — inclusive há quanto tempo um registro pode permanecer
  neste status"*) e `Transição` (*"a definir. Se transição significar saída da
  rede em andamento, contar como ocupando vaga fecha uma praça que está prestes a
  abrir"*). Um enum fechado errado aqui erra o teto do Z3 em silêncio.
  **Relacionado:** o título do SQO-1333 fala em lojas "abertas/em montagem", mas
  a regra vigente conta também `Transição` — **alinhar título e escopo**.
- **Quantas lojas do Radar não têm CNPJ?** Medir na primeira carga. Se o volume
  for relevante, a chave precisa ser revista com o Radar, não contornada no
  código.
- **Cobertura de coordenada.** Medição anterior (dump de 2026-10-26) indicava 34%
  das lojas sem coordenada utilizável **considerando um único endereço**; com
  dois endereços, precisa ser remedida nos dois campos, e a do endereço popular
  tende a ser pior, *"porque nunca foi usada para nada"* (seção 8, item 1).
  Com cobertura parcial, **dois pedidos equivalentes recebem vereditos diferentes**
  conforme a loja vizinha tenha ou não coordenada — o rascunho chama isso de
  "consequência de equidade" e trata a geocodificação como **pré-requisito de
  cronograma, não backlog** (ver SQO-1337).
- **Divergência de contagem conhecida:** as referências internas registram ora
  2.804 lojas / 1.841 com coordenada, ora 2.808 / 1.844 (seção 3). Conferir
  contra a carga real.
- **Modelagem: `source` ou coleção própria?** Ver Caminho/ideia de código.
- **Duas respostas em tela para a mesma pergunta (2ª ordem).** Com esta camada,
  "tem loja nossa perto?" passa a ter duas fontes no produto: ela e a camada
  Concorrentes, que erra por nome de bandeira. Além disso o dashboard de análises
  **já exibe "N lojas"** contando **contratos**
  (`modules/analysis/pages/dashboard/components/brands/brands.component.ts:118`;
  `.../state-graph/state-graph.component.ts:41`) — passam a existir duas
  contagens com o mesmo nome e valores diferentes. **Não está no escopo pedido**;
  está aqui para decisão de quem pediu o card.
- **Dossiê de região (2ª ordem).** A skill `analise-regiao-farmarcas` lê hoje a
  planilha estática. Com a camada no produto, dossiê e produto passam a contar
  lojas sobre fontes diferentes e podem divergir para o mesmo ponto.
- **Time do Radar precisa ser avisado:** campos novos e as duas coordenadas são
  pré-requisito, e a fila de qualidade de cadastro do Radar passa a fazer parte
  da regra — um município cadastrado errado erra o teto junto (RN-DADO-03).

**Critérios de aceite:**

- Dado que a camada foi carregada, quando se consulta uma loja pelo CNPJ, então
  vêm os **8 itens do Escopo** (18 campos, contando município, UF, latitude e
  longitude de cada um dos dois endereços), com as duas coordenadas separadas, e
  a data da última carga bem-sucedida.
- Dado um registro do Radar **sem CNPJ**, quando a camada é carregada, então ele
  entra marcado como `sem_chave` — e **não** é descartado nem mesclado com outro.
- Dado uma loja com latitude/longitude `0,0` (ou fora da caixa do território
  brasileiro), quando ela é lida, então a coordenada sai como **não utilizável**
  para aquele endereço — e **não** como um ponto válido distante.
- Dado uma loja com coordenada da Receita e **sem** coordenada do endereço
  popular, quando ela é lida, então ela aparece como elegível para contagem de
  município **e sinalizada como não checável na distância pelo endereço popular**
  — a cobertura é reportada por endereço, não por loja.
- Dado uma loja cujo endereço da Receita e endereço popular estão em
  **municípios diferentes**, quando ela é lida, então os dois municípios vêm
  preenchidos e distinguíveis.
- Dado uma loja com status que **não é** nenhum dos quatro conhecidos, quando ela
  é lida, então o status sai **como veio** e ela é contabilizada como **não
  classificada** — e **não** mapeada para o valor mais parecido.
- Não se pode fugir da seção Escopo do card
- Estar em conformidade com as regras de negócio
- Passar nos testes definidos por QA, **incluindo a validação de carga descrita
  abaixo**. Suíte verde sozinha não encerra este card.
- Conformidade com Figma: **não aplicável** (card de dado, sem tela)

> **Atenção de QA (precedente SQO-1162).** Teste unitário com Mongo mockado passa
> verde com a carga quebrada em produção. A validação real deste card é conferir
> a **contagem de lojas** e a **cobertura de coordenada por endereço** contra o
> cadastro do Radar no mesmo dia.

**Figma:** Não aplicável — card de dado, sem tela. (A página do Confluence
registra "A ser construído" para o Figma **da feature**, que é dos cards Z6/Z7/Z8.)

**Estimativa:** [DEFAULT: 5 pts — confirmar com o time]
**Prioridade:** [DEFAULT: P0 — confirmar com o time]
**Dependências:** Nenhuma. **Bloqueia diretamente:** Z1b, Z2, Z3, Z4.
**Bloqueia por transitividade:** Z5, Z6, Z7, Z8, Z10. Único card que não depende
deste: Z9.
**Revisado por (?_?) revisor-clareza-junior:** pronto para o júnior

---

## Z1b → SQO-1336

### [Dados] Rotina de Carga Diária D-1 da Camada de Lojas

**Contexto:**

**Comportamento atual.** Não há rotina nenhuma: o cadastro de lojas chega ao
Órbita como planilha, por upload manual (`POST /imports/:type`,
`api-orbita-nodejs/src/controllers/fileController.js:10`). Conferido nesta
sessão: **não existe agendador em nenhum dos dois backends** —
`grep -rniE "cron|node-schedule|agenda|setInterval|scheduler"` em
`api-orbita-nodejs/src`, `api-agent-orbita/src` e nos dois `package.json`
retorna **zero ocorrências**.

**Por que está errado.** O cadastro muda todo dia, por abertura, fechamento e
mudança de ponto. Um veredito de zoneamento calculado sobre uma planilha de
semanas atrás barra ou libera errado — e, pior, barra ou libera **com
confiança**, porque o analista não tem como saber a idade do dado.

**Impacto de negócio de deixar como está.** A camada do Z1 nasce desatualizada e
envelhece em silêncio. Como o zoneamento passa a ser automático, o erro deixa de
ser do analista que não conferiu e passa a ser do produto que afirmou.

Rastreabilidade: Confluence 4545904644 v14, seção "Regras de negócio → Base de
lojas sincronizada do Radar" (periodicidade D-1, falha de carga e limite de
defasagem). Detalhamento em `outputs/regras-negocio-zoneamento-orbita.md`,
RN-DADO-01.

**Referências visuais:**
Não aplicável — card de rotina, sem tela. O único reflexo em tela é a data da
carga exibida no veredito, que é escopo do Z5.

**Caminho/ideia de código:**

Sem rota de UI. ⚠️ **Suposição a resolver antes de estimar: não existe
agendador.** "Carga diária" não tem hoje onde rodar nestes repositórios (grep
acima). Decidir com o time: **Lambda agendada** — que é o padrão que o produto já
usa para processar fonte (`AWS_EXCEL_FILE_FUNCTION` em
`api-orbita-nodejs/src/services/sourceService.js:193`) — ou outro serviço.
**Não assumir que há cron.**

**Escopo do card:**

* Criar a rotina que roda **diariamente (D-1)** e atualiza a camada do Z1 a
  partir do cadastro do Radar.
* Registrar, a cada execução: data/hora, se foi bem-sucedida, e o volume de
  registros carregados.
* Calcular e expor o sinalizador **`cargaDefasada`** que as leituras do Z1
  devolvem.
* **Não entra neste card:** o contrato de dado e a modelagem da camada → Z1.
* **Não entra neste card:** transformar `cargaDefasada: true` em veredito
  `indeterminado` → isso é o **Z5**.

**Regras de negócio:**

1. A rotina roda **diariamente, em D-1** (dado do dia anterior).
2. **Se a carga falhar, o Órbita opera com a última carga bem-sucedida** — não
   fica sem base e não apaga o que tinha.
3. **Toda leitura devolve a data da última carga bem-sucedida e
   `cargaDefasada: true|false`**, calculado contra o limite de defasagem
   **configurado no ambiente**. Esta rotina **não calcula veredito**: o que ela
   garante é que a informação **chega**. Nunca devolver lista vazia, 404, erro
   genérico nem silêncio quando a carga está defasada — silêncio é lido como
   liberação, e um gate que falha aberto é pior que gate nenhum, porque cria a
   confiança de que a checagem aconteceu.
4. **Enquanto o limite de defasagem não for decidido (D-06), ele é parâmetro de
   configuração — nunca um número no código.**
5. **Loja que deixa de aparecer numa carga bem-sucedida não é apagada
   silenciosamente.** Se um CNPJ veio ontem e não veio hoje, o registro é mantido
   e marcado como `ausente na carga de <data>`. **Sumir do cadastro não é o mesmo
   que `Desativado`:** desativado é informação do Radar, ausência é falta de
   informação. Tratar uma como a outra **libera vaga no Z3 sem que ninguém tenha
   fechado loja**.
6. **A carga é idempotente:** rodar duas vezes no mesmo dia deixa exatamente um
   registro por CNPJ, e a data registrada é a da última execução bem-sucedida.
7. **Queda brusca de volume não substitui uma base boa.** Se a carga trouxer um
   volume muito menor que o da última bem-sucedida (corte percentual a definir
   com o time), ela é marcada como **suspeita** e a base anterior continua
   valendo até confirmação.
8. **O que NÃO muda com este card:** o upload manual de fontes
   (`POST /imports/:type`, `fileController.js:10`) e o mecanismo de
   `createDataSource()` (`sourceService.js:189`) continuam existindo como estão,
   para as demais camadas do produto.
9. **O que NÃO muda com este card:** nenhuma regra de zoneamento. A rotina não
   decide nada sobre pontos — só mantém o dado.

**Pontos em aberto:**

- **Onde a rotina roda?** Não existe agendador nestes 2 backends (ver
  Caminho/ideia de código). É a primeira decisão do card.
- **Qual é o limite de defasagem** acima do qual o veredito vira `indeterminado`?
  A página do Confluence diz "acima do limite de defasagem" **sem dar o número**
  (decisão D-06 do rascunho, dono "Produto propõe, Expansão aceita o custo").
  Sem esse valor a regra 3 não é testável com número fixo.
- **Qual é o corte de "volume suspeito"** da regra 7? Não consta em nenhuma das
  duas fontes; proposto aqui para o júnior não escolher sozinho. Definir também
  **quem confirma uma carga suspeita e em quanto tempo**: sem isso, "até
  confirmação" é indefinido e a base anterior envelhece silenciosamente. Note que,
  pela regra 3, o relógio da defasagem **não** zera com carga suspeita (ela não é
  bem-sucedida), então o caso acaba caindo em `cargaDefasada: true` sozinho.
  Confirmar se é esse o comportamento desejado ou se a carga suspeita deve gerar
  alerta próprio.
- **Como o Radar entrega o dado?** API, arquivo em bucket, banco replicado? A
  página não diz, e isso muda o card inteiro. Perguntar ao time do Radar.
- **Quem é avisado quando a carga falha?** A regra 2 mantém o produto de pé, mas
  ninguém fica sabendo. Definir destino do alerta (2ª ordem, fora do escopo
  pedido).

**Critérios de aceite:**

- Dado que a rotina roda com sucesso, quando a camada é lida, então a data da
  última carga bem-sucedida é a de hoje e `cargaDefasada` é `false`.
- Dado que a carga de hoje **falhou**, quando a camada é lida, então ela responde
  com os dados da última carga bem-sucedida e informa **a data dessa carga**, não
  a de hoje.
- Dado que a última carga bem-sucedida é mais antiga que o **limite de defasagem
  configurado no ambiente**, quando a camada é lida, então a resposta traz os
  dados **e** `cargaDefasada: true` com a data dessa carga — e **não** lista
  vazia, 404, erro genérico nem "nenhuma loja encontrada". O teste usa o valor
  configurado, nunca um número fixo no código.
- Dado um CNPJ presente na carga de ontem e **ausente** na de hoje, quando a
  camada é lida, então o registro continua existindo, marcado como ausente na
  última carga — e **não** aparece como `Desativado` nem some da contagem.
- Dado que a rotina roda **duas vezes no mesmo dia**, quando ela termina, então
  há exatamente **um** registro por CNPJ.
- Dado que a carga de hoje trouxe volume muito menor que o da última
  bem-sucedida, quando ela termina, então é marcada como **suspeita** e a base
  anterior continua valendo.
- Não se pode fugir da seção Escopo do card
- Estar em conformidade com as regras de negócio
- Passar nos testes definidos por QA, **incluindo conferir a contagem da carga
  contra o cadastro do Radar no mesmo dia** (ver atenção de QA do Z1)
- Conformidade com Figma: **não aplicável** (card de rotina, sem tela)

**Figma:** Não aplicável — card de rotina, sem tela.

**Estimativa:** [DEFAULT: 5 pts — confirmar com o time] — **sem base de código
para a parte de agendamento**, que não existe nestes repositórios.
**Prioridade:** [DEFAULT: P0 — confirmar com o time]
**Dependências:** Z1 (a camada precisa existir para ser atualizada).
**Bloqueia:** nenhum card em desenvolvimento — mas **bloqueia ligar o gate em
produção**. Sem esta rotina, Z6, Z7 e Z8 emitem veredito sobre uma carga manual
que envelhece em silêncio, que é o modo de falha que o Contexto deste card
descreve.
**Revisado por (?_?) revisor-clareza-junior:** pronto para o júnior

---


---

## Z1c → SQO-1337

### [Radar] Ajuste Manual da Coordenada da Loja no Cadastro

**Contexto:**

**Comportamento atual.** O cadastro de lojas do Radar não oferece forma de
corrigir a coordenada (latitude/longitude) de uma loja. Quando a geocodificação
do endereço erra, ou não resolve, o registro fica sem coordenada utilizável — ou,
pior, com uma coordenada que aponta para o lugar errado — e não há onde arrumar.
Medição sobre o dump de 2026-10-26: **34% das lojas não tinham coordenada
utilizável considerando um único endereço**, e há caso verificado de loja
cadastrada em Patrocínio Paulista/SP com coordenada a 342 m do centro de
Franca/SP, cidades a ~25 km.

**Por que está errado.** A partir do gate de zoneamento, a coordenada deixa de ser
enfeite de mapa e passa a decidir se um pedido é barrado. Loja sem coordenada
utilizável **não pode ser checada na distância mínima** (Z1 regra 5, Z2 regra 7),
e loja com coordenada errada é checada **contra o lugar errado**. Nos dois casos a
regra de zoneamento erra, e hoje ninguém tem como corrigir o dado de origem.

**Impacto de negócio de deixar como está.** Enquanto a cobertura for parcial,
**dois pedidos equivalentes recebem vereditos diferentes** conforme a loja vizinha
tenha ou não coordenada: um é barrado, o outro passa. O rascunho de regras chama
isso de "consequência de equidade, não só de cobertura" e registra que, visto de
fora, **isso é arbitrariedade**. É por isso que a geocodificação é tratada como
**pré-requisito de cronograma do gate, não item de backlog**.

Rastreabilidade: Confluence 4545904644 v14, seção "Regras de negócio → Base de
lojas sincronizada do Radar" (*"Loja sem coordenada utilizável entra na contagem
do município, mas não pode ser checada na distância"*). Dimensionamento e a
classificação como pré-requisito em `outputs/regras-negocio-zoneamento-orbita.md`,
seção "8. Pré-requisitos e impactos fora do escopo pedido", item 1, e RN-DADO-02,
RN-DADO-03 e RN-DADO-05.1.

**Referências visuais:**
Não informado — solicitar ao design. Existe precedente funcional **no Órbita**
(não no Radar) de ajustar coordenada de um registro de fonte:
`PUT /sources/{sourceName}/{geometryId}/coords`
(`PUT /:source/:id/coords`, `api-orbita-nodejs/src/controllers/sourceController.js:144`, exposto no front por
`SourceService.updateCoordinates()`,
`webapp-orbita-angular/src/app/shared/services/source.service.ts:114`). Serve como
referência de interação (arrastar o pin / informar lat-lng), **não** de
implementação: este card é no Radar.

**Caminho/rota:**
**Não aplicável — fora dos repositórios do Órbita.** O cadastro de lojas é do
**Radar**, outro produto, e seu código não está em nenhum dos 3 repositórios
mapeados (`api-agent-orbita`, `api-orbita-nodejs`, `webapp-orbita-angular`) — a
ausência vale para estes três, não para a empresa. A rota de navegação dentro do
Radar precisa ser informada pelo time do Radar; ver Pontos em aberto.

**Escopo do card:**

* No cadastro de loja do Radar, permitir **ajustar a coordenada** de cada um dos
  **dois endereços** da loja (Receita e popular), separadamente.
* Registrar que a coordenada foi ajustada manualmente, com data e autor — para
  distinguir coordenada geocodificada de coordenada corrigida à mão.
* **Não entra neste card:** nenhuma regra de zoneamento. Este card só conserta o
  dado de origem; quem consome é o Z1.
* **Não entra neste card:** geocodificar em massa os endereços sem coordenada.
  Isso é a outra metade do pré-requisito e precisa de card próprio no Radar — ver
  Pontos em aberto.
* **Não entra neste card:** a fila de qualidade de cadastro (detectar
  automaticamente divergência entre os dois endereços da mesma loja).

**Regras de negócio:**

1. O ajuste vale **por endereço**, não por loja: a loja tem duas coordenadas
   (Receita e popular) e elas são corrigidas de forma independente.
2. **Coordenada ajustada à mão é marcada como tal**, com data e autor. Sem essa
   marca, não dá para medir quanto da base depende de correção manual nem auditar
   um veredito que mudou porque alguém moveu um pin.
3. **O ajuste não apaga o endereço escrito.** Endereço textual e coordenada são
   dados distintos: corrigir o pin não corrige o endereço, e vice-versa.
4. A coordenada ajustada precisa passar pela mesma validação de **"coordenada
   utilizável"** definida no Z1 regra 3 (numérica, não `0,0`, dentro da caixa do
   território brasileiro). Salvar um pin inválido à mão recria o problema que o
   card existe para resolver.
5. **O que NÃO muda com este card:** o endereço da Receita continua sendo o
   endereço fiscal e o popular continua sendo o operacional. Este card não muda a
   semântica de nenhum dos dois, nem qual deles é "o principal".
6. **O que NÃO muda com este card:** nada no Órbita. A camada do Z1 apenas
   **recebe** a coordenada corrigida na carga D-1 seguinte (Z1b) — não há
   alteração de código do Órbita neste card.

**Pontos em aberto:**

- **Qual é a rota dentro do Radar?** Não verificável nestes 3 repositórios.
  Informar com o time do Radar antes de publicar — **não** herdar a frase-padrão
  do template ("Radar → ícone de 4 quadradinhos → Órbita → Órbita IA"), que é de
  outra feature e já foi para o board errada no SQO-1279 e no SQO-1323.
- **Quem pode ajustar a coordenada?** O ajuste passa a ter efeito sobre o
  veredito de zoneamento de terceiros: mover o pin de uma loja pode barrar ou
  liberar o pedido de outro associado. Definir perfil e alçada — isso **não** é
  detalhe de UI.
- **Este card sozinho resolve a cobertura?** Não. Ele resolve a **correção caso a
  caso**; os 34% sem coordenada precisam de **geocodificação em massa**, que é
  item separado e é o que de fato destrava o Z2. Confirmar com o time do Radar se
  existe card para isso — se não existir, a cobertura continua sendo o gargalo do
  gate mesmo com este card pronto.
- **A cobertura do endereço popular nunca foi medida.** O rascunho registra que
  ela *"tende a ser pior, porque nunca foi usada para nada"*. Medir antes de
  dimensionar o esforço: pode ser que a maior parte do trabalho esteja num campo
  que ninguém olhou ainda.
- **Divergência entre os dois endereços da mesma loja** (RN-DADO-05.1): acima de
  um limite a definir, é sinal de erro de cadastro, não de duas localizações
  reais. O limite é a decisão **D-16** e não está definido. Fora do escopo deste
  card, mas é o que diria **quais** lojas precisam de ajuste.
- **Impacto de 2ª ordem — mover um pin muda contagem e veredito alheios.** Pela
  regra 11 do Z3, a loja ocupa vaga no município de cada um dos dois endereços;
  corrigir uma coordenada pode **mudar o município** de um dos endereços e, com
  isso, abrir ou fechar uma praça para outro associado. Quem ajusta precisa saber
  disso. Fora do escopo pedido; registrado para decisão.

**Critérios de aceite:**

- Dado uma loja com coordenada errada no endereço da Receita, quando o usuário
  ajusta o pin desse endereço e salva, então **só** a coordenada da Receita muda —
  a do endereço popular fica como estava.
- Dado uma loja **sem** coordenada no endereço popular, quando o usuário informa a
  coordenada desse endereço, então ela passa a existir e a loja deixa de constar
  como não checável na distância por aquele endereço (verificável na carga D-1
  seguinte, no Z1).
- Dado um ajuste salvo, quando o registro é consultado, então consta que a
  coordenada foi **ajustada manualmente**, com data e autor.
- Dado que o usuário tenta salvar uma coordenada `0,0` ou fora da caixa do
  território brasileiro, quando ele salva, então o sistema **recusa** o valor — e
  não grava um pin inválido.
- Dado um ajuste de coordenada, quando o endereço textual é consultado, então ele
  **não** foi alterado.
- Não se pode fugir da seção Escopo do card
- Estar em conformidade com as regras de negócio
- Passar nos testes definidos por QA
- Estar em conformidade com o Figma

**Figma:** Não informado — solicitar ao design. ⚠️ O card existente no board
herdou o link do **Handoff — Órbita** do template: **confirmar/substituir**, este
card é do Radar.

**Estimativa:** [DEFAULT: 3 pts — confirmar com o time] — **sem base de código**,
o repositório do Radar não está mapeado aqui.
**Prioridade:** [DEFAULT: P0 — confirmar com o time] (pré-requisito de cronograma
do Z2, não backlog)
**Dependências:** Nenhuma no Órbita. **Bloqueia na prática:** a cobertura de
coordenada de que o Z2 depende.
**Revisado por (?_?) revisor-clareza-junior:** _pendente — card acrescentado após
a 2ª rodada de revisão_
# Épico B — Motor de zoneamento

## Z2 → SQO-1384

### [API] Checagem de Distância Mínima Entre Lojas Farmarcas

**Contexto:**

**Comportamento atual.** O Órbita não mede distância entre o ponto pedido e lojas
Farmarcas. O que existe é outra coisa: `POST /sources/search/warnings`
(`api-orbita-nodejs/src/controllers/sourceController.js:96` →
`searchService.js:556`) procura **análises de ponto** anteriores num raio de
300 m (`ANALYSIS_RADIUS_SEARCH = 300`, `searchService.js:10`) e devolve só
`{ hasAnalysis: boolean }` (`:566`). Nenhuma checagem de loja.

**Por que está errado.** A regra de zoneamento existe para evitar conflito e
concorrência desleal entre associados, e o instrumento dela é a **distância
mínima entre lojas** — 300 m para a mesma bandeira, 500 m para bandeiras
diferentes. Hoje essa conta é feita à mão pelo analista, que precisa saber que a
regra existe, onde ela está e qual limiar vale. Quando ele não sabe, a regra é
ferida.

**Impacto de negócio de deixar como está.** Ponto que viola a distância mínima
chega até o fim da análise e às vezes até o contrato. O custo é duplo: a análise
de mercado inteira é desperdiçada e, quando a violação é contra loja de **outro
associado**, vira conflito entre associados — exatamente o que a regra existe
para impedir.

**Alternativa descartada.** Medir a distância só pelo endereço fiscal (da
Receita) foi a especificação inicial e **foi descartada em 2026-11-17**: o
endereço fiscal pode ser o do escritório, de outra unidade do grupo ou de um
imóvel vizinho, o que deixa a regra cega justamente onde a loja de fato opera. A
decisão registrada é travar pelos **dois** endereços, e a área de negócio está
ciente de que isso **torna a regra mais dura** — mais pontos passam a violar — e
aceita o efeito.

Rastreabilidade: Confluence 4545904644 v14, seções "Regras de negócio →
Distância mínima entre lojas" e "→ Dois endereços por loja". Alternativa
descartada em `outputs/regras-negocio-zoneamento-orbita.md`, "RN-DADO-05 — Toda
loja tem dois endereços, e a regra trava nos dois".

**Referências visuais:**
Não aplicável — card de backend. Quem mostra em tela é Z6, Z7 e Z8.

**Caminho/ideia de código:**

Card de backend, sem rota de UI. Onde a mudança entra:

* A checagem nasce como uma nova agregação em
  `api-agent-orbita/src/services/radiusSearch/aggregations/` (a pasta já
  concentra as agregações por raio; `index.ts` é o barril que as expõe).
* **Molde a copiar:** `aggregateCompetitiveMapStores()` em
  `competitiveMap.ts:47` já faz a mesma forma de trabalho — lê uma fonte, filtra
  por `geometry: { $geoWithin: { $geometry: searchAreaGeometry } }` (`:58-62`) e
  calcula metros com `@turf/distance` (`:1`) em
  `distanceMeters: Math.round(distance(center, point([longitude, latitude]), { units: "meters" }))`
  (`:115-116`). **Reaproveitar esse formato em vez de inventar cálculo de
  distância.** Alternativa em Mongo puro: `$geoWithin: { $centerSphere: [[lng, lat], range / EARTH_RADIUS] }`
  com `EARTH_RADIUS = 6378100.0` (`api-orbita-nodejs/src/services/searchService.js:6, :62`).
* **Três diferenças obrigatórias em relação ao molde:** (1) a fonte é a camada de
  lojas do Z1, **não** `SOURCE_NAMES.COMPETITORS_ANALYSIS` — a camada Concorrentes
  não serve para esta regra (ver Z1); (2) cada loja tem **dois** pontos, então são
  duas medições por loja; (3) o molde descarta documento sem geometria devolvendo
  `null` — aqui a loja sem coordenada **não pode ser descartada**: ela sai como
  `nao_checada` (regra 7).
* **Não** criar isto dentro de `api-orbita-nodejs/src/services/searchService.js`:
  aquele arquivo é a busca de camadas do mapa e o `getWarnings` de análises, que
  as regras 10 e 11 mandam não tocar.
* ⚠️ **Em qual serviço o motor de zoneamento mora ainda não está decidido** —
  ver Z5, que tem o mesmo bloqueio. Z2 e Z3 devem nascer no mesmo serviço.

**Escopo do card:**

* Criar a checagem de distância mínima: dado um ponto (latitude/longitude) e,
  opcionalmente, o **id** da bandeira pretendida, devolver **todas as lojas
  Farmarcas candidatas avaliadas**, cada uma com seu resultado, a distância
  medida, o limiar aplicado e qual endereço foi usado.
* **A resposta não é só a lista de violações:** loja avaliada e aprovada e loja
  não avaliável precisam aparecer também, porque é a diferença entre as três que
  o Z5 imprime.
* **Vocabulário de resultado (vale para Z2, Z3, Z4 e Z5).** Cada regra checada
  devolve exatamente um destes valores, distintos de propósito: `fere` = a regra
  barra o ponto; `avisa` = foi ferida mas não barra; `nao_checada` = faltou dado
  para aplicar **esta regra** (ex.: loja sem coordenada); `ok` = aplicada e o
  ponto passou; `indeterminado` = não deu para situar o pedido (município ou
  população não resolvíveis — usado no Z1b e no Z3, **nunca** no Z2);
  `sem_teto` = só a regra de teto acima de 200.000 hab (Z3, regra 4).
  **Tipar o enum com os seis desde o Z2** — o Z5 consolida todos.
  **`nao_checada` nunca pode ser serializado como `ok`**, nem omitido.
  Quando uma regra for `nao_checada` por mais de uma causa ao mesmo tempo (ex.:
  loja sem coordenada **em** município abaixo de 60 mil), a resposta traz a
  **lista** de motivos, não um só — o Z5 precisa imprimir as duas lacunas.
* Devolver, por loja, o que o Z5 precisa imprimir: bandeira, bairro ou endereço,
  status, distância medida, qual endereço foi usado, e **se a loja é do próprio
  solicitante**.
* **Não entra neste card:** o teto de grupos (Z3), a regra de bandeira/modelo
  (Z4), o texto do aviso (Z5) e qualquer tela.
* **Não entra neste card:** alterar `POST /sources/search/warnings` nem o
  `ANALYSIS_RADIUS_SEARCH = 300` existente.

**Regras de negócio:**

1. A distância mínima é de **300 metros entre lojas da mesma bandeira** e
   **500 metros entre lojas de bandeiras diferentes**. São dois limiares porque
   bandeira diferente concorre mais de frente que bandeira igual.
2. **"Mesma bandeira" é comparação por identificador de bandeira, não por
   nome.** A tela de análise já trabalha com bandeira como id numérico
   (`Analysis.brand?: number`,
   `webapp-orbita-angular/src/app/shared/models/analysis.model.ts:116`), então o
   pedido chega com o id, nunca com o texto da marca — comparar por texto
   reintroduz o erro de grafia que a regra 8 do Z1 evita no grupo econômico.
3. **Se a bandeira pretendida não for informada, aplica-se o critério mais
   restritivo: 500 metros.** Nunca o mais permissivo — na dúvida a regra protege.
4. A distância é medida **por coordenada**, independentemente do município
   cadastrado da loja.
5. **Ponto em divisa de cidade também é avaliado:** a loja vizinha do outro lado
   da divisa concorre do mesmo jeito, mesmo estando em outro município.
6. **Toda loja é avaliada pelos dois endereços** (Receita e popular) e **vale a
   menor distância encontrada**. Basta **um** dos dois ferir para a regra estar
   ferida. A resposta declara contra qual endereço ocorreu — Receita, popular ou
   **ambos**. Dizer "distância checada" sem dizer contra qual endereço esconde
   metade da regra.
7. **Loja sem coordenada utilizável (definição no Z1, regra 3) sai como
   `nao_checada`, nunca como `ok`.** Se um endereço é checável e o outro não, o
   resultado **consolidado da loja** é `nao_checada` — meia checagem não é
   aprovação.
8. **Em cidades acima de 200.000 habitantes o descumprimento é `avisa`, não
   `fere`**, porque a página oficial de zoneamento não declara distância mínima
   para essa faixa. A faixa de população vem do Z3.
9. **Enquanto a decisão D-01 não for tomada, município abaixo de 60.000
   habitantes devolve `nao_checada`** com o motivo "faixa sem regra de distância
   definida" **somado aos demais motivos que se apliquem àquela loja**, nunca
   `fere` nem `ok`. É a faixa de maior volume de pedidos e
   liberar em silêncio ali é o pior resultado possível (ver Pontos em aberto).
10. **O que NÃO muda com este card:** `POST /sources/search/warnings`
    (`api-orbita-nodejs/src/services/searchService.js:556`) continua existindo,
    continua checando **análises de ponto** no raio de 300 m e continua devolvendo
    `{ hasAnalysis }`.
11. **O que NÃO muda com este card:** o **raio de análise** do mapa. Ele é o
    círculo que o analista desenha para estudar a região: 300 m (`RANGE_MIN`,
    `webapp-orbita-angular/src/app/modules/view/view.component.ts:30`) a 6.500 m
    (`RANGE_FREE_MAX`, `:43`) em passos de 100 m, mais três valores-sentinela que
    **não são metros** — 6600, 6700 e 6800 significam "Município", "Mesoregião" e
    "Estado" (`RANGE_CUSTOM` `:33`, `RANGE_CUSTOM_NAME` `:34-38`, exibidos por
    `radiusLabel()` `:225-226`). São dois conceitos diferentes com números
    parecidos. **Não reaproveitar um no lugar do outro, e não supor que todo valor
    do slider é uma distância em metros.**

**Pontos em aberto:**

- **A distância mínima vale abaixo de 60 mil habitantes?** Decisão **D-01**,
  marcada como bloqueante: *"Faixa de maior volume fica sem veredito"*, dono
  "Expansão". A página do Confluence não trata o caso — no texto oficial a
  distância aparece amarrada às faixas de 60–120 mil e 120–200 mil. A regra 9
  deste card é um **default explícito** para o júnior não escolher sozinho, não
  uma decisão tomada.
- **Violação contra loja do próprio solicitante: `fere` ou `avisa`?** Decisão
  **D-09**, bloqueante, porque *"RN-06 e RN-11 hoje se contradizem"*. A página diz,
  em "Perfil do solicitante", que sobreposição com loja do próprio solicitante
  *"é efeito econômico a dimensionar, e pode ser uma escolha dele"* — o que
  sugere aviso —, mas a seção "Distância mínima entre lojas" não abre exceção.
  Este card **devolve o sinalizador** "é do próprio solicitante"; quem decide o
  efeito é o Z5, e a decisão ainda não existe.
- **Distância por coordenada ignorando divisa de município** (regra 5) é a
  decisão **D-10**, também bloqueante. A página v14 já a afirma (*"ponto em divisa
  de cidade também é avaliado"*), mas o rascunho a lista como pendente de dono.
  Confirmar qual vale.
- **Qual é a lista canônica de bandeiras?** *(Lacuna levantada na geração deste
  card — sem registro na página do Confluence nem no rascunho de regras; não é
  decisão numerada.)* A regra 1 depende de comparar "mesma" × "diferente", e isso
  exige uma lista fechada vinda do Radar. **Não localizada nestes 3
  repositórios.** Até ela chegar, usar fixture de bandeiras no teste, nunca
  literal de produção.
- **Qual raio de busca usar para encontrar as lojas candidatas?** A página não
  diz. O rascunho (RN-DADO-03) menciona busca *"num raio de 1.000 m do ponto"*.
  Confirmar: um raio de busca menor que 500 m perderia violações — e é
  exatamente por isso que o critério de aceite exige que a loja aprovada
  **apareça** na resposta, em vez de só estar ausente da lista de violações.
- **Impacto de 2ª ordem — a regra fica mais dura e ninguém mediu quanto.**
  Travar pelos dois endereços aumenta o número de pontos que violam, e o rascunho
  registra (decisão **D-18**, bloqueante) que *"a medição que sustenta RN-02 (...)
  foi feita com um único endereço por loja. Contando os dois, esses números sobem
  — quanto, ainda não foi medido. Remedir antes de levar os percentuais à
  liderança."*

**Critérios de aceite:**

- Dado um ponto a **250 m** de uma loja Farmarcas **da mesma bandeira
  pretendida** (mesmo id de bandeira), quando a checagem roda, então a loja volta
  com resultado `fere`, distância 250 m e limiar aplicado 300 m.
- Dado um ponto a **400 m** de uma loja Farmarcas **de bandeira diferente**,
  quando a checagem roda, então a loja volta com resultado `fere` e limiar
  aplicado 500 m.
- Dado um ponto a **400 m** de uma loja Farmarcas **da mesma bandeira**, quando a
  checagem roda, então essa loja **aparece na resposta** com resultado `ok`,
  distância 400 m, limiar 300 m e o endereço usado identificado. **Não basta ela
  estar ausente da lista de violações** — loja ausente da resposta é bug de raio
  de busca, não aprovação.
- Dado um pedido **sem bandeira pretendida informada** e um ponto a **400 m de
  exatamente uma** loja Farmarcas (qualquer bandeira), quando a checagem roda,
  então a loja volta com `fere` e limiar aplicado **500 m**.
- Dado uma loja cujo endereço da Receita está a **700 m** e cujo endereço popular
  está a **280 m** do ponto, quando a checagem roda, então a loja volta como
  violação, com distância **280 m** e endereço violador **popular**.
- Dado uma loja cujo endereço da Receita está a **150 m** e o popular a **280 m**,
  ambos abaixo de 300 m, quando a checagem roda, então a loja volta como violação
  **única** (não duplicada), com endereço violador **`ambos`** e distância
  **150 m** (a menor).
- Dado uma loja com coordenada **só** do endereço da Receita, a **700 m** do
  ponto, e **sem** coordenada do endereço popular, quando a checagem roda, então
  ela aparece com **dois resultados por endereço** — Receita `ok`, popular
  `nao_checada` — e o resultado consolidado da loja é **`nao_checada`**, nunca
  `ok`.
- Dado uma loja **sem coordenada em nenhum dos dois endereços**, quando a
  checagem roda, então ela aparece como `nao_checada` — e **não** como "sem
  violação".
- Dado uma loja a 200 m do ponto, **cadastrada em município diferente** do ponto,
  quando a checagem roda, então ela volta como violação (a divisa não isenta).
- Dado um ponto em cidade **acima de 200.000 habitantes** a 200 m de uma loja da
  mesma bandeira, quando a checagem roda, então o resultado é **`avisa`**, não
  `fere`.
- Dado um ponto em município **abaixo de 60.000 habitantes** a 200 m de uma loja
  da mesma bandeira, quando a checagem roda, então o resultado é **`nao_checada`**
  com o motivo "faixa sem regra de distância definida (D-01 pendente)" — e **não**
  `fere` nem `ok`.
- Não se pode fugir da seção Escopo do card
- Estar em conformidade com as regras de negócio
- Passar nos testes definidos por QA
- Conformidade com Figma: **não aplicável** (card de backend)

**Figma:** Não aplicável — card de backend.

**Estimativa:** [DEFAULT: 5 pts — confirmar com o time]
**Prioridade:** [DEFAULT: P0 — confirmar com o time]
**Dependências:** Z1 (camada de lojas) e **Z3** (faixa de população do município
— regras 8 e 9). **Bloqueia:** Z5, Z6.
**Revisado por (?_?) revisor-clareza-junior:** pronto para o júnior

---

## Z3 → SQO-1385

### [API] Teto de Grupos Econômicos por Município

**Contexto:**

**Comportamento atual.** O Órbita não sabe quantos grupos econômicos já operam num
município, nem qual é o teto daquela cidade. Conferido: não há nenhum serviço de
zoneamento, teto ou "ocupar vaga" nos 3 repositórios. A contagem é feita à mão,
conferindo faixa de população e lista de lojas por fora do produto.

**Por que está errado.** O teto é a checagem **mais barata e mais decisiva** do
zoneamento: responde "a cidade está fechada" sabendo apenas o município, sem
precisar do endereço exato. Feito à mão, cada pessoa conta de um jeito — e o que
se conta não é óbvio: o teto conta **grupos econômicos**, não lojas, e contam
também contratos assinados e análises aprovadas, que ainda não são lojas.

**Impacto de negócio de deixar como está.** O analista faz a análise de mercado
inteira de uma cidade que já estava fechada antes de ele começar. E quando a
contagem erra para o outro lado, entra um grupo a mais numa praça que não
comporta — o conflito entre associados que a regra existe para evitar.

**Alternativa descartada.** Contar o teto em **lojas** (como a página 4.5 do
Confluence ainda escreve hoje) foi descartado em favor de contar **grupos
econômicos**. Motivo registrado em
`outputs/regras-negocio-zoneamento-orbita.md`, "RN-02": contando grupos, 173
municípios deixam de estar acima do teto, e a proporção de cidades acima do teto
cai de ~25% para ~4%. Contar lojas barra o associado que quer abrir a segunda
loja dele na mesma cidade, o que não é o conflito que a regra protege.
⚠️ **Essa troca é a decisão D-00, ainda marcada como bloqueante e sem dono
nomeado** — ver Pontos em aberto.

Rastreabilidade: Confluence 4545904644 v14, seções "Regras de negócio → Teto de
lojas por cidade" e "→ Quem ocupa vaga na contagem". Números e a decisão em
`outputs/regras-negocio-zoneamento-orbita.md`, seções "0. O que este documento
pede de decisão" (D-00) e "RN-02 — Faixas de população e teto do município".

**Referências visuais:**
Não aplicável — card de backend. Quem mostra em tela é Z7 e Z8.

**Caminho/ideia de código:**

Card de backend, sem rota de UI. Onde a mudança entra: nova agregação em
`api-agent-orbita/src/services/radiusSearch/aggregations/`, reaproveitando a
resolução de município + população de `cityInfluence.ts`.

* **O que já existe:** `findMunicipalIndicators()` (`cityInfluence.ts:40`)
  resolve o município por `$geoIntersects` via `findMunicipality()` (`:12`) no
  campo `properties.CD_MUN` (`collections.ts:21`), converte o código para string
  (`cityInfluence.ts:50`) e busca a população na fonte `"População MM 2023"`
  (`SOURCE_NAMES.MUNICIPAL_POPULATION`, `collections.ts:14`) pela chave
  `properties.CODMUNIC` (`:27`), com o **valor em `properties.Populacao2023`**.
  **São dois nomes de campo para o mesmo código.** `findMunicipality()` **não é
  exportada** e precisa ser exportada ou extraída para ser reusada.
  O nome `populacao_municipios` que aparece no rascunho de regras **não existe no
  código** — não procurar por ele.
* 🪤 **ARMADILHA A NÃO HERDAR.** Esse leitor devolve
  `population: Number(population?.properties?.Populacao2023 ?? 0)`
  (`cityInfluence.ts:77`), ou seja, **município sem população na base vira 0
  habitantes**, que cai na faixa "até 60.000" e devolve **teto 1 grupo** — um
  veredito que parece certo e é inventado. O critério de aceite deste card exige
  `indeterminado` nesse caso. Ao reusar ou copiar essa função, **trocar o `?? 0`
  por propagação explícita de "não encontrado"**; e **não alterar** o
  comportamento dos outros consumidores sem avaliar o impacto neles — eles usam
  população como indicador, não como gate.
* ⚠️ As fontes de **contratos** e **análises** desta contagem **não foram
  localizadas nestes 3 repositórios** (`analysis_data` só aparece como fonte de
  mapa em `api-orbita-nodejs/src/services/searchService.js:558`). Essa parte do
  caminho é pergunta ao time, não pista.

**Escopo do card:**

* Criar a checagem de teto: dado o município do ponto pedido e o solicitante,
  devolver **três números separados** — grupos ocupando vaga **antes** do pedido,
  grupos **com** o pedido, e o **teto da faixa** — mais se o pedido cabe.
* **A API não devolve frase pronta.** O texto do veredito (Z5) é montado sobre
  esses números.
* Devolver também: a origem de cada ocupante (loja / contrato / análise), a lista
  de **ocupantes descartados com o motivo** do descarte, a **população usada** e a
  **fonte dela**.
* Devolver o sinalizador **"o pedido soma grupo novo?"**, que o Z4 consome.
* Usa o vocabulário de resultado definido no Z2 (`fere` / `avisa` /
  `nao_checada` / `ok`), mais `indeterminado` quando o município ou a população
  não são resolvíveis.
* **Não entra neste card:** a distância mínima (Z2), a regra de bandeira/modelo
  (Z4), o texto do aviso (Z5) e qualquer tela.

**Regras de negócio:**

1. **O teto é contado por município**, não por bairro nem por região.
2. **O teto conta grupos econômicos, não lojas.** O que a regra impede é a
   entrada de um **grupo novo** numa praça cheia, não a segunda loja de quem já
   está lá.
3. As faixas, com **cortes fechados** em 60.000, 120.000 e 200.000, são:
   | População do município | Teto |
   |---|---|
   | Até 60.000 | 1 grupo econômico, sem expansão adicional |
   | De 60.001 a 120.000 | até 2 grupos (o 2º entra com bandeira popular — ver Z4) |
   | De 120.001 a 200.000 | até 3 grupos (com alternância de bandeiras — ver Z4) |
   | Acima de 200.000 | sem teto; ocupação decidida por market share |
   "Corte fechado" significa que 60.000 está na primeira faixa e 60.001 na
   segunda — não há sobreposição.
4. **Acima de 200.000 habitantes não há nada a calcular:** a API devolve
   `sem_teto` mais um aviso de que a ocupação é decidida caso a caso pela
   Expansão por market share. **Não implementar nenhuma conta de market share** —
   ela não existe no produto.
5. **Ocupam vaga:** lojas com status `Ativado`, `Montando` ou `Transição`;
   contrato de expansão **assinado e vigente**; e **análise de ponto aprovada**.
   Contrato e análise ocupam vaga porque reservam a praça antes de a loja existir
   no cadastro.
6. **Não ocupam vaga:** lojas com status `Desativado`; e **contrato cancelado ou
   distratado, que deixa de ocupar vaga imediatamente** — não no fim do mês, não
   na próxima carga.
6-bis. **Contrato com status fora da lista conhecida sai como `nao_checada`, não
   como "não ocupa vaga".** `ContractStatus` tem apenas
   `NOT_STARTED | STARTED | CANCELED`
   (`webapp-orbita-angular/src/app/shared/models/analysis.model.ts:167-171`) e
   **não tem distrato**. Até a decisão de Pontos em aberto, **não** implementar
   distrato como sinônimo silencioso de `CANCELED`: tratar um status desconhecido
   como "não ocupa vaga" libera vaga sem que ninguém tenha encerrado nada.
7. **Um mesmo ponto conta uma única vez.** Um ponto que percorreu análise →
   contrato → loja existe nas três bases ao mesmo tempo; contá-lo três vezes
   fecharia a cidade sozinho. Vale a **origem mais avançada**: loja, depois
   contrato, depois análise.
8. **A contagem considera o cenário DEPOIS do pedido.** A pergunta que a API
   responde não é "quantos grupos há hoje", é "quantos haveria se este pedido for
   aprovado".
9. **O pedido sempre soma uma loja** (conta para a regra 12) **mas soma um grupo
   econômico apenas quando o solicitante ainda não responde por loja, contrato
   vigente ou análise aprovada naquele município.** Quem já está na cidade pedindo
   mais uma loja não consome vaga nova de grupo.
10. **Ser associado em outro município não dá vaga; estar naquela cidade, sim.**
    A vaga é por praça, não por rede.
11. **Uma loja ocupa vaga no município de cada um dos seus dois endereços.** Se o
    da Receita e o popular estão em municípios diferentes, ela ocupa vaga **nos
    dois**. Decidido em 2026-11-17, pela mesma lógica de travar dos dois lados do
    Z2. Consequência a conhecer: uma loja conta duas vezes na rede, e numa cidade
    de teto 1 isso basta para barrar qualquer pedido novo ainda que a operação
    real esteja em outro município.
12. **Excesso de lojas (não de grupos) é `avisa`, nunca `fere`.** Quando a
    cidade, já com o pedido, passar a ter mais **lojas** do que o número da faixa,
    o Órbita avisa — mas não bloqueia. O que bloqueia é grupo acima do teto.
13. **Município não resolvível ou população ausente devolve `indeterminado`**,
    com o motivo. Nunca "0 grupos", nunca "sem teto", nunca a faixa mais
    permissiva. Ponto sem município **não é cidade livre**.
14. **O que NÃO muda com este card:** nada do fluxo de criação de contrato na
    tela de análise. `getContractAction()`
    (`webapp-orbita-angular/src/app/modules/analysis/pages/view/view.component.ts:295`)
    e os modais `contract-create` / `contract-cancel` (`:222-226`) continuam como
    estão. Este card **lê** contratos, não muda como eles são criados.
15. **O que NÃO muda com este card:** as situações e status de análise existentes
    (`AnalysisSituation` e `AnalysisStatus`,
    `shared/models/analysis.model.ts:52-100`) não são alteradas. Este card só
    **lê** quais contam como aprovada.

**Pontos em aberto:**

- **O teto conta grupos ou lojas — quem assina?** A página v14 já diz "O teto
  conta grupos econômicos, não lojas". Mas o rascunho registra isso como decisão
  **D-00, bloqueante, dono "quem assina a 4.5/6.1"**, e na seção 7 registra que a
  página oficial 4.5 **ainda expressa o teto em lojas**. Ou seja: a regra 2 deste
  card contradiz a página oficial de zoneamento da empresa. **Confirmar que a 4.5
  foi corrigida antes de este card ir para desenvolvimento** — do contrário o
  produto aplica uma regra que o documento oficial não sustenta.
- **Qual fonte de população corta a faixa?** Decisão **D-08, bloqueante**. A
  página do Confluence **não diz qual fonte usar**. O rascunho propõe a base
  interna e registra duas consequências: (a) *"A base interna não é o Censo 2022 e
  seu ano de referência não está declarado em lugar nenhum da base"* — em
  Franca/SP registra 366.566 contra 352.536 do Censo 2022 (+4,0%), e **perto dos
  cortes de 60, 120 e 200 mil essa diferença troca a faixa e o teto**; (b) o
  dossiê de região corta pelo Censo 2022, então produto e dossiê divergem para o
  mesmo ponto. A recomendação registrada da revisão de liderança é **adotar o
  IBGE**. **Sem essa decisão a regra 3 não é implementável.**
- **Como o pedido identifica o grupo econômico do solicitante?** A regra 9 depende
  de saber se o solicitante já responde por loja/contrato/análise naquele
  município, mas o único campo de solicitante hoje é
  `Analysis.isAssociated?: boolean` (`shared/models/analysis.model.ts:121`) — um
  sim/não, **sem identificador de grupo**, e sem obrigatoriedade
  (`analysisIsInvalid()`, `modules/analysis/pages/view/view.component.ts:347-353`,
  só exige `lead` ou `map.main.id`). O Z9 torna o perfil obrigatório, mas continua
  booleano. **Decidir qual campo chega no pedido como chave do grupo (id do GE?
  CNPJ do solicitante?)** — sem ela a regra 9 não é implementável e **todo
  solicitante é tratado como novo, que é o lado que barra**. Relacionado a D-13.
- **Contrato e análise aprovada bloqueiam ou só alertam?** Decisão **D-14,
  bloqueante** (*"Dá poder de bloqueio a base que era histórico"*). A página diz
  que ocupam vaga, o que implica bloqueio. Confirmar.
- **Quais situações de análise contam como "aprovada"?** Decisão **D-07,
  bloqueante**: *"Sem a lista, a contagem não é aplicável nem conferível"*. O
  código tem `AnalysisSituation.APPROVED = 4` (`analysis.model.ts:58`), mas há **9
  situações** no enum (`:52-62`) e não está decidido se só `APPROVED` conta ou se
  `IN_VALIDATION`, `TO_SEND_STUDY` e outras também. **Não assumir que é só a 4.**
- **Por quanto tempo a reserva por análise aprovada vale?** Decisão **D-02**:
  *"Sem prazo, análise antiga bloqueia indefinidamente"*. Não tratado na página.
- **"Distratado" não existe no modelo atual.** A regra 6 exige que contrato
  "cancelado ou distratado" deixe de ocupar vaga imediatamente, mas
  `ContractStatus` tem apenas `NOT_STARTED | STARTED | CANCELED`
  (`shared/models/analysis.model.ts:167-171`). Confirmar se distrato é o mesmo que
  `CANCELED` ou um estado novo. A página também diz que *"o evento de distrato
  precisa chegar ao Órbita"*, o que sugere uma integração que não existe.
- **Onde moram contratos e análises para esta contagem?** Não localizado nestes 3
  repositórios.
- **Impacto de 2ª ordem — contagens divulgadas mudam.** Pela regra 11, uma loja
  com endereços em municípios diferentes conta duas vezes na rede; qualquer
  relatório de "lojas por município/UF" muda. E o rascunho registra (**D-18**,
  bloqueante) que os percentuais que sustentam a decisão do teto foram medidos com
  **um endereço só** e precisam ser remedidos antes de ir à liderança.
- **Impacto de 2ª ordem — quem cadastra passa a barrar.** Contrato e análise
  ganham poder de bloqueio. Quem cadastra contrato e quem conclui análise precisa
  saber **antes** de o gate entrar no ar. Fora do escopo deste card.

**Critérios de aceite:**

- Dado um município de **55.000 habitantes** (faixa até 60.000, teto 1) onde já há
  1 grupo ocupando vaga, e um solicitante **que não responde por nenhuma loja,
  contrato ou análise aprovada naquele município**, quando a checagem roda, então
  o resultado é **`fere`** e a resposta traz os três números separados: grupos
  **antes** do pedido = **1**, grupos **com** o pedido = **2**, teto = **1**.
- Dado o mesmo município e um solicitante **cujo grupo econômico é exatamente o do
  grupo que já ocupa a vaga** (loja `Ativado` lá), quando a checagem roda, então a
  resposta traz grupos antes = **1**, grupos com o pedido = **1** (não 2), o
  solicitante marcado como **já presente** com a origem do casamento (`loja`), e
  resultado **`ok` por teto** (a regra 12 de densidade é avaliada à parte e pode
  sair `avisa` no mesmo pedido). O que prova a regra 9 é o "grupos com o pedido =
  1" explícito, não a ausência de impedimento.
- Dado um município com exatamente **60.000 habitantes**, quando a faixa é
  calculada, então vale a faixa "até 60.000" (teto 1); com **60.001**, vale a
  faixa seguinte (teto 2).
- Dado um ponto cuja análise foi aprovada, virou contrato e depois virou loja
  cadastrada, quando a contagem roda, então ele conta **uma única vez**, pela
  origem **loja**.
- Dado um município cujo **único** ocupante é um contrato com status `CANCELED`,
  quando a contagem roda, então a cidade aparece com **0 grupos** **e** o contrato
  aparece na lista de **ocupantes descartados, com o motivo "contrato
  cancelado"** — ausência silenciosa não vale.
- Dado **o mesmo município e o mesmo contrato com status `STARTED`**, quando a
  contagem roda, então a cidade aparece com **1 grupo**, de origem **contrato**.
  *(Os dois cenários juntos provam que a base de contratos está sendo lida; o
  primeiro sozinho não prova nada.)*
- Dado uma loja com endereço da Receita no município A e endereço popular no
  município B, quando a contagem roda para A e depois para B, então ela ocupa vaga
  **nos dois**.
- Dado um município de **80.000 habitantes** (número da faixa = 2) que já tem
  **2 lojas de 1 único grupo**, e um pedido de **mais uma loja desse mesmo
  grupo**, quando a checagem roda, então **não há `fere` por teto** (continua 1
  grupo de 2) **e** sai o **`avisa` da regra 12** ("a cidade passa a ter 3 lojas
  para um número de faixa de 2").
- Dado um município **acima de 200.000 habitantes**, quando a checagem roda, então
  a resposta é `sem_teto` com o aviso de market share, e **nenhuma conta de market
  share é executada**.
- Dado um município **sem população na base**, quando a checagem roda, então o
  resultado é **`indeterminado`** — nunca `ok`, nunca teto 1, nunca a faixa mais
  permissiva. *(Este é o critério que a armadilha do `?? 0` em `cityInfluence.ts:77`
  viola: reusar aquela função sem alteração faz o teste falhar — e é para falhar.)*
- Dado um ponto cuja coordenada **não cai dentro de nenhum município** da base de
  municípios, quando a checagem roda, então o resultado é **`indeterminado`** com
  o motivo "município não identificado para a coordenada" — e **não** "0 grupos",
  "sem teto" nem lista vazia.
- **Distrato: sem critério de aceite neste card**, porque o status não existe no
  modelo (`ContractStatus`, `shared/models/analysis.model.ts:167-171`). O
  comportamento exigido enquanto isso está na **regra 6-bis**.
- Não se pode fugir da seção Escopo do card
- Estar em conformidade com as regras de negócio
- Passar nos testes definidos por QA
- Conformidade com Figma: **não aplicável** (card de backend)

**Figma:** Não aplicável — card de backend.

**Estimativa:** [DEFAULT: 8 pts — confirmar com o time]
**Prioridade:** [DEFAULT: P0 — confirmar com o time]
**Dependências:** Z1. **Bloqueia:** **Z2 (faixa de população)**, Z4, Z5.
**Revisado por (?_?) revisor-clareza-junior:** pronto para o júnior

---

## Z4 → SQO-1386

### [API] Regra de Bandeira e Modelo de Negócio por Faixa de População

**Contexto:**

**Comportamento atual.** O Órbita não avalia com qual bandeira ou modelo de
negócio um grupo novo pode entrar numa cidade. Não existe o conceito de **modelo
de negócio** (`Popular` / `Convencional`) em nenhum dos 3 repositórios — e, em
particular, `BrandModel`
(`webapp-orbita-angular/src/app/shared/models/brand.model.ts`) tem **apenas**
`id`, `name` e `assets`: **não há de onde derivar o modelo a partir da bandeira
hoje.**

*Dois falsos amigos, para não gastar tempo atrás deles:* grep por `Popular`
retorna 4 ocorrências que são rótulos de agrupamento de **redes concorrentes**
("Super/Ultra/Maxi/Mega Popular",
`modules/view/components/manage/components/categorization/components/grouping/new/new.component.ts:85,91,97,151`);
e grep por `bandeira` no backend retorna
`api-agent-orbita/src/services/radiusSearch/aggregations/competitiveMap.ts:19-29`,
onde `"BANDEIRA"` é só uma das chaves para extrair o **nome de um concorrente**.

**Por que está errado.** O teto do Z3 responde "cabe mais um grupo nesta
cidade?", mas não responde "cabe **com esta bandeira**?". A regra de expansão
exige que, na faixa de 60.001 a 120.000 habitantes, o **segundo grupo da cidade**
entre com bandeira de modelo **Popular** — e entrar com Convencional fere o
zoneamento, mesmo havendo vaga. Sem essa checagem, o produto diz "pode entrar"
para um pedido que a regra barra.

**Impacto de negócio de deixar como está.** O pedido é liberado pelo teto, segue
para a análise de mercado, chega ao contrato, e a violação só aparece quando
alguém que conhece a regra olha o caso. O custo é a análise inteira mais o
retrabalho de desfazer uma expectativa já criada com o empresário.

**Alternativa descartada.** Exigir bandeira `Popular` da **2ª loja** da cidade —
que é como a página oficial 4.5 ainda escreve hoje — foi descartado em favor de
exigir do **2º grupo econômico**. Motivo: contando lojas, o associado que já está
na praça e quer abrir a segunda loja dele seria obrigado a trocar de bandeira, o
que não é o conflito que a regra existe para evitar (é a mesma troca
lojas→grupos do Z3). ⚠️ **Ressalva:** essa troca é a decisão **D-00**, ainda
bloqueante e sem dono nomeado — a alternativa foi descartada no Confluence v14,
mas a página oficial 4.5 ainda sustenta a outra.

Rastreabilidade: Confluence 4545904644 v14, seção "Regras de negócio → Bandeira e
modelo de negócio". Divergência com a página oficial em
`outputs/regras-negocio-zoneamento-orbita.md`, "RN-05 — Bandeira popular do 2º
grupo (faixa 60–120 mil)" e seção 7.

**Referências visuais:**
Não aplicável — card de backend.

**Caminho/ideia de código:**

Card de backend, sem rota de UI. Esta checagem nasce junto com a do Z3 e deve
viver **no mesmo serviço** que ele — e **em qual serviço o motor de zoneamento
mora ainda não está decidido** (mesmo bloqueio registrado no Z5).

Onde a bandeira vive hoje, para quem for ler o código: `getBrands()` em
`webapp-orbita-angular/src/app/shared/services/brand.service.ts:15`, que busca
`${apiCommon}/brand/all` (`:25`, com `apiCommon = environment.api.common` em
`src/app/core/http/http.base.service.ts:10`) — **uma quarta API, fora destes 3
repositórios**; consumida em
`modules/analysis/pages/view/view.component.ts:175` (`loadBrands()`, `:172-179`,
chamada no `ngOnInit` em `:123`) e exibida no select "Bandeira" em
`modules/analysis/pages/view/view.component.html:39`.

**Escopo do card:**

* Criar a checagem de bandeira/modelo: dado o município, a **faixa de população**
  e o pedido (id da bandeira pretendida + modelo de negócio + o sinalizador **"o
  pedido soma grupo novo?"** vindo do Z3), devolver se a combinação `fere`,
  `avisa`, é `nao_avaliada` ou `sem_apontamento`. *(Esse sinalizador é o mesmo
  insumo que em outros pontos aparece como "o solicitante já está na cidade" —
  **modelar um campo só**, com o nome do Z3.)*
* **Faixa de população** é o recorte da **regra 3 do Z3**, com cortes fechados.
  Este card **não recalcula** a faixa: consome a que o Z3 devolveu, inclusive a
  fonte de população, porque é ela que o Z5 precisa imprimir.
* Consumir do **Z3**: a faixa, a **contagem de grupos que ocupam vaga antes do
  pedido** e o sinalizador **"o pedido soma grupo novo?"**. ⚠️ O escopo do Z3 não
  promete uma "posição ordinal do grupo" — quem deriva 1º/2º/3º é **este** card,
  pela regra 2. Se a equipe preferir que o Z3 entregue a posição pronta, isso é
  mudança no escopo do Z3 e precisa ser combinada antes.
* **Não entra neste card:** a contagem do teto (Z3), a distância (Z2), o texto do
  aviso (Z5) e qualquer tela.

**Regras de negócio:**

1. **Na faixa de 60.001 a 120.000 habitantes, o grupo que entra como SEGUNDO da
   cidade deve abrir com bandeira de modelo `Popular`.** A exigência recai sobre
   o **2º grupo**, não sobre "a 2ª loja": se um grupo já presente abre a quinta
   loja dele, ele continua sendo o 1º grupo.
2. **"Entra como segundo grupo" é, operacionalmente, a conjunção de duas
   condições**, ambas calculadas pelo Z3: (a) o pedido **soma um grupo novo** —
   o solicitante não responde por loja, contrato vigente nem análise aprovada
   naquele município (Z3, regra 9); **e** (b) a contagem de grupos que ocupam vaga
   **antes** do pedido é exatamente **1**. Se (a) for falso, aplica-se a regra 4.
   Se a contagem antes do pedido for 0, aplica-se a regra 3.
3. **Pedido que entra como PRIMEIRO grupo da cidade não tem exigência de bandeira
   nem de modelo, em nenhuma faixa.** Todas as regras deste card saem como
   `sem_apontamento` — e isso **não é** `nao_avaliada`: não falta dado, falta
   regra aplicável.
4. **Se o pedido traz o segundo grupo da cidade na faixa 60.001–120.000 e o
   modelo é `Convencional`, o resultado é `fere`.** É impedimento, não aviso.
5. **Se o pedido é de loja adicional de um grupo que JÁ está na cidade, a
   exigência de bandeira `Popular` não se aplica: o resultado é `avisa`, nunca
   `fere`.** Conteúdo do aviso: "o grupo já ocupa vaga neste município; a
   exigência de bandeira Popular do 2º grupo não foi aplicada". **Este aviso não é
   o aviso de densidade do Z3 (regra 12)** — são dois fatos distintos e, se os dois
   ocorrerem, o Z5 imprime os dois, cada um com a sua regra nomeada.
6. **Se o modelo de negócio não for informado no pedido, a regra sai como
   `nao_avaliada` — nunca como "passou".** "Não avaliada" e "passou" são
   resultados diferentes e precisam sair diferentes.
   **Como isso chega ao veredito (Z5):** `fere` → `impedimento`, `avisa` →
   `alerta`, `nao_avaliada` → `indeterminado` **somente quando a regra era
   aplicável àquele pedido** (faixa 60.001–120.000 **e** pedido de 2º grupo),
   `sem_apontamento` → não entra no veredito. **Fora da faixa, ou quando o pedido
   não é o 2º grupo, a ausência do modelo NÃO gera `indeterminado`** — a regra
   simplesmente não se aplica. Sem essa ressalva, **todo** pedido viraria
   `indeterminado`, porque hoje nenhum ponto do produto informa modelo de negócio.
7. **Na faixa de 120.001 a 200.000 habitantes, se a cidade já tiver loja da
   bandeira pretendida, o resultado é `avisa` — nunca `fere`.** É a "alternância
   de bandeiras" da faixa: preferência por bandeira diferente, não proibição.
   Para esta regra, "já tiver loja" usa **o mesmo conjunto de status que ocupa
   vaga no Z3, regra 5** (`Ativado`, `Montando`, `Transição`); `Desativado` não
   conta. Conta **qualquer** loja daquela bandeira no município, do solicitante ou
   de outro grupo: a regra é sobre a bandeira presente na praça, não sobre quem a
   opera. *(Nenhum dos dois recortes está escrito na fonte — confirmar; estão aqui
   como default explícito.)*
8. **Acima de 200.000 habitantes este card não tem nenhuma regra a aplicar:**
   todas as suas regras saem como `sem_apontamento`. **O aviso de market share é
   do Z3 (regra 4) e não deve ser emitido aqui** — se os dois emitirem, o veredito
   imprime a mesma frase duas vezes.
9. **O que NÃO muda com este card:** a lista de bandeiras oferecida hoje na tela
   de análise continua como está (`getBrands()`, caminho acima). Este card **lê** a
   bandeira escolhida; não muda de onde a lista vem nem quais opções aparecem.
10. **O que NÃO muda com este card:** o teto numérico de grupos por faixa (Z3).
    Este card nunca altera quantos grupos cabem; só diz **com qual
    bandeira/modelo** o grupo pode entrar.
11. **O que NÃO muda com este card:** a camada Concorrentes e as chaves que ela
    usa para extrair nome de loja concorrente (`STORE_NAME_PROPERTY_KEYS`, que
    inclui `"BANDEIRA"`, em `competitiveMap.ts:19-29`). **Esse campo não é a
    bandeira Farmarcas** e não pode ser usado para comparar "mesma bandeira".

**Pontos em aberto:**

- **"Modelo de Negócio" é campo do pedido ou derivado da bandeira?** Decisão
  **D-13**: *"Define se é pergunta ao analista ou consulta à base"*, dono "Produto
  + Radar". A página lista Modelo de Negócio como campo da **carga de lojas**
  (Z1), mas a regra 6 fala em modelo informado **no pedido**. **São coisas
  diferentes e nenhuma das duas está pronta:**
  - *Derivar da bandeira* **não é possível com o contrato atual**: `BrandModel`
    tem só `id`, `name`, `assets`, e a lista é servida por `${apiCommon}/brand/all`
    — **uma quarta API**, fora destes 3 repositórios. Derivar exige mudar esse
    contrato, com um time que não é o do Órbita.
  - *Perguntar ao analista* exige **campo novo na tela de análise, que não
    existe** (o formulário tem `brand` em `analysis.model.ts:116`, nenhum campo de
    modelo). **Não reaproveitar "Tipo de Loja"** (`AnalysisStoreType` =
    `Nova`/`Conversão`/`Mudança de Ponto`, `analysis.model.ts:16-27`) — é outra
    coisa.
  - **Consequência de cronograma:** enquanto nenhuma das duas existir, a regra 1
    **nunca consegue concluir** — toda avaliação cai em `nao_avaliada`. Isso
    precisa estar claro para quem prioriza.
- **A página oficial 4.5 diz outra coisa** ("a 2ª loja deve ser popular" × "2º
  grupo"). Mesma decisão **D-00** do Z3, bloqueante e sem dono nomeado.
- **"Alternância de bandeiras" na faixa 120–200 mil está definida?** A página diz
  "até 3 grupos, com alternância de bandeiras" e, mais abaixo, que se a cidade já
  tiver loja da bandeira pretendida o Órbita **avisa, sem bloquear**. Confirmar que
  alternância é só isso — preferência avisada — e não uma regra de ordem.
- **O que acontece na faixa até 60.000 habitantes?** A página não dá nenhuma regra
  de bandeira para essa faixa, e o teto lá é 1 grupo. Confirmar se é mesmo "nada a
  avaliar".
- **A regra 5 pede mesmo um aviso, ou o esperado é silêncio?** A página do
  Confluence não é explícita neste ponto.
- **Lista canônica de bandeiras com o modelo de cada uma:** mesma lacuna do Z2.
  Não localizada nestes 3 repositórios.

**Critérios de aceite:**

- Dado um município de **80.000 habitantes** com 1 grupo ocupando vaga, e um
  pedido de **grupo novo** com bandeira de modelo **`Convencional`**, quando a
  checagem roda, então o resultado é **`fere`**, citando a exigência de bandeira
  Popular para o 2º grupo.
- Dado o mesmo cenário com bandeira de modelo **`Popular`**, quando a checagem
  roda, então a regra sai como **`sem_apontamento`** e **nenhuma** entrada deste
  card chega ao veredito do Z5 — o `liberado` final é decidido pelo Z5, depois de
  somar Z2 e Z3.
- Dado um município de **80.000 habitantes com 0 grupos ocupando vaga** e um
  pedido de grupo novo com modelo `Convencional`, quando a checagem roda, então o
  resultado é **`sem_apontamento`** (o pedido é o 1º grupo) — **não**
  `nao_avaliada`, **não** `fere`.
- Dado um município de 80.000 habitantes e um pedido de **loja adicional de um
  grupo que já está na cidade**, com modelo `Convencional`, quando a checagem
  roda, então o resultado é **`avisa`**, não `fere`.
- Dado um pedido de **2º grupo na faixa 60.001–120.000 sem modelo de negócio
  informado**, quando a checagem roda, então a regra sai como **`nao_avaliada`** —
  e o resultado **não** é "passou".
- Dado um pedido **sem modelo de negócio** num município de **40.000
  habitantes**, quando a checagem roda, então todas as regras saem como
  **`sem_apontamento`** — e **não** `nao_avaliada` (a regra não se aplicava).
- Dado um pedido com **bandeira pretendida informada mas sem modelo de negócio
  correspondente na origem do dado**, quando a checagem roda, então o resultado é
  **`nao_avaliada`** com o motivo "modelo de negócio da bandeira X não encontrado"
  — e **não** é tratado como `Convencional` nem `Popular` por default.
- Dado um município **sem população na base**, de modo que o Z3 devolveu
  `indeterminado` para a faixa, quando a checagem de bandeira roda, então ela
  devolve **`nao_avaliada`** com o motivo "faixa de população indeterminada" — e
  **nunca** assume a faixa mais permissiva nem conclui `sem_apontamento`.
- Dado um município de **150.000 habitantes** que já tem loja da bandeira
  pretendida (status que ocupa vaga), quando a checagem roda, então o resultado é
  **`avisa`**, não `fere`.
- Dado um município de **150.000 habitantes** com 2 grupos ocupando vaga e um
  pedido de grupo novo com bandeira **que ainda não existe na cidade**, quando a
  checagem roda, então não há `fere` nem `avisa` por este card.
- Dado um município de **250.000 habitantes**, quando a checagem roda, então todas
  as regras saem `sem_apontamento` e **nenhum aviso de market share é emitido por
  este card** (ele é do Z3).
- Não se pode fugir da seção Escopo do card
- Estar em conformidade com as regras de negócio
- Passar nos testes definidos por QA
- Conformidade com Figma: **não aplicável** (card de backend)

**Figma:** Não aplicável — card de backend.

**Estimativa:** [DEFAULT: 3 pts — confirmar com o time]
**Prioridade:** [DEFAULT: P1 — confirmar com o time]
**Dependências:** Z3 (faixa, contagem de grupos e "soma grupo novo?"), Z1
(bandeiras das lojas). **Bloqueia:** Z5.
**Revisado por (?_?) revisor-clareza-junior:** pronto para o júnior

---

## Z5 → SQO-1387

### [API] Veredito de Zoneamento com Motivo, Números e Rastreabilidade

**Contexto:**

**Comportamento atual.** A única coisa parecida com um veredito no produto é
`POST /sources/search/warnings`, que devolve `{ hasAnalysis: boolean }`
(`api-orbita-nodejs/src/services/searchService.js:566`) — um booleano, sem
motivo, sem número, sem contra o quê. O front traduz isso num toast de texto fixo
(`webapp-orbita-angular/src/app/modules/view/view.component.ts:360-364`) e, quando
a chamada falha, num **segundo toast de erro** (`:367-373`) — esse segundo toast é
o precedente que já existe no produto para "falha não vira silêncio", e é o
comportamento que a regra 7 generaliza.

**Por que está errado.** Um aviso que só diz que algo está errado informa ao
analista que ele perdeu tempo, mas não diz o que fazer em seguida. A página do
Confluence é explícita: *"Nenhum aviso pode dizer apenas que o ponto fere o
zoneamento"*. E sem um veredito único, os três pontos de disparo (mapa, salvar,
Órbita IA) montariam cada um o seu texto, e o mesmo ponto receberia explicações
diferentes em telas diferentes.

**Impacto de negócio de deixar como está.** Quando o impedimento é automático e o
motivo não é explicável, o analista vira mensageiro de *"seu pedido foi negado por
um motivo que não posso explicar"* — e o caso escala direto para a diretoria, caso
a caso, que é exatamente o custo que este trabalho existe para eliminar. Sem
registro dos números que sustentam o veredito, também não há como contestar nem
auditar uma decisão depois.

**Alternativa descartada.** Deixar cada tela montar seu próprio texto a partir dos
resultados brutos de Z2/Z3/Z4 foi descartado: a página exige que *"o modal traz a
mesma explicação exigida nas demais validações"*, ou seja, um único formato para
os três momentos.

Rastreabilidade: Confluence 4545904644 v14, seção "Regras de negócio → Conteúdo
obrigatório do aviso", mais as linhas de registro do veredito nas seções
"Validação 2" e "Análise feita pelo Órbita IA". Detalhamento em
`outputs/regras-negocio-zoneamento-orbita.md`, "RN-18.1 — Todo aviso explica o
motivo" e "RN-13 — Rastreabilidade do veredito".

**Referências visuais:**
Não aplicável — este card não desenha nem exibe tela. O Figma do conteúdo do
veredito em tela é pré-requisito dos cards **Z6, Z7 e Z8**.

**Caminho/ideia de código:**

Card de backend, sem rota de UI. O veredito é consumido por Z6, Z7, Z8 e
persistido pelo Z10.

> ⚠️ **PRÉ-REQUISITO PARA INICIAR — não é só um ponto em aberto, é um bloqueio.**
> Não existe serviço de zoneamento em nenhum dos 3 repositórios. Os dois
> candidatos e o que cada um implica:
> - **`api-orbita-nodejs`** é quem o mapa já consome (Z6), mas monta apenas
>   `/health`, `/imports`, `/sources`, `/markers`, `/grouping`, `/graphic`
>   (`app.js:52-57`) — **não serve `/expansion`**, que é quem o Z7 precisa chamar
>   ao salvar;
> - **`api-agent-orbita`** é quem tem as bases municipais
>   (`src/constants/collections.ts:14`) e as agregações por raio
>   (`src/services/radiusSearch/`), mas **não é chamado pelo fluxo de salvar**.
>
> Nenhum dos dois atende Z6 e Z7 ao mesmo tempo sem uma decisão de arquitetura.
> **Definir o serviço host antes de abrir a sprint** — o júnior não tem como
> começar sem isso.
>
> **Além do serviço host, duas outras decisões travam o início deste card:** o
> **aceite da precedência** da regra 2 pelo Produto e a **mecânica do rótulo
> anônimo** da regra 5. Sem as três, o card não entra em sprint.

**Escopo do card:**

* Definir e implementar **um único formato de veredito de zoneamento**, montado a
  partir dos resultados de Z2 (distância), Z3 (teto) e Z4 (bandeira/modelo).
* O veredito tem **um** resultado entre `liberado`, `alerta`, `impedimento`,
  `indeterminado` (ver regra 1).
* Para cada regra ferida, avisada ou não avaliada, o veredito traz: **qual
  regra** e **qual limiar** foi aplicado; **contra o quê** (a loja — bandeira,
  bairro ou endereço, status, distância medida, se é do próprio solicitante — ou a
  contagem — quantos grupos e qual o teto); e, **quando a regra é de distância**,
  **contra qual endereço** (ver regra 3).
* O veredito carrega sempre: os **números que o sustentam** (população e sua
  fonte, lojas, grupos, distâncias), a **data da carga do Radar** (do Z1b), as
  **lacunas declaradas**, e **quando ele foi calculado**.
* **Não entra neste card:** desenhar ou exibir qualquer tela (Z6, Z7, Z8), nem
  persistir o veredito junto da análise (Z10).
* **Não entra neste card:** fluxo de exceção aprovada (quem aprova, validade,
  motivo). A página v14 não trata exceção — **não implementar override**.

**Regras de negócio:**

1. **Os quatro resultados possíveis, e só eles:**
   | Resultado | Quando sai | O que significa |
   |---|---|---|
   | `impedimento` | Pelo menos uma regra foi **ferida** (distância abaixo do limiar — Z2; grupos acima do teto — Z3; 2º grupo com modelo `Convencional` na faixa 60–120 mil — Z4) | A regra barra o ponto. Não é "atenção": é "não pode" |
   | `alerta` | Nenhuma regra ferida, mas pelo menos um **aviso** (densidade de lojas — Z3 regra 12; descumprimento de distância acima de 200 mil hab — Z2 regra 8; bandeira repetida na faixa 120–200 mil — Z4 regra 7; loja adicional de grupo já presente na faixa 60–120 mil — Z4 regra 5) | O ponto pode seguir; há um fato a considerar. **`alerta` e "aviso" são a mesma coisa** — `alerta` é o valor no contrato, "aviso" é a palavra em tela |
   | `indeterminado` | Faltou dado ou a checagem não concluiu (regras 6 e 7) | A regra **não foi aplicada**. Nunca ler como liberação |
   | `liberado` | Todas as regras aplicáveis rodaram e nenhuma feriu nem avisou | O ponto passa no zoneamento |
   Uma regra que **não se aplica** àquele pedido **não é** `indeterminado`: ela
   simplesmente não entra no veredito.
2. **O veredito é um só, e a precedência entre as três checagens é explícita:**
   `impedimento` > `indeterminado` > `alerta` > `liberado`. Basta **uma** regra
   ferida para o veredito ser `impedimento`, mesmo que outra checagem tenha ficado
   `indeterminado`; sem nenhuma regra ferida, basta **uma** checagem incompleta
   para o veredito ser `indeterminado`, mesmo que o resto tenha passado;
   `liberado` só sai quando nada feriu, nada avisou e nada ficou faltando.
   **Independentemente do resultado final, o veredito lista TODAS as regras
   feridas, avisadas e não avaliadas** — a precedência decide o rótulo, não o que é
   mostrado. Um impedimento que esconde um dado faltando faz o analista corrigir o
   ponto e ser barrado de novo por outro motivo.
   ⚠️ **Esta precedência NÃO está escrita na fonte** (nem na página v14 nem no
   rascunho). Está proposta aqui para o card ser implementável e **precisa de
   aceite do Produto antes de desenvolver** — ver Pontos em aberto.
3. **Nenhum veredito pode dizer apenas que o ponto fere o zoneamento.** O texto
   obrigatório tem três partes: (a) a regra ferida, com o limiar aplicado; (b)
   contra o quê — a loja ou a contagem, com os dados listados no Escopo; (c)
   contra **qual dos dois endereços da loja**. **A parte (c) só existe quando a
   regra ferida é a de distância (Z2)**, porque é a única que compara
   coordenadas. Em impedimento por teto (Z3) ou por bandeira/modelo (Z4) o campo
   sai **ausente** — nunca preenchido com "ambos", "n/a" ou string vazia, que o
   front leria como dado existente.
4. **Nome de pessoa nunca aparece.** O responsável pelo grupo econômico vem na
   carga do Z1 porque liga o solicitante ao grupo, mas é dado pessoal (LGPD) e não
   sai no veredito — nem em tela, nem no registro do Z10.
5. **Os grupos econômicos aparecem com rótulo anônimo, estável dentro do
   município.** "Estável" significa que o mesmo grupo recebe o mesmo rótulo em
   **qualquer** consulta futura daquela cidade — em outra sessão, em outro dia, e
   **mesmo depois de outro grupo entrar ou sair do município**. **Não serve um
   contador por requisição nem um ordinal recalculado a cada consulta:** os dois
   passam num teste de duas chamadas seguidas e quebram em produção. O rótulo não
   precisa ser estável **entre** municípios. ⚠️ **A mecânica ainda não foi
   decidida** (ver Pontos em aberto): enquanto não for, esta regra **não é
   implementável**.
6. **`indeterminado` não é liberação.** Quando falta dado para aplicar uma regra
   **que era aplicável àquele pedido**, o veredito é `indeterminado` e **diz qual
   dado falta e qual regra ficou sem resposta**. Exemplos: população ausente → a
   faixa não sai → teto (Z3) e bandeira (Z4) ficam sem resposta; carga do Radar
   acima do limite de defasagem → distância e teto ficam sem resposta; modelo de
   negócio não informado **num pedido de 2º grupo na faixa 60.001–120.000**.
   **Mas** modelo de negócio não informado num município de 40 mil habitantes, ou
   num pedido de loja adicional, **não** gera `indeterminado`: a regra do Z4 não se
   aplicava.
   *Nota de realidade:* hoje o produto **não tem** campo de modelo de negócio em
   lugar nenhum. Sem essa ressalva, este card faria **todo** veredito sair
   `indeterminado` no dia em que subisse.
7. **Falha ou demora não liberam.** Se a consulta não concluir (carga
   indisponível, timeout, erro, permissão negada), o resultado é `indeterminado` e
   o veredito diz isso. Um gate que falha aberto é pior que gate nenhum, porque
   cria a confiança de que a checagem aconteceu.
8. **O veredito é produzido mesmo quando não há nada a apontar.** Quando tudo
   passa, o resultado é `liberado` com os números que o sustentam — é esse objeto
   que o Z10 registra. Quem decide **não mostrar nada em tela** nesse caso é o Z7 e
   o Z8; este card **sempre** devolve o veredito.
9. **O que NÃO muda com este card:** `POST /sources/search/warnings` e o
   `{ hasAnalysis }` que ele devolve continuam existindo como estão
   (`searchService.js:556-566`). Esse contrato — `SearchWarningsResponse` em
   `webapp-orbita-angular/src/app/shared/models/source.model.ts:394-396` — é
   exatamente **o formato que NÃO deve ser copiado**: é o booleano sem motivo que
   este card existe para não repetir.

**Pontos em aberto:**

- **Como se combinam resultados divergentes das três checagens?** A página v14
  define o **conteúdo** do aviso (*"Nenhum aviso pode dizer apenas que o ponto fere
  o zoneamento"*) mas **não define a precedência** entre `impedimento`, `alerta` e
  `indeterminado` quando duas checagens discordam — nem a página, nem o rascunho. A
  regra 2 propõe `impedimento > indeterminado > alerta > liberado` como default
  explícito, **mas isso é decisão de Produto e precisa de aceite**: é a régua do
  gate, mesmo dono da régua de viabilidade. Sem aceite, dois pontos equivalentes
  podem receber vereditos diferentes conforme quem implementou.
- **Em que serviço este veredito mora?** Ver o bloqueio em Caminho/ideia de
  código. É a primeira decisão do card.
- **Como se produz o rótulo anônimo estável?** A página diz "rótulo anônimo,
  estável dentro do município" **sem definir a mecânica**. Confirmar: derivado do
  identificador de grupo do Radar? Ordinal persistido por município? A escolha
  muda o que acontece quando um grupo entra ou sai da cidade — e a regra 5 não é
  implementável sem isso.
- **Quais lacunas saem em quais vereditos?** O rascunho registra (RN-13.2) que
  *"se todas as ressalvas imprimirem em todo veredito, a tela vira parede de texto
  e o analista para de ler — inclusive a que importa"*, e propõe que a lacuna só
  saia quando afeta aquele veredito. A página v14 **não traz essa restrição**.
  Confirmar qual vale: a diferença é entre um veredito legível e uma parede de
  texto.
- **"O que destravaria" entra ou não?** O rascunho pede que o aviso diga
  *"faltam 120 m"*, *"a cidade está fechada, 2 de 2 grupos"*, *"cabe se o modelo
  for Popular"* (RN-18.1 e RN-13.1). A página v14 **não lista isso entre os itens
  obrigatórios**. Confirmar — é o que transforma o aviso de "você perdeu tempo" em
  "faça isto a seguir", e o layout do modal (Z6) depende da resposta.
- **Violação contra loja do próprio solicitante: `impedimento` ou `alerta`?**
  Mesma pendência do Z2 (decisão **D-09**, bloqueante). Este card recebe o
  sinalizador, mas **não há decisão sobre qual resultado atribuir**: a regra 3 sabe
  o que escrever e o veredito não sabe o que concluir.
- **O veredito registra a versão da regra aplicada?** A página v14 não lista isso
  entre os obrigatórios, mas as regras de teto e bandeira estão em mudança agora
  (D-00). Sem versão, um veredito registrado pelo Z10 **não é reconstruível**
  depois que a regra mudar. *(Proposto no Escopo como "quando foi calculado";
  confirmar se a versão da regra entra junto.)*
- **Alvo de tempo de resposta.** Decisão **D-17**: o gate passa a estar no caminho
  crítico de toda entrada de análise e não há alvo declarado. Sem ele, a regra 7
  (timeout vira `indeterminado`) não tem um número para aplicar.

**Critérios de aceite:**

- Dado um ponto a 250 m de uma loja Farmarcas da mesma bandeira, quando o veredito
  é montado, então ele traz: resultado `impedimento`, a regra "distância mínima",
  limiar **300 m**, distância medida **250 m**, a bandeira e o status da loja, qual
  dos dois endereços violou, e a data da carga do Radar.
- Dado um ponto em cidade de 55.000 habitantes já com 1 grupo, quando o veredito é
  montado, então ele traz: `impedimento`, a regra "teto de grupos", a contagem
  "1 de 1", a população usada **e a fonte dela**.
- Dado um impedimento **por teto de grupos**, quando o veredito é montado, então o
  campo "contra qual endereço" vem **ausente** — não vazio, não "n/a", não "ambos".
- Dado um ponto em cidade **acima de 200.000 habitantes** a 200 m de uma loja da
  mesma bandeira (Z2 regra 8 → `avisa`) e nada mais ferido, quando o veredito é
  montado, então o resultado é **`alerta`** — nem `impedimento` nem `liberado`.
- Dado um ponto com **uma regra ferida** (teto) **e um aviso** (densidade), quando
  o veredito é montado, então o resultado é **`impedimento`** e o veredito lista
  **as duas** entradas — o aviso não some porque o impedimento prevaleceu.
- Dado um ponto que **fere a distância** e cujo município **não tem população na
  base**, quando o veredito é montado, então o resultado é **`impedimento`** (a
  regra ferida prevalece) e o veredito declara, junto, que o teto ficou **não
  avaliado por falta de população**.
- Dado um pedido de **2º grupo na faixa 60.001–120.000 sem modelo de negócio
  informado** e nada mais ferido, quando o veredito é montado, então o resultado é
  **`indeterminado`**, dizendo que falta o modelo — **nunca** `liberado`.
- Dado **o mesmo pedido num município de 40.000 habitantes**, quando o veredito é
  montado, então o resultado **não** é `indeterminado` por causa do modelo — a
  regra do Z4 sai como não aplicável e não entra.
- Dado que a última carga do Radar está **acima do limite de defasagem** (Z1b
  regra 3), quando o veredito é montado, então o resultado é **`indeterminado`**,
  com a data da carga e qual regra ficou sem resposta — e **não** uma contagem de
  lojas sobre dado velho.
- Dado um ponto sem nenhuma violação nem aviso, quando o veredito é montado, então
  o resultado é `liberado` **e os números que o sustentam vêm junto** (não é um
  veredito vazio).
- Dado que a consulta deu **timeout** ou voltou **403/sem permissão**, quando o
  veredito é montado, então o resultado é `indeterminado` com o motivo — **nunca**
  `liberado` e **nunca** resposta vazia.
- Dado uma violação contra loja de outro associado, quando o veredito é montado,
  então o grupo aparece com **rótulo anônimo** e **nenhum nome de pessoa** aparece
  em campo nenhum.
- Dado dois vereditos para o mesmo município gerados **em sessões diferentes e com
  um terceiro grupo tendo entrado na cidade entre os dois**, quando ambos citam o
  mesmo grupo econômico, então o rótulo anônimo é **o mesmo** nos dois. *(Um
  contador por requisição ou ordinal recalculado **não** atende.)*
- Dado um ponto com uma loja vizinha **sem coordenada**, quando o veredito é
  montado, então a lacuna "loja não checada na distância" aparece declarada — e
  essa loja **não** aparece como "não violou".
- Não se pode fugir da seção Escopo do card
- Estar em conformidade com as regras de negócio
- Passar nos testes definidos por QA
- Conformidade com Figma: **não aplicável** (sem tela neste card)

**Figma:** Não aplicável a este card — ele não desenha nem exibe tela. O Figma do
veredito em tela é pré-requisito de **Z6, Z7 e Z8**, e a página do Confluence
registra "A ser construído": solicitar ao design por aqueles cards.

**Estimativa:** [DEFAULT: 5 pts — confirmar com o time]
**Prioridade:** [DEFAULT: P0 — confirmar com o time]
**Dependências:** Z2, Z3, Z4. **Bloqueia:** Z6, Z7, Z8, Z10.
**Revisado por (?_?) revisor-clareza-junior:** pronto para o júnior

---

# Épico C — Disparo na interface

> ⚠️ **Vale para Z6, Z7 e Z9:** o clone local do `webapp-orbita-angular` está em
> `733e887` (2024-05-09) e **nenhuma branch remota é mais nova**. Confirmar com o
> time qual é o repositório do front em produção antes de estes cards entrarem em
> sprint — ver o aviso no topo deste documento.

## Z6 → SQO-1334

### [Mapa] Modal de Zoneamento ao Carregar o Ponto

**Contexto:**

**Comportamento atual.** No mapa do Órbita (rota `/view`), quando o analista
escolhe um ponto, o front já dispara uma checagem automática:
`checkNearbyAnalysis()`
(`webapp-orbita-angular/src/app/modules/view/view.component.ts:343`), chamada no
`ngOnInit` (`:168`) e a cada mudança de `main` ou `radius` (`:169-171`). Ela chama
`POST /sources/search/warnings` e, se vier `hasAnalysis: true`, mostra um **toast**
de texto fixo: *"Existe uma análise dentro da régua determinada. Por favor ative a
Camada de Análise ou entre em contato com o Analista responsável."* (`:360-364`).
Essa checagem é sobre **análises anteriores**, não sobre lojas — e não existe
nenhuma checagem de zoneamento no mapa.

**Por que está errado.** O analista descobre que o ponto fere a distância mínima
só depois de fazer a análise de mercado inteira — ou nunca, se não souber que a
regra existe. O momento de carregar o ponto é o único em que avisar ainda evita o
trabalho.

**Impacto de negócio de deixar como está.** A análise de mercado é o item mais
caro do processo. Gastá-la num ponto que a regra barra é desperdício puro, e é o
objetivo que a página declara: *"Não gastar análise de mercado em ponto que a
regra barra"*.

**Alternativa descartada.** Rodar o **zoneamento completo** já no carregamento do
ponto foi descartado: nesta etapa roda **apenas a distância**, com limiar único de
300 m, porque o endereço ainda não está necessariamente preciso e a checagem
precisa ser barata o bastante para rodar a cada mudança de ponto. Teto de grupos e
bandeira ficam para o salvar (Z7).

Rastreabilidade: Confluence 4545904644 v14, seção "Regras de negócio → Validação 1
— ao carregar o ponto", e "Objetivos do usuário". Ressalvas sobre o limiar em
`outputs/regras-negocio-zoneamento-orbita.md`, "RN-18 — Duas validações, em dois
momentos" (observações D-20 e D-21).

**Referências visuais:**
Não informado — solicitar ao design. **A página do Confluence pede modal, não
toast** (ver regra 4).

**Precedente de implementação de modal dentro do próprio módulo do mapa**
(conferido): `AuroraModalService` de `@farmarcas/aurora-angular` + um
`<rds-modal id="...">` no template, aberto por `this._modalService.open('<id>')`.
Exemplo: `modules/view/components/map/map.component.html:27`
(`<rds-modal #modalUpdade id="placeUpdate">`), aberto em `map.component.ts:726`,
serviço injetado em `map.component.ts:91`.
⚠️ **`modules/view/view.component.ts` não injeta hoje nenhum serviço de modal** —
só `ToastrService` (`:143`) e `AnalysisModalService` (`:148`). O
`AuroraModalService` precisa ser injetado e o `<rds-modal>` do zoneamento
acrescentado em `modules/view/view.component.html`. Enquanto não houver Figma,
seguir a estrutura do `placeUpdate` como referência.

**Caminho/rota:**

Duas entradas chegam no mapa, e **as duas disparam este card**:

1. **Órbita → tela inicial ("Qual o próximo ponto a ser analisado?") → digitar o
   endereço na busca e selecionar um resultado.** Não existe link nem item de menu
   para o mapa: quem navega é o `onExplore(place)` da home, que seta
   `MapService.map.main` e só então chama `this._router.navigate(['/view'])`
   (`modules/common/pages/home/home.component.ts:42`).
2. **Órbita → Análises de Pontos → abrir uma análise → "recuperar o mapa"**
   (`modules/analysis/pages/create/components/historic/historic.component.ts:118`),
   que restaura o mapa salvo, seta `map.analysisId` (`:109`) e navega para `/view`.

Como `map.main` já vem preenchido antes da navegação nas duas entradas, o
`checkNearbyAnalysis()` do `ngOnInit` (`modules/view/view.component.ts:168`) já
roda com o ponto na mão — é esse o "ao carregar o ponto" deste card.

*Observações:* a rota `view` está em `app.routes.ts:37` e **não é filha** do
`CommonNavigationComponent`, por isso o mapa abre sem menu lateral e não aparece
nele (itens: Início, Indicadores, Análises de Pontos, Contratos Fechados, Base de
Dados — `modules/common/components/navigation/navigation.component.ts:57-113`).
`/view` exige a permissão **`AccessOrbita`** no produto ORBITA
(`app.routes.ts:20-34`). Como se chega ao Órbita **a partir do Radar** não é
verificável nestes 3 repositórios — ver Pontos em aberto.

**Escopo do card:**

* No mapa, ao carregar o ponto, chamar a checagem de **distância entre lojas**
  (Z2) com limiar único de **300 m** e exibir o resultado como **modal** quando
  houver violação.
* O modal **apenas renderiza** o veredito do **Z5** — não monta texto próprio.
* O modal tem confirmação, e **depois de confirmar o analista segue com a
  análise** — este modal não bloqueia.
* **Ponto de entrada já existente como referência de MOMENTO, não como função a
  reaproveitar:** `checkNearbyAnalysis()`
  (`modules/view/view.component.ts:343`), disparado no `ngOnInit` (`:168`) e a
  cada mudança de `main`/`radius` (`:169-171`). **A checagem de zoneamento deve
  ser um método próprio**, não um `if` a mais dentro do `checkNearbyAnalysis()` —
  ver regra 10.
* **Não entra neste card:** o teto de grupos, a regra de bandeira/modelo, e
  qualquer bloqueio.
* **Não entra neste card:** remover ou alterar o toast de análise próxima.

**Regras de negócio:**

1. Esta validação **vale para o fluxo normal do mapa** — não para o Órbita IA
   (Z8) nem para o momento de salvar (Z7).
2. **Ao carregar o ponto, o Órbita checa APENAS a distância entre lojas.** Nada de
   teto de grupos, nada de bandeira.
3. **Nesta etapa é usado o limiar único de 300 metros, independentemente da
   bandeira.** É diferente do Z2, que aplica 300/500 conforme a bandeira — aqui a
   triagem é um número só, porque a bandeira pretendida ainda pode não estar
   definida.
4. **Se o ponto ferir a distância, aparece um MODAL em tela**, com o motivo.
   Modal, não toast: o toast de análise próxima que já existe
   (`view.component.ts:360`) pode passar despercebido, e a página pede modal.
5. **O analista pode seguir com a análise depois de confirmar.** Este modal
   informa; não barra.
6. O motivo exibido obedece ao conteúdo obrigatório do veredito (Z5, regra 3): a
   regra ferida com o limiar, contra qual loja (bandeira, bairro ou endereço,
   status, distância medida, se é do próprio solicitante) e contra qual dos dois
   endereços. **O modal não monta texto próprio.** A fonte
   (`regras-negocio-zoneamento-orbita.md`, RN-18.1) pede ainda uma 4ª parte,
   *"o que destravaria"* (ex.: *"faltam 120 m"*), que **está em decisão aberta no
   Z5** — prever espaço para ela no layout ou confirmar com o Z5 antes de fechar o
   Figma.
7. **Se a checagem de zoneamento falhar, der timeout ou não concluir, abre o MESMO
   modal, com resultado `indeterminado` e o dado que faltou** — nunca fica em
   silêncio e **nunca** cai só num toast. Silêncio no mapa é lido como "não tem
   nada por perto". Não confundir com o tratamento de erro que já existe para a
   checagem de **análise próxima**, que é um toast
   (`modules/view/view.component.ts:367-373`) e **continua como está** (regra 8).
8. **O que NÃO muda com este card:** o toast de análise próxima continua
   funcionando como hoje, com o mesmo texto e o mesmo gatilho. São dois avisos
   diferentes: um é sobre **análise anterior de outro analista**, o outro sobre
   **loja Farmarcas existente**.
9. **O que NÃO muda com este card:** o slider de **raio de análise** do mapa e o
   que ele significa. O limiar de 300 m da regra 3 é fixo e **não é** o raio
   escolhido pelo analista (ver o verbete "Raio de análise" no glossário).
10. **A checagem de zoneamento NÃO depende de o analista estar com o raio
    ligado.** O `checkNearbyAnalysis()` atual sai antes de chamar a API quando
    `map.radiusEnabled` é `false` (`modules/view/view.component.ts:347-353`), e
    `radiusEnabled` é um botão que o analista liga/desliga ("Raio da Análise",
    `view.component.html:34-35`; inicia `true` em `shared/models/map.model.ts:88`).
    O zoneamento **não herda esse guard**: depende só de haver coordenada do ponto
    (`lat` **e** `lng`). Com o raio desligado, o toast de análise próxima continua
    não aparecendo (isso não muda) e o modal de zoneamento **continua aparecendo**.
    *(Observação para quem for mexer: o guard atual testa `location.lat` duas vezes
    e **nunca testa `lng`** — bug pré-existente, não corrigir de carona sem
    combinar.)*

**Pontos em aberto:**

- **Os 300 m desta etapa são o limiar mais permissivo, não o mais seguro.** O
  rascunho registra: *"A regra vigente exige 300 m só para a mesma bandeira;
  contra bandeira diferente são 500 m. Checando sempre 300 m, todo ponto que
  estiver entre 300 e 500 m de uma loja de outra bandeira passa limpo na etapa 1 e
  só aparece como violação ao salvar — depois de o analista ter feito a análise
  inteira, que é exatamente o custo que a etapa 1 existe para evitar."* A
  recomendação registrada é usar **500 m** como triagem e o modal dizer se é
  violação certa (< 300 m) ou possível (300–500 m). **A página v14 decidiu 300 m**
  e este card implementa os 300 m; a recomendação está aqui porque **não consta que
  tenha sido endereçada**.
- **O teto de grupos saiu desta etapa.** Mesmo rascunho: *"Ele é a checagem mais
  barata e mais decisiva — responde 'a cidade está fechada' só com o município, sem
  precisar de endereço preciso — e agora só roda ao salvar. Resultado: o analista
  faz a análise inteira de uma cidade que já estava fechada antes de ele começar."*
  A página v14 mantém o teto só no salvar. Registrado para decisão.
- **Dois avisos com o mesmo número no mesmo instante (2ª ordem).** O toast de
  análise próxima usa `ANALYSIS_RADIUS_SEARCH = 300`
  (`api-orbita-nodejs/src/services/searchService.js:10`) e este modal usa 300 m
  também. No mesmo carregamento o analista pode receber os dois, com o mesmo
  número, sobre coisas diferentes. **Definir com o design se os textos distinguem
  claramente "análise anterior" de "loja Farmarcas", ou se os dois avisos se juntam
  num só** — juntar não está no escopo pedido. *(O título do SQO-1334 — "Cruzar
  dados de lojas **e análises**" — sugere que a intenção era juntar; confirmar.)*
- **O endpoint a chamar — e o PEDIDO também precisa mudar, não só a resposta.**
  `POST /sources/search/warnings` já existe e já é chamado neste exato momento
  (`shared/services/source.service.ts:91`), mas: (a) o **pedido** leva apenas
  `{ latitude, longitude }` no corpo e `?analysisId` na query (`:95-105`), contra
  `apiBase` — **sem bandeira, sem município e sem solicitante**, que é o que a
  regra 6 manda imprimir; (b) a **resposta** é só `{ hasAnalysis: boolean }`
  (`shared/models/source.model.ts:394-396`); (c) o serviço **ignora qualquer raio
  enviado** — sobrescreve `search.range = ANALYSIS_RADIUS_SEARCH`
  (`api-orbita-nodejs/src/services/searchService.js:560`). Decidir se o zoneamento
  entra ampliando esse contrato (pedido **e** resposta) ou num endpoint novo.
  **Ampliar o existente afeta qualquer outro consumidor de
  `/sources/search/warnings` — não localizei outro nestes 3 repositórios, mas a
  ausência vale só para estes três.**
- **A checagem deve observar `main` apenas, ou `main` e `radius`?** O gatilho atual
  observa `['main','radius']` (`view.component.ts:169-171`). Se o zoneamento entrar
  no mesmo gatilho, **um modal reabriria a cada ajuste do slider**, o que é
  inaceitável para modal (diferente de toast). E como o `range` é fixado no
  servidor e nem é enviado, **re-disparar na mudança de `radius` produz hoje uma
  requisição idêntica à anterior**. Recomendação: observar apenas `main`.
- **Reabrir o mapa de análise já avaliada.** A segunda entrada em `/view`
  (`historic.component.ts:118`) traz uma análise que já existe (`map.analysisId`
  setado em `:109`). O fluxo de análise próxima evita avisar contra si mesma
  passando `analysisId` ao endpoint (`source.service.ts:91-96`); o zoneamento não
  tem equivalente definido. **Decidir se o modal reabre a cada visita ou só na
  primeira avaliação do ponto.**
- **Caminho a partir do Radar não verificável.** A frase-padrão de outros cards do
  board ("Radar → ícone de 4 quadradinhos → Órbita → ...") **não foi usada aqui de
  propósito**: ela já foi para o board sem checagem no SQO-1279 e apontava para uma
  tela inexistente. O que está confirmado é o caminho **dentro** do Órbita.

**Critérios de aceite:**

- Dado que o analista carrega no mapa um ponto a **200 m** de uma loja Farmarcas,
  quando a tela termina de carregar o ponto, então **abre um modal** dizendo que o
  ponto fere o zoneamento, com a regra, o limiar de 300 m, a distância medida, os
  dados da loja e contra qual dos dois endereços foi.
- Dado que o modal está aberto, quando o analista confirma, então o modal fecha e
  ele **consegue seguir com a análise** normalmente.
- Dado que o analista carrega um ponto a **450 m** de uma loja Farmarcas de
  bandeira **diferente**, quando a tela carrega, então **nenhum modal de zoneamento
  abre** (o limiar desta etapa é 300 m) — este é o caso que a recomendação dos
  500 m em Pontos em aberto quer cobrir.
- Dado que o analista **desligou o botão "Raio da Análise"** e carrega um ponto a
  200 m de uma loja Farmarcas, quando a tela carrega, então **o modal de zoneamento
  abre do mesmo jeito** (e o toast de análise próxima continua não aparecendo, como
  hoje).
- Dado que o analista apenas **ajusta o slider de raio** sem mover o ponto, quando
  o raio muda, então o modal de zoneamento **não reabre**.
- Dado que a checagem de zoneamento **falha** (erro HTTP ou timeout), quando a tela
  carrega o ponto, então **abre o modal de zoneamento** com resultado
  **`indeterminado`** dizendo qual dado faltou — e **não** um toast, e **não** uma
  tela silenciosa.
- Dado um ponto que fere a distância **e** tem análise anterior no raio, quando a
  tela carrega, então os dois avisos são distinguíveis: um fala de loja Farmarcas,
  o outro de análise anterior.
- Dado um ponto sem nenhuma violação de distância, quando a tela carrega, então
  **nenhum modal de zoneamento aparece**.
- Não se pode fugir da seção Escopo do card
- Estar em conformidade com as regras de negócio
- Passar nos testes definidos por QA
- Estar em conformidade com o Figma

**Figma:** Não informado — solicitar ao design (a página do Confluence registra
"A ser construído"). ⚠️ O card existente no board herdou o link do **Handoff —
Órbita** do template: **confirmar/substituir**, ele não aponta para esta tela.

**Estimativa:** [DEFAULT: 5 pts — confirmar com o time]
**Prioridade:** [DEFAULT: P1 — confirmar com o time]
**Dependências:** Z2, Z5.
**Revisado por (?_?) revisor-clareza-junior:** pronto para o júnior

---

## Z7 → SQO-1388

### [Análise] Aviso de Zoneamento ao Salvar a Análise

**Contexto:**

**Comportamento atual.** Quando o analista salva uma análise de ponto, o fluxo
passa por `AnalysisViewComponent.onSubmit()`
(`webapp-orbita-angular/src/app/modules/analysis/pages/view/view.component.ts:204`),
que já sabe abrir um modal bloqueante antes de concluir — é o que faz hoje para
contrato (`_modalService.open('contract-create')`, `:222`) — e em seguida chama
`AnalysisService.create()` ou `.update()`
(`shared/services/analysis.service.ts:71` e `:79`), que gravam na API de expansão.
**Nenhuma checagem de zoneamento acontece nesse caminho.**

**Por que está errado.** O carregamento do ponto (Z6) só checa distância, com um
limiar de triagem. O teto de grupos econômicos da cidade e a regra de bandeira
nunca são checados — e são eles que barram a entrada de um grupo novo numa praça
fechada, que é o conflito entre associados que a regra existe para evitar.

**Impacto de negócio de deixar como está.** A análise é salva e segue para
validação, contrato e, no limite, abertura de loja, num ponto que a regra de
expansão barra. Desfazer isso depois custa relacionamento com o empresário e
escala para a diretoria caso a caso.

**Alternativa descartada.** Rodar o **teto de grupos já no carregamento do ponto**
(Z6), e não só aqui, foi considerado e **não** foi adotado: a página v14 mantém o
teto exclusivamente na validação 2. O rascunho registra a objeção literal (D-21):
*"Ele é a checagem mais barata e mais decisiva — responde 'a cidade está fechada'
só com o município, sem precisar de endereço preciso (RN-14) — e agora só roda ao
salvar. Resultado: o analista faz a análise inteira de uma cidade que já estava
fechada antes de ele começar."* Este card implementa a decisão da página; a
objeção está registrada no Z6 e **não consta que tenha sido endereçada**.

Rastreabilidade: Confluence 4545904644 v14, seção "Regras de negócio → Validação 2
— ao salvar a análise". Objeção e definição de `impedimento` em
`outputs/regras-negocio-zoneamento-orbita.md`, "RN-18 — Duas validações, em dois
momentos" e seção 5.

**Referências visuais:**
Não informado — solicitar ao design. Precedente de modal bloqueante no mesmo
fluxo: os modais `contract-create` / `contract-cancel` abertos por `onSubmit()`
(`modules/analysis/pages/view/view.component.ts:222-226`).

**Caminho/rota:**

Órbita → **Análises de Pontos** → formulário de análise → botão **"Salvar
análise"** (`modules/analysis/pages/view/view.component.html:146`, que chama
`onSubmit()`).

Confirmado: item de menu "Análises de Pontos" → `/analysis`
(`modules/common/components/navigation/navigation.component.ts:86-94`); o
formulário é o `AnalysisViewComponent`, servido em `/analysis/create` e
`/analysis/view/:analysisId` (`modules/analysis/analysis.routes.ts:15-22`).
**Toda a rota `/analysis` exige a permissão `ManagamentAnalysis` no produto
ORBITA** (`app.routes.ts:62-72` — atenção, a string no código está grafada
**`ManagamentAnalysis`**, com esse erro de digitação; é por ela que se procura).
Quem não tem a permissão não vê o item de menu nem entra na rota.

**Três caminhos chegam no mesmo `onSubmit()`** e todos disparam este card:
1. a rota `/analysis/create` e `/analysis/view/:analysisId`;
2. o mesmo formulário aberto como **modal a partir do mapa**, via
   `AnalysisModalService.open()` em `saveAnalysis(type)`
   (`modules/view/view.component.ts:299`, método em `:288`);
3. o **rascunho**, também como modal, via `saveDraftAnalysis()`
   (`modules/view/view.component.ts:221-225`) e o atalho do menu lateral
   (`modules/common/components/navigation/navigation.component.ts:50-54`) — **neste
   caminho o formulário abre com um `MapModel` vazio, sem ponto**.

**Escopo do card:**

* No salvar da análise, antes de concluir, rodar o zoneamento **completo**: teto
  de grupos (Z3), regra de bandeira/modelo (Z4) e distância com os **limiares
  reais** 300/500 m (Z2).
* Exibir o veredito do **Z5** como aviso, **apenas quando há algo a apontar**.
* Ponto de entrada: `AnalysisViewComponent.onSubmit()`
  (`modules/analysis/pages/view/view.component.ts:204`), seguindo o padrão de
  modal-antes-de-concluir já usado para contrato (`:217-233`).
  **Como esse padrão funciona hoje (ler antes de mexer):** `onSubmit(confirm = false)`
  abre o modal e dá `return` sem salvar (`:219-228`); o botão dentro do modal chama
  **`onSubmit(true)`** (`pages/view/view.component.html:116` e `:136`), e a segunda
  passagem pula o bloco de contrato (`:229-232`) e segue para
  `createAnalysis()`/`updateAnalysis()` (`:235-239`).
  ⚠️ **NÃO reaproveitar o parâmetro `confirm` para o zoneamento.** Ele é o flag do
  contrato: confirmar o zoneamento com o mesmo booleano faria o fluxo **pular o
  modal de contrato**, quebrando exatamente o que a regra 8 diz que não pode mudar.
  O zoneamento precisa do seu próprio estado de confirmação, e a ordem entre os
  dois modais tem de ser definida.
* **Não entra neste card:** persistir o veredito junto da análise → Z10.
* **Não entra neste card:** bloquear o salvamento (ver regra 4 e Pontos em aberto).
* **Não entra neste card:** a tela do Órbita IA (Z8).

**Regras de negócio:**

1. **Ao salvar, o Órbita roda a validação de grupo econômico naquela cidade** — o
   teto do município (Z3).
2. **Roda também a distância entre lojas com os limiares REAIS**: 300 m para a
   mesma bandeira e 500 m para bandeira diferente (Z2). Diferente do Z6, que usa
   300 m único como triagem.
3. **Roda também a regra de bandeira e modelo de negócio (Z4)**: na faixa de
   60.001 a 120.000 habitantes, o grupo que entra como 2º da cidade precisa abrir
   com bandeira de modelo `Popular`. Se o **modelo de negócio não estiver
   disponível no pedido**, esta regra sai como **"não avaliada"** no aviso — nunca
   como "passou" (o campo de modelo **não existe** no formulário hoje; ver Pontos
   em aberto).
4. **O aviso só aparece quando há algo a apontar** — quando o ponto fere o
   zoneamento (impedimento) ou quando há alerta. Em qualquer outro caso, nada
   aparece (regra 6).
5. **O texto do aviso usa o tempo verbal da fonte: o ponto "estaria bloqueado"
   pelo zoneamento, e por quê.** **Nesta entrega o aviso não impede o
   salvamento**: depois de confirmar, a análise é salva. Se a decisão em aberto
   ("bloqueia ou só avisa?") virar bloqueio de fato, isso é **mudança de escopo
   deste card** e não deve ser implementado por conta própria.
6. **Quando não há violação nem aviso, a análise é salva sem aviso em tela.**
   Nenhum modal, nenhum toast de "zoneamento ok".
7. **Se a consulta não concluir, o aviso diz `indeterminado`** e a análise não é
   salva como se o zoneamento tivesse passado.
8. **O que NÃO muda com este card:** o fluxo de contrato dentro do `onSubmit()`.
   `getContractAction()` (`modules/analysis/pages/view/view.component.ts:295`) e os
   modais `contract-create` / `contract-cancel` continuam exatamente como estão,
   **inclusive o parâmetro `confirm` do `onSubmit`, que continua sendo só do
   contrato**. O aviso de zoneamento é **mais um** modal no mesmo ponto, não um
   substituto, e **não pode reaproveitar o `confirm`**.
9. **O que NÃO muda com este card:** a validação de formulário existente,
   `analysisIsInvalid()` (`modules/analysis/pages/view/view.component.ts:347-353`).
   O zoneamento não entra como validação de campo.
10. **O que NÃO muda com este card:** o veredito **é produzido mesmo quando não há
    aviso** (Z5, regra 8). "Não mostrar em tela" (regra 6) **não é** "não calcular".

**Pontos em aberto:**

- **O aviso bloqueia ou só avisa?** A página do Confluence diz que o aviso informa
  que o ponto *"estaria bloqueado"* — o tempo verbal sugere que ele **não bloqueia
  de fato** nesta entrega. O rascunho, em compensação, define `impedimento` como
  *"Bloqueia. A análise não avança"*. **São leituras diferentes e a diferença é o
  card inteiro.** Confirmar antes de desenvolver.
- **Onde essa checagem roda — front ou API de expansão?** O salvar grava em
  `POST ${apiExpansion}/analysis` (`shared/services/analysis.service.ts:71`) e
  `PUT ${apiExpansion}/analysis/${analysis.id}` (`:79`), com
  `apiExpansion = environment.api.expansion` (`core/http/http.base.service.ts:9`).
  **Essa API não está em nenhum dos 3 repositórios** — o `api-orbita-nodejs` monta
  só `/health`, `/imports`, `/sources`, `/markers`, `/grouping`, `/graphic`
  (`api-orbita-nodejs/app.js:52-57`). Checar no front é frágil (dá para salvar
  chamando a API direto); checar na API de expansão exige um repositório que este
  card não alcança. **Decidir com o time, e provavelmente abrir um card irmão na
  API de expansão.**
- **O formulário tem o dado que a regra precisa?** A regra 2 exige a **bandeira
  pretendida** (existe: `Analysis.brand?: number`,
  `shared/models/analysis.model.ts:116`) e a regra 3 exige o **modelo de negócio**,
  que **não existe no modelo de análise** — confirmado nesta sessão. Sem ele, a
  regra de bandeira popular sai sempre como "não avaliada" (decisão **D-13**).
- **Análise de Território e análise sem ponto.** O zoneamento "ao salvar"
  pressupõe um ponto, mas o produto salva dois tipos (`AnalysisType.CITY` =
  "Território" e `POINT` = "Ponto", `shared/models/analysis.model.ts:6-14`, ambos
  oferecidos no mesmo fluxo de salvar do mapa —
  `modules/view/view.component.html:79` e `:84`) **e permite salvar análise de Ponto
  sem ponto** (`analysisIsInvalid()` só exige `lead` **ou** `map.main.id`,
  `pages/view/view.component.ts:347-353`; e os caminhos de rascunho abrem o
  formulário com `MapModel` vazio). A página v14 **não trata nenhum dos dois
  casos**. Definir antes de desenvolver: a distância exige coordenada, o teto exige
  só o município.
- **Alvo de tempo de resposta.** O rascunho registra (RN-18.3) que o gate *"está no
  caminho crítico de uma interação frequente"* e que *"é preciso um alvo de tempo
  de resposta declarado"* (D-17). Não há número, e sem ele o critério de timeout
  não é testável.
- **Dois modais no mesmo clique.** Confirmar a ordem entre o modal de zoneamento e
  o de contrato, e que o aviso se comporta igual nos **três** caminhos de entrada
  (modal dentro de modal é risco de UI real no caminho 2).
- **Impacto de 2ª ordem — a lista e os indicadores de análise.** Se o veredito
  passar a existir por análise, as telas de `/analysis` e `/analysis/dashboard`
  (que consomem `getSummary` e `getSummaryBreakdown`,
  `shared/services/analysis.service.ts:173` e `:193`) podem precisar de coluna,
  filtro ou recorte por veredito. **Não está no escopo pedido.**
- **Impacto de 2ª ordem — o analista deixa de ser o amortecedor.** O rascunho
  registra (RN-17) que hoje o analista é quem traduz a regra para o associado, e que
  um impedimento automático sem texto padrão produz *"seu pedido foi negado por um
  motivo que não posso explicar"*. **Não há texto padrão definido** do que se diz ao
  associado, nem canal de recurso. Fora do escopo; precisa de dono em Expansão.

**Critérios de aceite:**

- Dado um ponto em município de 55.000 habitantes que já tem 1 grupo econômico, e
  um solicitante sem nada naquele município, quando o analista salva a análise,
  então aparece o aviso dizendo que o ponto estaria bloqueado, citando o teto
  "1 de 1 grupo" e a população usada.
- Dado um ponto a **400 m** de uma loja Farmarcas de **bandeira diferente**, quando
  o analista salva, então aparece o aviso de violação de distância com limiar
  **500 m** — mesmo que o modal do Z6 (triagem de 300 m) não tenha aberto no
  carregamento.
- Dado um ponto em município de **80.000 habitantes** onde o solicitante entra como
  **2º grupo**, quando o analista salva, então o aviso traz a regra de
  bandeira/modelo do Z4 — **ou**, se o modelo não estiver disponível, traz essa
  regra explicitamente como **"não avaliada"**, nunca omitida.
- Dado um ponto **sem nenhuma violação e sem nenhum aviso**, quando o analista
  salva, então a análise é salva e **nenhum aviso de zoneamento aparece em tela**.
- Dado um ponto sem violação, quando a análise é salva, então o veredito `liberado`
  ainda assim foi calculado (verificável pelo registro do Z10) — "sem aviso em
  tela" não é "sem veredito".
- Dado uma análise de **Ponto salva sem ponto no mapa** (hoje possível), quando o
  analista salva, então o zoneamento **não é dado como `liberado`**: as regras que
  dependem de coordenada saem como **"não avaliada"** e o salvamento segue.
- Dado uma análise de **Território** (`AnalysisType.CITY`), quando o analista
  salva, então **[DECIDIR com produto:** o zoneamento não roda / roda só o teto do
  município**]**. Sem essa decisão o card não cobre metade dos tipos de análise.
- Dado que a consulta de zoneamento **deu timeout**, quando o analista salva, então
  aparece um aviso de `indeterminado` — e **não** um salvamento silencioso.
- Dado que a consulta de zoneamento está em andamento, quando o analista clica em
  "Salvar análise" de novo, então **o segundo clique não cria uma segunda análise**
  (o botão fica em estado de carregando, como já acontece no salvamento —
  `[disabled]="loading || analysisIsInvalid()"`, `view.component.html:146`, com
  `loading = true` em `view.component.ts:243` (`createAnalysis`) e `:267`
  (`updateAnalysis`)).
- Dado um ponto que dispara aviso de zoneamento **e** ação de contrato, quando o
  analista salva, então os dois modais aparecem sem se sobrepor e o fluxo de
  contrato continua funcionando como hoje.
- Não se pode fugir da seção Escopo do card
- Estar em conformidade com as regras de negócio
- Passar nos testes definidos por QA
- Estar em conformidade com o Figma

**Figma:** Não informado — solicitar ao design.

**Estimativa:** [DEFAULT: 5 pts — confirmar com o time]
**Prioridade:** [DEFAULT: P1 — confirmar com o time]
**Dependências:** Z5. **Atenção:** pode precisar de um card irmão na API de
expansão, fora destes 3 repositórios.
**Revisado por (?_?) revisor-clareza-junior:** pronto para o júnior

---

## Z8 → SQO-1335

### [Órbita IA] Modal de Zoneamento na Tela Final da Análise por IA

**Contexto:**

**Comportamento atual.** No Órbita IA, a análise é montada de uma vez: não há a
etapa de "carregar o ponto" no mapa nem a de "salvar a análise" que existem no
fluxo do analista. **Esta descrição vem da página do Confluence, não de leitura de
código** — a tela do Órbita IA não está nos 3 repositórios clonados, então
"nenhuma validação de zoneamento acontece nesse fluxo" é o que a fonte afirma, e
não algo verificado aqui.

O que **foi** verificado: o motor que produz a análise por IA é o
`api-agent-orbita` (`POST /analysis` → `analyzeViability()` em
`src/services/analysisAgent/index.ts:26`), ele devolve score, classificação e
narrativa (`index.ts:40-49`) e **não tem nenhuma noção de zoneamento, loja
Farmarcas ou grupo econômico** — isso, sim, está confirmado por leitura do código.

**Por que está errado.** As duas validações desenhadas para o fluxo do mapa (Z6 e
Z7) estão amarradas a dois momentos que **não existem** no fluxo da IA. Sem uma
regra própria, a análise por IA entregaria um resultado completo sem nunca ter
checado o zoneamento — e seria o único caminho do produto que ignora o gate.

**Impacto de negócio de deixar como está.** O Órbita IA é o caminho que existe
justamente para reduzir passos do analista. Se é o único que não checa zoneamento,
vira o caminho mais rápido para produzir uma análise que fere a regra.

**Alternativa descartada.** Reaproveitar a triagem de 300 m do fluxo do mapa (Z6)
foi descartado: ela existe porque, no mapa, há uma etapa barata de carregar o
ponto antes da análise cara. No fluxo da IA não existe essa etapa, então **não há
o que triar** — valem direto os limiares reais.

Rastreabilidade: Confluence 4545904644 v14, seção "Regras de negócio → Análise
feita pelo Órbita IA".

**Referências visuais:**
Não informado — solicitar ao design.

**Caminho/rota:**

**Não localizado nestes 3 repositórios — confirmar com o time.** Busca nesta
sessão por rota ou tela do Órbita IA (`path: 'ai'`, `orbita/ai`, `orbita.?ia`)
não retornou nada, e o webapp **não chama** o motor da IA (nenhuma referência ao
`api-agent-orbita` em `src/environments`). O menu lateral do webapp não tem item
de Órbita IA (`modules/common/components/navigation/navigation.component.ts:57-113`).

Registro de sessão anterior desta skill indica que a tela vive em um **4º
repositório do Órbita, ainda não clonado**. **A rota em si é desconhecida** —
qualquer caminho que apareça escrito em rascunhos anteriores é suposição, não
verificação. Preencher este campo só depois que alguém com acesso ao repositório
disser a rota. **Não copiar a frase-padrão "Radar → ícone de 4 quadradinhos →
Órbita → Órbita IA"** — ela já foi para o board no SQO-1279 apontando para tela
inexistente, e é o campo herdado do template neste card.

**Escopo do card:**

* Na montagem da **tela final do Órbita IA**, rodar as duas validações **ao mesmo
  tempo**: distância entre lojas com os limiares reais (Z2) e teto de grupos
  econômicos do município (Z3).
* Exibir o veredito do **Z5** como **modal**, apenas quando houver algo a apontar.
* **Não entra neste card:** a triagem de 300 m do fluxo do mapa.
* **Não entra neste card:** persistir o veredito → Z10.
* **Não entra neste card:** qualquer alteração no mapa (Z6) ou no formulário de
  análise (Z7).
* ⚠️ **Atenção de escopo (checado em 2026-11-23):** o código **da tela** não está
  nos 3 repositórios mapeados — a ausência vale para estes três, não para o produto
  inteiro. Já o **motor** da análise por IA está: `api-agent-orbita`
  (`POST /analysis`). Então este card provavelmente **se parte em dois**: um pedaço
  de cálculo no `api-agent-orbita` e um pedaço de modal no 4º repositório. **Não
  estimar como card único antes de o time confirmar essa divisão.**

**Regras de negócio:**

1. **Na análise feita pela IA, as duas validações rodam ao mesmo tempo**, no
   momento em que a tela final é montada. Não há dois momentos separados.
2. **Valem os limiares reais de distância: 300 m entre lojas da mesma bandeira e
   500 m entre bandeiras diferentes** (os mesmos do Z2). Os dois números são
   limiares de proximidade entre lojas e **não** têm relação com o raio de análise
   do mapa.
3. **A triagem de 300 m do fluxo do mapa NÃO se aplica aqui**, porque não existe
   etapa de carregar o ponto. Não reaproveitar o limiar único do Z6.
4. **O modal só aparece quando há algo a apontar** — se o ponto ferir o zoneamento
   ou se houver avisos.
5. **Quando não há violação nem aviso, nenhum modal é exibido e a tela final é
   entregue normalmente.**
6. **O modal traz a mesma explicação exigida nas demais validações** — o conteúdo
   obrigatório do veredito (Z5, regra 3).
7. **O veredito é calculado e entregue para registro mesmo quando não há modal**,
   como no fluxo do mapa. Quem persiste é o Z10.
   ⚠️ **Risco conhecido:** o motor da IA (`api-agent-orbita`) é **stateless** — ele
   devolve o resultado e não grava nada (`src/services/analysisAgent/index.ts:26-49`;
   o único acesso a Mongo do repositório é leitura de camadas). **Não foi
   encontrado, nestes 3 repositórios, nenhum ponto em que a análise da IA seja
   persistida como análise.** Então, hoje, **pode não existir "a análise" da IA para
   o veredito ficar junto.** Antes de desenvolver, confirmar se o fluxo da IA grava
   em `${apiExpansion}/analysis` ou em outro lugar — se não gravar em lugar nenhum,
   esta regra e o Z10 não se aplicam ao fluxo da IA e o card muda de tamanho.
8. **Se a consulta não concluir, o modal diz `indeterminado`** — a tela final não é
   entregue como se o zoneamento tivesse passado.
9. **O que NÃO muda com este card:** o restante da tela final da IA — camadas,
   números, narrativa, score de viabilidade. Este card acrescenta uma validação e um
   modal; não altera o conteúdo da análise.
10. **O que NÃO muda com este card:** o fluxo do mapa. Z6 continua com triagem de
    300 m e Z7 continua rodando no salvar, independentemente deste card.

**Pontos em aberto:**

- **Em qual repositório este card é implementado — e é um só?** A checagem desta
  sessão separa o card em duas metades, e só uma está fora de alcance:
  (i) **calcular** o veredito tem um repositório candidato **que está clonado**:
  `api-agent-orbita`, já o motor da análise por IA (`POST /analysis`,
  `src/routes/analysis.routes.ts:7`; `analyzeViability()`,
  `src/services/analysisAgent/index.ts:26`), que já lê camadas por raio
  (`src/services/radiusSearch/`);
  (ii) **exibir** o modal fica na tela do Órbita IA, **não localizada nestes 3
  repositórios**.
  Confirmar se o veredito entra no retorno do `POST /analysis` do
  `api-agent-orbita` ou se é chamada separada da tela. **Enquanto isso não for
  decidido, a estimativa abaixo não tem base.**
- **Qual é a rota real da tela final da IA?** Ver Caminho/rota.
- **O fluxo da IA coleta perfil do solicitante, bandeira e modelo de negócio?** O
  Z9 torna o perfil obrigatório **no formulário de análise**; não está confirmado
  que o fluxo da IA colete qualquer um dos três. Sem perfil, a regra do Z5 que
  distingue "loja do próprio solicitante" de "loja de outro associado" não tem como
  ser aplicada aqui. Sem bandeira, a regra 2 cai no critério mais restritivo
  (500 m, Z2 regra 3).
- **A análise da IA é persistida?** Ver regra 7. Se não for, a dependência Z10 ← Z8
  é vazia.
- **O modal aparece antes ou depois de a tela final renderizar?** A página diz
  "quando a tela final é montada". Se o modal cobrir a tela recém-entregue, o
  analista lê o impedimento com a análise completa atrás — o que contraria o
  objetivo de "não gastar análise de mercado em ponto que a regra barra", já que
  aqui a análise já foi gasta. **Registrado: no fluxo da IA esse objetivo não é
  alcançável pelo desenho atual.**

**Critérios de aceite:**

> **Executabilidade:** os critérios abaixo descrevem a tela do Órbita IA, que não
> está nos 3 repositórios clonados. Eles só se tornam testáveis depois que o
> repositório da tela for identificado. Até lá, servem de contrato de
> comportamento, não de roteiro de teste.

- Dado um ponto a **400 m** de uma loja Farmarcas de **bandeira diferente**,
  quando a tela final da IA é montada, então **abre um modal** de violação de
  distância com limiar **500 m** (e não com 300 m).
- Dado um ponto em município cujo teto de grupos já está preenchido, quando a tela
  final é montada, então o modal traz também a violação de teto, com a contagem de
  grupos e o teto da faixa.
- Dado um ponto **sem violação e sem aviso**, quando a tela final é montada, então
  **nenhum modal aparece** e a tela é entregue normalmente.
- Dado um ponto sem violação, quando a tela final é montada, então o veredito
  `liberado` foi calculado e entregue para registro — mesmo sem modal.
- Dado que a consulta de zoneamento falhou, quando a tela final é montada, então o
  modal diz `indeterminado` — e **não** há entrega silenciosa.
- Dado que a consulta volta **403/sem permissão** (e não timeout), quando a tela
  final é montada, então o modal diz `indeterminado` com o motivo "não foi possível
  consultar" — e **não** cai no caminho de `liberado`.
- Dado um pedido **sem bandeira pretendida**, quando a distância é avaliada, então
  vale o critério mais restritivo de **500 m**.
- Dado que o fluxo da IA **não informou o perfil do solicitante**, quando o ponto
  viola a distância, então o modal apresenta a violação **sem afirmar que a loja é
  de outro associado** e declara "perfil do solicitante não informado" como lacuna
  — e **não** assume terceiro por padrão.
- Não se pode fugir da seção Escopo do card
- Estar em conformidade com as regras de negócio
- Passar nos testes definidos por QA
- Estar em conformidade com o Figma

**Figma:** Não informado — solicitar ao design. ⚠️ O card existente no board
herdou o link do **Handoff — Órbita** do template: **confirmar/substituir**.

**Estimativa:** [DEFAULT: 5 pts — confirmar com o time] — **estimativa sem base de
código**, o repositório da tela não foi localizado e o card pode se partir em dois.
**Prioridade:** [DEFAULT: P2 — confirmar com o time]
**Dependências:** Z2, Z3, Z5. **Bloqueado por:** identificação do repositório da
tela do Órbita IA.
**Revisado por (?_?) revisor-clareza-junior:** pronto para o júnior

---

## Z9 → SQO-1389

### [Análise] Perfil do Solicitante como Pergunta Obrigatória no Início da Análise

**Contexto:**

**Comportamento atual.** O formulário de análise já tem um campo "Associado
Farmarcas" com opções Sim/Não
(`webapp-orbita-angular/src/app/modules/analysis/pages/view/view.component.html:46-47`,
ligado a `Analysis.isAssociated`, `shared/models/analysis.model.ts:121`). Mas ele
é **opcional** — a validação do formulário, `analysisIsInvalid()`
(`modules/analysis/pages/view/view.component.ts:347-353`), só exige `lead` ou
`map.main.id` — e fica **no formulário de análise**, que no fluxo do mapa só abre
**ao salvar** (`modules/view/view.component.ts:299`), ou seja, no fim.

**Por que está errado.** O perfil do solicitante muda **a leitura de uma violação
de distância**, não um detalhe de cadastro. Loja vizinha do próprio solicitante é
efeito econômico que ele mesmo pode estar escolhendo; loja vizinha de outro
associado é conflito de interesse entre associados — que é o que a regra existe
para evitar. Sem o perfil preenchido **no início**, o modal do Z6 não tem como
dizer qual dos dois casos é, e o analista recebe um aviso que não diz a coisa mais
importante sobre ele.

**Impacto de negócio de deixar como está.** A violação mais grave (contra outro
associado) e a mais aceitável (contra loja do próprio solicitante) chegam ao
analista com o mesmo texto. Ele trata as duas igual: ou barra o que era escolha
legítima do empresário, ou deixa passar o conflito entre associados.

**Alternativa descartada.** Criar um campo novo de "perfil do solicitante" foi
descartado em favor de reaproveitar o `isAssociated` que já existe
(`shared/models/analysis.model.ts:121`). Motivo: a tela de lista já imprime esse
campo exatamente com os dois rótulos que a página do Confluence pede —
`{{analysis.isAssociated ? 'ASSOCIADO' : 'NOVO EMPRESÁRIO'}}`
(`modules/analysis/pages/list/list.component.html:120`) —, o que é a melhor
evidência disponível de que a semântica é a mesma. **Custo aceito:** o campo é
`boolean` opcional e há análises antigas gravadas com ele, então o estado "não
informado" precisa ser tratado explicitamente (regras 2 e 8); com campo novo
esse problema não existiria.

Rastreabilidade: Confluence 4545904644 v14, seção "Regras de negócio → Perfil do
solicitante". Regra equivalente registrada no `CLAUDE.md` do projeto:
*"Perfil do solicitante é pergunta obrigatória: empresário novo ou já associado."*

**Referências visuais:**
Não informado — solicitar ao design. Existe o campo atual como referência
(`modules/analysis/pages/view/view.component.html:46-47`).

**Caminho/rota:**

Órbita → **Análises de Pontos** → formulário de análise (`/analysis/create`,
`modules/analysis/analysis.routes.ts:15-18`), bloco "Dados Básicos da Análise",
campo "Associado Farmarcas" (`pages/view/view.component.html:46-47`).

⚠️ **Armadilha de pasta:** a rota `create` é servida pelo `AnalysisViewComponent`
— o arquivo a editar é `modules/analysis/pages/view/view.component.ts|html`. A
pasta `modules/analysis/pages/create/` **não tem página nenhuma**: só os
subcomponentes comment/contract/historic.

**São três entradas para o mesmo formulário**, e o `onSubmit()` é o mesmo nas três:
(1) a rota `/analysis/create`; (2) o modal aberto do mapa, `saveAnalysis()` →
`AnalysisModalService.open()` (`modules/view/view.component.ts:288` e `:299`);
(3) o atalho "nova análise" do menu lateral, que cria **rascunho**
(`modules/common/components/navigation/navigation.component.ts:50-54`). A
obrigatoriedade precisa se comportar igual nas três.

**Onde a pergunta passa a aparecer "no início" ainda não está definido** — ver
Pontos em aberto e a partição sugerida no Escopo.

**Escopo do card:**

* Tornar o perfil do solicitante **pergunta obrigatória**, com as duas opções:
  **empresário novo** ou **empresário que já opera loja Farmarcas**.
* Reaproveitar o campo existente `Analysis.isAssociated`
  (`shared/models/analysis.model.ts:121`) e o select "Associado Farmarcas"
  (`pages/view/view.component.html:46-47`) em vez de criar campo novo — confirmar
  com o time que a semântica é a mesma.
* Tornar o campo obrigatório na validação do formulário (`analysisIsInvalid()`,
  `pages/view/view.component.ts:347-353`), **com o cuidado da regra 3** (a
  condição nova é `||`, não `&&`).
* Entregar o perfil para o veredito (Z5), que é quem distingue "loja do próprio
  solicitante" de "loja de outro associado".
* **Partição sugerida (porque "no início" não está decidido):**
  **Z9a — obrigatoriedade** (implementável hoje): tornar o campo obrigatório no
  formulário que já existe, com as armadilhas das regras 2, 3 e 4 resolvidas
  (terceiro estado, o `||` da validação, Território).
  **Z9b — antecipação** (bloqueado): mover ou duplicar a pergunta para antes do
  carregamento do ponto no mapa, para o modal do Z6 poder aplicar as regras 3 e 4.
  Só depois de o Produto dizer em qual tela a pergunta aparece.
  Sem essa partição, o card inteiro fica parado por uma decisão que afeta só
  metade dele.
* **Não entra neste card:** decidir se violação contra loja do próprio solicitante
  é impedimento ou alerta → decisão **D-09** (ver Z2 e Z5).
* **Não entra neste card:** identificar **qual** grupo econômico é o do
  solicitante. Este card captura o perfil (novo / já associado); o vínculo com o
  grupo é a lacuna registrada no Z3.

**Regras de negócio:**

1. **O perfil é pergunta obrigatória**, com duas opções: empresário novo, ou
   empresário que já opera loja Farmarcas. Hoje o campo existe e é opcional; este
   card muda **obrigatoriedade e momento**.
2. **"Não informado" é um terceiro estado e precisa ser tratado como tal.** O
   campo é `isAssociated?: boolean` (`analysis.model.ts:121`): **`false` ("Não" /
   empresário novo) é resposta válida, não ausência de resposta.** Toda checagem de
   preenchimento usa `== null` / `undefined`, **nunca** `!analysisModel.isAssociated`
   — tratar `false` como vazio impediria o analista de salvar qualquer análise de
   empresário novo, que é a maioria dos casos.
3. **A obrigatoriedade entra na validação que já existe, sem quebrar a regra
   atual.** `analysisIsInvalid()` (`pages/view/view.component.ts:347-353`) hoje é
   `isAPointAnalysis() && !lead && !map.main.id` — inválido **só** quando faltam
   *os dois* identificadores. A condição nova é um **`||`**, não um `&&`:
   ```ts
   analysisIsInvalid(): boolean {
     return (
       this.isAPointAnalysis() &&
       (this.analysisModel.isAssociated == null ||
        (!this.analysisModel.lead && !this.analysisModel.map.main.id))
     );
   }
   ```
   Pendurar `&& !isAssociated` no final faria a validação **nunca disparar**.
4. **A obrigatoriedade vale para análise de ponto; para análise de Território
   (`CITY`) é decisão em aberto.** A validação atual é inteira gated por
   `isAPointAnalysis()` (`pages/view/view.component.ts:341-345`) e o mapa oferece
   os dois tipos no mesmo botão de salvar (`modules/view/view.component.html:79` →
   `POINT`, `:84` → `CITY`). Enquanto não houver decisão, **manter o comportamento
   de hoje** para `CITY`: perfil não obrigatório, declarado como não informado no
   veredito.
5. **Quando o perfil é "já opera loja Farmarcas", o aviso rotula a sobreposição
   como "com loja do próprio solicitante"** e a apresenta como efeito econômico a
   dimensionar — pode ser escolha deliberada do empresário. *(Se é impedimento ou
   alerta não é decisão deste card — ver Z2/Z5.)*
6. **Quando o perfil é "empresário novo", o aviso rotula a sobreposição como "com
   loja de outro associado"**, que é o conflito que a regra existe para evitar.
7. **Sobreposição com loja do próprio solicitante e com loja de outro associado
   são itens distintos e NUNCA aparecem juntos** no mesmo item do aviso. Misturá-los
   esconde o grave atrás do aceitável.
8. **Quando o perfil está "não informado" (análise antiga, ou fluxo que não
   coleta), o aviso NÃO escolhe nenhum dos dois rótulos**: a parte da regra que
   depende do perfil sai como `indeterminado`, com a lacuna declarada. **Nunca
   assumir "de terceiro" por padrão** — seria barrar como conflito o que pode ser
   escolha do próprio empresário.
9. **O que NÃO muda com este card:** o campo continua sendo o mesmo, com as mesmas
   duas opções (`isAssociateItems`, `pages/view/view.component.ts:76-85`). Este
   card muda **obrigatoriedade e momento**, não o domínio do campo — a menos que o
   time confirme que a semântica precisa mudar.
10. **O que NÃO muda com este card:** os demais campos obrigatórios do formulário
    e o comportamento de rascunho (`draft`, `analysis.model.ts:142`). Não tornar
    outros campos obrigatórios de carona. O campo também continua desabilitado fora
    do modo de edição (`[disabled]="!editable"`, `pages/view/view.component.html:47`):
    abrir uma análise antiga em modo leitura **não** pode passar a exigir
    preenchimento.
11. **O que MUDA e o card precisa decidir: a lista de análises mente sobre o não
    informado.** `modules/analysis/pages/list/list.component.html:120` imprime
    `{{analysis.isAssociated ? 'ASSOCIADO' : 'NOVO EMPRESÁRIO'}}` — um ternário
    sobre um boolean opcional. Hoje, **toda análise com o campo vazio aparece como
    "NOVO EMPRESÁRIO"**. Se este card cria o estado "não informado", ou a lista
    passa a distinguir os três estados, ou ela continua afirmando algo falso sobre o
    histórico. **Escolher explicitamente** — não deixar como efeito colateral.

**Pontos em aberto:**

- **"Início da análise" é onde, exatamente?** A página diz "no início da análise"
  **sem apontar a tela**. No fluxo do mapa, o formulário só abre **ao salvar** —
  então "no início" exige ou uma pergunta nova antes de carregar o ponto no mapa,
  ou aceitar que o perfil só exista a partir do salvar. **Se o perfil só chegar no
  salvar, o modal do Z6 não terá como aplicar as regras 5 a 8**, e o aviso de
  distância no carregamento não conseguirá distinguir loja do próprio solicitante
  de loja de terceiro. **Esta é a decisão central do card e ela não está tomada.**
- **`isAssociated` significa a mesma coisa?** Evidência a favor encontrada nesta
  sessão: a tela de lista já traduz o campo exatamente nos dois termos da página —
  `'ASSOCIADO'` / `'NOVO EMPRESÁRIO'` (`list.component.html:120`). O que
  **continua não confirmado** é se os analistas preenchem com esse sentido na
  prática e o que há gravado no histórico. **Confirmar com uma contagem na base
  (quantas análises com `true`, `false` e nulo) antes de reaproveitar** —
  reaproveitar campo com semântica divergente contamina o histórico.
- **O que acontece com as análises já existentes sem o campo preenchido?** Tornar
  obrigatório não preenche retroativamente. A regra 8 define o comportamento no
  veredito; falta decidir o que a lista mostra (regra 11).
- **Rascunho exige perfil ou não?** O atalho do menu lateral cria rascunho
  (`navigation.component.ts:50-54`, `initAnalysis(..., draft = true)`). Se exigir, o
  atalho deixa de funcionar como captura rápida. **Decisão pendente.**
- **`rds-select` suporta `[required]`?** Nenhum `rds-select` do webapp usa
  `[required]` hoje (verificado: zero ocorrências em todos os `.html` de
  `src/app`); o único precedente de campo obrigatório é o `rds-input` do Lead
  (`[required]="isAPointAnalysis()"`, `pages/view/view.component.html:19`).
  **Confirmar com o design system** — se não suportar, a marcação visual vira
  trabalho extra e o card cresce.
- **O fluxo do Órbita IA coleta o perfil?** Ver Z8. Se não coletar, as regras 5 a 7
  não se aplicam lá.
- **Impacto de 2ª ordem — filtros e relatórios.** `isAssociated` passa de opcional
  a obrigatório, então a distribuição desse campo muda nas análises novas e qualquer
  corte por "associado sim/não" em `/analysis` ou `/analysis/dashboard` passa a
  comparar períodos com regras de preenchimento diferentes. Não está no escopo
  pedido.

**Critérios de aceite:**

- Dado o formulário de análise de ponto com o perfil **vazio**, quando o analista
  olha o botão "Salvar análise", então ele está **desabilitado** (mesmo mecanismo
  de hoje: `[disabled]="loading || analysisIsInvalid()"`,
  `pages/view/view.component.html:146`) **e** o campo recebe marcação visual de
  obrigatório.
- Dado o formulário com o perfil preenchido como **"Não" (empresário novo)**,
  quando o analista salva, então o salvamento **acontece** — "Não" é resposta, não
  ausência de resposta.
- Dado que o analista informou **empresário que já opera loja Farmarcas** e o ponto
  viola a distância contra uma loja **do próprio solicitante**, quando o aviso é
  montado, então ele diz que a sobreposição é **com loja do próprio solicitante**.
- Dado que o analista informou **empresário novo** e o ponto viola a distância
  contra uma loja Farmarcas, quando o aviso é montado, então ele diz que a
  sobreposição é **com loja de outro associado**.
- Dado um ponto que viola a distância contra uma loja do próprio solicitante **e**
  contra uma loja de outro associado, quando o aviso é montado, então os dois casos
  aparecem como **itens distintos**, nunca num único item.
- Dado uma análise **anterior a este card**, sem o perfil preenchido, quando ela é
  aberta, então ela **não quebra**, o perfil aparece como não informado, e a parte
  do veredito que depende do perfil sai como `indeterminado` — **não** como "de
  outro associado".
- Dado uma análise de **Território** (`AnalysisType.CITY`) aberta a partir do mapa,
  quando o analista salva **sem perfil**, então o comportamento é o de hoje (salva)
  — este card não endurece a análise de território.
- Dado um **rascunho** criado pelo atalho do menu lateral, quando o analista salva
  o rascunho **sem perfil**, então **[DECISÃO PENDENTE** — rascunho exige perfil ou
  não?**]**
- Não se pode fugir da seção Escopo do card
- Estar em conformidade com as regras de negócio
- Passar nos testes definidos por QA
- Estar em conformidade com o Figma

**Figma:** Não informado — solicitar ao design.

**Estimativa:** [DEFAULT: 3 pts — confirmar com o time] (Z9a isolado; Z9b depende
da decisão de "onde é o início")
**Prioridade:** [DEFAULT: P1 — confirmar com o time]
**Dependências:** Nenhuma para o campo em si. O **efeito** do perfil no veredito
depende do Z5.
**Revisado por (?_?) revisor-clareza-junior:** pronto para o júnior

---

## Z10 → SQO-1390

### [Análise] Registro do Veredito de Zoneamento Junto da Análise

**Contexto:**

**Comportamento atual.** Nada do que o Órbita checa hoje no carregamento do ponto
fica registrado. O resultado de `POST /sources/search/warnings` vira um toast
(`webapp-orbita-angular/src/app/modules/view/view.component.ts:360`) que some
quando o analista fecha a tela — e o `{ hasAnalysis }`
(`api-orbita-nodejs/src/services/searchService.js:566`) não é persistido em lugar
nenhum. A análise salva guarda o formulário e o mapa (`Analysis` em
`shared/models/analysis.model.ts:108-149`), mas **nenhum veredito**.

**Por que está errado.** A página do Confluence abre dizendo que hoje *"não fica
rastro de quem decidiu o quê"*. Um veredito que só existe enquanto a tela está
aberta não deixa rastro: dois meses depois ninguém sabe se o zoneamento foi
checado, contra qual base, com qual população, nem quantas lojas havia na época.

**Impacto de negócio de deixar como está.** Quando um associado contesta um
impedimento, ou quando alguém pergunta por que um ponto foi liberado, não há como
responder. E como a base de lojas é D-1 e a população pode mudar de fonte, o mesmo
ponto consultado em datas diferentes pode dar vereditos diferentes **sem que isso
seja um erro** — sem registro, essa diferença é indistinguível de uma falha.

**Alternativa descartada.** Recalcular o veredito na hora da leitura (em vez de
persistir um retrato) foi descartado: a base de lojas é D-1 e a fonte de população
ainda é decisão em aberto (Z3), então o mesmo ponto recalculado em outra data pode
dar outro resultado **sem que nada tenha dado errado**. Recalculando, a única prova
de que o veredito anterior existiu desaparece, e um associado que contesta um
impedimento não tem contra o que contestar. Por isso o registro é **retrato
imutável** (regra 6), e não valor derivado.

Rastreabilidade: Confluence 4545904644 v14 — seção "Validação 2 — ao salvar a
análise" (*"O veredito fica registrado junto da análise mesmo quando não há aviso,
com os números que o sustentam e a data da carga do Radar"*) e seção "Análise feita
pelo Órbita IA" (*"O veredito fica registrado junto da análise mesmo quando não há
modal, como no fluxo do mapa"*). Detalhamento em
`outputs/regras-negocio-zoneamento-orbita.md`, "RN-13 — Rastreabilidade do
veredito".

**Referências visuais:**
Não aplicável — card de persistência. A exibição do veredito registrado em alguma
tela **não está no escopo** (ver Pontos em aberto).

**Caminho/rota:**

**Não aplicável — fora dos 3 repositórios do Órbita.** A análise é gravada em
`POST ${apiExpansion}/analysis` (`shared/services/analysis.service.ts:71-76`) e
`PUT ${apiExpansion}/analysis/{analysisId}` (`:79-84`), e é lida em
`GET ${apiExpansion}/analysis/detail/{analysisId}` (`:65-69`) — é esse `GET` que os
critérios de aceite abaixo chamam de "quando a análise é consultada". Com
`apiExpansion = environment.api.expansion` (`core/http/http.base.service.ts:9`).
Essa API **não está em nenhum dos 3 repositórios** — o `api-orbita-nodejs` monta
apenas `/health`, `/imports`, `/sources`, `/markers`, `/grouping`, `/graphic`
(`api-orbita-nodejs/app.js:52-57`).

⚠️ **Atenção — existem dois `POST /analysis` diferentes no Órbita, e este card é
sobre o segundo:**
- `POST /analysis` do `api-agent-orbita` (`src/routes/analysis.routes.ts:7`):
  **calcula** a análise de viabilidade por IA, é stateless e **não grava nada**
  (`src/services/analysisAgent/index.ts:26-49`). **Não é aqui.**
- `POST ${apiExpansion}/analysis`: **grava** a análise do analista, mora na API de
  expansão, **fora destes 3 repositórios**. **É aqui.**

Quem grepar por `POST /analysis` acha o primeiro, que está clonado, e perde um dia
implementando persistência num serviço que não persiste.

**Escopo do card:**

* Persistir o veredito de zoneamento (Z5) **junto da análise**, nos dois fluxos: ao
  salvar no fluxo do mapa (Z7) e na tela final do Órbita IA (Z8).
* O registro guarda, no mínimo: o **resultado** (`liberado`/`alerta`/
  `impedimento`/`indeterminado`), as **regras aplicadas com o limiar de cada uma**,
  os **números que sustentam** (população e sua fonte, lojas, grupos, distâncias), a
  **data da carga do Radar**, as **lacunas declaradas** e **quando o veredito foi
  calculado**.
* Registrar **mesmo quando não houve aviso em tela**.
* **Não entra neste card:** exibir o veredito registrado em alguma tela (lista de
  análises, ficha da análise, relatório) — ver Pontos em aberto.
* **Não entra neste card:** recalcular o veredito depois. O registro é um retrato
  do momento, não um valor que se atualiza com a carga nova.
* ⚠️ **Atenção de escopo:** a implementação mora na API de expansão, fora destes 3
  repositórios. **Não inventar caminho de código** — este card precisa do
  repositório certo antes de ser estimado.

**Regras de negócio:**

1. **O veredito fica registrado junto da análise mesmo quando não há aviso em
   tela.** "Não mostrar" e "não registrar" são coisas diferentes: o caso `liberado`
   é justamente o que precisa de prova de que a checagem aconteceu.
2. O registro guarda **os números que sustentam o veredito**, não só o resultado.
   Sem os números, o registro não responde "por quê" dois meses depois.
3. O registro guarda a **data da carga do Radar** usada. A base é D-1 e envelhece;
   sem a data, não dá para distinguir um veredito correto de ontem de um veredito
   calculado sobre base defasada.
4. O registro guarda a **população usada e a fonte dela**, porque é ela que corta a
   faixa e o teto — e a fonte ainda é decisão em aberto (Z3).
5. O registro guarda as **lacunas declaradas** — por exemplo, lojas que não puderam
   ser checadas na distância por falta de coordenada. Um veredito `liberado` com 3
   lojas não checadas **não é a mesma coisa** que um `liberado` limpo.
6. **O registro é imutável.** Ele é o retrato do que a regra disse naquele momento,
   com aquela base. Recalcular por cima apagaria a única prova de que o veredito
   anterior existiu.
7. **Imutável inclui "não ser apagado por um re-save".** A atualização de análise é
   um `PUT ${apiExpansion}/analysis/${analysis.id}` que envia **o objeto `Analysis`
   inteiro** vindo do front (`shared/services/analysis.service.ts:79-84`). Se o
   front reenviar um objeto sem o veredito — ou com um veredito antigo carregado na
   tela — o `PUT` sobrescreve. **O servidor precisa ignorar ou rejeitar veredito
   vindo no corpo de um `PUT`**, em vez de confiar no payload. Editar o nome do lead
   de uma análise **não pode** mudar nem apagar o veredito.
8. **A mesma regra vale nos dois fluxos** — mapa e Órbita IA. A página diz
   explicitamente, para o fluxo da IA, "como no fluxo do mapa".
9. **O que NÃO muda com este card:** nenhum campo existente de `Analysis`
   (`shared/models/analysis.model.ts:108-149`) é alterado, renomeado ou removido.
   Este card **acrescenta** o veredito.
10. **O que NÃO muda com este card:** as análises já salvas não ganham veredito
    retroativo. Análise antiga fica **sem** veredito, e isso precisa ser
    distinguível de "veredito `liberado`" — **ausência de registro não é
    liberação**.

**Pontos em aberto:**

- **Qual é o repositório da API de expansão?** Não localizado nestes 3
  repositórios — a ausência vale para estes três, não para o produto. **Pista para
  encontrar o dono:** em produção a API responde em
  `https://expansion.api.radar.farmarcas.com.br`
  (`webapp-orbita-angular/src/environments/environment.production.ts:25`; em
  dev/staging, `https://api-stage.farmarcas.com.br/expansion`,
  `environment.staging.ts:30`) — host sob o domínio do **Radar**, então é com
  o time do Radar que se pergunta, não com "o time" em geral. Sem o repositório,
  este card não tem pista de código verificável e a estimativa não tem base.
- **O veredito registrado aparece em alguma tela?** A página v14 **não pede**
  exibição — e a versão 14 justamente *"Remove a regra de indicador de zoneamento
  verificado"*. Ou seja: a ideia de um indicador em tela existiu e **foi
  retirada**. Este card não a reintroduz. Confirmar se a decisão é definitiva ou se
  a exibição volta como card próprio.
- **Vereditos intermediários são registrados?** A validação 1 (Z6) roda a cada
  carregamento de ponto e pode rodar muitas vezes antes de existir uma análise
  salva. A página diz que o veredito fica registrado "junto da análise", o que
  sugere que só o do momento do salvar é persistido. Confirmar se os vereditos de
  triagem do mapa se perdem de propósito.
- **A análise do Órbita IA é persistida como análise?** Ver Z8, regra 7: **não foi
  encontrado nestes 3 repositórios nenhum ponto em que ela seja gravada**. Se não
  for, a regra 8 e a dependência Z10 ← Z8 são vazias.
- **Impacto de 2ª ordem — o volume de análises cresce.** O rascunho registra:
  *"Com o gate em toda entrada de análise, o volume de análises registradas cresce.
  Isso só não realimenta o teto porque apenas análise aprovada ocupa vaga — endereço
  consultado e descartado não reserva nada. Se essa distinção se perder na
  implementação, o produto passa a barrar a si mesmo: cada consulta fecharia um
  pouco mais o município."* **Este é o risco mais sério da feature inteira.**
  Confirmar que o registro do veredito **não cria análise nem reserva vaga**.
- **Impacto de 2ª ordem — LGPD no registro.** O veredito guarda dados das lojas que
  barraram. **Nome de pessoa não pode entrar nem no registro**, não só na tela — o
  rótulo anônimo do Z5 vale também aqui. Confirmar com quem cuida de LGPD qual é o
  prazo de retenção desse registro.
- **Impacto de 2ª ordem — quem mais lê a análise.** A base de análises já é lida
  como fonte do mapa (`structure.name: 'analysis_data'`,
  `api-orbita-nodejs/src/services/searchService.js:558`) e pelos indicadores
  (`getSummary` / `getSummaryBreakdown`, `shared/services/analysis.service.ts:173`
  e `:193`). Acrescentar um objeto de veredito a cada análise muda o payload lido
  por esses consumidores. Confirmar que nenhum deles quebra com campo novo.

**Critérios de aceite:**

- Dado uma análise salva cujo ponto **não tinha nenhuma violação**, quando a
  análise é consultada (`GET .../analysis/detail/{id}`), então existe um veredito
  registrado com resultado `liberado`, os números que o sustentam e a data da carga
  do Radar.
- Dado uma análise salva cujo ponto violava a distância mínima, quando a análise é
  consultada, então o veredito registrado traz a regra, o limiar aplicado, a
  distância medida, os dados da loja e contra qual dos dois endereços.
- Dado uma análise cujo veredito foi `liberado` **com lojas não checadas por falta
  de coordenada**, quando o registro é consultado, então as lacunas aparecem
  declaradas — o registro **não** é um `liberado` limpo.
- Dado uma análise salva ontem e uma carga nova do Radar hoje, quando o registro é
  consultado, então ele mostra a data da carga **de ontem**, não a de hoje, e os
  números **não** foram recalculados.
- Dado uma análise com veredito já registrado, quando o analista **edita e salva de
  novo** a análise (`PUT .../analysis/{id}`), então o veredito registrado
  **continua o mesmo** — não é apagado, não é sobrescrito pelo payload do front e
  não é recalculado com a carga de hoje.
- Dado um `PUT` de análise cujo corpo traz um objeto de veredito **diferente** do
  gravado, quando a requisição é processada, então o campo vindo do corpo é
  **ignorado** (ou a requisição é recusada) e o registro original permanece.
- Dado uma análise criada pelo **Órbita IA** sem modal, quando ela é consultada,
  então existe veredito registrado do mesmo jeito que no fluxo do mapa.
- Dado uma análise **anterior a este card**, quando ela é consultada, então ela
  aparece **sem veredito** — e isso é distinguível de um veredito `liberado`.
- Dado um veredito registrado, quando ele é consultado, então **nenhum nome de
  pessoa** aparece em campo nenhum; os grupos econômicos aparecem com rótulo
  anônimo.
- Não se pode fugir da seção Escopo do card
- Estar em conformidade com as regras de negócio
- Passar nos testes definidos por QA
- Conformidade com Figma: **não aplicável** (card de persistência, sem tela)

**Figma:** Não aplicável — card de persistência, sem tela.

**Estimativa:** [DEFAULT: 5 pts — confirmar com o time] — **estimativa sem base de
código**, o repositório da API de expansão não foi localizado.
**Prioridade:** [DEFAULT: P1 — confirmar com o time]
**Dependências:** Z5, Z7, Z8. **Bloqueado por:** identificação do repositório da
API de expansão.
**Revisado por (?_?) revisor-clareza-junior:** pronto para o júnior
