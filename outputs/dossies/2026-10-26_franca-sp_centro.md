# Dossiê de região — Centro (Av. Major Claudiano) · Franca/SP

> Dados do dump do Órbita de **2026-10-26** (cadastro de lojas de 2026-10-23),
> sem atualização automática. Coordenada: −20,5386 / −47,4006.
> Raios analisados: **300 m** e **5.000 m**. Este dossiê **não pontua** o ponto.
>
> **Solicitante:** não informado. Não altera este dossiê, porque não há loja
> Farmarcas ativa em Franca para canibalizar; alteraria a leitura se houvesse.
> **Bandeira usada na checagem:** Ultra Popular, modelo popular — é ela que
> define o mínimo de 300 m (mesma bandeira) contra 500 m (outra).
> **Zoneamento:** alerta, não impedimento. Franca tem **352.536 habitantes**
> (IBGE, Censo 2022), faixa *acima de 200 mil → sem teto de lojas, ocupação por
> market share*. Zero lojas Farmarcas ocupando vaga.
>
> Revisado por `(⌕) auditor-de-evidencia` em 2026-10-27.

## Em uma linha

Centro de uma Capital Regional de 352 mil habitantes, num mercado farmacêutico
de R$ 541,8 milhões ao ano de onde a Farmarcas **saiu** — duas lojas
desativadas e receita que foi de R$ 806 mil a zero.

---

## Forças

- **Capital Regional C, polo de 8 municípios.** A cidade atrai consumo de fora e
  vincula-se à metrópole de São Paulo. Comparação: a maioria dos municípios
  brasileiros é Centro Local, sem atração regional.
  Fonte: `regic_2018_municipio` via `contexto_municipio.py`. Confiança **alta**.
  Muda a leitura se: a REGIC é de 2018 e o papel da cidade pode ter mudado.

- **IPC no percentil 99 — 66º do Brasil.** Índice de potencial de consumo
  0,21104. Comparação: percentil 99 entre os 5.571 municípios da base.
  Fonte: `ranking_de_consumo` via `contexto_municipio.py`, bloco `percentis`.
  Confiança **alta**. Muda a leitura se: o IPC é municipal — não diz nada sobre
  este ponto dentro da cidade.

- **Duas fontes independentes concordam no tamanho do mercado.** Gasto em
  medicamentos na cidade: **R$ 580,1 milhões**. Comparação: a IQVIA mede
  R$ 541,8 milhões de receita nas três UTCs — 7% de diferença entre bases que
  não conversam.
  Fonte: `dados_farmacia_popular.GastosemMEDICAMENTOS` via
  `contexto_municipio.py`; `mercado_utc.py`. Confiança **média**: ano de
  referência do gasto não declarado no dump. Muda a leitura se: os dois forem
  de anos diferentes.

- **O zoneamento não barra.** Acima de 200 mil habitantes não há teto de lojas,
  e não há loja Farmarcas ativa disputando distância mínima. Comparação: em
  cidade de até 60 mil, uma única loja já fecharia a praça.
  Fonte: `zoneamento.py`, regra 4.5 do Confluence. Confiança **alta**.
  Muda a leitura se: a loja desativada a 342 m voltar a operar — pela premissa
  adotada, desativada não ocupa vaga, e essa premissa não está na regra oficial.

## Fragilidades

- **Saturação na média do país.** 1.490,1 habitantes por farmácia usando a
  população do dump (percentil 50, mediana nacional 1.492,6); **1.433,1 usando
  o Censo 2022** (percentil 46). Comparação: nos dois cortes, Franca é mercado
  nem desabastecido nem sobre-ofertado.
  Fonte: `contexto_municipio.py`, bloco `saturacao` — distribuição montada com a
  população do dump para os 5.541 municípios. Confiança **média**: o numerador
  muda conforme a população escolhida; a distribuição, não.
  Muda a leitura se: a contagem de 246 farmácias na cidade estiver desatualizada.

- **9 concorrentes em 300 m, 156 em 5 km.** Dentro de 300 m: Droga Raia,
  Drogasil e Drogão Super. Em 5 km somam-se Drogaria São Paulo (3) e Pague
  Menos (2). Comparação: quatro redes nacionais na área de influência.
  Fonte: `concorrentes_2025` via `raio_concorrencia.py`. Confiança **alta** para
  a contagem. Muda a leitura se: 3.700 registros da base foram descartados por
  coordenada inválida — alguns podiam ser daqui.

