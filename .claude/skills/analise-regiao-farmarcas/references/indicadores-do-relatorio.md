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

> **`fatMedio` é um RÓTULO DE FAIXA mensal, não o faturamento daquele PDV.**
> A periodicidade é mensal: o dump não a declara, o código do produto sim
> (`classifyByFatMedio`: *"Average monthly revenue (`fatMedio`)"*). Mas o campo
> **assume apenas os 8 valores da tabela abaixo em toda a base** — verificado em
> 2026-11-06: 100.612 registros, 8 valores distintos. Sete deles são o ponto
> médio da faixa e o mais baixo é o teto da faixa aberta embaixo, de modo que o
> número diz **em que faixa a loja caiu**, e não quanto ela vende. Está
> preenchido em menos da metade dos PDVs.
>
> Consequência para o texto do dossiê: mínimo, mediana e máximo desse campo são
> a **faixa mais baixa ocupada**, a **faixa mediana ocupada** e a **faixa mais
> alta ocupada** — nunca "o faturamento da loja X" nem "a mediana do faturamento
> dos vizinhos". A distância entre dois desses valores é distância entre faixas.
> Somá-los dá a soma dos rótulos, que é ordem de grandeza do porte das lojas do
> recorte, não a venda do recorte.

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
| **Faixa mais baixa ocupada** | mínimo de `fatMedio` entre as lojas do município com valor > 0 — é o rótulo da faixa, não a venda da loja | camada Concorrentes 2025 |
| **Faixa mediana ocupada** | mediana da mesma amostra | idem |
| **Faixa mais alta ocupada** | máximo da mesma amostra | idem |

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
> entra. Sem o valor informado, **o card não aparece** — card de destaque existe
> para carregar número, e três deles em sequência dizendo "—" gastam a faixa de
> maior atenção do relatório para informar que não há informação. O que
> destravaria continua escrito aqui e no formato do config: informe
> `receita_por_m2` e `aluguel_m2`, e os três cards voltam inteiros.

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
> ponto**, e a saída do script sempre diz qual critério casou.
>
> **O critério não vai para a nota do card, e o código do brick nunca vai.** A
> nota do card leva a comparação com a UF e a fonte do dado; o identificador do
> brick é nome de registro de base, não informa analista nem executivo e ainda
> anuncia "saída de robô" bem onde o problema a resolver é confiança no número.
> O que o leitor precisa saber — que **não se sabe em qual brick o ponto cai** —
> é lacuna obrigatória, escrita em linguagem de negócio, e é lá que ela fica. Por
> qual chave as duas tabelas casaram é detalhe de implementação, e vive na saída
> do script.

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

**Quando o raio volta quase vazio, a tabela ganha uma coluna — nunca uma segunda
tabela.** Com menos de cinco equipamentos etiquetados no raio pedido, o script
consulta também um círculo de 1.500 m e o relatório acrescenta a coluna "Em
1.500 m". O círculo largo é concêntrico e **contém** o pedido: as duas colunas
são aninhadas, não paralelas, e por isso não se somam. "Mais próximo" e
"Exemplos nomeados" saem sempre do maior círculo disponível, que é onde a
resposta é completa.

Duas tabelas foi como isso nasceu, e estava errado: as mesmas nove categorias
apareciam duas vezes, a primeira quase toda zerada, e o único equipamento do
raio curto reaparecia na segunda tabela, onde se lia como se fosse outro. A
tabela única também mostra a categoria **zerada nos dois círculos** — a de
cima a omitia, e "não há transporte nem a 1.500 m" é informação que o leitor
precisa ter.

O corte de cinco equipamentos e o raio de 1.500 m são **premissa da análise,
não medida**, e o relatório diz isso onde a coluna aparece.

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
| **Status (Recomendado / Não recomendado)** | o dossiê não pontua; a régua tem dono e vive no produto. O **parecer por número** (Bom / Na média / Ruim / Ambíguo / Sem referência) não é status: fala de um número contra o referente dele e nunca se soma — ver `benchmarks.md` |
| **Score de viabilidade (%)** | idem |
| **População flutuante** | não existe em fonte alguma: nem nas 57 bases, nem no código, nem em API pública localizada. Entra como lacuna, sempre |


## Implantação do ponto — esquina ou meio de quadra

Sai de `implantacao.py`, sobre a geometria viária do OpenStreetMap. Responde
onde o endereço está na quadra, que separa dois pontos da mesma rua mais do que
quase qualquer indicador de área: esquina tem duas faces de exposição e recebe
quem circula por duas vias; meio de quadra tem uma.

**Três portas, todas obrigatórias para afirmar:**

| Porta | O corte | Por que existe |
|---|---|---|
| Ancoragem | ponto a ≤ 20 m de via mapeada | mais longe, ou a coordenada está errada ou a via não está no mapa — e nos dois casos a classificação descreve outra coisa |
| Separação | esquina ≤ 20 m · meio de quadra ≥ 40 m | entre os dois há **zona morta deliberada**: ponto a 30 m de um cruzamento é "perto da esquina" na fala e não tem classificação defensável no dado |
| Nomeação | cruzamento só conta com duas vias **nomeadas e diferentes** | nó compartilhado por dois trechos da mesma rua é continuidade de via, não esquina |

Fora disso, `classificacao: null` e **o assunto não entra no relatório**, em
forma nenhuma. A cobertura viária do OSM é boa em cidade e irregular em
distrito pequeno, então a abstenção é o caso comum, não a falha.

## Cidades que têm este município como polo

A camada REGIC guarda, em cada município, apenas a **contagem** de municípios
influenciados — e, do outro lado, o polo a que cada um se vincula. A lista
nominal sai **invertendo** essa relação: influenciado é quem aponta para cá.
`contexto_municipio.py` faz a inversão e junta a população de cada um.

