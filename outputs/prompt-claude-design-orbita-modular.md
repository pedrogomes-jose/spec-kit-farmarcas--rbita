Construa um PROTÓTIPO NAVEGÁVEL E INTERATIVO — uma aplicação funcional de
verdade, não uma apresentação — de uma nova funcionalidade do Órbita, ferramenta
interna da Farmarcas usada pelo time de Expansão para avaliar a viabilidade
econômica de pontos comerciais para novas farmácias.

## O QUE ESTE ENTREGÁVEL É E O QUE NÃO É

É: uma única aplicação web interativa, que abre numa tela e navega para as
outras pela própria interface, como um software real. Quem recebe o link deve
conseguir CLICAR, ARRASTAR e VER O SISTEMA REAGIR.

NÃO é, em hipótese alguma:
- um deck, um conjunto de slides, ou uma sequência de telas estáticas;
- uma página com botões "próximo" / "anterior" passando por mockups;
- uma galeria de imagens de interface;
- telas numeradas lado a lado numa mesma página.

Não existe narração, não existe título de seção explicando o que a tela mostra,
não existe legenda do tipo "Tela 3 — modo de edição". A navegação acontece
dentro do produto: o usuário clica num botão do produto e chega noutro estado do
produto. Se em algum momento a saída parecer material de apresentação, está
errado.

Toda interação descrita abaixo precisa FUNCIONAR de fato, com estado real na
aplicação — não ser simulada com uma imagem do resultado.

## Contexto do produto

O analista de Expansão percorre hoje um fluxo linear:

1. Preenche dados básicos do lead (número do lead, nome do empresário,
   endereço, valor de aluguel, área total, área de venda).
2. Ajusta o pin de geolocalização num mapa e define o raio de análise — porque o
   empresário frequentemente envia o endereço errado. Clica em "Explorar com IA".
3. Recebe uma tela de resultado FIXA: sempre os mesmos indicadores, um score de
   viabilidade, uma lista de prós e contras escrita por IA, e um campo de
   comentário do analista.

O problema: a tela de resultado é igual para todo ponto. Uma rua comercial de
alto fluxo com poucos moradores e um bairro residencial recebem exatamente o
mesmo conjunto de indicadores — e o score penaliza a rua comercial por um motivo
que não se aplica a ela.

A funcionalidade a prototipar torna essa tela de resultado MODULAR.

## PERCURSO NAVEGÁVEL (o usuário percorre isto clicando, na ordem que quiser)

ENTRADA — Tela de ajuste do ponto
A aplicação abre aqui. Mostra os dados do lead já preenchidos, um mapa com um
pin arrastável e um slider de raio. Arrastar o pin e mover o slider devem
funcionar. O botão "Explorar com IA" leva ao próximo estado, com uma transição
curta de processamento (1 a 2 segundos) que deixa claro que a IA está montando
a análise.

