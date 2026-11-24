# Regras de negócio — Zoneamento no Órbita

> **Status:** rascunho v3, revisado por analista de Expansão e por liderança,
> com os refinamentos do PM de 2026-11-17 (dupla coordenada, campos de grupo
> econômico e gate universal). Pronto para transcrição no template de regra de
> negócio do Confluence.
> **Data:** 2026-11-17
> **Escopo:** aplicação automática das regras de zoneamento e expansão da
> Farmarcas dentro do Órbita, sobre uma base nova de lojas sincronizada do Radar
> em D-1, combinada com as bases de contratos de expansão e de análises de ponto.
> **Fonte das regras:** Confluence "4.5 Regras de Zoneamento e Regras de Expansão"
> (página 3755245621, v5 de 2026-02-24) e "6.1 Regras de Expansão" (3755769865, v8).

---

## 0. O que este documento pede de decisão

Este documento **não é só especificação de sistema**. Cinco itens abaixo mudam
quantos pedidos são barrados — são política de expansão, não implementação, e
precisam de dono nomeado antes de a página ser publicada.

| # | Decisão | Proposta deste documento | Dono |
|---|---|---|---|
| **D-00** | O teto conta **grupos econômicos** ou **lojas**? | grupos (RN-02) | quem assina a 4.5/6.1 |
| **D-08** | Fonte de população que corta a faixa | base interna do Órbita | Expansão |
| **D-14** | Contrato e análise aprovada **bloqueiam** ou **alertam**? | contrato bloqueia; análise, ver RN-03 | Expansão |
| **D-04** | Alçada e escopo da exceção aprovada | ver RN-12 | Expansão |
| **D-01** | Distância mínima vale abaixo de 60 mil habitantes? | hoje não é avaliada | Expansão |

### Recomendação de sequenciamento: ligar o gate em modo observação

Antes de bloquear qualquer pedido, o Órbita deve rodar o gate em **modo
observação por 60–90 dias**: calcula e registra o veredito, **não bloqueia**, e
mede sobre o fluxo real:

- quantos pedidos mudariam de resultado com o teto por grupo (RN-02);
- quantos impedimentos seriam falsos por erro de cadastro (RN-10);
- quantas exceções seriam pedidas, e contra qual regra;
- quantos pedidos seriam barrados por reserva de contrato ou análise (RN-03).

**Por quê:** a medição que sustenta RN-02 hoje (25% → 4% das cidades acima do
teto) foi feita sobre o **estoque de lojas**, não sobre o **fluxo de pedidos**.
A pergunta que a liderança vai fazer — "quantos pedidos dos últimos 12 meses
mudariam de veredito?" — ainda não tem resposta. O modo observação responde com
dado do próprio fluxo, em vez de projeção.

---

## 1. Objetivo

Hoje a consulta de zoneamento é manual e depende de o analista saber que ela
existe, onde consultar e como contar. Este documento define as regras para que o
Órbita execute essa consulta sozinho, **antes** da análise de mercado, e devolva
um veredito único e auditável para o ponto pedido.

O que a regra protege, no texto das próprias páginas: *"evitar conflito e
concorrência desleal entre associados"*, *"garantir a perenidade e expansão
saudável das lojas Farmarcas"* e *"evita a canibalização entre lojas pertencentes
a Farmarcas"*.

**Os três objetivos não apontam na mesma direção** — ver a ressalva em RN-02.

**O zoneamento é gate, não indicador.** A página 6.1 determina a consulta antes
de prosseguir com a análise. Portanto o Órbita não pode apresentar zoneamento
como mais uma camada ao lado de renda e concorrência: ele roda primeiro e
condiciona o resto.

---

## 2. Definições operacionais

| Termo | Definição no produto |
|---|---|
| **Município da praça** | O município (código IBGE 7 dígitos) do ponto pedido. É a unidade de contagem do teto. |
| **Loja Farmarcas** | Registro do cadastro de lojas vindo do Radar. **Nunca** uma loja identificada por nome de bandeira dentro da camada Concorrentes. |
| **Endereço da Receita** | Endereço fiscal da loja, como consta no cadastro da Receita Federal. Tem coordenada própria. |
| **Endereço popular** | Endereço de uso comercial/operacional da loja — onde ela de fato opera e é encontrada. Tem coordenada própria e **pode divergir** do endereço da Receita. |
| **Grupo econômico (GE)** | Unidade do teto. Campo próprio do cadastro do Radar, com responsável associado — ver RN-10 e D-03. |
| **Ocupar vaga** | Contar para o teto do município. Conceito interno deste documento; na interface, usar "a cidade está fechada / ainda cabe um grupo". |
| **Solicitante** | Quem pede a análise do ponto: empresário novo ou empresário que já opera loja(s) Farmarcas. |
| **Veredito** | Resultado do gate: `liberado`, `alerta`, `impedimento` ou `indeterminado`. |

> ⚠️ **Não usar "praça" sozinho na interface.** No dia a dia do time, praça é
> área de influência comercial — em cidade grande, o bairro ou a região. Usar a
> mesma palavra como sinônimo de município dentro do mesmo produto, ao lado das
> telas de mercado, troca o significado no meio da análise.

### 2.1 Status de loja — definição pendente

Os quatro status do cadastro decidem quem ocupa vaga (RN-03) e precisam de uma
linha de definição cada, vinda do Radar:

| Status | Ocupa vaga | Definição |
|---|---|---|
| Ativado | sim | loja em operação |
| Montando | sim | **a definir** — inclusive há quanto tempo um registro pode permanecer neste status |
| Transição | sim | **a definir.** Se transição significar saída da rede em andamento, contar como ocupando vaga fecha uma praça que está prestes a abrir |
| Desativado | não | loja encerrada |

---

## 3. Fontes de dado e contrato de dado

> Os números deste documento vêm do dump de bases do Órbita extraído em
> **2026-10-26** e do cadastro de lojas `relatorio-lojas-23_10_2026`. O dump é
> estático e envelhece em silêncio. **Divergência conhecida a resolver:** as
> referências internas registram ora 2.804 lojas / 1.841 com coordenada, ora
> 2.808 / 1.844. Conferir contra a carga do Radar antes de publicar.

