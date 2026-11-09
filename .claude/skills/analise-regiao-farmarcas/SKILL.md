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
- `references/lentes-do-dossie.md` — as 4 lentes no quadrante SWOT, a anatomia do item, a confiança como critério de entrada, o tier. **Step 4.**
- `references/benchmarks.md` — contra o que comparar. **Step 4.**
- `references/limites-e-vieses.md` — o que o dado não diz. **Step 5, obrigatório.**
- `references/modelo-de-dossie.md` — estrutura do entregável. **Step 6.**
- `references/benchmarks.md` — e o que NUNCA serve de referência.

## Critical

- **Perguntar SEMPRE se o solicitante é empresário novo ou já associado**, e
  qual bandeira e modelo (popular/convencional) ele pretende. Sem isso o dossiê
  não sabe se a loja Farmarcas vizinha é problema ou estratégia, e não consegue
  aplicar o zoneamento. É a primeira pergunta, não um detalhe de preenchimento.
- **O teto de zoneamento conta GRUPOS ECONÔMICOS, não lojas** (refinado com o PM
  em 2026-10-29). Barra a entrada de um **novo grupo** na praça — porque o que a
  regra protege é a convivência entre associados, e não há conflito onde só há um.
  Cidade com mais lojas que o número da faixa, todas do mesmo grupo, recebe
  **alerta de densidade**, nunca impedimento. Grupo sai do responsável pelo GE no
  cadastro, por nome e não por CNPJ — declare isso onde a contagem aparecer.
- **A exigência de bandeira popular na faixa de 60–120 mil também conta grupos.**
  Ela vale para o **2º grupo que entra** na praça, não para a 2ª loja contada. Loja
  adicional de grupo já presente recebe **alerta**, porque a página escreve "a 2ª
  loja" e não define esse caso.
- **Zoneamento é gate, não indicador.** Roda ANTES da análise de mercado. Se o
  veredito for `impedimento`, o dossiê **para** e devolve o impedimento com a
  regra citada. Não existe dossiê de mercado bonito que destrave um ponto que a
  regra de expansão barra.
- **Ponto barrado sai com praças alternativas — e isso NÃO é análise de mercado
  do ponto barrado.** São coisas diferentes, e confundi-las custou caro: levantar
  renda, concorrência e potencial do endereço reprovado sugere que há número a
  negociar ali, e não há — o que existe é decisão de quem é dono da regra. Listar
  praças onde a regra **não** barra não afirma nada sobre o endereço pedido: é o
  próximo passo, e sem ele o analista recebe um "não" sem caminho. O relatório de
  impedimento roda **um único** script além do gate, o de praças alternativas, com
  o filtro de disponibilidade ligado. Nenhum script de mercado do ponto.
- **Praça disponível conta GRUPOS ECONÔMICOS, nunca lojas.** Cidade com cinco
  lojas de um único dono e teto 2 **continua disponível** para um grupo novo —
  filtrar por contagem de lojas esconde justamente as praças que a lista existe
  para mostrar. E a disponibilidade depende da **bandeira pretendida**: na faixa
  de 60 a 120 mil o 2º grupo só entra com bandeira popular, então praça com um
  grupo instalado está aberta para quem pretende popular e fechada para quem
  pretende convencional. A mesma linha, duas respostas.
- **O entregável é SEMPRE HTML gerado por `montar_relatorio.py`** — dossiê
  completo e dossiê de impedimento, sem exceção. O gate decide QUAL relatório o
  script monta, não se há relatório: `veredito: impedimento` monta o relatório
  curto, sem rodar nenhum script de mercado. Markdown escrito à mão não é
  entregável — ele reabre a porta para número que o modelo formatou sozinho, que
  é exatamente o que a divisão número→script existe para fechar.
- **"Loja nossa" sai do cadastro de lojas (CNPJ + coordenada)**, nunca do nome
  de bandeira dentro da camada Concorrentes — esse dá falso positivo
  comprovado. Match por nome é suspeita a confirmar, e vai rotulada como tal.
