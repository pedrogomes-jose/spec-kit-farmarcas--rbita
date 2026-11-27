# Aprendizados — skill `orbita`

Uma entrada por rodada de uso real. Formato: data · o que funcionou · o que não
funcionou · caso de borda. Marque a procedência quando a entrada **não** vier de
uso real — aprendizado de teste e aprendizado de campo não valem o mesmo.

---

## 2026-11-27 — o analista não responde pelo empresário, e todo número ganha parecer

`PROCEDENCIA: decisão do PM (Pedro), em duas mensagens de 2026-11-27. Não é
aprendizado de uso: é mudança de produto, a ser observada nas próximas rodadas.`

- **Pergunta que só o empresário sabe saiu da conversa e entrou no dossiê.** A
  skill perguntava ao analista coisas que ele provavelmente não sabe — por que a
  receita da rede caiu, quem disputa o cliente de verdade, se o bairro mudou
  desde 2010, se o solicitante aceita operar a X km. A resposta era "não sei", a
  fase travava esperando quem não estava na conversa, e o fato — relevante —
  sumia do documento como lacuna genérica. Agora vale o **teste do
  respondente**: se o "não sei" do analista é assunto da conversa com o
  empresário, a pergunta vira item de `provocacoes_empresario` (tema, achado,
  pergunta, o que muda) e sai na seção "Para conversar com o empresário". Alvo
  de 10 a 15, teto de 15 — o PM pediu explicitamente para não virar lista de
  30 ou 40.
- **O dossiê agora vai ao empresário.** A regra antiga dizia que ele não ia. O
  PM decidiu o contrário: o analista apresenta o documento ao empresário, e as
  provocações existem para essa conversa. Nome de pessoa continua fora.
- **Parecer por número.** "Percentil 28" não dizia ao analista se era bom ou
  ruim, e a resposta depende do indicador. Cada número com referente passa a
  sair com **Bom / Na média / Ruim**, ou **Ambíguo / Sem referência**, pela
  tabela de direção em `analise-regiao-farmarcas/scripts/_parecer.py`. O corte
  é por tercil da distribuição (posição, não valor absoluto); o que muda entre
  indicadores é a direção. Sem score, sem recomendação, sem soma nem contagem de
  pareceres — o conferidor reprova "três indicadores bons", "saldo positivo" e
  "maioria dos indicadores".
- **O painel de perfil por cidade ganhou rótulo — revertendo a decisão de
  2026-11-25.** A "matiz única, sem ícone de bom/ruim" era decisão do PM e foi
  revista pelo PM em 2026-11-27: cada indicador do painel sai com o chip de
  parecer. A tira de percentil continua com uma matiz só (ela mostra posição,
  não qualidade), a ordem continua alfabética, e não há linha de total.

**O que vigiar**

- **Parecer lido como nota da cidade.** Se alguém escrever ou ler "a cidade tem
  mais bons que ruins", a decisão virou o que ela proíbe. O conferidor pega a
  forma escrita; a lida, só o auditor.
- **Direção discutível na tabela.** Densidade demográfica entrou como "mais é
  melhor" por analogia à urbanização, sem regra escrita da casa; habitantes por
  farmácia entrou como "mais é melhor" com a ressalva de cobertura da base.
  Se o PM discordar, muda uma linha em `_parecer.py`.
- **Provocações genéricas.** "Como está o movimento?" serve a qualquer praça.
  Toda provocação tem de partir de um achado desta sessão.

---

## 2026-11-26 — o seletor substitui o bloco numerado

`PROCEDENCIA: pedido do PM depois de tres rodadas de uso real.`

- **O bloco `P1/P2` resolveu um problema e criou outro.** Ele nasceu em
  2026-11-23 porque pergunta diluída na prosa não era vista. Vista ela passou a
  ser; respondida com conforto, não — "P1 - ... / P2 - ..." é digitação, e três
  rodadas depois o analista pediu para acabar com isso. Toda pergunta passa a
  sair em cartão de seletor, uma por cartão, no máximo quatro por chamada.
