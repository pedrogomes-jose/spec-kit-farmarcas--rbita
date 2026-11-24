# Revisão executiva — spec modular do Órbita

> Revisor: Executivo de Expansão (perspectiva de quem aprova investimento e defende a feature em sala de liderança).
> Objeto: `outputs/prompt-claude-design-orbita-modular.md` (515 linhas).
> Escopo: argumento de negócio, mensagem da demo, governança/credibilidade, objeções previsíveis, caso de negócio. **Não** cobre execução técnica nem usabilidade fina.
> Fontes internas usadas para ancorar os números: `docs/confluence/ia/analises/estudo-peso-populacao-score-viabilidade.md`, `docs/confluence/2025/estudos/estudo-metrificar-tempo-analise.md`, `docs/confluence/2025/estudos/estudo-historico-analises.md`, `docs/confluence/2025/orbita-descoberta-analise-pontos.md`.

---

## 1. Resumo executivo

A spec descreve um protótipo ambicioso e correto no diagnóstico — a régua vigente de fato penaliza rua comercial — mas **vende a solução errada**: 6 das 515 linhas descrevem a IA montando a análise sozinha (linhas 55-60), e cerca de 340 linhas descrevem o analista editando, montando gráficos e discutindo com a IA. Para a liderança de Expansão, isso lê como "agora o analista tem mais trabalho e mais decisões", exatamente o oposto da OKR vigente de **reduzir o tempo de análise de 3h para ~1h**.

Além disso, o motor de score proposto (linhas 399-403) troca um denominador fixo de 20 pontos por um **denominador variável**, o que quebra o corte de aprovação `scorePercent >= 34` hoje em produção e a comparabilidade com as **6.000+ análises já registradas**. Isso não é detalhe de protótipo: é a primeira coisa que alguém vai testar na frente do stakeholder.

Recomendação: **não apresentar como está**. Dá para salvar com três ajustes de enquadramento e um ajuste na matemática do score — nenhum deles exige reescrever as interações.

---

## 2. Pergunta 1 — Qual é o argumento de negócio, e ele se sustenta?

### 2.1 O argumento que a spec acha que está fazendo

"Modularizar a tela de resultado" para que cada tipo de ponto receba os indicadores certos.

### 2.2 O argumento que ela realmente sustenta

**BLOQUEIA — B1. A modularização, isolada, AUMENTA o conhecimento prévio exigido. Há contradição direta com o objetivo do produto.**

O CLAUDE.md do projeto define o objetivo como "reduzir progressivamente tanto o conhecimento prévio quanto o número de comandos/passos". A spec, lida como lista de capacidades, entrega o inverso:

- o analista passa a decidir **quais blocos** montar (linhas 84-91);
- passa a decidir **qual fonte** usar por indicador, com limitação metodológica para interpretar (linhas 74-82);
- passa a decidir **qual pergunta vira gráfico** e **se a forma é adequada** (linhas 131-204);
- passa a decidir **se discorda da IA** e a escrever justificativa (linhas 112-117, 358-366).

São quatro novas classes de decisão em cima de um analista que hoje recebe uma tela pronta. Hoje o conhecimento prévio exigido é "saber ler o score"; na proposta é "saber montar o score". Em termos de negócio: um analista sênior fica melhor, um analista novo fica pior, e a variância entre analistas sobe — que é precisamente o problema que o produto existe para resolver.

### 2.3 Onde o argumento defensável está escondido

Três trechos carregam todo o valor de negócio, e nenhum deles é o editor:

1. **Linhas 55-60 — a IA monta a análise sozinha e explica por quê.** "Deixe evidente que o analista não montou nada — a IA propôs e ele agora pode editar." Isto é a redução de conhecimento prévio. O editor é a válvula de escape, não a promessa.
2. **Linhas 391-397 — salvar montagem como padrão por perfil de ponto.** A própria spec reconhece: "É a única economia que se acumula: corta trabalho em toda análise futura, não só nesta." Correto, e é o único trecho com ROI composto.
3. **Linhas 303-320 — pauta de comitê com botão COPIAR.** "o analista monta essa pauta à mão hoje, e se ela só viver dentro do painel não eliminou passo nenhum." É o único passo manual **nomeado e eliminado** na spec inteira, e o argumento mais fácil de defender em sala.

