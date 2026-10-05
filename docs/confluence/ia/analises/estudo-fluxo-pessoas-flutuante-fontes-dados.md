# Estudo: Fluxo de Pessoas Flutuante como Camada Complementar do Score

> Nota: documento interno gerado numa sessão de análise com Claude Code em
> 2026-09-17, não migrado do Confluence. Complementa
> `estudo-peso-populacao-score-viabilidade.md` e
> `evolucao-camadas/orbita-evolucao-camadas.md`.

## Problema

O score de viabilidade do Órbita (0–20 pontos, 4 dimensões: população
residente, densidade demográfica, potencial de consumo mensal, classificação
de renda) não modela fluxo de pessoas/veículos passantes. Isso já é um gap
documentado: áreas com poucos residentes mas alto movimento comercial (ex.:
25 de Março) tendem a ser subestimadas pelo modelo atual, porque a única
compensação parcial disponível é o `potencial de consumo`, que não equivale a
fluxo de passantes.

A pergunta que motivou este estudo: **existe uma API/fonte de dado pronta
para medir fluxo de pessoas/veículos num ponto específico, e como isso se
encaixa no que o Órbita já sabe que falta?**

## "Geospatial AI" do Google não resolve isso

Investigado e descartado como solução direta:
- É uma plataforma de analytics geoespacial no Google Cloud (BigQuery + Earth
  Engine + datasets como Waze/estradas), voltada a empresas de
  transporte/logística com equipe própria de engenharia de dados — não uma
  API simples de "fluxo de veículos neste endereço".
- O Traffic Layer do Google Maps é só uma camada visual de congestionamento
  em tempo real, sem contagem de veículos.
- A Routes API usa tráfego histórico/ao vivo apenas para estimar tempo de
  viagem, não para expor volume de veículos por ponto.
- Não existe API pública do Google que devolva volume histórico de tráfego
  (algo como AADT) para um endereço específico — limitação confirmada em
  fóruns oficiais do Google Maps.

## Fontes de mercado identificadas

| Fonte | Tipo | Observação |
| --- | --- | --- |
| **GeoFusion (Cortex Intelligence)** | Geomarketing BR | Já faz mapeamento de fluxo de pedestres e veículos especificamente para expansão de varejo/franquias no Brasil, cobertura declarada em >5.500 municípios. Candidato mais direto. |
| Operadoras de telecom (Vivo, Claro, TIM) | Mobilidade agregada | Movimentação de dispositivos por área/horário — proxy de pessoas, envolve negociação comercial/jurídica (LGPD). |
| StreetLight Data, INRIX, TomTom Move, HERE Traffic Analytics | Provedores globais de mobilidade veicular | Fortes em EUA/Europa; cobertura granular no Brasil **não confirmada** — não assumir sem checar diretamente com o fornecedor. |
| CET-SP, DER-SP, DNIT | Dados públicos/institucionais | Contagens volumétricas oficiais, cobertura limitada às vias monitoradas. |
| Google Places API (Popular Times/busyness) | Proxy gratuito | Mede movimento em estabelecimentos próximos, não fluxo na via — sinal indireto, mais fraco em cidades menores. |

## Gap nas skills e subagentes do projeto

Levantamento de `.claude/skills/` e `.claude/agents/` mostrou que nenhuma
skill precisava ser alterada, mas havia um gap real de subagente:

- `engenheiro-dados-geoespaciais` só avalia viabilidade técnica de uma fonte
  **já citada** na spec — reativo, não busca fontes alternativas no mercado.
- `analista-expansao` sinaliza que uma camada falta no dia a dia, mas não
  propõe fonte alternativa.
- `executivo-expansao` justifica ROI de investimento, mas não escolhe fonte.

Criado `.claude/agents/estrategista-fontes-dados.md` — subagente que mapeia
proativamente fontes de mercado (pagas, públicas e proxies) para qualquer
camada ausente ou frágil, com foco em custo x cobertura x confiabilidade no
Brasil. Reutilizável para outras camadas além de fluxo (ex.: concorrência,
renda), não só para este caso.

## Sequência de skills recomendada (nenhuma foi alterada)

1. `/problem-validation` — validar com analistas reais (JTBD + Mom Test) que
   pontos de perfil "25 de Março" (baixo residencial, alto fluxo comercial)
   são de fato mal avaliados hoje, antes de investir em fonte de dado paga.
