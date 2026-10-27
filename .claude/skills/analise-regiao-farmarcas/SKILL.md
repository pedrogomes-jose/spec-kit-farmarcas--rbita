---
name: analise-regiao-farmarcas
description: Monta o dossiê de uma região para análise de ponto de farmácia da Farmarcas e entrega um relatório HTML no layout do relatório de viabilidade do Órbita — população na área, renda média, densidade, potencial de consumo com split entre Medicamentos e Higiene/Beleza/Nutrição, preço médio no brick, microterritório e concorrência, geradores de fluxo no entorno e praças alternativas — aplicando antes o gate de zoneamento (regras oficiais de expansão), e sem pontuar o ponto. Pergunta sempre se o solicitante é empresário novo ou já associado, porque isso muda a leitura de canibalização. Use quando o usuário disser 'analisa essa região', 'faz o dossiê desse ponto', 'o que tem nessa área', 'quais os pontos positivos e negativos desse endereço', 'tem concorrente perto daqui', 'vale olhar essa cidade', 'me dá o raio-X dessa região', ou fornecer um endereço/coordenada pedindo contexto para abrir loja. Do NOT use para calcular ou reproduzir o score de viabilidade 0–20 do produto → o dossiê não pontua, por decisão de produto; do NOT use para escrever cards do board SQO → use /orbita-user-stories; do NOT use para discovery de produto → use /product-discovery; do NOT use para escolher fornecedor de dado de mercado → use o subagente estrategista-fontes-dados.
---

# Dossiê de região — Farmarcas

Entrega o que a região **é**, para que o analista de Expansão gaste o tempo dele
decidindo, não coletando. Substitui a coleta manual de camadas descrita em
`docs/confluence/2025/orbita-descoberta-analise-pontos.md:161`.

Referências (ler quando indicado):
- `references/zoneamento-e-perfil.md` — regras oficiais de zoneamento e o que o perfil do solicitante muda. **Steps 1 e 2.**
- `references/indicadores-do-relatorio.md` — fonte, fórmula e unidade de cada indicador do relatório. **Steps 3 e 6.**
- `references/bases-orbita.md` — o que existe mesmo no dump e o que não existe. **Step 0/3.**
- `references/lentes-do-dossie.md` — as 4 lentes, a anatomia do item, o tier. **Step 4.**
- `references/benchmarks.md` — contra o que comparar. **Step 4.**
- `references/limites-e-vieses.md` — o que o dado não diz. **Step 5, obrigatório.**
- `references/modelo-de-dossie.md` — estrutura do entregável. **Step 6.**
- `references/benchmarks.md` — e o que NUNCA serve de referência.

## Critical

- **Perguntar SEMPRE se o solicitante é empresário novo ou já associado**, e
  qual bandeira e modelo (popular/convencional) ele pretende. Sem isso o dossiê
  não sabe se a loja Farmarcas vizinha é problema ou estratégia, e não consegue
  aplicar o zoneamento. É a primeira pergunta, não um detalhe de preenchimento.
- **Zoneamento é gate, não indicador.** Roda ANTES da análise de mercado. Se o
  veredito for `impedimento`, o dossiê **para** e devolve o impedimento com a
  regra citada. Não existe dossiê de mercado bonito que destrave um ponto que a
  regra de expansão barra.
- **"Loja nossa" sai do cadastro de lojas (CNPJ + coordenada)**, nunca do nome
  de bandeira dentro da camada Concorrentes — esse dá falso positivo
  comprovado. Match por nome é suspeita a confirmar, e vai rotulada como tal.
- **Venda por loja tem TRÊS fontes, e elas não medem a mesma coisa.**
  1. **Faturamento da camada de concorrentes** — *estimado*, presente em menos
     da metade dos cadastros, descreve aquela loja específica. Num raio curto
     costuma sobrar um valor só, ou nenhum.
  2. **Régua de canal** — *medida*: receita e quantidade de PDVs por canal
     (ABRAFARMA, FEBRAFAR, associações e franquias, independentes, outras redes
     corporativas) **e por UF**, da base do instituto. A camada de concorrentes
     já classifica cada loja num rótulo que mapeia para esses canais, então toda
     loja do raio ganha um faturamento de referência, mesmo as que têm o campo
     estimado vazio. É o que **dimensiona o mercado do raio**.
  3. **Receita das lojas do grupo** — *medida*, casa por CNPJ com o cadastro e
     permite filtrar pela bandeira pretendida. É o que a **nossa** operação
     fatura numa praça assim.

  As três entram no relatório, rotuladas, e a divergência entre elas é achado,
  não erro a resolver escolhendo uma.