**Veredito:** o argumento de negócio existe e é defensável, mas **não é "modularidade"**. É: *"a IA monta a análise certa para o tipo de ponto, o analista audita em vez de montar, e a pauta do comitê sai pronta."* A modularidade é o mecanismo, não a venda. A spec hoje vende o mecanismo.

### 2.4 Ajuste pedido

**AJUSTA — A1.** Inverter a proporção narrativa do prompt: abrir pela montagem automática, tratar edição como exceção auditável. Mover as linhas 55-60 para o topo, expandi-las, e rebaixar CONSTRUTOR DE GRÁFICOS e RÉGUA DE FORMA para apêndice.

---

## 3. Pergunta 2 — O que o protótipo vende e o que ele não vende

### 3.1 A única coisa que o diretor precisa sair entendendo em 10 minutos

> "Este ponto de rua comercial em Franca era penalizado pela nossa régua porque ela conta morador. O Órbita agora percebe o tipo de ponto, monta a análise adequada a ele, e traz para o score um dado que já coletamos hoje e nunca usamos: o custo por m² do ponto."

Uma frase, um cenário, um antes/depois. Tudo mais é suporte.

### 3.2 A spec coloca isso no caminho dele?

Parcialmente. O custo por m² está lá e bem argumentado (linhas 444-447: "é o exemplo mais convincente do que a modularização destrava") e o cenário de Franca é consistente (linhas 508-515). Mas a mensagem está **soterrada**:

| Seção | Linhas | Peso na spec | Peso na mensagem |
|---|---|---|---|
| IA monta a análise sozinha | 55-60 | 6 linhas | **todo** |
| Custo por m² entra no score | 444-447 | 4 linhas | **alto** |
| Pauta de comitê / COPIAR | 303-320 | 18 linhas | **alto** |
| Construtor de gráficos (6 perguntas) | 131-178 | 48 linhas | baixo |
| Régua de forma (8 regras) | 180-204 | 25 linhas | baixo |
| IA aplicada a gráficos (4 eixos) | 206-242 | 37 linhas | médio (só o Eixo 2) |
| Privacidade do fio / "não concordo" / RETRATADO | 262-280, 358-366 | 35 linhas | **negativo em demo** |

**AJUSTA — A2. O que eu cortaria da demo para proteger a mensagem:**

- **Construtor de gráficos:** de 6 perguntas (P1-P6) para **2** — P1 (variação por raio) e P5 (bandeiras concorrentes). P1 sustenta o argumento "o ponto forte do seu score depende do raio escolhido" (linhas 220-222), a demonstração mais impressionante do documento. O resto é catálogo.
- **Régua de forma:** de 8 regras para **1**, a de dois eixos Y (linhas 186-188), que a própria spec classifica como "o erro mais comum e o mais grave". Oito regras de boas práticas de gráfico numa demo de 10 minutos para liderança de Expansão desviam a conversa para estética.
- **4 eixos de crítica da IA:** demonstrar só o **Eixo 2 — contradição com o score** (linhas 215-226), que a própria spec chama de "o eixo mais valioso". Eixos 1, 3 e 4 ficam implementados, fora do roteiro.
- **Privacidade do fio (linhas 262-280):** manter como regra de produto, **retirar da superfície da demo**. Um diretor que lê "o fio de conversa é PRIVADO do analista; ninguém mais vê, nem no comitê" para a demo para discutir por que o analista esconde conversa do comitê. Discussão legítima, não é a dos 10 minutos. Se precisar aparecer, chamar de "rascunho", não de "privado".
- **"Não concordo" / RETRATADO (linhas 358-366):** mesma lógica. Bom produto, ruído em demo executiva.

### 3.3 O que o protótipo NÃO vende e será cobrado

