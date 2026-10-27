"""Preço médio por unidade e tamanho de mercado no brick IQVIA.

Uso:
    python mercado_brick.py --codigo-ibge 2800308 --uf SE \
        --lat -10.911123 --lng -37.049093
    python mercado_brick.py --uf SE --brick "994-SE_AJU_CENTRO"

Fonte: `cache/iqvia_brick.csv`, gerado por `preparar_iqvia_brick.py` a partir da
aba `DADOS POR BRICK E UTC`. É a única base do acervo com **unidades vendidas**,
e por isso a única que permite preço:

    preço médio por unidade = preco_consumidor / unidade

`preco_consumidor` é RECEITA a preço de consumidor, não preço unitário.

COMO O BRICK É LOCALIZADO — e por que não é exato:
O dump não permite dizer em qual brick um ponto cai (`bricks_iqvia` veio sem
polígono). O nome do brick traz UF e, nas cidades grandes, o BAIRRO:
`994-SE_AJU_CENTRO`. Em cidade grande o município vem abreviado (Aracaju = AJU,
Belo Horizonte = BH), então casar pelo nome do município falha. Casamos por
**UF + bairro do ponto**, e devolvemos também o agregado da UF como referência.
Toda a saída diz qual critério casou.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys

sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
import _bases as B  # noqa: E402

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache", "iqvia_brick.csv")


def ler_iqvia():
    if not os.path.exists(CACHE):
        raise FileNotFoundError(
            "base IQVIA por brick não preparada. Rode uma vez, da raiz do projeto: "
            "python .claude/skills/analise-regiao-farmarcas/scripts/preparar_iqvia_brick.py"
        )
    with open(CACHE, encoding="utf-8", newline="") as fh:
        for linha in csv.DictReader(fh):
            yield linha


def bairro_do_ponto(lat: float, lng: float, codigo_ibge: str):
    """Bairro cujo centroide está mais perto do ponto, dentro do município."""
    alvo_mun = str(codigo_ibge).strip()
    melhor = None
    for b in B.ler("bairros"):
        if (b.get("CODMUN") or "").strip() != alvo_mun:
            continue
        la, lo = B.num(b.get("Lat_C")), B.num(b.get("Lon_C"))
        if not B.coordenada_valida(la, lo):
            continue
        d = B.haversine_m(lat, lng, la, lo)
        if melhor is None or d < melhor[0]:
            melhor = (d, (b.get("NOME") or "").strip())
    if not melhor:
        return None, None
    return melhor[1], round(melhor[0])


def agregar(linhas, so_mat_atual=True):
    """Soma unidades e receita, e devolve o preço médio por unidade."""
    uni = rec = 0.0
    n = 0
    por_grupo = {}
    for r in linhas:
        if so_mat_atual and r["flag_mat"] != "MAT atual":
            continue
        u, p = B.num(r["unidade"]), B.num(r["preco_consumidor"])
        if u is None or p is None or u <= 0:
            continue
        uni += u
        rec += p
        n += 1
        g = r["provedor_descricao_grupo"]
        acc = por_grupo.setdefault(g, [0.0, 0.0])
        acc[0] += u
        acc[1] += p
    if not n:
        return None
    saida = {
        "unidades": round(uni),
        "receita_R$": round(rec, 2),
        "preco_medio_por_unidade_R$": round(rec / uni, 2),
        "linhas_agregadas": n,
    }
    saida["por_grupo"] = {
        g: {
            "unidades": round(v[0]),
            "receita_R$": round(v[1], 2),
            "preco_medio_por_unidade_R$": round(v[1] / v[0], 2) if v[0] else None,
        }
        for g, v in sorted(por_grupo.items())
    }
    return saida


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--uf", required=True)
    ap.add_argument("--codigo-ibge")
    ap.add_argument("--lat", type=float)
    ap.add_argument("--lng", type=float)
    ap.add_argument("--brick", help="nome exato do brick, se já souber")
    args = ap.parse_args()

    uf = args.uf.strip().upper()
    try:
        todas = list(ler_iqvia())
    except FileNotFoundError as e:
        B.emitir({"erro": str(e)})
        return 1

    da_uf = [r for r in todas if (r["codigo_uf"] or "").strip().upper() == uf]
    if not da_uf:
        B.emitir({"erro": f"nenhum brick da UF {uf} na base IQVIA"})
        return 1

    bairro = dist = None
    if args.lat is not None and args.lng is not None and args.codigo_ibge:
        bairro, dist = bairro_do_ponto(args.lat, args.lng, args.codigo_ibge)

    criterio = None
    alvo = []
    if args.brick:
        alvo = [r for r in da_uf if r["descricao_brick_rpe"].strip().upper() == args.brick.strip().upper()]
        criterio = f"nome exato do brick informado ({args.brick})"
    if not alvo and bairro:
        chave = B.normalizar(bairro)
        alvo = [r for r in da_uf if B.normalizar(r["descricao_brick_rpe"]).endswith("_" + chave)]
        if alvo:
            criterio = f"UF + bairro do ponto ({bairro}, centroide a {dist} m)"
    if not alvo and args.codigo_ibge:
        nome = None
        for m in B.ler("municipios"):
            if (m.get("CD_MUN") or "").strip() == str(args.codigo_ibge).strip():
                nome = m.get("NM_MUN")
                break
        if nome:
            chave = B.normalizar(nome)
            alvo = [r for r in da_uf if chave in B.normalizar(r["descricao_brick_rpe"])]
            if alvo:
                criterio = f"UF + nome do município ({nome})"

    bricks = sorted({r["descricao_brick_rpe"] for r in alvo})

    B.emitir(
        {
            "uf": uf,
            "bairro_do_ponto": bairro,
            "distancia_ao_centroide_do_bairro_m": dist,
            "criterio_de_casamento": criterio or "nenhum — só o agregado da UF está disponível",
            "bricks_casados": bricks,
            "brick": agregar(alvo) if alvo else None,
            "uf_inteira": agregar(da_uf),
            "_leitura": (
                "preço médio por unidade = receita a preço de consumidor ÷ unidades vendidas, "
                "no MAT atual. Compare o brick contra a UF: preço acima da UF indica mix mais caro "
                "ou menos pressão de desconto na região"
            ),
            "_limites": {
                "localizacao": "o dump não diz em qual brick o ponto cai; o casamento é por nome",
                "abreviacao": "cidade grande vem abreviada no nome do brick (Aracaju=AJU, Belo Horizonte=BH)",
                "carteira": "a base IQVIA é a carteira ATUAL da Farmarcas, com histórico retroagido",
            },
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