### 3.1 Base de lojas — sincronismo D-1 com o Radar

Substitui o relatório estático de lojas (`.xlsx`) usado hoje.

| Requisito | Definição |
|---|---|
| Periodicidade | Carga diária, D-1 |
| Chave | CNPJ da loja |

| Campo | Obrigatório para | Observação |
|---|---|---|
| CNPJ | identidade e deduplicação (RN-03.1, RN-04.1) | chave da carga |
| Nome / razão social | identificação em tela | — |
| **Endereço da Receita** + município + UF | contagem do teto (RN-02) | endereço fiscal |
| **Latitude e longitude do endereço da Receita** | distância mínima (RN-06) | — |
| **Endereço popular** + município + UF | contagem do teto (RN-02) | pode divergir do fiscal |
| **Latitude e longitude do endereço popular** | distância mínima (RN-06) | — |
| **Status** | quem ocupa vaga (RN-03) | Ativado / Montando / Transição / Desativado |
| **Bandeira** | distância mínima e alternância (RN-06, RN-07) | exige lista canônica (RN-06.5) |
| **Modelo de Negócio** | bandeira popular do 2º grupo (RN-05) | Popular / Convencional |
| **Grupo econômico** | teto (RN-02, RN-04) | **identificador próprio**, não só texto |
| **Responsável pelo grupo econômico** | vínculo com o solicitante (RN-04.1) | dado pessoal: ver RN-10.4 |

> ⚠️ **Pré-requisito a confirmar com o time do Radar.** A especificação inicial
> previa apenas nome, endereço, latitude e longitude de um único endereço. Sem
> `Grupo econômico` não há teto; sem `Status` não se sabe quem ocupa vaga; sem
> `Bandeira` não há distância mínima; sem `Modelo de Negócio` não há a exigência
> de bandeira popular; **sem as duas coordenadas não há como travar dos dois
> lados** (RN-DADO-05). Se algum campo não existir no Radar, a regra
> correspondente não pode ser automatizada e precisa ser declarada como não
> avaliada — nunca presumida.

> **Ganho que o campo próprio de grupo econômico traz.** Enquanto o GE era
> apurado pelo nome do responsável, grafia divergente inventava um grupo e barrava
> pedido que caberia (RN-10). Com identificador próprio vindo do Radar, essa
> classe de impedimento falso desaparece — **desde que o identificador seja
> estável e único por grupo**. Confirmar com o Radar: é chave de cadastro ou
> rótulo editável? Se for editável, a fragilidade continua, só muda de campo.

**RN-DADO-01 — Falha de carga.** Se a carga D-1 falhar, o Órbita opera com a
última carga bem-sucedida e **exibe a data da base em toda tela de zoneamento**.
Acima de um limite de defasagem (D-06), o gate devolve `indeterminado` em vez de
um veredito calculado sobre base velha.

**RN-DADO-02 — Cobertura de coordenada.** Loja sem coordenada utilizável entra
na contagem do teto (que é por município cadastrado) mas **não** pode ser
checada na distância mínima. Isso é lacuna declarada, não ausência de risco.

A cobertura passa a ser medida **por endereço**: uma loja pode ter coordenada da
Receita e não ter a do endereço popular, ou o contrário. O veredito declara qual
dos dois endereços foi checado e qual não foi — dizer "distância checada" sem
dizer contra qual endereço esconde metade da regra.

> ⚠️ **Consequência de equidade, não só de cobertura.** Com 66% de cobertura,
> dois pedidos equivalentes recebem vereditos diferentes porque a loja vizinha de
> um tem coordenada e a do outro não. Um é barrado, o outro passa. Visto de fora
> isso é arbitrariedade. **A geocodificação dos endereços é pré-requisito de
> cronograma do gate**, não item de backlog (seção 8).

**RN-DADO-03 — Cadastro em município errado.** Existem registros com coordenada
em município diferente do cadastrado (caso verificado em 2026-10-27: loja
cadastrada em Patrocínio Paulista/SP com coordenada a 342 m do centro de
Franca/SP, cidades a ~25 km). Como o teto é contado por município cadastrado, um
cadastro errado erra o teto junto.

O Órbita procura lojas por coordenada num raio de 1.000 m do ponto,
independentemente do município cadastrado. O resultado tem dois destinos:

- **muda o veredito** quando entra na checagem de distância mínima (RN-06.3);
- **não muda o veredito** quanto ao teto — vira item de fila de qualidade de
  cadastro do Radar, não alerta no meio da análise de ponto, onde o analista não
  tem como resolvê-lo.

**RN-DADO-05 — Toda loja tem dois endereços, e a regra trava nos dois.**

Endereço da Receita e endereço popular podem divergir, e a divergência é comum:
o endereço fiscal pode ser o do escritório, de outra unidade do grupo ou de um
imóvel vizinho. Usar só um deles deixa a regra cega justamente onde a loja de
fato opera, ou justamente onde ela está registrada.

| Onde | Como as duas coordenadas entram |
|---|---|
| **Distância mínima (RN-06)** | a loja é avaliada pelos **dois** pontos; vale a menor distância encontrada. Se qualquer um dos dois violar o mínimo, a regra está violada. |
| **Teto do município (RN-02)** | a loja ocupa vaga no município de **cada um** dos dois endereços — se eles caem em municípios diferentes, ela ocupa vaga nos dois |
| **Veredito** | declara contra qual endereço a violação ocorreu — Receita, popular ou ambos |

> **Decisão de negócio registrada:** a área de negócio está ciente de que travar
> pelos dois endereços **torna a regra de zoneamento mais dura** — mais pontos
> passam a violar a distância mínima — e aceita esse efeito.

**RN-DADO-05.2 — Loja com endereços em municípios diferentes ocupa vaga nos
dois.** Decidido em 2026-11-17, pela mesma lógica de travar dos dois lados.

Consequências a acompanhar, porque não são óbvias:

- **Uma loja conta duas vezes na rede**, em cidades diferentes. Pode fechar um
  município onde nenhuma loja foi aberta — basta que um endereço fiscal aponte
  para lá.
- **Numa cidade de teto 1, isso basta para barrar qualquer pedido novo**, ainda
  que a operação real esteja em outro município.
- **A medição que sustenta RN-02** (207 de 830 cidades contando lojas, 34
  contando grupos) foi feita com **um único endereço por loja**. Contando os
  dois, esses números sobem — quanto, ainda não foi medido. **Remedir antes de
  levar os percentuais à liderança.**
- O caso mais provável de endereços em municípios diferentes é **erro de
  cadastro**, não duas operações reais (RN-DADO-05.1). Com esta decisão, o erro
  de cadastro passa a fechar um município inteiro — o que torna a fila de
  qualidade do Radar parte da regra, não higiene opcional.

**RN-DADO-05.1 — Divergência entre os dois endereços é achado, não ruído.**
Quando a distância entre o endereço da Receita e o popular da mesma loja passar
de um limite a definir, o registro entra na fila de qualidade de cadastro do
Radar. Divergência grande costuma ser erro de cadastro, não duas localizações
reais — e nesse caso a regra endureceu contra um endereço que não existe.

### 3.2 Contratos de expansão e análises de ponto

| Base | Papel no zoneamento |
|---|---|
| `contratos_expansao` | Contrato assinado **ocupa vaga** antes de a loja existir no cadastro (RN-03) |
| `all_expansion.analysis_data` | Análise de ponto aprovada — ver RN-03 e D-14 |

**RN-DADO-04 — Histórico do ponto.** Além de ocupar vaga, a base de análises
responde a pergunta que hoje consome tempo do analista: **este endereço já foi
analisado antes, quando, e com que resultado?** O mesmo ponto volta por
corretores diferentes. O gate exibe o histórico do ponto (data, veredito
anterior, se houve exceção) sempre que houver análise anterior num raio curto.

### 3.3 População

**Decisão do PM, a ratificar com Expansão (D-08):** a faixa é cortada pela
**população da base interna do Órbita** (`populacao_municipios`).

> ⚠️ **Duas consequências que precisam estar visíveis para quem aprova.**
>
> 1. **A base interna não é o Censo 2022 e seu ano de referência não está
>    declarado em lugar nenhum da base.** Em Franca/SP ela registra 366.566
>    contra 352.536 do Censo 2022 (+4,0%, verificado na API do IBGE em
>    2026-10-26). Perto dos cortes de 60, 120 e 200 mil habitantes, essa
>    diferença **troca a faixa e o teto**.
> 2. **O dossiê de região produzido hoje pela skill de análise corta a faixa pelo
>    Censo 2022.** Mantidas as duas fontes, o mesmo ponto pode receber veredito
>    diferente no produto e no dossiê.
>
> **Posição da revisão de liderança:** diante de um associado barrado, "a regra
> usou uma base interna sem proveniência declarada" é indefensável; "usou o
> Censo/estimativa do IBGE, pública e datada" é defensável. A recomendação é
> adotar o IBGE, o que também fecha a divergência com o dossiê.

**RN-POP-01.** Toda tela e todo relatório que exibam veredito de zoneamento
declaram qual população foi usada, com fonte e ano de referência.

---

## 4. As regras

### RN-01 — O zoneamento roda antes da análise de mercado

Nenhuma análise de ponto avança para as camadas de mercado antes do veredito de
zoneamento. Ponto com `impedimento` não consome análise de mercado. Isso vale
para **todo caminho de entrada de análise**, mapa ou Órbita IA — ver RN-18.

**RN-01.1 — Duas válvulas obrigatórias.** A economia só se realiza se o analista
não voltar a fazer tentativa e erro na mão:

- **Ponto alternativo:** reexecutar o gate num ponto próximo precisa ser barato
  na tela, e o resultado deve indicar, quando possível, o que destravaria
  (ver RN-13.1).
- **Pedido de exceção:** destrava a análise de mercado sob demanda, porque quem
  aprova a exceção precisa dos números econômicos para decidir (RN-12).

### RN-02 — Faixas de população e teto do município

**Proposta: o teto conta GRUPOS ECONÔMICOS, não lojas (D-00).**

| População do município | Teto de grupos econômicos | Condição adicional |
|---|---|---|
| ≤ 60.000 | 1 | sem expansão adicional |
| 60.001 – 120.000 | 2 | o 2º grupo entra com bandeira **popular** (RN-05) |
| 120.001 – 200.000 | 3 | alternância de bandeiras (RN-07) |
| > 200.000 | sem teto | ocupação decidida por market share |

**Argumento a favor.** Não há conflito entre associados onde só há um associado.
Contando lojas, 207 das 830 cidades com loja ativa (25%) estouravam o teto;
contando grupos econômicos, são 34 (4%). A leitura por lojas acusava como
violação o que era estratégia de um único associado.

> **Os dois percentuais acima estão defasados (D-18).** Foram medidos com **um
> endereço por loja**. Com a contagem pelos dois endereços (RN-DADO-05.2), ambos
> sobem. Remedir antes de usá-los como argumento.

> ⚠️ **Argumento contrário, que a liderança precisa pesar (D-00).**
>
> 1. **O objetivo declarado tem duas metades, e esta proposta só atende uma.**
>    A regra também diz *"evita a canibalização entre lojas pertencentes a
>    Farmarcas"* — canibalização entre lojas do mesmo dono está dentro do escopo
>    original. A mudança de unidade retira isso do alcance do gate.
> 2. **"É risco dele, decisão dele" pressupõe que a Farmarcas não tem
>    exposição.** Ela tem: fornecimento, crédito, recebíveis, marca e share de
>    compra. Associado que se satura e quebra é prejuízo da central também.
> 3. **A mudança é uma liberalização material** (173 cidades deixam de estar
>    acima do teto) decidida fora do fórum que assina a 4.5/6.1.
>
> **Enquanto D-00 estiver aberto, o gate calcula e exibe as duas contagens — por
> loja e por grupo — e não escolhe sozinho qual barra.**

