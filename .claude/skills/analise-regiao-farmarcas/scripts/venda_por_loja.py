"""Quanto uma loja fatura, por duas fontes independentes.

Uso:
    python venda_por_loja.py --uf RN --municipio "São Gonçalo do Amarante"
    python venda_por_loja.py --uf RN --lat -5.75 --lng -35.30 --raio 30000
    python venda_por_loja.py --uf RN --bandeira "Maxi Popular" --modelo popular

DUAS FONTES, QUE NÃO SÃO A MESMA COISA

1. **Estimativa dos concorrentes** — campo de faturamento médio da camada
   Concorrentes. É **estimado**, está preenchido em menos da metade dos
   registros, e descreve o concorrente, não a nossa operação.

2. **Receita medida das lojas Farmarcas** — a planilha da IQVIA por brick traz
   `codigo_cnpj` nas linhas do grupo, e o cadastro de lojas traz o mesmo CNPJ
   com bandeira, modelo, status e coordenada. Cruzando os dois, sai a **receita
   medida por loja nossa**, não estimada — e dá para filtrar pela bandeira
   pretendida, que é a pergunta que o analista realmente faz.

A segunda é mais forte e tem limites próprios, todos declarados na saída.

PERIODICIDADE — a armadilha
`MAT atual` é *Moving Annual Total*: a receita acumulada de **12 meses**, não a
de um mês. Dividir por 12 só vale para loja que operou o período inteiro; loja
aberta no meio aparece baixa sem ser pequena. Por isso a saída traz os dois
valores e usa quartis, que aguentam o outlier, em vez de média.
"""

from __future__ import annotations

import argparse
import collections
import csv
import os
import sys

sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
import _bases as B  # noqa: E402

CACHE_IQVIA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache", "iqvia_brick.csv")
MESES_MAT = 12


def quartis(valores: list) -> dict:
    limpos = sorted(v for v in valores if v is not None and v > 0)
    if not limpos:
        return {"lojas": 0}

    def q(f):
        if len(limpos) == 1:
            return limpos[0]
        pos = f * (len(limpos) - 1)
        b = int(pos)
        a = min(b + 1, len(limpos) - 1)
        return limpos[b] + (limpos[a] - limpos[b]) * (pos - b)

    return {
        "lojas": len(limpos),
        "minimo": round(limpos[0], 2),
        "q1": round(q(0.25), 2),
        "mediana": round(q(0.50), 2),
        "q3": round(q(0.75), 2),
        "maximo": round(limpos[-1], 2),
    }


