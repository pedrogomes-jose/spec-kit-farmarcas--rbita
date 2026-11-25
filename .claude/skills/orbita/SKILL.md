---
name: orbita
description: Conduz a análise de região ou de ponto comercial da Farmarcas como conversa - pergunta o mínimo para fixar o ponto, roda o gate de zoneamento e os dados, e discute os números com o analista, desafiando hipótese que o dado não sustenta, explicando o que cada camada significa e transformando lacuna em pergunta, até fechar o dossiê HTML no layout do Órbita, entregue na versão CURTA do relatório com a cópia completa gerada ao lado para conferência. Também atende quem ainda não tem ponto - a partir de uma cidade de referência, lista as praças onde a regra de expansão não barra a entrada de um grupo novo. Use quando o usuário disser 'vamos olhar essa região', 'me ajuda a analisar esse ponto', 'vale abrir aqui?', 'o que você acha dessa praça?', 'onde eu deveria olhar?', 'que praças valem olhar perto de X?', 'tô pensando em abrir um ponto', 'quero entender essa cidade', ou fornecer um endereço ou uma cidade pedindo contexto para abrir loja. Também atende o MAPEAMENTO de praças: 'vamos fazer um mapeamento', 'faz um mapeamento de X', 'quero fazer um estudo', 'faz um estudo da região', 'mapear onde dá para abrir' — e aí entrega a lista de praças, não o dossiê de ponto. O dossiê de ponto só sai com endereço; sem endereço o pedido é mapeamento, qualquer que seja a palavra usada. Do NOT use quando o pedido for pelo roteiro direto, sem conversa ('gera o dossiê completo de X', 'roda a análise desse endereço') → use /analise-regiao-farmarcas; do NOT use quando o pedido for pela versão curta SEM conversa, a partir de um endereço já decidido → use /analise-regiao-farmarcas-enxuto; do NOT use para calcular o score de viabilidade 0–20 → o dossiê não pontua, por decisão de produto; do NOT use para escrever cards do board SQO → use /orbita-user-stories; do NOT use para discovery de produto → use /product-discovery.
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
- **Nada é pontuado.** A régua de viabilidade 0–20 pertence ao produto e tem
  dono. Vale para o ponto e para a praça: a lista de prospecção ordena por uma
  quantidade medida, não classifica. A conversa provoca e descreve — não emite
  veredito de viabilidade, não dá nota, não recomenda abrir.
- **Perfil, empresário e responsável pelo GE não viram premissa.** Sem saber se
  é empresário novo ou já associado, o dossiê não sabe se a loja Farmarcas
  vizinha é conflito entre associados ou escolha estratégica dele. **Quem é o
  empresário se pergunta sempre, inclusive quando ele se declara novo**: grupo
  econômico é o empresário que responde pelas lojas, a contagem do teto
  deduplica por nome e não por CNPJ, e sem o nome não há como checar se ele já
  está no cadastro com outra grafia — o erro que barra pedido que caberia. E se
  for já associado, `montar_relatorio.py` **aborta com erro fatal** sem o
  responsável pelo GE. Bandeira e modelo podem virar premissa declarada; estes
  três, não.
  **Isso vale para o dossiê de ponto, e só para ele.** No mapeamento não há
  solicitante: a vaga é calculada para um grupo novo, o documento declara que
  não sabe quem pede e não afirma nada sobre canibalização. Perguntar perfil,
  empresário, responsável pelo GE ou bandeira ali é cobrar o que o pedido ainda
  não tem — e foi o que travou a conversa em 2026-11-25, quando as três
  respostas vieram como "não tenho ainda".
- **Nome de pessoa nunca entra em entregável.** O responsável pelo GE entra por
  linha de comando na geração, nunca gravado no JSON.
- **Pergunta sem resposta trava a fase.** Toda pergunta sai numerada, no bloco
  final do turno, e nenhuma fase converge enquanto houver uma sem resposta
  explícita. "Não sei" e "pula" são respostas — viram lacuna declarada; o
  silêncio não é. Nunca siga porque "dá para seguir": seguir sem as respostas
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
| Provocações | `references/provocacoes.md` | o que perguntar em cima de cada camada |
| Aprendizados | `references/learnings.md` | o que já deu errado nesta skill. Se não existir, prossiga sem ele |