Por que nomear importa: "atende 3 cidades do entorno" não diz nada sobre
tamanho de mercado. Três cidades de 2 mil habitantes e três de 40 mil são
praças diferentes, e a diferença é exatamente o público que **não mora no
raio** e que nenhum indicador de área do relatório captura.

A contagem declarada pela base entra como conferência. Quando as duas
divergem, **as duas saem** e a divergência é o achado — não se escolhe uma em
silêncio.

## Cada indicador do município contra o país — parecer por número

Bloco do dossiê de ponto, dentro do contexto macroeconômico (desde 2026-11-27).
Os percentis municipais que `contexto_municipio.py` já apurava — renda
domiciliar per capita, IPC, PIB per capita, IFDM — e a razão de habitantes por
farmácia saem numa tabela com valor, mediana nacional, posição (percentil e
número de municípios comparados) e o **parecer** de cada um, por
`scripts/_parecer.py`. IPC e PIB per capita saem **Ambíguo**: o primeiro é
total, proxy de porte, e porte não prevê faturamento (correlação medida
−0,003); o segundo mede a planta em cidade industrial. Nenhum total, nenhuma
contagem de pareceres, e nenhum juízo sobre o município: o parecer é do
indicador, nunca do lugar.

---

# Perfil por cidade — lista de praças

Bloco do relatório "Onde olhar" (formato prospecção). A unidade é o **município**,
e não a unidade territorial: nenhuma destas camadas existe por UTC. Cada
indicador sai com valor, percentil na distribuição nacional da própria camada,
mediana nacional e número de municípios comparados.

**Regra de corte:** só per capita, percentual ou razão. Total absoluto é proxy
de porte e ordenaria as quatro dimensões por tamanho de cidade. Teto de três
indicadores por dimensão.

**Parecer por indicador** (desde 2026-11-27, decisão do PM que reverte a matiz
única de 2026-11-25): cada indicador sai com o chip de parecer ao lado do
percentil, calculado por `scripts/_parecer.py` pela direção do indicador e pelo
tercil da distribuição. Direções de hoje: renda, consumo em drogarias por
habitante, habitantes por farmácia, crescimento demográfico, crescimento do
mercado municipal, municípios influenciados, população urbana e densidade —
mais é melhor; classes A/B1/B2, captura do potencial e credenciamento ao
Farmácia Popular — **Ambíguo**; papel na rede urbana — **Sem referência**. A
tira de percentil continua com uma matiz (ela é posição, não juízo), a ordem
continua alfabética, e não há linha de total.

| Dimensão | Indicador | Base | Campo | Unidade |
|---|---|---|---|---|
| Poder de compra | renda domiciliar per capita | camada Renda Média por município | `Renda_media_domic_per_capita` | R$ |
| Poder de compra | consumo em drogarias por habitante | base municipal de Potencial de Consumo | `3ConsumoMedioDrogarias(p/habitante)R$` | R$/ano |
| Poder de compra | domicílios nas classes A, B1 e B2 | base do Farmácia Popular | `A(%)` + `B1(%)` + `B2(%)` | % |
| Folga competitiva | habitantes por farmácia | camada População × base do Farmácia Popular | derivado | hab |
| Folga competitiva | captura do potencial pelo varejo medido | base de crescimento por UTC × Potencial de Consumo | derivado | % |
| Folga competitiva | farmácias credenciadas ao Farmácia Popular | base do Farmácia Popular | `%farmaciascredenciadasaoFarmaciaPopnacidade` | % |
| Dinamismo | crescimento demográfico | camada Densidade Demográfica | `TaxadeCrescimentoDemografico(%aa)` | % a.a. |
| Dinamismo | crescimento do mercado farmacêutico do município | base de crescimento por UTC | derivado | % |
| Centralidade | municípios que este influencia | REGIC 2018 | `municipiosInfluenciados` | cidades |
| Centralidade | população urbana | camada Situação do Território | `03-PopulacaoUrbana%` | % |
| Centralidade | densidade demográfica | camada Densidade Demográfica | `DensidadeDemografica` | hab/km² |
| Centralidade | papel na rede urbana | REGIC 2018 | `classificacaoRegic` | rótulo, **sem percentil** |

## As duas fórmulas derivadas

**Habitantes por farmácia** = população municipal do dump ÷ total de farmácias
da cidade na base do Farmácia Popular. Percentil **alto = menos saturado**. A
população do dump é usada no numerador para manter a distribuição internamente
coerente; o viés de ~4% contra o Censo 2022 atinge o valor, não a posição.

**Captura do potencial** = soma da receita atual de todas as UTCs do município
÷ potencial de consumo anual do município × 100. A soma é de **receita**, nunca
média das taxas das UTCs — média de razão não é a razão do agregado, e uma UTC
minúscula em disparada faria a cidade inteira parecer crescer.

**Crescimento do mercado do município** = (soma da receita atual ÷ soma da
receita anterior − 1) × 100, pelas UTCs do município. É **municipal**, enquanto
a coluna de crescimento da tabela de praças é **por UTC**: dois números
parecidos na mesma tela, medindo recortes diferentes, e cada rótulo nomeia o
seu.

## Três coisas que ficaram de fora, e por quê

- **PIB per capita**: passa na regra de corte, mas em cidade industrial ou de
  mineração mede o valor agregado da planta, não a carteira de quem entra na
  loja.
- **Variação de empregos** (`movimentacao_economica`): a base não declara o
  período em lugar nenhum. Percentual de variação sem janela é número que
  parece medida. Entra quando o período for estabelecido.
- **`classificacaoRegic` e `hierarquia` como número**: são categóricos. A régua
  dessa escala pertence ao IBGE, e convertê-la em percentil aqui seria inventar
  uma.
