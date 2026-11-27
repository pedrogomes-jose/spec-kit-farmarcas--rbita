# As quatro lentes

O dossiê não dá nota e não dá veredito. Ele organiza o que se sabe da região em
quatro lentes, dispostas num **quadrante SWOT**, e cada item carrega o que
permite ao analista discordar.

**Anatomia de um item** — sem os três campos, o item não entra:

1. **número** — valor, com unidade, no texto
2. **fonte de dado** — em **campo próprio** (`fonte`), nunca no meio da frase
3. **comparação** — contra o município, a UF, ou a distribuição nacional
4. **parecer** (quando o número tem referente) — campo `parecer` do item, que
   diz se o número é bom ou ruim contra aquela comparação. O modelo informa o
   indicador e a posição (`{"indicador": "renda_por_habitante", "posicao":
   "acima", "referente": "anel de 5 km"}` ou `{"indicador":
   "habitantes_por_farmacia", "percentil": 4}`); o rótulo — Bom, Na média, Ruim,
   Ambíguo, Sem referência — sai de `scripts/_parecer.py`. Ver
   `benchmarks.md`, `## Parecer por número`

**A fonte sai do parágrafo.** Ela vai no campo `fonte` do item e aparece como
referência numerada no fim da frase, resolvida na seção **Fontes** ao final do
relatório. Fonte no meio do texto interrompe a leitura e, paradoxalmente, some
do radar de quem quer conferir: espalhada por dezesseis parágrafos, ninguém a
usa. Consolidada numa tabela, serve às duas coisas — o texto corre e o auditor
acha tudo num lugar só.

## A confiança decide a ENTRADA do item, e nunca vira texto

Avaliar a confiança continua obrigatório. **Escrevê-la, não.** Ela é critério
de corte, não conteúdo:

| Confiança do que se vai afirmar | O que acontece com a afirmação |
|---|---|
| **alta** | entra na lente, sem rótulo e sem a justificativa da nota |
| **média** | entra na lente, sem rótulo — e o limite do método vai para "O que este dossiê NÃO sabe" |
| **baixa** | **não entra na lente.** Vira lacuna, com as três perguntas respondidas |
| **nenhuma** (o dado não existe) | **não entra na lente.** Vira lacuna |

**O corte é por afirmação, não por item.** Um parágrafo costuma misturar
confianças: a loja desativada a 335 m é cadastral e tem CNPJ e coordenada, mas
o motivo do fechamento não está registrado em lugar nenhum. A existência e a
distância ficam na lente; o porquê sai dela e vira lacuna. Cortar o item
inteiro perderia um achado medido; mantê-lo inteiro contrabandearia um palpite.

**Nada é silenciado — muda de endereço.** O que saiu da lente aparece na seção
"O que este dossiê NÃO sabe" — ou em "Para confirmar em campo", quando o que
falta é ação do analista e não dado. As duas já existem, já são obrigatórias e
já estão no relatório. A regra da casa continua valendo: lacuna silenciada vira
conclusão errada. O que não vale mais é a lacuna disfarçada de achado.

### O que o número É fica; o quanto confiar nele sai

É a linha mais fina desta regra, e ela não é opcional: há ressalvas que a casa
**obriga** a escrever junto do número, e tirá-las junto com a nota de confiança
seria trocar um defeito de leitura por um erro de conteúdo.

| Fica na lente, junto do número | Sai para as lacunas |
|---|---|
| **unidade e recorte** — "é mensal", "é do município, não do quarteirão", "é acumulado de 12 meses" | a nota de confiança e o motivo dela |
| **a que o número se refere** — "a faixa mediana ocupada", "a loja média do canal" | o que faria o número estar errado |
| **viés declarado por regra da casa** — a janela dupla da régua de canal, a divergência entre fontes | o que falta para resolver o viés |
| **o que o número não distingue** — "a série é de receita, não separa volume de preço" | o que destravaria a distinção |

#### E a ressalva obrigatória vai no SUBSTANTIVO, nunca numa frase ao fim

Esta é a forma, e ela não é estilo: a ressalva que a casa obriga entra no **nome
do número dentro da frase**, não como oração explicativa fechando o parágrafo.

