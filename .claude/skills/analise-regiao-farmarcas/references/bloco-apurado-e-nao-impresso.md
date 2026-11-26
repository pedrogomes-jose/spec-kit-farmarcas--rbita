# Bloco apurado e não impresso — a falha que a conferência mecânica não pega

`verificar_dossie.py` confere **procedência**: todo número da narrativa tem um
valor apurado que o explica. Ela não confere **completude**: um bloco que o
script devolveu certo e o gerador não imprimiu passa limpo pelas seis seções da
conferência, porque nenhum número errado foi afirmado — simplesmente faltou um.

Auditoria de 2026-11-23, sobre o ponto da Av. Goiás 1997, em Gurupi/TO,
encontrou seis casos desta família numa só rodada. Todos passaram na conferência
mecânica. Dois deles faziam o relatório se contradizer dentro da mesma tela.

## A regra que sai daqui

**Bloco que o script devolve existe para ser impresso.** Se o gerador decide não
imprimir, a decisão fica escrita no código, com o motivo — não acontece por
omissão. E **contagem e detalhe da mesma coisa saem juntos**: contagem sozinha é
afirmação sem qualificação, e o leitor não tem o JSON para completar.

## Os quatro modos de errar, com o caso de cada um

### 1. Contagem sem o campo que muda a leitura dela

`lojas_farmarcas_no_raio` devolvia `total: 2` e, em `itens`, as duas com
`status: "Desativado"` e `ocupa_vaga_de_zoneamento: false`. O card imprimia só a
contagem — e "2 lojas da rede a 121 m e 154 m" lido isolado é canibalização com
loja própria, que é exatamente a distinção que a regra de perfil do solicitante
decide. Com o status, é ponto vago no quarteirão.

→ Card de contagem de loja **sempre** quebra por status.

### 0. A suspeita usada como se fosse fato — a raiz de vários dos outros

`_bases.py` e `references/bases-orbita.md` já diziam, desde 2026-10-27, que o
nome de bandeira na camada Concorrentes **vale como suspeita, nunca como fato**,
e que loja nossa sai do cadastro por CNPJ. O código não seguia: o split entre
concorrente e loja nossa era `B.eh_farmarcas(pdv)`, puro nome.

O nome erra nos **dois** sentidos, e cada um apareceu numa rodada real:

| Praça | O que o nome fez | Efeito no dossiê |
|---|---|---|
| Gurupi/TO, 2026-11-23 | tirou da contagem 2 lojas que o cadastro confirma como nossas (desativadas) | acertou por sorte — o CNPJ concorda |
| Lontras/SC, 2026-11-24 | tirou "SUPER POPULAR" a 250 m, que **não** está no cadastro e não tem loja da bandeira em SC | concorrente real fora da contagem, da régua de canal e do mercado somado |

O critério que resolve os dois é um só e já estava escrito: **entra como
concorrente tudo que o cadastro não confirma como nosso, por CNPJ**. Com ele, em
Lontras o anel de 300 m foi de 3 para 4 concorrentes e o mercado de
R$ 271.879,56 para R$ 421.509,59; em Gurupi nada se moveu, porque lá os dois
casamentos por nome são confirmados por documento.

Duas armadilhas de implementação:

- **CNPJ não casa como texto.** O cadastro grava com zero à esquerda
  (`02513661000146`) e a camada Concorrentes sem (`2513661000146`). Comparar cru
  faz a mesma loja parecer duas, e é provavelmente o motivo de o casamento por
  documento nunca ter substituído o casamento por nome. `B.so_digitos` normaliza.
- **A definição mora em `_bases`, não em cada script.** Enquanto
  `raio_concorrencia.py` filtrava por nome e `faturamento_canal.py` não filtrava
  nada, os dois respondiam "quanto o anel movimenta" com números diferentes —
  R$ 3.963.678,60 com 13 lojas contra R$ 4.316.619,50 com 15 em Gurupi — e a
  skill mandava rodar os dois sem dizer qual valia. Com `B.cnpjs_do_cadastro`
  nos dois, as saídas coincidem nas duas praças.

### 1b. Valor fora de faixa publicado como medida

