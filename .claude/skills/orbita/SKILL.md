---
name: orbita
description: Conduz a análise de região ou de ponto comercial da Farmarcas como conversa - pergunta o mínimo para fixar o ponto, roda o gate de zoneamento e os dados, e discute os números com o analista, desafiando hipótese que o dado não sustenta, explicando o que cada camada significa, dizendo se cada número é bom ou ruim contra o seu referente, transformando lacuna em pergunta e guardando o que só o empresário sabe como provocação para a conversa dele com o analista, até fechar o dossiê HTML no layout do Órbita, entregue na versão CURTA do relatório com a cópia completa gerada ao lado para conferência. Também atende quem ainda não tem ponto - a partir de uma cidade de referência, lista as praças onde a regra de expansão não barra a entrada de um grupo novo. Use quando o usuário disser 'vamos olhar essa região', 'me ajuda a analisar esse ponto', 'vale abrir aqui?', 'o que você acha dessa praça?', 'onde eu deveria olhar?', 'que praças valem olhar perto de X?', 'tô pensando em abrir um ponto', 'quero entender essa cidade', ou fornecer um endereço ou uma cidade pedindo contexto para abrir loja. Também atende o MAPEAMENTO de praças: 'vamos fazer um mapeamento', 'faz um mapeamento de X', 'quero fazer um estudo', 'faz um estudo da região', 'mapear onde dá para abrir' — e aí entrega a lista de praças, não o dossiê de ponto. O dossiê de ponto só sai com endereço; sem endereço o pedido é mapeamento, qualquer que seja a palavra usada. Do NOT use quando o pedido for pelo roteiro direto, sem conversa ('gera o dossiê completo de X', 'roda a análise desse endereço') → use /analise-regiao-farmarcas; do NOT use quando o pedido for pela versão curta SEM conversa, a partir de um endereço já decidido → use /analise-regiao-farmarcas-enxuto; do NOT use para calcular o score de viabilidade 0–20 → o dossiê não pontua, por decisão de produto; do NOT use para escrever cards do board SQO → use /orbita-user-stories; do NOT use para discovery de produto → use /product-discovery.
---

# Órbita — a análise como conversa

Mesma análise, mesmos scripts, mesmo entregável. Muda **como o analista chega
lá**: em vez de executar um roteiro que ele precisa conhecer, ele conversa, e a
conversa coleta o mínimo, roda os dados e discute os números com ele.

Esta skill **não tem scripts nem referências de domínio próprios**. Ela usa os
da `analise-regiao-farmarcas`, que continua sendo a dona das regras.

## Critical

Leia estas antes de qualquer outra coisa. Elas não cedem à conversa — a conversa
é que se organiza em volta delas.

- **Gate antes de mercado.** O zoneamento roda antes de qualquer número de
  mercado e pode encerrar a análise sozinho. Nenhum script de mercado roda antes
  do veredito sair. Com `impedimento`, o entregável é o impedimento com a regra
  citada, mais as praças onde a regra não barra — nunca o estudo do endereço
  reprovado.
- **Nenhum número sai do modelo. E, na conversa, nenhum número é adiantado.**
  Esta é a trava que a conversa ameaça: o roteiro protegia a regra porque cada
  número tinha um passo e um comando; conversando, a tentação é estimar entre uma
  rodada e outra. Pergunta que exige dado ainda não apurado se responde com **"não
  sei ainda — posso rodar X"**, seguido de rodar X. Nunca com ordem de grandeza,
  arredondamento, "deve ser por volta de" ou "costuma ser". Toda provocação que
  cita número cita número apurado **nesta sessão**.
- **Nada é pontuado — mas cada número tem parecer.** A régua de viabilidade
  0–20 pertence ao produto e tem dono. Vale para o ponto e para a praça: a lista
  de prospecção ordena por uma quantidade medida, não classifica. A conversa
  provoca e descreve — não emite veredito de viabilidade, não dá nota, não
  recomenda abrir, **não soma nem conta pareceres**. O que ela faz, por decisão
  do PM em 2026-11-27, é dizer **se cada número é bom ou ruim contra o seu
  referente** — percentil nacional, município, UF ou o anel maior —, porque a
  mesma posição é boa num indicador e ruim noutro e o analista não tem como
  saber sozinho. O rótulo sai da tabela de direção
  (`.claude/skills/analise-regiao-farmarcas/scripts/_parecer.py`): **Bom**,
  **Na média**, **Ruim** (possível dificuldade), **Ambíguo** quando a casa não
  tem direção defensável, **Sem referência** quando não há referente coerente.
  Nunca faixa absoluta, nunca número inventado. **O parecer é só do indicador,
  nunca do ponto, da cidade, da praça, do município ou da região** — não existe
  "cidade boa" ou "ponto ruim", e somar pareceres para julgar o lugar é a nota
  com outro nome; a conferência reprova as formas escritas disso.
- **Perfil e empresário não viram premissa.** Sem saber se é empresário novo ou
  já associado, o dossiê não sabe se a loja Farmarcas vizinha é conflito entre
  associados ou escolha estratégica dele. **Quem é o empresário se pergunta
  sempre, inclusive quando ele se declara novo**: o nome é o que permite checar
  se ele já está no cadastro antes de aceitar "novo" como fato. E se for já
  associado, `montar_relatorio.py` **aborta com erro fatal** sem esse nome.
  Bandeira e modelo podem virar premissa declarada; estes dois, não.
  **Empresário e responsável pelo grupo econômico são a mesma pessoa.** É uma
  pergunta só, e a resposta serve às duas coisas: o campo do cadastro se chama
  "responsável pelo GE" e é o empresário que responde pelas lojas. Perguntar
  duas vezes faz o analista repetir o nome que acabou de dar — foi o que
  aconteceu em 2026-11-24, quando a segunda resposta foi "mesma pessoa".
  **Isso vale para o dossiê de ponto, e só para ele.** No mapeamento não há
  solicitante: a vaga é calculada para um grupo novo, o documento declara que
  não sabe quem pede e não afirma nada sobre canibalização. Perguntar perfil,
  empresário, responsável pelo GE ou bandeira ali é cobrar o que o pedido ainda
  não tem — e foi o que travou a conversa em 2026-11-25, quando as três
  respostas vieram como "não tenho ainda".
- **Nome de pessoa circula na conversa e nunca no entregável.** São dois
  lugares com regras opostas, e confundi-los custa dos dois lados. **Na
  conversa, diga os nomes**: o analista precisa saber quem opera naquela cidade,
  de que grupo é a loja da esquina e se o empresário do pedido já aparece no
  cadastro — esconder isso dele tira a informação que a conversa existe para
  trazer. **No entregável, nenhum nome**: nem no HTML, nem no JSON da narrativa,
  que é arquivo versionado do repositório. O responsável pelo GE entra por
  `--ge` na linha de comando da geração, e é a conferência mecânica que verifica
  que nenhum nome do cadastro vazou para o corpo.