> **Premissa declarada:** a página escreve as faixas com limites sobrepostos
> (60, 120 e 200 mil). Aqui os cortes são fechados em 60.000, 120.000 e 200.000.

### RN-03 — Quem ocupa vaga

| Origem | Condição | Efeito |
|---|---|---|
| Cadastro de lojas (Radar) | `Status` ∈ {Ativado, Montando, Transição} | ocupa vaga |
| Cadastro de lojas (Radar) | `Status` = Desativado | não ocupa |
| Contrato de expansão | assinado e vigente | ocupa vaga, **impedimento** |
| Análise de ponto | situação aprovada (lista em D-07) | ver ressalva (D-14) |

> ⚠️ **Análise aprovada como bloqueio é a decisão de pior relação
> risco/benefício do documento (D-14).** Contrato tem contraparte, vigência e
> evento de distrato. Análise aprovada não tem nada disso, e hoje faltam: prazo
> de validade (D-02), lista de situações válidas (D-07), varredura dos registros
> antigos da base e evento confiável de cancelamento. Resultado concreto:
> associado barrado hoje por uma análise de terceiro feita há anos que ninguém
> encerrou — e que ele não pode saber de quem é, por LGPD.
>
> **Recomendação da revisão:** análise aprovada entra como **alerta de "vaga em
> disputa"**, não como impedimento, até que D-02 e D-07 estejam fechados e a base
> tenha passado por varredura. Contrato assinado bloqueia normalmente.

> **Premissa declarada:** a regra oficial não diz que loja desativada libera
> vaga, nem que contrato ou análise reservam vaga. As três decisões são do
> produto e precisam constar da página do Confluence quando ela for atualizada.

**RN-03.1 — Deduplicação obrigatória.** Um mesmo ponto comercial percorre
análise → contrato → loja cadastrada. Sem deduplicação, ele é contado **três
vezes** e barra um município sozinho. A contagem deduplica por, nesta ordem:

1. CNPJ, quando presente nos registros;
2. vínculo explícito de origem (análise que gerou o contrato, contrato que gerou
   a loja), se o dado existir;
3. proximidade geográfica (menos de 100 m) somada ao mesmo grupo econômico.

Se a deduplicação não for possível, o registro entra **uma única vez**, pela
origem mais avançada do funil (loja > contrato > análise), e o fato é declarado.

**RN-03.2 — Validade da reserva.** Contrato cancelado ou distratado deixa de
ocupar vaga imediatamente — **o evento de distrato precisa chegar ao Órbita**.
Análise aprovada expira após um prazo (D-02); sem prazo, uma análise antiga
bloqueia um município indefinidamente.

### RN-04 — Contagem com o pedido incluído

A regra decide sobre o cenário **depois** do pedido.

- O pedido sempre soma **uma loja**.
- O pedido soma **um grupo econômico** apenas quando o solicitante ainda não
  responde por loja, contrato ou análise aprovada neste município.

Logo: solicitante que já está no município não traz grupo novo e **não é barrado
pelo teto**, mesmo que a cidade já tenha mais lojas do que a faixa dimensiona.
Ser associado em outro município **não** dá vaga — estar na praça, sim.

> ⚠️ **Efeito de política a declarar (D-00).** Combinado com RN-02, isso cria
> exclusividade de facto: quem chega primeiro numa cidade pequena pode abrir N
> lojas e fechar o município para qualquer grupo novo, indefinidamente, em
> centenas de municípios. Pode ser a política desejada — mas precisa ser aprovada
> como política, não emergir como efeito aritmético de uma regra de contagem. Se
> a liderança não quiser isso, a correção é um limite de lojas por grupo por
> município (hoje só alerta, RN-09).

**RN-04.1 — O vínculo é proposto pelo sistema, confirmado pelo analista.** O que
a regra precisa saber não é "novo ou associado", é **"este solicitante já
responde por loja neste município?"** — isso é consulta ao cadastro, não pergunta
ao analista. O Órbita propõe o vínculo (por raiz de CNPJ, D-03) e o analista
confirma. Confirmar é um clique; descobrir é meia hora.

### RN-05 — Bandeira popular do 2º grupo (faixa 60–120 mil)

Na faixa 60.001–120.000 habitantes, o grupo que entra como **2º do município**
deve abrir com bandeira de modelo **Popular**.

| Caso | Resultado |
|---|---|
| Pedido traz o 2º grupo econômico e o modelo é Convencional | **impedimento** |
| Pedido é loja adicional de grupo já presente, modelo Convencional | **alerta** |
| **Modelo não informado no pedido, trazendo o 2º grupo** | **regra não avaliada**, declarada no veredito |

> No fluxo real o modelo raramente vem definido no pedido inicial — ele é
> consequência da análise e da negociação comercial. Sem a linha acima, o gate
> devolveria `liberado` por uma regra que nunca foi verificada, e o analista não
> teria como saber.

**RN-05.1.** Verificar se o modelo é derivável da bandeira no cadastro (D-13).
Se for, não deve ser pergunta ao analista; se bandeira e modelo puderem divergir
no registro, o documento precisa dizer qual prevalece.

> **Premissa declarada:** a página escreve "a 2ª loja", não "o 2º grupo". A
> leitura por grupo é coerente com o teto (RN-02) e cai junto com D-00.

### RN-06 — Distância mínima entre lojas Farmarcas

**A checagem roda contra os dois endereços de cada loja** — Receita e popular
(RN-DADO-05). Vale a menor distância encontrada: basta um dos dois violar o
mínimo para a regra estar violada. O veredito diz contra qual endereço.

| Caso | Distância mínima |
|---|---|
| Mesma bandeira | **300 m** |
| Bandeira diferente | **500 m** |

| Faixa de população | Resultado do descumprimento |
|---|---|
| ≤ 60.000 | **regra não avaliada hoje** — ver alerta abaixo (D-01) |
| 60.001 – 200.000 | **impedimento** (mas ver RN-06.1) |
| > 200.000 | **alerta** (a página não declara distância acima de 200 mil) |