- **Duas opções fixas em todo cartão: "Não sei" e "Recomendar".** A primeira já
  era resposta válida e agora é botão. A segunda é nova e tem limite escrito:
  recomendar caminho de análise sim, ordenar praça por qualidade não — essa é a
  régua que tem dono, e foi retirada à mão de dois relatórios em 2026-11-25.
- **O rótulo "Outros" do app não se renomeia.** O pedido era que ele virasse
  "Não sei"; o campo é do app e serve para escrever. Então "Não sei" entrou como
  opção explícita e o texto do cartão convida a escrever no campo livre.
- **Empresário e responsável pelo GE viraram uma pergunta só.** São a mesma
  pessoa; perguntar duas vezes fazia o analista repetir o nome, como em
  2026-11-24 ("mesma pessoa").
- **Nome de pessoa: a regra passou a ter dois lados.** Na conversa, diga — o
  analista precisa saber quem opera na cidade. No entregável, nunca. Antes a
  regra era só a segunda metade, e isso empobrecia a conversa sem proteger nada
  a mais.
- **Os raios estavam grandes demais e faltava "só nesta cidade".** A opção de
  cidade não é raio pequeno: a distância da lista é de centroide de município a
  centroide de município, então nenhum raio separa uma região da cidade das
  outras. Virou `--so-municipio`, por código IBGE, sem queda para a UF quando a
  lista sai curta — lista vazia é a resposta.
- **Camada com três ou mais linhas comparáveis passa a sair em tabela ou
  gráfico.** Com uma trava manual junto: a conferência mecânica lê o dossiê, não
  a conversa, então nada confere o que vai num gráfico. Só valor de script, e
  nenhuma conta dentro do widget.

**Defeito de conferidor encontrado por uso**

- **`índice de potencial de consumo` era reprovado como "a régua com outro
  nome".** É o nome de uma camada do acervo, com valor medido. O padrão passou a
  exigir que "potencial" não venha seguido de "de consumo"; "índice de potencial"
  solto continua reprovando.

---

## 2026-11-25 — mapeamento Amélia Rodrigues/BA, e o painel de perfil por cidade

`PROCEDENCIA: uso real conduzido pelo PM. Mapeamento entregue, depois três
passadas de auditoria e uma mudança de produto no meio.`

**O que nasceu desta rodada**

- **Painel de perfil por cidade.** O documento declarava que não mede qualidade
  de praça, e isso empurrava a comparação para a prosa, onde ela virava ranking
  por acidente. Agora cada cidade da lista ganha onze indicadores com valor e
  **percentil nacional da própria camada** — o único referente que a casa
  permite. Uma linha por município, não por praça: nenhuma dessas camadas existe
  por unidade territorial, e uma linha por praça repetiria o mesmo valor oito
  vezes para Salvador.
- **Contagem de grupo econômico por identificador**, não por nome do
  responsável. O PM pediu "conte pelo número do GE" e eu respondi que o campo
  não existia — **estava errado**: eu tinha olhado só a exportação da pasta das
  bases. Havia uma mais nova, com a coluna. Lição: antes de dizer que um campo
  não existe, olhar todas as exportações, não a que o script acha primeiro.
- **O conversor do cadastro passou a escolher o arquivo.** O comando
  documentado, sem argumento, teria rebaixado o cache em 18 dias e perdido a
  coluna nova, enquanto a constante de data no código continuaria anunciando a
  data antiga. Agora ele procura a exportação mais recente que tenha todas as
  colunas, aborta dizendo o que falta, e grava a data lida do nome do arquivo.

**O que o painel pegou que três camadas de conferência não pegaram**