- **O analista não responde pelo empresário.** Pergunta que só o empresário
  sabe responder — história da praça, por que uma loja fechou ou a receita caiu,
  concorrência vista de dentro, intenção, apetite, pergunta aberta demais — **não
  vai a cartão**. Ela vira item de `provocacoes_empresario` e sai no dossiê, na
  seção "Para conversar com o empresário": o analista leva o documento a ele, e
  é lá que a resposta acontece. Alvo de 10 a 15, teto de 15. O critério é o
  **teste do respondente**, em `## Protocolo de perguntas`.
- **Pergunta sem resposta trava a fase.** Toda pergunta **ao analista** sai em
  **seletor**, uma por cartão, e nenhuma fase converge enquanto houver uma sem
  resposta explícita. Provocação ao empresário não é pergunta ao analista e não
  trava nada. "Não sei" é resposta — vira lacuna declarada; o silêncio não é. Nunca siga porque "dá para seguir": seguir sem as respostas
  entrega o dossiê que o roteiro direto já entregaria, cobrando o custo da
  conversa. Os detalhes estão em `## Protocolo de perguntas`.
- **Lacuna é conteúdo, não rodapé.** Na conversa ela vira pergunta; no documento,
  seção. Nunca é preenchida por estimativa.
- **O tom da conversa não afrouxa o documento.** Conversar é o formato do turno.
  O dossiê continua afirmativo e preciso: "a loja mais próxima está a 178 m",
  nunca "parece haver uma loja relativamente perto".

## Step 0: Read Before You Write

| Fonte | Caminho | O que extrair |
|---|---|---|
| Regras de domínio inteiras | `.claude/skills/analise-regiao-farmarcas/SKILL.md`, bloco `## Critical` | as três fontes de venda por loja, a régua de canal, MAT, loja nossa sai do cadastro, card cita fonte |
| Zoneamento e perfil | `.claude/skills/analise-regiao-farmarcas/references/zoneamento-e-perfil.md` | o gate, as faixas, as distâncias e o que a regra não diz |
| Indicadores | `.claude/skills/analise-regiao-farmarcas/references/indicadores-do-relatorio.md` | fórmula, unidade e o que o relatório não traz |
| Inventário das bases | `.claude/skills/analise-regiao-farmarcas/references/bases-orbita.md` | o que dá e o que não dá para responder |
| As quatro lentes | `.claude/skills/analise-regiao-farmarcas/references/lentes-do-dossie.md` | o quadrante SWOT, a anatomia do item, a confiança como critério de entrada |
| Benchmarks | `.claude/skills/analise-regiao-farmarcas/references/benchmarks.md` | contra o que comparar — e o que nunca serve de referência |
| Limites e vieses | `.claude/skills/analise-regiao-farmarcas/references/limites-e-vieses.md` | o que o dado não diz |
| Modelo do dossiê | `.claude/skills/analise-regiao-farmarcas/references/modelo-de-dossie.md` | estrutura do entregável |
| Provocações | `references/provocacoes.md` | o que perguntar em cima de cada camada, e a quem — analista ou empresário |
| Parecer por número | `.claude/skills/analise-regiao-farmarcas/scripts/_parecer.py` e `benchmarks.md`, seção `## Parecer por número` | a direção de cada indicador, os rótulos e o que o parecer não pode virar |
| Aprendizados | `references/learnings.md` | o que já deu errado nesta skill. Se não existir, prossiga sem ele |

## O ritmo, e onde ele vale

- **Coleta (Fases 0 e A): 1–3 perguntas por turno, uma por cartão de seletor.**
  O analista ainda não tem nada na mesa, e um bloco de dez perguntas é
  formulário. Construa cada pergunta sobre a resposta anterior, e **nunca
  pergunte o que ele já disse**.
- **Provocação (Fase C): sem cota.** O dado já está posto. Provoque o quanto ele
  exigir — uma provocação por achado que muda a leitura, nenhuma por obrigação de
  formato. Três achados, três provocações; sete achados, sete; nenhum achado,
  nenhuma, e a fase avança. O que corta não é a quantidade, é o filtro `muda:` do
  `## Protocolo de perguntas`. A restrição de legibilidade virou regra de lugar:
  toda provocação vai **em cartão de seletor**, no máximo quatro por chamada, as
  da mesma camada juntas. Passando de quatro, vão as quatro de maior
  consequência e as outras esperam o turno seguinte — a sobra não evapora.
- **Render do estado a cada turno da Fase C**, para ele corrigir antes de você
  avançar:

```
Ponto: <endereço> · <município>/<UF>   Solicitante: <novo|já associado>
Gate: <veredito>                        Já rodou: área, concorrência, mercado
Falta para fechar: <o que ainda não tem número, fonte e comparação>
Sem resposta: <os assuntos das perguntas que ficaram em aberto>
```

- **O que o analista não souber vira marcador**, nunca silêncio:
  `[SUPOR: confirmar]` quando não veio dele, `[CONFIRM: X — a decidir]` quando
  ele adiou. Diga a consequência na hora: sem bandeira não se escolhe entre 300 m
  e 500 m; sem modelo, a exigência de bandeira popular do 2º grupo na faixa de 60
  a 120 mil não é aplicada.

## Protocolo de perguntas

Governa todas as fases. Medido em 2026-11-23: perguntas diluídas na prosa depois
do gate **não foram vistas**, e a skill avançou sem elas — o dossiê saiu igual ao
do roteiro direto, pagando o custo da conversa sem a contrapartida dela.

**Onde a pergunta aparece: no seletor, sempre.** Toda pergunta vai pela
ferramenta de escolha do app (`AskUserQuestion`) — impossível de não ver,
impossível de pular, e respondida com um clique. O bloco numerado `P1/P2` está
**aposentado**: ele resolveu a pergunta que ninguém via, mas trocou o problema
por outro, medido no uso em 2026-11-25 — responder "P1 - ... / P2 - ..." é
digitar, e a conversa inteira vira parede de texto. Prosa solta continua
proibida; o bloco numerado só volta onde o seletor não estiver disponível.

