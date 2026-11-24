# Revisão de pesquisa — spec modular do Órbita

> Parecer do subagente `ux-researcher` sobre
> `outputs/prompt-claude-design-orbita-modular.md` (515 linhas), executado em
> 2026-10-06.
>
> **Escopo:** qualidade da evidência por trás das decisões da spec e o que
> precisa ser testado antes de construir. Não avalia viabilidade técnica nem
> argumento de negócio.
>
> **Natureza deste documento:** é análise de evidência documental, não pesquisa
> com usuário. Tudo que eu afirmo aqui sobre comportamento de analista é
> hipótese, inclusive quando eu discordo da spec.
>
> **O que eu li para calibrar o que é evidência:**
> `outputs/revisao-analista-expansao-conversa-ia.md` (parecer anterior, já
> incorporado — não repito seus achados),
> `docs/confluence/2025/orbita-descoberta-analise-pontos.md`,
> `docs/confluence/2025/evolucao-camadas/evolucao-camadas-entrevista.md`,
> `docs/confluence/2025/evolucao-camadas/orbita-evolucao-camadas.md`,
> `docs/confluence/2025/estudos/estudo-historico-analises.md`,
> `docs/confluence/2025/estudos/estudo-metrificar-tempo-analise.md`,
> `docs/confluence/2025/indicadores-mapeamento-posthog.md`.

---

## 0. O que, neste repositório, conta como evidência

Antes de classificar as hipóteses da spec, preciso declarar o lastro disponível.
Isto não é detalhe: quase todo achado abaixo depende de onde está a linha entre
o que foi observado e o que foi suposto.

**CERTEZA — registrado, com fonte, e consistente entre documentos**

- A análise leva ~3 horas e a meta é 1 hora (descoberta, OKR).
- Os analistas desconfiam dos números do Órbita e conferem fora (Google,
  Caravela, IBGE) antes de registrar — está na descoberta em três lugares
  distintos ("Falta de confiança nos números apresentados no Órbita";
  "Falta de confiança sobre informações"; "Utilização de ferramentas diversas").
- As bases do próprio Órbita se contradizem entre si: `orbita-evolucao-camadas.md`
  documenta um concorrente que era uma loja Farmarcas, e registra que
  "aparentemente esse comportamento é conhecido pelo time de analistas".
- As camadas que o time mais usa estão listadas na descoberta: Concorrentes,
  Densidade demográfica, Renda média, Setor Censitário, Residentes|População,
  Pirâmide etária, Potencial de consumo, Situação de território.
- O trabalho pesado está FORA da tela de resultado: passos 7 a 10 da jornada
  (planilha, território, estrutura, feedback em PDF).
- Existe base comportamental consultável: `analysis_data` no MongoDB, >6 mil
  análises, com `createdAt`, `modifiedAt`, `updatedBy`, `comment`, `status`
  (`estudo-historico-analises.md`).

**SUPOSIÇÃO — afirmado em algum documento, sem observação por trás**

- Tudo que a spec afirma sobre como o analista vai reagir a uma tela editável e
  a uma IA que discorda. A fonte dessas afirmações é
  `revisao-analista-expansao-conversa-ia.md`, que declara de si mesmo, nas
  linhas 6 a 9: *"é a avaliação de um subagente que simula a perspectiva de quem
  monta o score... Não é pesquisa com usuário real"*. Catorze achados desse
  documento aparecem na tabela final como **Aplicado** na spec.

**DÚVIDA — ninguém olhou ainda**

- O comitê. Ele aparece como destinatário em toda a spec (seção
  "Comando principal: essa análise se sustenta no comitê?", linhas 303-320) e
  não há um único registro de pesquisa com quem participa dele.
- A pesquisa quantitativa de 08/10/2024, citada na descoberta, não está neste
  repositório. Não sei o N, as perguntas nem os resultados.

### Achado 0.1 — REGISTRA: a organização registra roteiro e não registra achado

`evolucao-camadas-entrevista.md` tem 15 perguntas, um participante listado
("Leandro Mendes /", sem o segundo nome) e **nenhuma resposta registrada**,
exceto uma linha solta no rodapé: *"Existem camadas que a visualização delas em
conjunto no mapa não fica claro."*

Isso é um risco de processo que vai se repetir no teste deste protótipo: o
roteiro sobrevive, o achado evapora. Antes de rodar qualquer sessão, defina onde
a síntese vai morar e quem a escreve. Senão daqui a seis meses existirá um
`roteiro-teste-modular.md` e nenhuma conclusão.

### Achado 0.2 — AJUSTA: a montagem padrão da spec não bate com as camadas que o time diz usar

A spec define o que vem montado na entrada (linhas 430-441). Comparando com a
lista de camadas mais usadas da descoberta:

| Camada mais usada (descoberta) | Está na montagem padrão da spec? |
|---|---|
| Concorrentes | Sim |
| Densidade demográfica | Sim |
| Renda média | Sim (classificação econômica) |
| Residentes / População | Sim |
| Pirâmide etária | Não — está no painel para adicionar |
| Potencial de consumo | Sim |
| **Setor Censitário** | **Ausente da spec inteira** |
| **Situação de território** | **Ausente da spec inteira** |

E a spec adiciona "Fluxo estimado de comércios no entorno" (linha 450), que não
aparece em lista nenhuma de uso real.

Duas dessas ausências são baratas de corrigir e caras de errar na frente do
stakeholder: um analista olhando a tela vai sentir falta de setor censitário,
que é justamente o recorte onde mora a limitação metodológica que a própria spec
escolheu destacar (linhas 79-82: o setor que intersecta o raio entra inteiro na
conta). Se a limitação é exibida mas a camada que a origina não existe na tela, o
aviso fica órfão.

---

## 1. Hipóteses que a spec assume como verdade

Reformulo cada uma como afirmação falseável, com critério e risco. Confirmo,
refuto ou corrijo as cinco candidatas e acrescento sete.

### H1 — "O analista quer montar a própria tela"

**Veredito: a candidata está certa como suspeita, e a evidência disponível aponta
contra ela.** Severidade: **BLOQUEIA**.

A descoberta trata a liberdade de escolha não como virtude, mas como a causa do
problema. Cito literal:

> *"Atualmente, em cada análise, o usuário para iniciar sua análise precisa tomar
> a iniciativa de escolher a primeira base, contando que essa pessoa saiba
> exatamente qual base escolher que são importantes pro negócio. Nesse contexto,
> estamos deixando de considerar pessoas que não tem a expertise ou anos de
> experiência nesse assunto."*

