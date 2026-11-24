# Vínculo Análise × Loja entre Órbita e Radar — cards para o board SQO

Épico: SQO-1362 — Vínculo Análise × Loja entre Órbita e Radar
Fonte primária: Confluence SR/4502421505 "Vínculo Análise × Loja entre Órbita e Radar" (v7, 2026-10-29).
Figma: Handoff — Órbita, página "✅📍 Refinamento 10/11 - Sprint Órbita IA alterações 4º trim 2" (node 12689-16549).
Revisado por (?_?) revisor-clareza-junior em 2026-11-09. Ajustado por Produto em 09/11: SQO-1365 excluído, regras do SQO-1364 enxugadas, seção "Pontos em aberto" removida dos cards.

---

### SQO-1364 — Tornar obrigatório o Tipo de Loja na análise e vincular a loja existente no Radar

**Contexto:** A análise de ponto já tem o campo Tipo de Loja (Nova, Conversão, Mudança de Ponto), mas ele é opcional e não aponta para nenhuma loja do Radar. Sem resposta obrigatória e sem o vínculo, o fechamento do contrato não tem como decidir se cria loja nova no Radar ou se aponta para a loja atual, e ninguém consegue dizer de qual análise uma loja nasceu. Glossário dos termos do domínio: ver a descrição do épico SQO-1362.

**Referências visuais:**
- Figma do refinamento 10/11/2026, quadro "FORMULÁRIO COMENTÁRIO PÚBLICO DEFAULT": a tela da análise, com os blocos Dados do Empresário, Dados Básicos da Análise, Oportunidade do Ponto, Localização do Ponto, Contratos, Comentários e Histórico da Análise.
- **A experiência de busca e vínculo da loja NÃO está desenhada.** A fonte declara "modal ou drop-down com busca, a definir com Design". Solicitar o desenho antes de iniciar o front-end.

**Caminho/rota:**
**Radar → ícone de 4 quadradinhos → Órbita → Análises de Pontos → abrir a análise → Dados Básicos da Análise**

Atenção: "Análises de Pontos" (plural) é o item de menu próprio que leva à listagem; "Análise de Pontos" (singular), logo acima no mesmo menu, leva ao dashboard de indicadores. São telas diferentes.

**Escopo do card:**
* Front-end do Órbita, em `webapp-orbita-angular/src/app/modules/analysis/pages/view/view.component.ts|html` — o mesmo componente atende `/analysis/create` e `/analysis/view/:analysisId` (`analysis.routes.ts`), então a mudança vale para criação e edição de uma vez. A pasta `pages/create/` tem só subcomponentes (comentário, contrato, histórico) e não é uma página.
* O select "Tipo de Loja" já existe em `view.component.html:43`, sem `[required]`; o bloqueio de salvamento entra em `analysisIsInvalid()` (`view.component.ts:347`), que hoje só valida Lead e ponto no mapa.
* Chamadas via `AnalysisService` (`src/app/shared/services/analysis.service.ts`), que fala com a API de expansão (`environment.ts:29`) por `HttpBaseService` (`http.base.service.ts:9`).
* **Não entra neste card:** a consulta de lojas ativas (SQO-1363), a exibição do tipo na listagem de análises e qualquer criação de loja (SQO-1366). A persistência do identificador da loja fica na API de expansão, **repositório fora dos 3 repos do Órbita — precisa de responsável nomeado no refinamento**.

**Regras de negócio:**
* O Tipo de Loja passa a ser obrigatório: enquanto não for respondido, o salvamento fica bloqueado com a mensagem "Informe se a análise é para mudança de ponto";
* Respondendo **Nova**, a análise é salva como ponto novo e nenhuma loja é vinculada;
* Uma análise se vincula a no máximo uma loja; a mesma loja pode estar vinculada a várias análises de mudança de ponto, porque são alternativas de ponto para a mesma loja;
* Loja que foi inativada depois do vínculo continua aparecendo na análise, marcada como inativa, e não bloqueia o salvamento;
* **O que não muda:** nenhum outro campo do formulário passa a ser obrigatório, e a edição continua sendo liberada pelo mesmo critério de hoje.