Eu escrevi "Salvador ocupa sete das doze linhas". São **oito**. O erro passou
pela conferência mecânica (o número existia na apuração), passou pelo auditor
duas vezes, e só caiu quando o painel contou sozinho e imprimiu 8 ao lado.
**Regra que nasce daí: número de contagem não se escreve à mão em prosa quando
o script já o tem.** O parágrafo-ponte do painel calcula; os outros dois pontos
que eu tinha escrito à mão foram os que sobreviveram à correção, e o auditor
teve de pegá-los na passada seguinte — com o documento afirmando 8 em três
lugares e 7 em dois, que é pior que o erro original.

**O modo de falha mais caro desta rodada: a correção que envelhece o vizinho**

Trocar a contagem de grupo para o identificador deixou, duas seções abaixo, uma
lacuna do gerador afirmando que a contagem era por nome — e um rodapé que
concluía "ou seja, confirme pelo CNPJ" a partir do critério abandonado três
linhas antes. É a mesma família do preço médio da passada anterior: **toda
lacuna fixa do gerador é uma afirmação sobre o que o documento não sabe, e
quando o documento passa a saber, ela mente.** Antes de fechar uma mudança,
varrer as lacunas fixas procurando a que ela acabou de tornar falsa.

Duas outras lacunas diziam que renda, população e potencial de consumo eram
desconhecidos — e o painel acabara de publicá-los. O que continua desconhecido é
a versão **por praça**, não o indicador.

**Consequência apurada e não propagada**

O script devolvia, no alerta de cadastro, que loja atribuída à praça errada
"muda a contagem de grupos e, com ela, a disponibilidade". O gerador imprimia só
o fato. É a família do `bloco-apurado-e-nao-impresso.md` aplicada a texto, e não
a número. E a consequência era **condicional**: onde a cidade não tem teto, não
muda nada — dizer isso ensina a ler o alerta na próxima cidade, onde decide.

**Ancorar no país não salva uma frase que compara dois casos**

Escrevi que o parque de Salvador é "menos adensado que o de Lauro de Freitas",
citando p75 e p21. Os percentis ancoram os números; o sujeito da frase continua
sendo a comparação entre as duas cidades, que é o que o painel declara inválido.
**Aposto não muda o que a oração afirma.** A redação que salva descreve cada
cidade contra a distribuição e diz, em voz alta, que a diferença entre elas não
é leitura que quatro casos sustentem.

No caminho inverso, a regra do painel estava absoluta demais — "comparar as
cidades desta lista entre si não é referente válido" — enquanto a leitura
comparava contagens do cadastro quatro vezes, legitimamente. Estreitada para os
**percentis**, que é o que ela de fato protege. Documento que se desobedece à
vista ensina o leitor a ignorá-lo.

**"E daí?" tem de nomear a decisão que muda**

O achado do Farmácia Popular — credenciamento no quintil inferior nas quatro
cidades — era verdadeiro, bem apurado, e não movia nada: um indicador uniforme
nas quatro não separa praça nenhuma. Ou ganha consequência concreta, ou vira
frase de contexto sem parágrafo próprio. **Parágrafo próprio promete
consequência.**

**Percentil sem o N não é reconferível**

O tamanho da distribuição varia por indicador — de 5.249 a 5.571 municípios — e
os dois de base mais estreita (captura e crescimento municipal) são os mais
citados na leitura. O número estava na apuração desde o início e não chegava ao
documento.

**O que vigiar na próxima rodada**

- **O nome "Folga competitiva" afirma folga**, e um dos seus três indicadores
  declara, na própria apuração, "é PERFIL DO PARQUE, não folga". A dimensão
  contradiz o indicador pelo rótulo. **Decidido pelo PM em 2026-11-25: fica como
  está.** O risco é conhecido e aceito — o texto do painel declara que o
  credenciamento é perfil do parque e que a razão de habitantes por farmácia é
  ambígua, então a ressalva está no documento mesmo com o rótulo afirmando
  folga. Vigiar se algum leitor lê a dimensão inteira como espaço livre; se
  acontecer, a correção é o rótulo, não mais texto.