| Não escrever | Escrever |
|---|---|
| "A mediana de faturamento da cidade é R$ 330.312. O campo registra em que faixa a loja caiu, não quanto cada uma vende, e a distância entre dois desses valores é distância entre faixas." | "A **faixa mediana ocupada** pelas 11 farmácias da cidade é a de R$ 330.312 por mês." |
| "O entorno movimenta R$ 5,27 milhões ao ano. São médias do canal no estado, nunca o faturamento de nenhuma dessas lojas em particular." | "Somadas as lojas pela **régua de canal** — a **loja média** de cada canal em Minas —, o entorno de 300 m movimenta R$ 5,27 milhões ao ano." |
| "São R$ 3,06 milhões de potencial. É demanda potencial de quem mora na área, não venda realizada, e a base não declara a periodicidade." | "O **potencial de consumo** em drogarias no raio de 300 m é de R$ 3,06 milhões." |

Nomeado certo, o número já não é lido como outro número — que era todo o motivo
da ressalva existir. Escrita depois, em frase própria, ela faz três estragos de
uma vez: repete o que o relatório **já declara em bloco próprio**, dobra o
parágrafo e empurra o achado para longe do começo. A regra da casa continua
valendo; mudou o lugar onde ela se cumpre.

### E há um terceiro destino: o que o relatório já declara sozinho

O gerador escreve blocos de método por conta própria — o card "Método de
rateio", com a cobertura do círculo e a contagem de setores, e os parágrafos
explicativos da renda, do potencial e dos geradores de fluxo, que já dizem que
cada setor entra pela fração que cai dentro do círculo e que as taxas são média
ponderada. **Repetir isso na lente não declara nada: duplica.**

| Não escrever na lente | Onde já está |
|---|---|
| "cada setor entra pela fração de área que cai dentro do círculo" | parágrafo explicativo da renda e do potencial |
| "as taxas entram como média ponderada — a renda por habitante pela população" | parágrafo explicativo da renda |
| "100% da área do círculo é coberta por setor com geometria" | card **Método de rateio**, com a contagem de setores ao lado |
| "o casamento do brick foi por nome de município" | nota do card de preço no brick |
| "o campo registra em que faixa a loja caiu, não quanto cada uma vende" | bloco **Concorrentes da praça — em que faixa de faturamento eles caem**, que já diz isso em três frases |
| "a distância entre dois desses valores é distância entre faixas" | o mesmo bloco, na última frase dele |
| "são médias do canal no estado, nunca o faturamento de nenhuma dessas lojas" | bloco **O que este número é e o que não é**, embaixo da tabela de canais |
| "a receita é acumulada de 12 meses e a contagem de PDVs é do ano corrente" | o mesmo bloco |
| "é demanda potencial, não venda realizada" · "a base não declara a periodicidade" | parágrafo explicativo do potencial de consumo |
| "é receita medida de loja da rede, não do concorrente" | título e notas do bloco **Lojas do grupo — receita medida** |

As quatro últimas linhas entraram depois das outras, e por um motivo que vale
registrar: elas são ressalvas que esta skill **obriga** a declarar, e por isso
vinham sendo escritas na lente como se não houvesse outro lugar. Há: o gerador
escreve cada uma delas, por extenso, no bloco onde o número aparece. A obrigação
se cumpre lá. Na lente, o que resta a fazer é **chamar o número pelo nome
certo** — faixa ocupada, loja média do canal, potencial de consumo — e seguir.

O efeito de escrever assim mesmo é concreto: o parágrafo da lente dobra de
tamanho, o número — que é o que o analista procura — vai para o meio ou para o
fim, e a mecânica de cálculo ocupa o lugar do achado. A lente responde **o que
a região é**; o método de apuração tem bloco próprio e ele já está preenchido.

A linha divisória é esta: fica na lente a ressalva sem a qual o leitor lê
**outro número** — a régua de canal é média da UF, o MAT é acumulado de doze
meses, o potencial e a captura são municipais, o potencial não tem
periodicidade declarada. Sai da lente a ressalva que descreve **como a conta
foi feita**, porque o relatório já a declara onde se procura por ela.

O teste é uma pergunta: a frase descreve **o indicador** ou **a sua qualidade**?
"É a média do canal em São Paulo, não a venda desta farmácia" descreve o
indicador — sem ela o leitor lê outro número. "Confiança média, porque a base
não traz a dispersão dentro do canal" descreve a qualidade — e vai para a
lacuna, onde se diz o que destravaria.