E o `CLAUDE.md` do projeto diz que a expectativa de evolução é *"reduzir
progressivamente tanto o conhecimento prévio quanto o número de comandos/passos"*.

A spec propõe o oposto literal do remédio documentado: mais graus de liberdade,
mais decisões por análise (ordem dos blocos, tamanho, fonte por bloco, quais
camadas, quais gráficos, qual pergunta do catálogo). A mitigação existe — a IA
pré-monta (linhas 55-60) — mas essa mitigação transfere o peso da hipótese para
H2, que é mais frágil ainda.

**Reformulação testável (é esta que vale a pena medir, não a original):**
> Dada uma montagem proposta pela IA, o analista edita a montagem em ao menos uma
> ação substantiva (adicionar/remover camada ou trocar fonte) em uma faixa
> intermediária das análises — nem quase nunca, nem quase sempre.
> Validação: entre 20% e 60% das análises nas primeiras 4 semanas.
> Invalidação: <10% (a modularidade não é usada, pagou-se por um editor que
> ninguém abre) ou >80% (a IA não acerta a proposta e a modularidade virou
> trabalho obrigatório, não opcional).

**Risco se falsa:** alto e assimétrico. Se ninguém edita, o custo é desperdício
de construção — recuperável. Se todo mundo edita porque a proposta da IA não
serve, a feature **aumenta** o tempo do passo 6 contra uma OKR que é de redução de
tempo, e devolve ao analista júnior exatamente a decisão que a descoberta diz
que ele não sabe tomar.

### H2 — "A IA consegue escolher a montagem certa por tipo de ponto"

**Veredito: confirmada como hipótese, e é a mais frágil do conjunto.**
Severidade: **BLOQUEIA**.

Esta hipótese tem três camadas empilhadas, todas sem evidência:

1. Que existe uma tipologia de ponto discreta e reconhecível ("rua comercial",
   "bairro residencial", "ponto isolado" — linha 392).
2. Que o sistema consegue classificar um ponto nessa tipologia a partir dos dados
   que tem.
3. Que existe uma montagem *certa* por tipologia, e que alguém sabe qual é.

Nenhuma das três aparece em documento algum. Pior: a spec constrói o cenário de
demonstração (linhas 508-515) justamente sobre a tipologia cuja variável decisiva
o produto **não tem** — o estudo
`estudo-fluxo-pessoas-flutuante-fontes-dados.md` existe neste repositório porque
fluxo de passantes não é modelado. A IA vai dizer *"priorizei fluxo de comércios"*
(linha 59) apoiada num indicador cuja régua a própria spec manda inventar e
rotular como "régua proposta, ainda não homologada" (linhas 425-428).

**Reformulação testável:**
> Dados 20 pontos já analisados no histórico (`analysis_data`), dois analistas
> seniores classificam independentemente cada um numa tipologia e listam as 5
> camadas que usariam. Validação: concordância entre os dois acima de 70% na
> tipologia e núcleo comum de ao menos 3 camadas por tipologia.
> Invalidação: os dois discordam da tipologia em mais de 1 ponto a cada 3 — nesse
> caso não existe "montagem certa" para a IA aprender, e a proposta automática é
> chute com cara de recomendação.

**Risco se falsa:** alto. Uma IA que propõe a montagem errada com confiança
destrói a credibilidade do assistente inteiro, e aí H3 cai junto. E este é um
teste barato: dá para rodar em uma tarde, com dois analistas, sobre o histórico
que já existe — **antes** de construir o protótipo.

### H3 — "O analista vai confiar numa IA que discorda dele"

**Veredito: confirmada, e com um agravante que a candidata não captura.**
Severidade: **AJUSTA** (do assistente, não da modularidade).

O agravante: a desconfiança documentada não é com a análise, é **com os números**.
A IA da spec fala apoiada nesses mesmos números, e a spec reconhece isso ao
exigir procedência em toda discordância (linhas 326-331). Mas a mitigação não foi
testada — ela veio inteira do subagente simulado.

Há uma coisa que a spec **não** resolve e que é a causa raiz da descoberta: quando
o analista acha que o número está errado, não existe caminho no produto. O
parecer anterior apontou isso ("contestar este dado") e a tabela de destino o
deixou **Em aberto**. Do ponto de vista de pesquisa: o problema reportado original
continua sem tratamento nesta spec, e a feature nova depende de confiança nos
mesmos dados que geraram o problema.

**Reformulação testável:**
> Num ponto onde a IA discorda do analista com procedência completa, ele
> responde dentro do produto (aceita a ação, clica "não concordo", ou pergunta no
> fio) em vez de sair da ferramenta.
> Invalidação: em mais da metade das discordâncias observadas, a reação é abrir o
> Google / consultar colega / fechar o painel.

**Risco se falsa:** médio-alto. O analista fecha o painel, e sobra uma tela
modular sem a camada que supostamente substitui o conhecimento prévio. A
modularidade sobrevive, o assistente não.

### H4 — "O analista sabe escolher entre duas fontes de dado"

**Veredito: confirmada, e eu acrescento um efeito de segunda ordem mais grave que
a hipótese original.** Severidade: **BLOQUEIA**.

A hipótese como colocada já é arriscada: a descoberta diz explicitamente que o
problema é ele **não** saber qual base escolher. Mas o risco maior não é ele
escolher errado — é o que a tela ensina quando as duas fontes discordam.

A spec exige (linhas 74-78) que trocar a fonte mude *ao mesmo tempo* o valor, a
procedência e a contribuição no score, e exige (linhas 450-453) que **todo**
indicador tenha ao menos duas fontes com valores diferentes. O resultado
observável para o analista é: o mesmo indicador, no mesmo ponto, tem dois valores
verdadeiros no Órbita.

Isso é o sintoma documentado em `orbita-evolucao-camadas.md` — bases que se
contradizem — promovido a funcionalidade. A reação registrada do analista a dados
conflitantes não é escolher a melhor fonte: é **ir conferir no Google**.

**Reformulação testável:**
> Ao ver dois valores divergentes para o mesmo indicador, o analista escolhe uma
> fonte e segue dentro do produto.
> Invalidação: ele verbaliza desconfiança nas duas, ou declara que conferiria
> fora, em mais de 2 de 5 participantes.

**Risco se falsa:** alto e direcionalmente perverso. A feature que deveria
aumentar a confiança nos números pode ser a que mais a reduz — e a confiança nos
números é o problema reportado que originou o produto, não um efeito colateral.
**Esta é a hipótese que eu testaria primeiro**, e dá para testar sem protótipo
nenhum: mostre a dois analistas dois valores de população para o mesmo raio, com
procedência, e observe o que eles fazem.

