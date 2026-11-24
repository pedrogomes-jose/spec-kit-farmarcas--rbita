# Zoneamento no Órbita — decisões para a liderança

**Para:** donos das regras de expansão (Confluence 4.5 e 6.1) · **De:** Produto — Órbita · **Data:** 2026-11-17
**Anexo:** documento completo de regras de negócio (15 páginas)

Hoje a consulta de zoneamento é manual e depende de o analista saber que ela existe, onde consultar e como
contar. O Órbita passa a rodá-la automaticamente antes da análise de mercado e devolver um veredito
auditável. **Cinco decisões abaixo são de política de expansão, não de construção de sistema: elas mudam
quantos pedidos são barrados.** Sem dono para cada uma, a página não deve ser publicada.

## As cinco decisões

| # | Decisão | Recomendação | Se não for decidida |
|---|---|---|---|
| 1 | O teto conta **grupos econômicos** ou **lojas**? | grupos, com a ressalva ao lado | gate exibe as duas contagens e não barra por nenhuma |
| 2 | Fonte da população que corta a faixa | Censo/estimativa IBGE, pública e datada | base interna, sem ano de referência declarado |
| 3 | Contrato e análise aprovada **bloqueiam** ou **alertam**? | contrato bloqueia; análise alerta | análise antiga de terceiro barra pedido novo |
| 4 | Alçada e escopo da exceção — e se o associado vizinho é ouvido | alçada de diretoria; distância contra terceiro não é excepcionável só internamente | exceção vira override livre e o gate perde função |
| 5 | Distância mínima vale abaixo de 60 mil habitantes? | sim, avaliar em toda faixa | faixa de maior volume sai sem veredito |

## O que muda no negócio

**Afrouxa de um lado.** Contando grupos econômicos em vez de lojas, os municípios acima do teto caem de
**207 de 830 (25%) para 34 (4%)** — medido no estoque de lojas, com um endereço por loja; números a
remedir com a dupla coordenada. E o solicitante que já opera na cidade deixa de ser barrado pelo teto.
Efeito a aprovar conscientemente: **quem chega primeiro numa cidade pequena pode abrir várias lojas e
fechar o município para qualquer grupo novo.**

**Aperta do outro.** Contratos e análises de ponto, que hoje são histórico, passam a barrar pedidos. E a
distância mínima passa a ser checada contra **os dois endereços de cada loja** — o da Receita e o popular,
que divergem com frequência —, o que torna a regra mais dura. Efeito já aceito pela área de negócio.

**O número que falta.** Quantos pedidos dos últimos 12 meses mudariam de veredito com a nova regra — isso
não foi medido, e é o número que esta decisão deveria ter. Ver recomendação.

## Riscos

| Agir | Não agir |
|---|---|
| Impedimento falso por erro de grafia no cadastro do grupo econômico | A regra segue dependendo de quem analisa, aplicada de forma diferente por pessoa, sem rastro |
| Atrito com associado barrado por reserva antiga de terceiro, que não pode ser detalhada (LGPD) | A página 4.5 já diverge da prática em quatro pontos — e ninguém tem o registro de quem decidiu o quê |
| Distância não checável em 34% da base, por falta de coordenada | Cada caso continua escalando para a diretoria, um a um |

## Recomendação: ligar em modo observação por 60–90 dias

O gate roda, calcula e registra o veredito — **e não bloqueia nada.** Mede, sobre o fluxo real: quantos
pedidos mudariam de resultado, quantos impedimentos seriam falsos por cadastro, quantas exceções seriam
pedidas e contra qual regra. A liderança decide ligar o bloqueio com dado do próprio fluxo, em vez de
projeção sobre o estoque — e as decisões 1, 3 e 5 ficam muito mais fáceis de tomar.

## Pré-requisitos

**Campos novos no Radar**, atualizados em D-1: identificador de grupo econômico e responsável, status,
bandeira, modelo de negócio e **as coordenadas dos dois endereços — o da Receita e o popular**. Sem eles o
gate não roda as regras que barram. **Geocodificação dos dois endereços** — hoje 34% das lojas não têm
coordenada utilizável considerando um só endereço, e a cobertura do endereço popular tende a ser pior,
porque nunca foi usada para nada.

## O que se pede nesta reunião

Aprovar o **modo observação** e **nomear uma pessoa responsável e uma data** para cada uma das cinco
decisões acima. As demais pendências do documento completo (15 ao todo) não bloqueiam este passo.