> ⚠️ **Buraco conhecido (D-01).** A checagem só roda acima de 60 mil habitantes.
> Isso fazia sentido quando o teto contava lojas: numa cidade de teto 1 com 2
> lojas, o teto barrava antes. Com o teto contando grupos, nasceu uma classe de
> casos — cidade abaixo de 60 mil onde o teto **não** barra porque as lojas são
> todas do mesmo grupo — em que a distância nunca é avaliada. **É a faixa de
> maior volume de pedidos**, ou seja, é justamente onde o gate não poupa a
> checagem manual. Até D-01 ser decidido, o Órbita declara explicitamente
> "distância mínima não avaliada nesta faixa".

**RN-06.1 — De quem é a loja que barrou (D-09).** RN-11.1 trata sobreposição com
loja do próprio solicitante como efeito econômico a dimensionar; a tabela acima
trata qualquer loja como impedimento. São respostas opostas para o pedido mais
comum do perfil "já associado": a 2ª loja dele a 250 m da própria loja.

Enquanto D-09 estiver aberto, o veredito **separa os dois casos** e nunca os
apresenta como o mesmo item:

| Loja que viola a distância | Resultado |
|---|---|
| de **outro** associado | impedimento (é o conflito que a regra protege) |
| do **próprio** solicitante | alerta com o efeito econômico dimensionado |

**RN-06.2 — Bandeira não informada.** Aplica-se o critério mais restritivo
(500 m) e o fato é declarado.

**RN-06.3 — Distância não respeita divisa de município (D-10).** O teto é
contado por município cadastrado, mas a distância mínima deve rodar **por
coordenada, independentemente do município**. Ponto em divisa, conurbação ou
distrito é caso comum, e uma loja Farmarcas a 300 m do outro lado da divisa é
exatamente o conflito entre associados que a regra protege. Sem esta regra, o
produto enxerga a loja e declara que aquilo não é zoneamento (RN-DADO-03).

**RN-06.4 — Loja sem coordenada.** Gera alerta de "distância não pôde ser
checada", com a contagem de lojas afetadas. O centroide do bairro pode indicar
ordem de grandeza, mas **nunca** derruba nem sustenta um impedimento sozinho.

**RN-06.5 — Normalização de bandeira.** A comparação de bandeira decide 300 vs
500 m. Variação de grafia entre duas lojas da mesma bandeira inverte o veredito —
a mesma fragilidade de RN-10, sem o mesmo cuidado. É necessária uma **lista
canônica de bandeiras**, com dono declarado.

### RN-07 — Alternância de bandeiras (faixa 120–200 mil)

Se o município já tem loja da bandeira pretendida, o Órbita emite **alerta**.

> **Premissa declarada:** a página não diz se a alternância é obrigatória.

### RN-08 — Acima de 200 mil habitantes

Não há teto de grupos. O gate devolve **alerta** informando que a ocupação é
decidida por market share, que o zoneamento não quantifica.

> **A dizer no sumário executivo:** na prática, **não há gate em cidade grande**.
> Está correto pela regra, mas sem essa frase a liderança assume uma cobertura
> que o produto não tem.

### RN-09 — Densidade de lojas (alerta, nunca impedimento)

Quando o município, **com o pedido**, passa a ter mais lojas do que o número da
faixa, o Órbita emite alerta mostrando lado a lado a contagem de lojas e a de
grupos econômicos.

**RN-09.1.** Alerta que não obriga ninguém a nada vira ruído em três meses. É
preciso definir o que este alerta exige: parecer escrito, ciência registrada, ou
nada. Se for nada, assuma que será ignorado.

### RN-10 — Identificação do grupo econômico

O grupo é apurado pelo **identificador de grupo econômico do cadastro do Radar**,
não pelo nome do responsável. O responsável entra como dado associado, para o
vínculo com o solicitante (RN-04.1), nunca como chave de contagem.

> **O que isso resolve.** Enquanto a contagem dependia do nome do responsável,
> grafia divergente entre duas lojas do mesmo dono inventava um grupo e barrava
> pedido que caberia — impedimento falso contra um associado por erro de
> digitação de terceiro. Com identificador próprio, essa classe some.

> ⚠️ **O que ainda não resolve.** O identificador só é confiável se for **chave
> estável e única por grupo**, não rótulo editável — confirmar com o Radar (3.1).
> E ele responde "quais lojas pertencem ao mesmo registro de grupo", não "quais
> grupos são o mesmo dono": continua sem cobrir dono com mais de um GE
> cadastrado, GE com vários CNPJs e sócios, e sócio minoritário de um grupo já
> presente — o que muda a resposta de RN-04.1.

**RN-10.1 — Divergência não produz impedimento.** Enquanto D-03 estiver aberto,
divergência de grupo que **produziria impedimento** devolve `indeterminado` com
revisão humana, nunca `impedimento`. Vale também para loja sem identificador de
grupo na carga.

**RN-10.2 — O que falta em D-03.** Uma **definição de negócio de grupo
econômico** (sócio comum? quadro societário? raiz de CNPJ?) — decisão de
Expansão/Jurídico, com implementação de Produto + Radar. Raiz de CNPJ sozinha
também erra: mesmo dono com raízes distintas continua virando dois grupos.

**RN-10.3 — Responsável ausente.** Loja sem responsável registrado não permite
afirmar de quem ela é — nem que é do solicitante, nem que não é. O Órbita
distingue "não informado no cadastro" de "não é do solicitante". Nunca publica
como afirmação o que é ausência de dado.

**RN-10.4 — LGPD, e o que *não* é dado pessoal.** Nome de pessoa não entra em
tela nem em entregável; os grupos aparecem com rótulo anônimo (Grupo A, Grupo
B...). **Bandeira, endereço, status e CNPJ da loja não são dado pessoal** e devem
aparecer — sem eles a tela de impedimento é inútil para quem precisa agir.

