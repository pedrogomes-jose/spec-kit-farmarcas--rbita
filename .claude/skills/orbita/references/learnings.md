# Aprendizados — skill `orbita`

Uma entrada por rodada de uso real. Formato: data · o que funcionou · o que não
funcionou · caso de borda. Marque a procedência quando a entrada **não** vier de
uso real — aprendizado de teste e aprendizado de campo não valem o mesmo.

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