### H5 — "A crítica de forma de gráfico é bem-vinda e não paternalista"

**Veredito: confirmada, e a spec vai além — ela afirma isso como fato.**
Severidade: **AJUSTA**.

Linha 212, literal: *"É a crítica mais objetiva e a que o analista aceita sem
resistência."* Isso é uma predição de comportamento humano escrita no imperativo,
sem fonte.

Mas há uma hipótese anterior e maior, que ninguém formulou: **o analista de
Expansão faz gráficos hoje?** A jornada da descoberta não menciona gráfico em
passo nenhum. Ela menciona planilha, PDF e feedback. A spec dedica ~70 linhas
(131-242) a um construtor de gráficos guiado, uma régua de forma com 8 regras e
uma análise de IA em 4 eixos — para um trabalho que não aparece na jornada
documentada.

**Reformulação testável (faça esta antes da outra):**
> O analista produz ou consome algum gráfico no processo atual de análise de
> ponto. Validação: ele consegue mostrar um artefato real (planilha, PDF de
> feedback) que contenha um gráfico feito por ele.
> Invalidação: nenhum dos participantes produz gráfico hoje — e aí a régua de
> forma é solução sem problema, por mais correta que esteja tecnicamente.

**Risco se falsa:** médio em dinheiro, alto em atenção. Se não há trabalho de
gráfico, a seção mais detalhada da spec é a menos útil, e ela consome a metade do
orçamento cognitivo da tela (ver seção 4) e do tempo da demo.

### H6 — "O comitê aceita análises com montagens diferentes entre si" (acrescentada)

Severidade: **BLOQUEIA**.

O score passa a ser percentual com denominador variável (linhas 399-403) e cada
análise pode ter composição distinta. A spec mitiga com sinalização na comparação
(linhas 125-129). O parecer anterior registrou a unidade do score como **Em
aberto**.

O ponto de pesquisa é outro e mais duro: o comitê é um **ritual de governança**, não
uma tela. Se a diretoria compara análises entre si, ou compara com histórico, a
modularidade quebra a comparabilidade de uma função organizacional — e nenhuma
decisão de usabilidade conserta isso. Nunca se falou com quem participa do comitê.

**Testável:** leve três análises com montagens diferentes a uma reunião de comitê
real e observe se alguém tenta compará-las. Invalidação: comparação direta entre
scores acontece e ninguém percebe que os denominadores diferem.

**Risco se falsa:** máximo. Rejeição por governança mata a feature
independentemente de qualquer resultado de usabilidade, e acontece depois de tudo
construído.

### H7 — "O problema é a tela ser fixa" (acrescentada)

Severidade: **BLOQUEIA**.

A spec abre com o enunciado do problema nas linhas 39-42: *"a tela de resultado é
igual para todo ponto... e o score penaliza a rua comercial por um motivo que não
se aplica a ela."*

**Não encontrei esse problema em nenhum documento de descoberta.** A raiz do
problema registrada é outra, literal: *"Falta de informações claras em um único
local, para o processo de análise de ponto"*, e os quatro itens de "O que precisa
ser resolvido" são: dificuldade de adicionar camadas e ver resultados **de forma
simples**; clareza das informações; informações num único lugar; confiança no
sistema.

"Adicionar camadas de forma simples" é compatível com modularidade. "A tela é
igual para todo ponto" é uma formulação de problema diferente, com solução
diferente, e eu não sei de onde ela veio. Pode ter vindo de uma conversa legítima
com a stakeholder — mas então precisa estar escrita e atribuída.

**Pergunta direta ao autor da spec, antes de qualquer teste:** quem disse que a
tela ser fixa é o problema? É fala de analista, de stakeholder, ou inferência de
produto? Se for inferência, isso muda a classificação de toda a spec de "solução
para problema validado" para "aposta".

### H8 — "A montagem salva como padrão será reutilizada" (acrescentada)

Severidade: **AJUSTA**.

A spec chama isso de *"a única economia que se acumula"* (linha 396). A origem da
ideia, rastreada: o parecer simulado a propôs, e antes dele existe a pergunta 15
do roteiro de abril/2025 — *"Você gostaria de salvar filtros usados com
frequência?"* — que é **pergunta de opinião hipotética** (violação clássica de Mom
Test: "você gostaria de") e cuja resposta **não foi registrada**.

Ou seja: a feature apontada como maior ganho acumulado se apoia numa pergunta
enviesada sem resposta.

**Testável sem construir nada:** rode uma consulta de leitura em `analysis_data`
comparando os conjuntos de camadas entre análises do mesmo analista. Se ele já
repete a mesma combinação hoje, o padrão tem lastro comportamental. Se cada
análise tem combinação diferente, "salvar como padrão" resolve uma repetição que
não existe. (Somente `SELECT`/leitura, com permissão prévia e ambiente declarado.)

### H9 — "O fio privado é o que destrava o uso" (acrescentada)

Severidade: **REGISTRA**.

A spec dedica uma seção inteira (linhas 262-280) à privacidade do fio, incluindo
uma proibição explícita de métricas por analista. A justificativa inteira vem do
subagente simulado, que escreveu em primeira pessoa *"Sem isso, não uso"*. É uma
decisão de produto defensável e provavelmente certa — mas é importante registrar
que **uma persona sintética escreveu o requisito de privacidade de um produto
corporativo**, e que há um stakeholder oposto não consultado: a liderança, que pode
exigir a trilha. Quem decide isso não é o analista nem o designer.

### H10 — "A marcação 'régua proposta, não homologada' protege" (acrescentada)

Severidade: **AJUSTA**.

A spec manda inventar réguas de 0 a 5 para concorrentes, comércios e custo por m²
(linhas 425-428) e rotulá-las. O rótulo é uma mitigação de confiança cuja eficácia
é ela própria uma hipótese — e a literatura de disclaimers é desfavorável: avisos
permanentes viram invisíveis. A própria spec reconhece o mecanismo em outro lugar
(linhas 344-349: *"senão vira disclaimer que o analista aprende a ignorar"*) e
depois o usa mesmo assim em quatro lugares distintos.

Efeito de segunda ordem concreto: o custo por m² é apontado como "o exemplo mais
convincente do que a modularização destrava" (linhas 444-447) **e** carrega régua
não homologada. O exemplo-carro-chefe da demo é o que o analista não pode levar
ao comitê. Isso vai aparecer na primeira sessão de teste.