- Não vende **redução de tempo**: nada na tela mostra quanto a montagem automática economizou. Sugestão barata: marcar na entrada, discreto, "análise montada pela IA em 2s". Só usar número de camadas ou de tempo se houver dado real — não inventar.
- Não vende **qualidade de decisão**: nada diz que o ponto certo foi aprovado ou o ponto ruim barrado. Ver seção 6.

---

## 4. Pergunta 3 — Risco de governança e credibilidade

Seção mais grave deste parecer.

### 4.1 Score com denominador variável

**BLOQUEIA — B2. O percentual proposto quebra o corte de aprovação em produção e a comparabilidade de 6.000+ análises históricas.**

Linha 403: *"a soma dos pontos dos indicadores presentes na tela, dividida pelo máximo possível daquela montagem, exibida como percentual de 0 a 100 — nunca em pontos absolutos, porque o total máximo varia conforme o que está na tela."*

O que existe hoje (`estudo-peso-populacao-score-viabilidade.md`):
- score sobre **20 pontos fixos** (4 dimensões x 5);
- `scorePercent = (score / 20) * 100`;
- **corte operacional `scorePercent >= 34` define "Recomendado"**.

Consequência aritmética direta, com a própria régua da spec (linhas 408-424): num ponto de rua comercial de Franca, densidade acima de 25.000 hab/km2 vale **0**. A linha 91 diz "Remover tira a contribuição do score na hora". Então:

```
Montagem completa:                      9 / 20 = 45%   -> Recomendado
Analista remove a densidade (que deu 0): 9 / 15 = 60%  -> +15 p.p. vindos de nada
```

**Remover um indicador ruim aumenta o score.** Não por má-fé: por construção. Qualquer analista descobre isso na segunda semana, e qualquer pessoa no comitê descobre em um minuto olhando a composição — que a spec, corretamente, mantém "SEMPRE visível" (linha 405). A transparência exigida é justamente o que expõe o problema.

Isso não é recurso, é **bomba**, por três motivos de negócio:

1. **Comitê:** dois pontos com percentuais diferentes deixam de ser comparáveis, e o comitê é descrito na documentação da Farmarcas como o fórum onde "é validado se um ponto poderá seguir como aprovado ou será reprovado" (`orbita-descoberta-analise-pontos.md`). O número que fundamenta a decisão perde base comum.
2. **Histórico:** as 6.000+ análises em base foram pontuadas sobre 20. Nenhuma análise nova é comparável a nenhuma antiga. Pontos já reprovados por score baixo podem voltar com montagem diferente — e ninguém consegue dizer se mudou o ponto ou mudou a régua.
3. **Auditoria:** "por que aprovamos este ponto em 2026?" passa a exigir reconstituir qual montagem estava na tela naquele dia.

**Mitigação obrigatória antes de virar produto:** exibir **dois números distintos e rotulados** — (a) *Score Farmarcas*, sempre sobre as 4 dimensões vigentes e 20 pontos fixos, imutável independentemente do que está na tela, que é o número que vai ao comitê; e (b) *Leitura complementar deste ponto*, o percentual da montagem, explicitamente não comparável e não decisório. Nunca um número só.

### 4.2 Régua vigente misturada com régua proposta

**BLOQUEIA — B3. A segregação prometida nas linhas 333-335 é matematicamente impossível com o motor de score da linha 403.**

Linhas 333-335: *"A interface mistura régua vigente da Farmarcas com régua proposta ainda não homologada. Toda afirmação diz de qual das duas está falando — só a régua vigente o analista leva ao comitê."*

Linha 427: *"crie uma régua de 0 a 5 coerente e marque-a visivelmente na interface como 'régua proposta, ainda não homologada'."*

Adicionar um indicador de régua proposta **altera numerador e denominador do mesmo percentual**. As linhas 376-377 explicitam: *"+8 pontos no numerador, +5 no máximo, score vai de 55% para 58%"*. Ou seja, uma regra não homologada move o número que a spec diz que o analista leva ao comitê. Rotular não resolve: a contaminação é aritmética, não de rótulo.

