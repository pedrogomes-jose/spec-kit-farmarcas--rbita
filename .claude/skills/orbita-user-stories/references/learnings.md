# Learnings — orbita-user-stories skill runs

Log entries appended here after each real use. Format:

Date: [YYYY-MM-DD]
What worked: [specific pattern that produced good output]
What didn't: [what failed or needed correction]
Edge case: [anything unexpected]
Rodadas do revisor-clareza-junior: [quantas vezes pediu ajuste até aprovar]

---

Date: 2026-09-17
What worked: Verificação de código real (Grep/Glob) antes de escrever "Escopo do card" pegou 2 problemas que teriam virado retrabalho: (1) a suposição inicial de que a base de municípios já existia ou era trivial de mapear estava errada — nenhuma das 3 collections do Órbita tem população por município, só um campo solto `properties.Municipio` usado por uma Lambda de geocodificação, sem relação com o pedido; (2) o revisor encontrou um segundo ponto de código (branch `sectorCodes.length === 0` em `radiusSearch/index.ts:142`) que a primeira versão do card não tinha citado — mudar só `aggregateDemographicDensity` teria deixado um caminho de código sem a correção.
What didn't: A primeira versão do card explicava o "o quê" da mudança mas não o "porquê" técnico (por que somar por setor para de funcionar em raio grande) — o revisor teve que puxar isso do próprio código (`$geoIntersects` não recorta geometria) e marcar como inferência a confirmar. Escrever o "porquê" desde a primeira versão, não só nas correções, deveria ser o padrão.
Edge case: O card acabou legitimamente bloqueado por decisões de produto/dado (limiar de "raio nível de cidade" indefinido no código, regra de multi-município indefinida, existência da base de municípios não confirmada) que nenhuma leitura de código resolve — o revisor corretamente distinguiu isso de um problema de clareza de texto e recomendou publicar como "aguardando refinamento" em vez de forçar aprovação. Isso confirma que a regra da skill de "parar após 2 rodadas e declarar ao usuário" é o comportamento certo, não uma limitação.
Rodadas do revisor-clareza-junior: 2 (primeira: "precisa de ajuste" por falta do "porquê" e 3 casos de borda faltando; segunda: ainda "precisa de ajuste" para 2 gaps novos e reais — definição de "score de viabilidade" e cobertura do branch de população zero — mas confirmou que os itens restantes são decisão de produto, não defeito do card; card publicado em "aguardando refinamento" após a 2ª rodada, sem forçar 3ª aprovação).

---

Date: 2026-09-17
What worked: Checagem posterior do `webapp-orbita-angular` (pedida pelo usuário depois do card já criado) achou um problema estrutural que a Step 0 original não pegou: o texto "Caminho/rota" do card SQO-1279 tinha copiado a frase-padrão do template ("Radar → ícone de 4 quadradinhos → Órbita → Órbita IA") sem checar se essa tela existe no frontend. Ela não existe — grep no menu principal (`navigation.component.ts`, 5 itens, nenhum "Órbita IA"), nenhuma chamada a `GET /layers/radius` ou `POST /analysis` do `api-agent-orbita` em lugar nenhum do repo, e `environment.ts` não tem base de API para o `api-agent-orbita`. Ou seja, o backend que o card altera pode não ter nenhum consumidor de frontend ainda.
What didn't: A Step 0 desta skill lista os 3 repositórios para checar "caminho/endpoint" mas não instrui explicitamente a verificar se a FUNCIONALIDADE (menu/tela) que o "Caminho/rota" descreve realmente existe no frontend — só verifica nomes de arquivo/endpoint quando já citados no Escopo do card. Isso deixou passar uma frase de navegação copiada do template sem validação. Falta reforçar: "Caminho/rota" é uma pista tão verificável quanto "Escopo do card" e deve passar pelo mesmo Grep/Glob antes de ser aceita.
Edge case: O usuário reforçou nesta sessão que o `webapp-orbita-angular` concentra muita regra de negócio no frontend (não só orquestração de UI) — reforça que a Step 0 desta skill não pode tratar o front como "só onde citar o componente", precisa ser lido com o mesmo rigor que o backend ao procurar regra de negócio existente, não só ao procurar pista de código.
Rodadas do revisor-clareza-junior: 0 nesta rodada (achado veio de investigação pós-publicação, não de uma nova revisão de card) — registrado como comentário no Jira (SQO-1279) em vez de reescrever a descrição, para manter histórico de que a suposição original existiu e foi corrigida.

---

