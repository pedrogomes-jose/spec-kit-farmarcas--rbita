"""Onde mais olhar: praças com mercado grande e pouca Farmarcas dentro.

Uso:
    python alternativas.py --uf SE --limite 12
    python alternativas.py --uf SE --excluir-municipio 2800308

Existe porque analisar só o ponto pedido responde "este serve?", e não "onde
seria melhor?". Cruza, por UTC:

  - receita total do mercado e crescimento  (mat_anterior_x_atual_utc_crescimento)
  - receita Farmarcas na UTC                (mesma base)
  - município da UTC                        (closeup_utc_varejo)
  - lojas Farmarcas ativas no município     (cadastro de lojas)
  - população do Censo 2022, quando em cache (faixa de zoneamento)

e devolve as praças ordenadas por mercado não atendido — receita total onde a
Farmarcas não fatura — já marcando se o zoneamento ainda tem vaga.

NÃO é recomendação de abertura: é lista de onde vale rodar um dossiê.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
import _bases as B  # noqa: E402

CACHE_CENSO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache", "censo2022.json")


CAMPO_POT_ANO = "1PotencialdeConsumoemR$-MedicamentoseHigieneecuidadospessoais-ANO"
CAMPO_POT_MES = "2PotencialdeConsumoemR$-Medicamentos+Higieneecuidadospessoais-MES"
CACHE_IQVIA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache", "iqvia_brick.csv")


def potencial_por_municipio() -> dict:
    """Potencial de consumo em drogarias por município — a base declara ANO e MÊS."""
    saida = {}
    for linha in B.ler("potencial_de_consumo"):
        cod = (linha.get("CODIGO") or "").strip()
        if not cod:
            continue
        saida[cod] = {
            "ano": B.num(linha.get(CAMPO_POT_ANO)),
            "mes": B.num(linha.get(CAMPO_POT_MES)),
        }
    return saida


def preco_por_municipio(uf: str) -> dict:
    """Preço médio por unidade dos bricks de cada município da UF.

    O nome do brick é `<num>-<UF>_<CIDADE>` e, nas cidades grandes, vem com o
    município abreviado (Aracaju = AJU). Então só casa onde o nome aparece
    inteiro — e é por isso que a saída devolve None em vez de forçar um número.
    """
    if not os.path.exists(CACHE_IQVIA):
        return {}
    import csv as _csv

    linhas = []
    with open(CACHE_IQVIA, encoding="utf-8", newline="") as fh:
        for r in _csv.DictReader(fh):
            if (r["codigo_uf"] or "").strip().upper() == uf and r["flag_mat"] == "MAT atual":
                linhas.append(r)

    nomes = {}
    for m in B.ler("municipios"):
        if (m.get("SIGLA_UF") or "").strip().upper() == uf:
            nomes[(m.get("CD_MUN") or "").strip()] = B.normalizar(m.get("NM_MUN", ""))

    saida = {}
    for cod, nome in nomes.items():
        uni = rec = 0.0
        for r in linhas:
            if nome and nome in B.normalizar(r["descricao_brick_rpe"]):
                u, pr = B.num(r["unidade"]), B.num(r["preco_consumidor"])
                if u and pr and u > 0:
                    uni += u
                    rec += pr
        saida[cod] = round(rec / uni, 2) if uni else None
    return saida


CACHE_CENTROIDES = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "cache", "centroides_municipios_v2.json"
)


def centroide_por_municipio() -> dict:
    """Centroide aproximado de cada município, por (UF, CIDADE) normalizados.

    O acervo NÃO traz coordenada de município: o polígono da UTC e o do setor
    ficaram no asset, e a coluna `geometry` do CSV guarda só a palavra "Polygon".
    A camada de concorrentes, porém, traz LAT/LONG por farmácia e cobre o país
    inteiro — farmácia existe em toda cidade. A MEDIANA das farmácias de uma
    cidade é, então, um centroide utilizável.

    Mediana e não média: a própria camada tem registros cadastrados numa cidade
    com coordenada em outra, e a média seria arrastada por eles. A mediana
    ignora o outlier sem precisar detectá-lo.

    MAS a mediana sozinha não basta, e o motivo custou uma praça falsa num
    dossiê (2026-11-06). Ela é calculada separadamente para latitude e
    longitude, então quando os registros da cidade se dividem entre dois
    lugares distantes o par (mediana_lat, mediana_lng) cai ENTRE os dois
    grupos — num lugar onde não existe farmácia nenhuma. Martins/RN tem 4
    registros: 2 em Martins/RN e 2 com coordenada de Presidente Médici/RO. A
    mediana devolvia -8,63/-49,91, no sul do Pará, e a cidade aparecia a 68 km
    de um ponto em Redenção/PA estando a ~2.000 km. Medido na camada inteira:
    81 dos 6.193 municípios com coordenada (1,3%) recebiam centroide num lugar
    sem farmácia alguma, até 1.675 km do registro mais próximo — 59 deles com
    exatamente 2 registros, que é a assinatura do defeito.

    Por isso a mediana é apenas a SEMENTE: o centroide devolvido é a farmácia
    real mais próxima dela. Assim o ponto é sempre um endereço que existe na
    camada, nunca um lugar interpolado. Em cidade com registro espalhado entre
    dois lugares, ele cai no grupo maior; no empate de 2 contra 2, cai num dos
    dois — e `dispersao_km` denuncia o caso, porque fica alta.

    É aproximação declarada, não geometria oficial: serve para ordenar praças
    por proximidade e para dizer a ordem de grandeza da distância, nunca para
    medir distância entre dois endereços.
    """
    if os.path.exists(CACHE_CENTROIDES):
        try:
            with open(CACHE_CENTROIDES, encoding="utf-8") as fh:
                return {tuple(k.split("\t")): v for k, v in json.load(fh).items()}
        except Exception:
            pass

    import statistics as _st

    pontos = {}
    for linha in B.ler("concorrentes_2025"):
        la, lo = B.num(linha.get("LAT")), B.num(linha.get("LONG"))
        if not B.coordenada_valida(la, lo):
            continue
        chave = (B.normalizar(linha.get("UF")), B.normalizar(linha.get("CIDADE")))
        if not chave[0] or not chave[1]:
            continue
        pontos.setdefault(chave, []).append((la, lo))

    saida = {}
    for k, v in pontos.items():
        sla = _st.median(p[0] for p in v)
        slo = _st.median(p[1] for p in v)
        # Encaixa a semente no registro real mais proximo: o centroide passa a
        # ser sempre uma farmacia que existe, nunca um ponto interpolado entre
        # dois grupos distantes. O(n) por cidade.
        la, lo = min(v, key=lambda p: B.haversine_m(sla, slo, p[0], p[1]))
        disp = round(_st.median(B.haversine_m(la, lo, p[0], p[1]) for p in v) / 1000.0, 1)
        saida[k] = [round(la, 6), round(lo, 6), len(v), disp]
    try:
        os.makedirs(os.path.dirname(CACHE_CENTROIDES), exist_ok=True)
        with open(CACHE_CENTROIDES, "w", encoding="utf-8") as fh:
            json.dump({"\t".join(k): v for k, v in saida.items()}, fh)
    except Exception:
        pass
    return saida


def partes_da_utc(nome: str) -> tuple:
    """Separa `UF-MUNICIPIO-LOCALIDADE` em (município, localidade).

    Município pequeno tem UTC única e nome sem localidade (`RN-ACARI`);
    município grande tem várias, cada uma com a sua (`RN-NATAL-CIDADE NOVA`).
    É a localidade que distingue uma linha da outra na mesma cidade — sem ela,
    Natal aparece onze vezes com números diferentes e nada explica a diferença.
    """
    pedacos = [p.strip() for p in (nome or "").split("-") if p.strip()]
    if len(pedacos) <= 1:
        return (nome or "").strip(), ""
    if len(pedacos) == 2:
        return pedacos[1], ""
    return pedacos[1], "-".join(pedacos[2:])


def alertas_do_cadastro(chave, sem_grupo: dict, popular_fora: dict, popular_aqui: dict):
    """O que, no cadastro, pode estar errando a contagem desta praça.

    Devolve `None` quando não há nada a dizer — alerta que aparece em toda linha
    deixa de ser alerta e passa a ser ruído de rodapé.

    Nunca carrega nome de pessoa nem de empresa: só contagem. Quem precisa saber
    QUAIS lojas divergem abre o cadastro; o relatório diz que existem e o que
    isso faz com o número ao lado.
    """
    fora = popular_fora.get(chave, 0)
    aqui = popular_aqui.get(chave, 0)
    sem = sem_grupo.get(chave, 0)
    if not (fora or aqui or sem):
        return None

    saida = {}
    if fora or aqui:
        saida["divergencia_de_endereco"] = {
            "lojas_daqui_com_endereco_popular_em_outra_cidade": fora or None,
            "lojas_de_outra_cidade_com_endereco_popular_aqui": aqui or None,
            "_leitura": (
                "a contagem de lojas desta praça usa o endereço da Receita, que é fiscal. "
                "Estas lojas têm endereço popular em município diferente, e podem estar "
                "contadas na praça errada — o que muda a contagem de grupos e, com ela, "
                "a disponibilidade"
            ),
        }
    if sem:
        saida["lojas_sem_grupo_economico_no_cadastro"] = {
            "lojas": sem,
            "_leitura": (
                "lojas ativas sem identificador de grupo preenchido. Elas contam como loja "
                "e não contam como grupo, então a praça pode aparecer com mais lojas do que "
                "grupos sem que isso seja erro de leitura — é falta de cadastro, e o teto "
                "pode estar sendo calculado contra um número de grupos menor que o real"
            ),
        }
    return saida


def teto_de_lojas(pop: int):
    if pop <= 60_000:
        return 1
    if pop <= 120_000:
        return 2
    if pop <= 200_000:
        return 3
    return None


def disponibilidade(pop, teto, n_grupos: int, modelo: str | None):
    """Cabe um grupo NOVO nesta praça? Devolve (bool|None, motivo legível).

    Conta GRUPOS, não lojas. Cidade com cinco lojas de um único dono e teto 2
    continua disponível: o que a regra protege é a convivência entre associados,
    e não há conflito onde só há um. Contar lojas aqui esconderia justamente as
    praças que a lista existe para mostrar.

    A faixa de 60 a 120 mil acrescenta uma condição que depende de QUEM pergunta:
    o 2º grupo a entrar tem de trazer bandeira popular. Uma praça dessa faixa com
    um grupo instalado está aberta para quem pretende bandeira popular e fechada
    para quem pretende convencional — a mesma linha, duas respostas.
    """
    if pop is None:
        return None, "sem população do Censo em cache — disponibilidade não apurada"
    if teto is None:
        return True, "sem teto (acima de 200 mil habitantes)"
    if n_grupos >= teto:
        return False, f"sem vaga — {n_grupos} grupo(s) para um teto de {teto}"
    # vaga existe; falta checar a exigência de bandeira popular do 2º grupo
    if teto == 2 and n_grupos == 1 and modelo == "convencional":
        return False, (
            "vaga existe, mas o 2º grupo desta faixa só entra com bandeira popular "
            "e o pedido é convencional"
        )
    sobra = teto - n_grupos
    return True, f"cabe grupo novo — {n_grupos} de {teto}, {sobra} vaga(s)"


# Teto de chamadas a API por rodada quando a disponibilidade precisa ser apurada
# dentro do raio. Sem teto seria uma chamada por candidato da UF; com ele, as
# maiores pracas do raio entram apuradas e o resto espera a vez. B.populacao_
# censo_2022 grava o que busca, entao da segunda rodada em diante sai do cache.
# ---------------------------------------------------------------------------
# Perfil das cidades da lista — valor e posição nacional, nunca nota
# ---------------------------------------------------------------------------
# A lista de praças ordena por mercado não atendido, que é quantidade medida, e
# o documento declara que não mede qualidade de praça. Isso empurrava a
# comparação para a PROSA, onde ela virava ranking por acidente: em 2026-11-25
# duas passadas de auditoria foram gastas tirando do texto "valem conferir
# primeiro", "o motivo mais interessante" e "olhar depois das duas primeiras".
#
# A saída é dar ao analista indicadores comparáveis, com o único referente que a
# casa permite (references/benchmarks.md): a posição de cada cidade na
# distribuição nacional da própria camada. Sem composto, sem ordenação nova.
#
# REGRA DE CORTE, e ela é o que impede o painel de virar ranking de porte:
# só entra indicador PER CAPITA, PERCENTUAL ou RAZÃO. Nunca total absoluto.
# IPC, PIB total, potencial anual, população e receita do município são todos
# proxies de tamanho — com qualquer um deles, as quatro dimensões ordenariam as
# cidades por porte ao mesmo tempo e o leitor concluiria "a capital é melhor em
# tudo". Teto: três indicadores por dimensão; o quarto entra substituindo.
#
# A unidade é o MUNICÍPIO, não a UTC. Nenhuma destas camadas existe por unidade
# territorial: numa cidade com várias UTCs, todas as linhas levariam valores
# idênticos — foi o defeito já corrigido para a taxa de captura, quando Natal
# aparecia capturando 19%, 12%, 8% e 5% em bairros diferentes.

def _classes_ab(linha) -> float | None:
    """Domicílios nas classes A + B1 + B2, em %. Derivado de três colunas."""
    partes = [B.num(linha.get(c)) for c in ("A(%)", "B1(%)", "B2(%)")]
    if any(p is None for p in partes):
        return None
    return sum(partes)


# (dimensão, rótulo, unidade, base, campo, leitura do percentil, fator)
#
# `fator` é só de APRESENTAÇÃO: várias colunas do acervo guardam percentual como
# fração (0,23 para 23%), e imprimir "0,2 %" ao lado de uma mediana de "0,2 %"
# não diz nada e ainda parece erro de ordem de grandeza. O percentil não muda —
# multiplicar todo mundo pela mesma constante não reordena nada.
INDICADORES_DO_PERFIL = [
    ("Poder de compra", "renda domiciliar per capita", "R$",
     "renda_media_municipio", "Renda_media_domic_per_capita",
     "percentil alto = renda acima da maioria dos municípios", 1),
    ("Poder de compra", "consumo em drogarias por habitante", "R$/ano",
     "potencial_de_consumo", "3ConsumoMedioDrogarias(p/habitante)R$",
     "percentil alto = gasta mais em farmácia por pessoa que a maioria", 1),
    ("Poder de compra", "domicílios nas classes A, B1 e B2", "%",
     "dados_farmacia_popular", _classes_ab,
     "percentil alto = mais domicílios de renda alta que a maioria", 100),

    ("Folga competitiva", "habitantes por farmácia", "hab",
     None, "habitantes_por_farmacia",
     "percentil alto = MENOS saturado: mais gente para cada farmácia", 1),
    ("Folga competitiva", "captura do potencial pelo varejo medido", "%",
     None, "captura",
     "percentil alto = mais do potencial da população já passa por farmácia medida", 1),
    ("Folga competitiva", "farmácias credenciadas ao Farmácia Popular", "%",
     "dados_farmacia_popular", "%farmaciascredenciadasaoFarmaciaPopnacidade",
     "percentil alto = parque mais credenciado; é PERFIL DO PARQUE, não folga", 100),

    ("Dinamismo", "crescimento demográfico", "% a.a.",
     "densidade_demografica", "TaxadeCrescimentoDemografico(%aa)",
     "percentil alto = cresce mais que a maioria dos municípios", 1),
    ("Dinamismo", "crescimento do mercado farmacêutico do município", "%",
     None, "crescimento_municipal",
     "percentil alto = mercado da cidade cresceu mais que o da maioria", 1),

    ("Centralidade urbana", "municípios que este influencia", "cidades",
     "regic_2018_municipio", "municipiosInfluenciados",
     "percentil alto = polo de mais cidades do entorno", 1),
    ("Centralidade urbana", "população urbana", "%",
     "situacao_territorio_municipio", "03-PopulacaoUrbana%",
     "percentil alto = população mais urbana que a maioria", 100),
    ("Centralidade urbana", "densidade demográfica", "hab/km²",
     "densidade_demografica", "DensidadeDemografica",
     "percentil alto = mais gente por km² que a maioria", 1),
]

# Fora de propósito, e o motivo escrito para ninguém reintroduzir:
# - PIB per capita: passa na regra de corte, mas em cidade industrial ou de
#   mineração mede o valor agregado da planta, não a carteira de quem entra na
#   loja. Três por dimensão já é o teto de leitura.
# - Variação de empregos (`movimentacao_economica`): a base NÃO declara o
#   período em lugar nenhum. Percentual de variação sem janela é número que
#   parece medida. Entra quando o período for estabelecido.
# - `classificacaoRegic` e `hierarquia`: são categóricos, e saem como RÓTULO sem
#   percentil. A régua dessa escala pertence ao IBGE; convertê-la em número aqui
#   seria inventar uma.


def _distribuicoes_derivadas():
    """As três distribuições nacionais que não são coluna de base.

    Montadas numa passada só sobre as bases de UTC, porque captura e crescimento
    municipal compartilham o mesmo somatório de receita por município.
    """
    import contexto_municipio as CM

    hab_farm = CM.habitantes_por_farmacia()

    # Receita por MUNICÍPIO = soma das UTCs dele. Nunca média das taxas das
    # UTCs: média de razão não é a razão do agregado, e a cidade com uma UTC
    # minúscula em disparada sairia crescendo muito.
    utc_mun = {}
    for linha in B.ler("closeup_utc_varejo"):
        uid = (linha.get("id_utc_var") or "").strip()
        if uid:
            utc_mun[uid] = (linha.get("codigo_mun") or "").strip()

    atual, anterior = {}, {}
    for linha in B.ler("mat_anterior_x_atual_utc_crescimento"):
        # A coluna de ligação desta base chama `utc_id_varejo`, e não
        # `id_utc_var` como em `closeup_utc_varejo`. Usar o nome errado não
        # quebra nada: devolve dicionário vazio, e todo município sai "sem
        # cobertura" como se a camada não o alcançasse. Pegou na primeira
        # rodada, em 2026-11-25, porque as quatro cidades saíram sem captura.
        cod = utc_mun.get((linha.get("utc_id_varejo") or "").strip())
        if not cod:
            continue
        atual[cod] = atual.get(cod, 0.0) + (B.num(linha.get("receita_atual_total")) or 0.0)
        anterior[cod] = anterior.get(cod, 0.0) + (B.num(linha.get("receita_anterior_total")) or 0.0)

    potenciais = potencial_por_municipio()
    captura = {}
    for cod, rec in atual.items():
        pot = (potenciais.get(cod) or {}).get("ano")
        if pot and pot > 0:
            captura[cod] = 100.0 * rec / pot

    crescimento = {
        cod: 100.0 * (rec / anterior[cod] - 1.0)
        for cod, rec in atual.items()
        if anterior.get(cod)
    }
    return {
        "habitantes_por_farmacia": hab_farm,
        "captura": captura,
        "crescimento_municipal": crescimento,
    }


def perfil_dos_municipios(candidatos: list) -> dict:
    """Uma entrada por município da lista, com os indicadores em percentil.

    Município, e não praça: quem decidiu isso foi o dado. Nenhuma destas camadas
    existe por unidade territorial, então uma linha por praça repetiria o mesmo
    valor sete vezes para Salvador e sugeriria sete cidades avaliadas.

    Não emite agregado nenhum — nem média de percentis, nem contagem de
    dimensões "ganhas". Dentro de uma mesma dimensão os indicadores podem
    apontar em direções opostas (renda alta com consumo de drogaria baixo é um
    achado), e qualquer composição apaga justamente isso.
    """
    derivadas = _distribuicoes_derivadas()
    regic = B.indexar_por_municipio("regic_2018_municipio")

    por_municipio = {}
    for c in candidatos:
        cod = c.get("codigo_ibge")
        if not cod:
            continue
        reg = por_municipio.setdefault(
            cod,
            {
                "municipio": c.get("municipio"),
                "uf": c.get("uf"),
                "codigo_ibge": cod,
                "pracas_na_tabela": 0,
                "alertas_de_cadastro": c.get("alertas_de_cadastro"),
                # Viaja junto porque a consequência do alerta de cadastro é
                # CONDICIONAL: onde não há teto, a contagem de grupos não decide
                # nada, e quem renderiza precisa saber disso para não anunciar
                # um risco que naquela cidade não existe.
                "teto_de_lojas": c.get("teto_de_lojas"),
                "papel_na_rede_urbana": None,
                "dimensoes": {},
                "sem_cobertura": [],
            },
        )
        reg["pracas_na_tabela"] += 1

    for cod, reg in por_municipio.items():
        linha_regic = regic.get(cod) or {}
        classe = (linha_regic.get("classificacaoRegic") or "").strip()
        if classe:
            reg["papel_na_rede_urbana"] = {
                "classificacao": classe,
                "_sem_percentil": "categoria ordinal do IBGE — virar número aqui seria inventar escala",
            }
        for dimensao, rotulo, unidade, base, campo, leitura, fator in INDICADORES_DO_PERFIL:
            valores = derivadas[campo] if base is None else B.distribuicao_municipal(base, campo)
            fonte = f"derivado.{campo}" if base is None else f"{base}.{campo if isinstance(campo, str) else 'derivado'}"
            resultado = B.percentil_em(valores, cod, leitura=leitura, fonte=fonte)
            resultado["rotulo"] = rotulo
            resultado["unidade"] = unidade
            if resultado.get("erro"):
                reg["sem_cobertura"].append(rotulo)
            elif fator != 1:
                # Escala de apresentação, aplicada DEPOIS do percentil.
                resultado["valor"] = round(resultado["valor"] * fator, 2)
                resultado["mediana_nacional"] = round(resultado["mediana_nacional"] * fator, 2)
            reg["dimensoes"].setdefault(dimensao, []).append(resultado)

    return {
        "_unidade": "MUNICÍPIO, não unidade territorial — nenhuma destas camadas existe por UTC, e uma linha por praça repetiria o mesmo valor em todas as regiões da mesma cidade",
        "_referente": "distribuição nacional dos municípios brasileiros da própria camada. Comparar as cidades desta lista entre si NÃO é referente válido: doze casos não são uma distribuição",
        "_sem_composicao": "nenhum agregado é emitido — nem média de percentis, nem contagem de dimensões. Dentro de uma dimensão os indicadores podem apontar em direções opostas, e compor apaga o achado",
        "_vies_da_populacao": "a razão de habitantes por farmácia usa a população do dump, estimativa ~4% acima do Censo 2022. A POSIÇÃO não herda o viés (numerador e denominador da mesma base, para todos os municípios); o VALOR herda, e não é comparável com a população do Censo que aparece na tabela de praças",
        "_ressalva_da_captura": "captura baixa pode ser mercado não capturado OU cobertura fraca do painel do instituto naquela praça. O acervo não separa os dois",
        "municipios": [por_municipio[c] for c in sorted(por_municipio, key=lambda k: (por_municipio[k]["municipio"] or "", por_municipio[k]["uf"] or ""))],
    }


LIMITE_APURACAO_NO_RAIO = 25


def apurar_zoneamento(c: dict, modelo) -> None:
    """Preenche população, teto e disponibilidade de uma praça, se faltarem.

    Os dois campos de disponibilidade saem SEMPRE juntos e da mesma função. Foi
    exatamente a atualização pela metade — `zoneamento` reescrito por contagem
    de lojas e `disponivel_para_grupo_novo` deixado como estava — que fazia
    praça disponível sumir da lista depois de ter sido apurada.
    """
    if c["populacao_censo_2022"] is not None or not c["codigo_ibge"]:
        return
    pop, _origem = B.populacao_censo_2022(c["codigo_ibge"])
    if not pop:
        return
    c["populacao_censo_2022"] = pop
    c["teto_de_lojas"] = teto_de_lojas(pop)
    disp, motivo = disponibilidade(
        pop, c["teto_de_lojas"], c["grupos_economicos_no_municipio"], modelo
    )
    c["zoneamento"] = motivo
    c["disponivel_para_grupo_novo"] = disp


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--uf", help="limita a uma UF (recomendado)")
    ap.add_argument("--excluir-municipio", help="código IBGE a tirar da lista")
    ap.add_argument("--limite", type=int, default=12)
    ap.add_argument("--min-receita", type=float, default=5_000_000.0)
    ap.add_argument("--modelo", choices=["popular", "convencional"],
                    help="modelo pretendido; decide a faixa 60-120 mil, onde o 2o grupo tem de ser popular")
    ap.add_argument("--so-disponiveis", action="store_true",
                    help="devolve apenas pracas onde cabe um grupo novo pela regra vigente")
    # Sem ancora geografica a lista e funcao da UF, nao do pedido: medido em
    # 2026-11-05, Pouso Alegre e Ipatinga (mesma UF, 390 km entre si) recebiam
    # listas IDENTICAS, 15 de 15 pracas iguais, nenhuma a menos de 150 km de
    # qualquer um dos dois. Ordenar por mercado absoluto entrega sempre a capital.
    ap.add_argument("--perto-de", metavar="LAT,LNG",
                    help="coordenada do ponto pedido; calcula a distancia ate cada praca")
    ap.add_argument("--raio-km", type=float,
                    help="descarta pracas alem deste raio (exige --perto-de)")
    # "Manter na cidade" nao e um raio pequeno. A distancia aqui e de centroide
    # de municipio a centroide de municipio, entao TODA regiao da cidade de
    # referencia tem a mesma distancia: nenhum raio separa uma regiao dela da
    # outra, e um raio pequeno ou pega a cidade inteira ou nao pega nada. O
    # recorte por cidade e por codigo IBGE, e e exclusivo com --raio-km.
    ap.add_argument("--so-municipio", metavar="CODIGO_IBGE",
                    help="mantem apenas as pracas deste municipio; nao cai para a UF quando o resultado e curto")
    ap.add_argument("--ordenar", choices=["mercado", "distancia"], default="mercado",
                    help="criterio de ordenacao; distancia exige --perto-de")
    # Opt-in, e nao sempre, porque `alternativas.py` e chamado por tres
    # formatos de relatorio e so a prospeccao imprime o painel. Bloco que o
    # script devolve e o gerador nao imprime e divida — ver
    # references/bloco-apurado-e-nao-impresso.md.
    ap.add_argument("--perfil-municipios", action="store_true",
                    help="acrescenta o perfil em percentis das cidades da lista")
    args = ap.parse_args()

    ancora = None
    if args.perto_de:
        try:
            _la, _lo = (float(x) for x in args.perto_de.replace(";", ",").split(",")[:2])
            ancora = (_la, _lo)
        except Exception:
            print("ERRO: --perto-de espera LAT,LNG (ex.: -22.21,-45.90)", file=sys.stderr)
            return 2
    if (args.ordenar == "distancia" or args.raio_km) and not ancora:
        print("ERRO: --ordenar distancia e --raio-km exigem --perto-de", file=sys.stderr)
        return 2
    if args.so_municipio and args.raio_km:
        print("ERRO: --so-municipio e --raio-km sao recortes concorrentes; escolha um",
              file=sys.stderr)
        return 2

    # UTC -> município
    utc_para_mun = {}
    for linha in B.ler("closeup_utc_varejo"):
        uid = (linha.get("id_utc_var") or "").strip()
        if uid:
            utc_para_mun[uid] = {
                "codigo_ibge": (linha.get("codigo_mun") or "").strip(),
                "municipio": (linha.get("municipio") or "").strip(),
                "uf": (linha.get("uf") or "").strip().upper(),
                "nome_utc": (linha.get("nome_utc_v") or "").strip(),
            }

    # lojas ativas por município
    lojas = {}
    # GRUPOS, nao lojas: e o grupo que ocupa vaga no teto. A chave e o ID
    # numerico do grupo economico no cadastro.
    #
    # Ate 2026-11-25 a deduplicacao era pelo NOME do responsavel normalizado, e
    # a fragilidade estava escrita aqui mesmo: grafia divergente entre duas
    # lojas do mesmo dono inventava um grupo e escondia uma praca disponivel,
    # num campo que e dado pessoal. A coluna `Grupo Economico` existe na
    # exportacao e e numerica — na exportacao de 10/11, 499 grupos pelo id
    # contra 499 pelo nome, nenhum grupo com responsavel variando entre lojas e
    # nenhum responsavel em mais de um grupo. Hoje as duas chaves dao o mesmo
    # resultado; a troca nao muda numero nenhum, fecha o modo de falha e tira
    # nome de pessoa da chave de contagem.
    grupos = {}
    # Loja ativa sem id de grupo preenchido. Sem isto, cidade com tres lojas e
    # nenhum grupo parece erro de leitura e nao falta de cadastro.
    sem_grupo = {}
    # A contagem de praca usa a cidade do endereco da RECEITA, que e fiscal. O
    # cadastro tambem tem o endereco POPULAR, e os dois divergem: medido em
    # 2026-11-25, 60 das lojas ativas apontavam para municipios diferentes. A
    # divergencia conta nos dois sentidos — uma praca ganha loja que nao esta
    # la, outra perde loja que esta — e numa praca pequena uma loja muda a
    # contagem de grupo, que muda o teto, que muda a disponibilidade.
    popular_fora = {}  # lojas desta cidade cujo endereco popular e em outra
    popular_aqui = {}  # lojas de outra cidade cujo endereco popular e aqui
    # Bandeiras ja presentes: a faixa 60-120 mil exige que o 2o grupo entre com
    # bandeira popular, entao a praca pode ter vaga e mesmo assim estar fechada
    # para quem pretende bandeira convencional.
    for loja in B.ler_cadastro_lojas():
        if (loja.get("Status") or "").strip() not in B.STATUS_OCUPA_VAGA:
            continue
        chave = (
            B.normalizar(loja.get("Cidade - Endereço Receita", "")),
            (loja.get("Estado - Endereço Receita") or "").strip().upper(),
        )
        lojas[chave] = lojas.get(chave, 0) + 1
        ge = (loja.get("Grupo Econômico") or "").strip()
        if ge:
            grupos.setdefault(chave, set()).add(ge)
        else:
            sem_grupo[chave] = sem_grupo.get(chave, 0) + 1

        cidade_pop = B.normalizar(loja.get("Cidade - Endereço Popular", ""))
        uf_pop = (loja.get("Estado - Endereço Popular") or "").strip().upper()
        # Popular em branco nao e divergencia: e ausencia de dado, e tratar como
        # divergencia encheria o relatorio de alerta que nao significa nada.
        if cidade_pop and (cidade_pop, uf_pop) != chave:
            popular_fora[chave] = popular_fora.get(chave, 0) + 1
            popular_aqui[(cidade_pop, uf_pop)] = popular_aqui.get((cidade_pop, uf_pop), 0) + 1

    censo = {}
    if os.path.exists(CACHE_CENSO):
        try:
            with open(CACHE_CENSO, encoding="utf-8") as fh:
                censo = json.load(fh)
        except (OSError, ValueError):
            censo = {}

    potenciais = potencial_por_municipio()
    precos = preco_por_municipio(args.uf.strip().upper()) if args.uf else {}

    candidatos = []
    for linha in B.ler("mat_anterior_x_atual_utc_crescimento"):
        uid = (linha.get("utc_id_varejo") or "").strip()
        meta = utc_para_mun.get(uid)
        if not meta:
            continue
        if args.uf and meta["uf"] != args.uf.strip().upper():
            continue
        if args.excluir_municipio and meta["codigo_ibge"] == args.excluir_municipio.strip():
            continue

        total = B.num(linha.get("receita_atual_total")) or 0.0
        nosso = B.num(linha.get("receita_atual_farmarcas")) or 0.0
        if total < args.min_receita:
            continue

        pop = censo.get(meta["codigo_ibge"])
        teto = teto_de_lojas(pop) if pop else None
        _chave_mun = (B.normalizar(meta["municipio"]), meta["uf"])
        ativas = lojas.get(_chave_mun, 0)
        n_grupos = len(grupos.get(_chave_mun, ()))
        disp, motivo = disponibilidade(pop, teto, n_grupos, args.modelo)
        _alertas = alertas_do_cadastro(
            _chave_mun, sem_grupo, popular_fora, popular_aqui
        )

        pot = potenciais.get(meta["codigo_ibge"]) or {}
        pot_ano = pot.get("ano")

        _mun_utc, _loc = partes_da_utc(meta["nome_utc"])
        candidatos.append(
            {
                "municipio": meta["municipio"],
                "localidade": _loc,
                "praca": f"{meta['municipio']} — {_loc}" if _loc else meta["municipio"],
                "uf": meta["uf"],
                "codigo_ibge": meta["codigo_ibge"],
                "utc": meta["nome_utc"],
                "receita_mercado_R$": round(total, 2),
                "receita_mercado_anterior_R$": round(B.num(linha.get("receita_anterior_total")) or 0.0, 2),
                "receita_farmarcas_R$": round(nosso, 2),
                "mercado_nao_atendido_R$": round(total - nosso, 2),
                "share_farmarcas": round(nosso / total, 4) if total else None,
                "crescimento_mercado": B.num(linha.get("crescimento_total")),
                "crescimento_farmarcas": B.num(linha.get("crescimento_farmarcas")),
                "lojas_farmarcas_no_municipio": ativas,
                "grupos_economicos_no_municipio": n_grupos,
                "alertas_de_cadastro": _alertas,
                "potencial_consumo_drogarias_ano_R$": pot_ano,
                "potencial_consumo_drogarias_mes_R$": pot.get("mes"),
                "_potencial_e": "do MUNICÍPIO inteiro — não existe potencial por UTC nas bases",
                "preco_medio_por_unidade_R$": precos.get(meta["codigo_ibge"]),
                "populacao_censo_2022": pop,
                "teto_de_lojas": teto,
                "zoneamento": motivo,
                "disponivel_para_grupo_novo": disp,
            }
        )

    # CAPTURA É MUNICIPAL, e repete nas UTCs da mesma cidade. Dividir a receita
    # de UMA UTC pelo potencial do município inteiro dá razão sem sentido — era
    # o que acontecia, e fazia Natal parecer capturar 19%, 12%, 8% e 5% em
    # bairros diferentes. O numerador precisa ser a receita do município toda.
    receita_por_municipio: dict = {}
    for c in candidatos:
        k = c["codigo_ibge"]
        receita_por_municipio[k] = receita_por_municipio.get(k, 0.0) + (c["receita_mercado_R$"] or 0)
    for c in candidatos:
        pot_ano = c.get("potencial_consumo_drogarias_ano_R$")
        rec_mun = receita_por_municipio.get(c["codigo_ibge"], 0.0)
        c["receita_do_municipio_R$"] = round(rec_mun, 2)
        c["taxa_de_captura_do_municipio"] = round(rec_mun / pot_ano, 4) if pot_ano else None
        c["_taxa_de_captura"] = (
            "receita somada de todas as UTCs do município ÷ potencial anual do município — "
            "é indicador MUNICIPAL, igual para todas as linhas da mesma cidade"
        )
        c["potencial_nao_capturado_R$"] = round(pot_ano - rec_mun, 2) if pot_ano else None


    def escala(v):
        if v is None:
            return "—"
        if abs(v) >= 1e9:
            return f"R$ {v / 1e9:.2f} bilhões".replace(".", ",")
        if abs(v) >= 1e6:
            return f"R$ {v / 1e6:.1f} milhões".replace(".", ",")
        if abs(v) >= 1e3:
            return f"R$ {v / 1e3:.0f} mil".replace(".", ",")
        return f"R$ {v:.2f}".replace(".", ",")

    for c in candidatos:
        # Frase montada a partir dos próprios números — é recomposição, não
        # interpretação. Nenhum juízo entra aqui.
        onde = f"em {c['localidade']}" if c.get("localidade") else "no município"
        pedacos = [f"mercado de {escala(c['mercado_nao_atendido_R$'])} sem receita nossa dentro, {onde}"]
        if c["lojas_farmarcas_no_municipio"] == 0:
            pedacos.append("nenhuma loja Farmarcas na cidade")
        else:
            pedacos.append(f"{c['lojas_farmarcas_no_municipio']} loja(s) Farmarcas já na cidade")
        if c["crescimento_mercado"]:
            pedacos.append(f"mercado crescendo {c['crescimento_mercado'] * 100:.0f}%")
        if c["taxa_de_captura_do_municipio"]:
            pedacos.append(
                f"{c['taxa_de_captura_do_municipio'] * 100:.0f}% do potencial anual do município já capturado"
            )
        if c["preco_medio_por_unidade_R$"]:
            pedacos.append(f"preço médio de R$ {c['preco_medio_por_unidade_R$']:.2f} por unidade".replace(".", ","))
        if c["crescimento_farmarcas"] is not None and c["crescimento_farmarcas"] < 0:
            # O que a base mede é a QUEDA. "Praça já testada e perdida" é uma
            # explicação possível para ela, e não a única — e esta frase dizia
            # a explicação, não a medida, contra a regra declarada três linhas
            # acima ("nenhum juízo entra aqui").
            #
            # Duas razões para a leitura antiga ser a menos provável das duas:
            # a base é a carteira ATUAL da rede com histórico retroagido (ver
            # `_limites.carteira`), então associado que SAIU não aparece como
            # queda — ele some da série inteira; e, medido em Salvador/BA em
            # 2026-11-25, as três regiões em retração (Itapoã-1, Vitória e
            # Plataforma) não tiveram saída de associado nenhuma: é loja que
            # continua operando e encolheu. Nenhuma base deste acervo separa os
            # dois casos, e por isso o script não escolhe.
            pedacos.append(
                f"ATENÇÃO: a receita da rede caiu {abs(c['crescimento_farmarcas']) * 100:.0f}% aqui "
                "— a base não diz por quê, e saída de associado não é a única explicação"
            )
        c["escala_mercado_nao_atendido"] = escala(c["mercado_nao_atendido_R$"])
        c["motivo"] = "; ".join(pedacos) + "."

    # --- distancia ate o ponto pedido
    # Sem isto a lista responde a pergunta errada. Quem recebeu um "nao" precisa
    # de praca que consiga operar, e a praca mais rica da UF e sempre a capital:
    # a mesma lista servia para dois pedidos a 390 km um do outro.
    sem_centroide = 0
    if ancora:
        cen = centroide_por_municipio()
        for c in candidatos:
            ponto = cen.get((B.normalizar(c["uf"]), B.normalizar(c["municipio"])))
            if not ponto:
                c["distancia_km"] = None
                c["_distancia_ausente"] = "município sem farmácia com coordenada na camada de concorrentes"
                sem_centroide += 1
                continue
            c["distancia_km"] = round(
                B.haversine_m(ancora[0], ancora[1], ponto[0], ponto[1]) / 1000.0, 1
            )
            c["_centroide_do_municipio"] = {
                "lat": ponto[0], "lng": ponto[1], "farmacias_usadas": ponto[2],
                # Distancia mediana das farmacias da cidade ate o centroide. Alta
                # significa registro espalhado entre lugares distantes — a cidade
                # existe, mas a distancia ate ela e menos confiavel.
                "dispersao_km": ponto[3] if len(ponto) > 3 else None,
                "_metodo": "farmácia real mais próxima da mediana das coordenadas da cidade — aproximação, não geometria oficial",
            }
            if c.get("motivo"):
                c["motivo"] = f"a {c['distancia_km']:.0f} km do ponto pedido; " + c["motivo"]

    # --- so esta cidade
    # Sem queda para a UF: aqui o pedido NAO e "pracas perto", e sim "pracas
    # nesta cidade". Lista vazia e resposta — significa que nenhuma regiao do
    # municipio passa no piso de receita ou na regra de zoneamento, e trocar
    # isso pela UF inteira responderia outra pergunta sem avisar.
    so_municipio = None
    if args.so_municipio:
        cod = args.so_municipio.strip()
        dentro_cidade = [c for c in candidatos if c["codigo_ibge"] == cod]
        for c in sorted(dentro_cidade, key=lambda x: -x["mercado_nao_atendido_R$"])[:LIMITE_APURACAO_NO_RAIO]:
            apurar_zoneamento(c, args.modelo)
        uteis_cidade = ([c for c in dentro_cidade if c["disponivel_para_grupo_novo"]]
                        if args.so_disponiveis else dentro_cidade)
        so_municipio = {
            "codigo_ibge": cod,
            "municipio": (dentro_cidade[0]["municipio"] if dentro_cidade else None),
            "utcs_do_municipio_no_acervo": len(dentro_cidade),
            "pracas_que_sobram": len(uteis_cidade),
            "_sem_queda_para_a_uf": True,
            "_se_vazio": None if uteis_cidade else (
                "nenhuma regiao deste municipio sobrou: ou nenhuma alcanca o piso de "
                f"R$ {args.min_receita:,.0f}".replace(",", ".")
                + " de receita de mercado, ou a regra de zoneamento nao deixa entrar grupo "
                "novo em nenhuma delas. A lista vazia E o achado — o caminho e o dossie de "
                "um ponto da cidade, que roda o gate sobre um endereco"
            ),
        }
        candidatos = dentro_cidade

    disponiveis_no_raio = None
    if args.raio_km:
        dentro = [c for c in candidatos if c.get("distancia_km") is not None
                  and c["distancia_km"] <= args.raio_km]
        # A contagem abaixo LE disponibilidade, entao a disponibilidade precisa
        # estar apurada antes dela. Sem isto, praca sem Censo em cache entrava
        # como indisponivel, a contagem nao alcancava o minimo e o raio caia:
        # numa maquina de cache vazio a lista voltava a ser a da UF inteira, que
        # ordenada por mercado absoluto e sempre a capital. Medido: com o cache
        # local vazio, a busca a partir de Pouso Alegre devolvia Belo Horizonte,
        # Juiz de Fora e Montes Claros.
        for c in sorted(dentro, key=lambda x: -x["mercado_nao_atendido_R$"])[:LIMITE_APURACAO_NO_RAIO]:
            apurar_zoneamento(c, args.modelo)
        # Contar o que SOBREVIVE ao filtro de disponibilidade, nao o que cai no
        # raio: medido em Araputanga/MT, havia 10 pracas a menos de 150 km e
        # NENHUMA disponivel — o raio era aplicado, a disponibilidade esvaziava
        # a lista depois, e o relatorio saia com tabela vazia e sem explicacao.
        uteis = [c for c in dentro if c["disponivel_para_grupo_novo"]] if args.so_disponiveis else dentro
        disponiveis_no_raio = len(uteis)
        # Raio que nao devolve nada e pior que raio nenhum: o leitor fica sem
        # caminho e sem saber por que. Cai para a lista inteira e DECLARA.
        #
        # LIMITE RESIDUAL: a apuracao acima cobre as maiores do raio, nao todas.
        # Praca pequena e sem cache ainda pode entrar na contagem como
        # indisponivel. O desvio erra para o lado de MOSTRAR MAIS pracas, nunca
        # de esconder — sem o raio a lista fica maior e _proximidade declara que
        # ele nao foi aplicado — e se corrige entre rodadas pelo cache.
        raio_aplicado = disponiveis_no_raio >= 3
        if raio_aplicado:
            candidatos = dentro
    else:
        raio_aplicado = False

    if args.ordenar == "distancia":
        # None por ultimo: praca sem centroide nao e praca perto.
        candidatos.sort(key=lambda c: (c.get("distancia_km") is None,
                                       c.get("distancia_km") or 0.0,
                                       -c["mercado_nao_atendido_R$"]))
    else:
        candidatos.sort(key=lambda c: -c["mercado_nao_atendido_R$"])

    # Só os finalistas puxam o Censo da API — é uma chamada por município, e
    # sem ela a coluna de zoneamento fica inconclusiva justamente onde importa.
    for c in candidatos[: args.limite]:
        apurar_zoneamento(c, args.modelo)

    melhores = (
        [c for c in candidatos if c["disponivel_para_grupo_novo"]][: args.limite]
        if args.so_disponiveis
        else candidatos[: args.limite]
    )

    B.emitir(
        {
            "filtro": {
                "uf": args.uf,
                "municipio_excluido": args.excluir_municipio,
                "receita_minima_R$": args.min_receita,
            },
            "utcs_avaliadas": len(candidatos),
            "melhores": melhores,
            # So existe quando pedido: ver o comentario da flag.
            "perfil_dos_municipios": perfil_dos_municipios(melhores) if args.perfil_municipios else None,
            "_disponibilidade": {
                "_regra": "cabe grupo novo quando os grupos econômicos com loja ativa na cidade são MENOS que o teto da faixa — e, na faixa de 60 a 120 mil, o 2º grupo só entra com bandeira popular",
                "_apuracao_do_grupo": "identificador de grupo econômico do cadastro de lojas. Até 2026-11-25 a contagem deduplicava pelo NOME do responsável, que quebra com grafia divergente — duas lojas do mesmo dono escritas de dois jeitos viravam dois grupos, e um grupo a mais barra um pedido que caberia. Loja ativa sem identificador preenchido conta como loja e não conta como grupo, e isso é declarado por praça",
                "_modelo_informado": args.modelo or "não informado — a restrição da faixa 60 a 120 mil não foi aplicada",
                "_filtro_aplicado": bool(args.so_disponiveis),
            },
            "_ordenacao": (
                "distância até o ponto pedido, pelo centroide do município; empate desfeito "
                "pelo mercado não atendido"
                if args.ordenar == "distancia"
                else "mercado não atendido = receita total da UTC menos a receita Farmarcas"
            ),
            "_so_municipio": so_municipio,
            "_proximidade": {
                "ancora": {"lat": ancora[0], "lng": ancora[1]} if ancora else None,
                "raio_km_pedido": args.raio_km,
                "raio_aplicado": raio_aplicado,
                "pracas_disponiveis_dentro_do_raio": disponiveis_no_raio,
                "_se_nao_aplicado": (
                    None if raio_aplicado or not args.raio_km else
                    f"só {disponiveis_no_raio} praça(s) disponível(is) dentro de "
                    f"{args.raio_km:.0f} km — menos que o mínimo de 3 para a lista ter valor. "
                    "O raio foi ignorado e a lista devolve a UF inteira; a distância de cada "
                    "linha continua declarada, e o fato de não haver praça perto É o achado"
                ),
                "pracas_sem_centroide": sem_centroide if ancora else None,
                "_metodo": (
                    "o acervo não traz coordenada de município — o polígono da UTC ficou no "
                    "asset e a coluna de geometria do CSV guarda só a palavra 'Polygon'. A "
                    "distância parte da MEDIANA das coordenadas de farmácia da cidade na "
                    "camada de concorrentes, que cobre o país inteiro, e usa a farmácia real "
                    "mais próxima dessa mediana — para que o centroide seja sempre um endereço "
                    "que existe, e nunca um ponto interpolado entre dois grupos distantes de "
                    "registros. É centroide aproximado: serve para ordenar praças e dar ordem "
                    "de grandeza, nunca para medir distância entre dois endereços."
                ) if ancora else "nenhuma âncora informada — a lista não considera distância",
            },
            "_leitura": (
                "lista de onde vale rodar um dossiê, não recomendação de abertura. "
                "Mercado grande sem nós pode ser oportunidade OU praça já testada e perdida, "
                "e esta apuração NÃO separa os dois: `crescimento_farmarcas` negativo mede "
                "queda de receita da rede na praça, não saída de associado. A base é a "
                "carteira atual com histórico retroagido, então quem saiu não aparece como "
                "queda — some da série. Para separar, é preciso o histórico de entrada e "
                "saída de associado por praça, que não está neste acervo"
            ),
            "_limites": {
                "zoneamento": "conclusivo para as praças listadas, que puxam o Censo da API quando falta cache; praça fora do limite pode sair sem apuração. A contagem é de GRUPOS econômicos, não de lojas, e a vaga é calculada para um grupo NOVO — para quem já opera na praça a leitura é outra. Vaga aqui é ausência de impedimento na contagem, não liberação: o gate roda no ponto, por zoneamento.py",
                "granularidade": "UTC não é raio nem bairro; serve para escolher a praça, não o ponto",
                "carteira": "a base IQVIA é a carteira ATUAL da Farmarcas, com histórico retroagido",
            },
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
