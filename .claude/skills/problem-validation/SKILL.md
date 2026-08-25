---
name: problem-validation
description: Valida uma hipótese de problema específica usando JTBD, The Mom Test e um critério objetivo de Go/No-Go — gera o job statement, o roteiro de entrevista focado em comportamento passado, a pergunta de switch interview, o pedido de fricção real (shadowing), o teste da moeda de troca, e termina com um veredito promissor/incerto/fraco. Use quando o usuário disser 'valida esse problema', 'vale a pena investigar isso', 'quero fazer o mom test', 'roteiro de validação de hipótese', 'go no-go dessa hipótese', 'JTBD desse problema', 'será que esse problema é real', ou apresentar UMA hipótese de problema específica para checar antes de investir esforço nela. Do NOT use para mapear um panorama amplo de dores e oportunidades → use /product-discovery; do NOT use para planejar logística de recrutamento ou screener completo de pesquisa → trate em conversa; do NOT use para conduzir de fato as entrevistas → esta skill entrega o roteiro e os critérios, não executa a pesquisa.
---

# problem-validation

Valida se UMA hipótese de problema específica é real e merece investimento, usando JTBD para enquadrar o job do usuário e The Mom Test para gerar um roteiro de entrevista focado em comportamento passado — nunca em opinião, desejo futuro ou validação de solução. Termina sempre com um critério objetivo de Go/No-Go e um veredito. Complementa `/product-discovery`: aquela skill mapeia um panorama amplo de dores (CSD + Árvore de Oportunidades); esta valida uma oportunidade específica em profundidade, com ou sem esse panorama prévio.

## Critical

- **Nunca valide a hipótese automaticamente.** Questione pressupostos, aponte vieses e lacunas antes de aceitar a formulação do problema como dado. Se o usuário já assumiu uma causa raiz, nomeie-a como suposição, não como fato.
- **Perguntas do roteiro Mom Test são sobre o PASSADO e comportamento real — nunca sobre opinião, desejo futuro, ou validação de solução.** Se uma pergunta gerada soaria como "você acharia útil...", "você usaria...", ou "você pagaria por...", ela está errada — reescreva focada no que a pessoa já fez.
- **Todo veredito final exige uma regra de parada objetiva.** Nunca termine a validação sem ela — sem regra de parada, o usuário não tem como saber quando parar de conversar e decidir.
- **Em modo encadeado (contexto vindo de `/product-discovery`), reutilize o que já foi levantado — mas isso não isenta a Suposição herdada do questionamento do Passo 1.** Outcome, Job Statement, oportunidade priorizada e Suposições/Dúvidas relacionadas não devem ser perguntados de novo — confirme e refine, não reinicie do zero. Porém, se a oportunidade priorizada carrega uma causa-raiz já assumida (uma Suposição, não uma Certeza, na CSD original), trate-a com o MESMO ceticismo que trataria uma suposição nova: nomeie-a, questione-a, e ofereça hipótese alternativa no Passo 1. "Reutilizar contexto" significa não repetir perguntas de enquadramento — nunca significa aceitar uma causa-raiz sem desafio.
- **Nunca invoque o subagente `ux-researcher` automaticamente.** O Passo 9 é sempre uma oferta explícita, nunca uma invocação implícita — o mesmo padrão de confirmação explícita usado em outras skills desta coleção (ex: `/prd-router` antes de ativar `/lovable-prompt` ou `/claude-system-builder`).

## Step 0: Leia Antes de Responder

| Fonte | Onde | O que extrair |
|-------|------|---------------|
| Contexto da conversa (modo encadeado) | conversa | Se a mensagem anterior veio de `/product-discovery`: outcome, Job Statement já esboçado, a sub-oportunidade priorizada, e as Suposições/Dúvidas da CSD relacionadas a ela |
| Descrição do problema (modo standalone) | conversa | O problema tal como o usuário formulou, o público-alvo, e qualquer causa-raiz já assumida |
| Aprendizados passados | references/learnings.md | Padrões e erros anteriores a evitar |

Se `references/learnings.md` não existir, prossiga sem ele.

## Determine o Modo de Entrada Antes de Responder

