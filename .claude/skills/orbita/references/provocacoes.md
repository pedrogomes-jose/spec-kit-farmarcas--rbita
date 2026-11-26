# O que perguntar em cima de cada camada

Banco de provocações da Fase C. Não é roteiro: escolha pela camada que o dado
fez falar, e ignore o resto. Nenhuma pergunta daqui vale antes de o número
estar na mesa.

## A regra que governa todas

Uma provocação só existe se tiver um **achado** atrás dela. Achado é um número
apurado nesta sessão que muda a leitura — alto demais, baixo demais, divergente
de outra fonte, ou ausente onde se esperava haver. Sem achado, não provoque:
ruído ensina o analista a ignorar as próximas.

E nenhuma provocação cita número que não saiu de script nesta sessão. Se a
pergunta exigir um dado que você não tem, a frase é **"não sei ainda — posso
rodar X"**, e aí você roda.

**Onde ela sai, e o que precisa carregar.** A provocação não fica colada na
camada: ela nasce em **cartão de seletor** (`AskUserQuestion`), um por pergunta,
marcada com a camada de origem e com o campo `muda:` preenchido — o que no dossiê
depende da resposta. Todo cartão traz **Não sei**, e **Recomendar** quando houver
recomendação honesta a dar. Sem esse campo a pergunta não entra. A leitura da camada
(o que o indicador significa, contra o que se compara) continua no corpo, junto
do número: aquilo é afirmação, não pergunta. As regras completas estão em
`## Protocolo de perguntas`, no `SKILL.md` desta skill.

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

**Provoque:**
- "Esse número é de 2010. Essa parte da cidade cresceu desde então? Se cresceu
  na borda e não aqui, o erro é pequeno; se verticalizou, é grande."
- "Moradores não são passantes. O que você espera que traga gente aqui que não
  mora na área?"

**Vira lacuna quando:** o analista não souber dizer se a região mudou. Escreva a
defasagem com a direção do viés, nunca reescale por fator municipal.

## Renda

**O que é:** rendimento médio por habitante e por domicílio dos setores no raio,
em média ponderada.

**Cuidado maior do acervo:** a **unidade** dos campos de renda não foi apurada.
Se vierem nominais de 2010, lê-los como reais de hoje é erro de ordem de
grandeza, não de 13%.

**Provoque:**
- "A renda do raio está acima ou abaixo da do município — e isso bate com o que
  você viu no lugar?"
- "Divergência entre o que o dado diz e o que o campo mostra aqui é informação,
  não erro a resolver escolhendo um dos dois."

**Vira lacuna sempre:** a unidade da renda é lacuna obrigatória enquanto não
houver apuração própria.

## Potencial de consumo

**O que é:** demanda estimada de drogarias na área, com split entre
Medicamentos e Higiene/Beleza/Nutrição.

**O que não é:** venda realizada, nem venda capturável. É quanto a população
daquela área tende a gastar, não quanto uma loja ali fatura.

**Provoque:**
- "Potencial alto com concorrência instalada é disputa, não espaço livre. Quem
  já está capturando isso?"
- "O split entre medicamento e higiene combina com a bandeira pretendida?"

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

**Provoque:**
- "São N farmácias no raio. Quantas você viu de fato quando esteve lá?"
- "A loja mais próxima está a X m e é de bandeira Y. Isso é concorrência direta
  ou o público é outro?"
- "O cadastro mostra loja da rede aqui perto. É do próprio solicitante ou de
  outro associado? A resposta muda de efeito econômico para conflito."

**Vira lacuna quando:** a loja casou por nome de bandeira e não por CNPJ — aí é
suspeita a confirmar, e vai rotulada como tal.

## Zoneamento

**O que é:** gate. O teto conta **grupos econômicos**, não lojas, e o grupo sai
do responsável registrado no cadastro, comparado por nome e não por CNPJ.

**Provoque:**
- "A cidade tem mais lojas que o número da faixa, mas todas do mesmo grupo: não
  barra, e divide o mesmo mercado. Isso muda o seu apetite aqui?"
- "A contagem de grupos é por nome. Vale conferir pelo CNPJ se duas lojas são do
  mesmo dono — grafia divergente inventa um grupo e barra um pedido que caberia."
- Abaixo de 60 mil habitantes, a distância mínima **não é avaliada**: declare
  como regra sem veredito, nunca como pergunta econômica de canibalização.

## Geradores de fluxo no entorno

**O que é:** equipamentos num raio de 500 m — hospitais, escolas, creches,
mercados —, do OpenStreetMap.

**O que não é:** fluxo de passantes. Contagem de equipamentos é proxy fraco, e
ausência no mapa não é ausência no mundo: a cobertura é irregular fora dos
grandes centros.

**Provoque:**
- "O mapa não encontrou nada em volta. Isso costuma ser falha de mapeamento, não
  deserto — o que existe ali que você viu?"
- "Esses geradores funcionam no mesmo horário da loja?"

## Implantação na quadra

**O que é:** esquina ou meio de quadra, pela malha viária.

**Regra de saída:** só afirme com confiança alta. Sem isso, **omita o assunto** —
não escreva que não foi possível determinar.

**Provoque, quando houver classificação:**
- "Esquina tem duas faces de exposição. A entrada vai ficar para qual via?"

## Preço médio por unidade e mercado da região

**O que é:** preço por unidade no brick e mercado farmacêutico da unidade
territorial.

**O que não é:** nem um nem outro é deste endereço. Não se sabe em qual brick o
ponto cai — o casamento é por município e bairro —, e em cidade grande a
unidade territorial é o agregado do município, não a vizinhança.

**Provoque:**
- "Esse preço é da região, não deste quarteirão. O perfil daqui é mais caro ou
  mais barato que o da cidade?"

## Praças alternativas

**O que é:** praças onde a regra não barra a entrada de um grupo novo, ordenadas
pelo mercado que circula sem passar pela rede.

**A armadilha:** mercado grande sem a rede pode ser oportunidade **ou praça já
testada e perdida**. A coluna de presença mostra qual dos dois — receita da rede
em queda é o segundo caso.

**Provoque:**
- "A rede já opera nessa praça e a receita dela caiu. Vale entender por que antes
  de colocá-la na frente da fila."
- "Essa praça está a X km. O solicitante aceita operar a essa distância?"

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
