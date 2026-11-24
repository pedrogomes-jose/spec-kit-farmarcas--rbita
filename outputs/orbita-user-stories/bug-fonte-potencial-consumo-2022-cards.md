### [Dados/Produção] Restaurar a fonte "Potencial de Consumo 2022" no cadastro de fontes de produção

**Contexto:**

COMPORTAMENTO ATUAL — Quando o Órbita analisa um ponto no nível "município", a API `GET /layers/radius?level=municipio` busca quatro indicadores municipais de uma vez (população, densidade demográfica, potencial de consumo e renda média). Para cada um, ela procura na coleção `sources` do MongoDB um registro cujo nome seja exatamente o nome esperado, e esse registro é quem diz em qual coleção do banco a base realmente mora. Em produção, a busca pelo registro **"Potencial de Consumo 2022"** não retorna nada, e a API responde HTTP 500 com `Fonte de dados "Potencial de Consumo 2022" não encontrada, removida ou com importação falha em "sources".`

POR QUE ESTÁ ERRADO — Esse registro é cadastro de dado, não código: ele existia quando o endpoint foi escrito e saiu do estado esperado em produção. Pela consulta que o código faz, só há duas formas disso acontecer: **(a)** não existe nenhum documento em `sources` com `name` ou `structure.name` igual a "Potencial de Consumo 2022" — por exemplo, a base foi reimportada com outro nome; ou **(b)** existe, mas está com status -1 ou 1, os dois únicos que a consulta descarta. Nenhuma das duas gera alerta hoje: o time só descobre quando um analista abre a tela e toma erro.

Esse padrão de falha já tem precedente no produto: em 20/08/2026 a camada de concorrentes trocou de safra e o código teve de ser ajustado junto (commits `b7dd347` e `266e4f9`). O nome "Potencial de Consumo 2022", por sua vez, entrou no código em 22/10/2026 (commit `6fb82dc`) e nunca mudou desde então — o que reforça a hipótese (a): a base mudou em produção e o código não soube.

IMPACTO DE NEGÓCIO — As quatro buscas rodam em paralelo com `Promise.all` (`cityInfluence.ts:51-72`), então a falha de UMA derruba a resposta inteira. O analista de Expansão não perde só o potencial de consumo: ele recebe erro 500 e **nenhum** número municipal — população, densidade, consumo e renda, todos juntos. Não há degradação parcial nem fallback. Na prática, toda análise em nível município está parada em produção.

TERMOS — **"Fonte de dados"** é o registro na coleção `sources` que aponta para a coleção do Mongo onde a base está carregada; o nome dela é a chave de busca. **"Nível município"** é o modo de análise em que os números vêm das bases do município inteiro, em vez das bases censitárias contidas no raio desenhado no mapa. **"Vintage"** (usado nos Pontos em aberto) é a safra/ano da base — no Órbita o ano costuma vir no próprio nome da fonte (ex.: "Concorrentes 2023" → "Concorrentes 2025").

ALTERNATIVAS DESCARTADAS — Nenhuma registrada na origem.

Rastreabilidade: erro capturado em produção pelo PM na aba Network do navegador em 17/11/2026 (print anexo ao card); payload de resposta `{ error: "Fonte de dados \"Potencial de Consumo 2022\" não encontrada, removida ou com importação falha..." }`. A mensagem é emitida em `api-agent-orbita/src/db/mongo.ts:52-57`.

**Referências visuais:**
Print do DevTools (aba Network → Preview) com o payload de erro, fornecido pelo PM em 17/11/2026 — anexar ao card no Jira.

**Caminho/rota:**
Não aplicável — card de dado/backend, sem tela própria.
Endpoint afetado: `GET /layers/radius` com `level=municipio` (`api-agent-orbita/src/routes/layers.routes.ts:7` → `src/controllers/layers.controller.ts:5-19` → `src/services/radiusSearch/index.ts:355-395` → `src/services/radiusSearch/aggregations/cityInfluence.ts:40-87`).
A tela que dispara esse endpoint **não foi localizada nestes 3 repositórios** — `webapp-orbita-angular` não chama `/layers/radius`. Ver Pontos em aberto 3.

**Escopo do card:**