**Critérios de aceite:**
- Não se pode fugir da seção Escopo do card;
- Estar em conformidade com as regras de negócio;
- Passar nos testes definidos por QA;
- Documentação no Swagger.

**Figma:** https://www.figma.com/design/qQtvVeOKuSCk8eWM8859Nn/Handoff---%C3%93rbita?node-id=12715-22685

---
**Épico:** SQO-1362 — Vínculo Análise × Loja entre Órbita e Radar
**Rastreabilidade:** Confluence SR/4502421505 (v7, 2026-10-29), seção Regras de negócio → "Vínculo da análise com a loja (Órbita)".
**Referências técnicas:**
- (webapp-orbita-angular) `src/app/shared/models/analysis.model.ts:16-26` — `AnalysisStoreType` já tem Nova, Conversão e Mudança de Ponto
- (webapp-orbita-angular) `src/app/modules/analysis/pages/view/view.component.html:43` — select "Tipo de Loja" já em tela, sem obrigatoriedade
- (webapp-orbita-angular) `src/app/shared/services/analysis.service.ts:71,79` — criação e atualização da análise na API de expansão
**Pontos de atenção:**
- Trava o início: reutilizar o campo atual ou criar um novo, o tratamento de **Conversão** e o que fazer com as análises já salvas sem resposta
- A API que persiste análise e contrato (expansão) não está entre os repositórios do Órbita clonados; nenhum nome de campo foi confirmado por leitura
- O campo existe desde antes deste card: a base atual tem análises sem resposta, e a regra de obrigatoriedade incide sobre elas
**Prioridade:** [DEFAULT: P0 — confirmar com o time] (é a marcação de que todo o resto depende)
**Estimativa:** [DEFAULT: 5 pts — confirmar com o time]
**Dependências:** SQO-1363 (consulta de lojas ativas)

---

### SQO-1363 — Consulta de lojas ativas do Radar para vínculo na análise

**Contexto:** Para vincular a análise a uma loja existente, o analista precisa encontrar essa loja sem sair do Órbita. Hoje não existe nenhuma consulta de lojas do Radar disponível no front do Órbita. Glossário dos termos do domínio: ver a descrição do épico SQO-1362.

**Referências visuais:**
- Nenhuma referência visual fornecida — a tela que consome a consulta é a de SQO-1364, ainda não desenhada. Confirmar com design/PM.

**Caminho/rota:**
Não aplicável — card técnico. Consumido pela tela de SQO-1364 (**Radar → ícone de 4 quadradinhos → Órbita → Análises de Pontos → abrir a análise**).

**Escopo do card:**
* Consulta de lojas do Radar exposta ao Órbita, com busca por texto, paginação e tratamento de erro, consumível por `webapp-orbita-angular/src/app/modules/analysis`.
* **Não entra neste card:** a interface de busca e o vínculo em si (SQO-1364).

**Regras de negócio:**
* O termo de busca aceita nome/razão social, ID da loja e CNPJ, pesquisando nos três ao mesmo tempo, sem o usuário escolher o campo;
* Só lojas ativas entram no resultado, porque mudança de ponto só se aplica a loja em operação;
* Cada item traz ID da loja, nome/razão social, CNPJ formatado e endereço com logradouro, número e cidade/UF;
* O CNPJ é encontrado com ou sem máscara, e a busca ignora acento e caixa;
* A consulta é paginada em 20 itens por página e devolve o total de registros;
* Termo com menos de 3 caracteres não dispara a consulta;
* Loja sem CNPJ ou sem endereço cadastrado aparece no resultado com o campo vazio, em vez de ser excluída;
* Busca sem resultado devolve lista vazia com total zero e resposta de sucesso — nunca erro, para a tela saber diferenciar "não existe" de "falhou";
* Base de lojas indisponível devolve erro explícito, nunca lista vazia com sucesso, senão o analista conclui que a loja não existe;
* Quem não tem permissão de análise no Órbita recebe negação de acesso, não a lista;
* **O que não muda:** a listagem de lojas do Radar e os filtros que ele já oferece seguem como estão; esta consulta é adicional.

**Critérios de aceite:**
- Não se pode fugir da seção Escopo do card;
- Estar em conformidade com as regras de negócio;
- Passar nos testes definidos por QA;
- Documentação no Swagger.

