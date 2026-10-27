# Indicadores do relatório — fonte, fórmula e unidade

O relatório segue o layout do **relatório de viabilidade do Órbita**, com uma
diferença declarada: **não traz score nem status**. No lugar do bloco
Status/Score fica o veredito do **gate de zoneamento** e o resumo em uma linha.

As definições abaixo foram lidas no código do produto (`api-agent-orbita`), não
inferidas. Onde o nosso cálculo difere do dele, está dito.

---

## Como os indicadores de setor são rateados

Três métodos, escolhidos em `--metodo`:

| Método | O que faz | Quando usar |
|---|---|---|
| **`area`** (padrão) | cada setor entra pela **fração da área** dentro do círculo | sempre, salvo motivo |
| `inteiro` | soma o setor inteiro que toca o raio | só para comparar com o produto |
| `krigagem` | interpolação geoestatística, **só onde aplicável** | quando houver vizinhança e estrutura espacial |

**Extensivo × intensivo.** Total que se divide no espaço — residentes,
domicílios, potencial — rateia-se pela fração. Taxa — renda média, densidade,
percentuais — entra como **média ponderada**, e o peso muda conforme o que a
taxa descreve: renda por habitante pondera-se pela população dentro do raio;
percentual de domicílio, pelos domicílios; densidade, pela área.

**Krigagem só passa em quatro portas**: amostra mínima de 12 setores na
vizinhança, estrutura espacial no variograma (efeito pepita abaixo de 80% da
variância), ajuste do modelo (R² mínimo de 0,30) e **ganho sobre a média dos
vizinhos na validação cruzada**. Falhando qualquer uma, devolve o motivo e o
cálculo volta para o rateio por área.

**Totais nunca são krigados.** Não se interpola uma soma. Quando a densidade
passa nas portas, o script oferece a população por densidade krigada × área
como **estimativa alternativa**, nunca como valor padrão.

## Bloco: Detalhes da região analisada

| Indicador | Script | Fórmula | Fonte |
|---|---|---|---|
| **População na área** | `raio_setores.py` | soma de `Residentes` dos setores que intersectam o raio | `densidade_demografica_do_setor_habkm` |
| **Domicílios** | `raio_setores.py` | soma de `Domicilios` | idem |
| **Moradores por domicílio** | `raio_setores.py` | média de `Mediademor/dom` | `classe_economica_dos_domicilios` |
| **Potencial de consumo** | `raio_setores.py` | soma de `PotencialdeconsumoDrogarias-SetorCensitario` | `potencial_de_consumo_setor_censitario` |
| **Setores encontrados** | `raio_setores.py` | contagem | geometria do asset |

## Bloco: Contexto macroeconômico

| Indicador | Script | Fórmula | Unidade |
|---|---|---|---|
| **Densidade demográfica** | `raio_setores.py` | **média** de `densidadedemografica` dos setores — não é população ÷ área do círculo | hab/km² |
| **Renda média por habitante** | `raio_setores.py` | média de `Rendimentomediohab` | R$ |
| **Renda média domiciliar** | `raio_setores.py` | média de `RendimentoMedioDomicilio` | R$ |
| **Verticalização** | `raio_setores.py` | média de `Verticalizacao%` | **fração 0–1** |
| **Área de venda estimada** | `montar_relatorio.py` | potencial ÷ R$/m² **informado** | m² |
| **Valor do aluguel / área do imóvel** | — | campo do analista | — |

> **Fração × percentual.** As colunas terminadas em `%` das bases setoriais
> guardam **fração de 0 a 1** — verificado: `Verticalizacao%` e `Agua%` vão de
> 0,0 a 1,0, sem nenhum valor acima de 1. Verticalização 0,56 é **56%**, não
> 0,56%. Nunca adivinhar a unidade pelo tamanho do número.

> **Área de venda.** Não existe benchmark de faturamento por m² nem no acervo
> interno (busca no Confluence, 2026-10-27) nem em fonte pública localizada
> (ABRAFARMA publica faturamento e nº de lojas, não área). Sem régua informada
> pelo analista, o campo fica vazio — como o relatório do produto faz com
> "Área de venda do imóvel". Inventar o número seria pior que deixar em branco.

## Bloco: Microterritório e concorrência

Definições copiadas de `api-agent-orbita/src/services/radiusSearch/`:

