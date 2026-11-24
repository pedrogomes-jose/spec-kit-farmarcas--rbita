---
name: analise-regiao-farmarcas-enxuto
description: Mesma análise de região da skill analise-regiao-farmarcas, no mesmo gate de zoneamento e com os mesmos números, entregue numa versão CURTA do relatório — sem a seção de Fontes, sem os parágrafos explicativos de cada bloco e sem os marcadores de referência no texto. Use quando o usuário pedir o dossiê 'enxuto', 'curto', 'direto', 'resumido', 'só o essencial', 'sem as explicações', 'sem as fontes', 'uma página', ou disser que o relatório está longo demais para circular. Do NOT use quando o dossiê for ser auditado, revisado pelo subagente auditor-de-evidencia, ou apresentado a quem vai questionar a origem dos números → use /analise-regiao-farmarcas, porque a versão enxuta não permite conferir de onde veio nenhum valor; do NOT use para calcular o score de viabilidade 0–20 → o dossiê não pontua; do NOT use para escrever cards do board SQO → use /orbita-user-stories; do NOT use quando o pedido for exploratório ou conversacional ('vamos olhar essa região', 'vale abrir aqui?') → use /orbita, que já entrega a cópia enxuta no fim da conversa.
---

# Dossiê de região — versão enxuta

Mesma análise, mesmo gate, mesmos números. Muda **uma coisa**: o relatório sai
sem o aparato de conferência.

## Como esta skill funciona

Ela não tem scripts nem referências próprias. **Siga a SKILL.md da skill
original, do Step 0 ao Step 6, sem exceção**:

    .claude/skills/analise-regiao-farmarcas/SKILL.md

Todas as regras valem aqui sem alteração — o gate de zoneamento antes de
qualquer mercado, a pergunta obrigatória sobre o perfil do solicitante, nenhum
número fora de script, o dossiê não pontua, nenhum nome de pessoa, lacuna
sempre declarada, o quadrante SWOT, os dois raios. Os scripts são os mesmos
arquivos, em `../analise-regiao-farmarcas/scripts/`.

## A única diferença: o Step 6

No lugar do comando de geração da skill original, use:

```
python .claude/skills/analise-regiao-farmarcas/scripts/montar_relatorio.py     --config outputs/dossies/<arquivo>.json     --saida  outputs/dossies/<arquivo>.html     --detalhes ocultos
```

Caminho a partir da **raiz do projeto**, igual ao dos caminhos de `outputs/` —
os scripts são os da skill original, não há cópia deles aqui.

`--detalhes ocultos` tira do documento:

- a seção **Fontes** inteira — a tabela numerada e a procedência geral;
- os **parágrafos explicativos** de cada bloco (como ler a renda, o que o
  potencial de consumo é e não é, o que a régua de canal mede);
- os **marcadores de referência** `[1] [2] …` do texto das lentes, que ficariam
  órfãos sem a tabela que os resolve.

Fica no rodapé a origem da coordenada e a data do acervo, que são o mínimo que
não pode sumir — toda distância do relatório é medida a partir da coordenada.

O que NÃO muda: a seção "O que este dossiê NÃO sabe" continua presente e
recolhida, e "Para confirmar em campo" continua visível. Lacuna não é aparato
de conferência, é conteúdo — e lacuna silenciada vira conclusão errada.

## Critical — o que esta skill troca, e por quem paga

- **O dossiê enxuto não permite conferir número nenhum.** Quem o receber e
  duvidar de um valor não tem para onde olhar dentro do arquivo. Isso é o
  oposto da tese do produto: o Órbita existe porque o analista não confia no
  número, e a tabela de fontes é o que responde "de onde saiu isso".
- **Por isso, sempre que o dossiê for circular, gere as DUAS cópias** — a
  enxuta para circular e a completa para arquivar junto do JSON:

```
python .claude/skills/analise-regiao-farmarcas/scripts/montar_relatorio.py     --config outputs/dossies/<arquivo>.json     --saida  outputs/dossies/<arquivo>-completo.html     --detalhes abertos
```

  É o mesmo JSON de narrativa e a mesma rodada de scripts; muda só o modo.
- **A auditoria roda sobre a cópia completa.** O subagente
  `(⌕) auditor-de-evidencia` verifica se cada afirmação tem fonte declarada —
  sobre a versão enxuta ele reprovaria tudo, porque a seção de fontes não está
  lá. Aponte-o para o `-completo.html`.
- **Se o pedido for para apresentar a executivo ou a quem decide, prefira a
  skill original.** O ganho da versão enxuta é de leitura corrida; a perda é
  justamente na hora em que alguém pergunta de onde veio o número.

## Racionalizações que não valem

| Tentação | Por que não |
|---|---|
| "Gero só a enxuta, a completa ninguém abre" | a completa é o que permite responder quando perguntarem; sem ela a pergunta vira retrabalho de uma análise inteira |
| "Tiro também a seção de lacunas, que é longa" | lacuna não é aparato, é conteúdo — e lacuna silenciada vira conclusão errada |
| "Escrevo a fonte dentro do parágrafo, já que a seção saiu" | fonte no meio do texto é exatamente o que a regra da casa proíbe; o lugar dela é a cópia completa |
| "Mando a enxuta para o auditor, ele entende" | ele reprova tudo por ausência de fonte, e com razão |
| "Uso a enxuta para relatório de impedimento" | o relatório de impedimento não recolhe nem esconde explicação: lá o parágrafo é a mensagem, não o acompanhamento de um número |