- **Casamento fraco subiu para 43 entradas.** Percentil é inteiro sem unidade, e
  a regra está certa — o risco é a lista ficar longa o bastante para ninguém ler.
  Conferir pelo par cidade+indicador, não pelo número.
- **Se alguém colorir a tira de percentil por faixa**, o painel vira nota num
  commit. A matiz única é a decisão, não um esquecimento.

---



## 2026-11-25 — mapeamento de praças: Sorocaba/SP

`PROCEDENCIA: uso real conduzido pelo PM. Sem endereco, sem solicitante. Lista
de pracas entregue.`

**O que não funcionou, e virou mudança de fluxo**

- **A Fase 0 estava escrita para o caso errado.** O escopo dizia "só quando não
  há ponto nem cidade", e o pedido veio com cidade e sem endereço — que é o caso
  mais comum de quem está escolhendo onde abrir. A skill caiu na Fase A e
  perguntou perfil, empresário, responsável pelo GE e bandeira. As três últimas
  voltaram como **"não tenho ainda"**, porque não havia solicitante: era
  exploração antes de haver dono do pedido.
- **Nenhuma das quatro perguntas muda uma linha da lista de praças.** A vaga é
  sempre calculada para grupo novo e a régua de distância mínima só existe sobre
  um endereço. Perguntá-las ali é cobrar o que o pedido não tem. Agora a Fase 0
  pergunta duas coisas: âncora e modelo.
- **Dezesseis números caíram na conferência de uma vez.** Escrevi na lista de
  praças a população do dump, a saturação da cidade, os limiares da regra em
  metros e valores de uma rodada de praças com outro raio. Todos vieram de
  script nesta sessão — mas o formato de prospecção roda **uma chamada só**, a
  de praças, e é contra a apuração dele que a conferência confere. Regra que
  nasce daí: na prospecção, cite o que a linha da praça traz — população do
  Censo, potencial, captura, preço médio, receita da praça e receita da rede.
- **Inventei precisão uma vez e fiz um ranking de cabeça outra.** Transformei o
  rótulo "R$ 150,7 milhões" em centavos e escrevi "a segunda que mais cresce"
  comparando dois números apurados. Peguei os dois relendo, antes de gerar.

**O que funcionou**

- Conferir o nome do responsável pelo GE contra o cadastro continua pagando: em
  Lontras desmentiu a declaração do solicitante, e aqui a ausência dele foi o
  sinal de que o caso não era dossiê de ponto.
- A trava de pergunta obrigatória segurou a conversa no lugar certo: as três
  respostas "não tenho ainda" viraram decisão de fluxo, não premissa silenciosa.

**Defeito de gerador encontrado por uso**

- **`--detalhes` não estava ligado no formato de prospecção.** As duas cópias
  saíam byte a byte idênticas, e havia seção de Fontes para tirar. Corrigido com
  uma ressalva que o caso de impedimento já tinha: a enxuta tira as Fontes e
  **mantém** o bloco "O que esta lista é, e o que ela não é" — lá o parágrafo é
  o conteúdo, e uma lista que circula sem ele é lida como recomendação de
  abertura, que é exatamente o que aquele bloco existe para impedir.

**Uma lacuna que afirmou um efeito sem medir — Jardim América, Sorocaba**

- **O caso técnico inteiro está em** `analise-regiao-farmarcas/references/
  bloco-apurado-e-nao-impresso.md`, **itens 8 e 9**: a UTC repetida no dump, os
  21 municípios atingidos, os R$ 7,49 bilhões de receita fantasma e o conserto.
  Não repito aqui — duas versões da mesma lição divergem com o tempo.
- **O que é desta skill:** eu escrevi, na seção de lacunas de um entregável, que
  a soma do município contava a região duas vezes **e que o share saía inflado**.
  A primeira metade estava certa e eu não tinha medido; a segunda estava errada
  — a UTC repetida tem receita zero da rede, então só o denominador dobra e o
  share sai **menor**. Depois, contestado, concedi que nada disso existia —
  também sem medir.
