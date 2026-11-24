# Revisão do analista — modularização, score e gráficos

> Saída integral do subagente `analista-expansao`, executado em 2026-10-06 sobre
> `outputs/prompt-claude-design-orbita-modular.md` (515 linhas, lido na íntegra).
>
> **Natureza deste documento:** avaliação de um subagente que simula a perspectiva
> de quem monta o score de ponto à mão hoje. Não é pesquisa com usuário real e não
> substitui validação com o time de Expansão.
>
> **Escopo:** o assistente conversável já foi revisado em
> `outputs/revisao-analista-expansao-conversa-ia.md` e não é reaberto aqui, exceto
> onde a modularização cria problema novo. Esta rodada cobre: percurso navegável e
> tela de entrada, interações 1, 2, 3, 4 e 6, construtor de gráficos (P1–P6), régua
> de forma, 4 eixos, motor de score, lista de indicadores, terminologia e o cenário
> de Franca.
>
> **Documentos conferidos para checar a régua e o vocabulário:**
> `docs/confluence/ia/analises/estudo-peso-populacao-score-viabilidade.md`,
> `docs/confluence/2025/orbita-descoberta-analise-pontos.md`,
> `docs/confluence/2025/orbita-indicadores.md`,
> `docs/confluence/2025/evolucao-camadas/orbita-evolucao-camadas.md`.
>
> **Severidades:** BLOQUEIA = eu não uso, ou a demo cai na frente do stakeholder.
> AJUSTA = uso, mas perco tempo ou confiança. REGISTRA = anotar, decidir depois.

---

## Resumo dos BLOQUEIA

| # | Achado | Seção da spec |
|---|---|---|
| B1 | Classificação vigente (alta/moderada/baixa) e limiar `scorePercent ≥ 34` sumiram do motor de score | MOTOR DE SCORE |
| B2 | Com denominador variável, **remover um indicador ruim sobe o score** — é matemática, não bug de implementação | MOTOR DE SCORE |
| B3 | Faltam duas das camadas mais usadas: **Lojas Farmarcas (canibalização)** e **Situação de território** | INDICADORES DISPONÍVEIS / Aba CAMADAS |
| B4 | Interação 6 não tem segundo cenário de dados definido, e compara conjunto de indicadores sem comparar **fonte** | INTERAÇÃO 6 / CENÁRIO |
| B5 | Seletor de fonte livre em cada bloco, sem fonte padrão governada, torna análises incomparáveis no comitê | INTERAÇÃO 2 |
| B6 | A tipologia "comércio de rua intenso" não tem origem definida, e a montagem da IA e o EIXO 3 dependem dela | ESTADO PRINCIPAL / EIXO 3 |
| B7 | "Fluxo estimado de comércios no entorno" chamado de **fluxo** — é contagem de POI; o cenário inteiro promete fluxo que o produto não tem | INDICADORES DISPONÍVEIS / INTERAÇÃO 5 |
| B8 | Os dois exemplos do EIXO 2 (população 1/5 **e** densidade baixa a 300m) só coexistem via inflação de setor censitário; na demo alguém faz a conta | EIXO 2 / CENÁRIO |

---

## 1. Fidelidade ao workflow real

### 1.1 A tela de entrada é onde meu trabalho de verdade começa — e ela está vazia

**AJUSTA — seção PERCURSO NAVEGÁVEL / ENTRADA (linhas 48–53)**

A spec descreve a entrada como "dados do lead já preenchidos, um mapa com um pin
arrastável e um slider de raio". Isso é o que a tela mostra hoje, não o que eu faço
nela.

O que eu faço entre receber o lead e clicar em "Explorar com IA":

1. Abro o endereço no Google Maps e no Street View. Confiro se o número existe, se a
   rua é comercial mesmo, se tem calçada, se tem onde parar o carro, de que lado da
   rua é o imóvel, se o ponto já foi farmácia antes (ponto queimado).
2. Conto as farmácias que eu **vejo** na rua. Esse é o número que eu levo pro comitê
   quando o Órbita diverge.
3. Arrasto o pin, porque o empresário mandou o endereço errado — isso a spec tem.

Nada disso entra no produto. A observação de rua morre na minha cabeça ou na minha
planilha, e é justamente a informação que o analista de operações me pede na
passagem de bastão (passo 13 da jornada da descoberta).

**Ajuste concreto:** na tela de entrada, um campo "o que eu vi na rua" que viaja
para dentro da análise de ponto e aparece junto do score, e Street View embarcado
ao lado do mapa. Custa pouco e é o único lugar do protótipo onde entra informação
que nenhuma fonte tem.

### 1.2 Mover o pin precisa mostrar o quanto o número se mexeu

**AJUSTA — seção PERCURSO NAVEGÁVEL / ENTRADA**

A spec diz que arrastar o pin "deve funcionar". Funcionar não basta. O motivo pelo
qual eu arrasto o pin é desconfiança do endereço; o que eu preciso ver é **quanto a
população e a densidade mudaram** quando eu movi 80 metros.

Se um deslocamento de 80 m muda a população em 30%, isso me diz, de graça, que o
número é artefato de setor censitário e que eu não devo levar ele sozinho pro
comitê. É o sinal de confiabilidade mais barato disponível na ferramenta e ele não
está especificado em lugar nenhum.

### 1.3 Falta a checagem de lead duplicado antes do trabalho

**AJUSTA — seção PERCURSO NAVEGÁVEL / ENTRADA**

Já apontei "já teve análise nesse endereço antes?" na rodada anterior, mas lá era um
chip da conversa. No percurso navegável o lugar certo é **outro**: na entrada, antes
de eu gastar 20 minutos. Se já existe análise naquele raio, eu quero saber ao digitar
o endereço, não ao perguntar à IA depois.

### 1.4 Os campos de aluguel e área precisam ser editáveis na entrada

**AJUSTA — ENTRADA (linha 49) vs. INDICADORES DISPONÍVEIS (linhas 444–447)**

A spec diz "dados do lead já preenchidos" e, mais adiante, que o custo por m² é
"calculado a partir do valor de aluguel e da área de venda que o analista já informou
na entrada". Se esses campos vierem travados no protótipo, a demonstração mais forte
da modularização — mexer no aluguel e ver o custo por m² e o score reagirem — não
acontece. O empresário manda número errado de área com a mesma frequência com que
manda endereço errado.

### 1.5 A transição de 1 a 2 segundos vende uma expectativa que não se cumpre

**REGISTRA — ENTRADA (linhas 51–53)**

Hoje a espera é bem maior. Para protótipo está certo; só não deixe ninguém sair da
demo achando que o tempo de resposta faz parte da entrega.

### 1.6 A montagem persistir só "enquanto a sessão estiver aberta" contradiz o resto da spec

**AJUSTA — INTERAÇÃO 1 (linha 70)**