### H11 — "O ganho de tempo está no passo 6" (acrescentada)

Severidade: **REGISTRA** (fronteira com o parecer de negócio — não aprofundo).

Só o registro de pesquisa: a OKR é 3h → 1h, e a jornada coloca o grosso do tempo
nos passos 7 a 10, fora desta tela. Toda a spec atua no passo 6. Existe risco real
de o passo 6 **subir** e o total não cair. Isso precisa ser medido antes e depois,
e hoje nem sabemos medir — `estudo-metrificar-tempo-analise.md` tem cinco linhas e
termina dizendo que ainda não se sabe determinar o início e o fim de uma análise.
**Sem instrumentação de tempo, a OKR é inverificável e o sucesso desta feature
também.**

### H12 — "O analista percebe que a tela é editável" (acrescentada)

Severidade: **AJUSTA**.

A spec exige "handles discretos" (linha 72) e um painel "recolhido por padrão"
(linha 258), e ao mesmo tempo exige "Deixe evidente que o analista não montou
nada — a IA propôs e ele agora pode editar" (linha 60). Discrição e evidência são
objetivos opostos; a spec pede os dois e não diz quem ganha. É exatamente o tipo
de conflito que só um teste de descoberta resolve — tarefa 1 do roteiro.

---

## 2. Este protótipo testa ou convence?

**Veredito: ele convence. E isso está escrito na spec, não é leitura minha.**
Severidade: **AJUSTA**.

Evidências, dentro do próprio documento:

- Linhas 12-22 — a lista inteira de "NÃO é" trata o risco de parecer apresentação,
  nunca o risco de não aprender nada. O critério de qualidade declarado é
  verossimilhança.
- Linha 479 — *"Alguém vai conferir na frente do stakeholder."* O leitor projetado
  é o stakeholder, não o analista.
- Linha 447 — *"é o exemplo mais convincente do que a modularização destrava."*
  Critério: convencer.
- Linhas 508-515 — cenário único, escolhido por ser *"um caso em que a população
  residente sozinha engana"*, ou seja, o caso em que a tela atual falha. A spec
  ainda instrui: *"a montagem padrão da IA deve privilegiar fluxo e custo do
  ponto."* O cenário foi desenhado para a feature ganhar.

O problema de pesquisa dessa última escolha é estrutural: **com um só cenário, e
justamente esse, o protótipo é incapaz de produzir evidência contrária.** Qualquer
coisa que aconteça confirma a tese. Um instrumento que não pode falhar não mede
nada.

### O que mudaria se o objetivo fosse aprender

1. **Segundo cenário, adversarial.** Um bairro residencial onde a tela fixa de
   hoje já funciona bem. A pergunta de aprendizado é: o analista mexe mesmo
   assim? Se ele não mexe quando não precisa, a IA acertou (bom). Se ele mexe
   sempre, por hábito ou desconfiança, a modularidade virou trabalho obrigatório.
2. **Uma variante sem o aviso explicativo da IA.** A linha 60 ensina o modelo
   mental ao participante. Metade das sessões deve entrar sem esse aviso, senão a
   descoberta de editabilidade (H12) não é testável — você mediu a eficácia do
   seu próprio tutorial.
3. **Log de eventos.** Timestamp de cada drag, troca de fonte, adição/remoção,
   alerta exibido, alerta dispensado, "não concordo", justificativa escrita (com
   contagem de caracteres). Sem isso a sessão vira lembrança do moderador — e o
   histórico deste repositório mostra o que acontece com achado não registrado
   (Achado 0.1).
4. **Permitir caminhos ruins.** O protótipo precisa deixar o analista montar uma
   análise ruim e seguir. Se todos os caminhos levam a uma tela bonita, você não
   descobre onde ele se perde.
5. **Dados que ele consiga conferir.** Hoje os valores são ilustrativos (linhas
   473-476). Para testar H4 (confiança em fontes), pelo menos o indicador de
   concorrentes precisa ser conferível no Google Maps — porque conferir no Google
   é o comportamento real documentado, e é o único jeito de observar a reação de
   desconfiança de verdade.

### Como atender aos dois com um build só

Dá, e é barato. Mesma aplicação, duas configurações:

| | Modo demo (stakeholder) | Modo pesquisa (analista) |
|---|---|---|
| Cenário | Franca, rua comercial | seletor: Franca **+** bairro residencial |
| Aviso da IA na entrada | ligado | desligado em metade das sessões |
| Chips sugeridos | curados (linhas 287-301) | inclui o chip proibido (ver 6.3) |
| Telemetria | desligada | log de eventos em console/arquivo |
| Dados | ilustrativos | ilustrativos, com concorrentes conferíveis |

Custo: um objeto de configuração e um segundo conjunto de dados. O ganho é que o
mesmo artefato que fecha a aprovação também gera evidência — e, importante na
ordem das coisas, **rode as sessões com analistas antes da apresentação ao
stakeholder**, não depois. Depois, o compromisso público já foi assumido e nenhum
achado muda nada.

---

## 3. Roteiro de teste de usabilidade

**Formato:** 5 participantes analistas de Expansão + 1 participante de comitê (se
houver pessoa distinta). 50 minutos, moderado, think-aloud, compartilhamento de
tela. Inclua obrigatoriamente **um analista com menos de 6 meses de casa** — é a
pessoa que a descoberta diz estar sendo deixada de fora, e é com ela que H1 e H4
falham primeiro. **O moderador não pode ser quem escreveu a spec.**

**Antes de abrir o protótipo (5 min, sem mostrar nada):** Mom Test puro, passado,
não futuro. *"Me conta a última análise de ponto que você fez. Qual foi o
endereço? O que você abriu primeiro? Em que momento você saiu do Órbita, e para
quê? Você fez algum gráfico?"* Isto calibra H5 e H11 com comportamento relatado
real, antes de qualquer contaminação pelo protótipo.

---

### Tarefa 1 — Descoberta sem instrução *(testa H12 e H1)*

**Nas palavras do moderador:**
> "Chegou o lead 1223, em Franca. Essa é a tela que o Órbita te devolveu. Faz o
> que você faria hoje para decidir se esse ponto vai para o comitê. Vai falando o
> que está pensando. Se tiver dúvida, pode falar, mas eu não vou responder agora."

Nenhuma menção a arrastar, editar, trocar fonte ou IA. Variante A entra com o
aviso da IA; variante B sem.

