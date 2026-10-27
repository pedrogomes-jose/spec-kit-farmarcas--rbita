# As quatro lentes

O dossiê não dá nota e não dá veredito. Ele organiza o que se sabe da região em
quatro lentes, e cada item carrega o que permite ao analista discordar.

**Anatomia de um item** — sem os quatro campos, o item não entra:

1. **número** — valor, com unidade, no texto
2. **fonte de dado** — em **campo próprio** (`fonte`), nunca no meio da frase
3. **comparação** — contra o município, a UF, ou o histórico de análises
4. **confiança** — alta / média / baixa, **com o motivo**, no texto

**A fonte sai do parágrafo.** Ela vai no campo `fonte` do item e aparece como
referência numerada no fim da frase, resolvida na seção **Fontes** ao final do
relatório. Fonte no meio do texto interrompe a leitura e, paradoxalmente, some
do radar de quem quer conferir: espalhada por dezesseis parágrafos, ninguém a
usa. Consolidada numa tabela, serve às duas coisas — o texto corre e o auditor
acha tudo num lugar só.

**A ressalva faz parte da frase, não é um apêndice rotulado.** Não existe campo
"muda a leitura se": o limite do método, o dado que falta e a condição que
inverteria a conclusão entram **explicados dentro do parágrafo**, no ponto em
que o leitor precisa deles.

| Não escrever | Escrever |
|---|---|
| "…Fonte: base da IQVIA. Confiança média. Muda a leitura se: o brick foi casado por bairro." | texto: "…Confiança média, porque o brick foi casado pelo bairro do ponto e não pela geometria: se o ponto cair num brick vizinho, o preço muda." · fonte: "base de faturamento por brick da IQVIA" |
| "…Muda a leitura se: a REGIC é de 2018." | "…O dado é de 2018, então descreve a cidade de sete anos atrás — o papel regional dela pode ter mudado desde então." |

O rótulo virava uma coleira: o modelo preenchia por obrigação, quase sempre
repetindo a linha de confiança, e o leitor aprendia a pular. Explicado dentro do
texto, o mesmo conteúdo é lido.

## Tier de decisão

Nem tudo pesa igual. O dossiê abre por **Tier 1** e só desce se houver espaço.
A ordem veio do que os analistas de fato abrem (`benchmark_historico.py
--panorama`), não de opinião.

| Tier | O que é | Entra sempre? |
|---|---|---|
| **0 — barra** | zoneamento: teto de lojas, distância mínima, modelo da bandeira | sim, e se barrar o dossiê para aí |
| **1 — decide** | concorrência no raio, loja Farmarcas no raio, potencial de consumo, renda, população | sim |
| **2 — contextualiza** | REGIC, PIB, IPC do bairro, Firjan, urbanização, mix de categorias da UTC | sim, resumido |
| **3 — só se relevante** | saneamento, verticalização, educação, pirâmide etária, movimentação econômica | só se mudar a leitura de um item do Tier 1 |

---

## Forças — o que joga a favor

| Sinal | Vem de |
|---|---|
| Potencial de consumo em drogarias e gasto em medicamentos | `dados_farmacia_popular.GastosemMEDICAMENTOS`, `potencial_de_consumo` |
| Cidade puxa público de fora | `regic_2018_municipio` — hierarquia e nº de municípios influenciados |
| IPC do bairro acima da média do município | `ranking_bairros.IPC` + `RANKINGMUNICIPIO` |
| Mercado farmacêutico local crescendo | `mat_anterior_x_atual_utc_crescimento.crescimento_total` |
| Alta urbanização | `situacao_territorio_municipio.03-PopulacaoUrbana%` |
| Desenvolvimento municipal acima da mediana | `firjan_ifdm_geral.IFDM` + posição nacional |

## Fragilidades — o que joga contra

| Sinal | Vem de |
|---|---|
| **Saturação**: habitantes por farmácia na cidade vs. mediana nacional | `populacao_municipios` ÷ `dados_farmacia_popular.totalfarmaciasnacidade` |
| Concorrente grande colado no ponto | `raio_concorrencia` — `fat_medio` e distância |
| Rede nacional no raio (Raia, Drogasil, Pague Menos, São João…) | `MDM-ClassifdoPDV` |
| Classe econômica concentrada em D/E ou em A | `dados_farmacia_popular.D/E(%)`, `A(%)` |
| Renda per capita abaixo da mediana estadual | `renda_media_municipio` |
| Cidade encolhendo | `densidade_demografica.TaxadeCrescimentoDemografico(%aa)` |
| Farmarcas perdendo para o mercado na UTC | `crescimento_farmarcas` < `crescimento_sem_farmarcas` |

## Oportunidades — o que ainda não foi tomado

| Sinal | Vem de |
|---|---|
| **Share Farmarcas zero ou baixo numa UTC de receita alta** | `mat_atual_utc_market_share` + `receita_atual_total` |
| Nenhuma loja Farmarcas credenciada ao Farmácia Popular na cidade | `dados_farmacia_popular.lojasFARMARCAScredenciadas` = 0 |
| Categoria crescendo acima do mercado | `mat_anterior_x_atual_utc_mix_categorias.*_crescimento` |
| Bairro com IPC alto e pouca concorrência no raio | cruzamento `ranking_bairros` × `raio_concorrencia` |
| Mercado cresce e o nº de PDVs não | `..._sem_cobertura.delta_pdvs` ≈ 0 com `crescimento` > 0 |

## Dificuldades — o que vai dar trabalho

> **Antes desta lente, saber quem pede.** Loja Farmarcas vizinha significa
> coisas opostas conforme o solicitante — ver `zoneamento-e-perfil.md`.

| Sinal | Vem de |
|---|---|
| **Canibalização com loja de OUTRO associado** — é o conflito que a regra de expansão existe para evitar | `zoneamento.py`, lojas com `do_solicitante: false` |
| **Sobreposição com loja DO PRÓPRIO solicitante** — pode ser estratégia (fechar mercado, share, poder de negociação), não defeito do ponto | `zoneamento.py`, lojas com `do_solicitante: true` |
| **Alerta de zoneamento** que não barrou mas pesa: alternância de bandeiras, distância acima de 200 mil hab, cadastro divergente | `zoneamento.py`, bloco `alertas` |
| Loja Farmarcas desativada perto — por que fechou? | `raio_concorrencia.lojas_farmarcas_no_raio`, status `Desativado` |
| Já houve análise reprovada perto daqui | `benchmark_historico --vizinhanca`, com o motivo registrado |
| Cidade pequena, UTC única, mercado concentrado | `mercado_utc` + `populacao_municipios` |
| **Fluxo de passantes não medido** | lacuna obrigatória — ver `limites-e-vieses.md` |
| Setor censitário indisponível no raio | lacuna da Fase 2 |

---

## Regra de corte

Item que não muda nenhuma decisão não entra. Se as quatro lentes somarem mais
de ~15 itens, o problema não é o ponto: é o dossiê. Cortar pelo Tier.
