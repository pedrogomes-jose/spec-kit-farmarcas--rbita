# POC - Consulta Interna de Farmácias no raio

> Fonte: https://farmarcas.atlassian.net/wiki/spaces/SR/pages/4055924738/POC+-+Consulta+Interna+de+Farm+cias+no+raio · Última atualização no Confluence: mai. 25, 2026

# Definição do Objetivo

‌

Esta POC tem como objetivo validar a viabilidade técnica de implementar uma experiência conversacional no Órbita, permitindo que o usuário faça perguntas em linguagem natural, como “Quais farmácias existem em um raio de 300 metros da Av. Paulista, 2300?”. A proposta é utilizar IA para interpretar a intenção da pergunta e normalizar a resposta, mantendo as consultas a dados internos sob responsabilidade da aplicação, reduzindo riscos de alucinação e fuga de contexto.

‌

## Contexto Atual

‌

Atualmente, já possuímos uma base relevante implementada, que é o fluxo de busca por endereço e raio:

* O usuário informa um endereço no frontend;
* O sistema obtém coordenadas do endereço;
* Um raio é aplicado, inicialmente 300m;
* O backend consulta camadas no MongoDB, incluindo a camada `Concorrentes`;
* A API retorna um `summary` e camadas detalhadas;
* Depois, o backend envia parte desses dados ao Gemini para gerar uma análise de viabilidade.

Atualmente, a IA não interpreta perguntas livres, ela apenas analisa dados já estruturados.

‌

## Viabilidade Técnica

‌

A implementação é viável com a stack atual. Não há necessidade inicial de trocar Gemini por outra ferramenta de IA. O modelo já suporta interpretação de texto e retorno estruturado via Zod. A principal mudança é criar um novo fluxo na API, separando interpretação da pergunta, consulta determinística e normalização da resposta.

A IA não deve ser responsável por “inventar” ou “descobrir” farmácias. Ela deve apenas interpretar a pergunta e normalizar a resposta final. A busca real deve continuar sendo feita por código e banco de dados.

### Evidências Técnicas Encontradas

A API já possui integração com Gemini via LangChain e saída estruturada com Zod. Também já existe consulta geoespacial por raio em `/layers/radius`, incluindo a camada `Concorrentes`. Portanto, a POC pode reaproveitar parte relevante da arquitetura atual, criando principalmente um novo fluxo de interpretação conversacional.

‌

## Premissas

‌

* A camada `Concorrentes` representa as farmácias concorrentes disponíveis para consulta, que é uma base interna, atualizada pelos analistas.
* O raio padrão será 300m quando não informado.
* A busca real será feita no MongoDB, não pela IA.
* O Gemini será usado para extração/normalização, não como fonte de verdade.
* O endereço informado poderá ser geocodificado com Google Maps ou serviço equivalente.

‌

## Arquitetura Recomendada

‌

Diferente do contexto atual, devemos alterar a arquitetura para conseguirmos atingir o seguinte fluxo:

Quando o usuário digitar a pergunta:

\-> Front envia pergunta para API;

\-> IA extrai intenção, endereço e raio;

\-> API valida os parâmetros extraídos;

\-> API geocodifica o endereço;

\-> API consulta a camada `Concorrentes` por raio;

\-> API estrutura os resultados; 

\-> IA formata a resposta final em linguagem natural;

\-> Front exibe a resposta ao usuário.

### Separação de Responsabilidades

Levando em consideração possíveis alucinações e melhorar a rastreabilidade, é importante frisar a responsabilidade que cada stack possui, pensando em diminuir as chances de erros nos retornos.

**IA:** Interpreta texto e formata resposta.

**Código:** Valida dados, chama geocoding, consulta MongoDB e monta JSON.

**Banco:** Fornece a verdade sobre os concorrentes no raio de acordo com as bases que temos hoje no Órbita. 

‌

## Alterações Necessárias

‌

No backend:

* Criar um novo endpoint, por exemplo `POST /chat/query`.
* Criar um novo serviço de interpretação de perguntas.
* Criar prompt específico para extrair intenção, endereço e raio.
* Criar schemas Zod para validar a saída da IA.
* Implementar ou ativar geocoding no backend.
* Reaproveitar `searchLayersByRadius()`.
* Estruturar o retorno da lista de concorrentes, com nome, CNPJ e endereço completo.

No frontend:

* Substituir ou complementar o campo atual por um campo conversacional.
* Criar chamada HTTP para o novo endpoint.
* Exibir loading, erro e resposta.
* Definir se a resposta aparece na tela inicial, em modal, ou na tela de pré-análise.
* Possivelmente manter o fluxo antigo como fallback.

‌

## Critérios de Sucesso

‌

Existem alguns pontos que precisam ser estressados e testados antes de qualquer implementação para obtermos a maior taxa possível de sucesso, dentre eles estão:

* A IA identifica corretamente a intenção “buscar farmácias”.
* A IA extrai corretamente o endereço informado.
* A IA extrai corretamente o raio quando ele estiver explícito.
* Quando o raio não for informado, o sistema aplica um padrão, como 300m.
* A API consulta a camada `Concorrentes` sem depender da IA para criar dados.
* A resposta detalhada inclui nome, CNPJ e endereço quando solicitado.
* O sistema não inventa farmácias inexistentes.
* O sistema pede esclarecimento quando a pergunta for ambígua.

‌

## Riscos e Pontos de Atenção

‌

Outro ponto que exige atenção são os riscos que a implementação pode conter, dentre eles estão:

* A IA pode interpretar errado endereço, raio ou intenção.
* O endereço pode ser ambíguo no geocoding.
* A camada `Concorrentes` pode ter dados incompletos.
* O frontend atual foi pensado para busca estruturada, não chat.
* Até o momento, não foi validada em detalhe a documentação operacional da API do Gemini, incluindo limites de uso, custos, latência, políticas de erro e comportamento em produção.
* LGPD ou cuidado com armazenamento de prompts, caso sejam persistidos.
* Custos, limites de uso e rate limit do Gemini e do serviço de geocoding.

‌

## Recomendação Final

‌

A recomendação é evoluir a POC em etapas. Primeiro, validar a interpretação de perguntas em linguagem natural com retorno estruturado. Depois, conectar essa interpretação à busca geoespacial já existente. Por fim, usar a IA para normalizar a resposta final ao usuário. Essa abordagem aproveita a stack atual, reduz riscos de alucinação e permite validar a viabilidade antes de investir em uma experiência conversacional completa.