def receita_por_cnpj() -> dict:
    """Receita MAT e unidades por CNPJ das lojas do grupo, da base da IQVIA."""
    if not os.path.exists(CACHE_IQVIA):
        raise FileNotFoundError(
            "base da IQVIA por brick não preparada. Rode uma vez, da raiz do projeto: "
            "python .claude/skills/analise-regiao-farmarcas/scripts/preparar_iqvia_brick.py"
        )
    acc: dict = collections.defaultdict(lambda: {"receita": 0.0, "unidades": 0.0})
    with open(CACHE_IQVIA, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            if r["provedor_descricao_grupo"] != "GRUPO FARMARCAS" or r["flag_mat"] != "MAT atual":
                continue
            cnpj = (r["codigo_cnpj"] or "").strip()
            rec, uni = B.num(r["preco_consumidor"]), B.num(r["unidade"])
            if cnpj and rec and uni:
                acc[cnpj]["receita"] += rec
                acc[cnpj]["unidades"] += uni
    return acc


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--uf")
    ap.add_argument("--municipio")
    ap.add_argument("--bandeira")
    ap.add_argument("--modelo", choices=["popular", "convencional"])
    ap.add_argument("--lat", type=float)
    ap.add_argument("--lng", type=float)
    ap.add_argument("--raio", type=float, default=30000.0, help="metros, quando --lat/--lng")
    ap.add_argument("--min-receita-ano", type=float, default=120_000.0,
                    help="piso para descartar loja aberta no meio do período")
    args = ap.parse_args()

    try:
        iqvia = receita_por_cnpj()
    except FileNotFoundError as e:
        B.emitir({"erro": str(e)})
        return 1

    sem_cadastro = 0

    # índice do cadastro por CNPJ
    cadastro = {}
    for l in B.ler_cadastro_lojas():
        c = (l.get("CNPJ") or "").strip()
        if c:
            cadastro[c] = l

    registros = []
    for cnpj, dados in iqvia.items():
        loja = cadastro.get(cnpj)
        if loja is None:
            sem_cadastro += 1
            continue
        lat = B.num(loja.get("Latitude - Endereço Receita"))
        lng = B.num(loja.get("Longitude - Endereço Receita"))
        dist = None
        if args.lat is not None and args.lng is not None and B.coordenada_valida(lat, lng):
            dist = B.haversine_m(args.lat, args.lng, lat, lng)
        registros.append(
            {
                "uf": (loja.get("Estado - Endereço Receita") or "").strip().upper(),
                "municipio": (loja.get("Cidade - Endereço Receita") or "").strip(),
                "bandeira": (loja.get("Bandeira") or "").strip(),
                "modelo": (loja.get("Modelo de Negócio") or "").strip(),
                "status": (loja.get("Status") or "").strip(),
                "receita_ano": dados["receita"],
                "unidades_ano": dados["unidades"],
                "distancia_m": round(dist) if dist is not None else None,
            }
        )

    def filtrar(r) -> bool:
        if r["status"] not in B.STATUS_OCUPA_VAGA:
            return False
        if r["receita_ano"] < args.min_receita_ano:
            return False
        if args.uf and r["uf"] != args.uf.strip().upper():
            return False
        if args.municipio and B.normalizar(r["municipio"]) != B.normalizar(args.municipio):
            return False
        if args.bandeira and B.normalizar(r["bandeira"]) != B.normalizar(args.bandeira):
            return False
        if args.modelo and B.normalizar(r["modelo"]) != B.normalizar(args.modelo):
            return False
        if args.lat is not None and (r["distancia_m"] is None or r["distancia_m"] > args.raio):
            return False
        return True

    def bloco(sel: list, rotulo: str) -> dict:
        ano = quartis([r["receita_ano"] for r in sel])
        if not ano.get("lojas"):
            return {"recorte": rotulo, "lojas": 0, "_leitura": "nenhuma loja do grupo neste recorte"}
        mes = {k: (round(v / MESES_MAT, 2) if k != "lojas" else v) for k, v in ano.items()}
        return {"recorte": rotulo, "receita_ano_R$": ano, "receita_mes_R$": mes}

    recortes = []
    sel = [r for r in registros if filtrar(r)]
    alvo = []
    if args.municipio:
        alvo.append(args.municipio)
    if args.lat is not None:
        alvo.append(f"raio de {int(args.raio)} m")
    if args.bandeira:
        alvo.append(args.bandeira)
    if args.modelo:
        alvo.append(args.modelo)
    recortes.append(bloco(sel, " + ".join(alvo) if alvo else "tudo"))

    # recortes de contexto, para o número não ficar sozinho
    if args.uf:
        na_uf = [r for r in registros if r["status"] in B.STATUS_OCUPA_VAGA
                 and r["receita_ano"] >= args.min_receita_ano
                 and r["uf"] == args.uf.strip().upper()]
        recortes.append(bloco(na_uf, f"toda a UF {args.uf.strip().upper()}"))
        if args.bandeira:
            band_uf = [r for r in na_uf if B.normalizar(r["bandeira"]) == B.normalizar(args.bandeira)]
            recortes.append(bloco(band_uf, f"{args.bandeira} na UF {args.uf.strip().upper()}"))
    nacional = [r for r in registros if r["status"] in B.STATUS_OCUPA_VAGA
                and r["receita_ano"] >= args.min_receita_ano]
    recortes.append(bloco(nacional, "rede inteira"))
    if args.bandeira:
        band_nac = [r for r in nacional if B.normalizar(r["bandeira"]) == B.normalizar(args.bandeira)]
        recortes.append(bloco(band_nac, f"{args.bandeira} na rede inteira"))

    B.emitir(
        {
            "filtro": {
                "uf": args.uf, "municipio": args.municipio, "bandeira": args.bandeira,
                "modelo": args.modelo,
                "raio_m": args.raio if args.lat is not None else None,
            },
            "_fonte": "receita medida da IQVIA por CNPJ, cruzada com o cadastro de lojas",
            "_periodicidade": (
                "MAT atual é a receita acumulada de 12 meses; o valor mensal é essa receita "
                "dividida por 12, o que só vale para loja que operou o período inteiro"
            ),
            "recortes": recortes,
            "cobertura": {
                "cnpjs_na_iqvia": len(iqvia),
                "casados_com_o_cadastro": len(registros),
                "sem_cadastro": sem_cadastro,
                "descartados_por_receita_minima": sum(
                    1 for r in registros if r["receita_ano"] < args.min_receita_ano
                ),
                "_piso": f"R$ {args.min_receita_ano:,.0f} ao ano, para tirar loja aberta no meio do período",
            },
            "_limites": {
                "carteira": "a base reflete a carteira ATUAL do grupo, com histórico retroagido: "
                            "loja que saiu foi apagada para trás",
                "cobertura": "cerca de um quarto dos CNPJs da IQVIA não casa com o cadastro",
                "o_que_mede": "receita de loja DO GRUPO, não do concorrente — é o que a rede "
                              "fatura numa praça assim, não o que o mercado todo fatura",
            },
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