- **Encadeado:** a conversa contém outcome, Job Statement e/ou oportunidade priorizada vindos de uma sessão de `/product-discovery`. Confirme o que já foi levantado em 1–2 frases e vá direto para o Passo 1 (reformulação) — não repita perguntas de enquadramento que a Fase A do `product-discovery` já respondeu.
- **Standalone:** o usuário apresenta um problema direto, sem contexto prévio de discovery. Se faltar a descrição do problema ou o público-alvo, peça-os primeiro — no máximo 2 perguntas, não um formulário — antes de seguir para o Passo 1.

**Se nenhuma hipótese de problema foi fornecida** (invocação direta sem contexto), peça a hipótese e o público-alvo usando esta abertura, que já sinaliza o rigor do processo:

> "Para validar, preciso de duas coisas:
> 1. **A hipótese de problema:** qual problema específico você quer checar? (ex: 'Acho que [público] desiste de [ação] porque [causa assumida]')
> 2. **O público-alvo:** quem você entrevistaria para checar isso?
>
> Com isso, eu questiono os pressupostos da hipótese, monto o Job Statement (JTBD), gero um roteiro The Mom Test de perguntas 100% sobre comportamento passado — nada de opinião ou desejo futuro —, peço uma fricção real (shadowing) e um teste de moeda de troca, e fecho com sinais de Go/No-Go, uma regra de parada objetiva, e um veredito."

## Passo 1: Reformulação Neutra + Questionamento de Pressupostos

Reformule o problema como o usuário apresentou, de forma neutra — removendo qualquer causa-raiz ou solução já assumida na formulação original. Identifique explicitamente pelo menos 1 pressuposto não comprovado (ex: "vocês disseram X é o motivo — isso é uma suposição, ainda não uma certeza") e ofereça, se fizer sentido, uma hipótese alternativa.

## Passo 2: JTBD Completo

Se o modo é encadeado e já existe um Job Statement esboçado, confirme-o e refine-o com o que faltar. Caso contrário, derive um novo a partir do problema:

```
Quando [situação], quero [progresso], para que eu possa [resultado].
```

Identifique os três jobs:
- **Funcional:** a tarefa prática que a pessoa tenta completar.
- **Emocional:** como ela quer se sentir, ou parar de sentir.
- **Social:** como ela quer ser percebida por outros.

## Passo 3: 3 Premissas Críticas

Liste exatamente 3 coisas que precisam ser verdade sobre o comportamento PASSADO do usuário para que esse problema seja real (não sobre o futuro, não sobre a solução). Ex: "o usuário já tentou resolver isso manualmente pelo menos uma vez", "o usuário já perdeu tempo ou dinheiro mensurável com isso".

## Passo 4: Roteiro The Mom Test (4–5 perguntas + Switch Interview)

Gere 4–5 perguntas abertas, focadas em fatos passados e comportamento real — nunca em opinião, desejo futuro ou validação de solução (ver regra no bloco Critical). Cada pergunta deve poder ser respondida com um fato ("na última vez que isso aconteceu, o que você fez?"), não com uma opinião ("você acha que isso é um problema?").

Mais **1 pergunta de switch interview**: dirigida a alguém que já tentou resolver esse problema e desistiu, formulada para revelar por que a tentativa falhou (ex: "da última vez que você tentou resolver isso com [ferramenta/processo] e parou de usar, o que aconteceu exatamente?").

## Passo 5: Fricção Real (Shadowing)

Peça para o usuário pedir, ao final de cada entrevista, para a pessoa mostrar a "gambiarra" concreta: a planilha, o processo manual, ou a tela que ela usa hoje para lidar com esse problema. Nomeie especificamente o que pedir para ver, dado o contexto do problema — não um pedido genérico de "me mostra como você faz".

## Passo 6: Teste da Moeda de Troca

Proponha o melhor pedido de compromisso — tempo (ex: "topa testar um protótipo por 15 min na próxima semana?") ou reputação (ex: "posso te citar/apresentar pro seu time como early adopter?") — para fazer ao final da entrevista, que meça interesse real em vez de educação/cortesia.

## Passo 7: Critério de Go/No-Go

- **✅ Sinais de confirmação (Go):** 2–3 sinais que, se aparecerem espontaneamente nas conversas, confirmam que o problema é real e vale investir.
- **⛔ Sinais de descarte/pivô (No-Go):** 1–2 sinais que indicariam pivotar ou abandonar a hipótese.
- **🛑 Regra de parada:** uma regra objetiva e verificável baseada em N conversas (ex: "se nenhum dos sinais de confirmação emergir espontaneamente em 3–5 conversas, o problema não tem densidade suficiente para seguir").