**RN-10.5 — Rótulos estáveis.** O rótulo de grupo deve ser estável pelo menos
dentro do município: hoje ele é reatribuído por ordem de leitura, então o mesmo
grupo é "Grupo B" num ponto e "Grupo C" em outro ponto da mesma cidade.

### RN-11 — Perfil do solicitante

| Perfil | O que muda |
|---|---|
| **Empresário novo** | Nenhuma sobreposição é estratégica para ele. Toda loja Farmarcas próxima é de terceiro — é o conflito que a regra existe para evitar. |
| **Empresário já associado** | Sobreposição com loja **dele mesmo** pode ser deliberada (fechar mercado, ganhar share e poder de compra). Não é defeito do ponto; é o preço de uma estratégia que ele escolheu. |

**RN-11.1.** O Órbita separa sempre, como itens distintos:

- sobreposição com loja **do próprio solicitante** → efeito econômico a dimensionar;
- sobreposição com loja **de outro associado** → conflito de interesse entre associados.

Juntar os dois apaga a diferença que decide. Ver RN-06.1.

### RN-14 — Precisão do pedido

Parte dos pedidos chega sem endereço: *"associado quer abrir em Lagarto/SE,
região do centro"*. O gate não pode depender de coordenada para responder a
pergunta que mais barra.

| Precisão do pedido | RN avaliáveis | RN não avaliáveis |
|---|---|---|
| Município | RN-02, RN-03, RN-04, RN-05, RN-07, RN-09 | RN-06 (distância) |
| Bairro | as acima, com distância aproximada e sem veredito | RN-06 como impedimento |
| Endereço com coordenada | todas | — |

**Por que importa:** um veredito parcial de município — *"a cidade está fechada,
2 de 2 grupos; não adianta procurar endereço"* — encerra o pedido em segundos e
evita a análise inteira. É a economia mais barata do documento.

### RN-15 — Tipos de pedido

O documento, até aqui, só sabe avaliar **abertura nova**. Quatro dos pedidos mais
frequentes não são abertura, e sem regra própria voltam para a planilha do
analista (D-12):

| Tipo de pedido | O que quebra sem regra própria |
|---|---|
| **Mudança de endereço** de loja existente | a loja de origem continua ocupando vaga, o pedido soma mais uma loja, e a distância mínima é medida **contra o próprio endereço antigo** — a loja é barrada por si mesma se mudar 200 m. Regra: a loja de origem sai da contagem e da checagem; o pedido não soma loja nem grupo. **Com dois endereços por loja, o pedido precisa dizer qual deles muda** — mudar só o popular, só o da Receita, ou os dois são situações diferentes. |
| **Reabertura** de loja desativada | desativada não ocupa vaga (RN-03); se o município encheu nesse meio-tempo, o próprio dono não consegue reabrir a loja dele. Há direito preservado? Por quanto tempo? (D-11) |
| **Troca de bandeira** de loja existente | não é ponto novo, mas muda RN-06 para os vizinhos (300 ↔ 500 m) e RN-07 |
| **Transferência de titularidade** entre associados | muda a contagem de grupos sem nenhum ponto novo — pode estourar o teto sem que ninguém tenha aberto nada |

### RN-16 — Transição e passivo

Antes de ligar o bloqueio, é preciso decidir:

- **Pedidos em curso na virada:** pedido hoje em análise é barrado amanhã?
- **Municípios hoje acima do teto** (34 contando grupos, 207 contando lojas):
  ficam travados indefinidamente, inclusive para o associado já presente?

### RN-18 — Duas validações, em dois momentos

Decisão da área de negócio em 2026-11-17. O zoneamento não roda uma vez só: roda
**no começo**, barato e parcial, e **no fim**, completo.

| Momento | O que roda | O que o usuário vê |
|---|---|---|
| **1. Ao carregar o ponto** (fluxo normal do mapa) | **apenas a distância entre lojas**, com limiar único de **300 m**, independentemente da bandeira | **modal em tela** quando fere, explicando o motivo |
| **2. Ao salvar a análise** | validação de **grupo econômico** no município (teto) **e** a regra de zoneamento completa, incluindo distância com os limiares reais (300 m mesma bandeira / 500 m outra) | **aviso** dizendo se o ponto estaria bloqueado pelo zoneamento, e por quê |
| **Órbita IA** | na **tela final da IA**, quando montada | **modal** quando fere, com a mesma explicação |

**RN-18.1 — Todo aviso explica o motivo.** Nunca "este ponto fere o zoneamento"
sozinho. Em qualquer um dos três momentos, o texto diz:

- **qual regra foi ferida**, com o limiar aplicado (300 m, 500 m, teto da faixa);
- **contra o quê** — a loja (bandeira, bairro/endereço, status, distância medida,
  e se é do próprio solicitante) ou a contagem (quantos grupos, qual o teto);
- **contra qual endereço** da loja, Receita ou popular (RN-DADO-05);
- **o que destravaria**, quando dá para dizer — "faltam 120 m", "a cidade está
  fechada, 2 de 2 grupos".

Sem isso, o aviso só informa que o analista perdeu tempo; com isso, ele diz o que
fazer em seguida.

**RN-18.2 — Falha ou demora não liberam.** Se a consulta não concluir (carga
indisponível, timeout, erro), o resultado é `indeterminado` e o aviso diz isso.
Nunca silêncio — silêncio é lido como "passou". Um gate que falha aberto é pior
que gate nenhum: cria a confiança de que a checagem aconteceu.

> ⚠️ **Os 300 m da etapa 1 são o limiar mais permissivo, não o mais seguro
> (D-20).** A regra vigente exige 300 m só para a **mesma** bandeira; contra
> bandeira diferente são **500 m**. Checando sempre 300 m, todo ponto que estiver
> entre 300 e 500 m de uma loja de outra bandeira **passa limpo na etapa 1** e só
> aparece como violação ao salvar — depois de o analista ter feito a análise
> inteira, que é exatamente o custo que a etapa 1 existe para evitar.
>
> **Recomendação:** usar **500 m** como limiar de triagem (o maior, que pega
> todos os casos) e deixar o modal dizer se é violação certa (< 300 m) ou
> possível (300–500 m, a depender da bandeira). Mesma simplicidade de
> implementação, sem falso "passou".

