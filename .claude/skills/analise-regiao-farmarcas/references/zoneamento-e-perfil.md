# Zoneamento e perfil do solicitante

Duas coisas que mudam o dossiê antes de qualquer número de mercado:
**quem está pedindo** e **se a regra de zoneamento deixa abrir**.

---

## 1. O perfil do solicitante é pergunta obrigatória

Se não estiver dito na solicitação, **perguntar**. Não assumir.

| Perfil | O que muda |
|---|---|
| **Empresário novo** | Nenhuma sobreposição é estratégica para ele. Toda loja Farmarcas próxima é de terceiro — e é exatamente o conflito que a regra de expansão existe para evitar ("evitar conflito e concorrência desleal entre associados", página 6.1). |
| **Empresário que já opera loja(s) Farmarcas** | Sobreposição com loja **dele mesmo** pode ser decisão deliberada: fechar mercado, tirar espaço do concorrente, ganhar share e poder de negociação na compra. Nesse caso "canibalização" não é defeito do ponto — é o preço de uma estratégia que ele escolheu. O dossiê descreve o efeito e deixa a escolha com ele. |

**A distinção que importa no texto:** separar sempre

- sobreposição com loja **do próprio solicitante** → efeito econômico a dimensionar;
- sobreposição com loja **de outro associado** → conflito de interesse entre associados.

São itens diferentes da lente Dificuldades. Juntá-los apaga a diferença que decide.

**O que o perfil NÃO muda:** o zoneamento. O teto de lojas por cidade conta
lojas, de quem quer que sejam (decisão do PM, 2026-10-27). Empresário existente
não ganha vaga extra por já ser da casa.

---

## 2. A regra de zoneamento (gate, não indicador)

Fonte: Confluence **"4.5 Regras de Zoneamento e Regras de Expansão"**
(espaço Gestão Farmarcas, página 3755245621, v5 de 2026-02-24) e
**"6.1 Regras de Expansão"** (3755769865, v8).

> Objetivo declarado: *"Garantir a perenidade e expansão saudável das lojas
> Farmarcas"*; *"Evita a canibalização entre lojas pertencentes a Farmarcas"*.
> A página 6.1 diz que a consulta acontece **antes de prosseguir** com a
> análise — por isso aqui o zoneamento é **gate**, e roda antes do mercado.

### Faixas por população

| População (Censo 2022) | Teto de lojas na cidade | Condições |
|---|---|---|
| ≤ 60.000 | **1** | sem expansão adicional |
| 60.001 – 120.000 | **2** | a 2ª deve ser de bandeira **popular** |
| 120.001 – 200.000 | **3** | alternância de bandeiras |
| > 200.000 | **sem teto** | ocupação decidida por market share |

### Distância mínima entre lojas Farmarcas

| Caso | Mínimo |
|---|---|
| **Mesma bandeira** | **300 m** |
| **Bandeira diferente** | **500 m** |

> ⚠️ **A página 4.5 está desatualizada neste ponto.** Ela escreve apenas
> "raio 300m". A regra vigente — 300 m mesma bandeira / 500 m outra bandeira —
> foi confirmada com o PM em 2026-10-27. **Vale corrigir a página.**

---

## 3. O que a regra oficial NÃO diz (e foi decidido fora dela)

Tudo aqui é premissa declarada. Nenhuma é invenção silenciosa, e todas saem
no bloco `lacunas` do script.

| Ponto em aberto | O que o script faz | Status |
|---|---|---|
| **Qual população corta a faixa** | usa o **Censo 2022 do IBGE** via API pública | decidido pelo PM em 2026-10-27 |
| **Teto conta lojas ou empresários?** | conta **lojas** | decidido pelo PM; a página escreve "empresários" |
| **Loja desativada ocupa vaga?** | **não** — ocupam vaga apenas `Ativado`, `Montando`, `Transição` | premissa, não está na regra |
| **Limites de faixa são sobrepostos** na página (60, 120, 200 mil) | corta em `≤60.000`, `≤120.000`, `≤200.000` | premissa |
| **Distância vale acima de 200 mil?** | calcula e levanta **alerta**, não impedimento | a página não declara |
| **Alternância de bandeiras é obrigatória?** | **alerta**, não impedimento | a página não declara |
| **Como popular e convencional diferem** | só aplica a exigência explícita da faixa 60–120 mil | a página diz que diferem, sem detalhar |

### Por que a população importa tanto

O dump do Órbita e o Censo 2022 **não dão o mesmo número** — Franca: 366.566
contra 352.536, +4,0% (verificado na API do IBGE). Perto dos cortes de 60, 120
e 200 mil, essa diferença **troca a faixa e o teto de lojas**. Por isso a faixa
é cortada pelo Censo, e o dossiê diz qual número usou.

---

## 4. Fonte de verdade: o cadastro de lojas, não o nome da bandeira

**Nunca** decidir que uma loja é nossa pelo nome da bandeira dentro da camada
`Concorrentes`. Caso real verificado em 2026-10-27:

> "FCIA FARMAVALE", a 112 m do centro de Franca/SP, casa com a bandeira
> Farmavale e **não existe no cadastro de lojas**. A única loja Farmarcas
> cadastrada em Franca é uma Ultra Popular **desativada**, a 4.784 m.

O match por nome vale como **suspeita a confirmar por CNPJ** — e é assim que
`raio_concorrencia.py` devolve, em bloco separado.

### O cadastro também erra

Uma loja cadastrada em **Patrocínio Paulista/SP** tem coordenada a **342 m do
centro de Franca** — cidades a ~25 km uma da outra. Como o teto de zoneamento é
contado **por cidade cadastrada**, um cadastro errado erra o teto junto.

Por isso `zoneamento.py` procura lojas por **coordenada** além do nome da
cidade, e levanta alerta quando acha loja próxima cadastrada em outra cidade.

**Cobertura:** só **1.841 das 2.804 lojas (66%)** têm coordenada utilizável —
931 estão vazias e 32 caem fora do Brasil. Para o terço restante não há como
checar distância mínima, e isso é lacuna declarada, não ausência de risco.

---

## 5. Como o gate termina

| Veredito | O que o dossiê faz |
|---|---|
| **impedimento** | **Para.** Abre com o impedimento, a regra citada e os números que a sustentam. Não gasta análise de mercado num ponto que a regra barra. |
| **alerta** | Segue o dossiê completo, com o alerta em destaque antes das lentes. |
| **liberado** | Segue o dossiê completo; registra na procedência que o gate passou. |
| **indeterminado** | Sem população do Censo não há faixa. Resolver antes de seguir. |
