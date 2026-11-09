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
| Faixas absolutas de "renda boa" / "população suficiente" | é exatamente o conhecimento prévio que a descoberta aponta como causa do problema (`orbita-descoberta-analise-pontos.md:34`) |
| O score 0–20 do produto | **o dossiê não pontua.** A régua tem dono (executivos) e vive no produto; reproduzi-la aqui cria dois números para a mesma pergunta |
| Porte do mercado local como previsor de faturamento | medido: correlação **−0,003** (p = 0,97) com o faturamento da loja |
| Média simples de qualquer série mensal da IQVIA | o dado mensal oscila mais de 5× em 36 de 182 lojas — só mediana e proporção |
