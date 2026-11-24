# Rubrica — analise-regiao-farmarcas (2026-10-29)

Cinco critérios, 20 pontos cada, /100. A+ = 90+. A = 80–89. B = 70–79. C = <70.

A mudança sob avaliação: **quando o gate de zoneamento reprova um ponto, o dossiê
deve indicar outras praças disponíveis** — disponíveis pela regra vigente, que
conta grupos econômicos e não lojas.

---

## 1. Routing quality (description) — universal

Pontua a frontmatter, não o corpo. Conta caracteres e frases-gatilho antes de ler
o body.

| Faixa | Âncora |
|---|---|
| 18–20 | >100 chars; WHAT+WHEN nos primeiros 250; ≥3 frases que o usuário digitaria; fronteira "Do NOT use for" com ponteiro para skill irmã existente; terceira pessoa; `name` do YAML == nome da pasta |
| 14–17 | Tudo acima menos um item — tipicamente fronteira sem ponteiro, ou WHEN depois dos 250 chars |
| 10–13 | Sem fronteira negativa, ou menos de 3 gatilhos, ou primeira pessoa |
| 4–9 | Descrição < 100 chars, ou sem WHEN |
| 0–3 | Sem frontmatter, ou `name` divergente da pasta (routing silenciosamente quebrado) |

## 2. Output specificity — universal

O entregável usa o contexto real (endereço dado, município resolvido, números do
dump) ou poderia ter sido escrito sem ler nada?

| Faixa | Âncora |
|---|---|
| 18–20 | Todo número do entregável vem de saída de script desta execução; município, faixa, teto e contagens são os reais |
| 14–17 | **Caminho de recusa principiada:** faltou contexto obrigatório (coordenada, perfil do solicitante) e a saída PARA, nomeia o que falta e diz o próximo passo, em vez de fabricar. Pontuar aqui, não em 4/20 |
| 10–13 | Mistura: parte real, parte genérica ou plausível-mas-não-verificada |
| 4–9 | Números plausíveis sem origem; "cerca de", "aproximadamente" |
| 0–3 | Saída que poderia servir a qualquer endereço |

## 3. Output format consistency — universal

Três execuções do mesmo input produziriam a mesma forma?

| Faixa | Âncora |
|---|---|
| 18–20 | HTML gerado por `montar_relatorio.py`; JSON de narrativa no formato declarado; blocos na ordem do modelo; o veredito do gate decide QUAL relatório sem ambiguidade |
| 14–17 | Forma certa com um desvio (bloco fora de ordem, campo do JSON inventado) |
| 10–13 | Markdown à mão onde o modelo pede HTML, ou formato reinventado |
| 4–9 | Forma diferente a cada execução |
| 0–3 | Sem formato reconhecível |

## 4. DOMÍNIO — Rastreabilidade do número (primário)

É a disciplina central desta skill: número sem script de origem não entra.

| Faixa | Âncora |
|---|---|
| 18–20 | Nenhuma aritmética feita na narrativa; toda comparação contra percentil, mediana ou o próprio município; fonte de dado (não de ferramenta) declarada por item; divergência entre bases sai com os dois números |
| 14–17 | Um ou dois valores derivados no texto, com as parcelas impressas ao lado |
| 10–13 | Percentual ou razão calculado pelo modelo sem o dado bruto ao lado |
| 4–9 | Número sem origem rastreável, ou fonte atribuída à base errada |
| 0–3 | Número inventado, ou comparação com outro dossiê / outra análise |

## 5. DOMÍNIO — Gate de zoneamento acionável (secundário) ← critério da mudança

O gate decide certo pela regra vigente **e**, quando barra, o dossiê entrega o
próximo passo útil em vez de só fechar a porta.

| Faixa | Âncora |
|---|---|
| 18–20 | Veredito correto contando **grupos econômicos** (não lojas), aplicado ao PEDIDO e não ao estado atual; quando barra, lista praças alternativas **filtradas por disponibilidade de zoneamento**, cada linha nomeando a localidade da UTC, com a ressalva de que grupo é apurado por nome e não por CNPJ; deixa explícito que indicar praça não é análise de mercado do ponto barrado |
| 14–17 | Veredito correto e alternativas presentes, mas sem o filtro de disponibilidade, ou sem a ressalva da apuração por nome |
| 10–13 | Veredito correto e o dossiê para sem indicar nada — o comportamento de hoje |
| 4–9 | Veredito pela contagem de lojas em vez de grupos, ou aplicado ao estado atual em vez do pedido |
| 0–3 | Gate não roda, roda depois do mercado, ou o ponto barrado recebe dossiê completo de mercado |

---

## Observações de calibração

- **Recusa principiada não é falha.** Input sem coordenada ou sem perfil do
  solicitante deve parar e perguntar. Pontuar 14–18 em 2 e em 4, não 4/20.
- **Input 04 é fronteira negativa.** Pedir o score 0–20 do produto deve ser
  recusado com ponteiro. Acertar = 20; responder com um score = 0.
- Cidade com muitas lojas de um único grupo **continua disponível**. Alternativa
  filtrada por contagem de lojas erra esse caso e cai para 4–9 no critério 5.
