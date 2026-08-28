# POC - Consulta Externa de Farmácias no raio

> Fonte: https://farmarcas.atlassian.net/wiki/spaces/SR/pages/4107567117/POC+-+Consulta+Externa+de+Farm+cias+no+raio · Última atualização no Confluence: ago. 11, 2026
> Nota: esta página continha imagens no Confluence original que não puderam ser migradas automaticamente. Consulte a fonte acima para o conteúdo visual completo.

# Definição do Objetivo

‌

Esta POC tem como objetivo validar a viabilidade técnica de, dado um **endereço e um raio de proximidade**, retornar uma **lista estruturada de farmácias** encontradas na região analisada, utilizando fontes externas confiáveis, para servir de insumo na investigação dos analistas.

Hoje as informações da base interna não são 100% corretas ou completas, e o analista realiza essa busca manualmente. A proposta é automatizar a descoberta inicial de estabelecimentos na área, facilitando o trabalho de conferência e, futuramente, permitindo um **comparativo com os dados internos**, de forma que o analista passe a **confirmar** ao invés de **buscar uma a uma e ainda validar os dados**.

> _**Info:** Embora a história mencione que "a resposta venha da IA consultando na internet", a abordagem recomendada **não utiliza o LLM como fonte de descoberta de farmácias**. A busca real deve ser feita por APIs determinísticas, como **CNES**, **Google Places** ou a base **MongoDB**, com orquestração determinística no backend. A IA, quando utilizada, entra apenas de forma opcional para formatação ou resumo textual, seguindo o mesmo princípio já adotado na análise de viabilidade: dados primeiro, narrativa depois._

---

## Contexto Atual

‌

Atualmente, o Órbita possui partes relevantes desse fluxo, porém de forma fragmentada entre frontend, backend e fontes de dados distintas.

Já possuímos uma base interna relevante implementada, que é o fluxo de busca por endereço e raio via GET /layers/radius. O backend consulta camadas no MongoDB, incluindo a camada Concorrentes, com dados curados pelos analistas, como CNPJ, rede, razão social e endereço. Essa camada é valiosa, mas pode estar incompleta ou desatualizada em relação ao que existe de fato na região.

No frontend, já existe integração com Google Maps por meio do `PlaceService.getNearby()`, que executa nearbySearch diretamente no browser. Esse recurso é utilizado de forma pontual no mapa, com termo livre e tipo genérico de estabelecimento, sem endpoint dedicado no backend, sem lista tabular estruturada e sem cruzamento automático com a base interna.

A `api-agent-orbita` já possui integração com Gemini via LangChain em POST `/analysis`. O padrão atual separa o cálculo determinístico da narrativa gerada pela IA. Hoje, porém, a IA não busca farmácias, ela apenas analisa dados demográficos já estruturados.

O geocoding ocorre no frontend. O backend recebe apenas lat, lng e radius, sem aceitar endereço textual. No frontend, o Google Maps é usado via SDK JavaScript, que é um pacote diferente do instalado no backend.

---

## Viabilidade Técnica

‌

A implementação é viável com a stack atual. Não há necessidade inicial de trocar Gemini por outra ferramenta de IA, nem de adotar soluções de "IA navegando na web".

Durante este estudo, foi realizada uma pesquisa comparativa sobre qual fonte externa utilizar para obter a listagem de farmácias. A conclusão principal é que a Google Places API, embora seja a solução mais conhecida e já parcialmente presente no frontend, não é a fonte mais assertiva para o contexto brasileiro quando o objetivo é apoiar a conferência cadastral dos analistas. Ela continua sendo adequada para descoberta complementar, mas existem alternativas oficiais, em especial o **CNES**, com maior valor cadastral, incluindo CNPJ.

A principal mudança arquitetural, portanto, não é apenas "ligar o Google Places no backend", mas sim definir uma estratégia de fontes e criar um novo fluxo que orquestre geocoding, consulta externa, cruzamento com a base interna e normalização do retorno. A IA permanece opcional e subordinada aos dados retornados pelas APIs.

A IA não deve ser responsável por "inventar" ou "descobrir" farmácias. A busca real deve continuar sendo feita por código e APIs/banco de dados.