---
**Épico:** SQO-1362 — Vínculo Análise × Loja entre Órbita e Radar
**Rastreabilidade:** Confluence SR/4502421505 (v7, 2026-10-29), seção "Vínculo da análise com a loja (Órbita)", item da busca.
**Referências técnicas:**
- (webapp-orbita-angular) `src/environments/environment.ts:34` — base do Radar já configurada no front do Órbita
- (api-orbita-nodejs) `src/controllers` — camadas, marcadores, fontes e gráficos; nenhuma entidade de loja, não é o alvo
- (api-agent-orbita) `src/constants/collections.ts` — só fontes de mercado (Concorrentes); não é cadastro de loja
**Pontos de atenção:**
- Não usar a camada Concorrentes como fonte de lojas: ela traz estabelecimentos de mercado, e casar por nome de bandeira ali devolve loja errada. A fonte é o cadastro de lojas do Radar, por ID e CNPJ
- O repositório que expõe lojas não está clonado: definir se a consulta nasce no Radar ou na API de expansão antes de estimar
**Prioridade:** [DEFAULT: P0 — confirmar com o time] (bloqueia o card 1)
**Estimativa:** [DEFAULT: 3 pts — confirmar com o time]
**Dependências:** Nenhuma

---

### SQO-1366 — Criar loja rascunho no Radar ao fechar o contrato de um ponto novo

**Contexto:** Quando o contrato de um ponto novo é fechado, alguém recria a loja no Radar à mão, redigitando endereço e coordenadas que já estão na análise, e sem registro de qual análise a loja veio. O gatilho automático elimina esse retrabalho e amarra loja, análise e contrato. **Loja rascunho** é um registro de loja no Radar criado automaticamente, ainda incompleto, que não conta como loja ativa — não confundir com **análise rascunho**, que é a análise salva sem ponto definido no mapa. Demais termos: ver a descrição do épico SQO-1362.

**Referências visuais:**
- Figma do refinamento 10/11/2026, nota do quadro de Gestão de Lojas: "RASCUNHO SERÁ SALVO EM GESTÃO DE LOJAS A PARTIR DO CONTRATO FECHADO AQUI NO ÓRBITA".

**Caminho/rota:**
**Radar → ícone de 4 quadradinhos → Órbita → Análises de Pontos → abrir a análise → bloco Contratos**

É nesse bloco que o status do contrato é alterado hoje. A tela "Contratos Fechados" do menu é somente listagem e não dispara nada — não é o ponto de entrada deste card.

**Escopo do card:**
* Criação automática da loja rascunho no Radar quando o contrato da análise fecha, com chave de vínculo entre análise, contrato e loja, e com retentativa, log e alerta em caso de falha.
* A alteração de status do contrato hoje passa por `webapp-orbita-angular/src/app/modules/analysis/pages/create/components/contract/contract.component.ts:70-105` e por `AnalysisService.updateContract` (`analysis.service.ts:237`), na API de expansão.
* **Não entra neste card:** exibir o vínculo em tela nos dois lados — a fonte declara que nesta entrega ele fica só no banco de dados.

**Regras de negócio:**
* Quando o contrato de uma análise de **ponto novo** fecha, o sistema cria automaticamente uma loja com status Rascunho no Radar;
* Cada análise/contrato gera no máximo uma loja rascunho: reprocessamento, reenvio do evento ou novo salvamento não criam duplicata, inclusive quando a primeira tentativa gravou mas a resposta se perdeu;
* Quando o contrato de uma análise de **mudança de ponto** fecha, nenhuma loja é criada — registra-se só o vínculo entre análise, contrato e a loja já existente;
* O vínculo para a análise e para o contrato de origem fica guardado apenas no banco de dados nesta entrega; não há tela que o mostre;
* A loja rascunho nasce com o endereço do ponto da análise (logradouro, número, bairro, CEP, cidade e UF), nome provisório, data de fechamento do contrato e o analista que **criou** a análise;
* A coordenada gravada é exatamente a do ponto da análise, sem arredondamento e sem nova geocodificação pelo endereço — é essa regeocodificação que hoje faz o pin da loja no Radar cair em lugar diferente do ponto analisado;
* Latitude e longitude são gravadas, mas não exibidas em tela;
* Análise sem Tipo de Loja preenchido não gera loja nenhuma: o contrato segue normalmente e o caso vai para log de tratamento manual;
* Se a criação falhar, o contrato continua fechado, o sistema tenta de novo e registra log e alerta para o time responsável; o contrato nunca é revertido por causa dessa falha;
* **O que não muda:** o fluxo de fechamento de contrato segue igual para quem opera; nenhuma etapa nova é pedida ao analista.