**O que estou realmente observando:**
- Tempo até a primeira ação que modifica a montagem, sem prompt.
- Ele lê o aviso da IA ou dispensa? (Variante A.)
- Ele olha a composição do score por conta própria?
- Ele verbaliza "posso mexer nisso?" — e em que minuto.
- O que ele faz primeiro: lê, confere, ou procura o que falta.

**Conta como FALHA:**
- 5 minutos sem nenhuma ação de edição e sem verbalizar que é editável.
- Ele trata a tela como relatório de leitura e pede para "exportar" ou
  "passar para a planilha" sem ter tocado em nada.
- Só na variante A ele descobre a editabilidade — significa que a descoberta
  depende do aviso, e aviso dispensável (linha 56: "discreto e dispensável") é
  aviso que não será lido na terceira análise.

---

### Tarefa 2 — Conferir um número *(testa H4 e H3 — rode cedo, é a mais importante)*

**Nas palavras do moderador:**
> "Esse número de população aí. Ele te parece certo? Faz o que você faria para ter
> certeza."

Se ele não achar o seletor de fonte sozinho, deixe falhar e só no fim da tarefa
mostre onde está, e observe a reação à divergência.

**O que estou realmente observando:**
- O primeiro movimento é dentro do produto ou para fora dele (Google, planilha,
  colega)?
- Ao ver dois valores para o mesmo indicador: ele escolhe um, ou desconfia dos
  dois?
- O que ele faz com a limitação metodológica exibida (linhas 79-82) — lê, ignora,
  ou ela aumenta a desconfiança?
- Ele percebe que a troca de fonte **mudou o score**?

**Conta como FALHA:**
- Ele diz alguma variante de "então nenhum dos dois está certo" — a feature
  amplificou o problema raiz.
- Ele troca a fonte, o score muda, e ele não nota ou não sabe dizer por quê.
- Ele vai para o Google e, ao voltar, não tem onde registrar que discorda do dado
  (o caminho "contestar este dado" ficou Em aberto no parecer anterior; esta
  tarefa mostra o custo dessa pendência).

---

### Tarefa 3 — Custo por m², o exemplo-carro-chefe *(testa H1, H10 e o painel de camadas)*

**Nas palavras do moderador:**
> "O aluguel aqui é R$ 4.000 e a área de venda é 200 m². Isso importa para a tua
> decisão? Se importar, me mostra na tela."

**O que estou realmente observando:**
- Ele encontra a aba CAMADAS sozinho? Quanto tempo?
- Reconhece "camada" como a palavra dele (a spec acertou ao recuperar o termo,
  linhas 498-501 — mas confirme na boca dele, não presuma).
- Ao adicionar, ele consegue dizer o que aconteceu com o score?
- **Reação à etiqueta "régua proposta, ainda não homologada"**: ele lê? O que ele
  diz que faria com esse indicador no comitê?

**Conta como FALHA:**
- Ele diz que não levaria o indicador ao comitê por não ser homologado — o
  exemplo mais convincente da modularização morre na primeira sessão, e isso é
  achado grande, não detalhe.
- Ele adiciona e não percebe a mudança no score (a animação da linha 100 não
  cumpriu a função).
- Ele procura custo por m² em "Indicadores" na navegação lateral em vez do painel
  (confusão entre o painel e a seção "Indicadores" do menu, linha 463).

---

### Tarefa 4 — A IA discorda *(testa H3 e o portão de justificativa)*

**Nas palavras do moderador:**
> "Imagina que para esse ponto você acha que comércios no entorno não te diz nada.
> Tira esse bloco da tela."

A remoção dispara o alerta (linhas 108-111) e, se configurado como grave, exige
justificativa (linhas 113-117).

**O que estou realmente observando:**
- Ele lê o alerta ou fecha reflexo?
- Encontra o "não concordo" de um clique (linhas 358-362)?
- Se escreve justificativa: **conte os caracteres e leia o conteúdo.**
- Ele abandona a remoção por causa do portão?
- Ele pergunta quem vai ler aquilo.

