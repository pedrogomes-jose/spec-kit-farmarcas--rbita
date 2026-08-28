# Estudo sobre dados de negócios

> Fonte: https://farmarcas.atlassian.net/wiki/spaces/SR/pages/3209625602/Estudo+sobre+dados+de+neg+cios · Última atualização no Confluence: abr. 08, 2025

## 🧭 **Objetivo final**

Exibir no seu sistema, de forma automatizada e confiável, os negócios próximos ao usuário, como:

* Farmácias
* Bancos
* Escolas
* Hospitais
* Supermercados

---

## ✅ **Estratégia Ideal - Etapas**

### **1. Identificação da Fonte de Dados**

| Fonte | Usar para | Tipo | Observações |
| --- | --- | --- | --- |
| **Google Places API** | Dados confiáveis, atualizados e ricos em detalhes | API comercial | Cota gratuita inicial. Requer chave de API. |
| **OpenStreetMap + Overpass API** | Apoio gratuito para regiões com boa cobertura OSM | Open source | Mais técnico, ideal para alimentar banco local |
| **Bases públicas (INEP, CNES, etc)** | Dados nacionais e estáticos (escolas, hospitais) | CSV ou API pública | Atualização periódica manual |

---

### **2. Estrutura técnica do sistema**

#### **Backend:**

* Crie uma camada de **serviço de localização** com:

    * Endpoint `/lugares-proximos?lat=x&lng=y&tipo=pharmacy`
    * Chamadas para Google Places ou OSM conforme a prioridade
    

#### **Frontend:**

* Mapa com marcador de localização do usuário
* Filtros para tipo de estabelecimento
* Marcação dos lugares retornados pela API com ícones customizados

#### **Armazenamento (opcional):**

* Banco relacional com suporte geográfico (ex: **PostGIS**)
* Cache para resultados populares, evitando requisições desnecessárias

---

### **3. Arquitetura resumida**

```
scss
```

CopiarEditar

`Usuário → Frontend (React, Leaflet ou Mapbox)          → Backend (Node/Express, Python/FastAPI etc)             → [Google Places API] (real-time)             → [OpenStreetMap API] (fallback ou offline)             → [Bases públicas] (importações periódicas) `

---

### **4. Prioridade de uso das fontes**

```
mermaid
```

CopiarEditar

`graph TD A[Usuário faz busca] --> B{Existe cache recente?} B -- Sim --> C[Retorna dados do cache] B -- Não --> D{Usar Google Places?} D -- Sim --> E[Consulta Google Places] D -- Não --> F[Consulta OSM Overpass] E --> G[Salva cache] --> H[Retorna ao usuário] F --> G `

---

### **5. Segurança & boas práticas**

* Use chave de API segura no backend
* Limite de requisições por IP/session
* Crie alertas para falhas nas chamadas às APIs
* Implemente logs de chamadas externas

---

## 💡 Extras úteis

* Use o **Mapbox** se quiser fugir do Google, mantendo alto nível de customização
* Utilize **geohash** ou **quadkeys** para indexar áreas geográficas no banco
* Faça pré-caching de locais mais populares (ex: centros urbanos)

---

Se quiser, posso:

* Montar a estrutura do backend (em Node, Python, etc)
* Gerar exemplos reais de chamadas para Google Places ou OSM
* Criar wireframes da interface com filtro de categorias

---

### ✅ **1. Google Places API (Google Maps Platform)**

A mais conhecida e completa.

**O que entrega:**

* Nome, tipo de lugar (ex: "farmácia"), localização (lat/lng), endereço, telefone, horário de funcionamento, avaliações, etc.

**Como usar:**

* Você faz uma requisição para `https://maps.googleapis.com/maps/api/place/nearbysearch/json` com parâmetros como:

    * localização (lat/lng)
    * raio de busca
    * tipo de lugar (`type=pharmacy`, `type=school`, `type=bank`, etc.)
    

**Exemplo:**

```
bash
```

CopiarEditar

`https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-23.5629,-46.6544&radius=1000&type=pharmacy&key=SUA_API_KEY `

**Prós:**