* **Diagnosticar** o estado do cadastro, escrevendo a resposta no card.
  **Como fazer:** criar um script **somente leitura** em `scripts/`, espelhando o padrão já existente em `scripts/dt-1162-migracao.ts` (card SQO-1162, que tratou um problema irmão: a fonte "Concorrentes 2025" reimportada com dado corrompido — tem dry-run por padrão, `--apply` e `--rollback --backup=<arquivo>`). Reaproveitar `getDatabase()` / `disconnectFromMongo()` de `src/db/mongo.ts`; a conexão vem de `MONGO_CONNECTION` e o banco de `MONGO_DATABASE` (`src/config/env.ts:9-12` — **atenção: `MONGO_DATABASE` tem default `"orbita"`, então pode não estar no `.env` e ainda assim funcionar, apontando para um banco diferente do que você imagina**). Rodar com `npx tsx scripts/<seu-script>.ts`. O script deve responder:
  1. existe documento em `sources` com `name` OU `structure.name` igual a "Potencial de Consumo 2022"?
  2. se existe, qual é o `status` dele?
  3. a coleção indicada em `structure.name` existe de fato no banco, e tem documentos?
  4. a mesma checagem para **todas as 9 fontes** envolvidas numa chamada `level=municipio` (ver regra 8), não só para a que apareceu no erro.
* **Corrigir o cadastro** conforme o diagnóstico (reimportar a base, reativar o registro ou reapontar a coleção), de forma que passe a existir um documento com esse nome exato, com status 2 (Success), apontando para uma coleção que existe e está populada.
* **Validar** que o endpoint volta a responder 200 com os indicadores municipais preenchidos, e que não caiu em nenhum dos outros dois erros do mesmo resolvedor: `"...não informa o nome da coleção"` (`mongo.ts:63-68`) e `"Coleção X, referenciada pela fonte de dados Y, não existe no banco"` (`mongo.ts:74-79`).
  **Os testes automatizados NÃO validam este card.** `pnpm test` (Vitest) roda com o Mongo mockado em `cityInfluence.test.ts:22` — ele passa verde com a produção quebrada e continuará passando depois do conserto, sem provar nada. A validação deste card é só a chamada real ao endpoint contra o banco corrigido.
* **Não entra neste card:** alterar `resolveSourceCollectionName`, criar fallback para fonte ausente, tirar o ano do nome hardcoded, ou criar monitoramento de fontes quebradas. São consequências reconhecidas do mesmo problema e viram card próprio — ver Pontos em aberto 1 e 2.

**Regras de negócio:**