**Conta como FALHA:**
- Justificativa com menos de ~15 caracteres ou sem conteúdo ("ok", "não se
  aplica", "."). O portão virou teatro e a trilha de auditoria é lixo com
  aparência de governança — pior que não ter.
- Ele desiste de uma ação legítima por causa do portão: o produto está impedindo
  julgamento humano correto, que é o oposto declarado do objetivo.
- Ele pergunta "isso vai aparecer para quem?" e muda o texto depois de saber. A
  justificativa virou peça política, não registro técnico. (Note que isto é
  justamente o risco que o parecer anterior levantou para o fio e resolveu
  tornando-o privado — mas a justificativa de alerta grave continua pública por
  decisão explícita, linhas 275-276. O risco migrou, não sumiu.)

---

### Tarefa 5 — Preparar o comitê *(testa H6 e a eliminação de passo)*

**Nas palavras do moderador:**
> "Você apresenta esse ponto no comitê amanhã de manhã. Se prepara."

Nenhuma menção ao comando "essa análise se sustenta no comitê?".

**O que estou realmente observando:**
- Ele aciona o comando principal espontaneamente (linhas 303-320)?
- Usa o COPIAR? Para onde ele colaria?
- Ele diz que ainda transcreveria para a planilha?
- Como ele explica o score percentual quando perguntado "e como você compara com
  a análise da semana passada?"

**Conta como FALHA:**
- Ele diz que transcreveria para a planilha do mesmo jeito. Nenhum passo foi
  eliminado — e a OKR é de tempo.
- Ele não encontra o comando principal sem ajuda.
- Perguntado sobre comparar com outra análise, ele compara os percentuais
  diretamente sem notar que os denominadores diferem. H6 confirmada como risco
  real, com observação, não com especulação.

---

### Riscos de viés deste método específico

- **Aquiescência.** Protótipo bonito + moderador interno = elogio. Mitigação:
  moderador neutro, e nunca pergunte "o que você achou"; pergunte "o que você
  faria agora".
- **Cenário cereja.** Franca foi escolhido porque a feature brilha nele.
  Mitigação: segundo cenário residencial em metade das sessões (seção 2).
- **Dados ilustrativos sequestram a sessão.** O analista vai contestar os números
  — comportamento real e esperado. Mitigação: declare uma vez, no início, que os
  números são ilustrativos, e **registre cada contestação como dado** (é medida
  direta da desconfiança), não como ruído a ser contornado.
- **Efeito novidade.** Arrastar bloco é divertido na primeira vez. Mitigação: não
  conte "ele adorou arrastar" como validação de H1; só a taxa de edição em uso
  real por 4 semanas vale.
- **Demanda característica na tarefa 4.** Eu mando ele remover um bloco; ele não
  escolheu remover. A reação ao alerta é válida, a decisão de remover não é.
  Declare isso na síntese.
- **N pequeno.** Se o time tem poucos analistas, 5 sessões podem ser quase o
  censo — o que é ótimo para achado qualitativo e **inútil** para qualquer
  percentual. Não escreva "60% dos analistas" com N=5.

---

## 4. Risco de sobrecarga cognitiva

**Veredito: são três produtos numa tela, mais um quarto embutido.**
Severidade: **BLOQUEIA** para o escopo do protótipo (não para a visão).

Separando por intenção de uso:

1. **Leitor de análise de ponto** — indicadores, score, composição, prós e
   contras, comentário. É o produto de hoje.
2. **Editor de montagem** — grade arrastável, redimensionamento, painel de
   camadas, seletor de fonte por bloco, salvar padrão. É um editor de dashboard.
3. **Interlocutor crítico** — assistente com fio único, dois modos, alertas por
   regra, portão de justificativa, "não concordo", retratação, ações aplicáveis
   com delta de score, pauta de comitê copiável. É um produto de conversa.
4. **Ferramenta de BI embutida** — construtor guiado por pergunta com catálogo de
   6 perguntas, régua de forma com 8 regras, análise de gráficos em 4 eixos. Isto
   tem spec própria neste repositório
   (`outputs/prompt-claude-design-orbita-graficos-incremento.md`); foi fundido
   aqui dentro.

Esses três modos competem por **atenção simultânea**: o analista arrasta um bloco
(modo editor) enquanto o score anima (modo leitor) e a IA dispara um alerta (modo
conversa). Três canais mudando ao mesmo tempo, dois deles não solicitados.

### Contradições internas que a sobrecarga expõe

- **AJUSTA — o bloco não cabe no que a spec pede dele.** Um único card precisa
  carregar: nome, valor, fonte, data-base, limitação metodológica em uma linha,
  contribuição no score, "régua proposta não homologada" quando aplicável,
  "sugerido pela IA, aceito por você" quando aplicável, e, se gráfico, "não entra
  no score" permanente — e tudo isso *"sem poluir"* (linha 80). São até 9 elementos
  de metadado por card multiplicados por 6-9 cards. Não cabe. A spec pede uma
  coisa impossível e o protótipo vai resolver isso em silêncio, provavelmente mal.
- **AJUSTA — painel recolhido que fala sozinho.** Linhas 258-260 pedem painel
  recolhido por padrão, que nunca cobre a grade; linhas 103-111 pedem alertas
  proativos. Recolhido + proativo = ou um badge que ninguém lê, ou uma intrusão
  disfarçada. A spec não escolhe. O teste da tarefa 4 revela qual dos dois.
- **AJUSTA — chips que se mexem.** Linhas 285 e 296: as sugestões mudam conforme o
  estado e ao menos uma se refere à última ação. Alvo móvel: o analista decide
  clicar num chip e ele já virou outro. Clássico gerador de erro. Mitigação:
  fixe os chips por 2-3 segundos após mudança de estado, ou faça a sugestão
  contextual aparecer em posição própria e separada dos chips estáveis.

### O que eu cortaria deste protótipo

**Cortar inteiro (vira spec própria, com validação própria):**
- Construtor de gráficos, régua de forma e os 4 eixos de análise de gráfico
  (linhas 131-242). Depende de H5, que não tem lastro — a jornada documentada não
  tem gráfico em passo nenhum. São ~110 das 515 linhas da spec, mais de 20% do
  esforço, apoiadas na hipótese menos sustentada. Se a demo precisa de gráfico,
  entregue **um** gráfico estático pronto (o de raio, P1), sem construtor e sem
  crítica de forma.
- Comparação entre análises (linhas 125-129). Depende de H6, que é decisão de
  governança não pesquisada. Mostrar comparação antes de resolver a unidade do
  score é demonstrar publicamente um problema em aberto.

**Esconder atrás de progressive disclosure:**
- **Seletor de fonte**: para dentro do bloco expandido / hover, não permanente em
  todos os cards. A procedência completa (fonte + data-base + limitação) vive no
  bloco expandido e no resumo exportado; no card, só o nome curto da fonte.
- **Salvar montagem como padrão** (linhas 391-397): só aparece ao fechar a
  análise, e só se houve edição. Hoje compete por atenção durante a montagem.
- **Eixos 3 e 4 da análise de IA** (pertinência e redundância): só no comando
  "se sustenta no comitê?", nunca proativos. São os mais julgadores e os mais
  suscetíveis de soar paternalistas.
- **Redimensionamento de bloco** (linha 71): arrastar para reordenar e
  redimensionar são duas interações; comece com reordenar.

**Manter sempre visível (e só isto):**
- Composição do score. É a mitigação mais importante da spec e a única que ataca o
  "por que 62%?" do comitê.
- Um canal de IA por vez.
- O rótulo "não entra no score" — se sobrar algum gráfico.

Com esse corte, a tela volta a ser **uma** tela com um modo de edição, e o teste
mede modularidade em vez de medir a capacidade do participante de sobreviver a
quatro produtos simultâneos.

---

## 5. Métricas de sucesso

Todas comportamentais. Nenhuma pergunta de opinião — "você gostou" e "você usaria"
não entram.

### Durante o teste (N pequeno: conte participantes, não percentuais)

| Sinal | Sucesso | Fracasso |
|---|---|---|
| Tempo até a 1ª edição não instruída (T1) | < 3 min, sem prompt | > 5 min ou não ocorre |
| Participantes que editam espontaneamente | ≥ 3 de 5 | ≤ 1 de 5 |
| Explicar por que o score mudou após editar (T3) | ≥ 4 de 5 acertam | ≤ 2 de 5 |
| Reação a duas fontes divergentes (T2) | escolhe uma e segue | desconfia das duas / vai ao Google |
| Saídas do protótipo para conferir fora | ≤ 1 por sessão | ≥ 3 por sessão |
| Justificativas de alerta grave com conteúdo real (T4) | ≥ 3 de 5 | ≥ 3 de 5 escrevem lixo curto |
| Ações legítimas abandonadas pelo portão | 0 | ≥ 1 |
| Aciona o comando de comitê sem dica (T5) | ≥ 3 de 5 | ≤ 1 de 5 |
| Diz que ainda transcreveria para a planilha (T5) | ≤ 1 de 5 | ≥ 3 de 5 |

**Desambiguação obrigatória de um resultado:** se o participante **não** edita nada,
isso pode ser a IA tendo acertado a montagem (ótimo) **ou** ele não ter percebido
que podia (péssimo). São opostos com a mesma aparência. Resolva no fim da sessão,
e só então: *"teve algo nessa tela que você teria montado diferente?"* Se ele lista
mudanças que não fez, era descoberta falhando.

### Nos primeiros usos reais (instrumente ANTES de lançar)

**Sinais de que funcionou**
- Taxa de edição da montagem entre 20% e 60% das análises, estável da semana 2 em
  diante (a estabilidade importa mais que o nível — queda a zero é efeito
  novidade).
- Mediana de 1 a 3 edições por análise editada. Zero significa editor inútil; mais
  de 8 significa que a proposta da IA não serve.
- Uso de padrão salvo > 25% das análises após 30 dias, **e** ao menos um padrão
  usado por quem não o criou (sem isso não houve difusão de conhecimento, que é o
  objetivo declarado de reduzir conhecimento prévio).
- Queda no tempo da etapa Órbita sem alta no tempo total ponta a ponta. Exige
  resolver `estudo-metrificar-tempo-analise.md` primeiro.
- Custo por m² presente em > 50% das análises de ponto comercial após 30 dias.
- Taxa de "não concordo" entre 5% e 25% dos alertas. Zero significa que ninguém lê
  os alertas; acima de 40% significa régua mal calibrada.

**Sinais de que falhou**
- Taxa de edição < 10% na semana 4 e nenhum participante relatando montagem
  divergente — a modularidade não é usada.
- Painel da IA fechado em > 70% das sessões a partir da semana 2.
- Mediana de comprimento das justificativas de alerta grave < 20 caracteres.
- Trocas de fonte altas (> 2 por análise) seguidas de abandono da análise ou de
  comentário registrando desconfiança — o seletor virou gerador de dúvida (H4
  falhando em produção).
- Planilhas de controle continuam com a mesma quantidade de campos preenchidos à
  mão.
- **Contra-métrica de guarda:** nº de análises devolvidas ou questionadas no
  comitê por score não comparável. Qualquer valor acima de zero no primeiro mês já
  pede revisão de H6.

**Nota de conformidade:** todas essas métricas são agregadas por regra, por
análise ou por período — **nenhuma por analista**. A proibição da linha 278 da spec
("nenhuma métrica individual de alertas ignorados") se aplica tanto à interface
quanto ao painel interno do time de produto. Se alguém puxar o recorte por pessoa
num comitê, a feature morre, exatamente como o parecer anterior antecipou. Escreva
isso no documento de instrumentação, não só na spec de interface.

---

## 6. Viés dentro da própria spec

### 6.1 — BLOQUEIA: linguagem de persona sintética apresentada como linguagem de campo

Linha 287, literal:

> *"Perguntas que devem aparecer, **nas palavras que o analista usa de verdade**:"*

Seguida de: *"Esse número bate com o que eu vejo no Google?"*, *"O que eu vou ter
que explicar no comitê?"*, *"Esse aluguel cabe no faturamento que esse ponto
consegue?"*

Rastreando a origem: essas frases vêm de
`revisao-analista-expansao-conversa-ia.md`, seção 3 ("O que falta, nas minhas
palavras"). E esse documento declara de si mesmo, nas linhas 6 a 9: *"é a
avaliação de um subagente que simula a perspectiva... Não é pesquisa com usuário
real e não substitui validação com o time de Expansão."*

Entre um documento e outro, a ressalva sumiu e a frase virou "as palavras que o
analista usa de verdade". Isso é **lavagem de evidência**: saída de modelo entra
como dado de campo. O conteúdo pode até estar certo — a frase do Google é
plausível porque o comportamento de conferir no Google **está** documentado na
descoberta. Mas a *formulação* não foi ouvida de ninguém.

**Correção mínima, de custo zero:** troque a linha 287 por *"Perguntas-hipótese, a
validar com analistas antes de fixar:"*. E, no teste, use a tarefa 5 para ouvir a
formulação real antes de mostrar os chips.

Isso vale para toda a cadeia: 14 itens marcados **Aplicado** na tabela final do
parecer anterior entraram na spec sem passar por usuário. Não estou dizendo que
estão errados. Estou dizendo que a spec hoje não distingue o que veio da
descoberta (evidência) do que veio do subagente (hipótese), e quem ler daqui a
três meses não vai conseguir distinguir.

### 6.2 — AJUSTA: reações do usuário escritas como requisito

- Linha 212: *"É a crítica mais objetiva e a que o analista aceita sem
  resistência."* Predição de comportamento, zero fonte.
- Linha 215: *"O eixo mais valioso."* Ranking de valor decidido antes de medir.
- Linha 342: *"Uma IA que só defende a régua contra o analista perde credibilidade
  e é fechada na terceira vez."* O "três" é da persona sintética.
- Linha 251: *"Teto de três alertas proativos seguidos."* Mesmo três.
- Linha 362: *"Se discordar custar um parágrafo, o analista fecha o painel."*
  Afirmação causal sobre comportamento humano.
- Linhas 373-374: *"três botões lado a lado viram menu."*

Nenhuma dessas é absurda; várias são boas apostas de design. O problema é o modo
verbal. Elas estão escritas como fatos conhecidos, e quem implementar vai tratá-las
como restrição dura em vez de parâmetro a calibrar. **Correção:** marque os números
(3 alertas, 3 botões, 3ª vez) como *parâmetros iniciais, a calibrar com uso*, numa
linha só.

### 6.3 — AJUSTA: a spec apaga a evidência do próprio fracasso

Linhas 299-301:

> *"NÃO inclua um chip 'por que o score ficou nesse percentual?' — a composição do
> score já está permanentemente visível na tela. Se o analista precisa perguntar
> isso, a tela falhou."*

A lógica está certa e a conclusão é autovedante. Se o analista precisar perguntar
isso, a tela falhou — e, tendo removido o chip, **você nunca vai saber que falhou**,
porque apagou o instrumento que mediria. É o equivalente a remover o termômetro
porque febre seria ruim.

**Correção:** no modo pesquisa, mantenha o chip e **meça os cliques**. Zero clique em
5 sessões é evidência de que a composição visível funciona — aí remova com lastro.
No modo demo, remova.

### 6.4 — BLOQUEIA: o cenário foi desenhado para a feature ganhar

Linhas 508-515. Cenário único, escolhido explicitamente por ser o caso em que
*"a população residente sozinha engana"*, com instrução de que *"a montagem padrão
da IA deve privilegiar fluxo e custo do ponto"*.

Isto é confirmação embutida no instrumento. Não existe estado do mundo, dentro
deste protótipo, em que a modularização apareça como desnecessária. Para demo é
legítimo e até recomendável. Para aprendizado, invalida tudo. Ver a correção na
seção 2 (segundo cenário residencial).

### 6.5 — AJUSTA: réguas inventadas vão virar proposta de fato

Linha 427: *"crie uma régua de 0 a 5 coerente"* para concorrentes, comércios e
custo por m², marcada como "régua proposta, ainda não homologada".

Um número mostrado numa tela, numa reunião de stakeholders, com animação e
contribuição no score, vira âncora. Daqui a dois meses alguém vai perguntar "por
que a régua de concorrência é essa?" e a resposta verdadeira será "um modelo
inventou para a demo". A etiqueta não impede ancoragem — ela só transfere a
responsabilidade.

**Correção barata:** antes do protótipo, peça a dois analistas que preencham a régua
de concorrência em 15 minutos (quantos concorrentes é 0, 3, 5 pontos). Vira régua
com autoria humana, dá material de conversa com o comitê, e custa menos que uma
reunião.

### 6.6 — REGISTRA: um viés que a spec acertou

Justiça: a seção TERMINOLOGIA (linhas 497-506) corrige a linguagem **com** lastro.
"Camada" está na descoberta ("inserção de camadas", lista de camadas mais usadas)
e a spec a recupera explicitamente. "Análise de ponto" vs. as quatro análises
também é fiel à jornada documentada. Esse é o padrão de decisão que o resto da
spec deveria seguir: citar de onde veio.

---

## Resumo — o que fazer antes de construir

Ordenado por custo, do mais barato ao mais caro. Os três primeiros não precisam de
protótipo nenhum e respondem as hipóteses mais caras.

1. **Pergunte ao autor da spec de onde veio o enunciado do problema** (linhas
   39-42). Ele não está na descoberta. 10 minutos. *(H7)*
2. **Teste de divergência de fontes, em papel.** Dois analistas, dois valores de
   população para o mesmo raio, com procedência. Observe o que fazem. 30 minutos
   cada. *(H4 — a hipótese mais perigosa, e a mais barata de testar)*
3. **Consulta de leitura em `analysis_data`** (somente leitura, com permissão e
   ambiente declarados): as combinações de camadas se repetem por analista? Isso
   responde H8 com comportamento real de 6 mil análises em vez de uma pergunta
   hipotética sem resposta. 1 hora.
4. **Exercício de tipologia com dois seniores**, 20 pontos do histórico: eles
   concordam sobre o tipo e sobre as camadas? Uma tarde. *(H2)*
5. **Corte gráficos e comparação do protótipo** (seção 4). Reduz a spec em ~25% e
   remove a parte com menos lastro.
6. **Construa o protótipo com o chaveamento demo/pesquisa** da seção 2.
7. **Rode as 5 tarefas com analistas ANTES da apresentação ao stakeholder.**
8. **Instrumente o produto antes do lançamento** com as métricas da seção 5,
   todas agregadas, nenhuma por analista.
9. **Leve três montagens diferentes a um comitê real** e observe se comparam
   scores. *(H6 — a que mata a feature depois de pronta)*

---

## Tabela de achados por severidade

| # | Achado | Severidade |
|---|---|---|
| H1 | "O analista quer montar a própria tela" contraria o remédio da descoberta (menos conhecimento prévio, menos passos) | BLOQUEIA |
| H2 | Não existe ground truth de "montagem certa por tipologia"; a IA propõe sem base | BLOQUEIA |
| H4 | Seletor de fonte pode amplificar a desconfiança nos números — o problema reportado original | BLOQUEIA |
| H6 | Comitê nunca foi pesquisado; score de denominador variável quebra comparabilidade de governança | BLOQUEIA |
| H7 | O enunciado do problema ("a tela é fixa") não aparece em nenhum documento de descoberta | BLOQUEIA |
| 4 | São três produtos numa tela, mais um BI embutido; escopo do protótipo precisa de corte | BLOQUEIA |
| 6.1 | Linguagem de persona sintética apresentada como "palavras que o analista usa de verdade" | BLOQUEIA |
| 6.4 | Cenário único desenhado para a feature ganhar; protótipo incapaz de gerar evidência contrária | BLOQUEIA |
| 2 | O protótipo convence, não aprende; falta chaveamento demo/pesquisa e telemetria | AJUSTA |
| H3 | Confiança numa IA apoiada nos números que o analista já desconfia | AJUSTA |
| H5 | Construtor de gráficos resolve um trabalho que não aparece na jornada documentada | AJUSTA |
| H10 | "Régua proposta não homologada" como mitigação de confiança, não testada, em 4 lugares | AJUSTA |
| H12 | Spec pede handles discretos e descoberta evidente ao mesmo tempo, sem decidir | AJUSTA |
| 0.2 | Montagem padrão omite Setor Censitário e Situação de território (camadas mais usadas) | AJUSTA |
| 4.b | Card com até 9 metadados e exigência de "sem poluir" — pedido impossível | AJUSTA |
| 4.c | Painel recolhido por padrão + alertas proativos: conflito não resolvido | AJUSTA |
| 4.d | Chips que mudam de conteúdo sob o cursor | AJUSTA |
| 6.2 | Reações do usuário escritas como requisito; números (3 alertas, 3 botões) sem lastro | AJUSTA |
| 6.3 | Remoção do chip de score apaga o instrumento que mediria a falha da tela | AJUSTA |
| 6.5 | Réguas inventadas pelo protótipo vão virar âncora de decisão | AJUSTA |
| 0.1 | A organização registra roteiro e não registra achado — risco de repetição | REGISTRA |
| H8 | "Salvar padrão" se apoia em pergunta hipotética de abril/2025 sem resposta registrada | REGISTRA |
| H9 | Requisito de privacidade do fio escrito por persona sintética; liderança não consultada | REGISTRA |
| H11 | Sem instrumentação de tempo (estudo de 5 linhas, inconcluso), a OKR 3h→1h é inverificável | REGISTRA |
| — | Pesquisa quantitativa de 08/10/2024 citada na descoberta e ausente do repositório | REGISTRA |
| 6.6 | Terminologia (camada, análise de ponto) é a parte da spec com lastro correto | REGISTRA |