- **A trava de número não pega isto.** A frase não tem número novo: tem
  **mecanismo**. `verificar_dossie.py` confere procedência de valor, não de
  causa, e uma lacuna bem escrita sobre um efeito inexistente passa limpa.
- **A régua:** lacuna que afirma um efeito — "conta duas vezes", "infla o
  share", "subestima" — é afirmação sobre o caminho do dado, e se confere lendo
  quem lê a base, com que chave, e o que itera a soma. Sem essa leitura, declare
  só o que viu ("a base traz a região em duas linhas") e pare ali. **O JSON do
  dossiê de Sorocaba ainda carrega a versão com a direção errada**, por decisão
  do PM de não mexer nele.

---

## 2026-11-23 — primeira rodada com o protocolo de perguntas: Gurupi/TO

`PROCEDENCIA: uso real conduzido pelo PM, logo após a mudança. Gate em alerta,
dossiê completo entregue, duas rodadas de auditoria.`

**O que funcionou**

- **O protocolo fez o que foi desenhado para fazer.** Uma pergunta aberta (P1,
  bandeira) travou a Fase A e foi respondida; sete perguntas no bloco final da
  Fase C foram respondidas **todas**, por número, de uma vez. Nenhuma passou
  despercebida, que era a falha que originou a mudança.
- **Diálogo para pergunta fechada funcionou melhor que o bloco.** Perfil, modelo
  e tipo de operação vieram em um turno só, sem ambiguidade.
- **Duas respostas mudaram número, não só prosa.** "Confie no cadastro" tirou
  duas lojas desativadas da contagem do anel e trocou R$ 4,32 mi/mês por
  R$ 3,96 mi/mês. "O ponto ficou livre" impediu que a escolha do endereço
  virasse vantagem competitiva na lente de Oportunidades.
- **O campo `muda:` pagou o custo dele.** Toda pergunta feita alterou um item,
  uma lacuna ou uma premissa. Nenhuma foi curiosidade.

**O que não funcionou**

- **Uma resposta ambígua não tem tratamento no protocolo.** Em P4 o PM
  respondeu "espere a etapa de geração de fluxo", que não é "não sei" nem
  conteúdo. Interpretei como "depois" e declarei a interpretação em voz alta
  antes de gerar — funcionou, mas por decisão minha e não por regra. **O
  protocolo precisa dizer o que fazer com resposta que não responde:**
  devolver a pergunta reformulada, ou declarar a leitura e seguir.
- **A trava de número continua sendo a que mais pega, e pegou duas vezes
  antes de qualquer script.** Escrevi "um quinto das farmácias" de 13÷67 e
  "quatro em cada cinco cidades" de um percentil 23. Peguei os dois relendo,
  antes de gerar — mas foram produzidos pela mesma mão e no mesmo movimento de
  querer facilitar a leitura. Converter percentil em "x em cada y" é aritmética
  do modelo disfarçada de didática.
- **Reintroduzi, numa frase, o que uma resposta tinha acabado de excluir.**
  Depois de "confie no cadastro", escrevi que duas lojas ocupavam a faixa mais
  alta do anel — e a segunda era justamente uma das desativadas. A decisão
  valeu para as contagens e não valeu para a frase três parágrafos adiante. O
  auditor pegou. **Regra que nasce daí:** resposta que exclui registro da
  análise vale para o documento inteiro, e a conferência disso é por registro,
  não por parágrafo.

**O que o auditor pegou e a conferência mecânica não**

- 11 reprovados na primeira passada, 8 resolvidos na segunda. A conferência
  mecânica passou limpa nas duas, com 0 números sem origem — ela confere
  procedência, não leitura. Dois achados graves só apareceram na leitura: duas
  réguas de população pareadas numa comparação (87.206 do acervo contra 85.125
  do Censo) e uma lacuna que o relatório remetia e que não existia.