**Quem precisa homologar antes disso virar produto:** a régua de score é regra de negócio de aprovação de ponto, não configuração de ferramenta. Precisa de dono formal — na prática, a liderança de Expansão que responde pelo comitê de ponto, junto de quem construiu a régua vigente das 4 dimensões. Sem esse aval, concorrência, comércios/POIs e custo por m² não podem entrar no número que sai da tela. **Pergunta aberta para quem está especificando: existe hoje dono formal da régua de score na Farmarcas? Não consegui identificar isso na documentação e não vou assumir.**

### 4.3 "A IA pode discordar da régua vigente"

**REGISTRA — R1.** Linhas 337-342: *"a IA precisa saber dizer 'a régua vigente te dá 5 em renda porque a classe é D/E, e eu acho que isso não sustenta no comitê deste ponto'."*

Produto: está certo, e o argumento das linhas 341-342 ("uma IA que só defende a régua contra o analista perde credibilidade e é fechada na terceira vez") é sólido.

Política: numa sala de liderança, uma ferramenta interna dizendo em tela que a régua da empresa está errada é uma afirmação sobre o trabalho de quem fez a régua — que pode estar na sala. **Não remova o comportamento, remova a surpresa:** alinhe antes com o dono da régua e apresente isso como achado de discovery, não como opinião da ferramenta descoberta ao vivo.

### 4.4 Padrão salvo por analista

**AJUSTA — A3.** Linhas 391-397. "Salvar montagem como padrão" sem dono cria réguas paralelas de fato: em seis meses existem onze "padrões de rua comercial", um por analista, e o comitê não sabe qual foi usado. É o maior ativo de ROI da spec e por isso precisa de governança desde o protótipo: padrão é **da equipe**, publicado por alguém com alçada, versionado, e a análise registra qual versão usou. A spec já pede "quantas análises já usaram cada padrão salvo" (linha 397) — bom instinto, falta o dono.

### 4.5 Comparação entre análises

**AJUSTA — A4.** Linhas 125-129 pedem que a comparação "sinalize de forma inequívoca que os dois scores NÃO são equivalentes". Sinalizar não-comparabilidade não resolve a necessidade do comitê, que é **comparar**. A tela precisa oferecer o *Score Farmarcas* das 4 dimensões vigentes lado a lado (sempre comparável) além do subconjunto comum. Caso contrário o produto diz ao comitê "não dá para comparar" — e o comitê compara mesmo assim, no olho.

### 4.6 Achado colateral que a demo vai expor

**REGISTRA — R2.** A tabela de classificação vigente (`estudo-peso-populacao-score-viabilidade.md`) tem inconsistência própria: a faixa 8-11 pontos é rotulada "Baixa viabilidade / Não recomendado" mas, pelo corte `scorePercent >= 34`, sai como **"Recomendado"**. Um protótipo que mantém a composição do score permanentemente visível torna isso evidente. Não é problema criado pela spec, mas aparece na demo. Decida antes se quer tratar como achado a apresentar ou evitar essa faixa no cenário de Franca.

---

## 5. Pergunta 4 — Onde a feature vai ser atacada na sala

### Objeção 1 (quase certa) — "Isso não vai AUMENTAR o tempo de análise?"

Vem direto da OKR de 3h -> 1h. O diretor vê arrastar bloco, escolher fonte, montar gráfico e conversar com IA, e conclui que você adicionou trabalho.

**A spec responde?** Sim, mas enterrado: montagem automática (55-60), padrão salvo (391-397), pauta copiável (303-320). Nenhum está no caminho visual dos primeiros 2 minutos.

**Correção:** depois do "Explorar com IA", a primeira coisa é a análise **já montada e já justificada** — e o apresentador diz "nada disso o analista montou" antes de tocar em qualquer card.

### Objeção 2 (certa) — "Se cada análise tem indicadores diferentes, como eu comparo dois pontos no comitê?"

