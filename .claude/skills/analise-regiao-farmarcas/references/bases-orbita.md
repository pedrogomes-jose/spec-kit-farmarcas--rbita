# Bases do Órbita — o que existe mesmo no dump

Dump local: `C:\Users\zequi\Downloads\bases órbita` (sobrescreva com a variável
de ambiente `ORBITA_BASES`). **57 arquivos, ~500 MB, extraídos em 2026-10-26.**

> O dump é **estático**. Não há rotina de atualização. Todo dossiê carimba a
> data e diz que o dado não se atualiza sozinho.

## A limitação que organiza tudo

O export achatou a coluna `geometry` para o **tipo** (`"Point"`, `"Polygon"`).
Os polígonos e as coordenadas das camadas de desenho ficaram nos assets em
`radar.farmarcas.com.br/orbita-assets/...`, fora do dump.

Consequência prática, por classe de base:

| Pergunta | Dá para responder hoje? |
|---|---|
| Como é o município / o bairro? | ✅ sim, direto |
| Quais concorrentes estão no raio? | ✅ sim — `concorrentes_2025` tem `LAT`/`LONG` |
| Tem loja Farmarcas no raio? | ✅ sim — pela bandeira dentro de `concorrentes_2025` |
| Como vai o mercado farmacêutico aqui? | ⚠️ por **UTC**, resolvida a partir do município |
| Quantos moram no raio? Qual a renda no raio? | ❌ **não** — exige a malha do IBGE (Fase 2) |
| Qual o share no **brick** IQVIA deste ponto? | ❌ **não** — brick sem polígono, e `mat_atual_brick_*` só traz o número |
| Qual o fluxo de passantes? | ❌ **não existe**, nem no dump nem no produto |

## Camadas municipais — chave `CODIGO` (IBGE 7 dígitos)

Carregadas por `scripts/contexto_municipio.py`.

| Base | Responde |
|---|---|
| `populacao_municipios` | população total e por gênero |
| `densidade_demografica` | hab/km², área, taxa de crescimento (cobertura parcial) |
| `situacao_territorio_municipio` | % urbana × rural, distância da capital |
| `renda_media_municipio` | renda domiciliar per capita |
| `pib` | PIB total, PIB per capita, consumo per capita urbano/rural |
| `ranking_de_consumo` | IPC e posição estadual/nacional |
| `firjan_ifdm_geral` | IFDM e componentes (educação, emprego & renda, saúde) |
| `indice_de_educacao` | % alfabetizada |
| `empresas_totais`, `empresas_por_segmento_de_atuacao` | tecido empresarial |
| `movimentacao_economica` | variação de empregos por setor (chave `cod_MMMM`) |
| `piramide_etaria_municipios` | faixas etárias por gênero |
| `potencial_de_consumo` | potencial urbano/rural, anual e mensal, por classe |
| `dados_farmacia_popular` | **total de farmácias na cidade**, credenciadas ao Farmácia Popular, **lojas Farmarcas credenciadas**, gastos em medicamentos, distribuição A/B1/B2/C1/C2/D-E |
| `regic_2018_municipio` | hierarquia na rede urbana, nº de municípios influenciados, texto de perfil |
| `municipios` | nome, UF, área — usada para resolver nome → código IBGE |

## Camadas de bairro

| Base | Chave | Observação |
|---|---|---|
| `bairros` | `CODIGO` | tem `Lat_C`/`Lon_C` (centroide) — único polígono com ponto aproveitável |
| `populacao_bairros_2025` | `CODIGO` | população, alfabetização, urbano × rural |
| `ranking_bairros` | `CODBAIRRO` | **IPC do bairro** e ranking dentro do município |
| `situacao_do_territorio` | `CODIGO` | % rural/urbana por bairro |

## Camada de ponto — a única com coordenada

`concorrentes_2025` — **100.612 registros, 100% com `LAT`/`LONG`.**

Campos que importam: `MDM-PDV` (nome da rede), `MDM-ClassifdoPDV`
(INDEPENDENTE, FRANQUIA, ASSOCIAÇÃO, rede nomeada), `fatMedio` (faturamento
médio estimado do PDV), `CNPJ`, `ENDERECO`, `BAIRRO`, `SITUACAO`.

Duas armadilhas:
- **vírgula decimal** nas coordenadas (`"-15,84696100000"`);
- valores `{"error":"#N/A"}` em vários campos — valem como **ausente**, nunca zero.

**Canibalização:** bandeiras Farmarcas aparecem dentro desta camada (ex.:
`DROGARIAS ULTRA POPULAR`, 271 registros). É o comportamento já documentado em
`docs/confluence/2025/evolucao-camadas/orbita-evolucao-camadas.md:12`. O script
separa loja nossa de concorrente pela lista de bandeiras em `_bases.py`.

## Mercado farmacêutico — IQVIA / CloseUp