**Critérios de aceite:**
- Não se pode fugir da seção Escopo do card;
- Estar em conformidade com as regras de negócio;
- Passar nos testes definidos por QA;
- Documentação no Swagger.

---
**Épico:** SQO-1362 — Vínculo Análise × Loja entre Órbita e Radar
**Rastreabilidade:** Confluence SR/4502421505 (v7, 2026-10-29), seção "Criação da loja rascunho no fechamento do contrato"; nota do Figma no quadro de Gestão de Lojas.
**Referências técnicas:**
- (webapp-orbita-angular) `src/app/shared/models/analysis.model.ts:167-178` — `ContractStatus` só tem Não iniciado, Iniciado e Cancelado; "fechado" não existe
- (webapp-orbita-angular) `src/app/shared/services/analysis.service.ts:227,237` — criação e atualização do contrato na API de expansão
- (webapp-orbita-angular) `src/app/modules/contracts/pages/list/list.component.ts:109` — "Contratos Fechados" é só listagem, confirmado por leitura
**Pontos de atenção:**
- Idempotência é o risco central: sem restrição única no banco, duas execuções concorrentes passam as duas pela consulta prévia e duplicam a loja
- Repositórios da expansão e do Radar não estão clonados; nenhum nome de tabela ou campo foi confirmado, e a estimativa é otimista por isso
- Não atribuir a quem nunca mexeu no Radar: nenhuma pista de código do alvo pôde ser validada
**Prioridade:** [DEFAULT: P0 — confirmar com o time] (é o gatilho que resolve a dor central do documento)
**Estimativa:** [DEFAULT: 8 pts — confirmar com o time]
**Dependências:** SQO-1364

---

### SQO-1367 — Área de Lojas Rascunho em Gestão de Lojas

**Contexto:** As lojas criadas automaticamente pelo fechamento de contrato precisam de um lugar para serem vistas e trabalhadas, sem se misturar às lojas ativas nem entrar em relatório, indicador ou integração que conta loja ativa. **Loja rascunho** é um registro de loja no Radar criado automaticamente, ainda incompleto, que não conta como loja ativa — não confundir com **análise rascunho**, que é a análise salva sem ponto no mapa. Demais termos: ver a descrição do épico SQO-1362.

**Referências visuais:**
- Figma do refinamento 10/11/2026, quadro "1 - RASCUNHOS - GESTÃO DE LOJAS - Lojas associadas": listagem com as colunas Lead, Bandeira, Endereço Popular, Tipo de Loja, Status, Situação, última atualização de dados e Ações, com campo de busca, filtro de seleção, paginação e ação de edição por linha.
- Para comparação, o quadro "1 - GESTÃO DE LOJAS - Lojas associadas" mostra a listagem atual, com Contato, Anjo, Status, Situação, Razão Social, Bandeira, Bloqueio, G.E. e última atualização de dados.

**Caminho/rota:**
**Radar → Gestão de Lojas → Lojas Rascunho**

**Escopo do card:**
* Listagem das lojas rascunho dentro de Gestão de Lojas, com busca, filtros, permissão, estado vazio e as ações de visualizar e efetivar.
* Exclusão dos rascunhos de toda consulta que hoje devolve loja ativa.
* **Não entra neste card:** a tela de efetivação do cadastro (SQO-1368) nem o levantamento dos consumidores de loja ativa, que precisa ser um card próprio de investigação.

