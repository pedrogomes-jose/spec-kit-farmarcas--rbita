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
macroeconômico → microterritório e concorrência → venda mensal por faixa →
potencial de consumo com split → geradores de fluxo → onde mais olhar → o que
NÃO sabe → **Fontes** (tabela numerada + procedência geral) → rodapé.

**A leitura da região é texto corrido.** Cada lente tem uma `abertura` que liga
os achados e um parágrafo por item — não lista de bullets. Bullet empilha
afirmações soltas; parágrafo obriga a ligar uma à outra, que é como o analista
lê. Os quatro campos continuam obrigatórios dentro do parágrafo, e a ressalva vem explicada no texto — **não existe campo "muda a leitura se"**.

**Toda fonte vai consolidada no fim, nenhuma no meio do texto.** Cada item
declara a sua no campo `fonte` do JSON; o relatório emite uma referência
numerada ao fim da frase e resolve todas na seção **Fontes**, que fecha o
documento com duas partes: a tabela numerada (referência → lente → afirmação →
fonte do dado) e a **procedência geral** (extrações, datas, instituições).

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

O esqueleto em markdown abaixo continua valendo como **conteúdo** de cada
item — é ele que vai para o JSON.

## Quando o zoneamento barra: dossiê de impedimento

Se `zoneamento.py` devolver `veredito: impedimento`, o entregável é **curto** e
não leva análise de mercado. Gastar páginas de mercado num ponto barrado dá ao
leitor a impressão de que há o que negociar.

```markdown
# Impedimento de zoneamento — <endereço> · <Município>/<UF>

> Checado em <data>, contra as regras de expansão vigentes.

## O ponto não passa no zoneamento
- **Regra:** <texto da faixa, citado>
- **Constatado:** <número de lojas × teto, ou distância × mínimo>
- **População usada:** <N> (IBGE, Censo 2022) — é ela que corta a faixa
- **Perfil do solicitante:** <novo | já associado>

## Lojas Farmarcas na cidade
<tabela: bandeira, modelo, status, distância, do solicitante ou de outro associado>

## O que mudaria o resultado
- <premissa que, se outra, destravaria — ex.: loja desativada que volte a contar>

## Alertas de cadastro
- <loja próxima cadastrada em outra cidade, loja sem coordenada>

## Fonte da regra
Confluence 4.5 (3755245621) e 6.1 (3755769865) · cadastro de lojas de <data>
```

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
- **<Indicador>: <número>** — <comparação>. Fonte: `<base>` via `<script>`.
  Confiança <alta/média/baixa>: <motivo>. <O que mudaria a leitura.>

## Fragilidades
- (mesma anatomia)

## Oportunidades
- (mesma anatomia)

## Dificuldades
- (mesma anatomia)

## O que este dossiê NÃO sabe
- **Fluxo de passantes** — não existe no produto nem no dump. Em rua comercial
  com poucos residentes, este dossiê subestima a região. <Sempre presente.>
- <Lacunas devolvidas pelos scripts, uma a uma, com o que destravaria cada uma.>

## Para confirmar em campo
- <No máximo 5 itens, cada um ligado a um item acima.>

## Procedência
| Afirmação | Script | Base | Data do dump |
|---|---|---|---|
```

---

## Regras de redação

- **Abre pelo que o analista não sabia.** Se as Forças forem óbvias para quem
  conhece a cidade, elas não abrem o dossiê.
- **Número sem comparação não entra.** "R$ 453,17" não; "percentil 38" sim.
- **A comparação nunca é outro dossiê.** Cada relatório é autossuficiente:
  percentil, mediana da base, histórico agregado ou o próprio município. Nem
  menção explícita a outra análise, nem eco dela.
- **Lacuna e item de campo são explicados**, não listados: o que falta, por que
  importa neste ponto, e o que destravaria. Uma linha solta não é acionável.
- **Lacuna é item de primeira classe**, com o mesmo destaque de um achado. A
  seção "O que este dossiê NÃO sabe" nunca é omitida nem resumida a "dados
  limitados".
- **Nunca usar o vocabulário da decisão** — "recomendado", "aprovado",
  "viável", "score", "nota". Essas palavras pertencem ao comitê e ao produto.
- **Nenhum nome de pessoa.** Nem de empresário, nem de consultor, nem de
  analista — nem quando aparecem no parecer histórico.
- **Divergência entre fontes é achado, não ruído.** Se `concorrentes_2025` e o
  CNES discordam, isso vira um item, com os dois números.
- **Nunca chamar de "loja nossa" o que só casou por nome de bandeira.** Ou está
  no cadastro com CNPJ, ou é "suspeita a confirmar".
- **Separar canibalização própria de canibalização de terceiro.** São itens
  diferentes: um é custo de estratégia, outro é conflito entre associados.

## Onde o dossiê termina

Ele é insumo para o comentário da análise no Órbita. Não substitui o parecer do
analista, não vai para o empresário, e não entra em apresentação executiva sem
o analista ter lido.