| Não escrever | Escrever |
|---|---|
| "O preço médio no brick é R$ 32,06. Confiança média, porque o brick foi casado pelo bairro do ponto e não pela geometria: se o ponto cair num brick vizinho, o preço muda." | lente: "O preço médio no brick é R$ 32,06, contra R$ 33,26 na UF." · lacuna: "**Em qual brick o ponto cai de fato.** O casamento foi pelo nome do município, não pela geometria… Destrava com a malha de bricks." |
| "Confiança alta para as contagens, que são cadastrais." | nada — a frase não acrescenta número, comparação nem ressalva |
| "Confiança nenhuma, por ausência de dado." | o item inteiro sai da lente e vira lacuna |

Por que a nota saiu do texto: ela repetia a mesma fórmula em todo parágrafo,
quase sempre para dizer "alta", dobrava o tamanho do quadrante e ensinava o
leitor a pular justamente a frase que carregava a ressalva. Sem ela, a lente
mostra o que se sabe e a seção de lacunas mostra o que não se sabe — cada
coisa onde se procura por ela.

## O quadrante

As quatro lentes saem em matriz 2×2, em **ordem fixa**, porque numa matriz quem
informa é a posição:

|  | A favor | Contra |
|---|---|---|
| **O que o ponto já é** | Forças | Fragilidades |
| **O que pode vir a ser** | Oportunidades | Dificuldades |

Quadrante sem item **continua desenhado**, com a linha de ausência no lugar do
texto: buraco na matriz é informação, e tirar a caixa desalinha as outras três.

O parecer não decide a lente. Um número "Bom" costuma estar em Forças, mas o
quadrante continua sendo escolhido pelo que o item afirma — e um "Ruim" em
Oportunidades é possível quando o item é a alavanca contra ele. O que não se
faz é contar pareceres por quadrante, nem transformar o conjunto num juízo
sobre o ponto, a cidade ou a praça: o parecer é só do indicador.

## Tier de decisão

Nem tudo pesa igual. O dossiê abre por **Tier 1** e só desce se houver espaço.
A ordem veio do que os analistas de fato abrem (`benchmark_historico.py
--panorama`), não de opinião.

| Tier | O que é | Entra sempre? |
|---|---|---|
| **0 — barra** | zoneamento: teto de lojas, distância mínima, modelo da bandeira | sim, e se barrar o dossiê para aí |
| **1 — decide** | concorrência no raio, loja Farmarcas no raio, potencial de consumo, renda, população | sim |
| **2 — contextualiza** | REGIC, PIB, IPC do bairro, Firjan, urbanização, mix de categorias da UTC | sim, resumido |
| **3 — só se relevante** | saneamento, verticalização, educação, pirâmide etária, movimentação econômica | só se mudar a leitura de um item do Tier 1 |

---

## Forças — o que joga a favor

| Sinal | Vem de |
|---|---|
| Potencial de consumo em drogarias e gasto em medicamentos | `dados_farmacia_popular.GastosemMEDICAMENTOS`, `potencial_de_consumo` |
| Cidade puxa público de fora | `regic_2018_municipio` — hierarquia e os municípios influenciados, **nomeados e com população somada** |
| **Ponto em esquina**, com duas faces de exposição e fluxo de duas vias | `implantacao.py` — só com confiança alta |
| IPC do bairro acima da média do município | `ranking_bairros.IPC` + `RANKINGMUNICIPIO` |
| Mercado farmacêutico local crescendo | `mat_anterior_x_atual_utc_crescimento.crescimento_total` |
| Alta urbanização | `situacao_territorio_municipio.03-PopulacaoUrbana%` |
| Desenvolvimento municipal acima da mediana | `firjan_ifdm_geral.IFDM` + posição nacional |

## Fragilidades — o que joga contra

| Sinal | Vem de |
|---|---|
| **Saturação**: habitantes por farmácia na cidade vs. mediana nacional | `populacao_municipios` ÷ `dados_farmacia_popular.totalfarmaciasnacidade` |
| Concorrente grande colado no ponto | `raio_concorrencia` — `fat_medio` e distância |
| Rede nacional no raio (Raia, Drogasil, Pague Menos, São João…) | `MDM-ClassifdoPDV` |
| Classe econômica concentrada em D/E ou em A | `dados_farmacia_popular.D/E(%)`, `A(%)` |
| Renda per capita abaixo da mediana estadual | `renda_media_municipio` |
| Cidade encolhendo | `densidade_demografica.TaxadeCrescimentoDemografico(%aa)` |
| Farmarcas perdendo para o mercado na UTC | `crescimento_farmarcas` < `crescimento_sem_farmarcas` |