Três níveis de persistência convivem na spec sem se falarem:

- montagem = só na sessão (linha 70);
- justificativa de alerta grave = permanente e "visível para quem abrir depois"
  (linhas 116–117);
- padrão salvo por tipologia = atravessa análises (linhas 391–397).

Se a montagem não persiste, a justificativa permanente aponta para um arranjo que
não existe mais, e quem abrir minha análise no comitê vê um score diferente do que
eu apresentei. **A montagem É a análise.** Para o protótipo, declare isso como
limitação do protótipo; para o produto, a montagem tem que ser salva com a análise
de ponto.

---

## 2. Terminologia

### 2.1 "Fluxo estimado de comércios no entorno" não é fluxo

**BLOQUEIA (B7) — INDICADORES DISPONÍVEIS (linha 449) e INTERAÇÃO 5 (linhas 109–111)**

Duas coisas erradas no mesmo nome:

- "Fluxo de comércios" não quer dizer nada. Comércio não flui. Ou é fluxo de
  pessoas, ou é quantidade/densidade de comércio.
- O exemplo da interação 5 diz: "você tirou o único indicador que captura fluxo num
  ponto onde a população residente é baixa". Contagem de POI **não captura fluxo** —
  é um proxy, e um proxy fraco. O estudo de score é explícito: "não há modelagem
  explícita de fluxo de passantes", e índice comercial por POI aparece lá como
  possibilidade futura de **médio prazo**.

