# Consolidado — revisão da spec modular do Órbita

Data: 2026-10-06
Spec revisada: `prompt-claude-design-orbita-modular.md` (515 linhas)
Revisores: executivo-expansao, analista-expansao, ux-researcher (independentes, em paralelo)
Pareceres completos: `revisao-executivo-expansao-modular.md`, `revisao-analista-expansao-modular.md`, `revisao-ux-researcher-modular.md`

Contexto confirmado pelo PM nesta sessão: a premissa da feature ("a tela é igual
para todo ponto") e a propriedade da régua de score são, ambas, dos executivos
da Farmarcas.

---

## Achado estrutural: a premissa executiva depende de uma capacidade que não existe

A spec promete que a IA monta a tela conforme o TIPO DE PONTO, e o cenário da
demo é "comércio de rua intenso". Mas:

- a **tipologia de ponto não existe no produto** — o estudo de bases a lista como
  médio prazo (analista B6). A montagem da IA e o EIXO 3 inteiro dependem dela.
- a variável que define essa tipologia é **fluxo de pessoas**, que o produto não
  tem. O indicador "Fluxo estimado de comércios no entorno" é **contagem de POI**,
  não fluxo (analista B7). Ver memória `orbita-gap-fluxo-pessoas-flutuante`.

Ou seja: o cenário escolhido para a demo é exatamente aquele cuja variável
decisiva o Órbita não mede. A feature é demonstrável, mas a demo afirma uma
capacidade que não está no produto nem no roadmap curto.

---

## TIER 1 — corrigir NA SPEC antes de gerar o protótipo

Baratos, e caros se passarem.

### 1.1 Score com denominador variável (3/3 revisores)
Hoje: score 0–20 fixo, `scorePercent = (score/20)×100`, corte `>= 34` = Recomendado
(`docs/confluence/ia/analises/estudo-peso-populacao-score-viabilidade.md:131,138`),
sobre 6.000+ análises em `analysis_data`.

A spec (linhas 403 e 91) torna o denominador variável. Consequências:
- **Remover indicador ruim INFLA o score**: 10/20 = 50% vira 9/15 = 60%.
- **O corte de 34% perde referente** — 34% de 20 e de 15 não dizem a mesma coisa.
- **Gaming sem má-fé**: basta remover os blocos que penalizam.

FIX: exibir **dois números rotulados** — *Score Farmarcas* 0–20 com classificação
(decisório, comparável, imune à montagem) + leitura percentual da montagem
(exploratória, não decisória).

### 1.2 Classificação vigente ausente (analista B1)
A spec transcreve as 4 faixas de indicador corretamente, mas omite as faixas de
classificação do score (16–20 alta / 12–15 moderada / 8–11 baixa / <8 não
recomendado) e o limiar de 34%. Incluir.

### 1.3 Contradição aritmética no EIXO 2 (analista B8) — VERIFICADO
Raio 300m = 0,2827 km². População 1/5 = 10–20 mil residentes → densidade de
35.368 a 70.732 hab/km² → faixa "acima de 25.000" = 0 pontos.
Os dois exemplos da seção EIXO 2 ("população pontuou 1 de 5" e "densidade
pontuou alto por ser baixa") não coexistem.
FIX: recalcular os exemplos, ou mostrar explicitamente a inflação de setor
censitário sobre o mapa (que é a única forma de os dois coexistirem) — e isso
na verdade reforça a mensagem da feature.

### 1.4 Cenário de Franca frágil onde mais importa (analista, resposta 7)
Aluguel de R$ 4.000 para 350 m² = R$ 11,43/m² total, R$ 20/m² de área de venda.
Isso soa a ponto secundário, não a rua de alto fluxo perto de hospital — e é
exatamente o número que sustenta o **custo por m²**, a demonstração principal
da feature. Revisar com valor de mercado real de rua comercial em Franca.

### 1.5 "Empresário: Pedro" é o nome do PM
Trocar no cenário.

### 1.6 Renomear "Fluxo estimado de comércios no entorno"
É contagem de POI. Chamar de proxy explicitamente, ou a demo promete fluxo.

---

## TIER 2 — decisões de escopo (precisam da chamada do PM)

### 2.1 Cortar o construtor de gráficos da demo (executivo + ux)
Ocupa ~110 das 515 linhas e é um BI embutido. Executivo cortaria 4 das 6
perguntas, 7 das 8 regras de forma e 3 dos 4 eixos de crítica. UX classifica a
tela como três telas.

### 2.2 Inverter o seletor de fonte (analista B5 + ux H4 + descoberta)
A descoberta registra que o analista **já desconfia dos números e valida no
Google** (`orbita-descoberta-analise-pontos.md:46`) e que **ter que escolher a
base é causa do problema** (linha 34). Mostrar dois valores divergentes para o
mesmo indicador ataca frontalmente essa dor.
FIX: fonte padrão governada; a segunda fonte vira **sinal de divergência**
("as duas bases discordam em 38% aqui"), não escolha do analista.

### 2.3 Camadas ausentes da lista real (analista B3) — VERIFICADO
Faltam **Lojas Farmarcas / canibalização** (`orbita-2025.md:216`;
caso real em `evolucao-camadas/orbita-evolucao-camadas.md:12`), **Situação de
território** (provável gate, não indicador) e **Setor Censitário**
(`orbita-descoberta-analise-pontos.md:146,150`).
Um score que vê o concorrente a 200m e ignora a loja Farmarcas a 180m não
sustenta numa sala de executivos de Expansão.

### 2.4 Comparação entre análises entrega disclaimer, não resposta (analista B4)
Não há segundo cenário de dados na spec, e a comparação não cobre fonte.
O analista compara **mesmo ponto em dois raios**, dois endereços do mesmo
empresário, e loja nossa já aberta — não metodologias.

### 2.5 Montagem persiste só na sessão
Contradiz justificativa permanente de alerta grave e "salvar montagem como
padrão". Resolver.

---

## TIER 3 — não se resolve na spec

### 3.1 Não há checagem independente no circuito
Quem nomeou o problema, quem é dono da régua e quem assiste à demo são as mesmas
pessoas. O analista, que tem a dor documentada, está fora da cadeia.

### 3.2 A régua proposta tem dono e ele está na sala
Rebatizar "régua proposta, ainda não homologada" como **pedido de homologação**
desta reunião, com as 3 dimensões nomeadas (concorrência, comércio no entorno,
custo por m²). Transforma passivo em ask.

### 3.3 Três testes que não precisam de protótipo (ux)
1. Perguntar a origem exata do enunciado do problema aos executivos — 10 min.
2. Mostrar dois valores divergentes de população a 2 analistas — 30 min cada.
   Decide o item 2.2.
3. Consulta **somente leitura** em `analysis_data` (6.000+ análises): as
   combinações de camadas se repetem por analista? Decide se a modularidade
   tem demanda real. Requer autorização e ambiente confirmado.

### 3.4 Baselines que faltam para o caso de negócio (executivo)
Existe: OKR 3h→1h, 6.000+ análises, PostHog por tela.
Falta: tempo ativo por análise, volume/mês, retrabalho, divergência
score × decisão do comitê. Os três últimos saem de `analysis_data`.

---

## Convergência independente

| Achado | Exec | Analista | UX |
|---|---|---|---|
| Denominador variável quebra score/histórico | B2 | B2 | H6 |
| Spec aumenta conhecimento prévio, contra o objetivo | B1 | resp. 2 | H1 |
| São três telas; construtor de gráficos é BI embutido | sim | — | sim |
| Seletor de fonte é problema, não feature | — | B5 | H4 |
| Régua não homologada contamina o número do comitê | B3 | B1 | — |

Três revisores com prompts e evidências diferentes convergiram no denominador do
score. É o achado mais sólido da revisão.
