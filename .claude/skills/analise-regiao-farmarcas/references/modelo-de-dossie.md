# Modelo do dossiê

O entregável é um **relatório HTML**, no layout do relatório de viabilidade do
Órbita, gerado por `scripts/montar_relatorio.py` a partir de um JSON de
narrativa. Português do Brasil. O dossiê existe para poupar tempo do analista —
se ficar longo, falhou.

**Dois arquivos, mesmo nome, em `outputs/dossies/`:**

| Arquivo | O que é | Quem escreve |
|---|---|---|
| `<data>_<municipio>_<ref>.json` | narrativa: resumo, as 4 lentes, lacunas, campo | o modelo |
| `<data>_<municipio>_<ref>.html` | o relatório renderizado, com todos os números | o script |

Nunca editar o HTML à mão: ele é saída de script, e uma correção feita nele se
perde na próxima geração. Corrigir sempre no JSON.

**Ordem dos blocos no HTML** (espelha o relatório do produto, sem o score):
zoneamento + resumo → leitura da região → detalhes da região → contexto
macroeconômico **+ cidades que têm este município como polo** →
microterritório e concorrência → venda mensal por faixa → potencial de consumo
com split → **implantação do ponto** + geradores de fluxo → onde mais olhar →
o que NÃO sabe (**bloco recolhido**, com a contagem no título) → para confirmar
em campo (seção própria, visível) → **para conversar com o empresário** (seção
própria, visível) → **Fontes** (tabela numerada + procedência
geral) → rodapé.

**Três blocos são condicionais, e a condição é de confiança, não de espaço:**

| Bloco | Entra quando | Quando não entra |
|---|---|---|
| Preço médio no brick | houve casamento de brick para o ponto | **o card some.** Um card de destaque mostrando "—" com o preço da UF ao lado convida a ler o agregado estadual como se fosse o do ponto |
| Implantação (esquina, meio de quadra) | a geometria viária sustenta a classificação com confiança alta | **o assunto some do relatório inteiro** — não vira lacuna, não vira "não foi possível determinar". Saber que não se sabe a posição na quadra não muda decisão, e a linha rouba atenção das lacunas reais |
| Área de venda, aluguel comercial e custo de ocupação | o analista informou a régua de cada um — R$/m² de faturamento e aluguel pesquisado | **o card some, um a um.** Card de destaque existe para carregar número; três deles em sequência dizendo "—" gastam a faixa de maior atenção do relatório para informar que não há informação. Cada um volta inteiro no momento em que o valor é informado |

Isso é exceção deliberada à regra de declarar toda lacuna. A regra existe
porque lacuna silenciada vira conclusão errada — e nenhuma conclusão se apoia
em não saber se o ponto é esquina. Onde o silêncio engana, a lacuna fica.

**A leitura da região é texto corrido.** Cada lente tem uma `abertura` que liga
os achados e um parágrafo por item — não lista de bullets. Bullet empilha
afirmações soltas; parágrafo obriga a ligar uma à outra, que é como o analista
lê. Os três campos continuam obrigatórios dentro do parágrafo — número,
comparação e a fonte em campo próprio. **Não existe campo "muda a leitura se"**
e **não se escreve a nota de confiança**.

**A leitura da região sai em quadrante SWOT**, em ordem fixa: Forças e
Fragilidades em cima, Oportunidades e Dificuldades embaixo; a favor à esquerda,
contra à direita. Empilhadas em coluna, as quatro lentes viravam quatro blocos
de texto em sequência e o par de cada linha, que é o contraste que o leitor
precisa fazer, ficava separado por uma tela de rolagem. Quadrante sem item
continua desenhado, com a linha de ausência no lugar do texto.

**A confiança decide a entrada do item, e nunca vira texto.** Confiança alta ou
média entra na lente sem rótulo e sem a justificativa da nota; confiança baixa
ou nenhuma **não entra na lente** e vira lacuna, com as três perguntas
respondidas. O corte é por **afirmação**, não por item: num mesmo parágrafo, a
parte cadastral fica e o palpite sai. Nada é silenciado — o que sai da lente
aparece em "O que este dossiê NÃO sabe". Ver `lentes-do-dossie.md`.

