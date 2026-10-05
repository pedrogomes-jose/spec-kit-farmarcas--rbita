Continue a partir do protótipo que você já construiu. NÃO refaça a aplicação,
NÃO reescreva o que já funciona e NÃO mude o motor de score existente. Mantenha
intactos o fluxo de entrada, o arrastar de blocos, a troca de base de dados dos
indicadores, o recálculo do score em tempo real e a comparação entre análises.

Adicione ao protótipo atual apenas o que está descrito abaixo.

## ALTERAÇÃO NO PAINEL DE ADICIONAR BLOCOS

O painel lateral que hoje adiciona indicadores passa a ter duas abas.

Aba INDICADORES: continua exatamente como está hoje.

Aba GRÁFICOS: abre o construtor guiado descrito a seguir. Gráficos NÃO entram no
score — cada bloco de gráfico exibe de forma discreta e permanente "não entra no
score", para o analista nunca confundir com indicador. Adicionar ou remover um
gráfico não pode mover o número do score.

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

Os gráficos usam os mesmos dados e as mesmas fontes já existentes no protótipo.
Trocar a fonte de um indicador precisa refletir também nos gráficos que usam
aquele indicador.

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

## A IA DE APOIO PASSA A ANALISAR OS GRÁFICOS

A IA de apoio que já existe no protótipo ganha quatro eixos novos de análise,
aplicados aos gráficos. Ela continua discreta e persistente num canto da tela,
nunca um modal que interrompe. Cada eixo gera comentário próprio, sempre citando
o bloco e o motivo concreto:

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

Um gráfico também pode disparar ALERTA GRAVE, com o mesmo tratamento que os
indicadores já têm hoje: o analista segue, mas escreve a justificativa, que fica
registrada e visível para quem abrir a análise depois.

## RESTRIÇÕES ADICIONAIS

- Todo gráfico tem legenda quando há duas ou mais séries, rótulos diretos apenas
  seletivos, grade e eixos em traço fino e recessivo, e tooltip no hover. O valor
  nunca é acessível só pelo tooltip.
- Nenhum gráfico usa dois eixos Y, em nenhuma circunstância.
- A cor segue a entidade, nunca a posição no ranking: filtrar uma categoria não
  pode repintar as que sobraram.
- Os gráficos seguem a mesma identidade visual já aplicada no protótipo: roxo
  profundo como cor de destaque, cinza para o contexto, cards brancos de cantos
  arredondados, tipografia sem serifa, tudo em português do Brasil.
- Mantenha o aviso de que os valores são ilustrativos.