- **R$ 25,46 milhões de faturamento somado entre os concorrentes do raio de
  5 km** — cobrindo apenas **85 dos 156** estabelecimentos. Comparação: é piso,
  não total; 71 PDVs não têm o campo preenchido.
  Fonte: `concorrentes_2025.fatMedio` via `raio_concorrencia.py`.
  Confiança **baixa** como total, **alta** como piso. Muda a leitura se: os 71
  faltantes forem sistematicamente maiores ou menores que os 85 medidos.

- **Renda exatamente na mediana nacional: R$ 453,17 per capita domiciliar**,
  percentil 50 entre 5.565 municípios (mediana R$ 456,30). Comparação: 69,6% dos
  domicílios são C1, C2 ou D/E; A + B1 somam 9,3%.
  Fonte: `renda_media_municipio` e `dados_farmacia_popular` via
  `contexto_municipio.py`, bloco `percentis`. Confiança **média**: ano de
  referência não declarado. Muda a leitura se: a renda do bairro do ponto
  divergir da média da cidade — e isso é lacuna da Fase 2.

## Oportunidades

- **Receita Farmarcas = 0 num mercado de R$ 541,8 milhões.** Comparação: o
  mercado cresceu **18,5%** no município no período MAT 202505 → 202605
  (R$ 457,3 mi → R$ 541,8 mi), sem nenhuma receita nossa dentro.
  Fonte: `mercado_utc.py`, bloco `mercado_municipio_somado_utcs`.
  Confiança **média**: o share **não foi medido** — as três UTCs de Franca estão
  ausentes de `mat_atual_utc_market_share`, e o zero é inferido da receita.
  Muda a leitura se: a base da IQVIA é a carteira atual, e quem saiu foi apagado
  para trás — ver a lente Dificuldades.

- **Nenhuma loja Farmarcas credenciada ao Farmácia Popular**, numa cidade onde
  89 das 246 farmácias (36,2%) são credenciadas. Comparação: o credenciamento é
  padrão de mercado aqui, e a rede está fora dele.
  Fonte: `dados_farmacia_popular.lojasFARMARCAScredenciadas` = 0 via
  `contexto_municipio.py`. Confiança **alta**. Muda a leitura se: o
  credenciamento mudou após o dump.

- **A UTC São Joaquim cresce 27%**, com R$ 128,4 milhões de receita atual.
  Comparação: 27% contra 18,5% do município — a maior das três UTCs (as outras:
  20,4% e 7%).
  Fonte: `mat_anterior_x_atual_utc_crescimento` via `mercado_utc.py`.
  Confiança **média**. Muda a leitura se: o dump não diz em qual das três UTCs
  este ponto cai.

## Dificuldades

- **A Farmarcas já esteve em Franca e saiu, com receita medida.** Na UTC Vila
  Chico Julio a receita Farmarcas foi de **R$ 806.050,09 para zero**, e a UTC
  registra `delta_pdvs = −1`: perdeu o único PDV enquanto o mercado ao redor
  crescia 7%. Comparação: as outras duas UTCs já tinham receita nossa zero antes.
  Fonte: `mercado_utc.py`. Confiança **alta**. Muda a leitura se: **por que
  fechou** — é a pergunta mais importante deste dossiê, e ele não a responde.

- **As duas lojas do grupo no raio de 5 km estão desativadas.** Uma a 4.784 m,
  cadastrada em Franca; outra a **342 m**, cadastrada em **Patrocínio
  Paulista/SP** — cidade a ~25 km. Ambas Ultra Popular, modelo Popular.
  Comparação: pelo cadastro, Franca tem 1 loja (desativada); pela geografia, são
  2 lojas desativadas perto do ponto.
  Fonte: `zoneamento.py` (`lojas_desativadas_na_cidade`,
  `lojas_proximas_cadastradas_em_outra_cidade`) e `raio_concorrencia.py`.
  Confiança **alta** de que há erro de cadastro; nenhuma de qual campo errou.
  Muda a leitura se: numa cidade abaixo de 200 mil, esse erro mudaria o teto de
  zoneamento aplicado.

- **Quatro concorrentes no raio de 5 km estão cadastrados em outra cidade:**
  FARMA TOTAL (Orlândia/SP, 723 m), DROGARIA VIDA FARMA (Cássia/MG, 1.723 m),
  DROGAFARMA PEDREGULHO 2 (Pedregulho/SP, 4.387 m) e FCIA FARMAVALE (Grão
  Mogol/MG, **112 m** — a ~700 km). Comparação: 4 de 156 registros do raio.
  Fonte: `raio_concorrencia.py`, bloco `qualidade_do_dado`. Confiança **alta**:
  ou a coordenada está errada, ou o cadastro está. Muda a leitura se: a FCIA
  FARMAVALE, a mais próxima, casa com bandeira do grupo — tratada abaixo como
  suspeita não confirmada, **não** como loja nossa.