| Indicador | Campo do produto | Fórmula |
|---|---|---|
| **Vendas totais no raio** | `microterritory.radiusTotalSales` | soma de `fatMedio` dos concorrentes no raio, só os com valor > 0 |
| **Média de faturamento por loja** | `microterritory.avgSalesPerStore` | vendas no raio ÷ nº de lojas **com faturamento válido** |
| **Vendas totais na região** | — | soma de `fatMedio` de todos os concorrentes **do município do ponto**. **Diverge do produto de propósito**: ele agrega as cidades tocadas pelo raio, o que perto de divisa vira o mercado da metrópole vizinha — em São Gonçalo do Amarante/RN o raio de 5 km alcançava seis municípios e o número inflava 13 vezes, de R$ 7,0 para R$ 91,3 milhões |
| **Venda mensal por faixa** | `monthlySalesTiers` | as 8 faixas fixas de `competitorRevenueTiers.ts` |

**Cidade de referência do cadastro.** A checagem de "cidade divergente" compara
a cidade cadastrada com o **município do ponto**, não com a mais frequente do
raio. Num raio que cruza divisa, cidade diferente é o esperado e não é defeito;
o bloco separa isso dos registros **implausíveis**, cadastrados em cidade que o
raio não alcança — esses sim são erro provável.

> **`fatMedio` é faturamento médio MENSAL estimado por PDV.** O dump não declara
> a periodicidade; o código do produto declara
> (`classifyByFatMedio`: *"Average monthly revenue (`fatMedio`)"*). É
> **estimado**, não medido, e está preenchido em menos da metade dos PDVs.

**As 8 faixas** (constantes de negócio, não variam com a localidade):

| # | Mínima | Máxima |
|---|---|---|
| 1 | R$ 1.336.854,12 | aberta |
| 2 | R$ 846.655,41 | R$ 1.336.854,11 |
| 3 | R$ 549.075,62 | R$ 846.655,40 |
| 4 | R$ 388.442,64 | R$ 549.075,61 |
| 5 | R$ 271.181,25 | R$ 388.442,63 |
| 6 | R$ 162.244,26 | R$ 271.181,24 |
| 7 | R$ 89.997,74 | R$ 162.244,25 |
| 8 | aberta | R$ 89.997,74 |

## Bloco: Quanto vende uma loja desta região

| Indicador | Fórmula | Fonte |
|---|---|---|
| **Menor venda observada** | mínimo de `fatMedio` entre as lojas do município com valor > 0 | camada Concorrentes 2025 |
| **Venda mediana** | mediana da mesma amostra | idem |
| **Maior venda observada** | máximo da mesma amostra | idem |

### Segunda fonte: receita medida das lojas do grupo

A planilha da IQVIA por brick traz **`codigo_cnpj` nas linhas do grupo**, e o
cadastro de lojas traz o mesmo CNPJ com bandeira, modelo, status e coordenada.
Cruzando os dois sai a **receita medida por loja nossa** — não estimada — e com
ela o recorte que o analista realmente quer: *quanto fatura uma loja desta
bandeira numa praça assim*.

| Indicador | Como |
|---|---|
| **Receita medida por loja** | soma de `preco_consumidor` do CNPJ no MAT atual |
| **Equivalente mensal** | receita MAT ÷ 12 |
| **Recortes** | município, raio, UF, bandeira, modelo e rede inteira |

Cobertura: **1.312 dos 1.790 CNPJs da IQVIA casam com o cadastro (73%)**, dos
quais 1.294 ativos e 800 com coordenada — o suficiente para medir por raio.

> **MAT é acumulado de 12 meses.** Dividir por 12 só vale para loja que operou o
> período inteiro; loja aberta no meio aparece baixa sem ser pequena. Por isso há
> um piso de receita anual que descarta esses casos, e a leitura usa quartis.

> **Carteira atual**: loja que saiu do grupo foi apagada para trás, então a
> amostra descreve quem está na rede hoje.

### Terceira fonte: a régua de canal — a que cobre o raio inteiro

As duas primeiras deixam um buraco: o campo estimado falta em mais da metade dos
cadastros, e a receita medida do grupo descreve a nossa loja, não o concorrente.
Num raio de 300 m é comum sobrar **um** valor estimado, ou nenhum — e um valor
só não descreve a vizinhança competitiva.

A régua de canal fecha esse buraco. As abas de canal da planilha da IQVIA trazem
receita e quantidade de PDVs por **canal e UF**, e `MDM-ClassifdoPDV` classifica
cada concorrente num rótulo que mapeia para esses canais:

| Indicador | Como |
|---|---|
| **Faturamento de referência por loja** | receita MAT do canal na UF ÷ PDVs do canal na UF ÷ 12 |
| **Mercado do raio** | soma da referência de cada concorrente do raio, por canal |
| **Faixa das lojas sem canal** | rede local não reconhecida entra entre o canal mais barato e o mais caro da UF, com a contagem declarada |
| **Confiança do mapeamento** | alta (o rótulo é a categoria), média (rede corporativa nomeada, atribuída por porte) ou nenhuma |