| Base | Chave | Responde |
|---|---|---|
| `closeup_utc_varejo` | `codigo_mun` → `id_utc_var` | ponte município → UTC |
| `mat_atual_utc_market_share` | `utc_id_varejo` | share Farmarcas na UTC |
| `mat_anterior_x_atual_utc_crescimento` | `utc_id_varejo` | crescimento **nosso vs. do mercado sem nós** |
| `mat_anterior_x_atual_utc_sem_cobertura` | `utc_id_varejo` | PDVs abertos/fechados, receita do mercado |
| `mat_anterior_x_atual_utc_mix_categorias` | `utc_id_varejo` | % e crescimento por categoria |
| `mat_atual_utc_bandeira`, `mat_atual_utc_grupo` | `utc_id_varejo` | bandeiras presentes, mix genérico/similar/propagado |
| `faturamento_lojas_municipio_closeup` | `codigoibge` | receita do município, anterior × atual |
| `mat_atual_brick_*`, `bricks_iqvia`, `bricks_2024` | `Brick` | ⚠️ **inalcançável a partir de um ponto** |

**Precisão da UTC:** 5.378 dos 5.570 municípios têm **uma única UTC** — nesses,
município → UTC é exato. São Paulo tem 84. Nas cidades grandes o número é o
agregado do município, e o script diz isso na saída.

### A régua de canal — a segunda via do faturamento do concorrente

A planilha `Faturamento IQVIA ... Detalhado por CNPJ, BRICK e UTC` tem duas abas
que as demais bases do dump não cobrem, e que `preparar_iqvia_canal.py` extrai:

| Aba | Granularidade | Traz |
|---|---|---|
| `DADOS POR CANAL - CPP` | canal × bandeira × **UF**, visão MAT | receita (`soma_cpp`) e unidades |
| `DADOS POR CANAL - PDV` | canal × bandeira × **UF**, visão YTD | quantidade de PDVs |

Os seis canais são ABRAFARMA, OUTRAS REDES CORPORATIVAS, GRUPO FARMARCAS,
FEBRAFAR, ASSOCIACOES + FRANQUIAS e INDEPENDENTES. As 27 UFs estão presentes nas
duas abas, e os seis canais aparecem em todas elas.

    R$ por loja/mês = receita MAT do canal na UF ÷ PDVs do canal na UF ÷ 12

Por que isso importa: `MDM-ClassifdoPDV`, na camada Concorrentes, classifica cada
loja num rótulo que mapeia para esses canais — 85% dos 100.612 registros caem em
quatro rótulos genéricos (`INDEPENDENTE`, `ASSOCIAÇÃO,`, `FRANQUIA`,
`OUTRAS REDES`), e o resto nomeia redes. Então **toda loja do raio ganha um
faturamento de referência medido**, inclusive as que têm o campo `fatMedio`
vazio — que são mais da metade.

**Duas ressalvas que não podem sumir do texto.** A receita é MAT (12 meses) e a
contagem de PDVs é YTD (ano corrente): janelas diferentes, viés em canal que
abriu ou fechou muita loja. E a base não traz dispersão **dentro** do canal — só
a média — então o número dimensiona mercado, nunca afirma o faturamento de um
endereço.

**A aba `RESULTADOS POR BRICK` não substitui isso:** ela registra, no próprio
rodapé, que *a IQVIA não disponibiliza quantidade de PDVs por brick na visão de
canais*. Por isso a régua é por UF, não por brick. E `mat_atual_qtd_pdvs` tem
coluna `Concorrente`, mas ela é **zero em todos os 2.087 bricks** — essa base
conta só PDVs Farmarcas.

**Aferição feita (2026-10-27).** Aplicando a régua às 47 farmácias cadastradas em
São Gonçalo do Amarante/RN, o mercado bottom-up dá R$ 32,0 milhões ao ano (43
lojas com canal) contra R$ 42,5 milhões medidos no total do município pela via
independente da UTC. Os dois caminhos ficam dentro de ~25% um do outro, na
direção esperada: a camada de concorrentes subconta lojas e quatro ficaram sem
canal. Serve de teste de sanidade, não de calibração.

## Histórico Farmarcas

| Base | Conteúdo |
|---|---|
| `all_expansion.analysis_data` | **6.946 análises**, 2.940 com coordenada, com `map.radius`, `map.sources[].name` (camadas usadas), `analysisSituationDescription` e o **parecer em texto** em `comment[n].text` |
| `contratos_expansao` | 497 contratos, 377 com coordenada, com raio e camadas usadas |
| `relatorio-lojas-23_10_2026.xlsx` | cadastro de lojas (requer `openpyxl`) |

**LGPD:** estas bases têm nome e e-mail de consultor, analista e empresário.
Os scripts descartam esses campos. O parecer em texto só sai com
`--com-parecer`, e **nunca** entra no dossiê com nome de pessoa.

## Cadastro de lojas — a fonte de verdade de "loja nossa"

`relatorio-lojas-23_10_2026_15_10_24.xlsx`, **2.804 lojas**. Convertido uma vez
para CSV por `scripts/preparar_cadastro_lojas.py`, porque `openpyxl` não existe
sob `python -I`, que é como os scripts de análise rodam.