- **Quase nenhuma memória institucional aqui.** Em 5 km há **uma** análise
  registrada: julho/2022, situação "Mapeamento Receptivo", raio 6.600 m, a 57 m
  do ponto. Comparação: nenhuma aprovada, nenhuma reprovada.
  Fonte: `all_expansion.analysis_data` via `benchmark_historico.py`.
  Confiança **alta** para a contagem. Muda a leitura se: nada — **não é
  prognóstico**; o parecer histórico não prediz desfecho de loja.

---

## O que este dossiê NÃO sabe

- **Fluxo de passantes.** Não existe no dump nem no produto. Em região central
  de comércio, este dossiê **subestima** o ponto. Nada aqui compensa isso.
  Destravaria: fonte de mobilidade (ver `estrategista-fontes-dados`).

- **Share Farmarcas medido por UTC.** As três UTCs de Franca estão **ausentes**
  de `mat_atual_utc_market_share`. O zero deste dossiê é **inferido** da receita,
  e share ausente não é share zero.

- **Por que as duas lojas Farmarcas fecharam.** O cadastro dá o status, não o
  motivo. Sem isso, a receita zero pode ser praça aberta ou praça já perdida — e
  as duas leituras levam a decisões opostas.

- **O efeito da carteira atual da IQVIA.** A base reflete quem está na rede hoje,
  com histórico retroagido. A queda de R$ 806 mil a zero pode ser saída real ou
  artefato dessa reconstrução.

- **Nada por setor censitário dentro do raio** — renda, classe econômica,
  potencial de consumo em drogarias, verticalização, saneamento, população.
  O export achatou a geometria. Destravaria: malha de setores do IBGE (Fase 2).

- **Em qual das 3 UTCs o ponto cai**, e o share por **brick** IQVIA, que o dump
  não permite alcançar (`bricks_iqvia` veio sem polígono).

- **Densidade demográfica do município** — Franca está ausente da base
  `densidade_demografica`.

- **A população do dump não é o Censo 2022.** O dump diz 366.566; o Censo diz
  352.536 (API do IBGE, consultada em 2026-10-26). Diferença de +4,0%, ano de
  referência do dump não declarado. A saturação acima é dada nas duas bases
  justamente por isso.

- **"FCIA FARMAVALE" a 112 m não foi confirmada.** O nome casa com bandeira do
  grupo, mas o CNPJ não está no cadastro de lojas. Destravaria: conferência do
  CNPJ.

- **Premissa de status:** só `Ativado`, `Montando` e `Transição` ocupam vaga de
  zoneamento. Desativada não ocupa — **premissa, não está na regra oficial**. É
  ela que sustenta "zero lojas ocupando vaga" e a não-checagem da distância de
  342 m.

- **Cobertura de coordenada:** **931 das 2.804 lojas (33%)** do cadastro não têm
  coordenada preenchida, e outras **32** têm coordenada fora do Brasil — 963
  (34,3%) inutilizáveis para checagem de distância. Em `concorrentes_2025`,
  **3.700 de 100.612 registros (3,7%)** foram descartados pelo mesmo motivo.

## Para confirmar em campo

1. **Por que as duas lojas Farmarcas de Franca fecharam** — decide se a receita
   zero é oportunidade ou praça perdida.
2. O CNPJ da "FCIA FARMAVALE" a 112 m — é loja do grupo ou homônimo?
3. A loja desativada a 342 m: fica em Franca ou em Patrocínio Paulista?
4. Contagem de fluxo de pedestres em dia útil e sábado — é o dado que falta.
5. Os quatro concorrentes cadastrados em outra cidade: coordenada ou cadastro?

## Procedência

| Afirmação | Script | Base | Data |
|---|---|---|---|
| Zoneamento, lojas Farmarcas, perfil | `zoneamento.py` | cadastro de lojas + Censo 2022 (API IBGE) | cadastro 2026-10-23 |
| REGIC, IPC, renda, classes, saturação, percentis | `contexto_municipio.py` | 15 bases municipais | dump 2026-10-26 |
| Concorrentes, qualidade de cadastro | `raio_concorrencia.py` | `concorrentes_2025` | dump 2026-10-26 |
| Mercado, crescimento, PDVs, receita Farmarcas | `mercado_utc.py` | `closeup_utc_varejo` + `mat_*_utc_*` | dump 2026-10-26 |
| Vizinhança de análises | `benchmark_historico.py` | `all_expansion.analysis_data` | dump 2026-10-26 |
| População do Censo 2022 | API pública | IBGE, agregado 4714, variável 93 | consultada 2026-10-26 |
