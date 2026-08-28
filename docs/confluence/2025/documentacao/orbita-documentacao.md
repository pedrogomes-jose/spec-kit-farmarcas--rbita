# Órbita - Documentação

> Fonte: https://farmarcas.atlassian.net/wiki/spaces/SR/pages/3213131802/rbita+-+Documenta+o · Última atualização no Confluence: abr. 10, 2025

### **1. Introdução**

#### 1.1 Objetivo do Documento

Esta documentação tem como objetivo apresentar de forma clara e detalhada o funcionamento do sistema **Órbita**, incluindo seu propósito, arquitetura, funcionalidades, regras de negócio e serviços integrados, com foco em garantir qualidade e alinhamento para o desenvolvimento, testes e evolução do produto.

#### 1.2 Escopo

O sistema **Órbita** é uma plataforma Geoespacial utilizada pelos analistas da **Farmarcas** para realizar análises de localização com o objetivo de abertura de novas lojas. Ele centraliza dados, análises, mapas e indicadores que antes eram tratados manualmente em diversas planilhas e ferramentas.

#### 1.3 Público-Alvo

* Equipe de Qualidade de Software;
* Desenvolvedores e Arquitetos;
* Analistas de Negócio;
* Equipe de Expansão;
* Gestores de Produto.

---

### **2. Visão Geral do Produto**

#### 2.1 Por que o Órbita existe?

Antes da criação do Órbita, os analistas utilizavam diversas ferramentas de mercado e planilhas para centralizar dados para análise de novos pontos. O processo era manual e sujeito a erros. O Órbita surgiu para centralizar, otimizar e padronizar este processo, dentro da plataforma Radar.

#### 2.2 Tecnologias Utilizadas