2. `/pm-especialista` (RICE/ICE + decision-frameworks) — priorizar entre
   proxy barato (curto prazo) e fonte robusta paga (médio/longo prazo), com
   pré-mortem antes de fechar contrato.
3. Depois de decidido: `engenheiro-dados-geoespaciais` (viabilidade técnica
   da fonte escolhida) e `executivo-expansao` (ROI do investimento).
4. Só então `/software-improvement` ou `/claude-system-builder` para
   especificar e implementar a integração.

## Atualização (2026-09-17): pesquisa web sobre os pontos não confirmados

Rodado `(⚑_⚑) estrategista-fontes-dados` + pesquisa web dedicada para
aprofundar os dois pontos abaixo. Resumo do que foi **confirmado** e do que
**segue em aberto**, com fonte e nível de confiança de cada afirmação.

### GeoFusion / Cortex Intelligence

- A Geofusion foi adquirida pela Cortex Intelligence (aporte de R$260
  milhões) e passou a operar como "Cortex Geofusion" — confirmado, confiança
  alta (fonte oficial: https://www.cortex-intelligence.com/blog/geofusion-agora-e-cortex
  e imprensa: https://exame.com/negocios/apos-aporte-de-r-260-milhoes-cortex-adquire-geofusion-e-amplia-modelo-de-inteligencia-de-dados/).
- Existe um produto de API oficial, o **Data License Service (DLS)**
  (https://geofusion.cortex-intelligence.com/dls), para licenciamento de
  dados via API ou entrega em lote — confiança média-alta (site oficial).
  **Porém a página não confirma que o DLS cobre fluxo de pedestres/veículos**;
  o foco declarado é perfil populacional, consumo e dados de empresas. Isto é,
  a suposição original de que "a GeoFusion tem API pronta para fluxo por
  endereço" **não foi confirmada** — pode ser um produto diferente (relatório/
  plataforma fechada) ou pode nem existir como dado consultável.
- Preço não é público; funciona por proposta comercial (assinatura mensal ou
  licença anual, variável por módulo/volume) — confiança média (fonte
  terciária: https://ondeabrir.com/blog/ferramentas-de-geomarketing, cita
  clientes como McDonald's, Cacau Show, Whirlpool, Santander).
- **Risco novo, mais crítico que o original**: mesmo confirmando que existe
  API, não está confirmado que o dado por trás dela é fluxo **medido**
  (sensores, contagem, parceiro de dados) e não um índice **modelado/
  estimado** a partir de variáveis socioeconômicas — prática comum em
  geomarketing. Se for estimado, o valor incremental sobre o que o Órbita já
  calcula internamente (população + consumo + renda) pode ser bem menor do
  que o esperado. Isso precisa ser perguntado explicitamente ao fornecedor,
  não assumido a partir da existência da API.

### StreetLight Data, INRIX, TomTom Move, HERE Traffic Analytics

- **StreetLight Data**: foi adquirida pela TomTom
  (https://www.tomtom.com/customers/streetlight/). Sua página oficial de
  cobertura/pricing (https://www.streetlightdata.com/pricing/) só menciona
  América do Norte (25 milhões de segmentos de rodovia nos EUA), sem citar
  Brasil ou América Latina — sinal indireto forte (não uma negativa
  explícita) de que não é a rota certa aqui.
- **INRIX**: expandiu para o Brasil em 2012 via parceria exclusiva com a
  MapLink, cobrindo >10.000km de rodovias, ruas urbanas e vias locais
  (https://inrix.com/press-releases/inrix-expands-brazil-exclusive-traffic-partnership-maplink/).
  Ainda publicava dado de congestionamento de São Paulo em 2021
  (via Statista, confiança média). Cobertura confirmada existe, mas o anúncio
  original é de 2012 — não está confirmado o quanto essa cobertura ainda é
  ativa/atualizada nem se chega a cidades médias/pequenas do interior.
- **TomTom Move (Traffic Stats)**: Brasil está listado na "Global Product
  Coverage" oficial (https://docs.tomtom.com/move-portal/guides/coverage),
  incluindo Traffic Stats, Area Analytics, O/D Analysis. Confirma cobertura
  formal no Brasil, mas a documentação **não especifica granularidade** (rua
  local vs. só rodovia/eixo arterial).
- **HERE Traffic Analytics**: Brasil coberto em 3 sub-regiões (documentação
  oficial: https://docs.here.com/traffic-api/docs/traffic-here-traffic-api-v7-coverage-information),
  com nível "Deep Coverage 2.0" declarado. É o mais promissor dos 4
  provedores globais para uma eventual POC, mas o nível de detalhe real em
  cidade média/pequena não foi testado, só declarado em documentação.
- **Conclusão geral sobre os 4**: são produtos de **tráfego veicular em rede
  viária** (rodovia/avenida monitorada), não desenhados para medir "pedestre
  passando na calçada de um endereço específico" — que é o sinal que o caso
  "25 de Março" realmente pede. Mesmo onde a cobertura Brasil está
  confirmada (TomTom, HERE), ela tende a ser mais forte em grandes eixos e
  centros urbanos, o que é o oposto de onde a Farmarcas também abre lojas
  (cidades médias/pequenas do interior).

### Fonte recomendada, com ressalva

**GeoFusion/Cortex segue como candidato mais alinhado ao caso de uso**
(única fonte desenhada desde a origem para decisão de expansão de varejo no
Brasil, com cases de varejo/franquia), mas a recomendação **não pode mais
ser tratada como "confirmada, só falta negociar preço"**. Ela está
condicionada a 3 perguntas bloqueantes diretas ao fornecedor, que nenhuma
pesquisa pública resolve:

1. O DLS (ou outro produto da Cortex Geofusion) realmente expõe fluxo de
   pedestres/veículos por endereço pontual, ou isso é um dado diferente do
   que a API cobre hoje?
2. Esse dado é medido/observado ou é um índice modelado a partir de outras
   variáveis (o que reduziria o valor incremental para o Órbita)?
3. Modelo de precificação (por consulta vs. assinatura fixa) — decisivo
   porque o Órbita consulta pontos em volume, não pontualmente.

Os 4 provedores globais de tráfego veicular não são descartados, mas
**HERE Traffic Analytics** é o único que justificaria uma POC exploratória
como fonte complementar (ex.: pontos à beira de rodovia/avenida monitorada);
os demais (StreetLight, INRIX, TomTom Move) têm sinais mais fracos ou mais
desatualizados de relevância para o caso de uso da Farmarcas.

## Riscos e suposições ainda não confirmadas

- **[Bloqueante, requer contato comercial]** Se a GeoFusion/Cortex realmente
  expõe fluxo de pedestres/veículos via API (DLS ou outro produto), e se
  esse dado é medido ou estimado por modelo.
- **[Bloqueante, requer contato comercial]** Modelo de precificação da
  GeoFusion/Cortex (por consulta vs. assinatura fixa) — muda o caso de
  negócio inteiro dado o volume de consultas do Órbita.
- Cobertura granular real dos 4 provedores globais fora de grandes eixos
  rodoviários segue sem validação de campo (só documentação oficial) —
  nenhum foi testado com amostra real em cidade média/pequena brasileira.
- Dado de telecom depende de avaliação jurídica (LGPD), o que pode adicionar
  meses ao cronograma.
- Google Places como proxy tende a ser mais fraco em cidades menores/interior,
  onde a Farmarcas também abre lojas.
- Nenhuma fonte paga deveria ser contratada antes de `/problem-validation`
  confirmar volume/frequência real do problema "25 de Março" na carteira de
  pontos avaliados pela Farmarcas — o gap está documentado conceitualmente,
  mas não há dado de quantos pontos reais isso afeta por ano.

## Próximos passos

1. Rodar `/problem-validation` com analistas de Expansão sobre a hipótese do
   perfil "25 de Março" — antes de comprometer orçamento em qualquer fonte
   paga.
2. Contato comercial com Cortex Geofusion para responder as 3 perguntas
   bloqueantes da seção acima (escopo real do DLS, natureza medida vs.
   estimada do dado, e modelo de precificação).
3. Se a GeoFusion não confirmar dado de fluxo real, avaliar POC com HERE
   Traffic Analytics como fonte complementar para pontos próximos a
   rodovia/avenida monitorada, e reconsiderar telecom (Vivo/Claro/TIM) como
   rota de médio/longo prazo apesar do cronograma jurídico mais longo.
