"""Contexto municipal do ponto: quem é esta cidade, e como ela se compara.

Uso:
    python contexto_municipio.py --municipio "FRANCA" --uf SP
    python contexto_municipio.py --lat -20.5386 --lng -47.4006

Sem --municipio, o município é inferido pelo concorrente mais próximo no dump
(método declarado na saída). Não é geocodificação: é vizinhança.
"""

from __future__ import annotations

import argparse
import json
import sys
import unicodedata

sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
import _bases as B  # noqa: E402

# base -> (campos que interessam, o que a base responde)
MUNICIPAIS = {
    "populacao_municipios": (
        ["01-POPULACAOTOTAL", "03-POPULACAOMASCULINA%", "05-POPULACAOFEMININA%"],
        "quantos moram no município",
    ),
    "densidade_demografica": (
        ["DensidadeDemografica", "Areaemkm2", "TaxadeCrescimentoDemografico(%aa)"],
        "densidade e se a cidade cresce ou encolhe",
    ),
    "situacao_territorio_municipio": (
        ["03-PopulacaoUrbana%", "05-PopulacaoRural%", "06-DistanciadaCapital"],
        "urbano x rural e distância da capital",
    ),
    "renda_media_municipio": (["Renda_media_domic_per_capita"], "renda domiciliar per capita"),
    "pib": (
        ["01-PIBTOTAL(R$MIL)", "02-PIBPERCAPITA(EMR$)", "03-CONSUMOPERCAPITAR$/ANOURBANO"],
        "porte econômico e consumo per capita",
    ),
    "ranking_de_consumo": (["IPC", "RankingEstadual", "RankingNacional"], "índice de potencial de consumo"),
    "firjan_ifdm_geral": (["IFDM", "Educacao", "Emprego&Renda", "Saude", "Estadual", "Nacional"], "desenvolvimento municipal"),
    "indice_de_educacao": (["03-POPULACAOALFABETIZADA%"], "escolaridade básica"),
    "empresas_totais": (["09-TOTAL", "04-CATEGORIACOMERCIO%", "08-CATEGORIASERVICOS%"], "tecido empresarial"),
    "dados_farmacia_popular": (
        [
            "totalfarmaciasnacidade",
            "NºfarmaciascredenciadasFarmaciaPopular",
            "%farmaciascredenciadasaoFarmaciaPopnacidade",
            "lojasFARMARCAScredenciadas",
            "GastosemMEDICAMENTOS",
            "A(%)", "B1(%)", "B2(%)", "C1(%)", "C2(%)", "D/E(%)",
        ],
        "mercado farmacêutico e classe econômica da cidade",
    ),
    "regic_2018_municipio": (
        ["classificacaoRegic", "hierarquia", "nivelInfluenciaTexto", "perfilCidadeTexto", "municipiosInfluenciados", "polosPrincipais"],
        "papel da cidade na rede urbana — de onde vem o público",
    ),
}


def slug(texto: str) -> str:
    t = unicodedata.normalize("NFKD", (texto or "").upper())
    return "".join(c for c in t if not unicodedata.combining(c)).strip()


def resolver_por_nome(nome: str, uf: str | None):
    alvo = slug(nome)
    achados = []
    for linha in B.ler("municipios"):
        if slug(linha.get("NM_MUN", "")) == alvo:
            if uf and (linha.get("SIGLA_UF", "").upper() != uf.upper()):
                continue
            achados.append(
                {"codigo": linha["CD_MUN"], "nome": linha["NM_MUN"], "uf": linha["SIGLA_UF"], "area_km2": B.num(linha.get("AREA_KM2"))}
            )
    return achados


def resolver_por_coordenada(lat: float, lng: float):
    """Infere o município pelo concorrente mais próximo. Método aproximado."""
    melhor = None
    for linha in B.ler("concorrentes_2025"):
        la, lo = B.num(linha.get("LAT")), B.num(linha.get("LONG"))
        if la is None or lo is None:
            continue
        d = B.haversine_m(lat, lng, la, lo)
        if melhor is None or d < melhor[0]:
            melhor = (d, linha.get("CIDADE", ""), linha.get("UF", ""))
    if not melhor:
        return None
    dist, cidade, uf = melhor
    achados = resolver_por_nome(cidade, uf)
    if not achados:
        return None
    achados[0]["_metodo"] = f"inferido pelo concorrente mais próximo ({dist:.0f} m) — não é geocodificação"
    return achados[0]


def populacao_censo_2022_safe(codigo: str):
    try:
        return B.populacao_censo_2022(codigo)
    except Exception as e:  # rede indisponível não pode derrubar o contexto
        return None, f"indisponível ({type(e).__name__})"


