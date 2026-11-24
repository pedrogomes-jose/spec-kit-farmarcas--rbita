# analise-regiao-farmarcas — refino da leitura da região · 2026-11-06

## O que foi pedido

Três mudanças na seção **Leitura da região** (as 4 lentes):

1. Deixar de fora qualquer menção ou análise de confiança **baixa ou nenhuma**.
2. Tirar do texto as explicações do **motivo** da nota de confiança.
3. Estruturar o layout da seção como um **SWOT**.

## Como foi verificado

**Não** foi rodado o loop sintético de 3 entradas do `/improve-skill`. Cada
entrada custaria um dossiê inteiro — pipeline de scripts sobre o dump das bases,
seis execuções entre original e melhorada — para medir uma mudança de formato.
No lugar disso, a verificação foi feita contra a **entrada real**: o dossiê de
Santa Fé do Sul/SP, com as 4 lentes e 15 itens já escritos, reescrito sob a
regra nova e regerado. É regressão sobre caso real, não sobre caso fabricado.

Medido na regeneração:

| | Antes | Depois |
|---|---|---|
| Prosa das lentes | 12.998 chars | 10.633 chars (**−18%**) |
| Itens nas lentes | 15 | 14 |
| Lacunas declaradas | 8 | 9 |
| Ocorrências de "confiança" no relatório | 15 | **0** |
| Layout | 4 blocos empilhados | quadrante 2×2 |

O dossiê de impedimento (Redenção/PA) foi regerado como controle: nenhuma
mudança de conteúdo, só os ~400 bytes de CSS novo.

Caminhos de borda testados direto na função: lente vazia (as 4 células saem
desenhadas, com a linha de ausência), ordem fixa independente da ordem do JSON,
narrativa sem lentes, e o aviso novo disparando sobre a narrativa antiga — ele
listou os 15 itens corretamente.

## A regra que ficou

A confiança **continua obrigatória de avaliar**. Mudou a função dela: era o 4º
campo escrito do item, virou **critério de entrada**.

| Confiança da afirmação | Destino |
|---|---|
| alta | lente, sem rótulo e sem o motivo |
| média | lente, sem rótulo — e o limite de método vira lacuna |
| baixa | lacuna, nunca lente |
| nenhuma | lacuna, nunca lente |

O corte é **por afirmação, não por item**: "a loja fechou a 335 m" é cadastral e
fica; "por que ela fechou" não está em base nenhuma e sai.

### O conflito que apareceu, e como foi resolvido

A skill **obriga** certas ressalvas a andarem coladas ao número — que a régua de
canal é a média da UF e não a venda daquela loja, que MAT é acumulado de 12
meses, que o setor entrou rateado com tal cobertura. Tirá-las junto com a nota
de confiança trocaria um defeito de leitura por um erro de conteúdo.

A linha que separa as duas coisas: **o que o número É fica; o quanto confiar
nele sai.** O teste é uma pergunta — a frase descreve o *indicador* ou a
*qualidade* dele? "É a média do canal em São Paulo, não a venda desta farmácia"
descreve o indicador, e sem ela o leitor lê outro número. "Confiança média,
porque a base não traz a dispersão dentro do canal" descreve a qualidade, e vai
para a lacuna, onde se diz o que destravaria.

Essa distinção não estava no pedido. Foi ela que impediu a mudança de quebrar
quatro regras do bloco `## Critical`.

## Arquivos alterados

| Arquivo | O que mudou |
|---|---|
| `scripts/montar_relatorio.py` | `bloco_lentes` passa a montar quadrante SWOT em ordem fixa, com célula vazia desenhada e rótulo de eixo; CSS `.swot` com responsivo e impressão; aviso novo quando a narrativa escreve a nota de confiança |
| `references/lentes-do-dossie.md` | anatomia do item de 4 para 3 campos; seção nova da confiança como critério de entrada; tabela "o que fica / o que sai"; descrição do quadrante; regra de corte em três etapas |
| `references/modelo-de-dossie.md` | layout SWOT, regra da confiança, esqueleto markdown sem a linha de confiança, regra de redação nova |
| `SKILL.md` | dois bullets em `## Critical` (corte por confiança, quadrante SWOT) mais o da distinção indicador/qualidade; Step 4 com a tabela de destino; Step 5 recebendo o que foi cortado; 7 racionalizações novas; 5 linhas de checklist |
| `outputs/dossies/2026-11-06_santa-fe-do-sul-sp_*.json/.html` | narrativa reescrita sob a regra nova e relatório regerado |

## O que ficou em aberto

- Renderizar a dispersão do centroide na tabela de praças alternativas.
- Trocar o truncamento da distância por arredondamento em `montar_relatorio.py`.
- O bloco de lacunas de setor só ingere o raio de 300 m, não o de 5 km.
