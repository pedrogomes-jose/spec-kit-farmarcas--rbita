# Grades — skill genérica `/user-stories` avaliada contra o rubric do Órbita

Nota metodológica: a skill genérica nunca foi desenhada para o board SQO nem
para os 3 repositórios do Órbita — ela é avaliada aqui contra o rubric
específico do Órbita para evidenciar exatamente o gap que motivou a
especialização, não como uma falha da skill genérica no seu próprio domínio.

## Input 01 — invocação direta, sem PRD

| Critério | Nota (/20) | Evidência |
|---|---|---|
| Roteamento | 16 | Descrição genérica dispara em "/user-stories" normalmente; não é específica de Órbita, mas não é o teste relevante aqui. |
| Especificidade | 16 | Recusa corretamente (Step 1 Caso B), pede PRD/descrição — comportamento correto, âncora de recusa aplicada. |
| Consistência de formato | 14 | O template de recusa é consistente, mas não menciona o formato Jira SQO nem os repositórios. |
| Fidelidade ao template SQO | 4 | Não sabe que existe um template Jira específico — nunca vai chegar a usá-lo. |
| Verificação de código + revisão júnior | 4 | Não tem noção de repositórios do Órbita nem de subagente de revisão. |
| **Total** | **54/100** | Grade: F (mas correto no que se propõe — a nota baixa é estrutural, não um bug) |

## Input 02 — PRD + pedido explícito pro board SQO

| Critério | Nota (/20) | Evidência |
|---|---|---|
| Roteamento | 14 | Dispara na palavra "cards"/"quebra em histórias", mas ignora "board SQO" — não tem noção do projeto Jira específico. |
| Especificidade | 12 | Usa o conteúdo do PRD/estudo real, mas sem checar `scoring.ts` ou o endpoint `/analysis` — cita algo genérico como "endpoint de análise" sem confirmar. |
| Consistência de formato | 8 | Produz Como/Eu quero/Para que + Gherkin solto — formato que o board SQO não aceita como está. |
| Fidelidade ao template SQO | 2 | Não usa nenhuma das 7 seções oficiais. |
| Verificação de código + revisão júnior | 2 | Nenhuma verificação de repositório, nenhum subagente chamado. |
| **Total** | **38/100** | Grade: F |

## Input 03 — linguagem adjacente, sem citar "user story"/"SQO"

| Critério | Nota (/20) | Evidência |
|---|---|---|
| Roteamento | 15 | "quero que o time comece a implementar" casa com o gatilho "quebra essa feature em histórias" mesmo sem citar o termo literalmente. |
| Especificidade | 10 | Reconhece `competitorsTotal`, `/layers/radius`, `/analysis` porque estão no texto do usuário — mas não confirma no código se `/analysis` realmente ignora esse campo hoje. |
| Consistência de formato | 8 | Mesmo formato solto do Input 02. |
| Fidelidade ao template SQO | 2 | Idem Input 02. |
| Verificação de código + revisão júnior | 2 | Idem Input 02 — nenhuma checagem real no `api-agent-orbita`. |
| **Total** | **37/100** | Grade: F |

**Média (01-03): 43/100 — F.** O gap não está na qualidade geral da skill
genérica (ela é bem construída para seu próprio escopo), está inteiramente
nos dois critérios de domínio que ela nunca foi desenhada para cobrir —
confirmando que a especialização pedida (não um tuning incremental) era a
abordagem certa.
