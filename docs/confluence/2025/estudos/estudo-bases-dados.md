# Estudo sobre bases de dados

> Fonte: https://farmarcas.atlassian.net/wiki/spaces/SR/pages/3209822227/Estudo+sobre+bases+de+dados · Última atualização no Confluence: abr. 16, 2025

### 🎯 Objetivos:

* Substituir o uso de planilhas e arquivos estáticos por uma fonte confiável e atualizada.
* Melhorar a experiência do usuário com dados contextualizados diretamente no mapa.
* Reduzir erros manuais e tempo gasto com manutenção de bases de dados locais.
* Tornar o sistema mais inteligente e preparado para futuras análises e cruzamento de dados públicos (ex: densidade populacional por área).

 

A integração possibilitará enriquecer a visualização do mapa com dados públicos dinâmicos, permitindo que usuários consultem informações contextuais ao interagir com os pins do mapa **(ex: ao clicar em um município, mostrar sua população atual, estado ao qual pertence, entre outros).**

Precisamos implementar a integração entre o **Órbita** e as **APIs públicas do IBGE**, com foco em obter informações oficiais, atualizadas e confiáveis sobre **estados**, **municípios**, **população** e, futuramente, **dados territoriais e socioeconômicos**.

‌

### <custom data-type="emoji" data-id="id-0">:moneybag:</custom> Benefícios da integração com a API do IBGE:

| Benefício | Detalhamento |
| --- | --- |
| **Atualização automática** | Os dados populacionais e de municípios são atualizados diretamente da fonte oficial, reduzindo riscos de desatualização. |
| **Padronização nacional** | Utiliza códigos IBGE para identificação única de localidades, facilitando integrações com outros sistemas governamentais. |
| **Redução de esforço manual** | Elimina a necessidade de atualizar planilhas e arquivos CSV manualmente a cada nova versão. |
| **Flexibilidade para expansão** | Permite, futuramente, incluir dados socioeconômicos, malha geográfica e outras informações do Censo e PNAD. |
| **Confiabilidade da fonte** | Dados provenientes diretamente do Instituto Brasileiro de Geografia e Estatística, autoridade máxima no assunto no Brasil. |

### 🧩 Escopo técnico:

As seguintes funcionalidades e estudos estão contemplados neste épico:

* Obtenção dinâmica da lista de **estados e municípios**.
* Consulta da **população atual** por município.
* Estudo sobre **geodados** (malha territorial em GeoJSON ou Shapefile).
* Verificação da **compatibilidade com os pins e cards** do mapa Órbita.
* Estruturação de **exemplos e documentação técnica** para uso contínuo no sistema.
* Planejamento para armazenar dados localmente quando necessário (ex: cache).

 

### 🔍 Referências técnicas:

* Documentação da API de localidades IBGE: [https://servicodados.ibge.gov.br/api/docs/localidades](https://servicodados.ibge.gov.br/api/docs/localidades)
* API de projeção populacional: [https://servicodados.ibge.gov.br/api/docs/projecoes](https://servicodados.ibge.gov.br/api/docs/projecoes)
* Portal de geociências e mapas do IBGE: [https://www.ibge.gov.br/geociencias/downloads-geociencias.html](https://www.ibge.gov.br/geociencias/downloads-geociencias.html)

‌

Com a utilização dos novos mapas vai ser possível eliminar a necessidade dessas bases manuais?

Sim, **com a utilização das APIs do IBGE é plenamente possível eliminar a necessidade de manter bases manuais** — principalmente se o objetivo for consultar informações como **nomes de estados, municípios, códigos IBGE, projeções populacionais, e futuramente dados territoriais**.

### ✅ O que você **pode automatizar e eliminar** com as APIs do IBGE:

| Tipo de dado | Elimina planilhas manuais? | Observações |
| --- | --- | --- |
| **Lista de estados e municípios** | ✅ Sim | Endpoints fornecem a hierarquia completa, com nomes, siglas e códigos oficiais. |
| **População por município** | ✅ Sim | Dados atualizados automaticamente pelo IBGE com projeções anuais. |
| **Códigos IBGE** | ✅ Sim | Fundamental para padronização e integrações. Evita erros humanos. |
| **Malha territorial (mapas)** | ⚠️ Parcialmente | Shapefiles e GeoJSONs são disponibilizados, mas precisam ser baixados periodicamente (não via API REST tradicional ainda). |
| **Dados socioeconômicos (renda, escolaridade)** | ⚠️ Em parte | Alguns estão disponíveis por API, mas muitos ainda exigem acesso via CSV ou portais específicos do IBGE. |

### 1. **Dados Geográficos e Demográficos**

* **Bairros, Distritos e Subdistritos**:

    * **Brasil Aberto**: Oferece uma API para obter a lista de bairros de uma cidade específica. ​[Dados Abertos Saúde+2Brasil Aberto+2Brasil Aberto+2](https://brasilaberto.com/docs/v1/districts?utm_source=chatgpt.com)
    * **IBGE**: Disponibiliza APIs que fornecem dados geográficos detalhados, incluindo distritos e subdistritos. ​
    
* **População_br, População UF, População MM 2023**:

    * **IBGE**: Oferece estimativas populacionais anuais para municípios e unidades federativas por meio de suas APIs. ​[Serviços e Informações do Brasil+3IBGE+3SciELO Brasil+3](https://www.ibge.gov.br/estatisticas/sociais/populacao.html?utm_source=chatgpt.com)
    
* **Densidade Demográfica UF, Densidade Demográfica MM**:

    * **IBGE**: Fornece dados sobre densidade demográfica através de suas APIs de dados agregados. ​[Agência de Notícias - IBGE+10Tecnospeed Blog+10Vision One+10](https://blog.tecnospeed.com.br/api-de-bancos-brasileiros/?utm_source=chatgpt.com)
    
* **Municípios, Estados**:

    * **Back4app**: Disponibiliza uma API com informações completas sobre todos os estados e cidades do Brasil. ​[Back4app™](https://www.back4app.com/database/back4app/api-estados-cidades-brasil?utm_source=chatgpt.com)
    

### 2. **Dados Econômicos e Sociais**

* **PIB 2021, Movimentação Econômica**:

    * **IpeaData**: Oferece uma API para consulta de dados econômicos, incluindo PIB e movimentação econômica. ​
    
* **Índice Educação 2021**:

    * **IpeaData**: Disponibiliza dados relacionados à educação por meio de sua API. ​
    
* **Firjan**:

    * **IpeaData**: Fornece acesso a indicadores como o Índice Firjan de Desenvolvimento Municipal. ​
    

### 3. **Estabelecimentos de Saúde e Serviços**

* **Hospitais, Clínicas Oftalmológicas, Farmácias, Óticas, Perfumarias**:

    * **DEMAS - API de Dados Abertos**: Fornece informações sobre estabelecimentos de saúde, incluindo hospitais e clínicas. ​[IBGE Servicodados+12Olhar Certo+12Vision One+12](https://olharcerto.com.br/?utm_source=chatgpt.com)
    * **Busca Saúde (Prefeitura de São Paulo)**: Utiliza APIs de geolocalização para facilitar a busca por unidades de saúde próximas. ​[Geoambiente](https://www.geoambiente.com.br/case-de-sucesso-busca-saude/?utm_source=chatgpt.com)
    

### 4. **Setores Financeiro e Comercial**

* **Bancos**:

    * **Banco do Brasil**: Oferece uma API que permite acesso a funcionalidades como consulta de saldo e histórico de transações. ​[Tecnospeed Blog](https://blog.tecnospeed.com.br/api-de-bancos-brasileiros/?utm_source=chatgpt.com)
    
* **Empresas por Segmento de Atuação, Empresas Totais**:

    * **Fintz**: Disponibiliza uma API para acesso a dados de empresas, fundos, títulos e ações. ​[Fintz: API Market Data Brasil+1Agência de Notícias - IBGE+1](https://fintz.com.br/?utm_source=chatgpt.com)
    

### 5. **Dados Censitários e de Consumo**

* **Setor Censitário, Potencial de Consumo - Setor Censitário**:

    * **IBGE**: Fornece dados detalhados por setor censitário através de suas APIs. ​
    
* **Domicílios Segundo Classe Econômica, Renda Média**:

    * **IBGE**: Oferece informações sobre domicílios e renda média por meio de suas APIs de dados agregados. ​
    

### 6. **Dados de Saúde**

* **Pirâmide Etária, População por Gênero**:

    * **IBGE**: Disponibiliza dados demográficos detalhados, incluindo distribuição por idade e gênero. ​[IBGE](https://www.ibge.gov.br/estatisticas/sociais/populacao.html?utm_source=chatgpt.com)
    

### 7. **Infraestrutura e Transporte**

* **Terminais Rodoviários**:

    * **APIs Governamentais**: O catálogo de APIs do governo pode conter informações sobre infraestrutura de transporte. ​[Serviços e Informações do Brasil](https://www.gov.br/conecta/catalogo/?utm_source=chatgpt.com)
    

### 8. **Dados de Mercado Farmacêutico**

* **Bricks IQVIA, MAT Atual - Brick Bandeira, MAT Atual - Brick Grupo, MAT Atual - Brick Market Share, MAT Atual - Qtd PDVs**:

    * **IQVIA PharmaReport**: Fornece dashboards com dados de vendas, crescimento e participação de mercado no nível de "brick" e sub-"brick". ​[IPEA Data+10IQVIA+10Vision One+10](https://www.iqvia.com/locations/belgium/solutions/business-intelligence-and-data-science/pharmareport?utm_source=chatgpt.com)
    

### Observações Gerais:

* **Atualização Automática**: A utilização dessas APIs permite que os dados sejam atualizados automaticamente, reduzindo a necessidade de manutenção manual e garantindo informações mais precisas e atuais.​
* **Limitações e Acesso**: Algumas APIs podem requerer registro, autenticação ou estar sujeitas a planos pagos, especialmente aquelas que fornecem dados mais específicos ou sensíveis.​
* **Integração**: A integração dessas APIs em seus sistemas dependerá das especificações técnicas de cada uma, sendo importante consultar a documentação oficial para implementação adequada.

---

### **Tarefa 1 – Estudo geral da API do IBGE**

🧑‍💻 _Responsável:_ Dev backend ou fullstack  
**O que será feito:**

* Acessar a documentação oficial da API do IBGE
* Entender os tipos de dados disponíveis (ex: regiões, estados, cidades, população).
* Identificar quais endpoints são mais relevantes para uso no mapa.

📌 **Explicação simples:**  
Vamos entender **quais dados o IBGE oferece** e como conseguimos buscá-los online, direto do sistema. Isso inclui nome de cidades, número de habitantes e mais.

💸 **Custos:**

> A API do IBGE é **gratuita** e pública. Não há cobrança por uso, mas é importante tratar bem o volume de requisições.

---

### **Tarefa 2 – Levantamento de dados por estado e município**

🧑‍💻 _Responsável:_ Dev backend  
**O que será feito:**

* Testar o endpoint de **localidades**:  
  `https://servicodados.ibge.gov.br/api/v1/localidades/estados`
* Para cada estado, obter lista de **municípios**, com nome, sigla e código IBGE.
* Armazenar um exemplo para referência (ex: SP com seus municípios).

📌 **Explicação simples:**  
Essa tarefa nos permite montar uma **lista navegável de estados e cidades**, para que o mapa mostre dados por região.

---

### **Tarefa 3 – Análise dos dados populacionais disponíveis**

🧑‍💻 _Responsável:_ Dev backend / analista de dados  
**O que será feito:**

* Estudar a API de **indicadores populacionais**:  
  `https://servicodados.ibge.gov.br/api/v1/projecoes/populacao/{id_municipio}`
* Verificar os dados retornados: população estimada, data, projeções futuras.

📌 **Explicação simples:**  
Aqui vamos buscar **quantas pessoas vivem em uma cidade**, dados úteis para criar filtros e análises no mapa do Órbita.

---

### **Tarefa 4 – Explorar informações geográficas e territoriais**

🧑‍💻 _Responsável:_ Dev frontend + backend  
**O que será feito:**

* Verificar se o IBGE fornece coordenadas geográficas ou dados espaciais úteis.
* Avaliar uso complementar com IBGE Geoserviços (shapefiles, limites territoriais).

📌 **Explicação simples:**  
Vamos ver se conseguimos **desenhar o contorno de bairros ou cidades no mapa**, com base nas áreas geográficas fornecidas pelo IBGE.

---

### **Tarefa 5 – Analisar compatibilidade com o mapa do Órbita**

🧑‍💻 _Responsável:_ Dev frontend  
**O que será feito:**

* Avaliar como integrar as informações do IBGE nos **pins ou regiões clicadas no mapa**.
* Pensar em uma estrutura que relacione **latitude/longitude com código IBGE**.

📌 **Explicação simples:**  
Queremos garantir que, ao clicar em um local no mapa, o sistema entenda **de qual cidade ou bairro se trata**, para buscar os dados certos.

---

### **Tarefa 6 – Montar documentação com exemplos de dados e respostas da API**

🧑‍💻 _Responsável:_ Dev backend  
**O que será feito:**

* Criar uma collection no Postman (ou outro) com exemplos de uso.
* Documentar os endpoints utilizados e a estrutura dos dados.
* Incluir exemplos em JSON de estados, cidades e população.

📌 **Explicação simples:**  
Depois da análise, vamos deixar tudo bem documentado para os devs conseguirem **usar os dados do IBGE no sistema** com facilidade.
