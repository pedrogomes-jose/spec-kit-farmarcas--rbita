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

## Riscos e suposições ainda não confirmadas

- Modelo comercial da GeoFusion (SaaS fixo vs. por consulta) e se oferecem
  API para consulta pontual por endereço — não confirmado, checar
  diretamente com o fornecedor antes de assumir viável.
- Cobertura granular real de StreetLight/INRIX/TomTom/HERE no Brasil fora de
  grandes eixos rodoviários — não confirmado.
- Dado de telecom depende de avaliação jurídica (LGPD), o que pode adicionar
  meses ao cronograma.
- Google Places como proxy tende a ser mais fraco em cidades menores/interior,
  onde a Farmarcas também abre lojas.

## Próximos passos

1. Rodar `/problem-validation` com analistas de Expansão sobre a hipótese do
   perfil "25 de Março".
2. Testar `(⚑_⚑) estrategista-fontes-dados` de verdade (requer sessão do
   Claude Code recarregada após a criação do arquivo) para aprofundar a
   comparação de fornecedores.
3. Contato comercial com GeoFusion para confirmar modelo de API e preço antes
   de qualquer decisão de investimento.