**Regras de negócio:**
* Gestão de Lojas ganha a área "Lojas Rascunho", separada da listagem de lojas associadas;
* Loja rascunho não aparece na listagem de lojas ativas e não entra em relatório, indicador ou integração que consome loja ativa;
* Nenhum contador existente de lojas ativas muda de valor por causa desta entrega;
* A listagem traz por linha: Lead, Bandeira, Endereço Popular, Tipo de Loja, Status, Situação, última atualização de dados e Ações;
* As ações por linha são visualizar detalhes e efetivar cadastro;
* Linha de rascunho quase sempre tem Bandeira, Tipo de Loja e Situação sem valor, porque a análise não preenche tudo: cada célula vazia exibe "-" e nenhuma quebra o layout;
* Sem nenhuma loja rascunho, a área mostra "Nenhuma loja em rascunho no momento" em vez de tabela vazia;
* Erro ao carregar mostra mensagem com ação de recarregar, sem derrubar a tela de Gestão de Lojas;
* Clicar em efetivar numa linha que outro usuário já efetivou informa "Esta loja já foi efetivada" e recarrega a lista, em vez de abrir o formulário;
* Só os perfis que hoje podem cadastrar loja no Radar enxergam a área e efetivam rascunho; sem permissão o item não aparece e o acesso direto pela URL é negado, nunca devolvendo lista vazia;
* Quando o rascunho é efetivado ou cancelado, a loja sai da listagem de rascunhos;
* **O que não muda:** a listagem de lojas associadas, suas colunas e seus filtros seguem como estão.

**Critérios de aceite:**
- Não se pode fugir da seção Escopo do card;
- Estar em conformidade com as regras de negócio;
- Passar nos testes definidos por QA;
- Estar em conformidade com o Figma.

**Figma:** https://www.figma.com/design/qQtvVeOKuSCk8eWM8859Nn/Handoff---%C3%93rbita?node-id=12715-23766

---
**Épico:** SQO-1362 — Vínculo Análise × Loja entre Órbita e Radar
**Rastreabilidade:** Confluence SR/4502421505 (v7, 2026-10-29), seções "Área de Lojas Rascunho (Radar)" e "Status da loja rascunho"; Figma Handoff — Órbita, quadro "1 - RASCUNHOS - GESTÃO DE LOJAS".
**Referências técnicas:**
- (Radar) repositório não disponível localmente — nenhuma tela, campo ou endpoint do Radar foi confirmado por leitura de código
- (webapp-orbita-angular) `src/environments/environment.ts:34` — confirma que o Radar é produto separado, hospedado fora do front do Órbita
**Pontos de atenção:**
- "Não entra em relatório, indicador ou integração que consome loja ativa" é o maior risco de regressão e exige mapear os consumidores de loja ativa antes: é card de investigação próprio, pré-requisito deste
- Não atribuir a quem nunca mexeu no Radar: nenhuma pista de código pôde ser validada
**Prioridade:** [DEFAULT: P1 — confirmar com o time]
**Estimativa:** [DEFAULT: 5 pts — confirmar com o time]
**Dependências:** SQO-1366; card de investigação dos consumidores de loja ativa

---

### SQO-1368 — Efetivar o cadastro da loja a partir da loja rascunho

**Contexto:** A loja rascunho só vira loja de verdade quando alguém da gestão de lojas completa o cadastro. Partir dos dados da análise evita redigitar endereço e coordenada, que é o retrabalho que originou toda esta mudança. Glossário dos termos do domínio: ver a descrição do épico SQO-1362.

**Referências visuais:**
- Figma do refinamento 10/11/2026, quadro "Rascunho Gestão de lojas": ficha da loja com cabeçalho (nome da loja, LEAD, ID) e os blocos Informações gerais (Endereço popular, Previsão de inauguração, Data de inauguração, Data de reinauguração, Endereço registrado na Receita), Transição de loja, Comentários, Anexos e Dados da loja.
- Nota do mesmo quadro: "O ENDEREÇO POPULAR PASSA PARA O FINAL DO FORMULÁRIO DA LOJA QUANDO SAI DO RASCUNHO, MANTENDO A MESMA ORDEM QUE JÁ ATUA HOJE ACRESCIDO DAS NOVAS INFOS: LEAD, BANDEIRA, TIPO DE LOJA, ÁREA DO IMÓVEL".