A coluna `Lixo%` da camada de estrutura e saneamento devolveu **231,7073** para
os setores do raio de Lontras, num campo de fração — água veio 0,9667 e esgoto
1,0 na mesma linha. `raio_setores.py` agora recusa publicar fração fora de
[0, 1]: o campo sai `None`, a lacuna é declarada com a unidade a conferir na
origem, e **o valor bruto fica em `campos_fora_de_faixa`**, para que a ressalva
continue tendo procedência conferível.

Nota sobre o que esse caso NÃO era: o gerador nunca renderizou `saneamento`, e o
`231,7` que aparecia no HTML era a narrativa declarando a corrupção — o
comportamento desejado. O risco real era outro: o valor estava na apuração, e um
dossiê que o afirmasse como medida **passaria** na conferência, porque ele tinha
procedência. Checagem de plausibilidade é coisa do script; procedência não
substitui faixa.

### 2. Dois recortes diferentes para a mesma pergunta, na mesma tela

`venda_mensal_por_faixa` somava `dentro + nossas` — as lojas do raio mais as que
casaram por nome de bandeira Farmarcas. O card logo acima, "Vendas totais no
raio", usa `concorrentes.fat_medio_somado_R$`, que é só `dentro`. A tabela
tabulava 9 lojas classificadas e o card dizia 7, a um palmo de distância.

→ Tabela e card que respondem à mesma pergunta usam o **mesmo recorte**, e a
coluna declara qual é ("Concorrentes no raio", não "Lojas no raio"). Loja nossa
não é concorrente — e a regra da casa já dizia que loja nossa é a do cadastro,
não a que casa por nome de bandeira.

### 3. Lacuna que o script reporta e o HTML não imprime

`qualidade_do_dado.implausiveis` marca o registro cadastrado em cidade que o
raio não alcança. Em Gurupi, 1 dos 13 concorrentes do anel de 300 m estava
cadastrado em Ibotirama/BA — e entrava na contagem de capa, entre as 6
independentes e na soma de R$ 3,96 milhões por mês da régua de canal. O gerador
lia `lacunas` do mesmo script e nunca este bloco.

→ Ressalva de **erro provável no dado impresso** não vai para a seção recolhida
de lacunas: fica ao lado do número que ela ressalva. Lacuna é o que não se sabe;
isto é defeito conhecido do registro que está na tela.

### 4. Filtro do script e número publicado medindo coisas diferentes

O card "Lazer Culto" contava 2 equipamentos em 500 m e nomeava, como exemplo,
um a 513 m. Não era bug de renderização: o `around:` do Overpass aceita o objeto
cuja **geometria** encosta no círculo, e `out center` devolve o **centroide**,
que num polígono grande (praça, estádio, quadra de prédios) cai bem mais longe.
O script aceitava o que o Overpass filtrou e publicava a distância do centroide.

→ O corte é refeito contra **a distância que o script publica**, senão contagem
e distância da mesma linha não conferem entre si. O que sai pelo corte é
declarado (`fora_do_raio_pelo_centroide`), não sumido.

### 5. O gerador afirma a EXPLICAÇÃO quando só mediu o fato

`alternativas.py` montava, para cada praça com receita da rede em queda,
"ATENÇÃO: a receita Farmarcas caiu aqui — **praça possivelmente já testada**", e
o gerador repetia o rótulo na tabela. Três linhas acima, o mesmo laço declara:
*"Frase montada a partir dos próprios números — é recomposição, não
interpretação. Nenhum juízo entra aqui."*

O que a base mede é a **queda**. "Praça já testada e perdida" é uma das causas
possíveis dela, e o acervo não tem como separá-la de "loja ficou e encolheu" —
não há histórico de entrada e saída de associado por praça. Pior: `_limites.carteira`
diz que a base da IQVIA é a **carteira atual com histórico retroagido**, de modo
que associado que saiu não aparece como queda, e sim some da série inteira. Pela
própria construção da base, a leitura afirmada era a menos provável das duas.

Medido em Amélia Rodrigues/BA, 2026-11-25: as três regiões de Salvador em
retração (Itapoã-1, Vitória, Plataforma) não tiveram saída de associado nenhuma.
A narrativa teve de escrever um parágrafo avisando que **a própria tabela
enganava** quem lesse só ela — e isso resolve metade do problema, porque a tabela
continuava enganando. Documento que declara o defeito e o mantém na tela não
corrigiu nada; declarar não é consertar.