## Passo 8: Veredito

Responda de forma direta:
- O problema parece **promissor**, **incerto** ou **fraco**, com base no que já se sabe até aqui?
- Qual é a **maior incerteza restante**?
- Qual a **evidência mínima necessária** para decidir se vale continuar investigando?

## Passo 9: Oferecer Revisão pelo Subagente ux-researcher

Depois de entregar o veredito do Passo 8, ofereça — nunca invoque automaticamente — uma segunda camada de revisão:

> "Quer que eu peça uma segunda opinião ao subagente **ux-researcher** antes de você ir a campo? Ele revisa especificamente: (a) se alguma pergunta do roteiro ainda soa como opinião disfarçada de comportamento passado, (b) se a amostra e a regra de parada são realistas para esse tipo de problema, e (c) se a hipótese reformulada no Passo 1 esgotou as causas alternativas mais óbvias."

Se o usuário confirmar, invoque o subagente `ux-researcher` passando como contexto a hipótese reformulada (Passo 1), o Job Statement (Passo 2), o roteiro completo (Passo 4) e o veredito (Passo 8) — não peça ao usuário para repetir nada disso.

Se o usuário recusar ou não responder à oferta, encerre normalmente. A oferta é sempre opcional e nunca bloqueia a entrega dos Passos 1–8.

## Formato de Output

Sempre entregue os 8 passos em sequência, numerados, em texto na conversa (esta skill não integra com Miro — é mais leve que `/product-discovery`, focada em preparar e avaliar a validação de uma hipótese, não em documentar um discovery amplo), seguidos sempre pela oferta do Passo 9. Use o Exemplo Trabalhado abaixo como referência de forma exata.

## Exemplo Trabalhado — Modo Standalone

**Input:**
> Acho que os freelancers que usam nosso app desistem porque a interface de criar tarefa é confusa. Quero validar se vale a pena investir nisso antes de redesenhar a tela.

**Resposta da skill:**

> **1. Reformulação neutra:** "Freelancers abandonam o fluxo de criação de tarefa" — sem assumir que a causa é a interface confusa. Pressuposto a questionar: vocês já concluíram que é a UI, mas isso ainda é uma Suposição. Hipótese alternativa: pode ser que o freelancer não entenda o que é uma "tarefa" no contexto da ferramenta (problema de modelo mental, não de UI).
>
> **2. Job Statement:** Quando um freelancer recebe uma solicitação de trabalho pelo app, ele quer registrar o que precisa ser feito rapidamente, para que possa voltar a focar no trabalho em si. (funcional: registrar a tarefa · emocional: não perder tempo com burocracia · social: parecer organizado para quem contratou)
>
> **3. Premissas críticas:**
> 1. O freelancer já tentou criar uma tarefa pelo menos uma vez e não completou o fluxo.
> 2. Esse abandono já causou um problema real e mensurável (perdeu prazo, teve que refazer, o contratante reclamou).
> 3. O freelancer já tentou uma forma alternativa de registrar isso (papel, outro app, mensagem).
>
> **4. Roteiro The Mom Test:**
> 1. Me conta sobre a última vez que você tentou criar uma tarefa no app — o que você fez, passo a passo?
> 2. O que você fez depois de travar ou desistir daquela vez?
> 3. Com que frequência isso acontece — toda vez que você recebe um trabalho novo, ou só às vezes?
> 4. Antes desse app, como você registrava as tarefas que precisava fazer?
> 5. **Switch interview:** você chegou a tentar usar [funcionalidade X do app] antes e parou? O que te fez parar exatamente?
>
> **5. Fricção real:** peça para a pessoa compartilhar a tela (print ou compartilhamento de tela) de onde ela registra as tarefas HOJE — seja um bloco de notas, WhatsApp para si mesmo, ou papel.
>
> **6. Moeda de troca:** pergunte se ela toparia testar um novo fluxo de criação de tarefa por 10 minutos ainda essa semana, com feedback ao vivo.
>
> **7. Go/No-Go:**
> - ✅ Go: (a) 3+ de 5 pessoas relatam ter abandonado o fluxo pelo menos uma vez; (b) a gambiarra mostrada (Passo 5) é consistente entre pessoas diferentes; (c) alguém aceita o teste de 10 min sem hesitar.
> - ⛔ No-Go: (a) as pessoas concluem a tarefa sem dificuldade quando você observa; (b) o "problema" só aparece quando você pergunta diretamente, nunca espontaneamente.
> - 🛑 Regra de parada: se nenhum sinal de Go aparecer espontaneamente em 5 conversas, a hipótese "interface confusa causa abandono" não tem densidade suficiente — considere a hipótese alternativa do Passo 1.
>
> **8. Veredito preliminar:** **Incerto.** A hipótese é plausível mas ainda não tem evidência de comportamento real — só a opinião do time. Maior incerteza: se o abandono é por UI ou por modelo mental (o que muda completamente a solução). Evidência mínima: 3 relatos espontâneos e consistentes de abandono, com a gambiarra mostrada, antes de decidir redesenhar a tela.
>
> **9.** Quer que eu peça uma segunda opinião ao subagente **ux-researcher** antes de você ir a campo? Ele revisa se alguma pergunta do roteiro ainda soa como opinião disfarçada de comportamento passado, se a amostra e a regra de parada são realistas, e se a hipótese do Passo 1 esgotou as causas alternativas mais óbvias.