## Oportunidades — a vantagem que ainda está em aberto

A lente responde **uma** pergunta: o que este ponto, ou este grupo, passa a ter
aqui que hoje não tem — e que a concorrência da região não tem. É **vantagem
competitiva**, não panorama favorável. Panorama favorável é Força.

Duas famílias, e não há terceira:

| Família | A pergunta que ela responde |
|---|---|
| **Vantagem do ponto** | o que este endereço permite fazer que as farmácias do raio não fazem |
| **Jogada de praça do grupo** | o que esta abertura trava para o outro lado — ocupar a praça, fechar a vaga, tirar o espaço que outra rede ocuparia |

**Anatomia — três respostas, e sem qualquer uma delas o item não entra:**

1. **Qual é a alavanca**, escrita como ação disponível: credenciar, ocupar,
   converter, montar o mix, abrir onde ninguém abre.
2. **Quem está deixando o espaço aberto** — o concorrente, o canal, a praça ou
   o programa que ninguém da rede usa ali —, nomeado e contado.
3. **Qual é o tamanho do espaço**, com o número e a comparação de sempre.

### O teste do status quo

**Se a frase continua verdadeira sem ninguém fazer nada, não é oportunidade.**
É Força — o que o ponto já é — ou contexto, e aí normalmente já está num card.

| Escrito assim, não é oportunidade | Onde pertence |
|---|---|
| "O grupo já movimenta R$ 16,90 milhões no brick" | Forças: é o que a praça já é |
| "A mediana medida da bandeira no estado é de R$ 370 mil por mês" | lente nenhuma — é régua de referência, e o relatório já imprime os cards de receita medida |
| "O entorno é verticalizado e tem supermercado a 178 m" | Forças: descreve o entorno de hoje |

O sintoma de ter errado aqui é a **sensação de genérico**. Item que descreve o
estado atual favorável serviria a qualquer dossiê de qualquer praça onde a rede
já opera — e o leitor sente isso antes de saber nomear. Oportunidade é
específica por construção: ela nomeia o que **não está** ocupado, e num outro
endereço a frase seria falsa.

### Oportunidade não se escreve como falta nossa

O mesmo fato muda de lente conforme a redação, e uma das duas contradiz o
quadrante em que está:

| Lido como deficit — não entra | Lido como alavanca — entra |
|---|---|
| "Uma só loja da rede credenciada ao Farmácia Popular na cidade. Bom Despacho tem 24 farmácias, 16 delas credenciadas, e apenas uma loja Farmarcas entre as credenciadas." | "O credenciamento ao Farmácia Popular é alavanca disponível para este ponto: 16 das 24 farmácias da cidade já operam por ele, num município que gasta R$ 75,41 milhões em medicamentos. É a norma da praça, e o endereço entra nela no ato do credenciamento." |

A primeira redação põe a rede no banco dos réus dentro da lente **a favor** — e
é daí que vem a impressão de que o quadrante se contradiz. O fato é o mesmo; o
que muda é se a frase aponta para o buraco ou para a ação que o preenche. Se,
depois de reescrito, o item só souber falar do buraco, ele era Fragilidade.

### A lente fala da REGIÃO, nunca da própria medição

A regra que engloba todas as anteriores, e o teste é de uma linha: **qual é o
sujeito da frase?** Se for a região, o ponto, a concorrência, a cidade ou o
grupo, a frase é da lente. Se for *a base*, *o campo*, *o dado*, *a medida*,
*as duas leituras*, *a divergência* ou *este relatório*, a frase é sobre o
dossiê — e o dossiê tem outros lugares para falar de si.

| Sujeito da frase | Para onde vai |
|---|---|
| a região, o ponto, a concorrência, a cidade, o grupo | **lente** |
| a base, o campo, a camada, o dado | bloco do relatório, que já o escreve |
| a divergência, as duas leituras, a medida | **lugar nenhum** — mostre os dois números e pare |
| este relatório, esta análise, a premissa adotada | lacuna |