## O ritmo, e onde ele vale

- **Coleta (Fases 0 e A): 1–3 perguntas por turno.** O analista ainda não tem
  nada na mesa, e um bloco de dez perguntas é formulário. Construa cada pergunta
  sobre a resposta anterior, e **nunca pergunte o que ele já disse**.
- **Provocação (Fase C): sem cota.** O dado já está posto. Provoque o quanto ele
  exigir — uma provocação por achado que muda a leitura, nenhuma por obrigação de
  formato. Três achados, três provocações; sete achados, sete; nenhum achado,
  nenhuma, e a fase avança. O que corta não é a quantidade, é o filtro `muda:` do
  `## Protocolo de perguntas`. A restrição de legibilidade virou regra de lugar:
  toda provocação sai **numerada, no bloco final do turno**, e as da mesma camada
  ficam adjacentes.
- **Render do estado a cada turno da Fase C**, para ele corrigir antes de você
  avançar:

```
Ponto: <endereço> · <município>/<UF>   Solicitante: <novo|já associado>
Gate: <veredito>                        Já rodou: área, concorrência, mercado
Falta para fechar: <o que ainda não tem número, fonte e comparação>
Perguntas abertas: P3, P7
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

**Onde a pergunta aparece.** Nunca no meio da prosa. Toda pergunta aberta sai num
bloco único, sempre o **último** do turno:

```
### Perguntas — responda por número

P1. [Concorrência] <pergunta>   · muda: <o que no dossiê depende da resposta>
P2. [População] <pergunta>      · muda: <...>
```

Os números são **estáveis na sessão**: P3 continua sendo P3 no turno seguinte, e
o turno seguinte reapresenta **só as pendentes**, com os mesmos números.
Renumerar quebra a resposta de quem responde por número.

**O que bloqueia.** Nenhuma fase converge enquanto houver pergunta sem resposta
explícita. "Não sei", "pula" e "depois" **são** respostas válidas: viram lacuna
declarada em `nao_sabe` ou `campo`, com o que a destravaria. O que não é resposta
é o silêncio — respondeu P1 e P2 e ignorou P3, o turno seguinte abre
reapresentando P3, e a Fase C não fecha.

**Filtro de admissão — só pergunta que refina.** Toda pergunta carrega o campo
`muda:` escrito. Se não for possível preenchê-lo com um item de lente, uma
lacuna, uma premissa, o raio ou o gate, **a pergunta não entra**. Ficam de fora:
curiosidade sobre o lugar, confirmação do que o dado na mesa já responde,
ressalva de método (isso é lacuna, não conversa) e pedido de veredito.

**E não se pergunta o que uma etapa obrigatória posterior vai levantar.** O
dossiê não encerra a análise do ponto: depois dele vêm etapas de campo que já
são obrigatórias por processo, e o levantamento de geradores de fluxo é uma
delas. Perguntar ao analista o que aquela etapa existe para produzir devolve
trabalho a quem veio reduzi-lo, e trava a conversa esperando uma resposta que
ninguém tem agora. Esse assunto **nasce em `campo`**, com o que muda conforme o
resultado, e nunca no bloco de perguntas. Medido em 2026-11-23: perguntei que
equipamentos de saúde existem em 500 m; a resposta foi "espere a etapa de
geração de fluxo", que é a resposta certa — a pergunta é que estava no lugar
errado. O teste: **se existe uma etapa do processo cujo produto é essa
resposta, o item é de campo, não de conversa.**

**Fechada vai por diálogo.** Pergunta com conjunto de opções conhecido — perfil
novo ou já associado, popular ou convencional, ponto novo/mudança/conversão, raio
de 300 m ou 500 m, gerar o dossiê ou puxar mais um assunto — usa a ferramenta de
escolha do app (`AskUserQuestion`): impossível de não ver, impossível de pular.
Pergunta aberta — bandeira pretendida, o que ele viu em campo, hipótese a
desafiar — vai pelo bloco numerado. Onde o diálogo não estiver disponível, ela
cai no bloco numerado; **nunca** em prosa solta.

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
- **O modelo, por diálogo:** convencional ou popular. É a única pergunta fechada
  desta fase.
- **O alcance é premissa sua até ele dizer o contrário.** Declare o raio que
  usou e pergunte a que distância o empresário aceitaria operar — a resposta
  muda quais praças entram antes de a lista ser ordenada.

**Não pergunte perfil, empresário, responsável pelo GE nem bandeira.** Nenhum
dos quatro muda uma linha desta lista: a vaga é sempre calculada para grupo
novo, e a régua de distância mínima só existe sobre um endereço. Perguntá-los
devolve trabalho a quem veio reduzi-lo. O documento declara que não sabe quem
pede, e por isso não afirma nada sobre canibalização.

```
python .claude/skills/analise-regiao-farmarcas/scripts/alternativas.py \
  --uf <UF> --perto-de <LAT>,<LNG> --raio-km 150 \
  --modelo <popular|convencional> --so-disponiveis --limite 12 \
  --perfil-municipios
