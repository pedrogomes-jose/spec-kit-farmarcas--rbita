# Órbita 2025

> Fonte: https://farmarcas.atlassian.net/wiki/spaces/SR/pages/3021340781/rbita+2025 · Última atualização no Confluence: jun. 12, 2025
> Nota: esta página continha imagens (prints de tela) no Confluence original que não puderam ser migradas automaticamente. Consulte a fonte acima para o conteúdo visual completo.

## Tela inicial

### Bricks

Nesse contexto, o termo **"brick"** está ligado a **análise de perfil de consumo em pontos físicos**, e é uma adaptação mais informal ou específica do mercado para se referir a **"unidades geográficas ou comerciais" usadas para estudo de comportamento do consumidor**.

### O que significa "Brick" nesse contexto?

Um **"brick"** é uma **área delimitada (como um quarteirão, bairro, zona de cobertura ou mesmo uma loja física específica)** usada como **unidade de análise** para entender o comportamento de compra dos consumidores que frequentam ou residem naquela região.

### Para que serve?

Empresas usam **bricks** para:

* Mapear o perfil de consumo por região;
* Identificar **hábitos de compra** locais (frequência, ticket médio, preferências);
* Definir **ações de marketing ou sortimento** específicas para cada área;
* Planejar expansão de lojas ou distribuição de produtos com base em **potencial de consumo local**.

### Exemplo prático:

Uma rede de supermercados pode dividir a cidade em vários **"bricks"** e analisar que:

* O brick do bairro X compra mais produtos premium e saudáveis.
* O brick do bairro Y consome mais promoções e marcas econômicas.

Com isso, ela adapta o **mix de produtos** em cada loja conforme o perfil de cada **brick**.

---

### Bricks - Market Share

É a **participação de uma empresa, marca ou loja nas vendas totais realizadas dentro de uma determinada área geográfica (o "brick")**.

### Em outras palavras:

Se você divide uma cidade ou região em "bricks" (áreas específicas), o **market share de um brick** indica **quanto uma empresa vende naquele pedaço, em relação ao total vendido ali**.

### Exemplo prático:

Imagine que você tem um brick chamado **Brick A**, que representa um bairro.

* As vendas totais do Brick A no mês foram R$ 1.000.000.
* A empresa **Farmácia Boa Saúde** vendeu R$ 250.000 nesse mesmo brick.

**Market share da Farmácia Boa Saúde no Brick A**: 250.000 / 1.000.000 × 100 = 25%

Ou seja, ela detém **25% do market share nesse brick**.

### Por que isso importa?

Saber o market share **por brick** ajuda a:

* Entender onde a marca é forte ou fraca;
* Ajustar ações locais de marketing, precificação ou sortimento;
* Descobrir **oportunidades de crescimento regional**;
* Comparar performance de diferentes lojas ou territórios;
* Otimizar expansão (por exemplo, abrir uma loja onde o market share ainda é baixo, mas o potencial é alto).

