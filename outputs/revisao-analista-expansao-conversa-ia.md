# Revisão do assistente conversável — perspectiva do analista de Expansão

> Saída integral do subagente `analista-expansao`, executado em 2026-10-05 sobre
> o incremento conversacional do Órbita IA.
>
> **Natureza deste documento:** é a avaliação de um subagente que simula a
> perspectiva de quem monta o score de ponto manualmente hoje. Não é pesquisa com
> usuário real e não substitui validação com o time de Expansão. Serve para
> antecipar objeções antes de construir.
>
> Documentos que o subagente leu: `outputs/prompt-claude-design-orbita-conversa-incremento.md`,
> `outputs/prompt-claude-design-orbita-modular.md`,
> `docs/confluence/2025/orbita-descoberta-analise-pontos.md`,
> `docs/confluence/ia/analises/estudo-peso-populacao-score-viabilidade.md`.

---

## 1. Conversa visível no comitê — é aqui que a feature morre

Franqueza, como você pediu: **sim, me inibe. Mas não pelo motivo que você supõe.**

Não é vergonha de perguntar coisa básica. Eu pergunto coisa básica pro colega do
lado toda semana. O que me trava é outra coisa: o fio registra **a IA discordando
de mim e eu seguindo mesmo assim**. No comitê, isso não é contexto — é munição. O
colega abre meu fio e diz "a IA te avisou que tinha bandeira forte a 300m e você
tocou". E quem me cobra não é o empresário: é minha liderança, na reunião de
resultado, três meses depois, quando a loja não performa.

O selo "deliberação interna, não vai pro PDF" **protege do medo errado**. Eu nunca
tive medo do empresário ler minha dúvida. Meu medo é interno. O selo resolve um
risco que não existe e deixa o risco real intacto.

Efeito de segunda ordem, e esse é o que mata: se o fio é visível por padrão, eu
paro de usar o fio. Volto a perguntar no WhatsApp do time e a anotar na planilha —
exatamente o comportamento de controle paralelo que a descoberta já aponta como
problema (seção "Retrabalho para salvar informações"). O produto recria o sintoma
que ele quer curar.

**Ajuste concreto:**

- Separar dois registros que a spec trata como um só:
  - **Justificativa de alerta grave** (já especificada no prompt modular):
    obrigatória, permanente, visível no comitê. Essa é a trilha de auditoria
    legítima e eu aceito, porque eu já escrevo justificativa hoje na planilha.
  - **Fio de conversa**: privado do autor por padrão. Eu escolho o que anexar ao
    comitê, trecho a trecho ("levar pro comitê"). Pin manual, não exposição
    automática.
- Botão "limpar rascunho do fio" antes de fechar a análise. Se eu não puder
  apagar, eu não escrevo.
- Regra explícita na spec: **nunca contabilizar nem exibir métricas do tipo
  "quantas vezes a IA discordou" ou "quantos alertas ignorados" por analista.**
  Basta alguém puxar esse número uma vez num comitê pra feature estar morta no mês
  seguinte. Isso precisa estar escrito, não subentendido.

---

## 2. Tom — a IA não pode defender um número que eu não confio

A desconfiança registrada na descoberta é **com os números**, não com a análise.
Então uma IA que me contesta, apoiada nos mesmos números que eu desconfio, é lida
como "a ferramenta errada me corrigindo". Fecho o painel na terceira vez.

O que muda o jogo: **a IA discordar da régua, não de mim.** Eu olho a régua
vigente e ela tem coisas que eu não defendo em comitê — densidade com lógica
inversa, renda D/E valendo 5 pontos (ponto mais pobre pontua mais alto),
concorrência não pontuando. Se o primeiro diálogo real dela for defender esse
score contra mim, perde credibilidade de uma vez. Se ela souber dizer "nessa
montagem a régua vigente te dá 5 em renda porque a classe é D/E, e eu acho que
isso não sustenta no comitê desse ponto específico", ela virou colega. É isso que
compra o direito de me criticar depois.