> ⚠️ **O teto de grupos saiu da primeira etapa (D-21).** Ele é a checagem **mais
> barata e mais decisiva** — responde "a cidade está fechada" só com o município,
> sem precisar de endereço preciso (RN-14) — e agora só roda ao salvar. Resultado:
> o analista faz a análise inteira de uma cidade que já estava fechada antes de
> ele começar. **Recomendação:** rodar o teto também ao carregar o ponto; o custo
> é uma consulta por município.

**RN-18.3 — Tempo de resposta.** Rodando em toda entrada de análise, o gate está
no caminho crítico de uma interação frequente. É preciso um alvo de tempo de
resposta declarado, e a consulta de zoneamento (teto, grupos, distância) tem de
ser servida da base sincronizada, não calculada sobre o dump a cada chamada.

**RN-18.4 — Veredito parcial é melhor que nenhum.** Quando o endereço ainda não
está preciso, o gate devolve o que já dá para afirmar no nível de município
(RN-14) em vez de não responder. É o caso mais frequente no início da análise.

> **Efeito a observar.** Com o gate em toda entrada, o volume de análises
> registradas cresce. Isso só não realimenta o teto porque **apenas análise
> aprovada ocupa vaga** (RN-03) — endereço consultado e descartado não reserva
> nada. Se essa distinção se perder na implementação, o produto passa a barrar a
> si mesmo: cada consulta fecharia um pouco mais o município.

---

## 5. Veredito, comunicação e exceção

| Veredito | Efeito |
|---|---|
| **liberado** | Segue para a análise de mercado. Registra na procedência que o gate passou. |
| **alerta** | Segue para a análise de mercado, com os alertas em destaque antes das camadas. |
| **impedimento** | **Bloqueia.** A análise não avança. A tela abre com o impedimento, a regra citada e os números que a sustentam. |
| **indeterminado** | Falta dado para aplicar a regra (população ausente, carga defasada, divergência de grupo). Resolver antes de seguir. **Não é liberação.** |

### RN-17 — Comunicação e recurso do associado

Hoje o analista é o amortecedor humano entre a regra e o associado. O gate
automático tira esse amortecedor; é preciso colocar algo no lugar, ou a
combinação "impedimento automático + motivo que não pode ser detalhado por LGPD"
produz *"seu pedido foi negado por um motivo que não posso explicar"* — e
escalada direta à diretoria, caso a caso, que é exatamente o custo que este
trabalho existe para eliminar.

1. **O Órbita produz veredito para o time de Expansão, não comunica impedimento
   ao associado.**
2. **Texto padrão** do que se diz ao associado, por tipo de impedimento.
3. **Canal e prazo de recurso**, que é a porta de entrada do pedido de exceção.

### RN-12 — Exceção aprovada

Impedimento só é superado por **exceção registrada**, nunca por decisão do
analista na tela.

| Campo | Obrigatório |
|---|---|
| Quem aprovou | sim — perfil com alçada (D-04) |
| Data e hora | sim |
| Qual impedimento está sendo excepcionado | sim — por identificador da regra |
| Motivo | sim — **lista fechada** de motivos, mais texto livre complementar |
| Validade | sim (D-05) |

**RN-12.1 — Segregação de função.** Quem pede ≠ quem aprova. O solicitante e o
consultor comercial do pedido nunca aprovam.

**RN-12.2 — Nem todo impedimento é igualmente excepcionável.** Em particular,
**distância mínima violada contra loja de outro associado não deve ser
excepcionável apenas por alçada interna**: a regra existe para proteger um
terceiro que não está na sala. Definir se, e como, o associado incumbente é
ouvido (D-04).

**RN-12.3 — Validade autoriza, não revoga.** A validade da exceção significa
"autoriza a decisão/abertura até a data X". **Jamais** "a loja aberta perde a
autorização depois" — isso criaria passivo jurídico com o associado.

**RN-12.4 — Monitoramento de volume.** Taxa de exceção por regra, por mês,
revisada pelo fórum dono da 4.5/6.1. Regra excepcionada acima de um patamar não
é regra — é regra errada, e a resposta certa é revisar a 4.5, não normalizar o
override.

**RN-12.5 — A exceção é por impedimento, não por ponto.** Excepcionar o teto de
grupos não libera a distância mínima.

### RN-13 — Rastreabilidade do veredito

Todo veredito carrega: a regra aplicada com a faixa, os números que a sustentam
(população e fonte, lojas, grupos, distâncias), a data da carga do Radar, o
critério de deduplicação de grupo e as lacunas declaradas.

**RN-13.1 — A tela de impedimento precisa deixar agir.** Números não bastam.
Quando bate impedimento, o passo seguinte do analista é ligar para o
regional/comercial. Na tela:

- **qual loja barrou, identificável:** bandeira, bairro/endereço, status,
  distância, rótulo do grupo, e se é do próprio solicitante (RN-10.4);
- **há quanto tempo a loja está no status atual** — uma loja "Montando" há 14
  meses, na prática, não existe;
- **o que destravaria:** "faltam 120 m", "cabe se o modelo for Popular", "libera
  se o contrato X for distratado";
- **se o ponto já foi analisado antes**, quando e com que resultado (RN-DADO-04);
- **se já existe exceção registrada** para este município/ponto, e o caminho para
  pedir uma — sem isso o analista vira mensageiro entre solicitante e aprovador.

**RN-13.2 — Declaração só quando a lacuna afeta este veredito.** Se todas as
ressalvas imprimirem em todo veredito, a tela vira parede de texto e o analista
para de ler — inclusive a que importa. A lacuna de distância abaixo de 60 mil,
por exemplo, só sai quando a cidade está nessa faixa.

---

## 6. Decisões pendentes

> **Dono é um papel ou uma pessoa, com prazo — não uma área.** Área não aprova
> nada. Nomear antes de publicar.