**A spec responde?** **Não.** Reconhece o problema (125-129) e o sinaliza, mas não oferece número comparável. Ver 4.1 e 4.5. **É a objeção que derruba a aprovação se não for respondida antes.**

### Objeção 3 (muito provável) — "Quem aprovou mudar a régua? Se concorrência passa a pontuar, o que acontece com os pontos que já reprovamos e com os que estão em negociação?"

**A spec responde?** Parcial. É honesta ao rotular "régua proposta, ainda não homologada" (427), mas não diz quem homologa, nem o que acontece com o histórico, nem se o novo score é retroativo. Ver 4.2.

### Objeção 4 (possível, de outro ângulo) — "Por que o analista pode esconder a conversa com a IA do comitê?"

Decorre das linhas 262-280. Boa regra de produto mal posicionada para plateia executiva. Ver 3.2.

---

## 6. Pergunta 5 — O que falta para virar caso de negócio

### 6.1 O que já existe e é aproveitável

| Baseline | Situação hoje | Fonte |
|---|---|---|
| Meta de tempo de análise | **3h -> ~1h** é OKR declarada | `estudo-metrificar-tempo-analise.md` |
| Volume de análises | **6.000+** registros em `analysis_data` (base de dev, descrita como próxima da produção) | `estudo-historico-analises.md` |
| Status final da análise | Campos `status` / `analysisSituation` com estados finais (Reproved, Business) | idem |
| Instrumentação de uso | PostHog mapeado **por tela** (Início, Indicadores, Análise de Pontos, etc.) | `indicadores-mapeamento-posthog.md` |

### 6.2 O que falta, e é o que a liderança vai pedir

1. **Tempo ativo por análise.** O que existe hoje é "tempo em aberto": média de **76 dias**, com casos de segundos a anos (`estudo-historico-analises.md`). Isso mede o ciclo do lead, não o esforço do analista — inútil como baseline de ROI e **perigoso se citado em sala**, porque alguém pergunta "então vocês vão de 76 dias para quanto?". O próprio estudo de métricas reconhece que falta definir início e fim da análise. **Sem esse número não há caso de negócio quantitativo. É o item mais importante desta lista.**
2. **Análises de ponto por mês e por analista.** Determina se economizar 30 min por análise vale 20h/mês ou 2h/mês no time. Extraível de `analysis_data` por `createdAt` (leitura).
3. **Taxa de retrabalho/reabertura.** Quantas análises são modificadas depois de encerradas (`modifiedAt` posterior ao status final) — proxy razoável e já disponível.
4. **Divergência entre score e decisão do comitê.** Quantos pontos "Recomendado" foram reprovados e quantos com score baixo viraram negócio. **É a métrica de qualidade de decisão**, e a única que justifica mexer na régua: se o score já discorda do comitê com frequência, a régua está errada e corrigi-la tem valor mensurável. Provavelmente extraível hoje cruzando score salvo com `status` final.
5. **Resultado do ponto aberto.** Faturamento/performance das lojas abertas contra o score que receberam. Número definitivo e o mais difícil — vive fora do Órbita.

### 6.3 Como eu montaria o número de ROI (sem inventar dado)

```
Economia mensal     = (análises de ponto por mês) x (minutos economizados por análise) / 60
Capacidade liberada = Economia mensal / (horas por análise hoje)
```

Com a OKR de 3h -> 1h já declarada, o enquadramento honesto é: *"esta feature é uma das alavancas da meta 3h->1h já aprovada; ela ataca a montagem da análise e a redação da pauta do comitê"* — e **não** um ROI novo e inventado. Prometer percentual sem baseline instrumentado é a forma mais rápida de perder credibilidade na segunda reunião.

**AJUSTA — A5.** Antes do comitê de aprovação (não antes do protótipo), rodar extração **somente de leitura** sobre `analysis_data` para os itens 2, 3 e 4. São três consultas e transformam o pitch de qualitativo em quantitativo. Pedir autorização e confirmar o ambiente antes de rodar.

---

## 7. Riscos e mitigação