**Defeitos de gerador descobertos por uso, não por teste**

Seis sintomas, mesma raiz — bloco que o script produz e o gerador não imprime,
ou imprime com registro a mais:

- card "Lojas Farmarcas no raio · 2" sem o status (as duas são desativadas);
- `venda_mensal_por_faixa` itera `dentro + nossas` em `raio_concorrencia.py`,
  então a tabela conta 9 lojas classificadas enquanto o card ao lado diz 7;
- lacuna genérica de fluxo de passantes duplicando a específica da narrativa;
- `camadas_indisponiveis_no_raio.farmacias` não chega ao HTML;
- `qualidade_do_dado.implausiveis` não é impresso — um dos 13 concorrentes do
  anel está cadastrado em Ibotirama e o script o marca como erro provável;
- POI a 513 m contado e nomeado dentro do raio de 500 m.

---

## 2026-11-23 — teste do PM: as perguntas não chegaram

`PROCEDENCIA: teste conduzido pelo PM, sem analista de Expansão. Gate liberado.`

**O que não funcionou**

- **Depois que o gate liberou, as perguntas ficaram diluídas na prosa do turno e
  não foram vistas.** O PM seguiu sem respondê-las — e a skill avançou assim
  mesmo, porque nada no checklist impedia. Um dossiê fechado com as perguntas em
  aberto é o dossiê que `/analise-regiao-farmarcas` já entregaria sem conversa
  nenhuma: a conversa virou custo sem contrapartida.