- **A régua de canal diz quanto uma loja MÉDIA do canal fatura naquele estado**
  — nunca quanto a farmácia da esquina vende. A base não traz dispersão dentro
  do canal: não há mínimo, máximo nem quartil por loja. Serve para dimensionar
  mercado e para situar um concorrente; não serve para afirmar o faturamento de
  um endereço, e o texto precisa dizer isso onde o número aparece.
- **A régua de canal mistura duas janelas.** A receita é acumulado de 12 meses
  e a contagem de PDVs é do ano corrente. Canal que abriu ou fechou muita loja
  no período sai enviesado. O viés é de segunda ordem para canal estável, e vai
  declarado junto do número.
- **Loja sem canal reconhecido vira faixa, não zero nem média.** Rede local que
  o mapeamento não conhece entra como intervalo entre o canal mais barato e o
  mais caro da UF, com a contagem declarada. Preencher com a média do raio
  inventa precisão que a base não tem.
- **MAT é acumulado de 12 meses, não de um mês.** Dividir por 12 só vale para
  loja que operou o período inteiro; loja aberta no meio aparece baixa sem ser
  pequena. Por isso o corte descarta receita anual implausível e a leitura usa
  quartis, não média.
- **Card cita a fonte na própria nota; texto não.** A consolidação no fim vale
  para a **prosa**, que se lê em ordem. O card se lê isolado, fora de ordem e
  muitas vezes é o único pedaço que alguém olha — então, quando a origem do
  número não é óbvia pelo rótulo, ela vai na nota do card. Vale para venda por
  loja, aluguel, preço por unidade e qualquer indicador vindo de base externa.
- **Fonte vai consolidada no fim, nunca no meio do texto.** Cada item da
  narrativa declara a sua no campo `fonte`; o relatório numera a referência no
  fim da frase e resolve todas na seção **Fontes**. Nenhum parágrafo, nota de
  card ou tabela cita fonte no corpo.
- **O corpo do relatório não fala de ferramenta.** Nada de nome de script,
  flag de linha de comando, nome de arquivo de base ou nome de bloco de JSON no
  texto que o analista lê. A rastreabilidade não cai, muda de endereço: o corpo
  cita a **fonte de dado** ("camada Concorrentes 2025", "Censo 2022 do IBGE",
  "base de faturamento por brick da IQVIA"), e a ferramenta fica no rodapé e nos
  arquivos de origem. `montar_relatorio.py` traduz o que escapar, mas a
  narrativa já deve nascer assim.
- **Em "Onde mais olhar", cada linha é uma UTC e diz QUAL localidade é.** A
  mesma cidade pode aparecer mais de uma vez — Natal tem onze UTCs —, mas nunca
  genérica: a linha nomeia o bairro ou distrito, "Natal/RN — Cidade Nova", para
  que se saiba qual praça está sendo indicada. Cidade repetida sem localidade
  nomeada vira a mesma oportunidade listada várias vezes com números diferentes.
- **Potencial e captura são do MUNICÍPIO, e repetem nas UTCs da mesma cidade.**
  Não existe potencial por UTC nas bases, então dividir a receita de uma UTC
  pelo potencial do município inteiro dá razão sem sentido — fazia Natal
  parecer capturar 19%, 12%, 8% e 5% em bairros diferentes. A captura é
  calculada sobre a receita somada de todas as UTCs da cidade, e a coluna diz
  que é municipal.
- **"Vendas totais na região" é sempre a venda total da CIDADE do ponto** —
  nunca o raio, nunca a macrorregião. O produto soma as cidades tocadas pelo
  raio; divergimos de propósito, porque perto de divisa isso vira o mercado da
  metrópole vizinha: em São Gonçalo do Amarante/RN o raio de 5 km alcançava seis
  municípios e inflava o número em 13 vezes. A divergência vai declarada.
