Continue a partir do protótipo que você já construiu. NÃO refaça a aplicação,
NÃO reescreva o que já funciona e NÃO mude o motor de score existente. Mantenha
intactos o fluxo de entrada, o arrastar de blocos, a troca de base de dados dos
indicadores, o construtor de gráficos, o recálculo do score em tempo real e a
comparação entre análises.

Adicione ao protótipo atual apenas o que está descrito abaixo.

## O ASSISTENTE PASSA A SER CONVERSÁVEL

Não crie uma segunda IA. O assistente discreto que hoje emite alertas é o mesmo
que passa a conversar — ele ganha um segundo modo, não um concorrente na tela.

MODO PROATIVO (já existe): a IA fala sem ser chamada, disparando alertas por
regra quando o analista mexe na montagem. Teto de três alertas proativos
seguidos sem o analista pedir nada; a partir daí ela silencia até ser chamada.

MODO CONVERSA (novo): o analista pergunta e a IA responde.

Os dois modos compartilham UM ÚNICO FIO, em ordem cronológica, visualmente
distinguíveis entre si.

O painel fica recolhido por padrão num canto, expande para conversar e NUNCA
cobre a grade de blocos — o analista precisa ver o painel mudando enquanto
conversa, porque as respostas alteram a tela.

## O FIO É PRIVADO POR PADRÃO

Esta é uma regra de produto, não um detalhe de interface, e precisa estar
evidente na tela.

O fio de conversa é PRIVADO do analista que o escreveu. Ninguém mais vê por
padrão — nem no comitê, nem quem reabrir a análise.

Cada mensagem do fio tem um botão "levar ao comitê", que fixa aquele trecho
específico na análise como material compartilhado. A anexação é trecho a trecho,
escolhida pelo analista, nunca automática.

Existe um botão "limpar rascunho do fio", disponível antes de fechar a análise.

A JUSTIFICATIVA DE ALERTA GRAVE É A EXCEÇÃO e continua como está hoje:
obrigatória, permanente e visível para todos. Essa é a trilha de auditoria
legítima e ela não se confunde com o fio de conversa.

PROIBIDO: a aplicação nunca exibe, conta ou agrega métrica do tipo "alertas
ignorados por analista", "quantas vezes a IA discordou" ou qualquer ranking
comparando analistas. Não crie esse número em lugar nenhum da interface.

## COMO O ANALISTA PERGUNTA

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

## COMANDO PRINCIPAL: ESSA ANÁLISE SE SUSTENTA NO COMITÊ?

O comando em destaque do painel não é "revisar minha análise" — é a pergunta que
o analista realmente faz antes de apresentar: "essa análise de ponto se sustenta
no comitê?".

Ele é oferecido também como passo leve no momento de FECHAR ou EXPORTAR a
análise, porque depois disso o analista não mexe mais nela.

A resposta é uma pauta de comitê, em três partes:

1. "O QUE VOCÊ VAI AFIRMAR E COM QUE EVIDÊNCIA" — as afirmações sustentadas,
   cada uma com o bloco e a fonte que a sustenta. Isto é pauta, não elogio: não
   escreva "sua análise está bem fundamentada".
2. "ONDE VÃO TE FURAR" — os pontos frágeis, nomeados como um colega nomearia.
3. "A PERGUNTA QUE VÃO TE FAZER E VOCÊ AINDA NÃO RESPONDE" — o que falta, mais as
   contradições entre blocos ou entre um bloco e o score.

A pauta tem um botão COPIAR, que entrega o texto pronto para colar — o analista
monta essa pauta à mão hoje, e se ela só viver dentro do painel não eliminou
passo nenhum.

## COMO A IA RESPONDE

ANCORADA NO QUE ESTÁ NA TELA. Toda resposta se refere aos blocos, camadas,
fontes e valores que de fato existem na análise atual. A IA nunca traz número que
não esteja no painel.

SEMPRE COM PROCEDÊNCIA JUNTO. Toda discordância carrega, na mesma mensagem, a
fonte, a data-base e a limitação metodológica do dado em que ela se apoia, mais
como conferir. Crítica sem procedência é opinião da ferramenta sobre o julgamento
de quem esteve na rua.

DECLARANDO O ESTATUTO DE CADA AFIRMAÇÃO. A interface mistura régua vigente da
Farmarcas com régua proposta ainda não homologada. Toda afirmação da IA diz de
qual das duas está falando. "Isso é regra vigente" e "isso é leitura minha com
régua ainda não homologada" são coisas diferentes, e só a primeira o analista
leva ao comitê.

PODENDO DISCORDAR DA RÉGUA, NÃO SÓ DO ANALISTA. A régua vigente tem pontos
discutíveis — renda D/E pontua mais que renda alta, densidade tem lógica
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

## DISCORDAR DA IA PRECISA SER BARATO

Todo alerta e toda crítica trazem um botão "não concordo", de UM clique. Ele abre
um campo curto e opcional para o motivo, e SILENCIA aquela regra nesta análise.

Se discordar custar um parágrafo, o analista fecha o painel em vez de responder.

Quando o analista demonstra que a IA estava errada, o alerta anterior fica
marcado no fio como RETRATADO. Sem isso, um alerta antigo continua parecendo de
pé para quem ler depois.

## AS RESPOSTAS TRAZEM AÇÕES APLICÁVEIS

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

## SALVAR MONTAGEM COMO PADRÃO

O analista pode salvar a montagem atual como padrão para um perfil de ponto (rua
comercial, bairro residencial, ponto isolado). Nas análises seguintes, a IA
oferece esse padrão junto com a montagem que ela própria propõe.

É a única economia que se acumula: corta trabalho em toda análise futura, não só
nesta. Deixe visível quantas análises já usaram cada padrão salvo.

## TERMINOLOGIA

- O painel de adicionar fala CAMADAS, que é a palavra que o time usa e que está no
  Órbita hoje. Uma camada alimenta um ou mais indicadores. "Bloco" fica reservado
  ao objeto arrastável na grade.
- Use FONTE em todo lugar. Não alterne com "base", "base de dados" e "base de
  origem" como se fossem termos diferentes.
- Diga sempre ANÁLISE DE PONTO, nunca só "análise" — existem quatro análises no
  processo e a ambiguidade confunde.

## RESTRIÇÕES ADICIONAIS

- Não existem duas IAs na tela. Um assistente, um fio, dois modos.
- A IA nunca responde com dado que não está na análise atual.
- Nenhuma resposta genérica de consultor: toda afirmação cita bloco, camada,
  valor ou fonte presente na tela.
- O painel de conversa não é um modal e não cobre a grade de blocos.
- Nenhuma métrica individual de alertas ignorados, em lugar nenhum.
- A conversa segue a mesma identidade visual já aplicada no protótipo: roxo
  profundo como cor de destaque, cards brancos de cantos arredondados, tipografia
  sem serifa, tudo em português do Brasil.