**Toda fonte vai consolidada no fim, nenhuma no meio do texto.** Cada item
declara a sua no campo `fonte` do JSON; o relatório emite uma referência
numerada ao fim da frase e resolve todas na seção **Fontes**, que fecha o
documento com duas partes: a tabela numerada (referência → lente → afirmação →
fonte do dado) e a **procedência geral** (extrações, datas, instituições).

**A seção Fontes sai RECOLHIDA por padrão**, com a contagem de referências no
título e um clique para abrir — aberta por inteiro na impressão, como a de
lacunas. Ela é o lastro do dossiê: é por ela que alguém confere de onde veio
cada número. O que muda é o peso visual — quem lê para decidir não percorre uma
tabela de catorze referências e uma lista de procedência no fim do documento, e
aberta ela empurrava o resto para longe da vista.

O botão `--detalhes` tem um terceiro modo, `ocultos`, que tira a seção do
documento e, com ela, os marcadores de referência do texto — número órfão no
meio da frase seria pior que nenhum. Nesse modo o rodapé passa a carregar a
origem da coordenada e a data do acervo, que são o mínimo que não pode sumir.
**O dossiê gerado assim não permite conferir número nenhum**, então a cópia que
for para o auditor de evidência é gerada com `--detalhes abertos`.

O mesmo vale para os blocos que não são lentes: nota de card, parágrafo
explicativo e tabela não citam fonte no corpo — a origem deles está na
procedência geral.

**O corpo não fala de ferramenta.** O relatório é lido por analista e por
executivo de Expansão. Nome de script, flag de linha de comando e nome de
arquivo de base não dizem nada a eles — e sinalizam "saída de robô", bem onde o
problema a resolver é confiança no número.

Em cada item, o campo de fonte nomeia **de onde o dado vem**, não com o que foi
lido:

| Não escrever | Escrever |
|---|---|
| `Fonte: concorrentes_2025 via raio_concorrencia.py` | Fonte: camada Concorrentes 2025 |
| `Fonte: mercado_utc.py` | Fonte: base de crescimento por UTC da IQVIA |
| `lido com benchmark_historico.py --com-parecer` | com o parecer registrado em texto |
| `Fonte: regic_2018_municipio` | Fonte: REGIC 2018, do IBGE |
| `(do_solicitante: false)` | o cadastro registra outro responsável |

A ferramenta aparece em dois lugares, e só: o **rodapé**, que lista as origens
de dado e a data do dump, e os **arquivos de origem** (`.json` da narrativa e os
scripts). `montar_relatorio.py` tem um tradutor que converte o que escapar, mas
contar com ele deixa a frase torta — a narrativa já deve nascer no vocabulário
do negócio.

**Não existe box de comentário do analista.** O relatório é insumo para o
comentário da análise no Órbita, que é onde o analista escreve — reservar
espaço em branco aqui só duplica o lugar da anotação.

**Três blocos levam parágrafo explicativo antes dos números**, porque o número
sozinho engana quem não construiu o indicador: a renda (é mensal, é de quem
mora, e renda por habitante não é renda domiciliar), o potencial de consumo
(é demanda potencial, não venda; soma setor inteiro; periodicidade não
declarada) e os geradores de fluxo (por que cada categoria traz gente, e o que
a contagem não diz).

