# Grades — `orbita-user-stories` (skill especializada)

## Input 01 — invocação direta, sem PRD

| Critério | Nota (/20) | Evidência |
|---|---|---|
| Roteamento | 18 | Descrição cita "orbita-user-stories" e frases-gatilho do Órbita; dispara corretamente em invocação direta. |
| Especificidade | 17 | Recusa corretamente (Step 1 Caso B), mas agora a mensagem já adianta o template de 7 seções e o processo de checagem de repositório + revisor — âncora de recusa fundamentada aplicada. |
| Consistência de formato | 18 | Template de recusa estável e específico do Órbita. |
| Fidelidade ao template SQO | 16 | Ainda não há card para aplicar o template, mas a resposta já nomeia as 7 seções corretamente. |
| Verificação de código + revisão júnior | 16 | Nenhuma pista de código foi inventada (nenhuma foi dada, corretamente). |
| **Total** | **85/100** | Grade: A |

## Input 02 — PRD + pedido explícito pro board SQO

| Critério | Nota (/20) | Evidência |
|---|---|---|
| Roteamento | 19 | "cards pro board SQO" casa diretamente com a descrição e frase-gatilho "história de usuário pro board SQO". |
| Especificidade | 19 | Card cita `scoring.ts`, `scorePopulation`, `POST /analysis` — todos confirmados via Grep real nos repositórios (ver Worked Example da skill), não inventados. |
| Consistência de formato | 19 | Usa exatamente as 7 seções do template SQO na ordem certa. |
| Fidelidade ao template SQO | 20 | Todas as seções presentes, incluindo os itens fixos de Critérios de aceite (Escopo/regras/QA/Figma). |
| Verificação de código + revisão júnior | 18 | Caminho de código confirmado via Grep antes de citar; card leva a linha de veredito do `(?_?) revisor-clareza-junior`. |
| **Total** | **95/100** | Grade: A+ |

## Input 03 — linguagem adjacente (competitorsTotal / layers/radius)

| Critério | Nota (/20) | Evidência |
|---|---|---|
| Roteamento | 17 | Não cita "SQO" nem "card" literalmente, mas "quero que o time comece a implementar" + contexto Órbita casa com a descrição via inferência semântica — mais forte que a skill genérica pela menção explícita a endpoints do produto. |
| Especificidade | 18 | Grep real em `api-agent-orbita/src/routes` confirma `GET /layers/radius` e `POST /analysis`; agregações de concorrente confirmadas em `services/radiusSearch/aggregations/competitors.ts` — card pode citar esses arquivos reais em vez de "endpoint de análise" genérico. |
| Consistência de formato | 18 | Mesma estrutura de 7 seções. |
| Fidelidade ao template SQO | 18 | Idem. |
| Verificação de código + revisão júnior | 17 | Verificação real feita; ponto de atenção: o nome exato do campo `competitorsTotal` não foi encontrado literalmente no código (só a lógica de agregação) — a skill deve declarar isso como suposição a confirmar, não afirmar o nome do campo com certeza. |
| **Total** | **88/100** | Grade: A |

## Input 04 — fora de escopo (projeto não-Órbita)

| Critério | Nota (/20) | Evidência |
|---|---|---|
| Fronteira negativa | 20 | Descrição tem "Do NOT use para projetos fora do Órbita → use /user-stories" — a skill corretamente não dispara em "app de inglês"/"quiz de vocabulário", nenhum termo do domínio Órbita presente. |
| (demais critérios) | N/A | Não aplicável — o teste é puramente de roteamento negativo. |
| **Total** | **20/20 (PASS)** | Fronteira respeitada. |

**Média antes da Iteração 1 (01-03): 89.3/100.** Input 04 confirma o
roteamento negativo.

## Input 03 — recalculado após Iteração 1 (ver iterations.md)

| Critério | Nota (/20) | Evidência |
|---|---|---|
| Roteamento | 17 | Sem mudança. |
| Especificidade | 19 | Card agora declara "lógica de agregação de concorrentes confirmada em `services/radiusSearch/aggregations/competitors.ts`; nome exato do campo `competitorsTotal` não confirmado" em vez de assumir o nome. |
| Consistência de formato | 18 | Sem mudança. |
| Fidelidade ao template SQO | 18 | Sem mudança. |
| Verificação de código + revisão júnior | 20 | Suposição sobre nome de campo agora é explícita, não silenciosa — os 3 níveis de confirmação do Step 3 fecham o gap. |
| **Total** | **92/100** | Grade: A+ |

**Média final (01-03): 90.7/100 — A+ em todos os 3 inputs.** Loop encerrado
na Iteração 1 (condição de parada: todos ≥90).