* Projeto que gerencia as informações: [https://github.com/farmarcas/api-orbita-nodejs](https://github.com/farmarcas/api-orbita-nodejs)
* Rota que devolve as informações de bases de dados disponíveis, inclusive do Brick: `https://orbita.api.dev.radar.farmarcas.com.br/sources`
* Base de dados: MongoDB → `orbita`
* Collection: `sources`

Query banco de dados:

```
[
  {
    $match:
      /**
       * query: The query in MQL.
       */
      {
        status: {
          $in: [0, 1, 2, 3]
        }
      }
  },
  {
    $lookup: {
      from: "grouping",
      localField: "_id",
      foreignField: "source",
      as: "grouping"
    }
  },
  {
    $lookup: {
      from: "graphic",
      localField: "_id",
      foreignField: "source",
      as: "graphic"
    }
  },
  {
    $lookup: {
      from: "update",
      localField: "name",
      foreignField: "source",
      as: "updates"
    }
  },
  {
    $project: {
      _id: 1,
      name: 1,
      structure: 1,
      status: 1,
      references: 1,
      geometryType: 1,
      fileType: 1,
      type: 1,
      error: 1,
      creationDate: 1,
      updateDate: 1,
      groupedBy: {
        $arrayElemAt: ["$grouping.grouping", 0]
      },
      graphicSetup: {
        $arrayElemAt: ["$graphic.graphic", 0]
      },
      update: {
        $arrayElemAt: ["$updates", 0]
      },
      geometryFile: 1,
      customMarker: 1
    }
  }
]
```

#### Resumo:

* Busca `sources` com os status: `[STATUS.Sucess, STATUS.Processing, STATUS.Error, STATUS.OnHolding]`
* Realiza junção com as informações de agrupamento, gráfico e atualização
* A data de atualização do item apresentado no front atual é referente ao valor que está em `sources`

#### Conclusão

De acordo com a análise, hoje é atualizado as collections porém não é inserido na collection `update`, é necessário que seja incluído a informação também na collection `update` com o seguinte modelo:

```
{
  "_id": {
    "$oid": "684b554f3f14e3e583ab8901"
  },
  "source": "MAT Atual - Brick Bandeira",
  "updateDate": {
    "$numberLong": "1709728577723"
  }
}
```

Com isso será retornado o atributo `update`, que sim representa a data de atualização de fato.

O que precisamos:

* Ao atualizar os dados, inserir também a informação na collection `update`
* O front passar a olhar esse atributo, pois ele se trata da atualização do dado e não do `source`
  * Caso não exista essa informação considera o atributo anterior

---

### Marcadores

* Os marcadores devem refletir marcadores no mapa
* Os marcadores tem que respeitar o raio? Ou seja, trazer só os resultados dentro do mapa ou fora também?

---

### Tipo de Mapa

* Temos basicamente três tipos de mapas e a função de troca entre eles

### Bancos

* Ao adicionar a camada de bancos os pins devem ser marcados no mapa
* Ao clicar em um marcador deve abrir o modal do lado direito da tela com informações daquele local

### Barreiras Geográficas

* Ao adicionar a camada de barreiras geográficas os pins devem ser marcados no mapa
* Ao clicar em um marcador deve abrir o modal do lado direito da tela com informações daquele local

### Clínicas Oftalmológicas

* Ao adicionar a camada os pins devem ser marcados no mapa
* Ao clicar em um marcador deve abrir o modal do lado direito da tela com informações daquele local

### Concorrentes

* Ao adicionar a camada os pins devem ser marcados no mapa
* Ao clicar em um marcador deve abrir o modal do lado direito da tela com informações daquele local

### Concorrentes 2023

* Ao adicionar a camada os pins devem ser marcados no mapa
* Ao clicar em um marcador deve abrir o modal do lado direito da tela com informações daquele local

### Farmácias

* Ao adicionar a camada os pins devem ser marcados no mapa
* Ao clicar em um marcador deve abrir o modal do lado direito da tela com informações daquele local

### Lojas Bifarma

* Ao adicionar a camada os pins devem ser marcados no mapa
* Ao clicar em um marcador deve abrir o modal do lado direito da tela com informações daquele local

### Lojas Farmarcas

* Ao adicionar a camada os pins devem ser marcados no mapa
* Ao clicar em um marcador deve abrir o modal do lado direito da tela com informações daquele local

### Lotéricas

* Ao adicionar a camada os pins devem ser marcados no mapa
* Ao clicar em um marcador deve abrir o modal do lado direito da tela com informações daquele local

### Mercado

* Ao adicionar a camada os pins devem ser marcados no mapa
* Ao clicar em um marcador deve abrir o modal do lado direito da tela com informações daquele local

### Óticas

* Ao adicionar a camada os pins devem ser marcados no mapa
* Ao clicar em um marcador deve abrir o modal do lado direito da tela com informações daquele local

### Perfumarias

* Ao adicionar a camada os pins devem ser marcados no mapa
* Ao clicar em um marcador deve abrir o modal do lado direito da tela com informações daquele local

### Indicadores > Análises de ponto

Análises de pontos, contratos fechados e base de dados são exibidos como painéis de indicadores dentro do Órbita.

### Base de dados

* Ao clicar em adicionar base é aberto um modal para escolher o tipo de arquivo