**Caminho/rota:**
**Radar → Gestão de Lojas → Lojas Rascunho → Ações → Efetivar cadastro**

**Escopo do card:**
* Ação "Efetivar cadastro" abrindo o cadastro de loja padrão já pré-preenchido pela análise, mais os quatro campos novos e a nova posição do Endereço Popular.
* **Não entra neste card:** a listagem de rascunhos (SQO-1367) e o cancelamento de rascunho, que não tem ação desenhada nem regra definida.

**Regras de negócio:**
* "Efetivar cadastro" abre o cadastro de loja padrão já com os campos pré-preenchidos pela análise;
* Enquanto a loja está em rascunho, o Endereço Popular aparece no bloco Informações gerais; a partir da efetivação ele aparece no final do formulário. A posição é definida na carga da tela pelo estado da loja, não reordenada durante a edição;
* Os campos Lead, Bandeira, Tipo de Loja e Área do Imóvel passam a existir no formulário de loja **para todas as lojas**, inclusive as cadastradas direto no Radar sem rascunho — para essas nascem vazios;
* Efetivado o cadastro, a loja deixa de ser rascunho e passa a aparecer nas listagens e consultas de loja;
* A loja efetivada mantém o vínculo com a análise e o contrato de origem — é a razão de ser da feature e não pode se perder na efetivação;
* Abrir a efetivação e fechar sem salvar deixa a loja como rascunho, sem alteração e sem registro parcial;
* Dois usuários efetivando o mesmo rascunho: o segundo recebe "Esta loja já foi efetivada por outro usuário" e nenhuma loja duplicada é criada;
* Erro de validação na efetivação mantém a loja como rascunho e preserva o que já foi digitado;
* Só os perfis que hoje podem cadastrar loja no Radar efetivam um rascunho;
* **O que não muda:** o **fluxo** de cadastro direto no Radar continua igual, com a mesma entrada e as mesmas validações de hoje. O **formulário**, esse muda para todos, porque ganha os quatro campos novos e a nova posição do Endereço Popular.

**Critérios de aceite:**
- Não se pode fugir da seção Escopo do card;
- Estar em conformidade com as regras de negócio;
- Passar nos testes definidos por QA;
- Estar em conformidade com o Figma.

**Figma:** https://www.figma.com/design/qQtvVeOKuSCk8eWM8859Nn/Handoff---%C3%93rbita?node-id=12715-23883

---
**Épico:** SQO-1362 — Vínculo Análise × Loja entre Órbita e Radar
**Rastreabilidade:** Confluence SR/4502421505 (v7, 2026-10-29), seção "Efetivação do cadastro (Radar)"; Figma Handoff — Órbita, quadro "Rascunho Gestão de lojas" e sua nota de ordem de campos.
**Referências técnicas:**
- (Radar) repositório não disponível localmente — o formulário de cadastro de loja não foi lido; nenhum campo foi confirmado por código
- (webapp-orbita-angular) `src/environments/environment.ts:34` — o cadastro de loja vive no Radar, fora dos repositórios do Órbita
**Pontos de atenção:**
- Os quatro campos novos e a nova ordem afetam todo cadastro de loja do Radar, não só os vindos de rascunho; medir o impacto antes
- Não atribuir a quem nunca mexeu no Radar: nenhuma pista de código pôde ser validada
**Prioridade:** [DEFAULT: P1 — confirmar com o time]
**Estimativa:** [DEFAULT: 5 pts — confirmar com o time]
**Dependências:** SQO-1367

---

## Pendências fora dos cards

* **Coluna "Identificação da Loja" na listagem de análises** — o card SQO-1365 foi excluído. O Figma (quadro "RASCUNHO ANÁLISES DE PONTO/MENU ABERTO") prevê a coluna e hoje nenhum card cobre isso. Confirmar se saiu do escopo de propósito.
* **Card de investigação:** mapear todos os consumidores de loja ativa no Radar — pré-requisito do SQO-1367.
* **Regra para contrato cancelado depois da loja rascunho criada** — estado que o sistema já produz hoje e que nenhuma fonte trata.
* **Confluence SR/4502421505 desatualizado:** diz "Figma: a ser construído" e descreve colunas da área de rascunhos que o desenho não tem.
