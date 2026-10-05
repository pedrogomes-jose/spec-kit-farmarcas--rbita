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