| Não escrever | Por quê |
|---|---|
| "Nenhuma das duas mede loja nenhuma, e a divergência entre elas é o próprio achado." | não acrescenta número nem comparação; só anuncia que o dossiê percebeu algo |
| "O grupo é apurado pelo nome do responsável no cadastro, e não pelo CNPJ." | é critério de apuração, e já está escrito por extenso na lacuna sobre grupos do cadastro |
| "O encerramento do ponto de origem é premissa deste relatório, e não consta de base nenhuma." | premissa é lacuna, e esta já existe lá |
| "quantas pessoas eles movem, nenhuma base responde" | fluxo de passantes é lacuna obrigatória, e está nela |
| "a posição se mantém alta nos dois cortes" | comenta a robustez do cálculo, não a cidade |

**Divergência entre fontes continua sendo achado — e o jeito de mostrá-la é pôr
os dois números à vista**, cada um com o nome certo. Quem lê o dossiê é analista:
vendo "a loja média do canal independente fatura R$ 69.439" e, no item seguinte,
"a faixa mais alta ocupada da cidade está dentro do raio de 300 m", ele enxerga a
tensão sozinho. Escrever "as duas discordam" rouba o espaço do número e não
acrescenta nada que o leitor já não tenha na frente.

O defeito é teimoso porque parece honestidade. Não é: é o dossiê falando de si
mesmo dentro da caixa reservada para falar do lugar.

### O mesmo número não aparece em duas lentes

Fato que corta para os dois lados fica na lente onde ele **muda mais a decisão**,
e a segunda leitura entra como oração do mesmo parágrafo. Repetido em duas
caixas do quadrante, o leitor não lê nuance: lê contradição, e passa a
desconfiar das quatro.

"18 das 26 lojas do raio são independentes" é fragilidade — o dinheiro que
circula no entorno é de loja pequena — **e** é vantagem — o concorrente típico
não tem escala de compra. Escolha a caixa e diga as duas coisas dentro dela.

### Sinais que costumam virar oportunidade legítima

| Sinal | Vem de | Por que é alavanca |
|---|---|---|
| Programa público disponível, já dominante entre os concorrentes | `dados_farmacia_popular` | credenciar é ação da loja, e o gasto do município dimensiona o espaço |
| **Share Farmarcas zero ou baixo numa UTC de receita alta** | `mat_atual_utc_market_share` + `receita_atual_total` | há receita que a rede não disputa |
| Categoria crescendo acima do mercado | `mat_anterior_x_atual_utc_mix_categorias.*_crescimento` | mix a montar que o entorno não montou |
| Bairro com IPC alto e pouca concorrência no raio | `ranking_bairros` × `raio_concorrencia` | demanda sem quem a atenda perto |
| Mercado cresce e o nº de PDVs não | `..._sem_cobertura.delta_pdvs` ≈ 0 com `crescimento` > 0 | espaço que ninguém está abrindo |
| Entorno concentrado no canal de menor escala | `faturamento_canal` + `raio_concorrencia` | retaguarda de rede compra e precifica onde o vizinho não alcança |
| **Teto de zoneamento ocupado pelo próprio solicitante** | `zoneamento.py`, perfil `existente` | enquanto ele ocupa a vaga, nenhum **outro grupo** entra na praça pela rede |

A última só existe para solicitante já associado, e precisa dizer exatamente o
que trava: a entrada de **outro grupo econômico pela rede Farmarcas** — nunca a
de concorrente de fora dela, que a regra de expansão não alcança. Escrita sem
esse recorte, ela promete um fechamento de praça que não existe.

## Dificuldades — o que o negócio vai ter de atravessar

A lente responde **uma** pergunta: o que, daqui para a frente, vai dificultar a
operação dar certo neste ponto. Obstáculo, custo, atrito, conflito ou risco de
execução — coisa que alguém vai ter de resolver para o negócio andar bem.

> **Antes desta lente, saber quem pede.** Loja Farmarcas vizinha significa
> coisas opostas conforme o solicitante — ver `zoneamento-e-perfil.md`.

**Anatomia — três respostas, e sem qualquer uma delas o item não entra:**

1. **O que vai dar trabalho**, nomeado como coisa a atravessar.
2. **Quem ou o que impõe** — a regra, o vizinho, o concorrente, o custo.
3. **O que custa se não for tratado**, com número quando houver.

### O teste do "e daí?"