→ Rótulo de tabela diz o que foi **medido**. Quando duas causas incompatíveis
produzem o mesmo sinal, o gerador nomeia o sinal e diz que não separa as duas —
nunca escolhe uma. A régua: se a narrativa precisa desmentir a tabela, o defeito
é da tabela.

### 6. O texto fixo promete um elemento que o layout não tem

A abertura do formato de prospecção dizia "a coluna de presença mostra qual dos
dois", e a tabela tem cinco colunas, nenhuma delas de presença — o dado vive
numa `div.nota` dentro da célula de mercado. Texto fixo do gerador envelhece
quando o layout muda, e ninguém relê a prosa ao mexer numa coluna. Vale para
**todo** relatório gerado no formato, não para a rodada que o expôs.

→ Prosa fixa que descreve o layout é dívida. Quando puder, descreva o dado
("sob o mercado de cada linha vem…"), não o móvel onde ele está.

### 7. Seção de origem fechada, prosa que usa camada de fora

A seção Fontes do formato de prospecção tinha cinco `<li>` fixos e nenhum slot
para a narrativa. As cinco cobrem o que a **tabela** usa — e a prosa se apoia em
camada que a tabela não mostra: em Amélia Rodrigues, a captura do potencial de
consumo sustentou dois parágrafos inteiros e não tinha onde ser declarada.

→ `cfg["fontes"]` (opcional, texto solto ou `{titulo, fonte}`) entra **depois**
das fixas, que o modelo não reordena nem remove. Número afirmado no corpo sem
origem na seção que existe para dar origem é a lacuna mais cara de um formato,
porque ela se parece com rigor.

### 8. A base não duplica; quem duplica é a lista que a consulta

`closeup_utc_varejo` repete linha: a mesma UTC aparece duas ou três vezes no
mesmo município, com geometria diferente e `id_utc_var` igual. Dois dos três
leitores montam dicionário por id e a repetição some sozinha. O terceiro,
`mercado_utc.py`, montava **lista** — e o `somar()` percorria essa lista lendo
um bloco que fora juntado por id, de modo que o valor da UTC repetida entrava
uma vez por linha.

Medido em 2026-11-26, sobre o dump de 2026-10-26: **21 dos 5.570 municípios**,
35 linhas a mais, **R$ 7,49 bilhões** de receita fantasma somados.

| Município | antes | depois | fator |
|---|---|---|---|
| Carapicuíba/SP | R$ 791,8 mi | R$ 263,9 mi | **3,00×** |
| Santa Bárbara d'Oeste/SP · Camboriú/SC | | | 2,00× |
| Sorocaba/SP | R$ 1,584 bi | R$ 1,167 bi | 1,36× |
| São Paulo/SP | R$ 24,33 bi | R$ 21,77 bi | 1,12× |

E não parava na receita: `qtd_utcs` contava linhas, `precisao_geografica`
escrevia "o município tem 5 UTCs" onde havia 4, e em Carapicuíba o ramo
*"exata — o município tem uma única UTC"* era **inalcançável**, porque a única
UTC da cidade chegava como três.

O share saía **menor**, não maior, e a direção importa: a UTC repetida de
Sorocaba tem receita zero da rede, então só o denominador dobrava — 1,87%
contra 2,54% reais.

→ Duas lições, e a segunda custou três rodadas:

1. **Deduplicar na leitura, pela chave da base**, e declarar o que foi
   descartado (`linhas_repetidas_descartadas` + lacuna). Descarte silencioso
   trocaria um número errado por outro número sem rastro.
2. **"A base somada tem uma linha por id" não protege nada.** Essa foi a
   formulação que atrasou o conserto: ela é verdadeira e irrelevante, porque
   quem conta duas vezes é a coleção que consulta a base, não a base. Para
   conferir um efeito, leia **quem lê**, com que chave, e o que itera a soma —
   `len(lista)` e `len(set(ids))` respondem em uma linha.

### 9. Conceder também é afirmar

Este item não é de código. O caso acima levou três rodadas porque, das duas
sessões envolvidas, uma inventou o mecanismo, a outra o refutou com medida, e
então **concedeu** um "nada contado em dobro ali" depois de ler metade do
script — o bloco de receita municipal, que de fato não duplica, parando antes
do `somar()` trinta linhas abaixo.

Concordar sem medir tem o mesmo custo que afirmar sem medir, e é mais difícil
de pegar, porque ninguém audita uma concordância. Acertar as rodadas anteriores
aumenta o risco: a confiança acumulada é exatamente o que dispensa a conferência.