- **A referência de cadastro é o município do ponto**, não a cidade mais comum
  do raio. Usar a modal erra feio em divisa: 36 lojas do próprio município
  foram marcadas como "cidade divergente" porque a modal do raio era a cidade
  vizinha. Cidade diferente perto de divisa é esperado; só é suspeita quando o
  raio não alcança a cidade cadastrada.
- **Setor censitário entra rateado pela fração dentro do raio**, nunca inteiro.
  Somar o setor inteiro produz número que contradiz a densidade da própria base
  (verificado: erro de +353% contra −0,4% do rateio). Taxa não se rateia: entra
  como média ponderada pelo que ela descreve.
- **Krigagem só com as quatro portas abertas** — amostra, estrutura espacial,
  ajuste e ganho na validação cruzada — e **nunca para totais**. Recusada,
  declara o motivo e volta para o rateio por área.
- **A unidade do campo nunca se adivinha.** As colunas `%` das bases setoriais
  guardam **fração de 0 a 1**: verticalização 0,56 é 56%. `fatMedio` é
  faturamento **mensal estimado** — está no código do produto, não no dump.
  Na dúvida, conferir em `references/indicadores-do-relatorio.md`, nunca inferir
  pelo tamanho do número.
- **Um dossiê nunca se apoia em outro.** Nada de "mais que o ponto analisado
  antes", "ao contrário daquela praça", "o dobro do que vimos em X". Cada
  dossiê é lido isolado, por quem pode nunca ter visto o outro — e comparar
  dois pontos específicos não é referência, é anedota: dois casos não formam
  distribuição. Referente válido é a **distribuição**: percentil nacional,
  mediana da base, histórico agregado de análises, ou o próprio município.
  Isso inclui o Centro de Franca/SP, que não serve de comparação em situação
  nenhuma — ele aparece nas referências apenas como caso de erro de dado.
- **População flutuante não existe** em fonte alguma — nem nas 57 bases, nem no
  código, nem em API pública. Entra como lacuna, nunca como estimativa.
- **Área de venda só com régua informada.** Sem um R$/m² que o analista forneça,
  o campo fica vazio, como no relatório do produto.
- **O dossiê NÃO pontua.** Nada de score, nota, percentual de viabilidade,
  "recomendado" ou "aprovado". A régua 0–20 tem dono (os executivos da
  Farmarcas) e vive no produto; duplicá-la cria dois números divergentes para a
  mesma pergunta e piora a desconfiança que originou o Órbita.
- **Nenhum número sai do modelo.** Todo valor do dossiê vem de um script em
  `scripts/` ou de API pública consultada nesta sessão. Se um número não tem
  script de origem, ele não entra — nem "aproximadamente", nem "cerca de".
- **Toda lacuna é declarada.** Base ausente, campo com erro de planilha,
  município fora de uma base: vira item da seção "O que este dossiê NÃO sabe",
  com o que destravaria. Lacuna silenciada vira conclusão errada.
- **"Fluxo de passantes" entra SEMPRE como lacuna**, em todo dossiê, mesmo em
  ponto residencial. Não existe no dump nem no produto, e é a variável que mais
  distorce ponto de rua comercial.
- **Rodar pelo menos dois raios.** O produto usa 300 m por padrão, mas o raio
  **mediano das 6.946 análises reais é 5.500 m**. Entregar só um raio responde
  outra pergunta que a do analista.
- **Nome de pessoa nunca entra** — nem empresário, nem consultor, nem analista,
  nem citado de parecer histórico. As bases têm esses campos; os scripts os
  descartam; o texto também descarta.
- **Vizinhança histórica é memória, não prognóstico.** Nunca escrever
  "reprovaram aqui, logo é ruim": o estudo em `analise-ponto-orbita` mediu que o
  parecer não prediz sobrevivência (p = 0,8275).
- **Divergência entre fontes é achado**, com os dois números — nunca escolher
  um em silêncio.
- **Carimbar a data do dump** no topo. O dado é estático e envelhece em silêncio.
- O dossiê é insumo para o comentário da análise no Órbita. **Não** vai para o
  empresário e **não** substitui o parecer do analista.

