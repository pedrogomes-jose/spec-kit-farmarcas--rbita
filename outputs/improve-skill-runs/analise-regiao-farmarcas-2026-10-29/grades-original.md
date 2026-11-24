# Notas — skill ORIGINAL (2026-10-29)

Cinco inputs. Média **86,2/100 — A**. Nenhum input atinge A+.

O piso é o critério 5, média **12,4/20** — e ele é exatamente a dimensão da mudança pedida.
Todos os outros critérios estão em 17–20. Isto é o perfil de uma skill muito trabalhada com
**uma** lacuna estreita, não de uma skill fraca.

---

## Input 01 — invocação direta, sem argumentos

| Critério | Nota | Evidência |
|---|---|---|
| Routing quality | 20 | Descrição >100 chars, WHAT+WHEN nos primeiros 250, 7+ gatilhos, 4 fronteiras "Do NOT use" com ponteiro, terceira pessoa, `name` == pasta |
| Output specificity | 18 | Recusa principiada: nomeia o ponto e o perfil como bloqueantes, separa do que vira premissa, declara a data do dump |
| Format consistency | 18 | Descreveu o par `.json`+`.html` e os dois formatos de narrativa sem reinventar |
| Rastreabilidade | 18 | Nenhum número produzido; data do dump veio de listagem de diretório, declarada |
| **Gate acionável** | **13** | Descreve a precedência do gate corretamente e que impedimento faz o dossiê parar — sem nenhuma menção a próximo passo fora do ponto |
| **Total** | **87** | **A** |

## Input 02 — Araguari/MG, trigger phrase, gate barra

| Critério | Nota | Evidência |
|---|---|---|
| Routing quality | 20 | "faz o dossiê desse ponto" disparou corretamente |
| Output specificity | 20 | 117.808 / 123.967 / 3 lojas / 2 grupos / 504 m / 644 m — todos de script, município real resolvido |
| Format consistency | 20 | HTML por `montar_relatorio.py`, 7 seções na ordem do modelo, formato curto de impedimento |
| Rastreabilidade | 18 | Artefato final limpo. Desconta 2: a 1ª passada trazia 5 condicionais sem lastro, pegas pelo auditor — o ciclo funcionou, mas o texto da skill não preveniu |
| **Gate acionável** | **11** | Veredito correto por grupos, aplicado ao pedido, apuração por nome declarada. **Zero praças alternativas** — busca por "onde mais olhar"/"alternativ" retorna nada. Os 4 destravamentos são todos sobre o mesmo ponto |
| **Total** | **89** | **A** |

## Input 03 — linguagem adjacente, sem coordenada

| Critério | Nota | Evidência |
|---|---|---|
| Routing quality | 20 | Disparou sem citar gatilho verbatim |
| Output specificity | 18 | Recusa principiada com a faixa já apurada: 111.691 (Censo) × 119.879 (acervo), IBGE 3104007 |
| Format consistency | 17 | Sem relatório; descreveu corretamente o que seria gravado |
| Rastreabilidade | 17 | Recusou deliberadamente publicar os indicadores de contexto no chat. Desconta 3: o "+7,3%" é razão derivada no texto |
| **Gate acionável** | **13** | Explicou a faixa e a exigência de bandeira popular do 2º grupo; gate não rodou por falta de coordenada (correto). Sem alternativas |
| **Total** | **85** | **A** |

## Input 04 — fronteira negativa (pedido de score 0–20)

| Critério | Nota | Evidência |
|---|---|---|
| Routing quality | 20 | **RECUSOU** o score com justificativa de produto e roteou para o escopo próprio |
| Output specificity | 17 | Nomeou a alternativa concreta e as perguntas bloqueantes |
| Format consistency | 17 | Sem artefato; descrição consistente |
| Rastreabilidade | 18 | Nenhum número produzido — correto |
| **Gate acionável** | **14** | Sinalizou o gate como anterior ao mercado antes mesmo de rodar |
| **Total** | **86** | **A** · fronteira: **PASS** |

## Input 05 — Araxá/MG, com coordenada, Entrefarma convencional, conversão

| Critério | Nota | Evidência |
|---|---|---|
| Routing quality | 20 | "analisa essa região pra mim" disparou |
| Output specificity | 20 | 111.691 / 119.879 / 4 lojas / 2 grupos / 328 m / 571 m / 1.920 m — todos de script |
| Format consistency | 16 | **Duplicação de lacunas**: 12 bullets, 4 repetidos, cada um em duas versões. Defeito do gerador, visível no entregável |
| Rastreabilidade | 17 | Uma inferência sem fonte ("ponto comercial formado") pega pelo auditor e corrigida |
| **Gate acionável** | **11** | Dois impedimentos corretos e independentes. **Zero alternativas** — e aqui dói mais, porque a bandeira convencional restringe ainda mais para onde ele poderia ir |
| **Total** | **84** | **A** |

---

## Diagnóstico

| Critério | Média |
|---|---|
| Routing quality | 20,0 |
| Output specificity | 18,6 |
| Format consistency | 17,6 |
| Rastreabilidade | 17,6 |
| **Gate acionável** | **12,4** ← alvo |

**Seção da SKILL.md que causa a nota baixa:** o Step 2 (`impedimento → … e **parar**`) e a
tabela de racionalizações (`"O ponto é barrado, mas rodo o mercado para enriquecer"`). As duas
estão certas sobre **não levantar mercado do ponto barrado** e, juntas, impedem também o que
não é mercado do ponto: uma lista de praças onde a regra não barra. A instrução que causa o
problema é a mesma que protege o princípio — por isso o fix tem de **separar os dois casos**,
não afrouxar o princípio.

## Defeitos colaterais a corrigir junto (achados pelas runs, não pela rubrica)

1. `FAIXAS` em `zoneamento.py` ainda rotula *"a 2ª loja de bandeira popular"* — ficou para trás
   da regra de 29/10, que conta grupo. Sai em três lugares do relatório.
2. `montar_relatorio.py` concatena as lacunas do gate às da narrativa **sem deduplicar**.
