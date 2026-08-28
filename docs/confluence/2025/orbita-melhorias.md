# Órbita - Melhorias

> Fonte: https://farmarcas.atlassian.net/wiki/spaces/SR/pages/3025567781/rbita+-+Melhorias · Última atualização no Confluence: jan. 14, 2025
> Nota: esta página continha imagens no Confluence original que não puderam ser migradas automaticamente. Consulte a fonte acima para o conteúdo visual completo.

Mapeando algumas melhorias que podem ser feitas na tela de indicadores - Analise de ponto

‌

Melhorias levantadas na dinâmica - Mais votadas

1. Ter a data das imagens do Street View no Órbita - 4 votos.
2. Salvar a análise ser ter que entrar no mapa - 3 votos.
3. Conseguir parar de usar o Sheets como dash - 3 votos.
4. Deixar todas as camadas á mostra e ai depois só seleciona - 3 votos. 
5. Conseguir deixar de usar o dash de contratos no sheets - 3 votos.
6. Ficha cadastral por link que envie as informações para o Óbita - 2 pontos.
7. Velocidade de carregamento e loading - 2 pontos.

‌

**Pequenos ajustes de grande valor:**

* Bloquear campo de lead em (+nova análise) para letras, afim de aceitar apenas números;
* Aviso de análise existente tela inicial desnecessário (Retirar aviso "existe uma análise dentro da régua determinada" (tela inicial e segue por todo processo);
* Informar ao usuário sobre possível carregamento de dados (loading...)
* Parte de comentário do órbita não apaga, nem edita;
* Levar para órbita data do street view (afim de alinhar uma maior credibilidade no dado de visualização);

‌

**Tarefa 1**

Retirar aviso que aparece sempre, independente de ter ou não uma analise em andamento ao buscar por um endereço a mensagem é exibida e fica na tela até que o usuário clique na tela.

**Aviso**  
”_Existe uma análise dentro da régua determinada. Por favor ative a Camada de Análise ou entre em contato com o Analista responsável.”_

**Tarefa 2**

Ajustar o mapa para que o padrão inicial ao acessar a tela seja o terceiro mapa da lista, pois as áreas que conversamos utilizam esse mapa por ter uma visão mais limpa e com a visão de comércios. 

Tarefa 3

Ajustar os textos apresentados ao entrar nos detalhes de uma camada aplicada, para que fiquem mais compreensivos.

‌

‌

### **1. Cores e Contraste**

* **Problema:** Algumas cores usadas nos ícones e textos não possuem contraste suficiente para garantir boa legibilidade, especialmente o amarelo em "Pendente".
* **Solução:**

    * Substitua o amarelo por uma cor mais forte (ex.: laranja escuro) ou adicione contornos para destacar os ícones.
    * Certifique-se de que todas as cores sigam as diretrizes de acessibilidade (WCAG) com relação ao contraste.
    

---

### **2. Hierarquia Visual**

* **Problema:** A hierarquia de informações não está clara, e os olhos do usuário podem se perder ao tentar encontrar informações importantes.
* **Solução:**

    * Utilize tamanhos diferentes de fonte ou negrito para destacar títulos, subtítulos e métricas importantes.
    * Separe visualmente as seções com espaçamento mais consistente ou bordas suaves.
    

---

### **3. Organização dos Cards (Status Gerais das Análises de Ponto)**

* **Problema:** Os cards de status (Negócio, Em Análise, Pendente, Lead Finalizado) são organizados horizontalmente, mas parecem desconectados do restante da tela.
* **Solução:**

    * Reorganize os cards em uma grade 2x2 para economizar espaço e facilitar a leitura em telas menores.
    * Adicione ícones maiores e títulos mais descritivos para reforçar a compreensão.
    

---

### **4. Gráficos e Taxa de Conversão**

* **Problema:** A "Taxa de Conversão" aparece destacada, mas o design atual não oferece contexto visual suficiente sobre sua relevância.
* **Solução:**

    * Adicione uma barra de progresso ou outro gráfico visual ao lado da taxa para reforçar seu impacto.
    * Reposicione o gráfico de "Pré-contratos fechados" mais próximo da Taxa de Conversão, criando uma relação visual.
    

---

### **5. Tabela de Situações das Análises**

* **Problema:** A tabela ocupa um grande espaço, mas carece de organização e elementos visuais para facilitar a leitura.
* **Solução:**

    * Adicione linhas ou faixas zebradas para facilitar a distinção entre as linhas.
    * Crie um menu suspenso ou botões para que o usuário possa filtrar os dados exibidos diretamente.
    * Considere adicionar um indicador visual (ex.: barras coloridas ou ícones) para destacar números mais relevantes.
    

---

### **6. Seção "Contratos por Bandeiras - 2025"**

* **Problema:** A seção está visualmente isolada no canto inferior direito, dificultando sua relação com o restante da tela.
* **Solução:**

    * Reposicione a seção para alinhá-la com o gráfico ou coloque-a mais centralizada.
    * Utilize ícones maiores ou miniaturas para tornar as informações mais chamativas.
    

---

### **7. Melhorias gerais de usabilidade**

* **Adicione tooltips (dicas) nos ícones** para explicar rapidamente o que cada métrica ou botão representa.
* Inclua botões de ação claros (ex.: "Nova análise") destacados com cores que chamem a atenção do usuário.
* Ajuste os espaçamentos entre as seções para evitar que a interface pareça "apertada".

---

### **Sugestão de Layout**

1. **Topo da página:** "Status Gerais das Análises de Ponto" seguido da "Taxa de Conversão".
2. **Meio:** Gráficos e tabela organizados lado a lado ou empilhados para otimizar o espaço.
3. **Rodapé:** "Contratos por Bandeiras" com ícones ou gráficos de fácil leitura.