| Campo | Valores |
|---|---|
| `Status` | Ativado 1.811 · Desativado 870 · Montando 122 · Transição 1 |
| `Modelo de Negócio` | **Popular 2.307 · Convencional 492** — é a distinção que a regra de zoneamento usa |
| `Bandeira` | Ultra Popular 1.868 · Conectadas 212 · Maxi Popular 195 · Entrefarma 140 · Bigfort 112 · AC Farma 96 · Super Popular 51 · Farmavale 42 · Maisfarma 29 · Mega Popular 24 · Farma100 15 · Maestra 14 · Mega Pharma 1 |
| `Nome do responsável pelo GE` | **694 grupos distintos** — é o "empresário" da regra |
| Coordenada | **1.841 utilizáveis de 2.804 (66%)** — 931 vazias, 32 fora do Brasil |
| Cidades | 1.095 |

É esta base, e não o nome de bandeira dentro de `concorrentes_2025`, que
decide se uma loja é da Farmarcas. Ver a seção de verificações abaixo.

## Camadas que existem no dump mas NÃO servem no raio

Sem coordenada própria: `farmacias` (cadastro Receita/QSA, só endereço),
`farmacias_populares_2025`, `bancos`, `clinicas_oftalmologicas`,
`barreiras_geograficas`, `setor_censitario` e todas as bases setoriais
(`renda_media`, `potencial_de_consumo_setor_censitario`,
`classe_economica_dos_domicilios`, `indice_de_verticalizacao`,
`estrutura_saneamento`, `perfil_area`, `populacao_por_genero`,
`densidade_demografica_do_setor_habkm`).

As setoriais **voltam a funcionar na Fase 2**, juntando por `Cod_setor` /
`CD_GEOCODI` com a malha de setores do IBGE (gratuita).
`farmacias` se resolve na Fase 3, via **CNES** (traz CNPJ e coordenada).

## Encoding

30 arquivos em UTF-8, 27 em cp1252 — no **mesmo** dump. `_bases.py` detecta por
arquivo. Nunca assumir um só.

## Verificações feitas contra fonte externa (2026-10-26)

> Os exemplos abaixo usam Franca/SP porque foi lá que os defeitos apareceram.
> São **casos de erro de dado**, não referência de comparação — Franca não
> serve de benchmark em nenhuma situação (ver `benchmarks.md`).

Rodadas na construção da skill. Repetir quando o dump for atualizado.

### A população do dump NÃO é o Censo 2022

| Fonte | Franca/SP |
|---|---|
| `populacao_municipios` (dump) | **366.566** |
| IBGE, Censo 2022 (agregado 4714, var 93) | 352.536 |
| IBGE, estimativa 2025 (agregado 6579) | 365.494 |

Diferença de **+4,0%** contra o censo. O valor do dump é compatível com uma
**estimativa/projeção recente**, não com o censo — e o **ano de referência não
está declarado em lugar nenhum da base**.

→ No dossiê, population do dump se escreve como "estimativa IBGE, ano de
referência não declarado no dump", nunca como "Censo 2022".

### 3,7% das coordenadas de `concorrentes_2025` são sujas

**3.700 de 100.594** registros caem fora do bounding box do Brasil
(lat −34 a +6, lng −74 a −35) — a mesma validação que o produto implementou
depois de ter o mapa quebrado por dado de Excel
(`documentacao-tecnica/entendimento-indicadores-analises.md:92`).

`_bases.coordenada_valida()` descarta esses registros, e `raio_concorrencia.py`
reporta quantos foram descartados.

### Bandeira na camada Concorrentes NÃO prova que a loja é nossa

"FCIA FARMAVALE", a 112 m do centro de Franca/SP, casa com a bandeira Farmavale
e **não existe no cadastro de lojas**. A única loja Farmarcas cadastrada em
Franca é uma Ultra Popular **desativada**, a 4.784 m.

→ Canibalização sai do cadastro (CNPJ + coordenada). O match por nome volta em
bloco separado, rotulado `suspeitas_por_nome_de_bandeira`.

### O próprio cadastro de lojas erra de cidade

Uma loja cadastrada em **Patrocínio Paulista/SP** tem coordenada a **342 m do
centro de Franca/SP** — cidades a ~25 km. Como o teto de zoneamento é contado
por cidade cadastrada, cadastro errado erra o teto junto. Por isso
`zoneamento.py` procura loja por coordenada além do nome da cidade.

### Cidade do cadastro diverge da geografia

Num raio de 2 km do centro de Franca/SP apareceram registros cadastrados em
Orlândia/SP, Cássia/MG e **Grão Mogol/MG** (a ~700 km). Um deles é loja
Farmarcas (bandeira Farmavale) a **112 m** do ponto.

→ `raio_concorrencia.py` devolve esses casos no bloco `qualidade_do_dado`. São
**achado do dossiê**, não ruído a filtrar: ou a coordenada está errada, ou o
cadastro está — e nos dois casos o analista precisa saber.