```

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
  valor, o percentil nacional, a mediana nacional e o número de municípios
  comparados, mais o papel na rede urbana.

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
- **O painel de perfil por cidade não compõe.** Não some percentis, não tire
  média, não conte dimensões "ganhas" e não diga "lidera em três das quatro" —
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

Pergunte 1–3 por turno, pelo canal que o `## Protocolo de perguntas` manda.
**Por diálogo**, porque o conjunto de opções é conhecido: empresário novo ou já
associado · popular ou convencional · ponto novo, mudança de ponto ou conversão.
**Pelo bloco numerado**, porque são abertas: endereço ou cidade · bandeira
pretendida · **quem é o empresário** · responsável pelo GE, se já associado.

**O empresário se pergunta sempre**, inclusive quando o perfil é novo — ver
`references/zoneamento-e-perfil.md`, seção 1. Com o nome em mãos, confira se ele
já aparece no cadastro antes de aceitar "novo" como fato: o grupo deduplica por
nome normalizado, e grafia divergente inventa ou funde grupo. O nome serve à
apuração e **nunca entra no entregável**.

**Sem coordenada não há raio.** Com só a cidade, diga que o resultado é perfil de
cidade — não disfarce.

```
python .claude/skills/analise-regiao-farmarcas/scripts/contexto_municipio.py --municipio "<NOME>" --uf <UF>
```

O código IBGE sai daí. **Nunca de memória**: código errado traz a população de
outra cidade e muda a faixa de zoneamento inteira.

**Convergência:** `lat`, `lng`, `municipio`, `uf` e `codigo_ibge` resolvidos;
perfil respondido; responsável pelo GE em mãos se o perfil for `existente`.

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

Três movimentos — e eles se dividem entre **o corpo do turno** e **o bloco final
de perguntas**. Medido em 2026-11-23: provocação colada em cada camada, espalhada
por um turno longo, vira garimpo e não é respondida.

Fica no corpo, junto do número:

1. **Ensinar a camada enquanto mostra.** O que é bom ou ruim naquele indicador
   naquele contexto, com a comparação junto. É o caminho direto para reduzir o
   conhecimento prévio exigido do analista, que é o objetivo do produto — e é
   afirmação, não pergunta, então fica onde o número está.

Vai para o bloco numerado no fim do turno, cada item marcado com a camada de onde
saiu:

2. **Desafiar a hipótese que o dado não sustenta.** "Você está contando com o
   fluxo da avenida, e isso não está em base nenhuma — como você checaria?"
3. **Transformar lacuna em pergunta.** "Ninguém sabe o fluxo aqui — vale uma
   contagem em campo antes de seguir?"

O bloco segue a ordem em que as camadas foram apresentadas, e as perguntas da
mesma camada ficam adjacentes. Cada uma com o campo `muda:` preenchido — sem ele,
a pergunta não entra.