---

## Análise Comparativa de Fontes de Dados

‌

Conforme pesquisa realizada, Google Places API não é a fonte mais assertiva para o contexto brasileiro. É adequada para descoberta, mas existem alternativas oficiais com maior valor cadastral.

‌

**Comparativo geral**

| Fonte | Assertividade | CNPJ | Busca por raio | Cobertura | Custo | Melhor para |
| --- | --- | --- | --- | --- | --- | --- |
| CNES ([http://gov.br](http://gov.br) ) | Alta | Sim | Sim | Registradas; pode ter defasagem | Gratuito | Fonte primária recomendada |
| Google Places API | Média | Não | Sim (até 50 km) | Ampla, incompleta | Pago | Descoberta complementar |
| MongoDB Concorrentes | Alta (curados) | Sim | Sim (implementado) | Só cadastrados | Infra existente | Comparativo |
| ANVISA | Alta | Sim (unitário) | Não | Validação | Gratuito | Conferência pós-lista |

Sobre o **Google Places**, a documentação oficial aponta limitações relevantes: teto de 60 resultados por consulta, viés de "prominência", ausência de CNPJ, dados comerciais (não regulatórios) e custo por requisição.

Sobre o **CNES**, trata-se do cadastro oficial e obrigatório de estabelecimentos de saúde no Brasil, incluindo farmácias (tipo 43 – FARMÁCIA). Oferece CNPJ, endereço, coordenadas e atualização diária via Portal de Dados Abertos do SUS. A busca por proximidade pode ser feita via API REST ou WebService SOAP do DATASUS. Limitações: possível defasagem cadastral pequena, de no máximo 15 dias de defasagem, coordenadas derivadas do endereço e raio informado em quilômetros (300 m = 0,3 km).

---

## Evidências Técnicas Encontradas

‌

No backend, já existe integração madura com Gemini + LangChain + Zod e busca geoespacial por raio com a camada Concorrentes.

No frontend, a UI de endereço + raio já existe, e o `PlaceService.getNearby()` comprova a viabilidade de nearby search via Google Maps SDK no browser. Ainda não há componente de lista dedicada para farmácias descobertas externamente.

Na pesquisa de fontes externas, identificamos o CNES como alternativa oficial com busca georreferenciada e CNPJ; o Google Places como complemento; e a ANVISA como validação por CNPJ.

Portanto, a POC pode reaproveitar boa parte da arquitetura atual, em especial `searchLayersByRadius()`, criando principalmente um novo fluxo de consulta externa e cruzamento de fontes.

---

## Cenários de Implementação

‌

### Cenário 1 — CNES + Places + Concorrentes (Recomendado produção)

Adota arquitetura híbrida: **CNES** como fonte primária (com CNPJ), **Google Places** como complemento, cruzamento com **Concorrentes**.

Quando o analista informar endereço e raio: → o backend geocodifica; → consulta CNES e Google Places; → faz merge e deduplicação; → cruza com Concorrentes; → retorna lista com flags de origem.

Prós: maior assertividade (CNPJ via CNES), cobertura ampla, comparativo com base interna. Contras: maior complexidade, dois provedores externos, latência maior. Custo: \~US$ 110/mês (com cache \~US$ 70/mês).

Veredito: Recomendado para produção.

‌

### Cenário 2 — Apenas Google Places (já parcialmente implementado)

Reutiliza `PlaceService.getNearby()` no frontend ou migra para backend.

Prós: menor esforço, time conhece Google Maps SDK. Contras: sem CNPJ, máximo 60 resultados, chave exposta no browser. Custo: \~US$ 110–300/mês conforme paginação.

Adequado para POC exploratória, não para assertividade cadastral plena.

Veredito: POC rápida de descoberta — não para assertividade cadastral.

‌

### Cenário 3 — Google Places + MongoDB (Concorrentes)

Places para descoberta + `searchLayersByRadius()` para cruzamento.

Prós: reaproveita infra existente, diff claro "já na base" vs "novo". Contras: Places sem CNPJ para novos, limite 60 resultados. Custo: \~US$ 110/mês (cache \~US$ 65).

Veredito: Bom equilíbrio custo × valor se CNES não estiver disponível a curto prazo.

---

## Quadro Resumo

‌

| Cenário | Assertividade | CNPJ | Esforço | Custo/mês | Recomendação |
| --- | --- | --- | --- | --- | --- |
| 1 — CNES + Places + Concorrentes | ★★★★★ | Sim | Alto | US$ 70–110 | Produção |
| 2 — Apenas Places | ★★☆☆☆ | Não | Baixo | US$ 65–300 | POC rápida |
| 3 — Places + Concorrentes | ★★★☆☆ | Parcial | Médio | US$ 65–110 | Evolução imediata |

---

## Arquitetura Recomendada (Cenário 1)

‌

Diferente do contexto atual, a arquitetura recomendada centraliza a orquestração no backend:

Quando o analista informar endereço e raio: → Front envia requisição para API; → Backend valida (Zod) e geocodifica; → Backend consulta CNES e Google Places; → Backend faz merge e cruza com Concorrentes; → Backend retorna JSON + flags; → Front exibe tabela, mapa e export; → (Opcional) IA formata resumo do diff.

**Separação de Responsabilidades**

Levando em consideração alucinações e rastreabilidade:

* CNES: farmácias registradas oficialmente (CNPJ, endereço).
* Google Places: complementar lacunas, não substituir CNES.
* MongoDB Concorrentes: comparativo interno, não substituir descoberta.
* Backend: orquestrar, validar, merge, cache, logs.
* IA: resumo opcional, não inventar estabelecimentos ou CNPJs.
* Frontend: entrada, lista, mapa, export, não chamar APIs externas direto em produção.

---

## Alterações Necessárias

‌

No backend:

* Criar POST `/pharmacies/search`;
* Ativar geocoding e integração CNES (+ Places se cenário híbrido);
* Serviço de merge; reaproveitar `searchLayersByRadius()`;
* Schemas Zod; cache e rate limiting.

No frontend:

* Serviço HTTP; componente de lista/tabela;
* Flags de origem, disclaimer, export CSV;
* Migrar nearby search para backend.

---

## Guardrails, Governança e Explicabilidade

‌

A API atual do Órbita foi construída com foco em entregar dados e análise de viabilidade, mas não foi desenhada desde o início com camadas explícitas de guardrails, governança ou explicabilidade para o analista. Em uma funcionalidade que combina fontes externas, base interna e, opcionalmente, narrativa de IA, esses pontos passam a ser requisitos.

### Guardrails (limites técnicos)

Guardrails são as regras de fronteira que impedem o sistema de sair do escopo seguro.

Na **entrada**, validar endereço e raio com Zod; tratar endereço ambíguo no geocoding retornando opções, não assumindo silenciosamente.

No **processamento**, a lista de farmácias só pode vir de CNES, Google Places e/ou MongoDB Concorrentes, nunca do Gemini. O merge entre fontes segue regras determinísticas (CNPJ exato, proximidade geográfica, similaridade de nome).

Na **saída**, validar resposta com Zod; se Gemini for usado, temperature 0, structured output e prompt explícito para não adicionar itens à lista. Em falha de API externa, erro claro, sem completar com IA.

Na **operação**, rate limiting, quotas, cache TTL, chaves Google apenas no backend.

### Governança (políticas e compliance)

Cada item deve indicar origem (`cnes`, `google_places`, `concorrentes`) e nível de confiança cadastral. Endereços pesquisados podem ter implicação LGPD, definir retenção de logs e minimizar dados enviados ao Gemini. Cumprir termos Google Maps (atribuição) e dados [http://gov.br](http://gov.br) . Manter billing alerts, monitoramento de custos e logs auditáveis (`requestId`, fontes consultadas, latência, status).

### Explicabilidade (por que o sistema retornou o que retornou)

Explicabilidade responde: "por que essa farmácia apareceu?" e "por que foi marcada como já existente na base?"

**Abordagem recomendada para esta POC — rastreabilidade nativa**

Como a descoberta é determinística (APIs + banco), a explicação deve ser transparente por construção:

* Fonte de cada registro
* `match_status` e `match_reason` no cruzamento com Concorrentes (_"CNPJ idêntico"_, _"nome similar + < 50 m"_)
* Endereço informado vs. geocodificado, com confiança
* Timestamp, raio e `requestId`

**Sobre LIME e SHAP**

LIME e SHAP são técnicas de explicabilidade **pós-hoc para modelos de machine learning** — atribuem importância a features para explicar uma predição opaca.

Nesta POC, **não é recomendado como abordagem principal**, porque:

* A lista de farmácias não vem de um modelo ML — vem de APIs determinísticas
* O score de viabilidade existente (`scoring.ts`) já é **regra explícita e testável**, não caixa-preta

| Contexto | LIME/SHAP? | Alternativa |
| --- | --- | --- |
| Lista CNES/Places/MongoDB | Não | Proveniência + flags + motivos |
| Merge heurístico | Parcial (se virar ML) | Score + limiar visível |
| Score viabilidade atual | Não necessário | Regras em código + testes |
| Modelo preditivo futuro | Sim | LIME/SHAP ou feature importance |

**Conclusão:** investir em explicabilidade nativa (proveniência, flags, motivos de match, disclaimers) traz mais valor aqui do que LIME/SHAP. Essas técnicas entram no radar **somente se** evoluirmos para modelos preditivos opacos, ex.: classificador de confiabilidade de POI ou matching aprendido.

**Gemini (se usado):** narrativa _grounded_ no JSON determinístico — contadores e flags reais no prompt; texto não altera a lista.

---

## Critérios de Sucesso

‌

Existem pontos que precisam ser estressados antes da implementação:

1. Lista retornada sem depender de IA para os dados.
2. CNPJ presente nos itens do CNES.
3. Geocoding resolve endereços BR; ambiguidade retorna opções.
4. Raio padrão 300m quando omitido.
5. Merge CNES + Places correto.
6. Match com Concorrentes identificado.
7. Sistema não inventa farmácias nem CNPJs.
8. UI exibe fonte e disclaimer.
9. Custos monitorados; latência < 5s.

---

## Riscos e Pontos de Atenção

‌

* Places como única fonte → baixa assertividade; mitigar com CNES primária.
* CNES desatualizado → Places como complemento.
* Custos Google → cache.
* API CNES indisponível → fallback Places + ETL local.
* Merge incorreto → regras por CNPJ + proximidade.
* Chave Google no frontend → backend proxy.
* LGPD em logs → retenção limitada.
* Confundir IA com descoberta → APIs determinísticas sempre.

---

## Recomendação Final

‌

A recomendação é evoluir a POC em etapas incrementais, aproveitando o que o Órbita já possui e validando cada camada antes de aumentar o investimento.

Para **validação inicial**, sugerimos começar pelo **Cenário 2 (Apenas Google Places)** — menor esforço, reaproveita o que já existe no frontend e permite testar rapidamente se a descoberta automatizada faz sentido. A expectativa, porém, deve ser de **lista exploratória**, não cadastral: o Places não traz CNPJ e depende de dados comerciais.

Em seguida, evoluir para o **Cenário 3 (Places + Concorrentes)**, cruzando a busca externa com a camada interna via `searchLayersByRadius()`. É aqui que a POC passa a entregar valor concreto ao analista — indicando o que já está na base e o que ainda precisa ser conferido.

Se o benchmark revelar lacunas relevantes (sem CNPJ, divergências frequentes, farmácias ausentes na base), avançar para o **Cenário 1 (CNES + Places + Concorrentes)** como **meta de produção** — combinando cadastro oficial, descoberta comercial e comparativo interno.

Sequência sugerida: **Cenário 2 → Cenário 3 → Cenário 1**.

Em todos os cenários, a busca real continua sendo feita por APIs e banco de dados, não pela IA; a camada Concorrentes deve ser enriquecida, não substituída; e o Gemini, se utilizado, fica restrito a formatação ou resumo.

Lembrando que não há impedimentos de seguirmos pelo **Cenário 1** diretamente, a ideia de implementação por camadas é apenas uma sugestão.