| Risco | Severidade | Mitigação |
|---|---|---|
| Score com denominador variável usado como número de decisão | BLOQUEIA | Dois números: *Score Farmarcas* (20 pts fixos, decisório) + leitura complementar (não decisória) |
| Régua não homologada contaminando o número do comitê | BLOQUEIA | Homologação formal antes de produção; na demo, isolar visualmente a contribuição proposta |
| Demo lida como "mais trabalho para o analista" | BLOQUEIA | Roteiro abre pela montagem automática; editor demonstrado como exceção |
| Padrões salvos virando réguas paralelas sem dono | AJUSTA | Padrão da equipe, publicado com alçada e versionado |
| "A IA discorda da régua" surpreendendo o dono da régua na sala | REGISTRA | Alinhamento prévio; apresentar como achado de discovery |
| **Risco de NÃO agir** | — | A régua vigente continua penalizando rua comercial e ignorando concorrência e custo do ponto (os três indicadores que não pontuam hoje). Cada ponto comercial subavaliado é uma loja não aberta num ponto bom; cada ponto residencial superavaliado por renda D/E é capital imobilizado num ponto ruim. **Manter a régua atual também é decisão, e ela já está errando — a diferença é que erra em silêncio.** |

---

## 8. Decisão necessária

1. **Antes de montar o protótipo:** aprovar a mudança de enquadramento (A1) e o modelo de dois números no score (B2/B3). Sem isso o protótipo nasce com um problema que a própria transparência da tela expõe em demo.
2. **Antes do comitê de aprovação:** definir o dono formal da régua de score e obter aval para as réguas propostas de concorrência, comércios e custo por m² (B3).
3. **Antes de prometer ROI:** extrair os baselines 2, 3 e 4 da seção 6.2 (A5).

---

## 9. Próximos passos após aprovação

1. Reescrever a abertura do prompt invertendo a proporção montagem-automática contra edição (A1).
2. Reescrever a seção MOTOR DE SCORE com os dois números separados (B2).
3. Enxugar o roteiro de demo: 2 perguntas de gráfico, 1 regra de forma, 1 eixo de crítica (A2).
4. Rodar as extrações de baseline (A5, somente leitura, com autorização e ambiente confirmado).
5. Alinhar previamente com o dono da régua antes de qualquer apresentação (R1, B3).

---

## Índice de achados

| ID | Severidade | Achado | Linhas da spec |
|---|---|---|---|
| B1 | **BLOQUEIA** | Modularização, como enquadrada, aumenta conhecimento prévio e contradiz o objetivo do produto | 66-129 e 131-204 contra 55-60 |
| B2 | **BLOQUEIA** | Score percentual com denominador variável quebra o corte >=34% e a comparabilidade com 6.000+ análises; remover indicador que deu 0 infla o score | 399-403, 91 |
| B3 | **BLOQUEIA** | Régua não homologada entra no mesmo percentual da vigente; a segregação prometida é aritmeticamente impossível; falta dono da homologação | 333-335, 376-377, 427 |
| A1 | AJUSTA | Inverter proporção narrativa: montagem automática primeiro, edição como exceção | 55-60 |
| A2 | AJUSTA | Cortar da demo: 4 das 6 perguntas de gráfico, 7 das 8 regras de forma, 3 dos 4 eixos, privacidade do fio e "não concordo" | 131-204, 206-242, 262-280, 358-366 |
| A3 | AJUSTA | Padrão salvo precisa de dono, alçada e versão — senão vira régua paralela | 391-397 |
| A4 | AJUSTA | Comparação precisa de um número comparável (4 dimensões vigentes), não só do aviso de não-equivalência | 125-129 |
| A5 | AJUSTA | Extrair baselines de volume, retrabalho e divergência score contra comitê antes de prometer ROI | — |
| R1 | REGISTRA | "IA discorda da régua vigente" é bom produto e risco político; alinhar antes | 337-342 |
| R2 | REGISTRA | Inconsistência pré-existente da régua (faixa 8-11 rotulada "Não recomendado" mas Status "Recomendado") ficará visível na demo | externo à spec |