1. A aplicação resolve a fonte por **nome literal**: a consulta casa `structure.name` OU `name` exatamente igual a "Potencial de Consumo 2022" (`mongo.ts:31-50`). Logo, corrigir a base com qualquer outro nome (ex.: "Potencial de Consumo 2024") **não** resolve o erro. Se o time decidir trocar a vintage da base (Ponto em aberto 6), **este card deixa de ser suficiente** — mudar o nome da fonte exige mudar `collections.ts:16` e vira card de código, não de dado. Enquanto essa resposta não vier, vale a regra: o nome cadastrado tem de ser exatamente "Potencial de Consumo 2022".
2. Havendo mais de um registro com o mesmo nome, vence o de alteração mais recente (`lastChangeDate` = maior entre `updateDate` e `creationDate`, ordenado desc, limite 1 — `mongo.ts:42-48`). Por isso não é necessário apagar o registro antigo: basta que o correto seja o mais recente.
3. Só os status **-1** e **1** são descartados pela consulta. **Atenção ao vocabulário: o mesmo status tem dois nomes.** No `api-agent-orbita` eles se chamam `REMOVED` (-1) e `IMPORT_FAILED` (1) (`collections.ts:39-42`); no cadastro legado, de onde o dado vem, são `Deleted` (-1) e `Error` (1) (`api-orbita-nodejs/src/models/source.js:2-9`). São os mesmos valores. Os demais status do legado — `Reindexed` (-2), `Processing` (0), `Success` (2), `OnHolding` (3) — **passam** no filtro. Ou seja, deixar a fonte em Processing faz o erro sumir e o número vir incompleto, que é pior que o erro. A correção só está pronta com status **2 (Success)**.
4. A base reimportada precisa manter o campo de **chave**: o município é casado por `properties.CODIGO` (`MUNICIPAL_INDICATOR_FIELDS.CONSUMPTION_CODE`, `collections.ts:29`), comparado contra o `CD_MUN` do ponto convertido para **string** (`cityInfluence.ts:50` e `:62-67`).
5. E precisa manter o campo de **valor**: `properties.PotencialdeConsumoTotalDrogarias`. Esse nome **não está em `collections.ts`** — está escrito direto no código em `cityInfluence.ts:79-81`. **Não confundir** com `CONSUMPTION_FIELDS.TOTAL_DRUGSTORE` (`collections.ts:57`), que é `properties.PotencialdeconsumoDrogarias-SetorCensitario`, o campo da base **de setor censitário**: nome parecido, base diferente. Se qualquer um dos dois nomes (chave ou valor) mudar, o erro 500 some mas o potencial de consumo passa a retornar 0 em silêncio — falha mais cara de achar que a atual.
6. O campo `PotencialdeConsumoTotalDrogarias` carrega o **total anual do município inteiro, em R$** — não é per capita e não é mensal (ordem de grandeza: bilhões para uma capital; ex.: 5.957.970.574,15, valor usado no teste `cityInfluence.test.ts:120`). O produto exibe o valor **mensal**, dividindo por 12 no código (`radiusSearch/index.ts:386`). A base deve continuar sendo anual; não converter nada na importação.
7. Não é necessário deploy nem restart da API: **enquanto a fonte estiver quebrada**, cada requisição reconsulta `sources`, porque o cache de resolução apaga a entrada sempre que a resolução falha (`mongo.ts:104`). Mas o caminho de **sucesso** é cacheado por 60s (`SOURCE_CACHE_TTL_MS`, `mongo.ts:10` e `:102`): se você aplicar um conserto que resolve para a coleção errada e depois corrigir de novo, espere até 60s antes de concluir que o segundo conserto não funcionou.
8. Corrigir só esta fonte pode não bastar para o endpoint voltar a 200. Antes de chegar aos indicadores municipais, `searchLayersByRadius` executa a busca de setor inteira (`radiusSearch/index.ts:362`), que resolve outras fontes pelo mesmo mecanismo. O conjunto que precisa estar saudável para um `level=municipio` responder 200 é: **Setor censitário, Potencial de Consumo - Setor Censitário, Renda Média, Concorrentes 2025, Municípios, População MM 2023, Densidade Demográfica MM, Potencial de Consumo 2022, Renda Média Municipio** (`collections.ts:5-18`). Checar todas de uma vez no diagnóstico.
9. **O QUE NÃO MUDA:** as fontes de nível setor continuam como estão — `level=setor` é o padrão do endpoint e não passa por esta fonte (`requests.ts:26-31`).
10. **O QUE NÃO MUDA:** o endpoint `POST /analysis` não é afetado — o `analysisAgent` não chama `searchLayersByRadius` em lugar nenhum, e não usa "Potencial de Consumo 2022". Não tocar nele neste card.

**Pontos em aberto:**

Os itens **1 (causa raiz)** e **4 (ambiente/permissão)** **bloqueiam o início da execução** — não começar sem resposta. Os demais podem ser respondidos durante.