- **Na Fase C, as provocações vieram coladas em cada camada**, espalhadas por um
  turno longo. Responder exigiu garimpar o texto de cima a baixo. É a mesma
  falha prevista na entrada de criação ("responder as duas primeiras e ignorar o
  resto"), só que a causa não era quantidade — era dispersão.

**O que mudou por causa disso**

- Nasceu o `## Protocolo de perguntas`: bloco numerado único no fim do turno,
  números estáveis na sessão, e nenhuma fase converge com pergunta sem resposta
  explícita. "Não sei" e "pula" contam como resposta e viram lacuna declarada;
  o que bloqueia é o silêncio.
- Pergunta de opções conhecidas (perfil, modelo, tipo de operação, gerar ou não)
  passou a usar o diálogo de escolha do app, que não dá para não ver nem pular.
- Entrou o filtro `muda:`: toda pergunta declara o que no dossiê depende da
  resposta, e sem isso não entra. Atende ao pedido de só perguntar o que refina.
- Na Fase C, a **leitura** da camada ficou no corpo junto do número; só a
  **pergunta** migrou para o bloco final, marcada com a camada de origem.

**O que vigiar na próxima rodada**

- Se o bloco final ficar longo demais, o filtro `muda:` não está cortando — o
  problema volta como lista intimidadora em vez de perguntas dispersas.
- Se o diálogo de escolha não estiver disponível no canal em uso, conferir que a
  pergunta fechada caiu no bloco numerado e não voltou para a prosa.

---

## 2026-11-19 — primeira rodada real: Várzea Alegre/CE

`PROCEDENCIA: uso real, com analista. Gate liberado, dossiê completo entregue.`

**O que funcionou**

- A trava de número pegou os três erros que ela existe para pegar, e todos foram
  meus: "100 m" onde o script devolve 103 m, "doze vezes" de uma razão que eu
  mesmo calculei errado, e "5,6%" que era `100 − 94,37`. Dois foram barrados
  pela conferência mecânica, um pelo auditor. **A conversa realmente convida a
  aritmética de cabeça, exatamente como o `## Critical` previu.**
- Rodar o pacote de uma vez e conversar em cima dele sustentou cinco grupos de
  provocação num turno só, sem cota. O analista respondeu quatro dos cinco.
- Responder "não sei ainda, posso rodar X" funcionou como movimento de conversa:
  quando ele perguntou que plano faria sentido, a saída foi rodar a camada de
  hierarquia urbana — que **contradisse** a premissa da pergunta dele.

**O que não funcionou, e é a lição cara**

- **Li as saídas dos scripts truncadas e perdi achado grande.** `head`, `[:1800]`
  e `-c 400` cortaram, entre outras coisas, uma categoria inteira de geradores
  de fluxo (15 equipamentos de lazer e culto, o mais próximo a 56 m, um
  calçadão), o bloco de saturação (2.560,9 habitantes por farmácia, percentil 91
  nacional) e os percentis já calculados de renda, PIB e IPC. Resultado: escrevi
  uma lente de Dificuldades dizendo que o comércio começava 103 m adiante quando
  havia calçadão a 56 m, e classifiquei como fragilidade um IPC que está no
  percentil 77. O auditor achou os dois.
- **Regra que nasce daí:** a saída do script se lê inteira antes de virar lente.
  Cortar por `head` é aceitável para conferir que rodou; nunca para decidir o que
  entra no dossiê.

**Caso de borda**

- Cidade sem brick próprio: nenhum dos 73 bricks do Ceará leva o nome de Várzea
  Alegre. Virou melhoria no `mercado_brick.py`, que agora devolve `bricks_vizinhos`
  por distância de centroide — declarado como patamar da região, nunca como o
  brick do ponto, porque o atalho oposto já inverteu a conclusão de um dossiê.

**Defeitos de infraestrutura encontrados por uso, não por teste**

- `_bases.emitir` e `verificar_dossie.py` quebravam com `UnicodeEncodeError` ao
  imprimir "→" e "←" no Windows. Invisíveis no desenvolvimento porque o gerador
  roda os scripts com `-X utf8`; quem não roda é a linha de comando que a própria
  skill documenta. O gate chegava ao veredito e morria no meio do JSON.

---

## 2026-11-19 — criação da skill

`PROCEDENCIA: entrada de CRIAÇÃO da skill, não de uso real. Nada aqui foi
observado com analista.`

**Decisões que já nasceram testadas**

- A âncora da prospecção é obrigatória, e isso é medição, não preferência: sem
  coordenada de referência, Pouso Alegre e Ipatinga (390 km entre si) recebiam
  listas idênticas, 15 de 15. Depois da correção, as duas listas ficaram com
  **zero praças em comum**.
- O limite de 1–3 perguntas por turno vale na coleta e **não** na provocação.
  Veio de pedido explícito do PM em 19/11/2026: cortar a terceira provocação
  para cumprir cota silencia achado que muda a leitura. A restrição que sobrou é
  de legibilidade — agrupar por assunto —, não de quantidade.

**O que vigiar nas primeiras rodadas com analista**

- **Número adiantado entre rodadas.** É a trava que a conversa mais ameaça e a
  razão de ela estar no `## Critical`. Se aparecer uma estimativa no meio da
  conversa, registre aqui a frase exata que a produziu.
- **A conversa virando formulário na Fase A.** Se o analista responder as duas
  primeiras perguntas e ignorar as outras, o turno estava longo demais.
- **Provocação sem achado atrás.** Sinal de que a Fase C entrou antes de os
  números estarem na mesa.
- **Fase 0 sendo usada como recomendação de abertura.** A lista diz onde vale
  rodar um dossiê. Se alguém encaminhar o HTML como "praças recomendadas", o
  aviso do corpo não está onde o leitor olha primeiro.

**Dívida conhecida**

- A disponibilidade de praça é sempre calculada para grupo **novo**; o script não
  sabe quem perguntou. Para solicitante que já opera na praça, hoje a conversa
  declara a diferença em vez de o script calcular.
- A apuração de zoneamento dentro do raio cobre as 25 maiores praças por
  mercado. Praça pequena sem Censo em cache pode entrar na contagem como
  indisponível na primeira rodada; o cache corrige a partir da segunda.