**Se a resposta a "o que isso dificulta?" for "nada", não é dificuldade.** É
resultado de gate, é premissa ou é lacuna — e cada um desses já tem lugar
próprio no relatório.

O item costuma denunciar-se sozinho, na última oração. Quem **termina** em "não
restringe este pedido", "não barra", "não há o que barrar", "sem veredito para
este endereço", "não se aplica" ou "é premissa deste relatório" está dizendo,
com todas as letras, que nada ali dificulta nada — e ocupa uma caixa do
quadrante para informar que não há o que informar.

| Escrito assim, não é dificuldade | Onde pertence |
|---|---|
| "Loja do mesmo grupo desativada a 10,5 km… não ocupa vaga no teto, de modo que não restringe este pedido" | lacuna — o que decide alguma coisa é **por que** ela fechou, e isso não está em base nenhuma |
| "A distância mínima não é avaliada nesta faixa de população. Fica registrada como regra, sem veredito" | lacuna — o dossiê não avalia essa regra aqui, e é isso que se declara |
| "O encerramento do ponto de origem é premissa deste relatório" | lacuna — premissa declarada é lacuna, sempre |
| "O teto é de um grupo e o solicitante já o ocupa, então não há conflito a arbitrar" | é o resultado do gate, que tem bloco próprio no topo — e, para associado já presente, costuma ser Oportunidade |

### Fragilidade é hoje; dificuldade é o caminho

A divisa entre as duas lentes da direita não é de intensidade, é de tempo. Três
concorrentes a 23 m **são** o que o ponto é: Fragilidade. Reescrever isso como
"vai ser difícil disputar o passante com eles" é a mesma frase duas vezes, e a
segunda sem número. Só vira Dificuldade o que acrescenta **o obstáculo adiante**
— o contrato, o custo de reforma, o período com duas lojas abertas, a regra que
vai pesar na mesa de aprovação.

### Sinais que costumam virar dificuldade legítima

| Sinal | Vem de | O que, concretamente, dificulta |
|---|---|---|
| **Canibalização com loja de OUTRO associado** | `zoneamento.py`, lojas com `do_solicitante: false` | é o conflito que a regra de expansão existe para evitar, e ele vai ter de ser arbitrado por alguém |
| **Sobreposição com loja DO PRÓPRIO solicitante** | `zoneamento.py`, `do_solicitante: true` | divide o mesmo mercado entre mais pontos do mesmo dono — pode ser estratégia e continua sendo custo |
| **Alerta de zoneamento que não barrou mas pesa** | `zoneamento.py`, bloco `alertas` | entra na mesa de aprovação e precisa de resposta antes de o ponto andar |
| Cidade pequena, UTC única, mercado concentrado | `mercado_utc` + `populacao_municipios` | sobra pouco espaço para errar mix ou preço e corrigir depois |
| Período de transição com dois pontos abertos | `zoneamento.py` + perfil do solicitante | durante ele, a praça divide o mesmo mercado entre mais lojas da própria rede |

**Loja Farmarcas desativada perto saiu desta tabela.** A existência, a bandeira e
a distância são cadastrais e verdadeiras, mas não impõem nada ao pedido — loja
desativada não ocupa vaga no teto. O que mudaria uma decisão é o **motivo** do
fechamento, que não está em base nenhuma. Então o assunto inteiro é lacuna, com
a pergunta de campo junto, e não item de lente.

**Ponto em meio de quadra também saiu**: é o que o ponto já é, logo Fragilidade.

**Dois assuntos NÃO entram nesta lente**, por confiança nenhuma — e por isso
mesmo são lacuna obrigatória, não item: o **fluxo de passantes**, que não existe
em fonte alguma (ver `limites-e-vieses.md`), e o **setor censitário
indisponível no raio**, que é ausência de medida e não achado sobre o ponto.

---

## Regra de corte

Três cortes, nesta ordem:

1. **Confiança baixa ou nenhuma** → sai da lente e vira lacuna.
2. **Não muda nenhuma decisão** → não entra em lugar nenhum.
3. **Mais de ~15 itens nas quatro lentes** → o problema não é o ponto, é o
   dossiê. Cortar pelo Tier.

O primeiro corte é novo e vem antes dos outros dois: um item de confiança baixa
pode ser muito relevante, e é exatamente por isso que ele pertence à seção de
lacunas, onde se diz o que destravaria, e não à lente, onde seria lido como
coisa sabida.