→ Antes de conceder "não é defeito", rode a medida que mostraria o defeito. Se
não houver uma, a resposta é "não medi", não "não é".

## Onde a ressalva é posta decide se ela sobrevive aos três modos

`--detalhes ocultos` não encolhe o documento por seção: ele apaga, do HTML
pronto, **todo `<p class="explica">`** e todo marcador `<sup class="ref">`, e
remove a seção Fontes. É cirúrgico e é cego — qualquer coisa escrita naquela
classe some do entregável que de fato circula, inclusive ressalva que não tem
nada de explicação de indicador.

Por isso o aviso de erro provável de cadastro (`bloco_implausiveis`) nasceu em
`div.alerta-dado`, e não em `p.explica`: escrito na outra classe, ele existiria
só na cópia de auditoria e faltaria justamente na versão que vai para o
solicitante. Mesma lógica vale para a nota de status do card de lojas, que vive
no corpo do card.

**Teste obrigatório para qualquer bloco novo de ressalva:** gerar nos três modos
e conferir que ele está nos três. Medido em 2026-11-23, sobre Gurupi, depois das
correções — card de lojas com status, lacuna de fluxo sem duplicata, lacuna da
camada de farmácias, aviso de implausíveis, contagem de POI e recorte da tabela
de faixas: idênticos em `abertos`, `recolhidos` e `ocultos`.

Duas coisas que **não** mudam com o modo, e que convém não confundir com ele:

- A seção "O que este dossiê NÃO sabe" fica inteira nos três modos — ela é
  `details.lacunas`, não `p.explica`. Lacuna que falta em `ocultos` falta nos
  três, e a causa é outra.
- Defeito de apuração (o corte de raio do POI, o recorte da tabela de faixas)
  nasce no script e é indiferente ao modo por construção. Procurá-lo "no modo
  certo" é perder tempo: ele está nos três ou em nenhum.

## O corte de lacunas em 6, e por que ele saiu

O gerador lia só os seis primeiros itens quando o bloco `lacunas` de um script
vinha em LISTA (`for item in lac[:6]`). Era a mesma família deste documento, na
sua forma mais traiçoeira: silenciava **por posição**, e nada no documento
dizia que algo tinha sumido.

O que a medição mostrou, sobre os 26 dossiês do repositório em 2026-11-24:

| | |
|---|---|
| Scripts com `lacunas` em lista | só `raio_setores.py`, `mercado_utc.py`, `contexto_municipio.py` |
| Maior lista já produzida | **exatamente 6** — Várzea Alegre/CE, uma linha por base de atributo sem registro no setor |
| Dossiês truncados até hoje | nenhum |

Duas conclusões, e a segunda é a que decidiu:

1. **Tirar o corte não muda nenhum dossiê existente.** O corte estava no teto,
   não acima dele. Verificado: Gurupi sai byte a byte idêntico, Várzea Alegre
   mantém 28 lacunas. Não era, portanto, decisão de volume — não havia volume
   a decidir.
2. **A checagem de fração fora de faixa acrescenta um SÉTIMO item** ao fim da
   lista de `raio_setores.py`. Numa praça como Várzea Alegre, que já ocupa as
   seis posições, a lacuna da fração corrompida seria a primeira a cair —
   justamente a que o script criou para não depender do bom senso do modelo.
   A correção de um defeito desta família tornava alcançável outro defeito da
   mesma família.

→ Lição de ordem geral: **cap silencioso em lista de lacuna é bug, não
formato.** Se algum dia a seção ficar longa demais, a saída é hierarquia visual
— ela já nasce recolhida, com contador no título —, nunca descartar item sem
avisar. E ao acrescentar item a uma lista que o gerador consome, confira o teto
de quem consome antes de assumir que ele cabe.

### Nota sobre o que o corte NUNCA escondeu

Os dois achados de Gurupi que o auditor pegou à mão — `camadas_indisponiveis_no_raio.farmacias`
e `qualidade_do_dado.implausiveis` — **não passavam por este corte**. O primeiro
vem do ramo DICT de `lacunas`, que nunca foi truncado; o segundo não está em
`lacunas` nenhuma, e é por isso que precisou do bloco próprio descrito acima.
Atribuir aqueles dois ao `lac[:6]` leva a procurar o defeito no lugar errado:
ramos diferentes do mesmo laço falham de maneiras diferentes.

