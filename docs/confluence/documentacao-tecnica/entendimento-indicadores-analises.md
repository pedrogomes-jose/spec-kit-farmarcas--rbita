# Entendimento dos indicadores de analises

> Fonte: https://farmarcas.atlassian.net/wiki/spaces/SR/pages/3881205769/Entendimento+dos+indicadores+de+analises · Última atualização no Confluence: mar. 05, 2026

[https://farmarcas.atlassian.net/browse/SQO-714](https://farmarcas.atlassian.net/browse/SQO-714)

‌

#### 1. Resumo da Análise

Foi realizada uma investigação técnica para entender a divergência de dados entre as telas de **Indicadores** e **Contratos Fechados**. Identificamos que o sistema apresentava números inconsistentes devido a filtros restritivos no Front-end e na forma como as agregações eram realizadas no Back-end.

* **Participantes da Call de Alinhamento:** Alexandre Gasparino, Gustavo Soares de Ávila e Leandro Mendes Filho.
* **Tarefa de Referência:** [SQO-734 - Corrigir as informações exibidas na seção "Influência por UF"](https://farmarcas.atlassian.net/browse/SQO-734)

---

#### 2. Origem dos Dados 

Para garantir a transparência solicitada nos critérios de aceite, detalhamos abaixo de onde cada tela extrai suas informações:

‌

**A. Tela de Análise de Pontos (Big Numbers):**

* **Classe:** `GetAnalysisCommand`
* **Funcionamento:** Os dados são extraídos da coleção `AnalysisData`. Toda vez que uma análise é criada ou editada, o comando executa um `$facet` no MongoDB para contar os documentos em tempo real.
* **Regra de Contagem:**

    * **Status (statusNumber):** Filtra apenas os status `0, 1, 4, 5`.
    * **Situação (analysisNumber):** Filtra apenas as situações `6, 7` (Mapeamento Ativo e Receptivo).
    
* **Reflexo imediato:** Sim. Ao criar uma análise com status "Pendente", o comando `GetAnalysisCommand` reprocessa a contagem e o Big Number é incrementado instantaneamente na tela.

‌

**B. Tela de Indicadores / Influência por UF:**

* **Classe:** `SummaryBreakdownAnalysisCommand`
* **Funcionamento:** Esta tela cruza dados de duas coleções: `ContractData` e `AnalysisData`.
* **Fluxo de Dados:**

    1. Busca contratos na `ContractData` dentro do range de data selecionado.
    2. Extrai os `idAnalysis` desses contratos.
    3. Busca as situações correspondentes na `AnalysisData` usando os IDs encontrados.
    4. Realiza o agrupamento (GroupBy) em memória no C# para montar o gráfico de situações.
    

‌

---

#### 3. Identificação da Causa Raiz (Divergência de Dados)

Durante a análise do código, identificamos o motivo pelo qual os dados "não batiam":

1. **Filtro Restritivo no Front-end:** O Front-end estava filtrando os resultados para exibir apenas o que era considerado "Negócio Fechado" (`AnalysisStatus.BUSINESS`), ignorando outros status que compunham o total da categoria.

    * _Código identificado:_ `series.name === 'total' ... data.name == AnalysisStatus.BUSINESS`
    
2. **Dependência de Status Específico:** As métricas de _Pré-contratos / Taxa de Conversão / Pontos Aprovados_ estavam condicionadas estritamente ao status de "Negócio", o que causava a sensação de dados faltantes quando contratos estavam em outros estágios.

‌

---

#### 4. Detalhamento das Regras de Negócio (Mapeamento de Status)

Para fins de conferência, os indicadores seguem o mapeamento abaixo (Exemplo baseado em Setembro):

| Situação da Análise | Valor Total (Contratos) | Valor Negócio (Fechado) |
| --- | --- | --- |
| Falta Informação | 12 | 3 |
| Pendente | 17 | 5 |
| Validação | 2 | 25 |
| Aprovado | 103 | 16 |
| Mapeamento Receptivo | 59 | 13 |

_Nota: O sistema agora garante que a soma das séries individuais corresponda ao valor exibido no "Total" do breakdown._

‌

---

#### 5. Implementação e Correções (Tarefa SQO-734)

As seguintes correções foram aplicadas para sanar as inconsistências na seção **Influência por UF**:

1. **Padronização do Lookup Manual:** Como a biblioteca interna de `Lookup` apresentava limitações de sintaxe (aspas incorretas), a lógica de cruzamento entre `ContractData` e `AnalysisData` foi validada para garantir que nenhum contrato fosse perdido no processo de junção.
2. **Validação de Coordenadas (Geográfica):** Foi implementada uma camada de validação global para Latitude e Longitude. Isso impede que dados "sujos" (coordenadas fora do Brasil ou do range global) entrem no sistema via Excel, o que causava erros de plotagem no mapa de Influência por UF.

    * _Regra:_ Latitude \[-34, +6\] / Longitude \[-74, -35\].
    
3. **Ajuste no Preenchimento de Enums:** A função `FillSituations` foi revisada para garantir que todos os nomes de Enums (`AnalysisStatus` e `AnalysisSituation`) sejam convertidos corretamente para seus valores numéricos, evitando que o Front-end receba chaves de dicionário inconsistentes.

‌

---

#### 6. Conclusão

Com as alterações realizadas, os dados exibidos na tela de Indicadores agora refletem fielmente o estado da base de dados de Contratos e Análises. A credibilidade do sistema foi restabelecida através da transparência dos filtros e da validação rigorosa na entrada dos dados.