Date: 2026-09-17
What worked: Ao ser corrigido pelo usuário ("o nome da tela é /orbita/ai"), a skill não aceitou nem rejeitou a informação — parou e comparou contra o código (grep por "ai" nas rotas reais, incluindo `git fetch` e checagem de outras branches) antes de decidir o que fazer. Como o código não confirmou a rota em nenhuma branch, a skill perguntou ao usuário a origem da informação em vez de escolher um dos dois lados sozinha. Resposta: existe um 4º repositório do Órbita, fora dos 3 mapeados por esta skill, que não foi clonado.
What didn't: A busca inicial por "Órbita IA" usou o padrão `IA['"]` (letras I-A) e não encontrou nada — mas a rota real é `ai` (letras A-I, ordem invertida). "IA" e "ai" são strings diferentes, não uma diferença de maiúsculas/minúsculas; buscar case-insensitive por um não cobre o outro. Isso quase gerou uma conclusão errada publicada num card real (SQO-1279 já tinha ido ao ar com "nenhum consumidor de frontend encontrado" antes dessa correção).
Edge case: A cobertura desta skill é limitada aos 3 repositórios mapeados no Step 0 (`api-agent-orbita`, `api-orbita-nodejs`, `webapp-orbita-angular`). Existe pelo menos um 4º repositório do Órbita (a tela `/orbita/ai`) fora desse escopo, ainda não identificado por nome. Qualquer afirmação do tipo "não encontrei consumidor/tela para X" deve ser qualificada como "não encontrei nestes 3 repositórios", nunca como fato absoluto sobre o produto inteiro — ver memória `orbita-repositorios-locais` para o aviso permanente sobre esse gap.
Rodadas do revisor-clareza-junior: 0 nesta rodada (correção baseada em informação direta do usuário, não em nova investigação de código nem em nova revisão de clareza) — card atualizado via `editJiraIssue` e comentário de correção adicionado ao SQO-1279.

## 2026-10-19 — Pedido de PRD completo (comparação de pontos comerciais)
- **O que funcionou:** a fronteira negativa do "Out of Scope" segurou — pedido
  de escrever o PRD em si foi recusado e roteado para `/claude-system-builder`
  (primário), `/lovable-prompt` e `/prd-router`, sem gerar card algum.
- **O que não funcionou:** nada a ajustar nesta rodada; não houve geração de card.
- **Caso de borda:** pedido que usa vocabulário do Órbita e soa próximo do
  backlog ("requisitos funcionais") mas é o artefato *anterior* ao card. Sinal
  de corte: o usuário pede objetivo/métricas/requisitos, não cards.
- **Rodadas do revisor-clareza-junior:** 0 (não aplicável — nenhum card gerado).

---

Date: 2026-10-19
PROCEDENCIA: entrada gerada por RUN DE AVALIACAO da skill (/improve-skill), nao por uso real.
Os achados de codigo abaixo foram produzidos por subagente e NAO foram reconferidos manualmente —
tratar como pista a verificar com Grep antes de usar como fato num card.
What worked: Conferir a direcao de "melhor" de cada dimensao no codigo antes de escrever a regra de "quem ganha a linha" evitou o erro mais provavel da feature de comparacao de pontos — densidade (`scoring.ts:65-70`) e renda (`economicClass.ts:7-35`) pontuam ao contrario do senso comum (menor densidade e menor renda pontuam mais). "Maior valor vence" teria recomendado o ponto errado em 2 das 4 linhas.
What didn't: A premissa do pedido ("pontos ja analisados") nao existe no codigo — o `api-agent-orbita` e stateless, nenhuma operacao de escrita em todo o `src`. A feature de 2 cards virou uma de 5 porque persistencia e identidade da analise (endereco/raio) precisaram virar card. Vale checar "o substantivo do pedido existe como entidade persistida?" antes de quebrar em cards, nao depois.
Edge case: O Cross-Skill Routing bloqueou os 2 cards de frontend (tela de resultado fora dos 3 repos mapeados), deixando a feature pedida pela metade no board. A regra esta certa, mas o resultado precisa ser comunicado como bloqueio acionavel ("clonem o 4o repo" / "usem /user-stories"), nao como recusa.
Rodadas do revisor-clareza-junior: 0 — run de avaliacao da skill (outputs/improve-skill-runs/orbita-user-stories-2026-10-19/outputs-original/02.md), subagente nao invocado e nenhum ticket criado por restricao do run.

## 2026-11-17 — Card de bug a partir de print de erro em produção

**O que funcionou:** partir da string literal do erro e grepar os 3 repos
achou a origem exata (`api-agent-orbita/src/db/mongo.ts`) em 1 busca, e dali
o endpoint, o consumidor e os campos lidos. Card de bug a partir de print de
DevTools é viável e fica forte quando a mensagem de erro é única no código.