- **Venda por loja tem TRÊS fontes, e elas não medem a mesma coisa.**
  1. **Faixa de faturamento da camada de concorrentes** — *não é medida nem
     estimativa por loja*: o campo assume **8 valores em toda a base** (verificado
     em 2026-11-06 sobre os 100.612 registros), um por faixa da régua, e o que ele
     diz é **em que faixa aquela loja caiu** — sete dos valores são o ponto médio
     da faixa e o mais baixo é o teto da faixa aberta embaixo. Está preenchido em
     menos da metade dos cadastros. A distância entre dois desses números é a
     distância entre faixas, nunca entre duas lojas, e nenhum deles é o
     faturamento de nenhum estabelecimento — escrever "mediana do faturamento dos
     vizinhos" é ler como medida o que é rótulo. Diga **faixa**: "a faixa mediana
     ocupada", "a faixa mais alta ocupada".
  2. **Régua de canal** — *medida*: receita e quantidade de PDVs por canal
     (ABRAFARMA, FEBRAFAR, associações e franquias, independentes, outras redes
     corporativas) **e por UF**, da base do instituto. A camada de concorrentes
     já classifica cada loja num rótulo que mapeia para esses canais, então toda
     loja do raio ganha um faturamento de referência, mesmo as que estão sem
     faixa preenchida. É o que **dimensiona o mercado do raio**.
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
- **A nota do card leva a comparação e a fonte — nunca a chave de casamento nem
  o código do registro.** "UF: R$ 29,89 · UF + nome do município (Irati) →
  1806-PR_IRATI" é identificador de base dentro do corpo do relatório: não diz
  nada a analista nem a executivo, e anuncia "saída de robô" bem onde o problema
  a resolver é confiança no número. O que o leitor precisa saber sobre o brick —
  que **não se sabe em qual deles o ponto cai** — é lacuna obrigatória, em
  linguagem de negócio. Por qual chave duas tabelas casaram é detalhe de
  implementação e vive na saída do script. O gerador avisa quando uma nota de
  card carrega identificador de base, nome de campo, nome de script ou flag.
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
- **Praça alternativa é ancorada no ponto pedido, nunca só na UF.** Ordenar por
  mercado absoluto devolve sempre a capital: medido em 2026-11-05, Pouso Alegre
  e Ipatinga — 390 km entre si, mesma UF — recebiam listas **idênticas**, 15 de
  15 praças, nenhuma a menos de 150 km de qualquer uma das duas. A lista era
  função do estado, não do pedido, e quem recebeu um "não" precisa de praça que
  consiga operar. Por isso toda busca de praças passa a coordenada do ponto e um
  **raio declarado**, e a tabela mostra a distância de cada linha. O raio é
  **premissa, não medida** — nenhuma fonte diz a que distância um empresário
  aceita operar —, e vai escrito no relatório com essa palavra.
- **Dentro do raio, a ordenação continua sendo por mercado.** Ordenar por
  distância pura foi testado e é pior: devolve o vilarejo mais próximo e esconde
  a praça boa a 80 km. O par que funciona é **filtrar por alcance, depois
  ordenar por mercado** — foi assim que Poços de Caldas e Varginha apareceram.
- **Raio sem praça disponível é achado, não falha.** Quando não há praça
  disponível dentro do raio, o filtro se desliga sozinho, a lista volta a cobrir
  a UF e o relatório **diz isso com todas as letras** — porque "o caminho mais
  próximo exige mudar de região" é informação, e tabela vazia não é. A distância
  de cada linha continua declarada para a decisão ser consciente.
- **A distância entre praças é aproximada e declarada como tal.** O acervo não
  traz coordenada de município: o polígono da UTC ficou no asset e a coluna de
  geometria do CSV guarda só a palavra "Polygon". A distância usa a **mediana**
  das coordenadas de farmácia da cidade na camada de concorrentes — mediana e
  não média, porque a camada tem registro cadastrado numa cidade com coordenada
  em outra. Serve para ordenar praças e dar ordem de grandeza, **nunca** para
  medir distância entre dois endereços.
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
  guardam **fração de 0 a 1**: verticalização 0,56 é 56%. `fatMedio` é **mensal**
  — está no código do produto, não no dump — e é **rótulo de faixa**, não valor
  da loja: oito valores em toda a base.
  Na dúvida, conferir em `references/indicadores-do-relatorio.md`, nunca inferir
  pelo tamanho do número.