## Step 0: Read Before You Write

| Fonte | Caminho | O que extrair |
|---|---|---|
| Regras de zoneamento | `references/zoneamento-e-perfil.md` | o gate, as faixas, as distâncias e o que a regra não diz |
| Indicadores do relatório | `references/indicadores-do-relatorio.md` | fórmula, unidade e o que o relatório não traz |
| Inventário das bases | `references/bases-orbita.md` | o que dá e o que não dá para responder |
| Dump das bases | `C:\Users\zequi\Downloads\bases órbita` (ou `ORBITA_BASES`) | os dados |
| Como o score funciona hoje | `docs/confluence/ia/analises/estudo-peso-populacao-score-viabilidade.md` | para **não** duplicar a régua |
| Jornada real do analista | `docs/confluence/2025/orbita-descoberta-analise-pontos.md` | etapas 5–9 e as dores |
| Poder preditivo do parecer | `C:\Users\zequi\projetos\analise-ponto-orbita\README.md` | o que não se pode afirmar |
| Bases conflitantes | `docs/confluence/2025/evolucao-camadas/orbita-evolucao-camadas.md` | loja nossa listada como concorrente |

## Step 1 — Fixar o ponto

Obter **endereço ou coordenada** e o **município**. Se vier só o endereço, pedir
a coordenada ao usuário ou geocodificar por fonte pública e **registrar a
precisão obtida**. Sem coordenada não há raio — e sem raio o dossiê vira perfil
de cidade, o que deve ser dito em vez de disfarçado.

Perguntar, porque cada uma muda o resultado e nenhuma é adivinhável:

1. **O solicitante é empresário novo ou já tem loja Farmarcas?** Se já tem,
   qual o responsável pelo GE — para separar loja dele de loja de outro associado.
2. **Qual bandeira pretendida** — decide a distância mínima (300 m mesma
   bandeira, 500 m outra).
3. **Popular ou convencional** — a faixa de 60–120 mil exige que a 2ª loja da
   cidade seja popular.
4. **É ponto novo, mudança de ponto ou conversão?**

Se o usuário não souber alguma, registrar como premissa explícita e seguir —
menos as duas primeiras, que mudam o gate e devem ser perguntadas.

Pegar o **código IBGE** do município na saída de `contexto_municipio.py`.
Nunca digitar de memória: código errado traz a população de outra cidade e
muda a faixa de zoneamento inteira.

## Step 2 — Gate de zoneamento (antes de qualquer análise de mercado)

Ler `references/zoneamento-e-perfil.md` e rodar:

```
python scripts/zoneamento.py --lat <LAT> --lng <LNG>     --municipio "<NOME>" --uf <UF> --codigo-ibge <CODIGO>     --bandeira "<BANDEIRA>" --modelo <popular|convencional>     --perfil <novo|existente> [--ge "<responsável pelo GE>"]
```

Na primeira vez, preparar o cadastro de lojas (uma vez só, a partir da raiz do
projeto, sem `-I` porque precisa de `openpyxl`):

```
python .claude/skills/analise-regiao-farmarcas/scripts/preparar_cadastro_lojas.py
```

Conforme o `veredito`:
- **impedimento** → escrever o dossiê curto de impedimento (ver
  `references/modelo-de-dossie.md`) e **parar**. Não rodar os scripts de mercado.
- **alerta** → seguir, com o alerta em destaque antes das lentes.
- **liberado** → seguir.
- **indeterminado** → resolver a população do Censo antes de continuar.

## Step 3 — Rodar os scripts de dado

**Pedir autorização antes de rodar.** Todos leem arquivos locais e APIs
públicas; nenhum escreve fora de `scripts/cache/` e `outputs/`.

Preparos de uma vez só (da raiz do projeto, **sem** `-I`, porque usam openpyxl):

```
python .claude/skills/analise-regiao-farmarcas/scripts/preparar_cadastro_lojas.py
python .claude/skills/analise-regiao-farmarcas/scripts/preparar_iqvia_brick.py
python .claude/skills/analise-regiao-farmarcas/scripts/preparar_iqvia_canal.py
```

Depois, por análise:

