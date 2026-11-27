# O que perguntar em cima de cada camada

Banco de provocações da Fase C. Não é roteiro: escolha pela camada que o dado
fez falar, e ignore o resto. Nenhuma pergunta daqui vale antes de o número
estar na mesa.

Cada camada tem **dois destinos**, e a diferença é quem sabe a resposta
(decisão do PM em 2026-11-27):

- **Ao analista** — cartão de seletor na conversa. Só o que ele sabe ou decide
  agora: atributos do pedido, recorte da análise, o que ele confere no sistema.
- **Ao empresário** — item de `provocacoes_empresario`, que sai no dossiê na
  seção "Para conversar com o empresário". O analista leva o documento ao
  empresário, e é lá que essas perguntas são respondidas.

## A regra que governa todas

Uma provocação só existe se tiver um **achado** atrás dela. Achado é um número
apurado nesta sessão que muda a leitura — alto demais, baixo demais, divergente
de outra fonte, ou ausente onde se esperava haver. Sem achado, não provoque:
ruído ensina o analista a ignorar as próximas.

E nenhuma provocação cita número que não saiu de script nesta sessão. Se a
pergunta exigir um dado que você não tem, a frase é **"não sei ainda — posso
rodar X"**, e aí você roda.

## O teste do respondente — para quem vai a pergunta

Antes de escrever o cartão, pergunte-se: **se o analista responder "não sei",
isso é uma lacuna dele ou um assunto da conversa com o empresário?**

| Vai ao analista (cartão) | Vai ao empresário (`provocacoes_empresario`) |
|---|---|
| atributo do pedido: perfil, nome do empresário, bandeira, modelo, tipo de operação, âncora, alcance | história da praça e da rede nela: por que a loja fechou, por que a receita caiu, quem saiu |
| recorte da análise: raio, rodar ou não uma camada, "Recomendar" | concorrência vista de dentro: quem disputa o cliente de verdade, como reagem a uma loja nova |
| o que ele confere no sistema nesta sessão: cadastro, CNPJ, endereço | intenção e apetite: formato, mix, preço de entrada, entrada do imóvel, distância que aceita operar |
| | fato local que só quem opera ali sabe: o bairro mudou desde 2010, o que traz gente à rua |

Pergunta **aberta demais** ("o que você acha da concorrência aqui?") não vai a
cartão nenhum: ou vira pergunta fechada que o analista responde, ou vira
provocação ao empresário. O item que uma etapa obrigatória de campo vai
produzir continua indo para `campo` — nem cartão, nem empresário.

**Onde cada uma sai, e o que precisa carregar.**

- **Cartão ao analista:** em **cartão de seletor** (`AskUserQuestion`), um por
  pergunta, marcada com a camada de origem e com o campo `muda:` preenchido — o
  que no dossiê depende da resposta. Todo cartão traz **Não sei**, e
  **Recomendar** quando houver recomendação honesta a dar. Sem `muda:` a
  pergunta não entra. As regras completas estão em `## Protocolo de perguntas`,
  no `SKILL.md` desta skill.