**Uma pergunta por cartão.** O diálogo aceita até quatro cartões numa chamada e
cada cartão é **uma** pergunta. Nunca junte duas num cartão ("qual o modelo e
até onde você opera?"), e nunca peça resposta por número em texto. Quando as
perguntas dependem umas das outras, mande uma e espere: a resposta da primeira
muda as opções da segunda.

**As opções de todo cartão.** Até quatro, e duas delas são fixas:

| Opção | O que significa |
|---|---|
| as respostas reais | **no máximo duas**, porque o teto do app é quatro opções |
| **Não sei** | vira lacuna declarada, com o que a destravaria |
| **Recomendar** | "me ajuda a decidir" — você responde com uma recomendação |

O app acrescenta sozinho um campo de escrita livre, e **o rótulo dele não se
renomeia** — é "Outros", e é por onde o analista digita o que as opções não
cobrem. Por isso o texto da pergunta diz que dá para escrever ali, sempre que a
resposta puder ser um valor qualquer: "ou escreva a distância".

**O que "Recomendar" pode responder, e o que não pode.** Ele é um pedido de
ajuda para decidir, não um pedido de veredito. **Pode**: escolher entre as
opções do próprio cartão e dizer por quê, com o que já foi apurado nesta sessão;
dizer que raio cobre o que ele descreveu; dizer qual modelo a regra de
zoneamento favorece naquela faixa de população; dizer qual lacuna fecha mais
coisa de uma vez; dizer que o certo é rodar X antes de decidir. **Não pode**:
ordenar praças por qualidade, dizer qual conferir primeiro, dar nota, dizer se
vale abrir. A régua de viabilidade pertence ao produto e tem dono — e a lista de
praças ordena por quantidade medida justamente para não virar ranking. Se a
recomendação honesta depender de número que ainda não rodou, **a recomendação é
rodar**, não estimar.

**O que bloqueia.** Nenhuma fase converge enquanto houver pergunta sem resposta
explícita. "Não sei" e o que ele escrever **são** respostas: viram lacuna
declarada em `nao_sabe` ou `campo`, com o que a destravaria. O que não é
resposta é o cartão ignorado — aí ele volta no turno seguinte, e a Fase C não
fecha.

**Antes de tudo, o teste do respondente — a pergunta é para o analista?**
Decisão do PM em 2026-11-27: a conversa não gasta a atenção do analista com o
que ele provavelmente não sabe. O teste: **se ele responder "não sei", isso é
uma lacuna dele ou um assunto da conversa com o empresário?**

| Fica com o analista — cartão | Vai ao empresário — `provocacoes_empresario` |
|---|---|
| atributos do pedido: âncora, modelo, alcance, perfil, nome do empresário, tipo de operação, bandeira | história da praça e da rede nela: loja que fechou, receita que caiu, associado que saiu |
| recorte da análise: raio, rodar ou não uma camada, "Recomendar" | concorrência vista de dentro: quem disputa o cliente, como reagem a loja nova |
| conferência que ele faz no sistema nesta sessão: cadastro, CNPJ, endereço | intenção e apetite do empresário: formato, mix, preço de entrada, entrada do imóvel, distância que aceita |
| | fato local que só quem opera ali sabe: o bairro mudou desde 2010, o que traz gente à rua |

Pergunta aberta demais não vai a cartão: ou vira fechada e respondível, ou vai
ao empresário. E o fato **não some**: a provocação carrega o achado (número
desta sessão), a pergunta e o que a resposta muda, e sai no dossiê. Ela não
leva `muda:`, não vira cartão e não trava fase — quem vai respondê-la não está
nesta conversa. Formato e exemplos em `references/provocacoes.md`.

**Filtro de admissão — só pergunta que refina.** Toda pergunta carrega o campo
`muda:`, que agora mora na descrição da opção ou no texto do cartão, não num
sufixo de linha. Se não for possível preenchê-lo com um item de lente, uma
lacuna, uma premissa, o raio ou o gate, **a pergunta não entra**. Ficam de fora:
curiosidade sobre o lugar, confirmação do que o dado na mesa já responde,
ressalva de método (isso é lacuna, não conversa) e pedido de veredito.

**E não se pergunta o que uma etapa obrigatória posterior vai levantar.** O
dossiê não encerra a análise do ponto: depois dele vêm etapas de campo que já
são obrigatórias por processo, e o levantamento de geradores de fluxo é uma
delas. Perguntar ao analista o que aquela etapa existe para produzir devolve
trabalho a quem veio reduzi-lo, e trava a conversa esperando uma resposta que
ninguém tem agora. Esse assunto **nasce em `campo`**, com o que muda conforme o
resultado, e nunca em cartão. Medido em 2026-11-23: perguntei que equipamentos
de saúde existem em 500 m; a resposta foi "espere a etapa de geração de fluxo",
que é a resposta certa — a pergunta é que estava no lugar errado. O teste: **se
existe uma etapa do processo cujo produto é essa resposta, o item é de campo,
não de conversa.**

## Como mostrar número na conversa

Quem lê é o analista de Expansão, e o que ele recebe hoje são blocos de texto
com números dentro. **Camada que é conjunto de números não vai em prosa.**

| O que você tem | Como mostra |
|---|---|
| 3 ou mais linhas comparáveis (praças, concorrentes, faixas) | **tabela markdown** na sua resposta |
| série, distribuição, composição, percentil | **gráfico**, por `show_widget` |
| um ou dois números | **frase** — gráfico de duas barras é enfeite |
| um número contra um limite (saturação, teto) | frase com a comparação junto |
| um número contra um referente (percentil, município, UF, anel maior) | frase com a comparação **e o parecer**: "percentil 6 de renda — ruim, no terço de baixo do país" |

**A tabela vai na resposta, nunca dentro do widget** — é o próprio guia da
ferramenta que manda isso, e tabela em markdown já sai legível. O widget é para
o gráfico.

**A leitura continua ao lado do desenho.** O gráfico substitui o despejo de
números, não a frase que diz o que aquilo significa — "ensinar a camada enquanto
mostra" é a razão de esta skill existir, e um gráfico sem leitura devolve ao
analista o trabalho de interpretar sozinho, que é exatamente o que ele já faz
hoje.

**E aqui a trava de número fica por sua conta.** A conferência mecânica lê o
dossiê, não a conversa: nada confere o que você desenha num gráfico. Por isso,
no desenho:

- **só entra valor que saiu de script nesta sessão**, igual ao resto;
- **nenhuma conta dentro do widget** além de arredondar e formatar. Percentual,
  diferença, média e razão calculados em JavaScript são número do modelo com
  outra roupa;
- **nenhuma ordenação que vire ranking de qualidade.** Barra ordenada por
  mercado não atendido é a medida; barra ordenada por "melhor praça" é a régua
  que tem dono;
- **a fonte vai no texto que acompanha**, como em qualquer número desta skill.

## Abertura

Sem contexto nenhum, abra assim — e só assim:

> Vou montar o dossiê desta região com você. Funciona em quatro tempos: fixo o
> ponto, rodo o gate de zoneamento, trago os números e converso em cima deles, e
> no fim gero o relatório em HTML. Começo com o que você tem: **um endereço, uma
> cidade, ou nem isso** — se ainda não há ponto, eu levanto as praças onde a
> regra de expansão não barra a entrada.

Com contexto parcial, abra confirmando o que já entendeu em bullets e pergunte
**só o que falta**.

**O que decide o caminho é o endereço, não a palavra usada.**

| O que veio | Para onde vai |
|---|---|
| endereço, ou endereço + coordenada | Fase A → dossiê de ponto |
| "mapeamento", "estudo", "mapear", com ou sem cidade | Fase 0 → lista de praças |
| só cidade, só região, ou nada | Fase 0 → lista de praças |

Cidade sem endereço **não** é caso de dossiê: numa cidade de centenas de
milhares de habitantes, a média entre um bairro central e um periférico não
descreve nenhum dos dois. Diga isso e vá para a Fase 0 — não ofereça um perfil
de cidade como se fosse análise de ponto.

## Fase 0 — Mapeamento de praças *(sempre que não houver endereço)*

**Objetivo:** sair de "onde eu deveria olhar?" para 1 a 3 praças escolhidas.

**Pergunte o mínimo, e não é o do dossiê.** Aqui não há solicitante: só entram
a **âncora** e o **modelo**.

- **A âncora é obrigatória.** Sem coordenada de referência, a lista é função da
  UF e não do pedido — medido em 2026-11-05, Pouso Alegre e Ipatinga, 390 km
  entre si, receberam listas idênticas, 15 de 15. A primeira pergunta é **"a
  partir de onde?"**, e a resposta aceitável é uma cidade de referência, não só
  uma UF. Com a cidade em mãos, a coordenada sai do cache de centroides da
  própria apuração — centroide aproximado pela mediana das farmácias da cidade,
  que vai declarado como tal.
- **O modelo:** convencional ou popular, em cartão. Com Não sei e Recomendar —
  na faixa de 60 a 120 mil habitantes a regra exige que o 2º grupo seja popular,
  e dizer isso é recomendação legítima, não veredito.
- **O alcance é pergunta, não premissa sua.** Pergunte até onde ele aceita
  operar, em cartão, com estas opções:

  | Opção | O que faz |
  |---|---|
  | **Só nesta cidade** | `--so-municipio <CODIGO_IBGE>` — as regiões do próprio município |
  | **Até 15 km** | `--raio-km 15` |
  | **Não sei** | fica com 15 km, declarado como premissa, e vira lacuna |
  | **Recomendar** | você responde com a distância que cobre o que ele descreveu |

  No campo de escrita livre ele digita qualquer distância — diga isso no texto
  do cartão. **Raio grande responde outra pergunta:** de 80 km para cima a lista
  vira a da região, e ordenar por mercado absoluto devolve sempre a cidade
  maior. Medido em 2026-11-25: a 80 km de Amélia Rodrigues, sete das doze linhas
  eram Salvador.

**"Só nesta cidade" não é raio pequeno, e o script trata separado.** A distância
da lista vai de centroide de município a centroide de município, então **todas**
as regiões da cidade de referência estão à mesma distância — nenhum raio separa
uma região dela da outra, e um raio curto pega a cidade inteira ou não pega
nada. Por isso o recorte é por código IBGE. Duas consequências a dizer ao
analista:

- a coluna de distância sai **0 km em todas as linhas**, porque é a distância da
  cidade até ela mesma — não é a distância do bairro ao centro;
- **lista curta ou vazia é a resposta**, e o script não cai para a UF inteira
  como faz quando um raio devolve menos de três praças. Vazia significa que
  nenhuma região da cidade alcança o piso de R$ 5 milhões de receita de mercado,
  ou que a regra não deixa entrar grupo novo em nenhuma — e o caminho então é o
  dossiê de um ponto da cidade, que roda o gate sobre um endereço.

**Não pergunte perfil, empresário, responsável pelo GE nem bandeira.** Nenhum
dos quatro muda uma linha desta lista: a vaga é sempre calculada para grupo
novo, e a régua de distância mínima só existe sobre um endereço. Perguntá-los
devolve trabalho a quem veio reduzi-lo. O documento declara que não sabe quem
pede, e por isso não afirma nada sobre canibalização.

```
python .claude/skills/analise-regiao-farmarcas/scripts/alternativas.py \
  --uf <UF> --perto-de <LAT>,<LNG> \
  <--raio-km 15 | --so-municipio CODIGO_IBGE> \
  --modelo <popular|convencional> --so-disponiveis --limite 12 \
  --perfil-municipios
```

`--raio-km` e `--so-municipio` são recortes concorrentes e o script recusa os
dois juntos. No JSON da narrativa, "só nesta cidade" é `"so_municipio": true`,
que exige `codigo_ibge` — e aí a faixa do documento diz "somente neste
município" em vez do raio.

`--perfil-municipios` acrescenta, na **mesma saída**, o perfil em percentis das
cidades da lista. Continua sendo **um script só** — não acrescente uma segunda
chamada para obter camada municipal.

Converse em cima da lista: por que esta praça e não aquela, o que é mercado não
atendido, o que "cabe no teto" significa e o que não significa.

**Convergência:** 1 a 3 praças escolhidas, cada uma com a razão dita. A escolha
e a razão dela são **prosa em `leitura`** — filtrar linhas da tabela para mostrar
só as escolhidas seria o modelo decidindo quais números o documento mostra.

**A entrega é igual à do dossiê: enxuta para circular, completa ao lado.** O
`--detalhes` vale neste formato — a enxuta tira a seção Fontes e mantém o bloco
"O que esta lista é, e o que ela não é", as lacunas e os itens de campo. Aquele
bloco é conteúdo, não aparato: sem ele a lista que circula é lida como
recomendação de abertura.

```
python .claude/skills/analise-regiao-farmarcas/scripts/montar_relatorio.py \
  --config outputs/dossies/<arquivo>.json \
  --saida  outputs/dossies/<arquivo>.html --detalhes ocultos

python .claude/skills/analise-regiao-farmarcas/scripts/montar_relatorio.py \
  --config outputs/dossies/<arquivo>.json \
  --saida  outputs/dossies/<arquivo>-completo.html --detalhes abertos
```

**Provocações ao empresário no mapeamento: só quando há empresário.** Sem
solicitante — o caso comum aqui — não há com quem conversar, e o campo
`provocacoes_empresario` fica vazio. Quando o mapeamento é feito para um
empresário conhecido, o que só ele sabe (até onde aceita operar, por que saiu
de uma praça, que formato pretende) vai para o campo, no mesmo formato do
dossiê, e sai na seção "Para conversar com o empresário".

**Entregue a enxuta renderizada**, para abrir sozinha no painel lateral, e rode
a conferência mecânica sobre a completa. Depois **ofereça** abrir o dossiê de
uma das praças — oferta, nunca invocação automática, e ela só anda quando
houver endereço.

**Todo número deste documento tem de estar na apuração DELE.** Este formato roda
um script só, o de praças — e continua rodando, mesmo depois do painel. A
fronteira do que você pode citar são **duas** listas, e nada fora delas:

- **da linha da praça:** população do Censo, potencial de consumo, captura,
  preço médio, receita da praça e receita da rede nela;
- **do perfil por cidade:** os indicadores das quatro dimensões, cada um com o
  valor, o percentil nacional, a mediana nacional, o número de municípios
  comparados e o **parecer** que o painel imprime ao lado, mais o papel na rede
  urbana.

Número municipal que você leu em `contexto_municipio.py` ou em `mercado_utc.py`
durante a conversa **continua sem procedência aqui** — medido em 2026-11-25,
dezesseis números caíram assim na conferência, e foi por não existir camada
municipal apurada neste formato. Agora existe: use o painel, não a memória da
conversa.

**Na conferência, o casamento fraco vai ficar longo.** Percentil é inteiro
abaixo de 100 e sem unidade, então toda citação de percentil cai lá. A regra
está certa e não se mexe nela. O que muda é como se lê: achado cujo caminho
começa com `perfil_dos_municipios` confere-se pelo **par cidade + indicador**,
não pelo número solto.

**Travas desta fase:**
- Ordenação é por mercado não atendido, que é quantidade medida. **Não vire
  ranking de "melhor praça".**
- **O painel de perfil por cidade dá parecer por número e não compõe.** Desde
  2026-11-27 cada indicador sai com Bom / Na média / Ruim, ou Ambíguo / Sem
  referência — diga-o na leitura, é ele que poupa o analista de saber se
  percentil 28 é bom ou ruim naquele indicador. Mas não some percentis nem
  pareceres, não tire média, não conte dimensões "ganhas" nem indicadores
  "bons", e não diga "lidera em três das quatro" —
  é a mesma composição proibida, escrita por extenso, e o verificador reprova.
  Dentro de uma dimensão os indicadores podem apontar em direções opostas, e é
  esse contraste que vale conversar.
- **O percentil compara a cidade com o Brasil, nunca com as outras da lista.**
  Quatro ou doze casos não são uma distribuição. "A cidade com maior percentil
  de renda desta lista" é ranking com outro nome.
- **A ordem do painel é alfabética.** Dizer "a primeira do painel" é citar o
  alfabeto, não um achado.
- **A unidade do painel é o município; a da tabela, a unidade territorial.** A
  mesma cidade aparece uma vez num e várias no outro, e nenhum indicador do
  painel distingue uma região da outra dentro da mesma cidade.
- O raio é premissa declarada, não medida. Nenhuma fonte diz a que distância um
  empresário aceita operar.
- "Cabe no teto" é ausência de impedimento na contagem de grupos, **não
  liberação**: o gate de verdade roda sobre um endereço.
- A vaga é calculada para grupo **novo**. Se o solicitante já opera naquela
  praça, declare que a leitura é outra — o script não sabe quem perguntou.

## Fase A — Ancoragem

**Objetivo:** fixar o ponto e obter o que o gate exige.

Pergunte 1–3 por turno, **uma por cartão de seletor**, como manda o
`## Protocolo de perguntas`. O que esta fase precisa coletar:

| Pergunta | Opções do cartão |
|---|---|
| empresário novo ou já associado | as duas · Não sei · Recomendar |
| **quem é o empresário** | escrita livre — diga no texto que é para digitar o nome |
| ponto novo, mudança de ponto ou conversão | as três · Não sei |
| popular ou convencional | as duas · Não sei · Recomendar |
| bandeira pretendida | escrita livre · Não sei · Recomendar |

**O empresário se pergunta sempre**, inclusive quando o perfil é novo — ver
`references/zoneamento-e-perfil.md`, seção 1. **É uma pergunta só**: empresário
e responsável pelo grupo econômico são a mesma pessoa, e perguntar as duas faz
ele repetir o nome. Com o nome em mãos, confira contra o cadastro antes de
aceitar "novo" como fato. **Diga o que achou, com nome**: a conversa é o lugar
onde nome de pessoa circula. O entregável não é.

**Sem coordenada não há raio.** Com só a cidade, diga que o resultado é perfil de
cidade — não disfarce.

```
python .claude/skills/analise-regiao-farmarcas/scripts/contexto_municipio.py --municipio "<NOME>" --uf <UF>
```

O código IBGE sai daí. **Nunca de memória**: código errado traz a população de
outra cidade e muda a faixa de zoneamento inteira.

**Convergência:** `lat`, `lng`, `municipio`, `uf` e `codigo_ibge` resolvidos;
perfil respondido; nome do empresário em mãos — ele é o `--ge` da geração se o
perfil for `existente`.

## Fase B — Gate de zoneamento

```
python .claude/skills/analise-regiao-farmarcas/scripts/zoneamento.py --lat <LAT> --lng <LNG> \
  --municipio "<NOME>" --uf <UF> --codigo-ibge <CODIGO> \
  --bandeira "<BANDEIRA>" --modelo <popular|convencional> \
  --perfil <novo|existente> [--ge "<responsável>"]
```

Comunique o veredito em uma frase, com a regra citada. Não é pergunta, é fato.

- `impedimento` → pule a Fase C. Vá para a D no formato de impedimento, e
  converse sobre praças alternativas — nunca sobre o mercado do ponto barrado.
  O impedimento também leva `provocacoes_empresario`: o que só o empresário sabe
  sobre a loja da rede que ocupa a vaga, o motivo do pedido e as praças onde a
  regra não barra.
- `alerta` → siga, com o alerta em destaque.
- `liberado` → siga.
- `indeterminado` → resolva a população do Censo antes de continuar.

**Convergência:** veredito conhecido e dito ao analista.

## Fase C — Leitura com provocação

Rode o pacote de dados **de uma vez** — a lista completa de comandos está no
Step 3 de `.claude/skills/analise-regiao-farmarcas/SKILL.md` — e traga os números
para a mesa. A conversa acontece em cima deles, não antes.

**Leia cada saída inteira antes de transformá-la em lente.** Cortar com `head`
ou fatiar a string serve para conferir que o script rodou; nunca para decidir o
que entra no dossiê. Medido em 2026-11-19: truncar as saídas escondeu uma
categoria inteira de geradores de fluxo — um calçadão a 56 m do ponto — e fez
uma lente afirmar o contrário do que o dado mostrava, além de deixar de fora o
indicador de saturação e os percentis nacionais que a apuração já traz prontos.

Três movimentos — e eles se dividem entre **o corpo do turno** e **os cartões de
pergunta**. Medido em 2026-11-23: provocação colada em cada camada, espalhada
por um turno longo, vira garimpo e não é respondida.

**Traga as camadas desenhadas.** Este é o turno mais denso da conversa, e é onde
a regra de `## Como mostrar número na conversa` mais pesa: praças, concorrentes,
faixas etárias e percentis vão em tabela ou gráfico, com a leitura ao lado.

Fica no corpo, junto do número:

1. **Ensinar a camada enquanto mostra — com o parecer.** Todo número que tem
   referente sai dizendo se é bom ou ruim **para aquele indicador**, pelo rótulo
   da tabela de direção (`_parecer.py`): Bom, Na média, Ruim, Ambíguo ou Sem
   referência, com uma linha de porquê. É o caminho direto para reduzir o
   conhecimento prévio exigido do analista, que é o objetivo do produto — e é
   afirmação, não pergunta, então fica onde o número está. No dossiê, o item da
   lente leva o campo `parecer` (`{"indicador": ..., "percentil": N}` ou
   `{"indicador": ..., "posicao": "acima|abaixo", "referente": "..."}`) e o
   rótulo sai do script. Indicador fora da tabela sai "Sem referência" — não
   invente direção.

Vai para os cartões de pergunta, cada um dizendo de que camada saiu — **só se
passar no teste do respondente**:

2. **Desafiar a hipótese que o dado não sustenta.** "Você está contando com o
   fluxo da avenida, e isso não está em base nenhuma — como você checaria?"
3. **Transformar lacuna em pergunta.** "Ninguém sabe o fluxo aqui — vale uma
   contagem em campo antes de seguir?"

Vai para `provocacoes_empresario`, sem cartão e sem travar a fase:

4. **Guardar para o empresário o que só ele sabe.** Cada achado cuja pergunta
   reprovou no teste do respondente vira um item com `tema`, `achado`,
   `pergunta` e `o_que_muda`. Diga ao analista, em uma linha, quantas ficaram
   guardadas para a conversa com o empresário — e siga. Alvo de 10 a 15, teto
   de 15: passando disso, ficam as de maior consequência.

Os cartões seguem a ordem em que as camadas foram apresentadas, e os da mesma
camada ficam juntos. Cada um com o `muda:` preenchido — sem ele, a pergunta não
entra. No máximo quatro por chamada; o resto espera o turno seguinte.

Leia `references/provocacoes.md` para o que perguntar em cima de cada camada.

Para cada item candidato à lente, exija os três campos escritos: **número**,
**fonte de dado** em campo próprio e **comparação**. A confiança é critério de
corte e **nunca vira texto**: afirmação de confiança baixa ou sem dado desce
para lacuna, e o limite de método de item de confiança média vira lacuna também.

**Convergência:** as quatro lentes com itens de três campos (e `parecer` onde
o número tem referente), cortadas por confiança e tier até caber em ~15 itens,
mais `nao_sabe` e `campo` não vazios, `provocacoes_empresario` com 10 a 15
itens —
e **nenhum cartão sem resposta explícita**. Com pendência, a fase não fecha:
reapresente as pendentes.

**Ao fechar, mostre o que montou — e só então pergunte.** Não gere sozinho, e
não pergunte no escuro: perguntar "gero ou quer puxar mais algum assunto?" logo
depois do turno mais denso da conversa faz o analista decidir sem ver o que
está decidindo. A ordem é esta, nesta sequência:

1. **Escreva a narrativa em JSON** (formato na Fase D), acrescentando os dois
   campos que só o resumo usa:

```json
"resumo_gate": "frase única com o veredito do gate e a regra citada",
"resumo_perguntas": [
  {"titulo": "a pergunta, em uma frase", "texto": "o que muda conforme a resposta"}
]
```

   `montar_relatorio.py` ignora os dois. A narrativa vem antes do resumo, não
   depois: é o que faz todo número do resumo ser, por construção, um número que
   a conferência mecânica já confere.

2. **Gere o resumo**, que é HTML e sai de script — pelo mesmo motivo que o
   dossiê:

```
python .claude/skills/analise-regiao-farmarcas/scripts/resumo_fechamento.py \
  --config outputs/dossies/<arquivo>.json \
  --saida  outputs/dossies/<arquivo>-resumo.html
```

3. **Entregue o arquivo renderizado**, para que abra sozinho no painel lateral, e
   pergunte pelo diálogo: gerar o dossiê agora, ou puxar mais um assunto antes.

O script monta a ficha do ponto, o quadrante com os títulos dos itens de cada
lente (com o rótulo do parecer, quando houver), as lacunas e os itens de campo
pela primeira frase de cada um, o bloco "O que vai para a conversa com o
empresário" e a seção de perguntas. Ele avisa quando `resumo_gate` ou `resumo_perguntas` faltam.

**A seção "Onde ainda cabe pergunta" é a que justifica o resumo existir.** As
outras descrevem; essa convida. O analista acabou de responder um bloco de
perguntas e tende a ler o fechamento como formalidade — nomear onde uma resposta
dele ainda mudaria o documento é o que transforma "pode gerar" em revisão de
verdade. Escolha as duas ou três lacunas de maior consequência, e diga em cada
uma o que muda conforme a resposta.

**O resumo não cria número, e agora isso é estrutural.** Ele é renderizado a
partir do JSON, então não há onde o modelo formatar número sozinho — era
exatamente o buraco do resumo escrito à mão, que ficava fora do alcance da
conferência. O que você escreve no JSON é o que o resumo mostra.

**O resumo não é o entregável e não pode parecer um.** O script marca a faixa de
pré-leitura no topo e no rodapé, dizendo que o documento ainda passa pela
conferência e pelo auditor. Nunca circule o resumo no lugar do dossiê: ele não
tem seção de Fontes e não foi auditado.

## Fase D — Dossiê

A narrativa já foi escrita no fim da Fase C, antes do resumo de fechamento —
aqui você gera a partir dela. Os formatos estão documentados no topo de
`montar_relatorio.py` — três: gate liberado/alerta, gate impedimento e
prospecção (`"tipo": "prospeccao"`).

**Se o analista puxou mais um assunto no fechamento**, volte à Fase C, converse,
emende o JSON e **gere o resumo de novo** antes de perguntar. Resumo
desatualizado é pior que resumo nenhum: ele descreve um documento que não é mais
o que vai sair. Como ele é renderizado do JSON, regerar é um comando.

**Esta skill entrega a cópia enxuta, e gera as duas.** São o mesmo JSON e a
mesma rodada de scripts; muda só o modo. A enxuta é o entregável porque a
conversa já cumpriu, turno a turno, o papel que a seção de Fontes cumpre no
documento: o analista viu cada número aparecer e perguntou de onde veio. A
completa continua obrigatória porque é sobre ela que a conferência roda —
`--detalhes ocultos` tira a tabela de Fontes inteira, e sobre a enxuta o
auditor reprovaria tudo por falta de procedência.

```
python .claude/skills/analise-regiao-farmarcas/scripts/montar_relatorio.py \
  --config outputs/dossies/<arquivo>.json \
  --saida  outputs/dossies/<arquivo>.html \
  --detalhes ocultos \
  [--ge "<responsável>"]

python .claude/skills/analise-regiao-farmarcas/scripts/montar_relatorio.py \
  --config outputs/dossies/<arquivo>.json \
  --saida  outputs/dossies/<arquivo>-completo.html \
  --detalhes abertos \
  [--ge "<responsável>"]
```

Depois, sempre, a conferência mecânica **sobre a cópia completa**, e só então o
auditor, também sobre ela:

```
python .claude/skills/analise-regiao-farmarcas/scripts/verificar_dossie.py \
  --config    outputs/dossies/<arquivo>.json \
  --relatorio outputs/dossies/<arquivo>-completo.html \
  --ge "<responsável usado na geração>"
```

Corrija **no JSON** e gere as duas de novo até fechar limpo. **Nunca edite o
HTML à mão** — é saída de script. Depois passe pelo subagente
`(⌕) auditor-de-evidencia`, apontando-o para o `-completo.html`.

Entregue a enxuta e diga, em uma linha, que a completa está ao lado dela para
quem precisar conferir um número. **A enxuta é o que o analista leva ao
empresário**: é nela que a seção "Para conversar com o empresário" vira roteiro
da reunião. O que **não** sai da enxuta: "O que este
dossiê NÃO sabe" e "Para confirmar em campo" continuam lá — lacuna é conteúdo,
não aparato de conferência.

## Racionalizações que não valem

| Tentação | Por que não |
|---|---|
| "Já tenho contexto para montar as lentes a partir do primeiro input" | o que você tem são suposições suas, não o contexto dele; item sem número, fonte e comparação não entra |
| "Vou perguntar tudo de uma vez na coleta, para ser eficiente" | conversa é processo de pensamento; o bloco de dez perguntas é o formulário que esta skill existe para substituir |
| "Já provoquei três coisas, guardo o resto para não cansar" | se o dado sustenta o achado, ele sai neste turno — achado adiado é achado perdido |
| "Não achei nada relevante, mas preciso provocar alguma coisa" | provocação sem achado por trás é ruído, e ensina o analista a ignorar as próximas |
| "Posso adiantar a ordem de grandeza enquanto o script roda" | é exatamente assim que número do modelo entra no dossiê; diga "não sei ainda" e rode |
| "É só uma subtração entre dois números apurados, posso escrever o resultado" | o resultado não está em saída nenhuma e a conferência o reprova — em 2026-11-19 caíram assim um "5,6%" de `100 − 94,37`, um "doze vezes" de uma razão errada e um "100 m" que eram 103 m |
| "Li o começo da saída e já entendi o que ela diz" | o achado que decide costuma estar depois do corte: um calçadão a 56 m ficou fora de um dossiê por isso |
| "Ele já é associado, sigo sem o nome do responsável" | o gerador aborta, e antes disso a prosa já estaria afirmando de quem é cada loja sem ter apurado |
| "Ele perguntou do mercado, respondo antes do gate" | gate é gate: ponto barrado não tem análise de mercado, e adiantá-la sugere que há número a negociar |
| "Ele só quer saber onde olhar, rodo a lista sem âncora" | sem âncora a lista é a da UF e devolve a capital para qualquer pedido — medido |
| "Ele deu a cidade, então dá para montar o dossiê dela" | sem endereço não há raio, e numa cidade grande a média entre bairro central e periferia não descreve nenhum dos dois; é mapeamento, e diga por quê |
| "No mapeamento pergunto o perfil e a bandeira, para já adiantar" | nenhum dos dois muda uma linha da lista, e em 2026-11-25 as respostas vieram como "não tenho ainda" — perguntar ali é cobrar o que o pedido não tem |
| "Li o número no contexto do município, posso citar na lista de praças" | a apuração da prospecção tem uma chamada só; número de outro script não tem procedência nela e a conferência reprova — use o que a linha da praça traz |
| "A praça está no topo da lista, logo é a melhor" | a ordem é por mercado não atendido, que é uma quantidade medida, não uma nota |
| "A lente está com 2 itens, está bom" | lente rasa esconde o que decide; corte por tier até ~15 itens, não por cansaço |
| "Ele não respondeu, mas dá para seguir" | é a falha medida em 2026-11-23: a skill avançou sem as respostas e entregou o dossiê do roteiro direto, cobrando o custo da conversa |
| "Pergunto no meio do parágrafo, fica mais natural" | pergunta no meio da prosa não foi vista em teste; o lugar dela é o cartão de seletor |
| "Mando as perguntas numeradas em texto, que cabe mais" | responder "P1 - ... / P2 - ..." é digitação, e o analista disse isso em 2026-11-25; cartão se responde com um clique |
| "Junto duas perguntas num cartão só, para economizar" | o cartão tem uma resposta; duas perguntas nele devolvem metade da informação e você não sabe qual metade |
| "Ele pediu recomendação, digo qual praça vale mais a pena" | recomendar caminho de análise é ajuda; ordenar praça por qualidade é a régua que tem dono, e foi removida à mão de dois relatórios |
| "Desenho o gráfico com a conta feita no JavaScript" | conta no widget é número do modelo com outra roupa, e a conferência não enxerga a conversa |
| "São três números, faço um gráfico para ficar bonito" | gráfico de duas ou três barras é enfeite; três linhas comparáveis são tabela, um número é frase |
| "Pergunto ao analista por que a receita da rede caiu, ele deve saber" | quem sabe é o empresário; o analista responde "não sei", a fase trava e o fato some do documento — vai para `provocacoes_empresario` |
| "Pergunta aberta sobre a concorrência rende conversa" | rende "não sei"; ou vira pergunta fechada que o analista responde, ou vai ao empresário |
| "Guardo trinta provocações para o empresário, assim nada se perde" | lista longa vira questionário; alvo de 10 a 15, teto de 15 |
| "Percentil 28 fala por si" | não fala: é bom num indicador e ruim noutro, e é exatamente o que o analista não sabe — diga o parecer |
| "Três indicadores bons e um ruim: dá para dizer que a praça é boa" | é a nota com outro nome; o parecer é só do indicador, nunca do lugar, e a conferência reprova contagem, saldo e juízo sobre ponto, cidade ou praça |
| "A cidade é boa" / "o ponto é ruim" / "essa praça é favorável" | o rótulo fala de um número contra o referente dele, não do lugar |
| "Escrevo 'Bom' no parecer, o indicador não está na tabela mas é óbvio" | sem direção declarada o rótulo é palpite; sai "Sem referência", e a direção nova entra na tabela por decisão do PM |
| "Essa pergunta é interessante, mesmo sem mudar nada" | pergunta que não muda item, lacuna ou premissa gasta a atenção das que mudam |
| "Renumero as perguntas a cada turno" | ele responde por número; renumerar quebra a resposta dele |
| "Pergunto se pode gerar sem mostrar o que montei" | ele acabou de atravessar o turno mais denso da conversa e vai responder "pode" por cansaço; sem ver as lentes e as lacunas, a autorização não é revisão |
| "Escrevo o resumo à mão, que é mais rápido que preencher os dois campos" | à mão ele fica fora do alcance da conferência, e bem diagramado passa a parecer entregável — o pior dos dois mundos para a trava de número |
| "Deixo `resumo_perguntas` vazio, as lacunas já estão listadas" | lista de lacuna descreve; a seção de perguntas convida, e é a única parte do resumo que pede resposta. Sem ela o analista responde "pode gerar" por cansaço, que é a falha que o resumo existe para evitar |
| "Ele pediu mais um assunto, gero o dossiê e aviso depois" | o resumo que ele aprovou descrevia outro documento; emende o JSON, regrave o resumo e pergunte de novo |
| "Pergunto o que a etapa de campo vai levantar, para adiantar" | se existe uma etapa obrigatória cujo produto é essa resposta, perguntar devolve trabalho a quem veio reduzi-lo; o item nasce em `campo` |
| "Ele se declarou empresário novo, não preciso do nome" | novo é o que ele diz ser, e o cadastro é quem confirma |
| "Pergunto o empresário e depois o responsável pelo GE" | são a mesma pessoa; a segunda pergunta só faz ele repetir o nome |
| "Não digo o nome do grupo na conversa, por LGPD" | a regra é sobre o entregável; na conversa o analista precisa saber quem opera na cidade, e escondê-lo tira a informação que a conversa existe para trazer |
| "Gero só a enxuta, que é o que ele vai circular" | a conferência e o auditor rodam sobre a completa, onde está a tabela de Fontes; sem ela, o auditor reprova tudo por falta de procedência |
| "Gero só a completa e ofereço a enxuta se ele pedir" | nesta skill a enxuta é o entregável, não uma oferta — a conversa já fez o papel que a seção de Fontes faz no documento |
| "A conversa foi boa, escrevo o dossiê em markdown" | o entregável é sempre HTML gerado por script — markdown à mão reabre a porta para número que o modelo formatou sozinho |

## Antes de considerar terminado

Não dê a tarefa por encerrada enquanto todos estes não forem verdade:

- [ ] **No mapeamento:** âncora, modelo e alcance perguntados, e **nada** de
      perfil, empresário, GE ou bandeira
- [ ] **No mapeamento:** se o alcance foi "só nesta cidade", o documento diz que
      a distância de 0 km é da cidade até ela mesma, e lista curta não virou
      lista da UF
- [ ] **No mapeamento:** todo número do documento existe na apuração dele, que
      tem uma chamada de script só
- [ ] **No dossiê de ponto:** há endereço com coordenada — sem isso o pedido era
      mapeamento
- [ ] Perfil do solicitante e nome do empresário perguntados — **uma pergunta
      só**, porque o empresário é o responsável pelo GE
- [ ] "Empresário novo" conferido contra o cadastro, não aceito só pela
      declaração do solicitante
- [ ] Gate rodado **antes** de qualquer script de mercado, e veredito comunicado
- [ ] Todo número do documento existe numa saída de script desta sessão
- [ ] Nenhum número foi dito na conversa sem script por trás
- [ ] As quatro lentes com número, fonte e comparação em cada item — ou, no impedimento, `leitura`, `o_que_mudaria` e `alertas_cadastro`
- [ ] `nao_sabe` e `campo` preenchidos, cada lacuna dizendo o que falta, por que importa e o que destravaria
- [ ] Nenhuma nota de confiança escrita no texto
- [ ] Nenhum nome de pessoa no entregável, e `ge` vazio no JSON
- [ ] O dossiê não pontuou, não deu nota e não recomendou
- [ ] `verificar_dossie.py` fechou sem reprovação
- [ ] Nenhuma pergunta ficou sem resposta explícita; as não respondidas viraram
      lacuna dizendo o que destravaria
- [ ] Toda pergunta saiu em cartão de seletor, uma por cartão, com `muda:`
      preenchido — nenhuma em prosa solta nem numerada em texto
- [ ] Todo cartão trouxe **Não sei**, e **Recomendar** onde cabia recomendação
- [ ] Nenhum cartão perguntou ao analista o que só o empresário sabe — passou
      no teste do respondente
- [ ] `provocacoes_empresario` com 10 a 15 itens (teto 15), cada um com achado
      desta sessão, pergunta e o que muda, sem nome de pessoa
- [ ] Todo número com referente saiu com parecer — na conversa e, no dossiê,
      no campo `parecer` do item — e nenhum parecer foi somado, contado ou
      usado para ordenar praça
- [ ] Camada com três ou mais linhas comparáveis foi mostrada em tabela ou
      gráfico, com a leitura ao lado
- [ ] Nenhum número desenhado num gráfico veio de conta feita no widget
- [ ] O resumo de fechamento foi gerado em `<arquivo>-resumo.html` e entregue
      renderizado, com `resumo_gate` e `resumo_perguntas` preenchidos no JSON
- [ ] O script do resumo não emitiu aviso de campo faltando
- [ ] O analista foi avisado de que estava pronto e **autorizou** a geração

## Para onde mandar o que não é desta skill

- Roteiro direto, sem conversa → `/analise-regiao-farmarcas`
- Relatório curto a partir de um endereço já decidido, sem conversa →
  `/analise-regiao-farmarcas-enxuto` (esta skill já entrega a versão curta; o
  que a outra faz é chegar nela pelo roteiro direto)
- Cards do board SQO → `/orbita-user-stories`
- Discovery de produto → `/product-discovery`
- Escolher fornecedor de dado para uma camada vazia → subagente `(⚑_⚑) estrategista-fontes-dados`
- Dúvida se o dossiê fala a língua de quem decide → subagente `(◔◡◔) analista-expansao`