```
python scripts/contexto_municipio.py  --municipio "<NOME>" --uf <UF>
python scripts/malha_setores.py       --codigo-ibge <CODIGO>          # 1ª vez do município
python scripts/raio_setores.py        --lat <LAT> --lng <LNG> --raio 300  --codigo-ibge <CODIGO>
#   --metodo area|inteiro|krigagem   (padrão: area)   --comparar  mostra os três
python scripts/raio_concorrencia.py   --lat <LAT> --lng <LNG> --raio 300  --municipio "<NOME>" --uf <UF>
python scripts/raio_concorrencia.py   --lat <LAT> --lng <LNG> --raio 5000 --municipio "<NOME>" --uf <UF>
#   --municipio é obrigatório na prática: define a cidade de referência e a "região"
python scripts/mercado_utc.py         --codigo-ibge <CODIGO>
python scripts/mercado_brick.py       --uf <UF> --codigo-ibge <CODIGO> --lat <LAT> --lng <LNG>
python scripts/pois_no_raio.py        --lat <LAT> --lng <LNG> --raio 500
python scripts/benchmark_historico.py --lat <LAT> --lng <LNG> --vizinhanca 5000
python scripts/alternativas.py        --uf <UF> --excluir-municipio <CODIGO>
python scripts/venda_por_loja.py      --uf <UF> --bandeira "<BANDEIRA>" --modelo <popular|convencional>
python scripts/faturamento_canal.py   --uf <UF> --lat <LAT> --lng <LNG> --raio 300
```

`malha_setores.py` baixa a geometria dos setores do município do asset público
do Órbita (~4,5 MB, cacheado) — é ela que destrava população, renda, densidade e
potencial de consumo no raio. Sem ela esses quatro indicadores não existem.

Cada script devolve JSON com um bloco `lacunas`. **Ler o bloco `lacunas` com a
mesma atenção dos dados** — ele é metade da entrega. `montar_relatorio.py`
roda tudo de novo por conta própria, mas o modelo precisa ter lido a saída para
escrever as lentes.

## Step 4 — Montar as lentes

Ler `references/lentes-do-dossie.md` e `references/benchmarks.md`.

Para cada item candidato, exigir os quatro campos: número, **fonte de dado**,
comparação e confiança com o motivo. **Não existe campo "muda a leitura se"** —
a ressalva e o limite do método entram explicados dentro do parágrafo, onde o
leitor precisa deles. Item sem comparação não entra. Item que não muda nenhuma
decisão não entra. Cortar pelo Tier até caber em ~15 itens.

## Step 5 — Limites

Ler `references/limites-e-vieses.md` e montar "O que este dossiê NÃO sabe".
Fluxo de passantes é obrigatório. Somar as lacunas devolvidas pelos scripts.

**Cada lacuna é explicada, não listada.** Três perguntas respondidas em cada
uma: *o que falta*, *por que isso importa neste ponto* e *o que destravaria*.
Uma linha solta como "a base X não tem o município" não é acionável — diga o
que deixa de ser possível saber por causa disso, e o que resolveria.

O mesmo vale para "Para confirmar em campo": cada item diz **o que checar e o
que muda conforme a resposta**.

## Step 6 — Escrever a narrativa e gerar o relatório

Ler `references/modelo-de-dossie.md` e `references/indicadores-do-relatorio.md`.

O entregável é **HTML**, montado por script. A divisão é a regra da casa:

    número -> script     (o modelo não formata nem recalcula)
    texto  -> modelo     (o modelo não inventa número)

1. Escrever a narrativa em JSON — resumo em uma linha, as quatro lentes com os
   cinco campos em cada item, `nao_sabe` e `campo`. O formato está no topo de
   `scripts/montar_relatorio.py`. Salvar em
   `outputs/dossies/<AAAA-MM-DD>_<municipio>_<referencia>.json`.
2. Gerar o relatório:

```
python scripts/montar_relatorio.py     --config outputs/dossies/<arquivo>.json     --saida  outputs/dossies/<arquivo>.html
```

3. Conferir o HTML: cada card tem número ou "—" com o motivo; nenhum campo
   inventado; o bloco de zoneamento aparece no topo no lugar do score.

