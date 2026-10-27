# Benchmarks — contra o que comparar

> Número isolado não diz nada. "Renda de R$ 453" não é bom nem ruim; "renda no
> percentil 38 das cidades onde já analisamos" é uma frase acionável.

## A regra

Nenhum indicador aparece sozinho. Cada um vem com **um** referente, nesta ordem
de preferência:

1. **O histórico de análises da Farmarcas** — 6.946 análises em
   `all_expansion.analysis_data`. É a régua tácita do time.
2. **O município ou a UF** — quando a pergunta é "este bairro dentro desta
   cidade" (ex.: `ranking_bairros.RANKINGMUNICIPIO`).
3. **A mediana nacional da própria base** — quando não há recorte melhor.

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

## O que o histórico já respondeu

Rodando `benchmark_historico.py --panorama` sobre o dump de 2026-10-26:

| Fato | Valor | Por que importa |
|---|---|---|
| Análises na base | 6.946 (2.940 com coordenada) | universo do benchmark |
| Situação | 2.257 Reprovado · 1.865 Aprovado · 2.330 Mapeamento | reprovar é o desfecho mais comum |
| **Raio mediano usado** | **5.500 m** (min 300, max 6.800) | o padrão de 300 m do produto **não é** a prática |
| Camadas mais abertas | Municípios · Setor censitário · Potencial de Consumo · Concorrentes · Renda Média · Densidade do Setor · Região de Influência · **Lojas Farmarcas** | é a régua tácita: o que o time olha de verdade |

Duas leituras diretas:
- **Dossiê com raio de 300 m responde outra pergunta** que a do analista.
  Rodar pelo menos dois raios (300 m e ~5 km) e mostrar os dois.
- **"Lojas Farmarcas" está no top-8 de camadas usadas** e **não entra no score
  do produto**. A lente Dificuldades existe por causa disso.

## Vizinhança como contexto, nunca como prognóstico

`benchmark_historico.py --lat --lng --vizinhanca` lista as análises já feitas
perto do ponto, com situação e, sob `--com-parecer`, o texto do parecer.

Isso é **memória institucional**: "a 800 m daqui reprovou-se em 2024, pelo
motivo X". É contexto para o analista confirmar ou contestar.

**Não é previsão.** O estudo em `C:\Users\zequi\projetos\analise-ponto-orbita`
mediu: parecer aprovado × reprovado **não prediz** se a loja sobrevive
(log-rank p = 0,8275 sobre 101 fechamentos), e contra o próprio brick as
reprovadas **não ficaram atrás**. Escrever "reprovaram aqui, logo é ruim" é
contrariar a evidência que a própria Farmarcas produziu.

## O que NÃO é referência

| Não use | Por quê |
|---|---|
| **Outro dossiê já feito** | um dossiê é lido isolado, por quem pode nunca ter visto o outro. E dois pontos específicos não formam distribuição: "o dobro do ponto anterior" não diz se o número é alto ou baixo, só que é diferente de um caso. Vale para menção explícita e para eco ("ao contrário de um calçadão central") |
| **O Centro de Franca/SP como referência de comparação** | proibido por decisão do PM em 2026-10-27, em qualquer situação. Franca aparece nas referências apenas como **caso de erro de dado** (falso positivo de bandeira, cadastro em cidade errada, população do dump × Censo) — isso é evidência de defeito, não régua |
| Faixas absolutas de "renda boa" / "população suficiente" | é exatamente o conhecimento prévio que a descoberta aponta como causa do problema (`orbita-descoberta-analise-pontos.md:34`) |
| O score 0–20 do produto | **o dossiê não pontua.** A régua tem dono (executivos) e vive no produto; reproduzi-la aqui cria dois números para a mesma pergunta |
| Porte do mercado local como previsor de faturamento | medido: correlação **−0,003** (p = 0,97) com o faturamento da loja |
| Média simples de qualquer série mensal da IQVIA | o dado mensal oscila mais de 5× em 36 de 182 lojas — só mediana e proporção |
