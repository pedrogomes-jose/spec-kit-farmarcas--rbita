# Estudo sobre histórico de análises

> Fonte: https://farmarcas.atlassian.net/wiki/spaces/SR/pages/3487334403/Estudo+sobre+hist+rico+de+an+lises · Última atualização no Confluence: set. 30, 2025
> Nota: esta página continha imagens no Confluence original que não puderam ser migradas automaticamente. Consulte a fonte acima para o conteúdo visual completo.

# Mapeamento do Fluxo de Análise

Uma análise é um registro criado para avaliar oportunidades de negócio, como abertura de lojas, expansão de franquias, etc. Ela reúne informações do lead, empreendedor, localização, status do processo e interações dos envolvidos.

## Armazenamento das Análises

* As análises são salvas na coleção `analysis_data` do banco de dados MongoDB, atualmente possuímos mais de 6 mil análises no banco de dados de Develop, desconsiderando os status das mesmas.

Total de análises no banco de dados de Develop (não reflete dados reais do banco de dados de Produção, porém, é um valor bem próximo disso)
## Principais campos do documento de análise

* **\_id:** Identificador único da análise.
* **lead:** Código do lead relacionado.
* **entrepreneur:** Nome(s) do empreendedor.
* **createdAt:** Data/hora em que a análise foi criada (quando o processo começou).
* **modifiedAt:** Data/hora da última alteração (quando alguém mexeu na análise).
* **status:** Situação atual da análise (ex: Em análise, Pendente, Reprovado, Em negócio).
* **analysisSituation:** Etapa do processo (ex: Aprovado, Em análise).
* **comment:** Lista de comentários feitos por usuários, cada um com autor e data.
* **createdBy / updatedBy:** Quem criou e quem fez a última alteração.

Exemplo de um documento de análise do banco de dados.
## Cálculo do tempo em aberto de uma análise

* **Início:** Quando a análise é criada (`createdAt`).
* **Fim:** Quando o status muda para um dos finais (ex: Reprovado, Em negócio).
* **Tempo em aberto:** Diferença entre a data de criação e a data de encerramento.

Criei uma pipeline de Aggregation no MongoDB para conseguir um valor médio de tempo em que as análises ficam abertas, com os dados do bando de Develop, e o resultado foi uma média de 76 dias abertos.

Cálculo da média de tempo em que uma análise fica em aberto.
Porém, existem muitas divergências no tempo em que as análises permanecem abertas, onde as análises com menores tempo em aberto possuem um tempo médio de segundos , enquanto as que estão com maior tempo médio aberto, batem anos.

Comparação: acima, análises que passaram mais tempo em aberto e abaixo, análises que passaram menos tempo em aberto.
## Registro de Alterações

* Cada alteração registra quem fez (`updatedBy`) e quando (`modifiedAt`).
* Comentários mostram o autor e a data de cada interação.

## Status possíveis

* **InAnalise:** Em análise (a equipe está avaliando o caso)
* **Pending:** Pendente (aguardando alguma ação ou informação)
* **Sended:** Enviado (foi encaminhado para outro responsável)
* **Reproved:** Reprovado (não foi aprovado para seguir)
* **FinalizedLead:** Lead finalizado (o processo do lead foi encerrado)
* **Business:** Em negócio (virou uma oportunidade de negócio)

## Diagrama de como os dados são tratados

Diagrama do fluxo de gravação das análises
## Conclusão

O mapeamento do fluxo de análise mostra que o processo é estruturado e rastreável, permitindo identificar o ciclo completo de cada oportunidade de negócio. O uso do MongoDB para armazenar as análises garante flexibilidade e escalabilidade, enquanto os campos de data e status possibilitam o acompanhamento preciso do tempo em aberto de cada registro.

A média de 76 dias para o tempo em aberto das análises indica que, embora o fluxo funcione, casos extremos podem distorcer o resultado, sugerindo a necessidade de revisões periódicas e ajustes nos processos para evitar gargalos. O registro detalhado de alterações e comentários contribui para a transparência e facilita auditorias e decisões.