Antes de apresentar, passar pelo subagente `(⌕) auditor-de-evidencia`. Se ele
reprovar algum item, corrigir **no JSON** e gerar o relatório de novo — nunca
editar o HTML à mão, que é saída de script.

Acionar `(◔◡◔) analista-expansao` quando houver dúvida se o dossiê fala a
língua de quem decide, e `(⚑_⚑) estrategista-fontes-dados` **só** quando uma
lente ficar vazia por falta de fonte.

## Racionalizações que não valem

| Tentação | Por que não |
|---|---|
| "Faço uma nota de 0 a 10 só para resumir" | é a régua de novo, com outro nome |
| "O usuário não disse o perfil, assumo empresário novo" | é a pergunta que muda a leitura de canibalização — pergunte |
| "O ponto é barrado, mas rodo o mercado para enriquecer" | dossiê completo de ponto barrado sugere que há o que negociar |
| "Casou com bandeira Farmarcas, então é loja nossa" | falso positivo comprovado; confirme no cadastro |
| "Uso a população do dump, que é a da tela" | perto de 60/120/200 mil ela troca a faixa de zoneamento |
| "A cidade estourou o teto, mas é tudo do mesmo dono, então libero" | a regra aplicada conta lojas; mostre as duas leituras e mantenha o impedimento |
| "O número deve girar em torno de X" | número sem script não entra |
| "A lacuna é técnica demais, resumo como dados limitados" | lacuna genérica não permite o analista agir |
| "Ponto residencial, pulo o aviso de fluxo" | o aviso é incondicional |
| "300 m basta, é o padrão do produto" | a prática real do time é 5.500 m de mediana |
| "Reprovaram aqui, então sinalizo risco" | o parecer não prediz desfecho |
| "Cito o parecer histórico com o nome que está lá" | LGPD; nome nunca entra |
| "As duas bases divergem, uso a mais confiável" | a divergência é o achado |
| "0,56 deve ser 0,56%" | as colunas `%` setoriais são fração: 0,56 é 56% |
| "Somo o setor inteiro, é o que o produto faz" | produz número que contradiz a densidade da própria base |
| "Multiplico a renda média pela fração do setor" | taxa não se rateia; entra como média ponderada |
| "Krigo a população, fica mais preciso" | não se interpola um total; krigue a densidade e integre |
| "Estimo a área de venda por comparação" | sem régua de R$/m² informada, não há estimativa honesta |
| "Comparo com o Centro de Franca, que já analisei" | proibido como referência, em qualquer situação |
| "Comparo com o ponto que analisei semana passada" | dois casos não são distribuição; use percentil ou mediana |
| "Só cito de leve o outro dossiê, sem nome" | eco também é referência cruzada; o leitor não tem o outro em mãos |
| "Edito o HTML para ajustar um número" | o HTML é saída de script; corrija a origem |
| "Cito o script na fonte, assim fica rastreável" | rastreável é a fonte de DADO; o script vai no rodapé |
| "Fecho o item com 'muda a leitura se'" | o rótulo foi removido; explique a ressalva na própria frase |
| "A lacuna é uma linha, o leitor deduz o resto" | lacuna sem o porquê e sem o destravamento não é acionável |
| "Cito a fonte na frase, fica mais rastreável" | espalhada em 16 parágrafos ninguém usa; consolidada, sim |
| "O card também manda a fonte para o fim" | card se lê isolado; a nota dele carrega a origem |
| "Pego aluguel médio de portal de anúncio" | não é fonte verificável; sem o valor informado, o campo fica vazio |
| "A média de faturamento basta para dizer quanto se vende" | a distribuição tem cauda longa; mostre mínimo, mediana e máximo |
| "Uso só o faturamento dos concorrentes" | é estimado e cobre metade; a receita medida do grupo existe e filtra por bandeira |
| "Receita MAT é do mês" | MAT é acumulado de 12 meses; dividir por 12 só vale para loja do período inteiro |
| "As duas fontes divergem, escolho a melhor" | a divergência é achado: uma mede concorrente, a outra mede a nossa bandeira |
| "Só uma loja do raio tem faturamento, então não dá para dimensionar o mercado" | a régua de canal cobre toda loja classificada, inclusive as de campo vazio |
| "A régua de canal diz que aquela loja fatura R$ X" | diz o que a loja MÉDIA do canal fatura na UF; a dispersão dentro do canal não está na base |
| "A loja não casou com nenhum canal, uso a média das outras" | vira faixa entre o canal mais barato e o mais caro, com a contagem declarada |
| "Somo o raio pela régua de canal e chamo de mercado do município" | o raio cruza divisa; mercado do município é o total medido da cidade |
| "Conto equipamentos no OSM e chamo de fluxo" | é proxy fraco; fluxo continua sendo lacuna |
| "Região é o que o raio alcança" | região é a CIDADE do ponto; o raio em divisa vira macrorregião |
| "Listo a cidade sem dizer qual UTC é" | sem a localidade, a mesma cidade repetida parece oportunidade duplicada |
| "Captura da UTC = receita dela ÷ potencial da cidade" | numerador e denominador em recortes diferentes; captura é municipal |

