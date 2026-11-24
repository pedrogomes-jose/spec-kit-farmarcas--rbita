# Resumo — /improve-skill em orbita-user-stories (2026-10-19)

## Antes → depois

| | Baseline | Melhorada |
|---|---|---|
| Média (3 inputs pontuados) | **75,0 — B** | **93,3 — A+** |
| Pior input | 03: **54 (C)** | 03: **93 (A+)** |
| Teste de fronteira (input 04) | PASS | PASS |
| Iterações | — | **1** |

## O achado que motivou tudo

A skill original **não conseguia produzir o card SQO-1323** — o card que o
usuário aprovou nesta sessão. O input 03 reproduziu aquele cenário (transcrição
de reunião → card de Gestão de Lojas do Radar → board SQO) e a skill entregou
**zero cards**: a regra de `Cross-Skill Routing` mandou parar e rotear para
`/user-stories`, que emite Gherkin solto, fora do template que o board exige.

O escopo da skill estava definido pelo **produto/código**, quando o que a
determina é o **board de destino**. Corrigido isso, o mesmo input passou a
produzir 4 cards no template correto.

## Correção de maior alavancagem

Escopo por board, não por produto: o Step 0 decide primeiro de qual produto é o
card; se for Órbita, a verificação nos 3 repositórios continua obrigatória; se
for outro produto no mesmo board, o Step 3 é pulado e o card declara
"Não aplicável — fora dos repositórios do Órbita" em vez de inventar caminho.
Sozinha, essa mudança moveu o input 03 em +39 pontos.

## O conflito que precisou de decisão, não de conserto

A skill exigia Gherkin nos critérios de aceite; o SQO-1323 aprovado não tem
Gherkin — tem os 4 critérios fixos do board e 10 regras numeradas. Como estava,
a skill reprovaria o próprio card-modelo. Resolvido com duas formas explícitas
(A: Gherkin + fixos, para comportamento observável de UI/API; B: só os fixos,
quando cada regra numerada já é verificável por QA), com o
`(?_?) revisor-clareza-junior` checando se a escolha se sustenta. Os dois
re-runs usaram formas diferentes e ambos pontuaram 20/20 em formato.

## O que a skill passou a fazer que não fazia

1. Seção obrigatória **"Pontos em aberto"** com trecho literal da fonte, ou
   "Nenhum" — separa o que está decidido do que não está.
2. **Step 3B — efeitos de segunda ordem** (4 perguntas obrigatórias). No re-run
   do input 03 isso capturou sozinho um impacto que ninguém tinha mapeado: o
   total de lojas ativas enviado à Febrafar e a parceiros **sobe no dia do
   deploy**, porque as bloqueadas deixam de ser status e passam a contar.
3. **Contexto com tríade** (comportamento atual / por que está errado / impacto
   de negócio) e registro de **alternativas descartadas**.
4. **Regras numeradas e atômicas**, com item obrigatório declarando o que
   **NÃO** muda.
5. **Transcrição de reunião como fonte primária**, com leitura de 100% e porção
   declarada quando parcial.
6. **Step 6B** para atualizar card existente, com guarda contra campo herdado de
   template (precedente real: SQO-1279 e SQO-1323).

## Pendência deixada em aberto, não resolvida sozinha

O subagente `(?_?) revisor-clareza-junior` é declaradamente do Órbita na própria
description ("cards do Órbita", "domínio Órbita", "três repositórios do Órbita").
A skill agora avisa o subagente quando o card é de produto fora do Órbita, para
ele não cobrar pista de código — mas a description do **agente** não foi alterada.
Se o uso em cards não-Órbita virar rotina, vale ajustar o agente também.