## Exemplo Trabalhado — Modo Encadeado (a partir de `/product-discovery`)

**Contexto herdado da conversa (Fase D do `/product-discovery`):**
> Outcome: aumentar a taxa de conclusão do fechamento de folha de 68% para 90% em 90 dias. Job Statement: Quando o time de RH fecha a folha, quer ter certeza de que cada contracheque está correto antes de aprovar, para liberar o pagamento sem gerar erro. Oportunidade priorizada: "RH re-confere manualmente mesmo com sistema validando automaticamente" (evidência: 1 citação de cliente, marcada `[APROFUNDAR: evidência fraca]`). Suposição relacionada: falta de confiança no sistema, não falta de validação técnica.

**Input do usuário:** "Quer que eu já valide a oportunidade prioritária?" → **Sim.**

**Resposta da skill (modo encadeado — pula direto para o Passo 1, sem re-perguntar outcome/usuários/JTBD):**

> Usando o que já levantamos no discovery: outcome de fechamento de folha, Job Statement de "ter certeza antes de aprovar", e a oportunidade priorizada — RH confere manualmente mesmo com validação automática disponível.
>
> **1. Reformulação neutra:** "RH não confia o suficiente na validação automática do sistema para parar de conferir manualmente" — sem assumir que resolver é adicionar mais validação técnica (essa era a Suposição original, já sinalizada como incerta na Fase B).
>
> **2. Job Statement:** reaproveitado do discovery, sem alterações — já está completo (funcional/emocional/social já identificados).
>
> **3. Premissas críticas:**
> 1. O RH já foi exposto a pelo menos um erro de contracheque no passado que não foi pego pelo sistema.
> 2. Esse hábito de conferência manual já consome tempo mensurável (parte dos 3.2 dias em times grandes).
> 3. O RH já tentou confiar apenas no sistema pelo menos uma vez e teve um resultado ruim, ou nunca tentou por medo.
>
> [... roteiro Mom Test, switch interview, fricção real, moeda de troca e Go/No-Go seguem o mesmo formato do exemplo standalone, adaptados ao contexto de confiança em validação automática de folha de pagamento]
>
> **8. Veredito preliminar:** Incerto — a única evidência hoje é 1 citação (`[APROFUNDAR: evidência fraca]` na CSD). Maior incerteza: se a desconfiança vem de uma experiência real de erro, ou é um hábito herdado sem incidente concreto. Evidência mínima: 3 relatos espontâneos de "já fui pego de surpresa por um erro que o sistema não pegou" antes de decidir investir em transparência/explicabilidade da validação em vez de só robustecer a validação técnica.
>
> **9.** Quer que eu peça uma segunda opinião ao subagente **ux-researcher** antes de você ir a campo? Ele revisa se alguma pergunta do roteiro ainda soa como opinião disfarçada de comportamento passado, se a amostra e a regra de parada são realistas, e se a hipótese do Passo 1 esgotou as causas alternativas mais óbvias.

## Saídas Fora de Escopo

Esta skill NÃO lida com:
- Mapear um panorama amplo de dores e oportunidades (Matriz CSD, Árvore de Oportunidades) → use /product-discovery
- Planejamento de logística de recrutamento ou screener completo de pesquisa (cronograma, qualificação de participantes) → trate em conversa
- Conduzir as entrevistas de fato → esta skill entrega o roteiro e os critérios de decisão, não executa a pesquisa