**Ajustes concretos:**

- **Crítica só com procedência junto.** Toda discordância carrega fonte,
  data-base e limitação metodológica na mesma mensagem, mais um caminho de
  conferência. Sem isso é opinião da ferramenta sobre o julgamento de quem está na
  rua.
- **Discordar da IA tem que ser barato.** Botão "não concordo" em cada alerta, um
  clique, grava o motivo em texto curto e **silencia aquela regra nesta análise**.
  Se pra discordar eu tiver que escrever parágrafo, eu fecho o painel.
- **A IA marca o estatuto de cada afirmação.** As duas specs misturam régua
  homologada com "régua proposta, não homologada" (concorrentes, comércios, custo
  por m²). Na conversa isso tem que aparecer em cada frase, não só no bloco. "Isso
  é regra vigente da Farmarcas" é diferente de "isso é leitura minha com régua
  ainda não homologada" — e eu só levo a primeira pro comitê.
- **Teto de alertas proativos por sessão.** Modo proativo + modo conversa no mesmo
  fio significa que ela pode falar sem parar enquanto eu arrasto bloco. Três
  alertas seguidos sem eu pedir e vira ruído.
- Falta na spec o caso oposto: **quando eu estou certo e ela estava errada.** O
  prompt diz "quando o analista está certo, confirma dizendo o motivo" — mas não
  diz o que acontece com o alerta anterior dela. Tem que ficar marcado no fio como
  retratado, senão o comitê lê o alerta antigo como se continuasse de pé.

---

## 3. Perguntas sugeridas — metade não é pergunta minha

| Chip proposto | Veredito |
|---|---|
| "Por que o score ficou nesse percentual?" | **Cortar como chip.** Isso não devia ser pergunta — o breakdown por dimensão devia estar sempre na tela (o próprio estudo de score recomenda isso em "curto prazo"). Se eu preciso perguntar, a tela falhou. |
| "O que mais pesa contra este ponto?" | **Manter.** Eu faço essa. Mas minha formulação real é "o que eu vou ter que explicar no comitê". |
| "Qual indicador está faltando na minha análise?" | **Fraco como chip.** Isso é trabalho dela, proativo. Se ela sabe o que falta, por que esperou eu perguntar? |
| "Essa análise se sustenta num comitê?" | **A melhor da lista.** É literalmente o que eu penso antes de apresentar. Promover a comando principal, acima de "Revisar minha análise". |
| "O que mudaria se eu aumentasse o raio para 500m?" | **Boa, mas vira ação, não chip.** Eu testo raio arrastando o slider. Útil é o antes/depois lado a lado, não uma resposta em texto. |
| "Por que você escolheu esses indicadores?" | **Pergunta de primeira semana.** Eu faço uma vez e nunca mais. Não ocupa slot permanente. |
| "Tem algo aqui que se contradiz?" | **Redundante** com a parte 4 do "Revisar minha análise". Duplica comando. |

**O que falta, nas minhas palavras:**

- **"Esse número bate com o que eu vejo no Google?"** — essa é a pergunta número 1
  da minha rotina e nenhuma das duas specs a contempla. Hoje eu abro Street View e
  conto farmácia na rua antes de confiar no Órbita. A IA não precisa ter a
  resposta: precisa dizer de onde veio o número, qual a data-base e por que pode
  divergir do Maps.
- **"Quantos concorrentes e de que bandeira?"** — concorrência não pontua no
  score, mas é a primeira coisa que o comitê pergunta. Hoje é a camada que eu mais
  uso.
- **"Esse ponto parece com qual loja que a gente já abriu?"** — eu não comparo com
  a média da cidade, eu comparo com loja real. É o argumento que mais convence
  comitê.