* **Front-end**: Angular v12 + [http://deck.gl](http://deck.gl)  + Google Maps
* **Back-end**:

    * Node.js (api-orbita)
    * .NETCore (api-expansion)
    
* **Infraestrutura & Serviços**:

    * AWS S3, Lambda, ElastiCache
    * MongoDB Atlas
    * Sentry
    * Google Maps API
    

---

### **3. Funcionalidades Principais**

#### 3.1 Mapa

* Visualização Geoespacial com diferentes tipologias de mapa
* Ferramentas: Centralizar, Régua, Raio da Análise, Tela Cheia
* Camadas de dados e marcadores
* Modais de edição de dados, agrupamentos e gráficos

#### 3.2 Análise de Pontos

* Criação de análise com ou sem ponto pré-buscado
* Possibilidade de salvar como análise de ponto ou território
* Retorno automático para análise anterior após salvar

#### 3.3 Indicadores

* Big Numbers (YTD)
* Taxa de Conversão (por mês)
* Pré-Contratos fechados
* Influência por UF

#### 3.4 Cidades Disponíveis

* Baseada em planilhas atualizadas pela equipe de Expansão

#### 3.5 Histórico de Análises e Contratos

* Visualização, edição, filtros, busca e criação de novas análises/contratos

#### 3.6 Base de Dados

* Upload e gestão de fontes de dados (Excel, Shape)
* Edição e exclusão de dados
* Configuração de agrupamentos e gráficos

---

### **4. Regras de Negócio**

| Funcionalidade | Regra de Negócio |
| --- | --- |
| Salvar Análise | Deve conter todos os campos obrigatórios preenchidos no modal |
| Agrupamentos | É permitido editar nome, valor, cor e excluir agrupamentos |
| Camadas | Só podem ser removidas ou editadas com ações específicas do menu |
| Indicadores | Big Numbers são fixos (YTD), Taxa de Conversão segue mês selecionado |
| Bases de Dados | Só podem ser removidas se não estiverem vinculadas a uma análise |
| Retorno à tela anterior | Após salvar nova análise, o usuário volta ao mapa com todas as camadas mantidas |

---

### **5. Casos de Uso (Simplificados)**

#### Caso de Uso 1: Criar uma nova análise no mapa

1. Usuário acessa o Mapa
2. Busca um endereço ou ponto específico
3. Aplica camadas de dados e configurações
4. Clica em "Salvar Análise"
5. Escolhe entre ponto ou território
6. Preenche o modal e confirma
7. Análise é salva e o usuário permanece no mesmo estado visual do mapa

#### Caso de Uso 2: Adicionar nova base de dados

1. Usuário acessa "Base de Dados"
2. Seleciona "Adicionar base"
3. Envia arquivo .xlsx ou .shp
4. Sistema processa e armazena no MongoDB via AWS Lambda
5. Base fica disponível para uso em análises

---

### **6. Qualidade e Testes**

#### 6.1 Estratégia de Testes

* Testes Funcionais (UI e API)
* Testes de Integração entre aplicações
* Testes de Performance (tempo de carregamento de camadas/mapa)
* Testes de Validação de Dados (bases de dados e cálculos)

#### 6.2 Cobertura Crítica

* Criação e edição de análises
* Upload e manipulação de bases de dados
* Configuração de gráficos e agrupamentos
* Indicadores (Big Numbers, Taxa de Conversão)

#### 6.3 Critérios de Aceitação

* Análises devem ser persistidas corretamente no MongoDB
* Visualizações devem manter o estado do mapa após ações
* Indicadores devem refletir dados corretos conforme regras de negócio

---

### **7. Arquitetura Técnica**

#### 7.1 Estrutura de Aplicações

* **webapp-orbita** (Angular): Interface de usuário
* **api-expansion** (.NET): Gestão de análises e contratos
* **api-orbita** (Node.js): Gestão de dados geoespaciais
* **jobs-orbita** (Node.js): Funções assíncronas (processamento de arquivos, geração de dados)

#### 7.2 Dependências

* **MongoDB Atlas**: Armazena dados de análise, agrupamentos e gráficos
* **AWS Lambda**: Processamento de arquivos e dados geoespaciais
* **AWS S3**: Armazenamento de arquivos
* **ElastiCache**: Cache para consultas com geometria definida
* **Google Maps API**: Geolocalização e visualização de mapa

---

### **8. Considerações Finais**

O sistema Órbita representa uma evolução no processo de análise geoespacial da Farmarcas. Sua estrutura modular, baseada em serviços modernos e escaláveis, permite que o time de Expansão atue de forma mais eficiente e estratégica. Esta documentação deverá ser atualizada continuamente conforme novas funcionalidades e regras forem implementadas.

 

---

---

---

### _**Futuras melhorias no documento:**_

 

### 🔍 **Seção 3 – Funcionalidades**

**O que você já tem:** Bem descrito! Explicou Mapa, Indicadores, Histórico, Contratos, Bases, etc.  
**O que pode complementar:**

* Exemplos práticos de uso (ex: "Como um analista usaria a funcionalidade X no dia a dia?")
* Campos obrigatórios nos modais (quais são, o que significam)
* Comportamento esperado ao interagir com múltiplas camadas ou bases ao mesmo tempo
* Tipos de arquivos aceitos nas bases (.xlsx, .shp) e limitações

---

### 📜 **Seção 4 – Regras de Negócio**

**O que você já tem:** Algumas regras bem explicadas.  
**O que pode complementar:**

* Limitações (ex: "uma análise de ponto não pode conter mais de X camadas")
* Cálculos importantes (ex: como é calculada a taxa de conversão? média, soma, etc.)
* Permissões por perfil de usuário (se houver mais de um tipo de acesso)
* Validações de dados no momento do upload de bases (ex: campos obrigatórios nas planilhas)

---

### 📊 **Seção 5 – Casos de Uso**

**O que você já tem:** Já há um bom início com 2 fluxos.  
**O que pode complementar:**

* Casos de erro (ex: "O que acontece se uma base for inválida?")
* Fluxos alternativos (ex: editar uma análise existente, deletar base)
* Fluxo de visualização de indicadores com filtros aplicados
* Como funciona a navegação entre páginas

---

### 🧪 **Seção 6 – Qualidade e Testes**

**O que você já tem:** Estratégias de testes e cobertura bem alinhadas  
**O que pode complementar:**

* Regras para dados mockados em ambiente de testes (se existir)
* Como versionar testes (ex: quando atualizar ou revisar testes em novas versões)
* Indicadores de qualidade (ex: tempo médio de resposta das APIs, taxa de falhas no upload)

---

### 🛠️ **Seção 7 – Arquitetura Técnica**

**O que você já tem:** Desenho muito bom das integrações e serviços.  
**O que pode complementar:**

* Nomes dos buckets no S3 (se aplicável)
* Exemplo de payload de análise no MongoDB (estrutura básica dos dados)
* Como funciona o versionamento das análises salvas
* Limites de uso do Google Maps (ex: quota diária, fallback)