**O que não funcionou:** citei ~9 números de linha de memória do que tinha
lido, e 8 estavam deslocados em 1-5 linhas. Pior: atribuí o campo
`PotencialdeConsumoTotalDrogarias` a `collections.ts` quando ele está
hardcoded em `cityInfluence.ts:79-81` — e `collections.ts:57` tem um campo
**de nome parecido, de outra base** (`...-SetorCensitario`). Um júnior teria
mexido na base errada. **Conferir arquivo:linha com `nl`/`sed -n` no momento
de escrever o card, não de memória da leitura anterior.**

**Caso de borda:** critério de aceite pode ser logicamente inválido sem ser
óbvio. Usei `summary.averageIncome` preenchido como prova de que as fontes
municipais resolveram — mas o código faz fallback para o valor de setor
quando a renda municipal é nula (`radiusSearch/index.ts:388-391`), então o
campo vem preenchido com a fonte quebrada. **Antes de escrever "então o
campo X vem preenchido", checar se existe fallback que o preenche por outro
caminho.** Mesma classe: ponto fora de qualquer município devolve o resultado
de setor, não zeros.

**Armadilha de validação:** `pnpm test` mocka o Mongo (`cityInfluence.test.ts:22`),
então passa verde com produção quebrada. O critério fixo "Passar nos testes
definidos por QA" vira armadilha em card de dado — precisa dizer qual é a
validação real.

**Precedente reutilizável:** `api-agent-orbita/scripts/dt-1162-migracao.ts`
(card SQO-1162) é o padrão do time para mexer em fonte quebrada: dry-run por
padrão, `--apply`, `--rollback --backup=`. Card que pede diagnóstico em
produção deve apontar esse script em vez de só dizer "diagnosticar".

**Rodadas do revisor-clareza-junior:** 1 rodada, veredito "precisa de ajuste"
com 4 bloqueios reais + 9 correções de citação. Todas verificadas no código
antes de incorporar — e todas procediam.

## 2026-11-24 — Zoneamento: markup quebrado no Jira + 7 cards que nunca subiram

**O que funcionou:** antes de reescrever, ler o campo `description` cru dos
cards existentes (`getJiraIssue`) separou três estados que de fora pareciam um
só: 2 cards preenchidos mas **com markup errado**, 3 ainda com o template vazio
e `xxxxxx`, e 7 que só existiam no markdown local. O pedido do usuário ("os
cards ficaram ruins") cobria os três, mas cada um exigia uma ação diferente.

**O que não funcionou — e é a lição principal desta rodada:** a rodada anterior
gravou os cards em **wiki markup do Jira** (`h5.`, `_itálico_`, `# lista`,
`|| tabela ||`, `{quote}`) num campo que o Jira interpreta como **markdown**.
Resultado em tela: `#` e `##` viraram títulos H1/H2 gigantes no lugar de lista
numerada, a tabela do glossário virou texto solto, e `_Contexto:_` saiu em
itálico onde o template usa negrito. **`editJiraIssue` com
`contentFormat: markdown` exige markdown de verdade — nunca wiki markup.**

**Duas armadilhas de serialização confirmadas nesta sessão:**
- `[DEFAULT: 3 pts]` sai renderizado como `\[DEFAULT: 3 pts\]`, com as barras à
  mostra. **Usar parênteses:** `(DEFAULT: 3 pts — confirmar com o time)`.
- Um item de lista que começa com `1)` dentro de um `*` vira lista ordenada
  aninhada. **Não abrir item de bullet com número seguido de parêntese.**

**Caso de borda — o template oficial não tem "Pontos em aberto".** O SQO-1060
tem 7 seções; esta skill exige 8. Quando o usuário pede "o template puro", as
duas regras colidem. Saída adotada: dobrar as lacunas **bloqueantes de
estimativa** dentro de "Escopo do card"/"Regras de negócio" (que são seções do
template) e deixar o resto num bloco curto de "Pendências de negócio" **depois**
das 7 seções, preservando a forma do template. O documento longo em
`outputs/orbita-user-stories/` fica como arquivo do que foi cortado.

**Glossário:** repetido em 12 cards, ele diverge na primeira mudança de regra.
Virou página única no Confluence (4555636743), filha da página de regras, com os
cards linkando. Vale como padrão para épico grande.

**Rodadas do revisor-clareza-junior:** 0 — **o usuário proibiu explicitamente
executá-lo nesta rodada**. O Step 5 da skill foi pulado por ordem direta e isso
foi declarado ao usuário na entrega, não contornado em silêncio.
