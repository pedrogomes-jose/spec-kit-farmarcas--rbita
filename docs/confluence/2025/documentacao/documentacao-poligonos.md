# Documentação - Polígonos

> Fonte: https://farmarcas.atlassian.net/wiki/spaces/SR/pages/3214999564/Documenta+o+-+Pol+gonos · Última atualização no Confluence: abr. 11, 2025

### O que são **polígonos** em sistemas de mapas?

**Polígonos** são formas **fechadas** desenhadas sobre o mapa, usando **vários pontos conectados por linhas**. Eles servem para **delimitar uma área específica**, como:

* Um bairro
* Um terreno
* Uma zona de cobertura
* Uma área de risco
* Um território de entrega
* Uma unidade de negócio, franquia, etc.

---

### 💡 Exemplos práticos:

* Quando um app mostra a **área de cobertura de um serviço**, como o iFood ou Uber Eats → ele está usando **polígonos**.
* Em uma plataforma imobiliária, para destacar o **terreno** ou área de um imóvel.
* Em sistemas corporativos, para mostrar os **pontos de interesse**, como áreas de expansão ou locais estratégicos para abrir novas unidades.

---

### 🧱 Como é construído?

* Um polígono é definido por uma **sequência de coordenadas geográficas** (latitude e longitude).
* O sistema desenha **linhas entre os pontos**, e a primeira coordenada se conecta à última para **fechar a forma**.

Exemplo básico (em código, só pra visualização):

```
json
```

CopiarEditar

`[   [ -46.6333, -23.5505 ],   [ -46.6335, -23.5502 ],   [ -46.6331, -23.5499 ],   [ -46.6333, -23.5505 ]  // Fecha o polígono ] `

---

### 📍 Para que serve em um sistema como o da imagem que você enviou?

No contexto de análise de pontos ou expansão:

* O sistema pode usar **polígonos** para representar **áreas de estudo**, como regiões onde novos pontos estão sendo mapeados.
* Ajuda a entender **se há sobreposição entre áreas**, **espaçamento entre lojas**, **concorrência em uma zona**, etc.