**Todo parágrafo explicativo sai RECOLHIDO por padrão**, com a primeira frase
dele como rótulo à vista e o texto a um clique — aberto na impressão, e fora do
documento com `--detalhes ocultos`. No relatório de impedimento eles nunca são
recolhidos: lá o parágrafo é o conteúdo, não o acompanhamento de um número. O
parágrafo
continua obrigatório: o que muda é que, somados, eles eram mais texto que os
números que explicam, e quem já conhece o indicador relia tudo a cada dossiê. O
rótulo que fica à vista carrega a ressalva em uma linha ("Estes três números
são rótulos de faixa, não faturamento de loja"), de modo que o leitor apressado
não perde o aviso que o parágrafo existe para dar.

Esses parágrafos são escritos **pelo gerador**, e é por isso que a lente não
explica método: o card "Método de rateio" já traz a cobertura do círculo e a
contagem de setores, e o parágrafo da renda já diz que cada setor entra pela
fração que cai dentro do círculo e que as taxas são média ponderada. Escrever
isso de novo no texto da lente duplica a explicação e empurra o número para o
fim do parágrafo. Ver `lentes-do-dossie.md`.

O esqueleto em markdown abaixo continua valendo como **conteúdo** de cada
item — é ele que vai para o JSON.

## Quando o zoneamento barra: dossiê de impedimento

Se o gate devolver `veredito: impedimento`, o entregável continua sendo **HTML
gerado por script** — a regra vale para os dois casos, e abrir exceção criaria um
segundo formato, escrito à mão, por onde volta exatamente o número que o modelo
formatou sozinho. O que muda é o **conteúdo**: nenhum script de mercado roda.

`montar_relatorio.py` reconhece o veredito sozinho e monta o relatório curto. A
escolha não é de quem escreve a narrativa: o script roda o gate, lê o veredito e
despacha. Se o JSON trouxer as quatro lentes num ponto barrado, elas são
ignoradas e o script avisa.

**Por que o relatório curto não leva mercado.** Gastar páginas de população,
renda e concorrência sobre um ponto que a regra barra diz ao leitor que há
número a negociar. Não há: o que existe para resolver é decisão de quem é dono
da regra. O relatório diz isso na abertura, e declara como lacuna que nenhuma
camada foi levantada — senão o silêncio é lido como ausência de problema nelas.

### O JSON da narrativa de impedimento

Mesmos campos de identificação do dossiê completo (`endereco`, `lat`, `lng`,
`codigo_ibge`, `municipio`, `uf`, `bandeira`, `modelo`, `perfil`), e no lugar de
`lentes`:

| Campo | O que leva |
|---|---|
| `resumo` | a frase única, factual — por que o ponto não passa |
| `leitura` | lista de **parágrafos**, não bullets: o impedimento explicado |
| `o_que_mudaria` | o que, se fosse outro, destravaria — cada um rotulado como regra ou como hipótese |
| `alertas_cadastro` | o que no cadastro pode estar errado e erraria o teto junto |
| `nao_sabe` | lacunas, as três perguntas respondidas em cada uma |
| `campo` | o que confirmar, e o que muda conforme a resposta |
| `provocacoes_empresario` | o que só o empresário sabe — sobre a loja que ocupa a vaga, o motivo do pedido, as praças onde a regra não barra. Mesmo formato do dossiê completo |

O script preenche sozinho, a partir do gate: população do Censo com a data de
extração, faixa aplicada, teto, as duas contagens, a tabela de lojas da cidade,
os alertas do gate e as lacunas dele.

### As duas contagens do teto se comparam sobre o PEDIDO

É o erro que o relatório existe para não cometer. Comparar o estado atual da
cidade ("1 loja e 1 empresário, empate") responde a pergunta errada. A pergunta
é se **esta loja cabe**: a loja pretendida sempre entra na contagem por lojas, e
só entra na contagem por empresários se o solicitante ainda **não** tiver loja
na cidade. Num pedido de segunda loja do mesmo associado numa cidade de teto 1,
as duas leituras divergem — e a leitura por empresários, que é a que a página
4.5 escreve, caberia. O relatório mostra as duas e **mantém** o impedimento pela
regra vigente, porque qual leitura vale não é decisão de quem analisa o ponto.

### Praças alternativas: a exceção que o impedimento TEM de trazer

O relatório curto não leva mercado **do ponto barrado** — e leva uma lista de
praças onde a regra não barra. Não é contradição, são perguntas diferentes:

| Pergunta | Entra no impedimento? | Por quê |
|---|---|---|
| Quanto vale o mercado **deste endereço**? | **Não** | sugere que há número a negociar num ponto que a regra barra |
| Onde a regra **não** barra? | **Sim** | não afirma nada sobre o endereço pedido, e é o único próximo passo que o analista tem |

Sem a segunda, o entregável devolve um "não" com quatro destravamentos, todos
sobre o mesmo ponto — e o empresário sai sem saber para onde olhar.

**Disponível conta grupos econômicos, nunca lojas**, e depende da bandeira
pretendida: na faixa de 60 a 120 mil o 2º grupo só entra com bandeira popular.
A apuração do grupo é por nome do responsável, não por CNPJ — declarado na própria
seção, porque é o que pode esconder uma praça que está disponível.

### O que o relatório de impedimento traz

Zoneamento + resumo → o ponto não passa (regra, constatado, as duas contagens) →
leitura do impedimento → lojas Farmarcas no município → o que mudaria o
resultado → **onde mais olhar (praças onde a regra não barra)** → alertas de
cadastro → o que esta checagem NÃO sabe (recolhido) → para confirmar em campo
(seção própria) → para conversar com o empresário (seção própria) → Fontes →
rodapé.

---

```markdown
# Dossiê de região — <endereço ou referência> · <Município>/<UF>

> Dados do dump do Órbita de <data>, sem atualização automática.
> Raios analisados: <300 m> e <5.000 m>. Este dossiê **não pontua** o ponto.
> **Solicitante:** <empresário novo | já associado>. **Bandeira:** <X>, <popular|convencional>.
> **Zoneamento:** <liberado | alerta> — <regra da faixa aplicada>.

## Em uma linha
<O que esta região é, em uma frase factual. Não é veredito.>

## Forças
- **<Indicador>: <número>** — <comparação>. Fonte: `<base>` (campo próprio).
  **Parecer:** <Bom | Na média | Ruim | Ambíguo | Sem referência> — <uma linha
  de porquê>. <Campo `parecer` do item; o rótulo sai do script.>
  <Sem nota de confiança e sem o motivo dela: confiança baixa ou nenhuma não
  chega até aqui, e confiança alta ou média não se anuncia.>

## Fragilidades
- (mesma anatomia)

## Oportunidades
- **<Alavanca disponível>** — <quem está deixando o espaço aberto, nomeado e
  contado> <+ o tamanho do espaço, com comparação>. Fonte: `<base>`.
  <Vantagem competitiva em aberto, nunca panorama favorável: se a frase continua
  verdadeira sem ninguém fazer nada, o item é Força. E nunca escrita como falta
  da rede — a lente é "a favor".>

## Dificuldades
- (mesma anatomia)

## O que este dossiê NÃO sabe
- **Fluxo de passantes** — não existe no produto nem no dump. Em rua comercial
  com poucos residentes, este dossiê subestima a região. <Sempre presente.>
- <Tudo que ficou de fora das lentes por confiança baixa ou nenhuma, com o que
  falta, por que importa neste ponto e o que destravaria.>
- <O limite de método dos itens de confiança média que entraram nas lentes.>
- <Lacunas devolvidas pelos scripts, uma a uma, com o que destravaria cada uma.>

## Para confirmar em campo
- <No máximo 5 itens, cada um ligado a um item acima.>

## Para conversar com o empresário
1. **<A pergunta, curta, para ser dita em voz alta>** <tema: camada ou lente>
   <O achado: o número apurado que motiva a pergunta.>
   O que a resposta muda: <a leitura que depende dela.>
<De 10 a 15 itens, teto de 15. O que o analista provavelmente não sabe e o
empresário sabe: história da praça, concorrência vista de dentro, intenção,
apetite. Sem nome de pessoa.>

## Procedência
| Afirmação | Script | Base | Data do dump |
|---|---|---|---|
```

---

## Regras de redação

- **Abre pelo que o analista não sabia.** Se as Forças forem óbvias para quem
  conhece a cidade, elas não abrem o dossiê.
- **Número sem comparação não entra.** "R$ 453,17" não; "percentil 38" sim.
- **A ressalva obrigatória vai no substantivo, não em frase ao fim.** "A faixa
  mediana ocupada é R$ 330.312", "a loja média do canal independente fatura
  R$ 69.439". A explicação da base — que o campo é rótulo de faixa, que a régua
  é média da UF, que o potencial não é venda realizada — já sai por extenso no
  bloco do relatório onde o número aparece; repetida na lente, só empurra o
  achado para o fim do parágrafo.
- **A palavra "confiança" não aparece na leitura da região.** Nem o rótulo, nem
  o motivo dele, nem a versão disfarçada ("o dado é robusto", "com alguma
  ressalva", "nem todas as lojas têm o campo preenchido"). Se é preciso
  ressalvar, ou a afirmação não entra, ou a ressalva é lacuna.
- **A comparação nunca é outro dossiê.** Cada relatório é autossuficiente:
  percentil, mediana da base, histórico agregado ou o próprio município. Nem
  menção explícita a outra análise, nem eco dela.
- **Lacuna e item de campo são explicados**, não listados: o que falta, por que
  importa neste ponto, e o que destravaria. Uma linha solta não é acionável.
- **Lacuna é item de primeira classe.** A seção "O que este dossiê NÃO sabe"
  nunca é omitida nem resumida a "dados limitados". Ela sai **recolhida** no
  HTML — fechada por padrão, contagem no título, um clique para abrir, e aberta
  por inteiro na impressão. Isso muda o peso **visual** da seção, não o rigor
  dela: o texto de cada lacuna continua respondendo o que falta, por que importa
  neste ponto e o que destravaria. "Para confirmar em campo" fica **fora** do
  bloco recolhido, em seção própria, porque é ação do analista e não lacuna.
- **Nunca usar o vocabulário da decisão** — "recomendado", "aprovado",
  "viável", "score", "nota". Essas palavras pertencem ao comitê e ao produto.
- **Todo número com referente leva parecer — e o parecer é por número.**
  "Bom", "Na média", "Ruim" (possível dificuldade), "Ambíguo" e "Sem
  referência" são o vocabulário permitido (decisão do PM em 2026-11-27), pela
  tabela de direção de `scripts/_parecer.py`. Nunca somados, contados ou
  usados para ordenar: "três indicadores bons" é nota. Ver `benchmarks.md`,
  `## Parecer por número`.
- **"Para conversar com o empresário" é roteiro, não questionário.** De 10 a
  15 perguntas, cada uma partindo de um número do documento, escritas para o
  analista dizer em voz alta. Passam pelo **teste do respondente**: se o
  analista provavelmente não sabe e o empresário sabe, a pergunta é daqui; se
  o analista sabe, ela foi feita na conversa; se é produto de etapa de campo,
  é item de campo.
- **Nenhum nome de pessoa.** Nem de empresário, nem de consultor, nem de
  analista — nem quando aparecem no parecer histórico.
- **Divergência entre fontes é achado, não ruído.** Se `concorrentes_2025` e o
  CNES discordam, isso vira um item, com os dois números.
- **Nunca chamar de "loja nossa" o que só casou por nome de bandeira.** Ou está
  no cadastro com CNPJ, ou é "suspeita a confirmar".
- **Separar canibalização própria de canibalização de terceiro.** São itens
  diferentes: um é custo de estratégia, outro é conflito entre associados.

## Onde o dossiê termina

Ele é insumo para o comentário da análise no Órbita **e o roteiro da conversa
do analista com o empresário** — decisão do PM em 2026-11-27, que reverte a
regra de que ele não ia ao empresário. O analista apresenta o documento (a
cópia enxuta), e a seção "Para conversar com o empresário" existe para essa
reunião. Não substitui o parecer do analista, não leva nome de pessoa, e não
entra em apresentação executiva sem o analista ter lido.