- **Um dossiê nunca se apoia em outro.** Nada de "mais que o ponto analisado
  antes", "ao contrário daquela praça", "o dobro do que vimos em X". Cada
  dossiê é lido isolado, por quem pode nunca ter visto o outro — e comparar
  dois pontos específicos não é referência, é anedota: dois casos não formam
  distribuição. Referente válido é a **distribuição**: percentil nacional,
  mediana da base, distribuição nacional da própria camada, ou o próprio
  município — nunca o histórico de análises, que não entra no dossiê.
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
- **A leitura da região só aceita confiança alta ou média, e nunca escreve a
  nota.** A confiança continua sendo avaliada em cada afirmação — ela só mudou
  de função: decide se a afirmação **entra** na lente, em vez de virar frase.
  Confiança **baixa ou nenhuma não entra na lente**; vai para "O que este dossiê
  NÃO sabe", com as três perguntas respondidas. E o **motivo da nota não aparece
  em lugar nenhum da lente** — nem rotulado ("Confiança média, porque…"), nem
  disfarçado ("o dado é robusto", "com alguma ressalva"). O corte é por
  **afirmação**, não por item: no mesmo parágrafo, a parte cadastral fica e o
  palpite sai. Nada é silenciado — muda de endereço, e o endereço já existe.
