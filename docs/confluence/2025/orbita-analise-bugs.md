# Órbita - Analise de bugs

> Fonte: https://farmarcas.atlassian.net/wiki/spaces/SR/pages/3022553098/rbita+-+Analise+de+bugs · Última atualização no Confluence: fev. 11, 2025
> Nota: esta página continha imagens no Confluence original que não puderam ser migradas automaticamente. Consulte a fonte acima para o conteúdo visual completo.

**Bug 2**

<custom data-type="emoji" data-id="id-0">:lady_beetle:</custom> BUG - Órbita

**Ambiente:** Produção e Stage

**Login:** Usuário Farmarcas - Admin

**Caminho no sistema:** 

Login Radar - Órbita - Nova Análise - Salvar análise

**Descrição do Problema:**  
Ao preencher os dados necessários para salvar uma nova analise e clicar em salvar analise, o sistema está apresentando uma mensagem **“Não foi possível criar a Análise.”**

**Passos para Reprodução:**  
Acessar o Órbita em homologação e clicar em **Nova análise** no canto superior direito da tela, o modal irá se abrir para o preenchimento das informações **(Lead, Empresário…)**, ao preencher os dados o botão de **Salvar análise** será habilitado e ao clicar o erro é apresentado na tela. **“Não foi possível criar a Análise.”**

**Resultado Esperado:**  
Deve ser possível salvar a análise normalmente e só apresentar a mensagem no caso de alguma falha pontual ao gravar uma nova ação.

Aparentemente a nova analise está sendo salva, mas está muito demorada, após realizar o registro e tentar salvar a mensagem de erro foi apresentada e não apareceu os novos registros, porém ao retornar a tela foi possível identificar os três registros e além disso os novos retornos foram apresentados.

---

**Bug 3**

 <custom data-type="emoji" data-id="id-1">:lady_beetle:</custom> BUG - Órbita

**Ambiente:** Produção e Stage

**Login:** Usuário Farmarcas - Admin

**Caminho no sistema:** 

Login Radar - Órbita - Nova Análise - Salvar análise

**Descrição do Problema:**  
Ao criar uma nova analise de ponto os status não estão sendo refletidos na tela nos big numbers apresentados, temos duas colunas da tabela onde temos alguns status iguais e nesse caso faz sentido verificar qual deles está ligado aos números e o motivo de não refletir na tela.

**Passos para Reprodução:**  
Ao acessar o Órbita e salvar uma analise, deve gravar qual o status e qual a situação do ponto preenchida e verificar se está refletindo na tela, onde temos os status em destaque. Os números estão disponíveis em Analise de Pontos e Indicadores - Analise de pontos [https://dev.radar.farmarcas.com.br/orbita/analysis/dashboard](https://dev.radar.farmarcas.com.br/orbita/analysis/dashboard)  [https://dev.radar.farmarcas.com.br/orbita/analysis?myAnalysis=true&page=1](https://dev.radar.farmarcas.com.br/orbita/analysis?myAnalysis=true&page=1) 

**Resultado Esperado:**  
Ao criar uma analise de ponto, o “status” dessa analise deve refletir na tela para que seja possível acompanhar de forma visual as quantias referente ao lista abaixo.

---

**Bug 4**

 <custom data-type="emoji" data-id="id-4">:lady_beetle:</custom> BUG - Órbita

**Ambiente:** Produção e Stage

**Login:** Usuário Farmarcas - Admin

**Caminho no sistema:** 

Login Radar - Órbita - Home - Informar um endereço - Explorar

**Descrição do Problema:**  
Hoje, independente de ter ou não uma analise em andamento no prazo de 7 dias, ao buscar por um endereço a mensagem é exibida e fica na tela até que o usuário clique na tela.

_**“Existe uma análise dentro da régua determinada. Por favor ative a Camada de Análise ou entre em contato com o Analista responsável.”**_

**REGRAS**

A mensagem deve ser exibida se:

* Houver uma analise dentro de 300 metros aberta em menos de 7 dias corridos. Ou seja, qualquer analise de ponto nova em que existe outra a 300 metros dela que foi a 7 atrás ou menos deve sinalizar na tela.
* Se existir um contrato fechado da mesma região (300 metros) que está sendo analisada, também deve sinalizar com a mensagem na tela.
* Se já houver uma loja existente da Farmarcas na região (300 metros), deve avisar o analista para que seja analisado caso a caso.

**Passos para Reprodução:**  
Ao acessar o Órbita, buscar por um endereço comum de buscas. Ex: Av Paulista, 2300 e dessa forma o sistema vai apresentar a mensagem no canto inferior esquerdo, de que existe uma analise em andamento. Devemos investigar se o Órbita está considerando as regras para trazer esse retorno.  [https://dev.radar.farmarcas.com.br/orbita/analysis/dashboard](https://dev.radar.farmarcas.com.br/orbita/analysis/dashboard)  [https://dev.radar.farmarcas.com.br/orbita/analysis?myAnalysis=true&page=1](https://dev.radar.farmarcas.com.br/orbita/analysis?myAnalysis=true&page=1) 

**Resultado Esperado:**  
Ao iniciar uma nova analise de ponto, o sistema só deve exibir a mensagem se houver as condições reportadas nas regras abaixo, e consequentemente deixar de exibir caso alguma das regras deixe de fazer sentido. Ex: A analise existente passar dos 7 dias de “reserva.”

---

**Bug 4**

 <custom data-type="emoji" data-id="id-7">:lady_beetle:</custom> BUG - Órbita

**Ambiente:** Produção e Stage

**Login:** 

**Caminho no sistema:** 

Login Radar 

**Descrição do Problema:**

Ao

‌

**Passos para Reprodução:**  
Ao 

**Resultado Esperado:**  
Ao

---

**Bug 21**

 <custom data-type="emoji" data-id="id-8">:lady_beetle:</custom> BUG - Órbita

**Ambiente:** Produção e Stage

**Login:** Usuário Farmarcas - Admin

**Caminho no sistema:** 

Login Radar - Órbita - Analise de pontos - Filtros - Bandeira

**Descrição do Problema:**

Ao utilizar o filtro de bandeira na tela de analises de pontos mesmo vendo que existem lojas de determinada bandeira, o sistema não está retornando a tabela com os dados corretos filtrados sendo exibidos na tela.

‌

**Passos para Reprodução:**  
Ao acessar o Órbita, entrar na pagina de análise de pontos e utilizar o filtro de bandeiras  [https://dev.radar.farmarcas.com.br/orbita/analysis?myAnalysis=true&page=1](https://dev.radar.farmarcas.com.br/orbita/analysis?myAnalysis=true&page=1) 

**Resultado Esperado:**  
Ao realizar o filtro de Bandeira, deve refletir de forma correta a listagem com os registros que fazem parte da bandeira selecionada.

---

Possível bug, ou comportamento estranho do gráfico, onde as datas não estão fazendo sentido

‌

‌

Possível Bug, ou melhoria é que o N de lead deixa preencher com letras também, ao invés de apenas números

Bug

Ao clicar em indicadores, quando o menu lateral está fechado ele não abre as opções para que o usuário consiga clicar, é como se o menu ficasse inativo.

‌
