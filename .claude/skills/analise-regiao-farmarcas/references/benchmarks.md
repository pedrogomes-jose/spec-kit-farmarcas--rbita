# Benchmarks — contra o que comparar

> Número isolado não diz nada. "Renda de R$ 453" não é bom nem ruim; "renda no
> percentil 38 das cidades onde já analisamos" é uma frase acionável.

## A regra

Nenhum indicador aparece sozinho. Cada um vem com **um** referente, nesta ordem
de preferência:

1. **O município ou a UF** — quando a pergunta é "este bairro dentro desta
   cidade" (ex.: `ranking_bairros.RANKINGMUNICIPIO`).
2. **O percentil ou a mediana nacional da própria camada** — é o referente que
   transforma um número solto numa frase acionável.
3. **O período anterior do próprio indicador** — crescimento contra si mesmo.

O histórico de análises **não** é referente: ver a seção abaixo.

## Parecer por número — bom ou ruim contra o referente

Decisão do PM em 2026-11-27. O referente transformava o número numa frase
("percentil 28"), mas a frase ainda exigia do leitor saber se 28 é bom ou ruim
**naquele indicador** — e a resposta muda de um para outro: percentil 28 de
renda é ruim; num indicador em que menos é melhor, seria bom. É o conhecimento
prévio que o produto existe para tirar do analista.

Por isso todo número que tem referente sai com um **parecer**:

| Rótulo | Quando |
|---|---|
| **Bom** | o número está do lado favorável do referente, pela direção do indicador |
| **Na média** | percentil no terço do meio, ou em linha com o recorte comparado |
| **Ruim** | do lado desfavorável — possível dificuldade |
| **Ambíguo** | a casa não tem direção defensável para o indicador (ex.: captura do potencial, credenciamento ao Farmácia Popular, classes A/B, totais de porte) |
| **Sem referência** | não há referente coerente (ex.: contagem de concorrentes num raio, categoria do REGIC) |

**De onde vem o rótulo.** Da tabela de direção em `scripts/_parecer.py`: cada
indicador tem uma direção (mais é melhor, menos é melhor, ambíguo, ou que
depende do modelo da bandeira) e o motivo dela, apoiado nas lentes da casa e
nesta página. O corte por percentil é por **tercil da distribuição** — posição,
nunca valor absoluto. Contra um recorte da região (município, UF, anel maior),
vale a posição acima/abaixo. O rótulo é calculado pelo script; o modelo só diz
qual indicador e qual posição, e a conferência mecânica reprova rótulo que
contradiga a tabela.

**O que o parecer não pode virar** — e a conferência mecânica reprova:

- **soma, contagem, saldo ou maioria de pareceres** ("três indicadores bons",
  "saldo positivo", "a maioria dos indicadores é ruim"): é a nota reintroduzida
  por extenso;
- **score, nota ou recomendação**: a régua 0–20 continua com o produto;
- **ordenação de praças ou cidades**: o parecer compara um número com o seu
  referente, nunca uma cidade com a outra;
- **faixa absoluta**: nenhum "renda boa é acima de R$ X" — o corte é posição na
  distribuição ou no recorte comparado;
- **direção inventada**: indicador fora da tabela sai "Sem referência"; direção
  nova entra na tabela por decisão do PM, com o motivo escrito.

## Um dossiê não se apoia em outro

A tentação é grande justamente porque o analista anterior **é** o leitor: ele
lembra do ponto passado e a comparação parece informativa. Mas o relatório
circula, e quem recebe não tem o outro em mãos — a frase vira afirmação sem
referente verificável.

E há o problema de fundo: **dois casos não são uma distribuição**. Dizer que uma
praça tem "seis vezes o share da outra" não informa se 5,7% é muito ou pouco;
informa que dois números diferem. O referente que responde a pergunta é o
percentil, a mediana da base ou o histórico agregado — e esses estão todos
disponíveis.

## O histórico de análises não entra no dossiê

A base de análises da casa existe e é tentadora como referente — ela é a régua
tácita do time. **Ela não entra no relatório**, em forma nenhuma: nem contagem
de análises, nem "já analisamos aqui", nem resultado de análise anterior, nem
parecer.