- **O que o número É fica na lente; o quanto confiar nele sai.** A linha é fina
  e não é opcional, porque esta skill **obriga** certas ressalvas a andarem
  junto do número: que a régua de canal é a média da UF e não a venda daquela
  loja, que MAT é acumulado de 12 meses, que potencial e captura são municipais,
  que a periodicidade do potencial não é declarada pela base. Essas descrevem **o
  indicador** — sem elas o leitor lê outro número — e continuam na lente. O que
  descreve a **qualidade** do indicador ("a base não traz a dispersão", "o
  casamento foi por nome") vai para a lacuna, onde se diz o que destravaria.
  Ver a tabela em `references/lentes-do-dossie.md`.
- **A lente não explica o método: o relatório já explica.** O gerador escreve
  sozinho o card "Método de rateio" — com a cobertura do círculo e a contagem de
  setores — e os parágrafos explicativos da renda, do potencial e dos geradores
  de fluxo, que já dizem que cada setor entra pela fração que cai dentro do
  círculo e que as taxas são média ponderada. Escrever isso de novo na lente
  **não declara nada, duplica**: o parágrafo dobra de tamanho e o número, que é o
  que o analista procura, é empurrado para o fim. Nada de "cada setor entra pela
  fração de área", "as taxas entram como média ponderada", "100% do círculo é
  coberto por setor com geometria" ou "o casamento do brick foi por nome" dentro
  das lentes. A ressalva que muda **qual número se está lendo** fica; a que
  descreve **como a conta foi feita** já tem bloco próprio, e ele vem preenchido.
- **A leitura da região é um QUADRANTE SWOT**, em ordem fixa: Forças e
  Fragilidades em cima, Oportunidades e Dificuldades embaixo; a favor à
  esquerda, contra à direita. Numa matriz quem informa é a posição, não o
  rótulo — e empilhadas em coluna as quatro lentes viravam quatro blocos de
  texto em sequência, com o par de cada linha separado por uma tela de rolagem.
  Quadrante sem item continua desenhado, com a linha de ausência no lugar do
  texto: buraco na matriz é informação.
- **Toda lacuna é declarada.** Base ausente, campo com erro de planilha,
  município fora de uma base: vira item da seção "O que este dossiê NÃO sabe",
  com o que destravaria. Lacuna silenciada vira conclusão errada.
- **A seção de lacunas sai RECOLHIDA, nunca encurtada.** O gerador a monta como
  bloco expansível, fechado por padrão, com a contagem no título e aberta num
  clique — e aberta por completo na impressão, porque em PDF não há clique.
  Recolher é decisão de **hierarquia visual**: aberta, a lista ocupa uma tela
  inteira perto do fim e empurra as Fontes para fora da vista. Não é licença
  para escrever menos: a seção continua com todas as lacunas, cada uma com as
  três perguntas respondidas. O que o leitor vê fechado é a contagem — que
  existe justamente para ele não concluir que não há lacuna nenhuma.
- **"Para confirmar em campo" é seção própria e visível.** Mora fora do bloco
  recolhido, porque não é lacuna: é o que o analista vai fazer. Ficava dentro
  da seção de lacunas por acidente de marcação, e recolher uma teria levado a
  outra junto.
- **"Fluxo de passantes" entra SEMPRE como lacuna**, em todo dossiê, mesmo em
  ponto residencial. Não existe no dump nem no produto, e é a variável que mais
  distorce ponto de rua comercial.
- **Rodar pelo menos dois raios: 300 m e ~5 km.** O padrão de 300 m do produto
  responde uma pergunta mais estreita que a do analista, cuja prática real gira
  em torno de 5 km. Os dois saem no relatório, comparados. O relatório mostra os
  raios e o que muda entre eles — nunca de onde veio essa calibração.
- **Nome de pessoa nunca entra** — nem empresário, nem consultor, nem analista,
  nem citado de parecer histórico. As bases têm esses campos; os scripts os
  descartam; o texto também descarta.
- **O dossiê NUNCA fala de outras análises.** Nem quantas existem na base, nem
  que já houve análise neste ponto ou nesta região, nem o resultado delas, nem
  o parecer de ninguém — em nenhuma lente, lacuna, nota de card ou seção de
  fontes. Dois motivos somados: o parecer **não prediz desfecho** (medido em
  `analise-ponto-orbita`: log-rank p = 0,8275 sobre 101 fechamentos), de modo
  que citá-lo sugere um sinal que não existe; e o dossiê descreve **a região**,
  não o que a casa já decidiu sobre ela. Por isso `benchmark_historico.py` saiu
  do fluxo: o que ele responde é calibração interna da skill, não conteúdo.
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
| Poder preditivo do parecer | `C:\Users\zequi\projetos\analise-ponto-orbita\README.md` | por que análise anterior não entra no dossiê |
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
- **impedimento** → escrever a narrativa curta de impedimento (ver
  `references/modelo-de-dossie.md`), gerar o HTML e **parar**. Não rodar os
  scripts de mercado: `montar_relatorio.py` reconhece o veredito e não os roda.
  O relatório curto **inclui a seção de praças alternativas**, montada pelo único
  script que roda além do gate — ver a regra no `## Critical` sobre por que isso
  não contradiz "não levantar mercado do ponto barrado".
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
python scripts/implantacao.py         --lat <LAT> --lng <LNG>
#   esquina ou meio de quadra — só afirma com confiança alta; sem ela, OMITA o assunto
python scripts/alternativas.py        --uf <UF> --excluir-municipio <CODIGO> \
                                      --modelo <popular|convencional> --so-disponiveis
#   --so-disponiveis filtra por GRUPOS econômicos < teto, não por lojas
#   --modelo é obrigatório na prática: sem ele a exigência de bandeira popular do
#   2º grupo na faixa 60–120 mil não é aplicada, e a lista indica praça barrada
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

Para cada item candidato, exigir os três campos escritos: número, **fonte de
dado** (em campo próprio) e comparação. **Não existe campo "muda a leitura se"**
e **a nota de confiança não é escrita**.

A confiança é avaliada em cada afirmação e usada como **critério de corte**:

| Confiança da afirmação | Para onde ela vai |
|---|---|
| alta | lente, sem rótulo e sem o motivo da nota |
| média | lente, sem rótulo — e o limite do método vira lacuna |
| baixa | **lacuna**, nunca lente |
| nenhuma (o dado não existe) | **lacuna**, nunca lente |

Cortar por afirmação, não por item: "a loja fechou a 335 m" é cadastral e fica;
"por que ela fechou" não está em base nenhuma e sai. Item sem comparação não
entra. Item que não muda nenhuma decisão não entra. Cortar pelo Tier até caber
em ~15 itens.

A saída é um **quadrante SWOT**, com as quatro lentes em ordem fixa. Escrever
cada lente pensando no par dela: Forças se lê ao lado de Fragilidades, e
Oportunidades ao lado de Dificuldades.

## Step 5 — Limites

Ler `references/limites-e-vieses.md` e montar "O que este dossiê NÃO sabe".
Fluxo de passantes é obrigatório. Somar as lacunas devolvidas pelos scripts —
**e tudo que o Step 4 cortou das lentes**: cada afirmação de confiança baixa ou
nenhuma, e o limite de método de cada item de confiança média que entrou. É
esta seção que impede o corte das lentes de virar silêncio; ela é o outro lado
da mesma regra, não um depósito.

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

1. Escrever a narrativa em JSON. **Com o gate liberado ou em alerta:** resumo em
   uma linha, as quatro lentes com os campos de cada item, `nao_sabe` e `campo`.
   **Com o gate em impedimento:** resumo, `leitura` (parágrafos), `o_que_mudaria`,
   `alertas_cadastro`, `nao_sabe` e `campo` — sem lentes, que seriam ignoradas.
   Os dois formatos estão no topo de `scripts/montar_relatorio.py`. Salvar em
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
| "O ponto é barrado, então não indico nada — seria sugerir que há saída" | a saída existe, só não é neste endereço; praça onde a regra não barra é o próximo passo, não negociação do ponto |
| "Filtro praça disponível por lojas < teto" | o teto conta grupos; cinco lojas de um dono só deixam a praça disponível, e o filtro por lojas a esconderia |
| "Listo as praças sem saber a bandeira do pedido" | na faixa 60–120 mil o 2º grupo tem de ser popular; sem o modelo você indica praça onde ele seria barrado de novo |
| "Casou com bandeira Farmarcas, então é loja nossa" | falso positivo comprovado; confirme no cadastro |
| "Uso a população do dump, que é a da tela" | perto de 60/120/200 mil ela troca a faixa de zoneamento |
| "A cidade tem mais lojas que o teto, então está barrada" | o teto conta GRUPOS ECONÔMICOS; se todas respondem ao mesmo grupo, é alerta de densidade, não impedimento |
| "O solicitante já é associado, então não é grupo novo na praça" | ser da casa não dá vaga; o que conta é já responder por loja NESTA cidade |
| "O número deve girar em torno de X" | número sem script não entra |
| "A lacuna é técnica demais, resumo como dados limitados" | lacuna genérica não permite o analista agir |
| "Ponto residencial, pulo o aviso de fluxo" | o aviso é incondicional |
| "300 m basta, é o padrão do produto" | a prática real do time é 5.500 m de mediana |
| "Reprovaram aqui, então sinalizo risco" | o parecer não prediz desfecho — e análise anterior não entra no dossiê, em forma nenhuma |
| "Digo só que já analisaram esta região, sem o resultado" | continua sendo informação de outra análise; o dossiê descreve a região, não o histórico de decisões sobre ela |
| "Cito quantas análises a base tem, para dar lastro ao método" | número de análises é dado interno; no relatório ele só serve para o leitor perguntar o que mais há ali |
| "Não achei se é esquina, então escrevo que não foi possível determinar" | saber que não se sabe a posição na quadra não muda decisão; omita o assunto inteiro |
| "Não casou brick, mas deixo o card com o preço da UF na nota" | card de destaque dizendo "—" convida a ler o agregado estadual como se fosse o do ponto |
| "A cidade influencia 3 municípios" | nomeie os três e some a população: três cidades de 2 mil e três de 40 mil são praças diferentes |
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
| "O ponto é barrado, escrevo o impedimento em markdown mesmo" | o entregável é HTML nos dois casos; o gerador tem relatório de impedimento |
| "Gero sem o responsável, o vínculo o script resolve" | sem ele toda loja vira de outro associado e a contagem por empresários inverte — o relatório sai afirmando o contrário, sem avisar no corpo |
| "As duas contagens do teto empatam hoje, então não divergem" | a pergunta é sobre o PEDIDO: a loja nova sempre entra na contagem por lojas, e só entra na por empresários se o solicitante ainda não tiver loja na cidade |
| "Cito o script na fonte, assim fica rastreável" | rastreável é a fonte de DADO; o script vai no rodapé |
| "Escrevo na lente que o setor entrou pela fração de área — é ressalva obrigatória" | era, e deixou de ser: o card de método e o parágrafo da renda já dizem isso. Na lente vira duplicação que empurra o número para o fim do parágrafo |
| "Declaro a cobertura do círculo na lente, senão ela some do relatório" | ela não some: sai no card **Método de rateio**, com a contagem de setores ao lado |
| "Explico a ponderação das taxas para o leitor não somar errado" | o parágrafo explicativo da renda já explica, e com mais espaço do que a lente tem |
| "Tirei a mecânica do rateio e tirei junto que o potencial não tem periodicidade" | são coisas diferentes: a periodicidade muda QUAL número se lê (12×), a fração de área descreve como a conta foi feita |
| "Fecho o item com 'muda a leitura se'" | o rótulo foi removido; se é preciso ressalvar, a ressalva é lacuna |
| "Escrevo 'Confiança alta' para o leitor saber que o número é firme" | ela é critério de ENTRADA: o item estar na lente já diz isso. Escrita, repetia-se em todo parágrafo e ensinava a pular a frase |
| "O item é de confiança baixa, mas é importante demais para ficar de fora" | é por ser importante que ele vai para as lacunas, onde se diz o que destravaria — na lente ele seria lido como coisa sabida |
| "Não escrevo 'confiança', escrevo 'o dado é robusto'" | é a mesma nota com outra roupa; o quadrante não comenta a própria qualidade |
| "Tirei a nota e tirei junto que a régua de canal é a média da UF" | essa frase descreve o INDICADOR, não a qualidade dele: sem ela o leitor lê o número como venda daquela loja. Ressalva obrigatória por regra da casa fica |
| "A afirmação é meio cadastral e meio palpite, então corto o item todo" | o corte é por afirmação: a parte medida fica na lente, o palpite vira lacuna |
| "Uma lente ficou sem item, tiro a caixa dela" | buraco na matriz é informação, e tirar a caixa desalinha as outras três |
| "A lacuna é uma linha, o leitor deduz o resto" | lacuna sem o porquê e sem o destravamento não é acionável |
| "A seção vem recolhida, então posso ser breve nas lacunas" | recolher é hierarquia visual, não permissão para escrever menos; quem abre o bloco precisa das três perguntas respondidas |
| "Recolhida é quase omitida, então corto as lacunas fracas" | o critério de entrada não mudou: entra toda lacuna que muda decisão, e a contagem no título denuncia o corte |
| "Deixo o bloco aberto, a lacuna é importante" | a importância está no conteúdo e na contagem do título; aberto, ele engole a tela e esconde as Fontes |
| "Cito a fonte na frase, fica mais rastreável" | espalhada em 16 parágrafos ninguém usa; consolidada, sim |
| "O card também manda a fonte para o fim" | card se lê isolado; a nota dele carrega a origem |
| "Ponho o critério de casamento na nota do card, assim fica rastreável" | rastreável é a fonte de DADO; a chave de casamento e o código do brick são nome de registro de base, e o que o leitor precisa — não saber em qual brick o ponto cai — é lacuna |
| "Pego aluguel médio de portal de anúncio" | não é fonte verificável; sem o valor informado, o campo fica vazio |
| "A média de faturamento basta para dizer quanto se vende" | a distribuição tem cauda longa; mostre mínimo, mediana e máximo |
| "Uso só o faturamento dos concorrentes" | é rótulo de faixa, cobre metade dos cadastros e não mede loja nenhuma; a receita medida do grupo existe e filtra por bandeira |
| "A mediana do faturamento dos vizinhos é R$ X" | esse campo tem 8 valores fixos: o que existe é a FAIXA mediana ocupada, e a distância entre dois valores é distância entre faixas |
| "Receita MAT é do mês" | MAT é acumulado de 12 meses; dividir por 12 só vale para loja do período inteiro |
| "As duas fontes divergem, escolho a melhor" | a divergência é achado: uma mede concorrente, a outra mede a nossa bandeira |
| "Só uma loja do raio tem faturamento, então não dá para dimensionar o mercado" | a régua de canal cobre toda loja classificada, inclusive as de campo vazio |
| "A régua de canal diz que aquela loja fatura R$ X" | diz o que a loja MÉDIA do canal fatura na UF; a dispersão dentro do canal não está na base |
| "A loja não casou com nenhum canal, uso a média das outras" | vira faixa entre o canal mais barato e o mais caro, com a contagem declarada |
| "Somo o raio pela régua de canal e chamo de mercado do município" | o raio cruza divisa; mercado do município é o total medido da cidade |
| "Conto equipamentos no OSM e chamo de fluxo" | é proxy fraco; fluxo continua sendo lacuna |
| "Região é o que o raio alcança" | região é a CIDADE do ponto; o raio em divisa vira macrorregião |
| "Listo a cidade sem dizer qual UTC é" | sem a localidade, a mesma cidade repetida parece oportunidade duplicada |
| "Listo as maiores praças da UF, que são as melhores oportunidades" | sem âncora no ponto a lista vira função do estado: dois pedidos a 390 km um do outro recebiam listas idênticas, e nenhuma praça a menos de 150 km de nenhum dos dois |
| "Ordeno por distância, assim fica perto do empresário" | testado e pior: devolve o vilarejo mais próximo e esconde a praça boa a 80 km. Filtre por alcance, depois ordene por mercado |
| "Nenhuma praça cabe no raio, então deixo a tabela vazia" | tabela vazia não é resposta; desligue o filtro, mostre a UF e DECLARE que não há praça perto — é esse o achado |
| "A distância até a praça é precisa, saiu de cálculo" | é mediana das farmácias da cidade, porque o acervo não tem coordenada de município; serve para ordenar, não para medir endereço |
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
- [ ] Rateio proporcional aplicado, com a cobertura do círculo declarada **no card
      de método** — e não repetida na prosa das lentes
- [ ] "Vendas totais na região" calculada sobre a cidade do ponto, não sobre o raio
- [ ] Registros de cadastro implausível separados dos de cidade vizinha
- [ ] Se usou krigagem, o diagnóstico e os campos recusados estão no dossiê
- [ ] Split de consumo entre Medicamentos e Higiene/Beleza/Nutrição presente
- [ ] Preço médio do brick com o critério de casamento declarado
- [ ] Geradores de fluxo no entorno, ou a lacuna do Overpass declarada
- [ ] Implantação do ponto (esquina, meio de quadra) presente **se** houve
      confiança alta — e totalmente ausente, sem menção, se não houve
- [ ] Zona de influência com os municípios **nomeados** e a população somada
- [ ] Card de preço no brick presente só quando houve casamento de brick
- [ ] Nenhuma menção a outras análises: nem contagem, nem existência, nem resultado
- [ ] **Impedimento: seção de praças alternativas presente**, filtrada por grupos
      econômicos abaixo do teto e pela bandeira pretendida, com a ressalva de que
      grupo é apurado por nome e não por CNPJ
- [ ] Dito, na seção de praças, que indicar praça NÃO é análise de mercado do ponto
      barrado — e que cada praça ainda precisa do seu próprio dossiê
- [ ] Em "Onde mais olhar", cada linha nomeia a localidade da UTC — nenhuma cidade genérica repetida
- [ ] Praças alternativas ancoradas na coordenada do ponto, com a distância de cada
      linha visível e o raio declarado como premissa — e, se não houver praça
      disponível dentro dele, isso dito no texto em vez de tabela vazia
- [ ] Potencial e captura rotulados como municipais
- [ ] Leitura da região em **texto corrido**, com abertura por lente — sem bullets
- [ ] Leitura da região em **quadrante SWOT**, nas quatro posições fixas, com a
      lente vazia desenhada em vez de omitida
- [ ] Explicação presente antes da renda, do potencial de consumo e dos geradores de fluxo
- [ ] "Onde mais olhar" com escala por extenso, preço médio, captura e o porquê de cada praça
- [ ] Nenhuma citação de fonte na prosa — todas na seção Fontes, numeradas
- [ ] Cards de origem não óbvia citam a fonte na própria nota — e nenhuma nota
      carrega código de brick, nome de campo, de script ou de arquivo de base
- [ ] Venda por loja nas TRÊS fontes: **faixa** ocupada pelos concorrentes (rótulo, nunca medida), régua medida por canal e receita medida do grupo
- [ ] Mercado do raio dimensionado pela régua de canal, com a contagem de lojas sem canal declarada
- [ ] Dito, onde a régua de canal aparece, que ela é a média do canal na UF e não o faturamento daquela loja
- [ ] Receita medida filtrada pela bandeira pretendida, com o recorte nacional ao lado
- [ ] Seção Fontes com a tabela numerada e a procedência geral
- [ ] Nenhum nome de script, flag ou arquivo de base no corpo do relatório
- [ ] Relatório HTML gerado por `montar_relatorio.py`, não escrito à mão — vale
      também para o dossiê de impedimento, que tem relatório próprio
- [ ] As contagens do teto mostradas **aplicadas ao pedido**, não ao estado atual
      da cidade, e com grupos econômicos separados de lojas
- [ ] Origem da coordenada do ponto declarada — geocodificada ou informada
- [ ] Abaixo de 60 mil habitantes sem impedimento: a distância mínima declarada
      como regra SEM VEREDITO, não como pergunta de canibalização
- [ ] Solicitante já associado: relatório gerado **com o responsável pelo GE**, senão
      o vínculo das lojas e a contagem por empresários saem como não apurados
- [ ] Nenhuma referência a outro dossiê, nem explícita nem por eco
- [ ] Toda comparação é contra distribuição, município ou histórico agregado
- [ ] Nenhuma comparação com o Centro de Franca/SP
- [ ] Todo item das lentes com os três campos: número, fonte em campo próprio e comparação
- [ ] **A palavra "confiança" não aparece em nenhuma lente** — nem rotulada, nem
      disfarçada ("o dado é robusto", "com alguma ressalva")
- [ ] Nenhuma afirmação de confiança baixa ou nenhuma dentro das lentes — cada
      uma delas presente em "O que este dossiê NÃO sabe", com as três perguntas
- [ ] Limite de método dos itens de confiança média presente nas lacunas
- [ ] Nenhuma lente explicando o método de cálculo — fração de área, ponderação
      das taxas, cobertura do círculo e critério de casamento do brick vivem nos
      blocos que o gerador escreve, não no texto das lentes
- [ ] Nenhum "muda a leitura se" no relatório
- [ ] Cada lacuna e cada item de campo explicado: o que falta, por que importa aqui, o que destrava
- [ ] Nenhum score, nota ou "recomendado"
- [ ] Seção "O que este dossiê NÃO sabe" presente, com fluxo de passantes —
      recolhida por padrão, com a contagem no título, e com o conteúdo íntegro
      dentro dela
- [ ] "Para confirmar em campo" em seção própria, fora do bloco recolhido
- [ ] Tabela de procedência fechando o documento
- [ ] Nenhum nome de pessoa
- [ ] Aprovado pelo `(⌕) auditor-de-evidencia`