ESTADO PRINCIPAL — Resultado montado pela IA
A tela de análise aparece já montada, com um aviso discreto e dispensável da
própria IA explicando por que ela escolheu aquele arranjo para ESTE ponto
("região de comércio de rua intenso: priorizei fluxo de comércios e custo do
ponto sobre população residente"). Deixe evidente que o analista não montou
nada — a IA propôs e ele agora pode editar.

Esta tela é o centro do protótipo. Tudo abaixo acontece dentro dela.

## INTERAÇÕES QUE PRECISAM FUNCIONAR DE VERDADE

1. ARRASTAR E REORGANIZAR BLOCOS
   Cada indicador, gráfico e bloco de texto é um card arrastável numa grade.
   Arrastar precisa funcionar com o mouse, com a grade refluindo e indicando a
   zona de encaixe. Blocos têm tamanhos diferentes (indicador compacto, gráfico
   largo, bloco de texto) e o tamanho é ajustável. O arranjo persiste enquanto a
   sessão estiver aberta. Sensação de Notion ou Airtable: handles discretos,
   encaixe claro, nenhum modal pesado.

2. TROCAR A BASE DE DADOS DE ORIGEM DE UM INDICADOR
   Cada bloco tem um seletor de fonte. Ao trocar a fonte, precisam mudar AO
   MESMO TEMPO, de verdade: o valor exibido, a procedência mostrada no bloco
   (nome da fonte, data-base, limitação metodológica em uma linha) e a
   contribuição daquele indicador no score. Nada disso pode ser estático.
   Exemplo de limitação que precisa caber no bloco sem poluir: a população
   residente, na fonte padrão, soma os habitantes de todos os setores
   censitários que INTERSECTAM o raio — o setor inteiro entra na conta mesmo que
   só uma ponta esteja dentro.

3. ADICIONAR E REMOVER BLOCOS
   Um painel lateral que abre e fecha, com duas abas.

   Aba CAMADAS: lista o que pode ser puxado das fontes conectadas, agrupado por
   tema (demografia, renda, concorrência, comércio, custo do ponto). "Camada" é a
   palavra que o time usa e que já existe no Órbita; cada camada alimenta um ou
   mais indicadores. Arrastar dali para a grade adiciona o bloco de verdade, com
   seu valor e sua entrada no score. Remover tira a contribuição do score na hora.

   Aba GRÁFICOS: abre o construtor guiado descrito na seção CONSTRUTOR DE
   GRÁFICOS. Gráficos NÃO entram no score — cada bloco de gráfico exibe de forma
   discreta e permanente "não entra no score", para o analista nunca confundir
   com indicador.

4. SCORE RECALCULADO EM TEMPO REAL
   O score não é um número desenhado: é computado em código a partir dos blocos
   presentes na tela, a cada mudança, com animação curta no número. Ver regras
   na seção MOTOR DE SCORE.

5. A IA QUESTIONADORA, DISPARADA POR REGRA
   Um assistente discreto e persistente num canto da tela, nunca um modal que
   interrompe. Ele reage ao que o usuário acabou de fazer, por regra
   determinística, não por texto fixo. Dois níveis:

   - SUGESTÃO: aviso leve e dispensável, citando o indicador e o motivo
     concreto. Ex.: ao remover o bloco de comércios no entorno num ponto de rua
     comercial, surge "você tirou o único indicador que captura fluxo num ponto
     onde a população residente é baixa — o score vai subestimar o movimento".

   - ALERTA GRAVE: quando a montagem comprometeria a credibilidade da análise, o
     analista PODE seguir, mas precisa escrever uma justificativa antes de
     continuar. O campo de justificativa é funcional, o texto é salvo e passa a
     aparecer permanentemente no bloco de score e no resumo da análise, visível
     para quem abrir depois.

   A IA analisa também os GRÁFICOS do painel, em quatro eixos — ver a seção
   A IA DE APOIO APLICADA AOS GRÁFICOS.

   O mesmo assistente também CONVERSA: o analista pergunta e ele responde, no
   mesmo painel e no mesmo fio — ver a seção ASSISTENTE CONVERSÁVEL.

6. COMPARAÇÃO ENTRE ANÁLISES
   Um botão na tela abre a comparação desta análise com outra, montada com um
   conjunto diferente de indicadores. A comparação precisa sinalizar de forma
   inequívoca que os dois scores NÃO são equivalentes, e mostrar qual
   subconjunto de indicadores as duas análises têm em comum.

## CONSTRUTOR DE GRÁFICOS (guiado por pergunta)

O analista NUNCA começa escolhendo "pizza" ou "barra". Ele começa escolhendo o
que quer saber. O construtor abre com um catálogo de perguntas; ao escolher uma,
o sistema monta o gráfico na forma recomendada e oferece as alternativas válidas
para aquela pergunta. O analista pode trocar para uma alternativa — e é aí que a
IA opina.

Catálogo de perguntas, cada uma com sua forma recomendada:

P1. "Como [indicador] muda conforme eu aumento o raio?"
    Dados: o mesmo indicador medido a 100m, 300m, 500m e 1000m.
    Recomendado: LINHA, uma série, com marcador destacado no raio atual da
    análise e rótulo direto apenas nesse ponto e no extremo.
    Alternativa válida: área (uma série).
    Vale para população, densidade, potencial de consumo, renda, concorrentes.

P2. "Como este ponto se compara à cidade, mesorregião e estado?"
    Dados: o valor do indicador no raio contra a média dos três recortes.
    Recomendado: BARRAS HORIZONTAIS COM ÊNFASE — o ponto na cor de destaque, os
    três recortes em cinza. Não é um gráfico de quatro cores: é um gráfico de um
    valor contra seu contexto.
    Alternativa válida: colunas verticais com a mesma ênfase.
    Marque este recorte na interface como "comparativo territorial — recorte a
    confirmar", porque a disponibilidade desses agregados ainda não foi validada.

P3. "Como a população se distribui por faixa etária?"
    Dados: categorias ordenadas (0-14, 15-29, 30-44, 45-59, 60+).
    Recomendado: COLUNAS com rampa ordinal de uma única cor, claro para escuro.
    Alternativa válida: barras horizontais.

P4. "Como a renda se distribui por classe econômica?"
    Dados: classes ordenadas (A, B1/B2, C1/C2, D/E).
    Recomendado: COLUNAS com rampa ordinal, ou BARRA EMPILHADA ÚNICA quando a
    leitura desejada for parte-do-todo.

P5. "Quais bandeiras concorrentes estão no raio?"
    Dados: categorias nominais com contagem.
    Recomendado: BARRAS HORIZONTAIS, uma cor só para todas as barras, ordenadas
    da maior para a menor. Teto de 7 categorias; o excedente vira "Outras".

P6. "Que tipos de comércio existem no entorno?"
    Dados: categorias nominais, leitura de composição.
    Recomendado: BARRAS HORIZONTAIS (nomes longos) ou BARRA EMPILHADA ÚNICA.
    Rosca só é alternativa válida com 6 fatias ou menos.

O construtor mostra, antes de inserir, uma pré-visualização do gráfico com os
dados reais do cenário — o analista vê o que vai receber antes de confirmar.

## RÉGUA DE FORMA QUE A IA APLICA

Estas regras são determinísticas e devem estar implementadas em código. Quando o
analista viola uma, a IA comenta citando o gráfico e o motivo concreto — nunca
"revise seu gráfico".

- DUAS MÉTRICAS DE ESCALAS DIFERENTES NO MESMO GRÁFICO: nunca em dois eixos Y. A
  IA propõe dois gráficos separados ou indexar ambas na mesma base. Este é o erro
  mais comum e o mais grave, porque inventa uma correlação que o dado não tem.
- ROSCA OU PIZZA COM MAIS DE 6 FATIAS, ou usada para comparar valores próximos:
  a IA propõe barras.
- GRÁFICO DE UMA BARRA SÓ, ou rosca de duas fatias: a IA aponta que isso é um
  indicador, não um gráfico, e oferece converter o bloco em indicador.
- MAIS DE 7 CATEGORIAS COM COR: a IA propõe agrupar o excedente em "Outras" ou
  trocar por tabela.
- COR POR TAMANHO EM CATEGORIA SEM ORDEM NATURAL (bandeiras concorrentes
  coloridas da mais escura para a mais clara conforme a contagem): a IA aponta
  que a cor está repetindo o que o comprimento da barra já diz, e propõe uma cor
  só.
- LINHA EM DADO CATEGÓRICO (bandeiras, tipos de comércio): a IA propõe barras,
  porque linha afirma continuidade onde não existe.
- EIXO DE VALOR QUE NÃO COMEÇA EM ZERO em gráfico de barras: a IA aponta que a
  diferença está visualmente exagerada.
- RÓTULO NUMÉRICO EM TODO PONTO: a IA propõe legenda mais rótulo seletivo no
  extremo e no ponto atual.

## A IA DE APOIO APLICADA AOS GRÁFICOS

A IA analisa os gráficos do painel em quatro eixos. Cada um gera comentário
próprio, sempre citando o bloco e o motivo:

EIXO 1 — ADEQUAÇÃO DA FORMA
   Aplica a RÉGUA DE FORMA acima. É a crítica mais objetiva e a que o analista
   aceita sem resistência.

EIXO 2 — CONTRADIÇÃO OU REFORÇO COM O SCORE
   O eixo mais valioso. A IA cruza o que o gráfico mostra com o que o score
   pontuou. Exemplos que precisam funcionar no cenário de Franca:
   - "Seu score não penaliza concorrência, mas o gráfico mostra concorrentes de
     bandeiras fortes dentro de 300m."
   - "A densidade pontuou alto por ser baixa a 300m, mas o gráfico de raio mostra
     que ela sobe de faixa a partir de 500m — o ponto forte do seu score depende
     do raio escolhido."
   - "A população pontuou 1 de 5, e o comparativo territorial mostra este ponto
     abaixo da média da cidade: o gráfico reforça o score."
   Quando o gráfico CONTRADIZ um indicador que pontuou, o comentário aparece
   também dentro do bloco de score, junto da composição.

EIXO 3 — PERTINÊNCIA AO TIPO DE PONTO
   O cenário classifica o ponto como comércio de rua intenso. Um gráfico de faixa
   etária da população residente tem baixa pertinência aqui, porque quem consome
   não mora ali. A IA aponta isso e sugere a pergunta mais pertinente.

EIXO 4 — REDUNDÂNCIA E COBERTURA DO PAINEL
   Olha o painel inteiro, não o gráfico isolado. Dispara quando três ou mais
   gráficos são do mesmo tema, e quando um tema relevante para aquele ponto está
   ausente — por exemplo nenhum gráfico de concorrência num raio com concorrentes
   registrados. O texto precisa nomear o viés: "quatro dos cinco blocos são
   demografia; a análise está enviesada por omissão da concorrência."

Um gráfico também pode disparar ALERTA GRAVE, com o mesmo tratamento dos
indicadores: o analista segue, mas escreve a justificativa, que fica registrada
e visível para quem abrir a análise depois.

## ASSISTENTE CONVERSÁVEL

Não existem duas IAs na tela. O assistente discreto que emite os alertas é o
mesmo que conversa — ele tem dois modos, não um concorrente.

MODO PROATIVO: a IA fala sem ser chamada, disparando alertas por regra quando o
analista mexe na montagem. Teto de três alertas proativos seguidos sem o analista
pedir nada; a partir daí ela silencia até ser chamada.

MODO CONVERSA: o analista pergunta e a IA responde.

Os dois modos compartilham UM ÚNICO FIO, em ordem cronológica, visualmente
distinguíveis entre si.

O painel fica recolhido por padrão num canto, expande para conversar e NUNCA
cobre a grade de blocos — o analista precisa ver o painel mudando enquanto
conversa, porque as respostas alteram a tela.

### O fio é privado por padrão

Esta é uma regra de produto, não um detalhe de interface, e precisa estar
evidente na tela.

O fio de conversa é PRIVADO do analista que o escreveu. Ninguém mais vê por
padrão — nem no comitê, nem quem reabrir a análise.

Cada mensagem tem um botão "levar ao comitê", que fixa aquele trecho específico
na análise como material compartilhado. A anexação é trecho a trecho, escolhida
pelo analista, nunca automática. Existe também um botão "limpar rascunho do fio",
disponível antes de fechar a análise.

A JUSTIFICATIVA DE ALERTA GRAVE É A EXCEÇÃO: continua obrigatória, permanente e
visível para todos. É a trilha de auditoria legítima e não se confunde com o fio.

PROIBIDO: a aplicação nunca exibe, conta ou agrega métrica do tipo "alertas
ignorados por analista", "quantas vezes a IA discordou" ou qualquer ranking
comparando analistas. Não crie esse número em lugar nenhum da interface.

### Como o analista pergunta

Campo de texto livre no rodapé do painel, com perguntas sugeridas acima dele em
chips clicáveis. As sugestões MUDAM conforme o estado atual da tela.

Perguntas que devem aparecer, nas palavras que o analista usa de verdade:

- "Esse número bate com o que eu vejo no Google?"
- "O que eu vou ter que explicar no comitê?"
- "Quantos concorrentes tem no raio e de que bandeira?"
- "Esse aluguel cabe no faturamento que esse ponto consegue?"
- "O que muda se eu for para 500m?"

Quando o analista acabou de remover um bloco, de trocar uma fonte ou de adicionar
um gráfico, pelo menos uma das sugestões precisa se referir ao que ele acabou de
fazer.

NÃO inclua um chip "por que o score ficou nesse percentual?" — a composição do
score já está permanentemente visível na tela. Se o analista precisa perguntar
isso, a tela falhou.

### Comando principal: essa análise se sustenta no comitê?

O comando em destaque do painel é a pergunta que o analista realmente faz antes
de apresentar: "essa análise de ponto se sustenta no comitê?". Ele é oferecido
também como passo leve no momento de FECHAR ou EXPORTAR a análise, porque depois
disso o analista não mexe mais nela.

A resposta é uma pauta de comitê, em três partes:
1. "O QUE VOCÊ VAI AFIRMAR E COM QUE EVIDÊNCIA" — as afirmações sustentadas, cada
   uma com o bloco e a fonte que a sustenta. Isto é pauta, não elogio: não escreva
   "sua análise está bem fundamentada".
2. "ONDE VÃO TE FURAR" — os pontos frágeis, nomeados como um colega nomearia.
3. "A PERGUNTA QUE VÃO TE FAZER E VOCÊ AINDA NÃO RESPONDE" — o que falta, mais as
   contradições entre blocos ou entre um bloco e o score.

A pauta tem um botão COPIAR, que entrega o texto pronto para colar — o analista
monta essa pauta à mão hoje, e se ela só viver dentro do painel não eliminou
passo nenhum.

### Como a IA responde

ANCORADA NO QUE ESTÁ NA TELA. Toda resposta se refere aos blocos, camadas, fontes
e valores que de fato existem na análise atual. A IA nunca traz número que não
esteja no painel.

SEMPRE COM PROCEDÊNCIA JUNTO. Toda discordância carrega, na mesma mensagem, a
fonte, a data-base e a limitação metodológica do dado em que ela se apoia, mais
como conferir. Crítica sem procedência é opinião da ferramenta sobre o julgamento
de quem esteve na rua.

DECLARANDO O ESTATUTO DE CADA AFIRMAÇÃO. A interface mistura régua vigente da
Farmarcas com régua proposta ainda não homologada. Toda afirmação diz de qual das
duas está falando — só a régua vigente o analista leva ao comitê.

PODENDO DISCORDAR DA RÉGUA, NÃO SÓ DO ANALISTA. A régua vigente tem pontos
discutíveis: renda D/E pontua mais que renda alta, densidade tem lógica
invertida, concorrência não pontua. A IA precisa saber dizer "a régua vigente te
dá 5 em renda porque a classe é D/E, e eu acho que isso não sustenta no comitê
deste ponto". Uma IA que só defende a régua contra o analista perde credibilidade
e é fechada na terceira vez.

COM RECUSA HONESTA, DITA UMA VEZ. Quando a pergunta sai do que os dados
sustentam, a IA diz o que não tem e oferece a pergunta vizinha que conseguiria
responder. Mas a limitação estrutural do ponto é declarada UMA VEZ, no topo da
montagem — "ponto classificado como comercial; a régua vigente subestima esse
perfil porque pontua residente" — e não repetida a cada resposta, senão vira
disclaimer que o analista aprende a ignorar.

SABENDO O QUE ESTÁ FORA DE ESCOPO. Esta é a análise de PONTO. Perfil, território
e estrutura são outras análises e não estão aqui. A IA nunca diz que a análise se
sustenta sem registrar que cobre apenas o ponto.

COM TOM QUESTIONADOR E CONSTRUTIVO. Direta, sem bajulação. Nunca abre com "ótima
pergunta". Quando o analista está certo, confirma dizendo o motivo.

### Discordar da IA precisa ser barato

Todo alerta e toda crítica trazem um botão "não concordo", de UM clique. Ele abre
um campo curto e opcional para o motivo, e SILENCIA aquela regra nesta análise.
Se discordar custar um parágrafo, o analista fecha o painel em vez de responder.

Quando o analista demonstra que a IA estava errada, o alerta anterior fica marcado
no fio como RETRATADO. Sem isso, um alerta antigo continua parecendo de pé para
quem ler depois.

### As respostas trazem ações aplicáveis

A conversa precisa mudar a análise, não só comentá-la.

As respostas vêm com UMA ação recomendada em destaque. Alternativas ficam atrás
de "outras opções" — três botões lado a lado viram menu e devolvem ao analista
justamente a decisão que o produto deveria estar tirando dele.

Antes de aplicar, a ação MOSTRA O DELTA DE SCORE: "+8 pontos no numerador, +5 no
máximo, score vai de 55% para 58%". Depois de aplicada, fica marcada no bloco de
composição como "sugerido pela IA, aceito por você" — a autoria é do analista,
porque é ele quem responde no comitê.

Ações destrutivas (remover bloco, remover gráfico) pedem confirmação e oferecem
DESFAZER imediato dentro do próprio fio.

Ações que precisam funcionar:
- "Adicionar a camada de custo por m²"
- "Adicionar o gráfico de bandeiras concorrentes no raio"
- "Trocar a fonte da população para a base alternativa"
- "Simular 500m e mostrar o antes e depois lado a lado"
- "Salvar esta montagem como padrão para ponto de rua comercial"

### Salvar montagem como padrão

O analista pode salvar a montagem atual como padrão para um perfil de ponto (rua
comercial, bairro residencial, ponto isolado). Nas análises seguintes, a IA
oferece esse padrão junto com a montagem que ela própria propõe. É a única
economia que se acumula: corta trabalho em toda análise futura, não só nesta.
Deixe visível quantas análises já usaram cada padrão salvo.

## MOTOR DE SCORE (implemente este cálculo em código)

O score é a soma dos pontos dos indicadores presentes na tela, dividida pelo
máximo possível daquela montagem, exibida como percentual de 0 a 100 — nunca em
pontos absolutos, porque o total máximo varia conforme o que está na tela.

A composição do score fica SEMPRE visível: quais indicadores entraram, quantos
pontos cada um deu, quais estão na tela mas fora do score.

Faixas vigentes no Órbita hoje (0 a 5 pontos cada, use exatamente estas):

População na área (residentes)
  acima de 200.000 = 5 | 120.000 a 199.999 = 3 | 20.000 a 119.999 = 2
  10.000 a 19.999 = 1 | abaixo de 10.000 = 0

Densidade demográfica (hab/km²) — atenção, a lógica é INVERSA
  até 5.000 = 5 | 5.001 a 10.000 = 3 | 10.001 a 25.000 = 2 | acima de 25.000 = 0

Potencial de consumo mensal em drogarias (R$)
  acima de 2.000.000 = 5 | 1.500.000 a 2.000.000 = 4
  1.000.000 a 1.499.999 = 3 | 500.000 a 999.999 = 2 | abaixo de 500.000 = 1

Classificação econômica (renda média)
  A++/A+ (R$ 19.024,01 ou mais) = 0 | B1/B2 (R$ 4.508,01 a 19.024) = 1
  C1/C2 (R$ 1.275,01 a 4.508) = 3 | D/E (até R$ 1.275) = 5

Para os indicadores que hoje NÃO pontuam (concorrentes no raio, comércios e
pontos de interesse próximos, custo por m²), crie uma régua de 0 a 5 coerente e
marque-a visivelmente na interface como "régua proposta, ainda não homologada".
Não apresente essas réguas como se fossem regra vigente.

## INDICADORES DISPONÍVEIS NO PROTÓTIPO

Já existem no produto e devem vir montados pela IA na entrada:
- População na área (residentes)
- Densidade demográfica (hab/km²)
- Potencial de consumo mensal em drogarias
- Classificação econômica (renda média)
- Concorrentes no raio
- Comércios e pontos de interesse próximos
- Prós e contras gerados por IA
- Comentário do analista
- Score de viabilidade

Disponíveis no painel para adicionar, demonstrando o ganho da modularização:
- CUSTO POR M² DO PONTO — calculado a partir do valor de aluguel e da área de
  venda que o analista já informou na entrada. Este dado já é coletado hoje e
  não entra no score; é o exemplo mais convincente do que a modularização
  destrava. Garanta que ele esteja no painel e que adicioná-lo mexa no score.
- Faixa etária da população
- Fluxo estimado de comércios no entorno

Cada indicador precisa ter pelo menos duas fontes alternativas selecionáveis,
com valores e limitações diferentes entre si, para a troca de fonte ter efeito
observável.

## LINGUAGEM VISUAL

Siga a identidade do Órbita, visível no produto atual:
- Roxo profundo como cor primária, em botões sólidos e no item ativo da
  navegação lateral. Fundo geral claro, quase branco.
- Navegação lateral fixa à esquerda, fundo branco, ícones de linha finos, item
  ativo em roxo sólido com texto branco. Itens: Início, Indicadores, Análises de
  Pontos, Contratos Fechados, Base de Dados, Órbita IA (ativo).
- Conteúdo em cards brancos com cantos bem arredondados e sombra difusa e suave.
- Rótulos de campo em caixa alta, pequenos, cinza médio, precedidos de ícone de
  linha; valor logo abaixo em texto escuro e maior.
- Mapa presente e integrado, não decorativo.
- Botão primário roxo, cantos arredondados, com ícone de seta à direita.
- Tipografia sem serifa, geométrica, limpa.
- Toda a interface em português do Brasil.

## RESTRIÇÕES

- Não invente nomes de bases de dados da Farmarcas. Use rótulos genéricos e
  plausíveis ("Base demográfica IBGE 2022", "Base interna de concorrência",
  "Base de estabelecimentos CNEFE") e deixe um aviso discreto e permanente na
  interface indicando que os valores são ilustrativos.
- Os números precisam ser internamente consistentes: o score mostrado tem que
  bater com a soma das contribuições exibidas, e trocar a fonte tem que produzir
  uma variação coerente. Alguém vai conferir na frente do stakeholder.
- Nenhum alerta genérico do tipo "revise sua análise": todo alerta cita o
  indicador e o motivo concreto.
- Nenhum elemento de apresentação: sem capa, sem título de seção narrando a
  funcionalidade, sem rodapé com número de tela.
- Todo gráfico tem legenda quando há duas ou mais séries, rótulos diretos apenas
  seletivos, grade e eixos em traço fino e recessivo, e tooltip no hover. O valor
  nunca é acessível só pelo tooltip.
- Nenhum gráfico usa dois eixos Y, em nenhuma circunstância.
- A cor segue a entidade, nunca a posição no ranking: filtrar uma categoria não
  pode repintar as que sobraram.
- Não existem duas IAs na tela. Um assistente, um fio, dois modos.
- A IA nunca responde com dado que não está na análise atual.
- Nenhuma resposta genérica de consultor: toda afirmação cita bloco, valor ou
  fonte presente na tela.
- O painel de conversa não é um modal e não cobre a grade de blocos.
- Nenhuma métrica individual de alertas ignorados, em lugar nenhum da interface.

## TERMINOLOGIA

- O painel de adicionar fala CAMADAS, que é a palavra que o time usa e que já
  existe no Órbita. Uma camada alimenta um ou mais indicadores. "Bloco" fica
  reservado ao objeto arrastável na grade.
- Use FONTE em todo lugar. Não alterne com "base", "base de dados" e "base de
  origem" como se fossem termos diferentes.
- Diga sempre ANÁLISE DE PONTO, nunca só "análise" — existem quatro análises no
  processo da Farmarcas (perfil, ponto, território e estrutura) e a ambiguidade
  confunde.

## CENÁRIO (use estes dados de forma consistente em toda a aplicação)

Lead 1223 · Empresário: Pedro · Endereço: Franca, SP · Raio inicial: 300 m ·
Aluguel: R$ 4.000,00 · Área total: 350 m² · Área de venda: 200 m².

O ponto fica numa região de comércio de rua movimentado, perto de hospital e
supermercado — um caso em que a população residente sozinha engana, e por isso
a montagem padrão da IA deve privilegiar fluxo e custo do ponto.