| "Cidade diferente da modal do raio é erro de cadastro" | perto de divisa é o esperado; erro é a cidade que o raio não alcança |

## Checklist de saída

- [ ] Perfil do solicitante declarado no cabeçalho
- [ ] Gate de zoneamento rodado, com a faixa e a população do Censo citadas
- [ ] Canibalização afirmada só com base no cadastro de lojas
- [ ] Canibalização própria separada da de outro associado
- [ ] Data do dump no topo
- [ ] Dois raios rodados e comparados
- [ ] Geometria dos setores baixada, e os 4 indicadores de cabeçalho preenchidos
- [ ] Rateio proporcional aplicado, com a cobertura do círculo declarada
- [ ] "Vendas totais na região" calculada sobre a cidade do ponto, não sobre o raio
- [ ] Registros de cadastro implausível separados dos de cidade vizinha
- [ ] Se usou krigagem, o diagnóstico e os campos recusados estão no dossiê
- [ ] Split de consumo entre Medicamentos e Higiene/Beleza/Nutrição presente
- [ ] Preço médio do brick com o critério de casamento declarado
- [ ] Geradores de fluxo no entorno, ou a lacuna do Overpass declarada
- [ ] Em "Onde mais olhar", cada linha nomeia a localidade da UTC — nenhuma cidade genérica repetida
- [ ] Potencial e captura rotulados como municipais
- [ ] Leitura da região em **texto corrido**, com abertura por lente — sem bullets
- [ ] Explicação presente antes da renda, do potencial de consumo e dos geradores de fluxo
- [ ] "Onde mais olhar" com escala por extenso, preço médio, captura e o porquê de cada praça
- [ ] Nenhuma citação de fonte na prosa — todas na seção Fontes, numeradas
- [ ] Cards de origem não óbvia citam a fonte na própria nota
- [ ] Faixa de venda por loja nas TRÊS fontes: estimada dos concorrentes, régua medida por canal e receita medida do grupo
- [ ] Mercado do raio dimensionado pela régua de canal, com a contagem de lojas sem canal declarada
- [ ] Dito, onde a régua de canal aparece, que ela é a média do canal na UF e não o faturamento daquela loja
- [ ] Receita medida filtrada pela bandeira pretendida, com o recorte nacional ao lado
- [ ] Seção Fontes com a tabela numerada e a procedência geral
- [ ] Nenhum nome de script, flag ou arquivo de base no corpo do relatório
- [ ] Relatório HTML gerado por `montar_relatorio.py`, não escrito à mão
- [ ] Nenhuma referência a outro dossiê, nem explícita nem por eco
- [ ] Toda comparação é contra distribuição, município ou histórico agregado
- [ ] Nenhuma comparação com o Centro de Franca/SP
- [ ] Todo item com os quatro campos, e a ressalva explicada dentro do texto
- [ ] Nenhum "muda a leitura se" no relatório
- [ ] Cada lacuna e cada item de campo explicado: o que falta, por que importa aqui, o que destrava
- [ ] Nenhum score, nota ou "recomendado"
- [ ] Seção "O que este dossiê NÃO sabe" presente, com fluxo de passantes
- [ ] Tabela de procedência fechando o documento
- [ ] Nenhum nome de pessoa
- [ ] Aprovado pelo `(⌕) auditor-de-evidencia`