- **Provocação ao empresário:** objeto em `provocacoes_empresario` com `tema`
  (a camada ou lente), `achado` (o número apurado nesta sessão que motiva a
  pergunta), `pergunta` (curta, para ser dita em voz alta na reunião) e
  `o_que_muda` (o que a resposta muda na leitura). **Não vira cartão e não trava
  fase.** Alvo de **10 a 15** por dossiê, teto de 15 — passou disso, ficam as de
  maior consequência. Escreva sem nome de pessoa ("o empresário", "o outro
  associado") e sem tom de veredito: é convite a contar o que ele sabe.

A leitura da camada (o que o indicador significa, contra o que se compara, e o
**parecer** — se o número é bom ou ruim para aquele indicador) continua no
corpo, junto do número: aquilo é afirmação, não pergunta.

## Três formas, e quando cada uma cabe

| Forma | Quando usar | Exemplo |
|---|---|---|
| **Desafiar a hipótese** | o analista afirmou algo que nenhuma base sustenta | "você está contando com o fluxo da avenida — isso não está em base nenhuma; como você checaria?" |
| **Ensinar enquanto mostra** | o número só significa algo contra uma referência | "a renda no raio está acima da do município; num ponto de bairro isso costuma empurrar o mix para perfumaria, e não para genérico — é o que você espera vender aqui?" |
| **Lacuna como pergunta** | o que falta muda a decisão | "ninguém sabe quanta gente passa aqui; vale uma contagem em campo antes de seguir, ou o ponto se decide sem isso?" |

---

## População e densidade no raio

**O que é:** moradores e domicílios dos setores censitários que caem no raio,
rateados pela fração de área de cada setor dentro do círculo.

**O que não é:** gente que passa. E **é Censo 2010** — as camadas setoriais do
acervo são de 2010, conferido na pessoa contra a API do IBGE. O número sai
subestimado, com o teto do erro na diferença entre os dois censos do município.

**Ao empresário:**
- "Esse número é de 2010. Essa parte da cidade cresceu desde então? Se cresceu
  na borda e não aqui, o erro é pequeno; se verticalizou, é grande."
- "Moradores não são passantes. O que traz gente a esta rua que não mora aqui?"

**Vira lacuna quando:** o analista não souber dizer se a região mudou. Escreva a
defasagem com a direção do viés, nunca reescale por fator municipal.

## Renda

**O que é:** rendimento médio por habitante e por domicílio dos setores no raio,
em média ponderada.

**Cuidado maior do acervo:** a **unidade** dos campos de renda não foi apurada.
Se vierem nominais de 2010, lê-los como reais de hoje é erro de ordem de
grandeza, não de 13%.

**Parecer:** renda é indicador em que mais é melhor — acima do município ou no
terço de cima do país é "Bom"; abaixo, "Ruim" (`_parecer.py`).

**Ao empresário:**
- "A renda do raio está [acima/abaixo] da do município. É esse o cliente que
  você espera no balcão?"
- Divergência entre o que o dado diz e o que o empresário conta é informação,
  não erro a resolver escolhendo um dos dois — vira lacuna com as duas leituras.

**Vira lacuna sempre:** a unidade da renda é lacuna obrigatória enquanto não
houver apuração própria.

## Potencial de consumo

**O que é:** demanda estimada de drogarias na área, com split entre
Medicamentos e Higiene/Beleza/Nutrição.

**O que não é:** venda realizada, nem venda capturável. É quanto a população
daquela área tende a gastar, não quanto uma loja ali fatura.

**Ao empresário:**
- "Potencial alto com concorrência instalada é disputa, não espaço livre. Quem
  já está capturando isso hoje?"
- "O split entre medicamento e higiene combina com o mix que você pretende?"

## Concorrência no raio

**Três fontes, e elas não medem a mesma coisa** — leia o `## Critical` da skill
base antes de falar de faturamento de concorrente.

- A **faixa de faturamento** da camada de concorrentes é rótulo de faixa, não
  medida por loja: o campo assume oito valores em toda a base e está preenchido
  em menos da metade dos cadastros. Diga "a faixa mediana ocupada", nunca "o
  faturamento dos vizinhos".
- A **régua de canal** é medida, e diz quanto fatura a **loja média do canal
  naquele estado** — nunca a farmácia da esquina.
- A **receita das lojas do grupo** é medida e casa por CNPJ.

**Ao analista (cartão):**
- "O cadastro mostra loja da rede aqui perto e o vínculo não fechou pelo nome.
  Confere pelo CNPJ se é do próprio solicitante?" — é conferência de sistema,
  e a resposta muda de efeito econômico para conflito.

**Ao empresário:**
- "São N farmácias no raio. Quais delas disputam o seu cliente de verdade?"
- "A loja mais próxima está a X m e é de bandeira Y. Como ela reage quando abre
  farmácia perto?"
- "Que farmácias abriram ou fecharam por aqui nos últimos anos, e por quê?"

**Vira lacuna quando:** a loja casou por nome de bandeira e não por CNPJ — aí é
suspeita a confirmar, e vai rotulada como tal.

## Zoneamento

**O que é:** gate. O teto conta **grupos econômicos**, não lojas, e o grupo sai
do responsável registrado no cadastro, comparado por nome e não por CNPJ.

**Ao analista (cartão):**
- "A contagem de grupos é por nome. Vale conferir pelo CNPJ se duas lojas são do
  mesmo dono — grafia divergente inventa um grupo e barra um pedido que caberia."

**Ao empresário:**
- "A cidade tem mais lojas que o número da faixa, mas todas do mesmo grupo: não
  barra, e divide o mesmo mercado. Isso muda o seu apetite aqui?"
- Abaixo de 60 mil habitantes, a distância mínima **não é avaliada**: declare
  como regra sem veredito, nunca como pergunta econômica de canibalização.

## Geradores de fluxo no entorno

**O que é:** equipamentos num raio de 500 m — hospitais, escolas, creches,
mercados —, do OpenStreetMap.

**O que não é:** fluxo de passantes. Contagem de equipamentos é proxy fraco, e
ausência no mapa não é ausência no mundo: a cobertura é irregular fora dos
grandes centros.

**Ao empresário** (o levantamento de geradores é etapa de campo; o que vai
aqui é o que ele sabe da rotina da rua):
- "O mapa não encontrou nada em volta. Isso costuma ser falha de mapeamento, não
  deserto — o que traz gente a esta quadra?"
- "Esses geradores funcionam no mesmo horário que a loja vai funcionar?"

## Implantação na quadra

**O que é:** esquina ou meio de quadra, pela malha viária.

**Regra de saída:** só afirme com confiança alta. Sem isso, **omita o assunto** —
não escreva que não foi possível determinar.

**Ao empresário, quando houver classificação:**
- "Esquina tem duas faces de exposição. A entrada vai ficar para qual via?"

## Preço médio por unidade e mercado da região

**O que é:** preço por unidade no brick e mercado farmacêutico da unidade
territorial.

**O que não é:** nem um nem outro é deste endereço. Não se sabe em qual brick o
ponto cai — o casamento é por município e bairro —, e em cidade grande a
unidade territorial é o agregado do município, não a vizinhança.

**Parecer:** para bandeira popular, preço abaixo da referência é "Bom"; para
convencional a casa não tem direção, e o parecer sai "Ambíguo".

**Ao empresário:**
- "Esse preço é da região, não deste quarteirão. Você vai entrar com a régua de
  preço da rede ou com o preço da praça?"

## Praças alternativas

**O que é:** praças onde a regra não barra a entrada de um grupo novo, ordenadas
pelo mercado que circula sem passar pela rede.

**A armadilha:** mercado grande sem a rede pode ser oportunidade **ou praça já
testada e perdida**. A coluna de presença mostra qual dos dois — receita da rede
em queda é o segundo caso.

**Ao empresário:**
- "A rede já opera nessa praça e a receita dela caiu. O que você sabe do que
  aconteceu lá?"
- "Essa praça está a X km. Você aceita operar a essa distância?"

---

## Provocações que não valem

| Tentação | Por que não |
|---|---|
| "O que você acha desses números?" | devolve a pergunta sem oferecer leitura; o analista veio para reduzir o trabalho dele, não para aumentá-lo |
| "Esse ponto parece bom para você?" | é pedido de veredito, e esta skill não pontua nem recomenda |
| Perguntar algo que o dado na mesa já responde | gasta a atenção que o achado real precisa |
| Provocar sobre camada que não rodou | toda provocação cita número apurado nesta sessão |
| "Deve ter uns X mil moradores aí" | número do modelo; diga "não sei ainda" e rode o script |
| Listar cinco ressalvas de método seguidas | ressalva de método é lacuna, não conversa; a conversa é sobre o lugar |
| Pergunta sem o campo `muda:` preenchido | se você não sabe dizer o que muda no dossiê conforme a resposta, ela não refina nada e rouba a atenção das que refinam |
| Provocação no meio do parágrafo da camada | medido em 2026-11-23: espalhadas pelo turno, não foram respondidas; o lugar é o cartão de seletor |
| Provocação numerada em texto, para responder por P1/P2 | medido em 2026-11-25: responder por número é digitação, e a conversa vira parede de texto |
| Perguntar ao analista o que só o empresário sabe | ele responde "não sei", a fase trava esperando quem não está na conversa, e o fato some do documento; o lugar é `provocacoes_empresario` (PM, 2026-11-27) |
| "O que você acha da concorrência aqui?" ao analista | pergunta aberta demais: ou vira fechada e respondível, ou vai ao empresário |
| Trinta provocações ao empresário "para não perder nada" | lista longa vira questionário e o empresário responde as três primeiras; alvo de 10 a 15, teto de 15 |
| Provocação ao empresário sem achado atrás | a regra que governa todas vale aqui também: sem número apurado, é curiosidade |