* Dados atualizados, confiáveis e ricos
* Facilidade de uso
* Documentação excelente

**Contras:**

* Pago após um certo volume (existe uma cota gratuita mensal)
* Limitações de uso comercial dependendo do plano

---

### 🗺️ **2. OpenStreetMap (OSM) + Overpass API**

Fonte **gratuita e open-source** de dados geográficos colaborativos.

**O que entrega:**

* Estabelecimentos por tipo, nome, localização, tags descritivas (ex: `amenity=pharmacy`, `amenity=school`)

**Como usar:**  
 Você pode usar a [Overpass API](https://overpass-turbo.eu/) para fazer consultas como:

```
xml
```

CopiarEditar

`[out:json]; node   ["amenity"="pharmacy"]   (around:1000,-23.5629,-46.6544); out; `

**Prós:**

* Gratuito
* Pode armazenar os dados localmente
* Sem limite de uso (com bom uso de cache)

**Contras:**

* Dados nem sempre tão atualizados quanto o Google
* Nem todas as regiões são bem mapeadas
* Mais técnico de usar

---

### 🧠 **3. APIs específicas por segmento (Brasil)**

* **INEP (para escolas)**: [https://dadosabertos.inep.gov.br/](https://dadosabertos.inep.gov.br/)
* **CNES (Cadastro Nacional de Estabelecimentos de Saúde)**: [https://cnes.datasus.gov.br/](https://cnes.datasus.gov.br/)
* **Bancos**: Algumas instituições têm APIs públicas ou podem ser cruzadas com CNPJs em bases como Receita Federal.

---

### 🧪 **4. Dados por scraping (última opção)**

Você também pode usar técnicas de **web scraping** (ex: coletar de sites como Telelistas, Apontador, Guias locais), **mas com muito cuidado legal**:

* Baixa confiabilidade
* Termos de uso podem proibir
* Baixa escalabilidade

---

### 🔁 Estratégia ideal para um sistema

Se estiver construindo algo **escalável e confiável**, o melhor é:

* Usar **Google Places API** ou **Mapbox Search API** para dados em tempo real
* Complementar com **OpenStreetMap** (sobretudo se quiser manter seu próprio banco)
* Usar **bases públicas específicas** quando forem relevantes

‌

## 🗂️ **Fontes alternativas para as bases**

### 1. **Farmácias**

* **Fonte sugerida**: Google Places API (`type=pharmacy`)
* **Alternativa gratuita**: OpenStreetMap com Overpass API
* **Exemplo de consulta OSM**:

    ```
    xml
    ```

    CopiarEditar



    `node["amenity"="pharmacy"](area:3600062421); `



---

### 2. **Hospitais**

* **Fonte pública (Brasil)**: CNES - Cadastro Nacional de Estabelecimentos de Saúde

    * [https://dados.gov.br/dataset/cnes](https://dados.gov.br/dataset/cnes)
    * Atualizações regulares do Ministério da Saúde
    
* **Alternativa**: Google Places (`type=hospital`) ou OSM (`amenity=hospital`)

---

### 3. **Lojas Bifarma / Farmarcas**

* **Fonte alternativa**:  
   Essas são **marcas específicas**, então:

    * Usar **Google Places API com** `name=Bifarma` **ou** `name=Farmarcas`
    * Alternativa: web scraping dos sites das redes (com cautela e permissão)
    

---

### 4. **Lotéricas**

* **Fonte sugerida**:

    * [Correios (Brasil)](https://www.correios.com.br) → possui a listagem de agências e lotéricas.
    * Alternativa via Google Places (`type=finance` + filtro por nome com "lotérica")
    

---

### 5. **Mercados**

* **Google Places API**: `type=supermarket`
* **OpenStreetMap**: `shop=supermarket`

---

### 6. **Óticas**

* **Google Places API**: busca por `name=Ótica` ou `type=store` com `keyword=óculos`
* **OSM**: `shop=optician`

---

### 7. **Perfumarias**

* **Google Places API**: `keyword=perfumaria` ou `type=store` com filtro de nome
* **OSM**: `shop=perfumery`