Ordem de grandeza no Rio Grande do Norte, para calibrar a leitura — ABRAFARMA
R$ 1,03 milhão por loja/mês, outras redes corporativas R$ 417 mil, Grupo
Farmarcas R$ 294 mil, FEBRAFAR R$ 129 mil, associações e franquias R$ 102 mil,
independentes R$ 44,5 mil. **Vinte e três vezes** entre o topo e a base: o canal
do concorrente importa mais para o mercado do raio que a contagem de lojas.

> **É a média do canal na UF, não o faturamento daquela loja.** A base não traz
> dispersão dentro do canal — sem mínimo, sem máximo, sem quartil. Duas
> independentes no mesmo quarteirão podem diferir várias vezes, e isso não
> aparece aqui. Serve para dimensionar mercado e situar um concorrente; não
> serve para afirmar quanto a farmácia da esquina vende, e o texto diz isso onde
> o número aparece.

> **Duas janelas diferentes.** A receita é MAT (12 meses) e a contagem de PDVs é
> YTD (ano corrente). Canal que abriu ou fechou muita loja no período sai
> enviesado — efeito de segunda ordem para canal estável, declarado junto do
> número.

> **A atribuição das redes nomeadas é julgamento, não campo da base.** Os quatro
> rótulos genéricos cobrem 85% dos registros e mapeiam sozinhos; as redes
> nomeadas são atribuídas por porte numa lista declarada em
> `scripts/faturamento_canal.py`. Mover uma rede de ABRAFARMA para outras redes
> corporativas muda a referência dela em mais de duas vezes — por isso a lista é
> explícita e revisável pelo time de Expansão.

**As três fontes não medem a mesma coisa** e vão lado a lado no relatório: a
estimada descreve **aquela loja**, a régua de canal descreve o **mercado do
raio**, e a medida do grupo descreve a **nossa operação**. Divergência entre
elas é achado, não erro a resolver escolhendo uma — e quando convergem, vale
dizer: em São Gonçalo do Amarante/RN a única vizinha com campo preenchido
registrava R$ 90,0 mil e a régua do canal dela apontava R$ 102,4 mil, 14% de
diferença entre duas vias independentes.

São o **piso, o meio e o teto do que as lojas vizinhas já faturam** — não
projeção para a loja nova. Em varejo farmacêutico a distribuição tem cauda
longa, então a média descreve mal os dois extremos: a mediana diz o que uma
loja típica fatura, e a distância entre mínimo e máximo diz o quanto o
resultado depende de execução e ponto, não da região. O bloco traz também os
quartis e a mesma estatística para o raio.

**A fonte vai na nota de cada um dos três cards**, porque card se lê isolado.

## Bloco: Aluguel comercial e custo de ocupação

| Indicador | Como |
|---|---|
| **Aluguel comercial** | informado pelo analista, em R$/m², com a referência que ele usou |
| **Área de venda estimada** | potencial ÷ R$/m² de faturamento informado |
| **Custo de ocupação estimado** | área estimada × aluguel por m², mensal |

> **Não existe fonte pública de aluguel comercial por m² por município.** O
> índice de mercado mais usado cobre **dez capitais**, é publicado em PDF mensal
> e não tem interface de consulta — para a maioria das praças da rede não há
> número a buscar. Média de portal de anúncio não é fonte verificável e não
> entra. Sem o valor informado, os três campos ficam vazios **com o motivo**.

## Bloco: Potencial de consumo da região

| Indicador | Fórmula |
|---|---|
| **Total** | soma de `PotencialdeconsumoDrogarias-SetorCensitario` nos setores do raio |
| **Medicamentos** | total × `Medicamentos(%)` médio, normalizado contra Higiene |
| **Higiene, Beleza & Nutrição** | total × `Higieneecuidadospessoais(%)` médio, normalizado |

O produto expõe os dois percentuais como `avgConsumptionMedications` e
`avgConsumptionHygiene`. A normalização existe porque as duas médias não somam
exatamente 1 entre setores.

## Bloco: Preço médio no brick — `mercado_brick.py`

**Única fonte do acervo com unidades vendidas.** Vem da planilha
`Faturamento IQVIA ... Detalhado por CNPJ, BRICK e UTC`, aba
`DADOS POR BRICK E UTC`, convertida por `preparar_iqvia_brick.py`.

    preço médio por unidade = preco_consumidor ÷ unidade

`preco_consumidor` é **receita** a preço de consumidor, não preço unitário — o
nome engana. O recorte sai por **brick** e por **UF**, e separado entre
`GRUPO FARMARCAS` e `CONCORRENTES`, o que mostra o posicionamento de preço da
rede contra o mercado.