| # | Decisão | Por que trava | Dono | Bloqueia publicar? |
|---|---|---|---|---|
| **D-00** | Teto conta grupos econômicos ou lojas | É mudança de política, não refinamento; libera 173 municípios | quem assina a 4.5/6.1 | **sim** |
| **D-01** | Distância mínima abaixo de 60 mil habitantes | Faixa de maior volume fica sem veredito | Expansão | **sim** |
| **D-02** | Validade da reserva por análise aprovada | Sem prazo, análise antiga bloqueia indefinidamente | Expansão | sim, se análise bloquear |
| **D-03** | Definição de negócio de grupo econômico e critério de dedup | Nome divergente produz impedimento falso | Expansão/Jurídico, com Produto + Radar | não, se adotado RN-10.1 |
| **D-04** | Alçada e escopo da exceção, e se o incumbente é ouvido | Sem alçada, RN-12 é override livre | Expansão | **sim** |
| **D-05** | Validade da exceção aprovada | Exceção perpétua reabre o município para sempre | Expansão | para ligar o gate |
| **D-06** | Defasagem máxima tolerada da carga do Radar | Define quando o veredito vira `indeterminado` | Produto propõe, Expansão aceita o custo | não |
| **D-07** | Situações de análise que contam como "aprovada" | Sem a lista, a contagem não é aplicável nem conferível | Produto + Expansão | **sim**, se análise bloquear |
| **D-08** | Fonte de população | Duas fontes = dois vereditos para o mesmo ponto | Expansão | **sim** |
| **D-09** | Distância violada contra loja do próprio solicitante: impedimento ou alerta | RN-06 e RN-11 hoje se contradizem | Expansão | **sim** |
| **D-10** | Distância roda por coordenada, ignorando divisa de município | Ponto em divisa é o conflito real não coberto | Expansão | **sim** |
| **D-11** | Reabertura de loja desativada: direito preservado, por quanto tempo | Dono pode não conseguir reabrir a própria loja | Expansão | não |
| **D-12** | Tipos de pedido suportados pelo gate | Quatro pedidos comuns voltam para a planilha | Produto + Expansão | não |
| **D-13** | Modelo de Negócio é derivável da bandeira | Define se é pergunta ao analista ou consulta à base | Produto + Radar | não |
| **D-14** | Contrato e análise bloqueiam ou alertam | Dá poder de bloqueio a base que era histórico | Expansão | **sim** |
| ~~D-15~~ | Loja com endereços em municípios diferentes ocupa vaga nos dois? | **Decidido em 2026-11-17: sim, ocupa nos dois** (RN-DADO-05.2) | PM | resolvida |
| **D-18** | Remedir o % de municípios acima do teto contando os dois endereços | Os números de RN-02 foram medidos com um endereço só e vão subir | Produto | **sim**, antes de levar os percentuais à liderança |
| **D-16** | Distância máxima tolerada entre os dois endereços da mesma loja | Acima dela, é erro de cadastro, e a regra endurece contra endereço inexistente | Produto + Radar | não |
| **D-17** | Alvo de tempo de resposta do gate | Ele passa a estar no caminho crítico de toda análise (RN-18.3) | Produto | não |

---

## 7. Divergências com as páginas atuais do Confluence (a corrigir)

| Página | O que está escrito | O que vale |
|---|---|---|
| 4.5 | "raio 300m" | 300 m mesma bandeira / **500 m bandeira diferente** |
| 4.5 | teto expresso em lojas | proposta: teto conta **grupos econômicos** (D-00) |
| 4.5 | "a 2ª loja" deve ser popular | proposta: a exigência recai sobre o **2º grupo** (D-00) |
| 4.5 | faixas com limites sobrepostos (60, 120, 200 mil) | cortes fechados em 60.000 / 120.000 / 200.000 |

**Sequência correta, e ela não é a deste rascunho:** aprovação da liderança →
correção da 4.5/6.1 → este documento publicado como **anexo operacional** dessas
páginas. Publicado antes, ele se torna uma fonte paralela que se declara mais
correta que a página oficial.

**Falta nomear quem é dono da 4.5 e da 6.1** — sem isso não há a quem submeter.

---

## 8. Pré-requisitos e impactos fora do escopo pedido

1. **Geocodificação dos endereços do cadastro — agora dos dois.** 34% das lojas
   já não tinham coordenada utilizável considerando um único endereço; com
   Receita e popular, a cobertura precisa ser medida e resolvida **nos dois
   campos**, e a do endereço popular tende a ser pior, porque nunca foi usada
   para nada. Enquanto não houver cobertura, travar dos dois lados endurece a
   regra só onde há dado — o que é desigual entre pedidos equivalentes
   (RN-DADO-02). É **pré-requisito de cronograma**, não backlog.
2. **Campos novos no Radar** (identificador de grupo econômico, responsável,
   status, bandeira, modelo de negócio e as duas coordenadas). Sem eles o gate não
   roda as regras que barram.
3. **Qualidade de cadastro vira caminho crítico.** Com o teto contando grupos, o
   cadastro de grupo econômico passa a barrar pedidos; e com a dupla coordenada,
   um endereço popular errado endurece a regra contra um ponto que não existe
   (RN-DADO-05.1).
4. **Contratos e análises passam a ter efeito de bloqueio.** Quem cadastra
   contrato e quem conclui análise precisa saber disso **antes** de o gate entrar
   no ar — inclusive para distratos e cancelamentos, que precisam chegar ao
   Órbita.
5. **Dossiê de região.** A skill de análise corta a faixa pelo Censo 2022;
   mantida a base interna no produto, os dois divergem perto dos cortes (D-08).

## 9. Métrica de sucesso (a definir antes de ligar)

O documento não tem argumento de ROI enquanto não houver linha de base:

- minutos de analista por análise, hoje × depois;
- % de pedidos encerrados no gate, antes da análise de mercado;
- análises concluídas por mês;
- taxa de exceção por regra;
- taxa de impedimento revertido por erro de cadastro.

Sem isso, o documento será aprovado ou rejeitado por opinião.