1. **Causa raiz ainda não determinada — não corrigir sem responder.** O código permite duas causas distintas ("não encontrada" vs. "status -1 ou 1") e a mensagem de erro junta as duas numa frase só. Se a causa for troca de vintage, repetir a importação com o nome antigo resolve hoje e quebra de novo no próximo ano: o nome está hardcoded com o ano em `collections.ts:16`, junto com "Concorrentes 2025" (:11), "REGIC 2018 - Município" (:13) e "População MM 2023" (:14). **Isso ultrapassa o escopo deste card** — abrir card técnico separado para desacoplar nome de fonte da vintage da base.
2. **Não existe detecção automática de fonte quebrada.** O incidente foi descoberto por um usuário em produção. Confirmar com o time se vale card de monitoramento (healthcheck que resolve todas as fontes de `SOURCE_NAMES` e alerta) — fora do escopo deste card.
3. **Qual tela dispara `/layers/radius?level=municipio`?** Nenhuma chamada a esse endpoint foi encontrada **nestes 3 repositórios** do Órbita. Já descartado nesta investigação: o `webapp-orbita-angular` consome a API legada (`POST /sources/search`, `source.service.ts:76-89`), não o `api-agent-orbita`. Procurar fora destes 3 repositórios e confirmar com o time, para dimensionar o alcance do incidente e saber onde validar a correção.
4. **Ambiente e permissão.** O card pressupõe correção em **produção**. Confirmar quem tem acesso e executa (provável que um júnior não tenha), se a mesma falha existe em homologação, e se a reimportação passa pela tela de fontes do Órbita legado ou por carga direta no banco. Sem isso resolvido, o card não é executável e não deve entrar na sprint.
5. **Registro antigo duplicado.** Pela regra 2 ele é inofensivo para esta correção, mas confirmar com o time se deve ser marcado como -1 para limpeza, em vez de ficar no banco.
6. **Comparabilidade histórica.** Se a correção trouxer uma vintage diferente de 2022, o potencial de consumo municipal muda para todos os pontos já analisados, e análises novas deixam de bater com relatórios antigos do mesmo endereço. Confirmar com o dono do produto se a vintage pode mudar nesta correção ou se deve ser mantida 2022.

**Critérios de aceite:**

- Dado um ponto dentro de um município com base de consumo carregada, quando `GET /layers/radius?lat=<lat>&lng=<lng>&radius=<m>&level=municipio` é chamado, então a resposta é HTTP 200 e `summary.consumptionPotential` vem maior que 0.
- Dado o mesmo ponto e a mesma chamada, quando a resposta é recebida, então `summary.population` e `summary.demographicDensity` vêm maiores que 0 — provando que as fontes municipais de população e densidade também resolveram. **`summary.averageIncome` não serve como prova**: quando o indicador municipal é nulo, o código mantém o valor calculado pelos setores do raio (`radiusSearch/index.ts:388-391`), então ele vem preenchido mesmo com a fonte "Renda Média Municipio" quebrada. Para validar a renda municipal, comparar o valor retornado com o `properties.Renda_media_domic_per_capita` do documento do município na coleção de renda municipal.
- Dado que o cadastro foi corrigido, quando se consulta a coleção `sources` em produção, então o documento vencedor para "Potencial de Consumo 2022" está com status 2 (Success) e aponta para uma coleção que existe e tem documentos.
- Dado um ponto dentro de um município que **não tem linha** na base de consumo (caso de borda), quando o endpoint é chamado, então a resposta é HTTP 200 e `summary.consumptionPotential` vem 0 — não 500. (Comportamento já coberto pelo teste "returns zero for an indicator the municipal base does not have", `cityInfluence.test.ts:150-164`.)
- Dado um ponto que **não cai em nenhum município** (ex.: coordenada no mar), quando o endpoint é chamado com `level=municipio`, então a resposta é HTTP 200 **com os números de setor**, e não com zeros — o código devolve o resultado de setor sem sobrescrever nada (`cityInfluence.ts:48` → `radiusSearch/index.ts:377`). Isso é o esperado, não um defeito; não abrir bug por causa disso.
- Dado que a correção foi aplicada sem deploy da API, quando chega a primeira requisição posterior à correção, então ela já retorna 200 (confirma a regra 7).
- Não se pode fugir da seção Escopo do card
- Estar em conformidade com as regras de negócio
- Passar na validação de QA, que **para este card** é a chamada real ao endpoint contra o banco corrigido — não a suíte automatizada (ver Escopo → Validar)
- Estar em conformidade com o Figma — **não aplicável neste card**, que não altera interface

**Figma:** Não aplicável — card de dado/backend, sem alteração de interface.

**Estimativa:** [A CONFIRMAR — definir só depois da resposta do Ponto em aberto 1. O card embute script de diagnóstico, execução em produção, escolha entre três consertos diferentes e possível reimportação de base; e se a vintage mudar, deixa de ser card de dado e vira card de código.]
**Prioridade:** [DEFAULT: P0 — confirmar com o time] (erro 500 em produção, sem workaround)
**Dependências:** Nenhuma
**Revisado por (?_?) revisor-clareza-junior:** pronto para o júnior