Leia `references/provocacoes.md` para o que perguntar em cima de cada camada.

Para cada item candidato à lente, exija os três campos escritos: **número**,
**fonte de dado** em campo próprio e **comparação**. A confiança é critério de
corte e **nunca vira texto**: afirmação de confiança baixa ou sem dado desce
para lacuna, e o limite de método de item de confiança média vira lacuna também.

**Convergência:** as quatro lentes com itens de três campos, cortadas por
confiança e tier até caber em ~15 itens, mais `nao_sabe` e `campo` não vazios —
e **nenhuma pergunta do bloco sem resposta explícita**. Com pendência, a fase não
fecha: reapresente as pendentes com os mesmos números.

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
lente, as lacunas e os itens de campo pela primeira frase de cada um, e a seção
de perguntas. Ele avisa quando `resumo_gate` ou `resumo_perguntas` faltam.

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
quem precisar conferir um número. O que **não** sai da enxuta: "O que este
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
| "Pergunto no meio do parágrafo, fica mais natural" | pergunta no meio da prosa não foi vista em teste; o lugar dela é o bloco final, numerada |
| "Essa pergunta é interessante, mesmo sem mudar nada" | pergunta que não muda item, lacuna ou premissa gasta a atenção das que mudam |
| "Renumero as perguntas a cada turno" | ele responde por número; renumerar quebra a resposta dele |
| "Pergunto se pode gerar sem mostrar o que montei" | ele acabou de atravessar o turno mais denso da conversa e vai responder "pode" por cansaço; sem ver as lentes e as lacunas, a autorização não é revisão |
| "Escrevo o resumo à mão, que é mais rápido que preencher os dois campos" | à mão ele fica fora do alcance da conferência, e bem diagramado passa a parecer entregável — o pior dos dois mundos para a trava de número |
| "Deixo `resumo_perguntas` vazio, as lacunas já estão listadas" | lista de lacuna descreve; a seção de perguntas convida, e é a única parte do resumo que pede resposta. Sem ela o analista responde "pode gerar" por cansaço, que é a falha que o resumo existe para evitar |
| "Ele pediu mais um assunto, gero o dossiê e aviso depois" | o resumo que ele aprovou descrevia outro documento; emende o JSON, regrave o resumo e pergunte de novo |
| "Pergunto o que a etapa de campo vai levantar, para adiantar" | se existe uma etapa obrigatória cujo produto é essa resposta, perguntar devolve trabalho a quem veio reduzi-lo; o item nasce em `campo` |
| "Ele se declarou empresário novo, não preciso do nome" | novo é o que ele diz ser, o cadastro é quem confirma — e a contagem do teto deduplica por nome, onde uma grafia divergente barra pedido que caberia |
| "Gero só a enxuta, que é o que ele vai circular" | a conferência e o auditor rodam sobre a completa, onde está a tabela de Fontes; sem ela, o auditor reprova tudo por falta de procedência |
| "Gero só a completa e ofereço a enxuta se ele pedir" | nesta skill a enxuta é o entregável, não uma oferta — a conversa já fez o papel que a seção de Fontes faz no documento |
| "A conversa foi boa, escrevo o dossiê em markdown" | o entregável é sempre HTML gerado por script — markdown à mão reabre a porta para número que o modelo formatou sozinho |

## Antes de considerar terminado

Não dê a tarefa por encerrada enquanto todos estes não forem verdade:

- [ ] **No mapeamento:** âncora e modelo perguntados, e **nada** de perfil,
      empresário, GE ou bandeira
- [ ] **No mapeamento:** todo número do documento existe na apuração dele, que
      tem uma chamada de script só
- [ ] **No dossiê de ponto:** há endereço com coordenada — sem isso o pedido era
      mapeamento
- [ ] Perfil do solicitante e nome do empresário perguntados, e responsável pelo
      GE em mãos se já associado
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
- [ ] Toda pergunta feita tinha o campo `muda:` preenchido, e nenhuma saiu solta
      no meio da prosa
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