Dois motivos somados. O primeiro é medido: parecer aprovado × reprovado **não
prediz** se a loja sobrevive (log-rank p = 0,8275 sobre 101 fechamentos), e
contra o próprio brick as reprovadas não ficaram atrás. Citar o histórico
sugere ao leitor um sinal que a própria Farmarcas já mediu não existir. O
segundo é de escopo: o dossiê descreve **a região**, não o que a casa já
decidiu sobre ela — quem lê precisa formar juízo sobre o ponto, não ancorar no
juízo anterior.

O que sobrou dessa base é **calibração interna da skill**, não conteúdo: é dela
que veio a decisão de rodar dois raios, 300 m e ~5 km, em vez de só o padrão do
produto. Essa decisão aparece no relatório como os dois raios comparados, nunca
como a sua procedência.

## O que NÃO é referência

| Não use | Por quê |
|---|---|
| **O histórico de análises** | o parecer não prediz desfecho, e o dossiê descreve a região e não as decisões anteriores sobre ela |
| **Outro dossiê já feito** | um dossiê é lido isolado, por quem pode nunca ter visto o outro. E dois pontos específicos não formam distribuição: "o dobro do ponto anterior" não diz se o número é alto ou baixo, só que é diferente de um caso. Vale para menção explícita e para eco ("ao contrário de um calçadão central") |
| **O Centro de Franca/SP como referência de comparação** | proibido por decisão do PM em 2026-10-27, em qualquer situação. Franca aparece nas referências apenas como **caso de erro de dado** (falso positivo de bandeira, cadastro em cidade errada, população do dump × Censo) — isso é evidência de defeito, não régua |
| Faixas absolutas de "renda boa" / "população suficiente" | um valor fixo escrito aqui seria conhecimento prévio cristalizado e envelheceria em silêncio. O juízo de bom/ruim é permitido (ver `## Parecer por número`), mas sempre por **posição** contra o referente — percentil ou recorte da região —, nunca contra um corte absoluto |
| O score 0–20 do produto | **o dossiê não pontua.** A régua tem dono (executivos) e vive no produto; reproduzi-la aqui cria dois números para a mesma pergunta. O parecer por número não é score: não se soma, não se conta e não recomenda |
| Porte do mercado local como previsor de faturamento | medido: correlação **−0,003** (p = 0,97) com o faturamento da loja |
| Média simples de qualquer série mensal da IQVIA | o dado mensal oscila mais de 5× em 36 de 182 lojas — só mediana e proporção |
| **As outras praças da mesma lista** | quatro ou doze casos não são uma distribuição. É o mesmo erro de "o dobro do ponto anterior", com mais linhas: comparar as cidades do painel entre si cria uma régua de qualidade que o dado não sustenta, e ordená-las por qualquer percentil é ranking com outro nome. O referente de cada indicador é o país |
| **Qualquer composição entre percentis** | média, soma ou contagem de "dimensões ganhas". Dentro de uma mesma dimensão os indicadores podem apontar em direções opostas — renda baixa com consumo de farmácia alto é um achado —, e compor apaga exatamente o que vale conversar. Vale para número e para texto: "lidera em três das quatro" é a composição escrita por extenso |

### Aplicação canônica do referente de percentil

O **perfil por cidade** da lista de praças é a forma que esta regra toma no
produto: cada indicador sai com o valor, o percentil na distribuição nacional
dos municípios brasileiros da própria camada, a mediana nacional, quantos
municípios entraram na comparação e o **parecer** daquele número (desde
2026-11-27). Nada mais — nenhum agregado entre eles.

Regra de corte que o acompanha: **só entra indicador per capita, percentual ou
razão**. Total absoluto — IPC, PIB total, potencial de consumo anual, população,
receita do município — é proxy de porte, e um painel com qualquer um deles
ordena as cidades por tamanho em todas as dimensões ao mesmo tempo. O leitor
conclui "a capital é melhor em tudo", que é a régua de qualidade entrando pela
porta dos fundos.