> **Como o brick é localizado.** `bricks_iqvia` veio sem polígono, então não há
> como dizer em qual brick o ponto cai. O nome do brick traz UF e, nas cidades
> grandes, o bairro (`994-SE_AJU_CENTRO`), com o município **abreviado**
> (Aracaju = AJU, Belo Horizonte = BH). O casamento é por **UF + bairro do
> ponto**, e a saída sempre diz qual critério casou.

## Bloco: Geradores de fluxo — `pois_no_raio.py`

Hospitais, creches e escolas, mercados, bancos, transporte, moradia coletiva e
individual, comércio e serviços, lazer e culto. Fonte: **OpenStreetMap** via
Overpass API pública.

Existe porque as camadas do dump que responderiam isso (`bancos`,
`clinicas_oftalmologicas`, `farmacias`, `barreiras_geograficas`) vieram sem
coordenada ou sem polígono.

Cada categoria vem com **o motivo de trazer gente para a calçada** — consulta
que gera receita na saída, entrada e saída de escola em horário fixo, fila de
banco que prende a pessoa no quarteirão, ponto de ônibus que despeja passante
que não mora nem trabalha ali. É rótulo descritivo do tipo de equipamento, não
afirmação sobre o ponto: nenhum número sai daí.

Equipamento **sem nome** no OSM entra na contagem e fica **fora** da coluna de
exemplos — "(sem nome)" repetido polui a leitura sem informar nada.

> Contagem de equipamentos é **proxy fraco** de fluxo: diz que há geradores,
> não quanta gente passa. **Não substitui** o dado de passantes, que continua
> sendo lacuna obrigatória. Cobertura do OSM é colaborativa e irregular —
> ausência no mapa não é ausência no mundo.

## Bloco: Onde mais olhar — `alternativas.py`

Praças da mesma UF ordenadas por **mercado não atendido** (receita da UTC menos
a receita Farmarcas), com share, crescimento, lojas ativas e o veredito de
zoneamento resolvido pelo Censo.

**Cada linha é uma UTC, e diz qual localidade é.** Município grande tem várias
— Natal tem onze, Mossoró duas —, então a mesma cidade aparece mais de uma vez.
O que não pode é aparecer **genérica**: o nome da UTC traz a localidade
(`RN-NATAL-CIDADE NOVA`), e a tabela mostra "Natal/RN — Cidade Nova". Sem isso,
três linhas de Natal com números diferentes parecem três oportunidades
distintas na mesma praça.

**Potencial e captura são do município**, e repetem nas linhas da mesma cidade.
Não existe potencial por UTC nas bases; dividir a receita de uma UTC pelo
potencial do município inteiro produziria razão sem sentido — era o que fazia
Natal parecer capturar 19%, 12%, 8% e 5% em bairros diferentes. A captura usa a
**receita somada de todas as UTCs da cidade** sobre o potencial municipal.

Colunas da tabela:

| Coluna | Fórmula | Fonte |
|---|---|---|
| **Praça** | município, UF e **localidade da UTC** | `closeup_utc_varejo` |
| **Mercado não atendido** | receita da UTC − receita Farmarcas, com a **escala por extenso** (milhares/milhões/bilhões) ao lado do valor exato | `mat_anterior_x_atual_utc_crescimento` |
| **Potencial** | potencial de consumo em drogarias do município, **anual** | `potencial_de_consumo`, coluna que declara ANO |
| **Captura** | receita somada das UTCs do **município** ÷ potencial anual do município | derivado |
| **Preço médio** | receita a preço de consumidor ÷ unidades, nos bricks do município | `iqvia_brick.csv` |
| **Por que olhar** | frase montada **a partir dos próprios números** da linha — recomposição, não juízo | `alternativas.py` |

Como ler captura: **baixa com mercado grande é demanda represada; alta é praça
madura**, onde entrar significa tirar de alguém. O preço médio diz se a praça é
de ticket alto ou de volume — e bandeira popular conversa melhor com preço baixo.

O município pode ficar **sem preço** quando o nome vem abreviado no brick
(Aracaju = AJU): nesse caso a coluna sai vazia, nunca forçada.

É **lista de onde vale rodar um dossiê**, não recomendação de abertura. Mercado
grande sem a rede dentro pode ser praça aberta **ou** praça já testada e
perdida — `crescimento_farmarcas` negativo é o segundo caso.

## O que o relatório deliberadamente NÃO traz

| Campo do relatório do produto | Por quê |
|---|---|
| **Status (Recomendado / Não recomendado)** | o dossiê não pontua; a régua tem dono e vive no produto |
| **Score de viabilidade (%)** | idem |
| **População flutuante** | não existe em fonte alguma: nem nas 57 bases, nem no código, nem em API pública localizada. Entra como lacuna, sempre |