## Cross-Skill Routing

- Se o usuário quiser depois organizar múltiplas oportunidades (validadas ou não) numa visão mais ampla → recomende `/product-discovery`.
- Se esta skill for chamada a partir de `/product-discovery` (Fase D, D6), sempre honre o contexto passado — outcome, Job Statement, oportunidade priorizada, Suposições/Dúvidas — sem re-perguntar (ver "Determine o Modo de Entrada").
- Após o veredito do Passo 8, sempre ofereça (Passo 9) uma segunda opinião do subagente `ux-researcher` sobre qualidade de evidência, viés das perguntas e formulação da hipótese — apenas se o usuário confirmar.

## Atalhos Comuns — Não Tome Estes

| O que Claude pode pensar | Por que está errado |
|---------------------------|----------------------|
| "O usuário já parece convencido do problema, posso pular o questionamento de pressupostos" | É exatamente quando o usuário está mais convencido que o risco de confirmação é maior. O Passo 1 é obrigatório mesmo com alta confiança aparente. |
| "Essa pergunta de opinião é mais fácil de responder, vou incluir uma no roteiro" | Perguntas de opinião ("você acharia útil?") geram respostas educadas, não fatos. Todo roteiro Mom Test é 100% sobre comportamento passado. |
| "O modo é encadeado, mas vou confirmar tudo de novo por segurança" | Re-perguntar o que o `/product-discovery` já levantou desperdiça o contexto e frustra o usuário. Confirme em 1-2 frases e siga em frente. |
| "A oportunidade já veio com uma causa-raiz assumida do discovery anterior, então já está validada" | Uma Suposição herdada continua sendo uma Suposição, não uma Certeza. Reutilizar o enquadramento (outcome, JTBD) não significa aceitar a causa-raiz sem o mesmo questionamento do Passo 1 que se aplicaria a uma suposição nova. |
| "Posso pular a regra de parada, o usuário vai saber quando parar" | Sem regra objetiva, a validação nunca termina — o usuário continua conversando indefinidamente sem um critério de decisão. |
| "3 premissas é muito específico, vou listar quantas fizerem sentido" | O formato fixo (exatamente 3) força priorização. Uma lista aberta vira uma lista de desejos, não de premissas testáveis. |
| "O veredito do Passo 8 já está completo, posso pular a oferta do Passo 9" | A oferta é o que conecta o roteiro gerado a uma segunda camada de revisão de qualidade — pular a oferta silenciosamente priva o usuário da chance de checar viés antes de ir a campo. |
| "O usuário parece confiante na hipótese, vou invocar o ux-researcher direto sem perguntar" | Confirmação explícita é obrigatória, nunca inferida do tom da mensagem — mesmo padrão de confirmação já usado em `/prd-router` antes de ativar outra skill ou agente. |

## Antes de Marcar Completo

- [ ] Modo de entrada determinado (encadeado ou standalone) antes de responder
- [ ] Se encadeado: contexto do `/product-discovery` reutilizado, nenhuma pergunta repetida
- [ ] Passo 1: pelo menos 1 pressuposto questionado explicitamente
- [ ] Passo 2: Job Statement completo com jobs funcional, emocional e social
- [ ] Passo 3: exatamente 3 premissas críticas sobre comportamento passado
- [ ] Passo 4: 4-5 perguntas Mom Test, todas sobre fatos passados (nenhuma pede opinião, desejo futuro ou validação de solução) + 1 pergunta de switch interview
- [ ] Passo 5: pedido de fricção real específico ao contexto, não genérico
- [ ] Passo 6: teste da moeda de troca com pedido concreto (tempo ou reputação)
- [ ] Passo 7: sinais de Go, sinais de No-Go, e regra de parada objetiva baseada em N conversas
- [ ] Passo 8: veredito (promissor/incerto/fraco) + maior incerteza + evidência mínima necessária
- [ ] Passo 9: oferta explícita de revisão pelo subagente `ux-researcher` feita — sem invocação automática, sem exigir confirmação para entregar os Passos 1-8

## Após Concluir: Registrar Aprendizado

Adicione ao final de `references/learnings.md`:

```
Data: [hoje]
Modo: [standalone / encadeado]
Problema validado: [1 linha]
O que funcionou: [padrão de pergunta ou abordagem que gerou boa resposta]
O que não funcionou: [pergunta que precisou reescrita ou gerou confusão]
Edge case: [algo inesperado]
```