def percentil_municipal(prefixo: str, campo: str, codigo: str, maior_e_melhor: bool = True) -> dict:
    """Posição de um indicador municipal na distribuição nacional da própria base.

    Existe porque número isolado não decide nada: "renda de R$ 453,17" não é boa
    nem ruim; "percentil 38 dos 5.565 municípios" é.
    """
    valores = {}
    for cod, linha in B.indexar_por_municipio(prefixo).items():
        v = B.num(linha.get(campo))
        if v is not None:
            valores[cod] = v
    alvo = valores.get(str(codigo).strip())
    if alvo is None:
        return {"erro": f"município ausente em {prefixo}.{campo}"}
    ordenados = sorted(valores.values())
    abaixo = sum(1 for v in ordenados if v < alvo)
    pct = round(100.0 * abaixo / len(ordenados))
    return {
        "valor": alvo,
        "percentil": pct,
        "mediana_nacional": round(ordenados[len(ordenados) // 2], 2),
        "municipios_comparados": len(ordenados),
        "_leitura": ("percentil alto = acima da maioria" if maior_e_melhor else "percentil alto = abaixo da maioria"),
        "_fonte": f"{prefixo}.{campo}",
    }


def saturacao(codigo: str) -> dict:
    """Habitantes por farmácia no município, e em que percentil isso cai.

    Número isolado não diz nada: 1.490 hab/farmácia só significa algo contra a
    distribuição dos 5.570 municípios. O percentil é a comparação.
    """
    pop = {c: B.num(l.get("01-POPULACAOTOTAL")) for c, l in B.indexar_por_municipio("populacao_municipios").items()}
    farm = {c: B.num(l.get("totalfarmaciasnacidade")) for c, l in B.indexar_por_municipio("dados_farmacia_popular").items()}

    razoes = {}
    for c, p in pop.items():
        f = farm.get(c)
        if p and f and f > 0:
            razoes[c] = p / f

    alvo = razoes.get(codigo)
    if alvo is None:
        return {"erro": "município sem população ou sem contagem de farmácias nas bases"}

    ordenados = sorted(razoes.values())
    abaixo = sum(1 for v in ordenados if v < alvo)
    meio = ordenados[len(ordenados) // 2]

    # A distribuição inteira usa a população do DUMP, para ser internamente
    # coerente. Mas o cabeçalho do dossiê usa o Censo 2022 (é ele que corta a
    # faixa de zoneamento), e as duas populações divergem ~4%. Sem declarar a
    # base, o leitor não fecha a conta. Por isso devolvemos as duas razões.
    censo, origem_censo = populacao_censo_2022_safe(codigo)
    f = farm.get(codigo)
    por_censo = None
    if censo and f:
        alvo_censo = censo / f
        por_censo = {
            "habitantes_por_farmacia": round(alvo_censo, 1),
            "percentil": round(100.0 * sum(1 for v in ordenados if v < alvo_censo) / len(ordenados)),
            "_origem": origem_censo,
            "_ressalva": "numerador do Censo contra distribuição montada com o dump — aproximação",
        }

    return {
        "_base_da_distribuicao": "população do dump do Órbita (estimativa, ano não declarado)",
        "habitantes_por_farmacia": round(alvo, 1),
        "mediana_nacional": round(meio, 1),
        "percentil": round(100.0 * abaixo / len(ordenados)),
        "municipios_comparados": len(ordenados),
        "com_populacao_do_censo_2022": por_censo,
        "_leitura": (
            "percentil ALTO = mais habitantes por farmácia = mercado menos saturado. "
            "Percentil BAIXO = muita farmácia para pouca gente."
        ),
        "_fontes": "populacao_municipios.01-POPULACAOTOTAL ÷ dados_farmacia_popular.totalfarmaciasnacidade",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--municipio")
    ap.add_argument("--uf")
    ap.add_argument("--lat", type=float)
    ap.add_argument("--lng", type=float)
    args = ap.parse_args()

    if args.municipio:
        achados = resolver_por_nome(args.municipio, args.uf)
        if not achados:
            B.emitir({"erro": f"município {args.municipio!r} não encontrado na base `municipios`"})
            return 1
        if len(achados) > 1:
            B.emitir({"erro": "nome ambíguo — informe --uf", "candidatos": achados})
            return 1
        municipio = achados[0]
    elif args.lat is not None and args.lng is not None:
        municipio = resolver_por_coordenada(args.lat, args.lng)
        if not municipio:
            B.emitir({"erro": "não foi possível inferir o município por coordenada"})
            return 1
    else:
        ap.error("informe --municipio (e --uf) ou --lat/--lng")

    codigo = str(municipio["codigo"]).strip()
    saida = {"municipio": municipio, "indicadores": {}, "lacunas": []}

    for base, (campos, pergunta) in MUNICIPAIS.items():
        try:
            indice = B.indexar_por_municipio(base)
        except FileNotFoundError as e:
            saida["lacunas"].append({"base": base, "motivo": str(e)})
            continue
        linha = indice.get(codigo)
        if not linha:
            saida["lacunas"].append({"base": base, "motivo": "município ausente nesta base", "responde": pergunta})
            continue
        bloco = {"_responde": pergunta, "_arquivo": B.achar(base).rsplit("\\", 1)[-1]}
        for campo in campos:
            bruto = linha.get(campo)
            valor = B.num(bruto)
            bloco[campo] = valor if valor is not None else (bruto or None)
            if bloco[campo] is None:
                saida["lacunas"].append({"base": base, "campo": campo, "motivo": "ausente ou erro de planilha"})
        saida["indicadores"][base] = bloco

    saida["saturacao"] = saturacao(codigo)
    saida["percentis"] = {
        "renda_media_domic_per_capita": percentil_municipal("renda_media_municipio", "Renda_media_domic_per_capita", codigo),
        "ipc": percentil_municipal("ranking_de_consumo", "IPC", codigo),
        "pib_per_capita": percentil_municipal("pib", "02-PIBPERCAPITA(EMR$)", codigo),
        "ifdm": percentil_municipal("firjan_ifdm_geral", "IFDM", codigo),
    }
    B.emitir(saida)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