Isso importa porque o cenário escolhido para a demo (comércio de rua intenso, "a
montagem padrão da IA deve privilegiar fluxo") monta a narrativa inteira em cima de
um dado que o produto não tem. Alguém do time vai perguntar "de onde vem esse fluxo?"
e a resposta honesta é "é contagem de padaria e loja de roupa".

**Ajuste:** renomear para **"Densidade de comércio no entorno (proxy de fluxo)"** e
reescrever o alerta da interação 5 como "você tirou o único **proxy** de movimento
num ponto onde a população residente é baixa". Perde pouco de impacto e ganha a
credibilidade inteira.

### 2.2 "Pirâmide etária" é a palavra do time; a spec fala "faixa etária"

**AJUSTA — P3 (linhas 157–160) e INDICADORES DISPONÍVEIS (linha 448)**

A descoberta lista as camadas que o time mais usa e lá está **"Pirâmide etária"**,
não "faixa etária". Dois efeitos:

- vocabulário: o painel precisa falar pirâmide etária para o time reconhecer a
  camada que ele já usa;
- dado: pirâmide etária tem recorte por sexo. P3 recomenda "colunas com rampa
  ordinal de uma única cor" em 5 faixas e joga o sexo fora. Pode ser decisão
  consciente, mas então diga que é — hoje parece desconhecimento da camada.

### 2.3 Três blocos listados como INDICADORES não são indicadores

**AJUSTA — INDICADORES DISPONÍVEIS (linhas 439–441)**

"Prós e contras gerados por IA", "Comentário do analista" e "Score de viabilidade"
estão na lista de indicadores. Nenhum dos três é indicador: não vem de camada, não
tem fonte, não pontua.

Isso contradiz a própria regra da spec: a aba GRÁFICOS exige o selo permanente "não
entra no score" para "o analista nunca confundir com indicador" (linhas 94–96). A
mesma confusão está sendo criada na lista de indicadores. **O selo "não entra no
score" tem que valer para todo bloco não pontuável, não só para gráfico.**

E a regra da linha 451 ("cada indicador precisa ter pelo menos duas fontes
alternativas") fica impossível de cumprir nesses três — e também no custo por m²,
cuja única fonte sou eu digitando na entrada.

### 2.4 "Custo do ponto" não é camada puxada de fonte conectada

**AJUSTA — INTERAÇÃO 3, aba CAMADAS (linhas 88–91)**

A aba CAMADAS "lista o que pode ser puxado das fontes conectadas", agrupado por tema,
e um dos temas é "custo do ponto". Custo do ponto não vem de fonte nenhuma: é conta
em cima do que eu digitei. Marque esse bloco como **derivado de entrada do analista**
e tire o seletor de fonte dele, senão o primeiro clique no seletor mostra uma lista
vazia ou inventada.

### 2.5 "Mesorregião" não é palavra do meu comitê

**AJUSTA — P2 (linhas 148–155)**

Ver item 3.2. Ninguém no comitê pergunta como o ponto está em relação à mesorregião
de Franca.

### 2.6 Classe econômica: P4 e a régua usam nomenclaturas diferentes

**AJUSTA — P4 (linha 163) vs. MOTOR DE SCORE (linha 422)**

P4 lista as classes como "A, B1/B2, C1/C2, D/E". A régua vigente usa **"A++/A+"**.
São rótulos diferentes para a mesma dimensão na mesma tela. Quem olhar o gráfico e
depois a composição do score vai achar que são coisas distintas.

### 2.7 A limitação da densidade é mais enganosa que a da população, e não está na spec

**AJUSTA — INTERAÇÃO 2 (linhas 79–82)**

A spec traz muito bem a limitação da população (soma dos setores que intersectam).
Mas a limitação da **densidade** é pior e está ausente: pelo estudo,
`demographicDensity` é a **média da densidade dos setores**, não população dividida
pela área do raio. São duas métricas com significados diferentes, e a densidade é a
que tem lógica invertida no score — ou seja, é a que mais pontua e a que menos se
explica. A linha de limitação do bloco de densidade é mais necessária que a de
população.

---

## 3. O catálogo de 6 perguntas — o que eu pergunto e o que não

### Veredito pergunta a pergunta

| Pergunta | Veredito |
|---|---|
| **P1** — como o indicador muda com o raio | **Faço toda análise.** Melhor pergunta do catálogo. Mas a forma recomendada está errada — ver 3.1. |
| **P2** — ponto vs. cidade, mesorregião e estado | **Faço um terço dela.** Cidade sim. Mesorregião e estado, nunca. Ver 3.2. |
| **P3** — distribuição por faixa etária | **Não é assim que eu pergunto.** Ver 3.3. |
| **P4** — renda por classe econômica | **Faço, mas o dado pode não existir.** Ver 3.4. |
| **P5** — quais bandeiras concorrentes no raio | **Pergunta certa, resposta errada.** Falta distância. Ver 3.5. |
| **P6** — tipos de comércio no entorno | **Quase nunca nessa forma.** O que eu procuro é gerador de fluxo, não composição. Ver 3.6. |

### 3.1 P1 — linha num dado que é escada, e a própria spec proíbe isso

**AJUSTA forte — P1 (linhas 141–146) vs. RÉGUA DE FORMA (linhas 199–200)**

P1 recomenda LINHA para o mesmo indicador a 100m, 300m, 500m e 1000m. Mas a
população por raio **não é curva, é escada**: o backend soma os setores inteiros que
intersectam o círculo. Passar de 290 m para 310 m pode não mudar nada, e passar de
310 m para 330 m pode acrescentar um setor inteiro de 4.000 habitantes de uma vez.

A régua de forma da própria spec diz, três seções abaixo: "linha afirma continuidade
onde não existe". É exatamente o que P1 faz. E com a densidade é pior, porque ela é
média de setores — ela pode **cair** quando o raio aumenta, e a linha vai sugerir uma
tendência que é só troca de amostra.

**Ajuste:** forma recomendada = **colunas nos quatro raios**, com o raio atual
destacado, mais a quantidade de setores censitários somados em cada raio exibida.
Se insistir em linha, use linha em degrau (step), não interpolada.

### 3.2 P2 — corta mesorregião e estado; a comparação que eu faço é outra

**AJUSTA — P2 (linhas 148–155)**

Minha comparação real, em ordem de uso:

1. este ponto contra **a cidade** — uso, mas como contexto, não como argumento;
2. este ponto contra **outra loja nossa já aberta** que se parece com ele — **é o
   argumento que mais convence comitê**, disparado;
3. este ponto contra **o outro endereço que o mesmo empresário mandou**.

Mesorregião e estado não entram em nenhuma discussão minha. A própria spec já marca
P2 como "comparativo territorial — recorte a confirmar" porque os agregados não foram
validados. Então: valide o recorte **cidade** e corte os outros dois. Um recorte
confirmado vale mais que três não confirmados.

(Comparar com loja aberta já foi registrado como "em aberto" na rodada anterior. Só
reforço que ele reaparece aqui como **a** pergunta de gráfico, não só como chip.)

### 3.3 P3 — eu não pergunto distribuição, eu pergunto 60+

**AJUSTA — P3 (linhas 157–160)**

Em farmácia, a faixa etária não é uma curva que eu leio: é **uma pergunta só**.
"Quanto desse raio tem 60 anos ou mais?" Idoso é uso contínuo, uso contínuo é
recorrência, recorrência é o faturamento que sustenta o aluguel. A segunda, bem
depois, é 0–14 (puericultura, fralda, leite).

Um gráfico de cinco colunas me faz ler cinco números para extrair um. Pela régua de
forma da própria spec, "gráfico de uma barra só é um indicador, não um gráfico" —
pois é: **o que eu quero aqui é um indicador "% da população com 60+", não um
gráfico.** O gráfico de 5 faixas serve como detalhe sob demanda, não como resposta.

**Nas minhas palavras, a pergunta que falta:** *"Tem idoso suficiente aqui pra
sustentar uso contínuo?"*

### 3.4 P4 — a régua vigente trabalha com renda MÉDIA, não com distribuição

**AJUSTA — P4 (linhas 162–166) vs. MOTOR DE SCORE (linhas 421–423)**

O indicador vigente é "Classificação econômica (**renda média**)" — um valor, uma
classe para a área. P4 pede a **distribuição da população por classe**. É outro dado,
de outra camada. A spec assume que ele existe e não diz de onde vem.

Se a distribuição existir, ótimo, e aí vem a pergunta óbvia no comitê: o score usa a
média (que cai em C1/C2 e vale 3 pontos) enquanto o gráfico mostra que metade do raio
é D/E e a outra metade é B. Média de classe econômica em bairro misto é das coisas que
mais enganam. **Se a distribuição existe, ela deveria estar no score, não só no
gráfico.** Decida e declare.

### 3.5 P5 — a pergunta é certa, mas sem distância a resposta não decide nada

**AJUSTA forte — P5 (linhas 167–171)**

Concorrência é a camada que eu mais uso (está em primeiro lugar na lista de camadas
mais usadas da descoberta) e é a primeira coisa que o comitê pergunta. Então P5 merece
estar aí.

Mas barras horizontais de contagem por bandeira joga fora a informação que decide:
**a distância e o lado da rua.** Três Pague Menos a 280 m é um ponto; três Pague Menos
a 50 m, na mesma calçada, é outro ponto completamente diferente — e os dois produzem
exatamente o mesmo gráfico.

**Ajuste:** a forma recomendada para P5 é **lista ordenada por distância** (bandeira,
distância em metros, lado da via quando houver) **com os marcadores no mapa**, e o
gráfico de contagem por bandeira como alternativa. O mapa já está na tela e a spec diz
que ele é "integrado, não decorativo" — use para isso.

### 3.6 P6 — composição de comércio não me ajuda; gerador de fluxo sim

**AJUSTA — P6 (linhas 172–176)**

Saber que tem 12 lojas de roupa, 8 padarias e 5 lanchonetes não muda minha decisão.
O que muda é se o raio tem **gerador de fluxo de saúde ou de alta frequência**:
hospital, UBS, clínica, laboratório, supermercado, terminal de ônibus, lotérica,
banco, escola. O cenário da própria spec diz "perto de hospital e supermercado" — isso
é a informação que importa, e P6 a dilui no meio de uma composição de 7 categorias.

**Nas minhas palavras, a pergunta que falta:** *"Esse ponto pega o fluxo de quê?"* —
resposta: lista de geradores no raio, com distância, destacando os de saúde.

### 3.7 As perguntas que eu faço toda semana e não estão no catálogo

Nas minhas palavras, em ordem de frequência:

1. **"Onde estão os concorrentes em relação ao meu ponto, e de que lado da rua?"**
   (ver 3.5 — é a P5 feita direito)
2. **"Esse ponto pega o fluxo de quê?"** (ver 3.6)
3. **"Quanto do raio é vazio?"** — não está em lugar nenhum da spec. Em Franca, com a
   indústria de calçado, um raio de 300 m pode ter galpão, chácara, avenida larga,
   córrego. Se 40% do raio é não residencial, população e densidade estão os dois
   mentindo e o score inteiro é construído em cima disso. A pergunta é: *"desse
   círculo, quanto é gente morando e quanto é galpão?"*
4. **"Tem loja nossa perto? Eu vou canibalizar alguém?"** — ver B3, seção 6.1. Pergunta
   de comitê garantida, e não existe no catálogo nem na lista de indicadores.
5. **"Tem idoso suficiente pra sustentar uso contínuo?"** (ver 3.3)
6. **"Esse dado é de quando? A rua mudou desde então?"** — censo 2022, análise 2026. Em
   rua comercial quatro anos muda tudo. Não é gráfico, é um carimbo de data-base que a
   spec já prevê no bloco (linha 76) — só precisa estar **no gráfico também**, porque é
   o gráfico que vai pro comitê.

---

## 4. Conhecimento prévio exigido

### 4.1 Trocar a fonte de um indicador: eu não faria, e se fizesse não defendo

**BLOQUEIA (B5) — INTERAÇÃO 2 (linhas 74–82) e linha 451**

Resposta direta: **não, eu não sei escolher entre duas fontes, e esse é exatamente o
tipo de decisão que o produto deveria estar tirando de mim.**

Pôr um seletor de fonte em todo bloco é transferir uma decisão metodológica para quem
não tem como tomá-la. O CLAUDE.md do projeto diz que a expectativa é "reduzir
progressivamente o conhecimento prévio"; a interação 2 anda na direção contrária. Hoje
eu não escolho fonte — eu desconfio do número e vou conferir no Google. O problema
reportado na descoberta é literalmente "falta de confiança nos números". Um dropdown de
fontes não resolve desconfiança: ele a institucionaliza e me dá duas versões em vez de
uma.

**O que aconteceria no comitê:** eu uso a fonte A para população, o colega usa a B. Os
dois scores saem como percentual, os dois parecem comparáveis, e a discussão deixa de
ser sobre o ponto e passa a ser sobre metodologia. Em três comitês, o time cria uma
regra informal de "todo mundo usa a fonte padrão" — e aí o seletor virou enfeite que só
gera risco.

**O que eu precisaria ver no bloco para ter segurança de trocar:**

1. qual é a fonte **padrão da Farmarcas** para aquele indicador, marcada como padrão;
2. data-base das duas;
3. **cobertura**: o que cada fonte cobre e o que ela não cobre (ex.: a base de
   concorrência pega farmácia independente ou só rede?);
4. **a divergência entre elas em número**: "as duas fontes discordam em 38% neste raio";
5. se já houve análise aprovada usando a fonte alternativa.

**Ajuste que eu defendo, e que é mais barato que o seletor:** inverter a mecânica. A
fonte padrão é **governada e travada**, e a segunda fonte entra como **sinal de
divergência**, não como opção de menu: quando as duas discordam acima de um limiar, o
bloco acende e diz "estas duas fontes discordam em 38% aqui — confira". Isso é o
princípio de "destacar o que precisa de atenção humana" aplicado direito. A troca
continua possível, mas vira exceção justificada (mesmo tratamento do alerta grave:
registra o motivo, fica visível), não ação de rotina.

**No mínimo, se o seletor ficar como está:** qualquer indicador fora da fonte padrão
tem que acender **no cabeçalho da análise de ponto**, não só dentro do bloco, e tem que
aparecer na comparação da interação 6 (ver 4.3).

### 4.2 A tipologia do ponto aparece do nada

**BLOQUEIA (B6) — ESTADO PRINCIPAL (linhas 55–60), EIXO 3 (linhas 228–231), CENÁRIO (linha 513)**

Toda a inteligência da tela depende de uma frase: "região de comércio de rua intenso".
Dela saem a montagem proposta pela IA, o EIXO 3 inteiro (pertinência ao tipo de ponto)
e a declaração única de limitação no topo.

A spec nunca diz **de onde vem essa classificação**. No Órbita hoje ela não existe; o
estudo de score lista "tipologia de mercado (flag residential / mixed /
commercial_high_traffic)" como possibilidade de **médio prazo**, ainda não feita.

Na demo, a primeira pergunta vai ser "como ele sabe que isso é rua comercial?". Se a
resposta for "está escrito no cenário", a feature vira mágica e o resto da discussão
não acontece.

**Ajuste:** a tela mostra a tipologia **com o critério ao lado, clicável** — ex.
"classificado como comércio de rua: densidade de comércio alta + população residente
baixa no raio" — e com a opção de o analista **corrigir a tipologia em um clique**, o
que remonta a tela. Isso é honesto, é demonstrável e me dá o único controle da montagem
que realmente importa.

### 4.3 Comparação entre análises: eu comparo pontos, não metodologias

**BLOQUEIA (B4) — INTERAÇÃO 6 (linhas 125–129) e CENÁRIO (linhas 508–515)**

**Eu comparo pontos hoje? Sim — mas não do jeito que a spec propõe.** As três
comparações que eu faço, em ordem de frequência:

1. **o mesmo ponto em dois raios** (300 m e 500 m). Essa é diária. A spec já cobre com
   a ação "simular 500m e mostrar antes e depois lado a lado" — e é a melhor coisa da
   spec nesse tema.
2. **dois endereços do mesmo empresário.** Ele manda duas opções e eu preciso dizer
   qual. É a comparação que o comitê me pede nominalmente, e ela não está na spec.
3. **este ponto contra uma loja nossa já aberta parecida.** Registrada como "em aberto"
   na rodada anterior.

A interação 6, do jeito que está, compara **"esta análise com outra, montada com um
conjunto diferente de indicadores"**. Isso não é comparação de pontos: é comparação de
metodologias. Quem tem essa dúvida é o time de produto, não eu.

E o resultado principal da feature, como especificado, é um aviso: "sinalizar de forma
inequívoca que os dois scores NÃO são equivalentes". Uma tela cuja entrega principal é
um disclaimer não corta passo nenhum do meu trabalho.

**Dois ajustes, e a feature passa a servir:**

- **Recalcular os dois scores restritos ao subconjunto comum** e apresentar esse número
  como o comparável, com os indicadores exclusivos de cada lado listados fora da conta.
  Isso transforma o aviso em resposta. Hoje, quando duas análises não batem, eu refaço
  uma na mão para igualar — é esse o passo manual a eliminar.
- **Comparar fonte, não só conjunto de indicadores.** Duas análises com exatamente os
  mesmos indicadores mas fontes diferentes parecem comparáveis e não são (ver 4.1). A
  comparação tem que mostrar divergência de fonte com o mesmo destaque que dá à
  divergência de indicador.

**E a falha de spec que trava a construção:** a seção CENÁRIO define **um** ponto (Lead
1223, Franca). A interação 6 precisa de **dois**. Nenhum segundo cenário está
especificado — nem endereço, nem indicadores, nem valores. Quem construir vai inventar,
e a restrição da linha 478 ("os números precisam ser internamente consistentes... alguém
vai conferir na frente do stakeholder") cai justamente na tela de comparação, que é onde
dois conjuntos de números ficam lado a lado.

**Sugestão de segundo cenário, coerente com o argumento do produto:** o mesmo Lead 1223
com o pin a 400 m dali, numa quadra residencial — mesmo empresário, duas opções. Cobre a
comparação 2 da minha lista, usa dados da mesma cidade (consistência mais fácil) e
demonstra o ponto da modularização melhor do que comparar com um ponto aleatório: mesma
cidade, montagens diferentes, **porque os pontos são de naturezas diferentes**.

---

## 5. Redução de passos manuais

### 5.1 Montar a tela: para mim é trabalho A MAIS na maioria das análises

**AJUSTA, mas é o achado que mais muda a prioridade do que construir — INTERAÇÃO 1 (linhas 66–72)**

Resposta direta: **arrastar bloco é a interação menos valiosa da spec inteira, e
"salvar montagem como padrão" é a mais valiosa.**

Por quê. Hoje a tela vem pronta e igual. Isso tem um custo (a rua comercial é
penalizada) e um benefício que ninguém está contando: **eu não decido nada, e todas as
análises são comparáveis entre si.** A modularização resolve o custo e destrói o
benefício, e a spec só fala do custo.

Volume: pelo `orbita-indicadores.md`, o time fez entre 28 e 46 análises por mês em 2025
(média ~37), ou seja ~9 por semana no time inteiro. Das que passam por mim, a grande
maioria é bairro residencial comum, onde a tela padrão responde. **Eu mexeria na
montagem em 1 a 3 análises por semana, no máximo** — pontos de rua comercial, pontos
dentro de galeria ou supermercado, e os casos em que o comitê devolveu pedindo um dado
específico.

Nas outras, se a IA mexer na montagem, ela me deu trabalho novo: eu tenho que **ler a
montagem dela e decidir se concordo** — um passo que hoje não existe. O aviso da linha
57 ("um aviso discreto e dispensável da própria IA explicando por que ela escolheu
aquele arranjo") é bem-intencionado, mas é leitura obrigatória antes de eu confiar no
score, por mais discreto que seja.

A spec diz "a IA já monta e você só edita". Isso é verdade na prática **se e somente se**
três coisas forem verdade:

1. **Existe a montagem padrão da casa, e ela é um clique.** Um botão "usar a montagem
   padrão" sempre visível, que volta a tela ao arranjo de sempre. Sem isso, toda análise
   vira uma negociação com a IA.
2. **A IA só remonta quando a tipologia foge do comum.** Em ponto residencial padrão, a
   IA deveria entregar a tela de sempre **e dizer que entregou a de sempre** — "ponto
   residencial típico, montagem padrão". Isso me economiza a leitura e, de quebra, torna
   o aviso informativo nos casos em que ela realmente mudou algo.
3. **Padrão salvo por tipologia é visível desde a primeira tela**, não escondido como
   ação da conversa. A spec já o tem (linhas 391–397) e já o reconhece como "a única
   economia que se acumula". Concordo inteiramente — então ele não pode depender de eu
   pedir à IA. Na entrada, junto do raio, deveria ter "montagem: padrão rua comercial
   (usada em 14 análises)".

**Em resumo:** a modularização vale pela **tipologia + padrão salvo**, não pelo arrastar.
Se o protótipo gastar a demo mostrando bloco sendo arrastado, ele vende a parte que não
me economiza tempo.

### 5.2 Adicionar e remover blocos: aqui corta trabalho de verdade

**REGISTRA (positivo) — INTERAÇÃO 3 (linhas 84–96)**

Essa funciona. Custo por m² é o melhor exemplo possível: o dado já é coletado, já está na
minha mão, e hoje não entra em lugar nenhum — eu faço essa divisão na calculadora e anoto
na planilha. Tirar ele da planilha e pôr na análise, com entrada no score, corta passo
real.

Gráfico não entrar no score, com selo permanente, está certo e eu não discuto.

Duas ressalvas:

- **o custo por m² precisa declarar o denominador.** A spec diz "calculado a partir do
  valor de aluguel e da área de venda" (R$ 4.000 / 200 m² = R$ 20,00/m²), mas o cenário
  também dá a área total (R$ 4.000 / 350 m² = R$ 11,43/m²). Os dois números vão existir
  na cabeça de quem olha. Se o bloco não disser qual base usou, o indicador fica
  incomparável entre análises — e comparar custo por m² entre pontos é exatamente para o
  que ele serve.
- **a régua proposta do custo por m² precisa de âncora.** A spec diz "crie uma régua de 0
  a 5 coerente" (linhas 425–427). Coerente com o quê? R$ 20/m² é caro ou barato? Quem sabe
  responder é quem tem anos de casa — o conhecimento prévio que o produto quer eliminar. A
  âncora disponível está no próprio Órbita: a tela **Contratos Fechados**. Derive as faixas
  dos contratos já fechados e diga isso na interface ("faixa derivada de N contratos
  fechados, régua ainda não homologada"). Uma régua inventada num indicador que ninguém
  sabe ler é pior que não ter o indicador.

### 5.3 O que continua fora: a transcrição para a planilha

**REGISTRA — já apontado na rodada anterior, reaparece aqui por outro caminho**

Os passos 7 a 10 da jornada (planilha de análise de ponto, território e estrutura em
fontes externas, feedback, PDF) continuam intocados. Não repito o argumento. Registro só
o efeito **sobre a modularização especificamente**: se a montagem não persiste (ver 1.6) e
eu transcrevo para a planilha, a planilha vira a versão oficial da análise e a montagem
modular vira rascunho. Aí a feature inteira perde o sentido.

---

## 6. Camadas faltando ou irrelevantes

### 6.1 Faltam camadas que estão na lista das mais usadas pelo time

**BLOQUEIA (B3) — INDICADORES DISPONÍVEIS (linhas 430–449) e aba CAMADAS (linhas 88–91)**

A descoberta lista nominalmente as camadas que o time mais usa no Órbita:
Concorrentes, Densidade demográfica, Renda média, **Setor Censitário**,
Residentes|População, Pirâmide etária, Potencial de consumo, **Situação de território**.
A página de evolução de camadas cita também a camada **Lojas Farmarcas**.

Três dessas não aparecem na spec:

1. **Lojas Farmarcas (canibalização).** Esta é a mais grave. A spec cobre concorrente e
   esquece a nossa própria rede. Num time de Expansão, "eu estou abrindo em cima de um
   associado nosso?" é pergunta de comitê garantida — e é a única que pode reprovar um
   ponto com score alto. Um score que considera o concorrente a 200 m e ignora a
   Farmarcas a 180 m não é um score de viabilidade. **Precisa estar entre os indicadores
   que vêm montados por padrão, não no painel de adicionar.**
2. **Situação de território.** Está na lista de camadas mais usadas. *Inferência minha,
   confiança média, a confirmar com o time:* tem a ver com território já ocupado /
   exclusividade de associado existente. Se for isso, é um **gate**, não um indicador —
   reprova o ponto independentemente do score, e precisa aparecer antes de qualquer
   pontuação, não como bloco arrastável de 0 a 5. Confirmar antes de modelar.
3. **Setor Censitário.** Hoje eu abro essa camada justamente para **ver o desenho dos
   setores no mapa** e entender o quanto o número está inflado. A spec substitui isso por
   uma linha de texto no bloco (linhas 79–82). A linha de texto é boa, mas não resolve: eu
   preciso **ver** os polígonos sobre o círculo para saber se o excesso é grande ou
   pequeno. É o remédio direto para o B8 (ver 8.3) e para a desconfiança nos números, que
   é o problema reportado original.

**Ajuste na aba CAMADAS:** os grupos propostos são "demografia, renda, concorrência,
comércio, custo do ponto". Falta um grupo: **território e rede própria** (lojas Farmarcas,
situação de território, setor censitário).

### 6.2 Camada proposta que eu cortaria

Nenhum indicador da lista é inútil. O que eu corto é recorte de gráfico: mesorregião e
estado em P2 (ver 3.2).

---

## 7. Motor de score

### 7.1 Conferência das faixas transcritas, linha a linha

Conferi a seção MOTOR DE SCORE (linhas 408–423) contra
`docs/confluence/ia/analises/estudo-peso-populacao-score-viabilidade.md`.

| Dimensão | Transcrição confere? |
|---|---|
| População (linhas 410–412) | **Confere.** >200.000=5, 120.000–199.999=3, 20.000–119.999=2, 10.000–19.999=1, <10.000=0 |
| Densidade, lógica inversa (linhas 414–415) | **Confere.** ≤5.000=5, 5.001–10.000=3, 10.001–25.000=2, >25.000=0 |
| Potencial de consumo (linhas 417–419) | **Confere.** >2MM=5, 1,5–2MM=4, 1–1,499MM=3, 500k–999k=2, <500k=1 |
| Classificação econômica (linhas 421–423) | **Confere.** A++/A+ ≥19.024,01=0; B1/B2 4.508,01–19.024=1; C1/C2 1.275,01–4.508=3; D/E ≤1.275=5 |

**Os valores estão certos.** Mas a transcrição está **incompleta em dois pontos
críticos**, e a incompletude é mais perigosa do que erro de número seria.

### 7.2 O que foi deixado de fora da régua vigente

**BLOQUEIA (B1) — MOTOR DE SCORE (linhas 399–428)**

Ficaram de fora da spec duas regras vigentes que estão na mesma tabela do estudo:

**(a) A classificação final.** 16–20 = alta viabilidade; 12–15 = viabilidade moderada;
8–11 = baixa viabilidade; <8 = não recomendado. **É nisso que o comitê fala.** Ninguém na
sala diz "o ponto deu 55%" — dizem "deu viabilidade moderada". A spec exibe só percentual
e apaga o vocabulário que a reunião usa.

**(b) O limiar de recomendação: `scorePercent ≥ 34` = Recomendado.** Esse número determina
o status na tela hoje, e ele some completamente da spec. Com denominador fixo em 20, 34% ≈
6,8 pontos. Com denominador variável, 34% de uma montagem de 30 pontos são 10,2 pontos. **O
limiar continua parecendo o mesmo e passa a significar outra coisa.** É a quebra silenciosa
— ninguém percebe, porque o número na tela não muda.

**(c) Registre também a contradição que já existe na régua vigente:** a faixa 8–11 é
classificada como "baixa viabilidade / não recomendado" **e** aparece com status
"Recomendado" por estar acima de 34%. Já levantei isso na rodada anterior; aqui é relevante
porque a spec do motor de score é o lugar onde essa contradição deveria ser resolvida ou
declarada, e ela simplesmente não aparece.

**(d) Detalhe de implementação com efeito real:** potencial de consumo **nunca dá 0** — o
piso da régua é 1. Então o score mínimo com as quatro dimensões vigentes é 1/20 = 5%, não
0%. Se as réguas propostas (concorrência, comércio, custo por m²) tiverem 0 de verdade, a
distribuição do score muda quando elas entram. Quem implementar precisa saber disso, senão
vai "corrigir" o piso 1 achando que é erro.

**(e) Buraco pequeno nas faixas, herdado do estudo:** população exatamente igual a 200.000
não cai em nenhuma faixa ("acima de 200.000" e "120.000 a 199.999"). Na prática nunca
acontece num raio de 300 m, mas o código precisa de uma decisão. REGISTRA.

### 7.3 Percentual de um máximo variável: quebra minha comparação, e tem efeito pior

**BLOQUEIA (B2) — MOTOR DE SCORE (linhas 399–403)**

Resposta direta: **não funciona pra mim, e o problema maior não é a comparação com o
histórico — é que o score passa a subir quando eu apago má notícia.**

**O problema de fundo, em números.** Suponha uma análise com 10 de 20 pontos = 50%. A
população deu 1 de 5 (ponto de rua comercial, poucos residentes — exatamente o cenário de
Franca). Eu removo o bloco de população, porque "não se aplica a este ponto":

> (10 − 1) / (20 − 5) = 9 / 15 = **60%**

Apaguei o indicador que me prejudicava e o ponto virou melhor. Isso não é bug que se
conserta na implementação: **é a aritmética do percentual com denominador variável.**
Remover qualquer indicador que esteja abaixo da média da montagem sempre sobe o score.

E a spec me dá a ferramenta para isso em um arrasto (interação 3: "remover tira a
contribuição do score na hora"), com a tela de resultado toda montável por mim. O alerta
grave cobre um caso específico (remover o indicador de movimento num ponto de rua), mas o
incentivo é estrutural e vale para todos os indicadores.

Isso se descobre **na primeira semana**, e no dia em que alguém descobrir, ninguém no
comitê acredita em score de novo. É o risco mais sério de toda a spec, porque ataca
exatamente o problema reportado original — desconfiança nos números.

**Os outros dois efeitos, menores mas reais:**

- **comparação com análises antigas morre.** Eu tenho um ano de análises em 0–20, e a
  classificação (alta/moderada/baixa) é a linguagem do comitê e da planilha. Com
  denominador variável, nada disso é comparável e a classificação não tem como ser
  calculada;
- **réguas não homologadas contaminam o score inteiro.** A spec marca os blocos novos como
  "régua proposta, ainda não homologada" (linha 427) — mas quando eles entram no numerador
  **e no denominador**, o número final deixa de ser o score vigente. O bloco é marcado; **o
  score não é.** E é o score que eu levo pro comitê.

**O ajuste que eu defendo, e que resolve os três de uma vez:**

A tela mostra **dois números, sempre, lado a lado**:

1. **SCORE VIGENTE — X de 20, classificação Y.** Calculado só com as quatro dimensões
   homologadas, independentemente do que eu montei na tela. Imune à montagem, imune à
   remoção de bloco, comparável com todo o histórico e com a planilha. **É este que vai pro
   comitê.**
2. **LEITURA DA MONTAGEM — Z%**, com a composição visível e o selo "inclui régua ainda não
   homologada" quando for o caso. É a leitura adaptada ao tipo de ponto, é o argumento da
   modularização, e é honestamente rotulada como ainda não vigente.

Isso custa uma linha a mais na tela e resolve: o gaming (o vigente não se mexe), a
comparação com o histórico, a linguagem do comitê, o limiar de 34% e a separação entre
régua homologada e proposta. Também é o que torna a modularização **vendável**
internamente: ela deixa de ser "mudamos o score de vocês" e passa a ser "mantivemos o score
de vocês e acrescentamos uma leitura".

E o "delta de score antes de aplicar" que já está na spec (linha 376) fica melhor assim:
"+8 no numerador, +5 no máximo, leitura vai de 55% para 58% — **score vigente não muda**".

---

## 8. Sinalização de atenção

### 8.1 Os quatro eixos estão na ordem errada de prioridade

**AJUSTA — A IA DE APOIO APLICADA AOS GRÁFICOS (linhas 206–242) vs. teto de três alertas (linha 250)**

Os quatro eixos estão certos como conceito. O problema é de orçamento de atenção.

O EIXO 1 (adequação da forma) tem **oito regras determinísticas** atrás dele (a RÉGUA DE
FORMA inteira). Ele vai disparar o tempo todo. E a spec define um teto de três alertas
proativos seguidos. Resultado: **as regras de forma consomem o orçamento e o EIXO 2 nunca
fala** — e o EIXO 2 é o único que muda minha decisão. A própria spec diz que ele é "o eixo
mais valioso" (linha 215) e que o EIXO 1 é "a crítica mais objetiva e a que o analista
aceita sem resistência" (linha 212). Exatamente: é a que eu aceito sem resistência, logo é
a que **não precisa gastar alerta.**

**Ajuste:** erro de forma não é alerta — é correção silenciosa **dentro do bloco do
gráfico**, com um "ajustar" de um clique. Só EIXO 2, 3 e 4 entram no fio e no teto de três.
Prioridade de disparo: **EIXO 2 > EIXO 4 > EIXO 3 > EIXO 1**.

### 8.2 A régua de forma em si: eu aceito e não discuto

**REGISTRA (positivo) — RÉGUA DE FORMA (linhas 180–204)**

As oito regras são corretas e o enquadramento está certo: elas são objetivas e eu não tenho
argumento contra. "Dois eixos Y inventa correlação que o dado não tem" e "gráfico de uma
barra só é um indicador, não um gráfico" são exatamente o tipo de coisa que eu erro sem
perceber e aceito sem briga.

Duas observações, ambas de contradição interna da spec:

- a regra "linha em dado categórico" é violada pela recomendação de P1 (ver 3.1);
- a regra "gráfico de uma barra só é indicador" é violada por P3 na prática (ver 3.3),
  porque o que eu quero de faixa etária é um número só.

### 8.3 EIXO 2: os exemplos são os certos, mas um deles derruba a demo

**BLOQUEIA (B8) — EIXO 2 (linhas 217–224) e CENÁRIO (linhas 508–515)**

O EIXO 2 é a melhor ideia da spec inteira. "A densidade pontuou alto por ser baixa a 300m,
mas o gráfico de raio mostra que ela sobe de faixa a partir de 500m — o ponto forte do seu
score depende do raio escolhido" é literalmente o que eu quero que alguém me diga antes do
comitê. Isso é sinalização de atenção feita direito.

**O problema está nos números.** Dois exemplos do EIXO 2, no mesmo cenário:

- "A população pontuou 1 de 5" → pela régua, isso é entre 10.000 e 19.999 residentes;
- "a densidade pontuou alto por ser baixa a 300m" → pela régua, densidade ≤ 10.000 hab/km²
  (3 ou 5 pontos).

Raio de 300 m = π × 0,3² = **0,283 km²**. Dez mil habitantes nessa área dariam **~35.400
hab/km²** — faixa "alta", 0 pontos em densidade. Os dois exemplos parecem se contradizer na
cara de quem fizer a divisão, e **alguém vai fazer**: a própria spec avisa que "alguém vai
conferir na frente do stakeholder" (linha 478).

Tecnicamente os dois **podem** coexistir, porque população soma os setores inteiros que
intersectam e densidade é a média dos setores — se os setores forem bem maiores que o
círculo, dá para ter 10.000 somados com densidade média baixa. Mas isso significa que **os
10.000 habitantes estão majoritariamente fora do raio de 300 m**, e a demo precisa ser capaz
de dizer isso em uma frase, não ser pega por ela.

*Inferência minha, confiança média, a confirmar com dado real:* Franca é cidade de interior
de porte médio (~350 mil habitantes) com densidade urbana baixa; num raio de 300 m em área
de comércio de rua, a população residente real deve ficar na casa de 1.000 a 3.000 pessoas —
o que, pela régua, dá **0 pontos** em população, não 1. O "1 de 5" parece ter vindo
emprestado do estudo (que usa 10.189 habitantes, de outro caso).

**Ajuste, e ele resolve três coisas de uma vez:** o bloco de população exibe, junto do
número, **quantos setores censitários foram somados e qual fração da área deles está dentro
do raio** — e os polígonos desses setores desenhados sobre o círculo no mapa (camada Setor
Censitário, ver 6.1). Isso: (i) torna os dois exemplos do EIXO 2 defensáveis em vez de
contraditórios; (ii) materializa a limitação que a spec hoje só descreve em texto; (iii)
ataca a desconfiança nos números, que é o problema reportado original. É a melhor relação
custo/benefício do protótipo inteiro.

E revise os números do cenário para que população, densidade e área do raio sejam
aritmeticamente coerentes entre si antes de construir.

### 8.4 EIXO 2 depende de um gráfico que a própria spec diz não ter dado

**AJUSTA — EIXO 2 (linhas 223–224) vs. P2 (linhas 154–155)**

O terceiro exemplo do EIXO 2 é: "a população pontuou 1 de 5, e o comparativo territorial
mostra este ponto abaixo da média da cidade". Mas P2 está marcada na interface como
"comparativo territorial — recorte a confirmar, porque a disponibilidade desses agregados
ainda não foi validada". Um exemplo do eixo mais valioso se apoia num gráfico que a spec
declara não validado. Troque o exemplo ou valide o recorte de cidade (ver 3.2).

### 8.5 EIXO 4 está certo e é o que eu mais subestimo em mim mesmo

**REGISTRA (positivo) — EIXO 4 (linhas 233–238)**

"Quatro dos cinco blocos são demografia; a análise está enviesada por omissão da
concorrência" é um comentário que eu não faria sozinho e que me pouparia uma devolução de
comitê. Mantenha, e dê a ele prioridade sobre o EIXO 1 (ver 8.1).

---

## 9. Cenário de Franca — plausibilidade dos números

**AJUSTA / REGISTRA — CENÁRIO (linhas 508–515)**

*Aviso: as avaliações abaixo são inferências de ordem de grandeza, não consulta a dado de
mercado. Confirme com um lead real antes da demo — o custo de checar é baixo e o custo de
ser corrigido na frente do time de Expansão é alto.*

| Dado | Veredito |
|---|---|
| **Franca, SP** | Boa escolha. Cidade de interior de porte médio, com rua comercial de verdade e hospitais. Não é caso artificial. |
| **Raio 300 m** | Plausível como padrão de rua comercial. Confirme se 300 m é mesmo o default do Órbita hoje — a spec diz "raio inicial", P1 oferece 100/300/500/1000, e o slider da entrada precisa ter as mesmas paradas, senão o gráfico e o slider discordam. |
| **Área total 350 m²** | **Grande para ponto de rua.** É loja de formato ampliado, não a farmácia de bairro típica. Não é implausível, mas não é o caso médio — e o custo por m² vai parecer barato por causa do tamanho. |
| **Área de venda 200 m² (57% do total)** | 43% de área não-venda é bastante, mesmo contando estoque, depósito e administrativo. Confira a proporção com um contrato real; se a relação usual for mais alta, o custo por m² de venda do cenário fica otimista. |
| **Aluguel R$ 4.000** | **É o número mais frágil do cenário.** Implica R$ 11,43/m² sobre a área total e R$ 20,00/m² sobre a área de venda. Para um imóvel de 350 m² em rua comercial movimentada, perto de hospital e supermercado, isso soa **baixo** — soa a ponto secundário ou de bairro, não a rua de alto fluxo. Como o custo por m² é apresentado na spec como "o exemplo mais convincente do que a modularização destrava" (linha 446), ele é justamente o número que o time de Expansão vai olhar primeiro, e é o único do cenário que todo mundo na sala tem referência de cabeça. **Se esse número soar errado, a demo perde credibilidade exatamente na tela onde deveria ganhar.** |

**Recomendação:** pegue um lead real de rua comercial de Franca (ou de cidade equivalente)
e use os valores dele. Se não for possível, suba o aluguel para algo coerente com 350 m² em
rua de alto fluxo e **declare que os valores são ilustrativos** — a spec já exige esse aviso
para as bases (linha 475); estenda-o ao aluguel e à área.

**Dois pontos menores:**

- **"Empresário: Pedro"** é o nome do PM que vai apresentar. Numa demo interna isso lê como
  placeholder e distrai. Troque por outro nome.
- A tensão central do cenário — "um caso em que a população residente sozinha engana" — é a
  escolha certa e é o que justifica a feature. Só não a sustente sobre um indicador chamado
  "fluxo" que é contagem de POI (ver 2.1).

---

## 10. Resposta direta às sete perguntas

1. **O catálogo P1–P6 é o que eu pergunto de verdade?** Parcialmente. P1 e P5 são minhas,
   P4 é minha mas pode não ter dado; P2 eu faço só em um terço (cidade — nunca mesorregião
   nem estado); P3 e P6 estão formuladas como distribuição quando o que eu quero é um número
   e uma lista. Faltam: onde estão os concorrentes e a que distância; esse ponto pega o
   fluxo de quê (geradores); quanto do raio é vazio; tem loja nossa perto; tem idoso
   suficiente; esse dado é de quando.
2. **Montar a tela é trabalho a mais ou a menos?** A mais, na maioria das análises. Eu
   mexeria na montagem em 1 a 3 análises por semana. O valor está na tipologia e no padrão
   salvo, não no arrastar — e falta um "usar a montagem padrão" de um clique.
3. **Eu trocaria a fonte de um indicador?** Não, e não sei escolher — é o conhecimento
   prévio que o produto deveria eliminar. Inverta: fonte padrão governada, e a segunda fonte
   vira **sinal de divergência**, não opção de menu. Dois analistas com fontes diferentes
   tornam a discussão do comitê metodológica em vez de ser sobre o ponto.
4. **Motor de score.** As quatro faixas estão transcritas **corretamente**. Mas faltam a
   classificação vigente (16–20 / 12–15 / 8–11 / <8) e o limiar `scorePercent ≥ 34`, e o
   percentual com denominador variável **faz o score subir quando eu removo um indicador
   ruim** (10/20=50% vira 9/15=60%). Solução: exibir sempre os dois números — score vigente
   0–20 com classificação, e a leitura da montagem em %.
5. **Comparação entre análises.** Eu comparo pontos, não metodologias: o mesmo ponto em dois
   raios, dois endereços do mesmo empresário, e este ponto contra loja nossa já aberta. A
   forma proposta entrega um disclaimer; para servir, precisa recalcular os dois scores no
   subconjunto comum, comparar também a **fonte**, e ter um segundo cenário de dados
   especificado (hoje não tem).
6. **O que falta do meu processo real.** A tela de entrada ignora tudo que eu faço antes
   dela: Street View, contagem de farmácia na rua, estacionamento, ponto queimado, checagem
   de lead duplicado. Falta ver o quanto o número se mexe quando eu arrasto o pin. Faltam as
   camadas Lojas Farmarcas, Situação de território e Setor Censitário. E a montagem só
   persistir na sessão contradiz a justificativa permanente e o padrão salvo.
7. **Cenário de Franca.** Cidade e raio, plausíveis. Área total 350 m² é grande para rua e a
   proporção de área de venda (57%) merece conferência. **O aluguel de R$ 4.000 é o número
   frágil**: R$ 11,43/m² total, R$ 20/m² de venda — soa a ponto secundário, não a rua
   comercial de alto fluxo perto de hospital. É justamente o número que sustenta o indicador
   de custo por m², que a spec elege como a melhor demonstração da feature.

---

## 11. O que eu mudaria antes de construir, em ordem

1. **Dois números de score na tela**: vigente 0–20 com classificação, e leitura da montagem
   em %. Resolve gaming, histórico, linguagem do comitê, limiar de 34% e a separação entre
   régua homologada e proposta.
2. **Adicionar as camadas Lojas Farmarcas, Situação de território e Setor Censitário**; as
   duas primeiras montadas por padrão.
3. **Fonte padrão governada**, com a segunda fonte virando sinal de divergência; troca de
   fonte vira exceção registrada e visível no cabeçalho da análise de ponto.
4. **Mostrar os setores censitários somados sobre o mapa** e acertar a aritmética do cenário
   (população × densidade × área do raio).
5. **Definir a origem da tipologia** e deixá-la corrigível em um clique.
6. **Renomear "fluxo estimado de comércios" para proxy**, e reescrever o alerta da interação 5.
7. **Especificar o segundo cenário** da comparação e recalcular pelo subconjunto comum.
8. **Botão "usar montagem padrão"** sempre visível; padrão salvo por tipologia já na entrada.
9. **Reordenar os eixos da IA**: forma vira correção silenciosa no bloco; só EIXO 2, 4 e 3
   gastam alerta.
10. **Revisar os números do cenário de Franca** com um lead real, começando pelo aluguel.