- **"Esse aluguel cabe no faturamento que esse ponto consegue?"** — custo por m²
  sozinho não decide nada. A conta que eu faço na planilha é aluguel contra
  potencial de consumo. Se o custo por m² é o "exemplo mais convincente da
  modularização" (está assim no prompt modular), ele precisa vir cruzado, não
  isolado.
- **"Já teve análise nesse endereço antes?"** — lead duplicado acontece e
  descobrir tarde queima tempo.

---

## 4. "Revisar minha análise" — serve, mas não nessas quatro partes

Momento de uso: **nunca durante o comitê** — no comitê eu apresento, não mexo na
tela. Antes do comitê, sim, mas o ponto exato não é "quando eu lembrar de clicar":
é **antes de eu transcrever pra planilha**. Depois que transcrevi, mudar a análise
custa retrabalho duplo (tela + planilha) e eu simplesmente não mudo mais. Então o
gatilho certo não é um botão solto no painel — é um check leve e obrigatório no
"fechar/exportar análise".

Sobre as quatro partes: **a parte 1 ("o que está bem fundamentado") é a que eu
pulo.** Ela não me dá nada e é justamente a que faz o parecer parecer avaliação de
desempenho. Corta ou colapsa fechada.

**Reformulação na linguagem do comitê:**

1. ~~O que está bem fundamentado~~ → **"O que você vai afirmar e com que
   evidência"** (vira minha pauta, não elogio).
2. **"Onde vão te furar"** (o frágil, mas nomeado como o colega nomeia).
3. **"A pergunta que vão te fazer e você ainda não responde"** (o que falta, com o
   uso real).
4. **Contradição entre blocos e score** — manter, é a parte mais objetiva e a que
   eu aceito sem resistência.

E uma coisa que falta: **o parecer precisa sair da tela em formato de pauta
copiável.** Hoje eu monto essa pauta à mão pro comitê. Se o parecer só vive dentro
do painel, ele não eliminou passo nenhum — só me deu uma leitura a mais.

---

## 5. Ações por botão — reduzem passo de verdade, mas em duas delas eu perco o controle

Adicionar indicador e inserir gráfico por botão: **reduz passo de verdade, sem
ressalva.** Isso é bom.

Onde quebra:

- **Qualquer ação que mexe no score sem eu entender a régua.** No comitê vou ser
  perguntado "por que 62%?" e "a IA adicionou" não sobrevive à pergunta. Ajuste: a
  ação **mostra o delta de score antes de aplicar** ("+8 pts no numerador, +5 no
  máximo → score vai de 55% para 58%") e, depois de aplicada, fica marcada no
  bloco de composição como "sugerido pela IA, aceito por você". A autoria tem que
  ser minha e visível.
- **"Remover o gráfico de faixa etária" como ação de IA.** Botão de IA que apaga
  coisa minha é onde a sensação de perder controle é concreta e justificada. Ação
  destrutiva precisa de confirmação e de **desfazer imediato dentro do próprio
  fio**, ao lado do selo "aplicado".
- **Até três botões por resposta é demais.** Três opções viram menu e me obrigam a
  decidir o que eu não sei decidir — que é exatamente o conhecimento prévio que o
  produto deveria estar eliminando. Uma ação recomendada em destaque, as outras
  atrás de "outras opções".

**Ações que faltam e que são as que mais cortam trabalho meu:**

- **"Simular 500m e me mostrar antes/depois"** — eu testo raio em toda análise, na
  mão, uma de cada vez.
- **"Salvar essa montagem como padrão para ponto de rua comercial"** — eu repito a
  mesma montagem entre análises parecidas. Isso elimina passo em toda análise
  futura, não só nesta. É a maior economia disponível e não está na spec.
- **"Comparar com a loja X que já abrimos"**.

---

## 6. O que está faltando do meu processo real

**6.1 — A conversa para onde meu trabalho continua.** A jornada da descoberta tem
13 passos; a tela de análise é o passo 6. Minhas 3 horas estão nos passos 7 a 10:
transcrever pra planilha, análise de território e estrutura em fontes externas
(Google, Caravela, IBGE), montar o feedback e virar PDF. O incremento é todo
dentro do passo 6.

Pior: a spec **proíbe explicitamente** a IA de ajudar no momento em que ela mais
economizaria tempo. "Não entra no feedback do empresário" está certo como regra de
privacidade, mas está sendo lido como "a IA não ajuda a escrever o feedback". São
coisas diferentes. **Ajuste: ação "gerar rascunho do feedback a partir do que
ficou fundamentado"** — texto editável por mim, com evidência e fonte já citadas,
sem a deliberação. Isso é o que transforma "reorganizar trabalho manual" em
"eliminar trabalho manual".

**6.2 — Território e estrutura não existem em lugar nenhum.** Se o score e a
conversa só falam do ponto, metade da discussão do comitê continua fora do Órbita,
e meu fio registrado vai parecer incompleto pra quem abrir. No mínimo, a IA
precisa saber dizer "essa análise cobre ponto; território e estrutura não estão
aqui" — senão o "Revisar minha análise" vai me dizer que a análise se sustenta
quando falta metade dela.

**6.3 — Quando eu discordo do número, não existe caminho.** Minha reação nº 1 hoje
é não acreditar no dado e ir conferir fora. Nenhuma das duas specs trata disso.
**Falta "contestar este dado"**, que registra minha discordância e gera chamado
pro time de dados. Isso ataca a causa raiz apontada na descoberta ("falta de
confiança nos números apresentados no Órbita") — que é o problema reportado
original, e o incremento conversacional inteiro passa ao largo dele.

**6.4 — A recusa honesta sobre fluxo vai virar ruído.** O cenário escolhido é
Franca, comércio de rua intenso, e o estudo de score confirma que fluxo de
passantes não é modelado. Se a IA responde "não tenho dado de fluxo" em toda
pergunta, em todo ponto comercial — que é o caso de demonstração —, isso deixa de
ser honestidade e vira disclaimer que eu aprendo a ignorar. **Ajuste: declarar a
tipologia e a limitação uma vez, no topo da montagem ("ponto classificado como
comercial; a régua vigente subestima esse perfil porque pontua residente"), e não
repetir a cada resposta.**

---

## 7. Terminologia

- **"Camada" sumiu das duas specs.** A descoberta e o glossário do projeto falam
  camada — é a palavra que o time usa e que está no Órbita hoje ("inserção de
  camadas", lista de camadas mais usadas). As specs falam bloco, indicador, fonte,
  base de origem. Manter "bloco" para o objeto arrastável da tela é razoável, mas
  **o painel de adicionar tem que falar "camadas"**, senão o time não reconhece o
  próprio vocabulário.
- **"Fonte", "base" e "base de origem" aparecem como sinônimos no mesmo
  documento.** Escolher um termo.
- **"Análise" é ambíguo.** Na jornada são quatro análises (perfil, ponto,
  território, estrutura). "Revisar minha análise" vai ser lido como as quatro.
  Nomear **"revisar esta análise de ponto"**.
- **"Score" mudou de unidade sem ninguém decidir isso.** Hoje o time fala em
  pontos (0–20) e em classificação (alta viabilidade, moderada, não recomendado).
  A spec modular passa a exibir percentual com denominador variável conforme a
  montagem. Consequência que extrapola a conversa e precisa de decisão explícita:
  **a classificação vigente deixa de ser comparável entre análises e com o
  histórico.** A conversa vai expor isso na primeira semana — a IA diz "62%" e no
  comitê perguntam "62% de quê?". Some-se a isso a inconsistência que já está na
  tabela do estudo (faixa 8–11 classificada como "baixa viabilidade / não
  recomendado" mas com status "Recomendado" por ≥34%). Se ninguém resolver isso
  antes, a IA conversável vira a porta-voz de uma contradição que já existe.

---

## 8. Conhecimento prévio — a regra mais rígida da spec trabalha contra o objetivo do produto

"A IA nunca responde com dado que não está na análise atual" é boa para honestidade
e péssima para o que o produto promete eliminar. Exemplo real: 8 concorrentes em
300m é muito ou pouco? A IA ancorada só na tela me devolve o número que eu já
estou vendo. **Quem sabe responder é quem tem anos de casa — exatamente o
conhecimento prévio que o Órbita deveria dispensar.**

**Ajuste:** permitir dado de fora da análise **desde que seja do próprio Órbita** —
histórico de análises aprovadas, lojas já abertas, médias por tipologia — e
rotulado visivelmente como referência, não como dado deste ponto. Sem benchmark, a
conversa é honesta e inútil para quem está começando, que é justamente o público
que a descoberta diz estar sendo deixado de fora ("estamos deixando de considerar
pessoas que não tem a expertise ou anos de experiência").

---

## Resumo do que eu mudaria antes de construir

1. Fio privado por padrão, com anexação seletiva ao comitê; justificativa de
   alerta grave continua obrigatória e visível. **Sem isso, não uso.**
2. "Não concordo" de um clique em todo alerta, e IA capaz de discordar da régua a
   meu favor.
3. Trocar metade dos chips pelas perguntas que eu faço de verdade, começando por
   "esse número bate com o Google?".
4. "Revisar minha análise" sem a parte de elogio, acionado no fechar da análise,
   com saída copiável como pauta de comitê.
5. Delta de score visível antes de aplicar, autoria marcada como minha, desfazer em
   ações destrutivas.
6. Ação de gerar rascunho do feedback e ação de salvar montagem como padrão por
   tipologia — é onde o tempo real é cortado.
7. Decidir a unidade do score (pontos vs. percentual de denominador variável) antes
   de a IA começar a falar dele.

---

## Destino de cada achado

| Achado | Decisão |
|---|---|
| Fio privado + anexação seletiva | **Aplicado** no incremento e no prompt completo |
| "Não concordo" de um clique, com retratação no fio | **Aplicado** |
| IA discorda da régua; procedência e estatuto em toda afirmação | **Aplicado** |
| Teto de alertas proativos | **Aplicado** |
| Chips reformulados ("bate com o Google?", comitê, concorrentes, aluguel) | **Aplicado** |
| Comando principal vira "se sustenta no comitê?", em 3 partes, copiável, no fechar | **Aplicado** |
| Delta de score antes de aplicar, autoria do analista, desfazer | **Aplicado** |
| Uma ação em destaque, resto atrás de "outras opções" | **Aplicado** |
| Salvar montagem como padrão por tipologia | **Aplicado** |
| Simular 500m com antes/depois | **Aplicado** como ação |
| Terminologia: camada, fonte, análise de ponto | **Aplicado** |
| Tipologia e limitação declaradas uma vez, não a cada resposta | **Aplicado** |
| Guard de escopo (cobre ponto, não território/estrutura) | **Aplicado** |
| Proibição de métrica de alertas ignorados por analista | **Aplicado** |
| Gerar rascunho do feedback ao empresário | **Fora de escopo** — feature própria, colide com a regra de privacidade; maior economia de tempo apontada, vale iniciativa separada |
| Benchmark com histórico e lojas abertas | **Fora de escopo** — afrouxa a regra que protege contra resposta inventada; capacidade futura nomeada |
| "Contestar este dado" com chamado ao time de dados | **Em aberto** — ataca a causa raiz da desconfiança, mas é fluxo novo fora da tela de análise |
| Comparar com loja já aberta | **Em aberto** — depende de base de lojas existentes |
| Unidade do score (pontos vs. percentual variável) | **Em aberto** — decisão de produto, já registrada como risco desde o início |