## Deduplicação de lacuna: os dois lados do mesmo mecanismo

A mesma auditoria levantou duas queixas opostas sobre a dedup de lacunas, e as
duas vieram do mesmo ponto do código.

- **Duplicata que sobrou.** `fluxo_de_passantes` era a única chave sem entrada em
  `CONSEQUENCIA` e caía no ramo cru `"chave: valor"`. Saía como uma linha só, sem
  por que importa e sem o que destrava — contra a regra de que lacuna de uma
  linha não é acionável — e ao lado da versão escrita pelo modelo, que era
  completa. O tema cru tinha **uma palavra longa só** ("passantes"), e a dedup se
  abstém de temas de uma palavra de propósito. Explicada, a linha ganha
  vocabulário, a comparação de tema funciona e ela cede o lugar à escrita.
- **Supressão que estava certa.** A camada `farmacias` ("cadastro Receita/QSA")
  não saía no HTML, e isso foi relatado como lacuna omitida. Não era: o item 12
  do "O que este dossiê NÃO sabe" diz a mesma coisa, melhor, escrito pelo modelo.
  A dedup fez o trabalho dela. **Grep por string de motivo não prova omissão** —
  o motivo do script é a pior redação das duas, e a seção certa é a que o leitor
  vê, não a frase que o JSON guarda.

Entre as duas, a skill prefere duplicar a silenciar: lacuna silenciada vira
conclusão errada, lacuna repetida só cansa. Por isso a dedup exige tema de duas
palavras longas e 60% de coincidência, e não um prefixo.

## Unidade da regra no enunciado do alerta

`zoneamento.py` dizia, no alerta de densidade, "quantidade de lojas acima do que
a faixa de população dimensiona". A faixa dimensiona **grupos econômicos** — é o
que `_aplicada` declara e o que a regra refinada com o PM em 2026-10-29
estabelece. O alerta compara lojas contra um teto de grupos, e é justamente por
comparar unidades diferentes que ele é alerta e não impedimento.

O enunciado errado não muda o gate, e muda o dossiê: **o modelo escreve a
narrativa a partir do texto do script**. Em Gurupi, a lente de Dificuldades saiu
com "A praça passa a ter 4 lojas da rede para uma faixa que dimensiona 2" —
herdando a troca de unidade de quem a alimentou.

→ Texto de script é insumo de redação, não só log. Unidade errada ali reaparece
no entregável com a assinatura do modelo.

---

## Caso resolvido na origem: `--perfil-municipios`

`alternativas.py` é chamado por **três** formatos — dossiê completo, impedimento
e prospecção —, e só a prospecção imprime o perfil por cidade. Emitir o bloco
sempre criaria, de uma vez, dois casos da família que este documento descreve:
dois formatos recebendo apuração que ninguém renderiza.

A saída foi não produzir o bloco para quem não vai imprimi-lo. O perfil é
**opt-in**, por flag, e os dois pontos de chamada que não a passam carregam o
motivo escrito:

- **dossiê completo** — o ponto já tem percentis municipais próprios, vindos da
  apuração de contexto do município. Um painel das praças alternativas
  competiria com a análise do endereço que é o assunto do documento.
- **impedimento** — o formato é deliberadamente sem número de mercado do ponto
  barrado. Quatro dimensões de perfil ali se leem como análise de consolação, e
  a decisão de não as mostrar é consciente, não esquecimento.

A regra que fica: quando um bloco serve a um formato só, a correção é **não
emitir** para os outros, e não lembrar de não imprimir.

## Defeito desta família, encontrado por uso em 2026-11-25

A célula "Grupos/teto" da tabela de praças imprimia **"a cidade não tem teto"**
sempre que o teto vinha nulo. Mas nulo tinha dois significados — cidade acima da
faixa onde a regra impõe limite, ou população nunca apurada — e no segundo caso
a frase aparecia colada em "disponibilidade não apurada", na mesma célula.

Não era bloco apurado e não impresso: era bloco apurado e **traduzido errado**,
porque a renderização decidia pela nulidade de um campo em vez de pelo campo que
já carregava o motivo escrito. Variante da mesma família, e o teste é o mesmo:
*o que o script sabe chegou inteiro à tela, ou chegou a conclusão de quem
renderizou?*
