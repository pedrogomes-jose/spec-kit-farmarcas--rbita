"""Mercado farmacêutico da região pela UTC (unidade territorial de varejo).

Uso:
    python mercado_utc.py --codigo-ibge 3516200

Granularidade honesta: o dump NÃO permite localizar um ponto dentro de uma UTC
(ou de um brick IQVIA) — o polígono ficou no asset. O que dá é município → UTC.
Isso é EXATO para 5.378 dos 5.570 municípios (96,5%), que têm uma única UTC.
Nas cidades grandes (São Paulo tem 84 UTCs) o resultado é o agregado do
município, não o da vizinhança do ponto — e a saída diz isso.
"""

from __future__ import annotations

import argparse
import sys

sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
import _bases as B  # noqa: E402


def indexar_por_utc(prefixo: str) -> dict:
    saida = {}
    for linha in B.ler(prefixo):
        utc = (linha.get("utc_id_varejo") or "").strip()
        if utc:
            saida[utc] = linha
    return saida


def limpar(linha: dict) -> dict:
    fora = {"_id", "utc_id_varejo", "type", "assetFile"}
    return {k: (B.num(v) if B.num(v) is not None else v) for k, v in linha.items() if k not in fora}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--codigo-ibge", required=True)
    args = ap.parse_args()
    codigo = args.codigo_ibge.strip()

    utcs = []
    for linha in B.ler("closeup_utc_varejo"):
        if (linha.get("codigo_mun") or "").strip() == codigo:
            utcs.append(
                {
                    "utc_id_varejo": (linha.get("id_utc_var") or "").strip(),
                    "nome": (linha.get("nome_utc_v") or "").strip(),
                    "municipio": (linha.get("municipio") or "").strip(),
                    "uf": (linha.get("uf") or "").strip(),
                }
            )

    if not utcs:
        B.emitir({"erro": f"nenhuma UTC encontrada para o código IBGE {codigo}"})
        return 1

    bases = {
        "market_share_farmarcas": "mat_atual_utc_market_share",
        "crescimento": "mat_anterior_x_atual_utc_crescimento",
        "mix_categorias": "mat_anterior_x_atual_utc_mix_categorias",
        "mix_grupo_produto": "mat_atual_utc_grupo",
        "bandeiras_na_utc": "mat_atual_utc_bandeira",
        "cobertura": "mat_anterior_x_atual_utc_sem_cobertura",
    }
    indices = {}
    lacunas = []
    for rotulo, prefixo in bases.items():
        try:
            indices[rotulo] = indexar_por_utc(prefixo)
        except FileNotFoundError as e:
            lacunas.append({"base": prefixo, "motivo": str(e)})

    for utc in utcs:
        uid = utc["utc_id_varejo"]
        for rotulo, indice in indices.items():
            linha = indice.get(uid)
            utc[rotulo] = limpar(linha) if linha else None
            if linha is None:
                lacunas.append({"utc": uid, "base": bases[rotulo], "motivo": "UTC ausente nesta base"})

    # ATENÇÃO: esta base tem UMA LINHA POR UTC, não por município. Em cidade com
    # várias UTCs, pegar a primeira linha devolveria o número de uma UTC rotulado
    # como se fosse o do município. Somamos todas as linhas do código IBGE.
    linhas_fat = [limpar(l) for l in B.ler("faturamento_lojas_municipio_closeup")
                  if (l.get("codigoibge") or "").strip() == codigo]
    fat = None
    if linhas_fat:
        def soma(campo):
            vals = [x.get(campo) for x in linhas_fat if isinstance(x.get(campo), (int, float))]
            return round(sum(vals), 2) if vals else None
        fat = {
            "linhas_utc": len(linhas_fat),
            "receita_atual_total": soma("receita_atual_total"),
            "receita_anterior_total": soma("receita_anterior_total"),
            "detalhe_por_utc": linhas_fat,
        }
        if fat["receita_anterior_total"]:
            fat["crescimento"] = round(
                fat["receita_atual_total"] / fat["receita_anterior_total"] - 1, 4
            )

    # Total do município = soma das UTCs. A base `faturamento_lojas_municipio_closeup`
    # tem UMA linha por município (5.250 de 5.570) carregando o id de apenas UMA
    # das UTCs — em Franca o valor dela é idêntico ao de uma única UTC. Tratar
    # como PARCIAL, nunca como total do município.
    def somar(campo):
        vals = []
        for u in utcs:
            bloco = u.get("crescimento") or {}
            v = bloco.get(campo)
            if isinstance(v, (int, float)):
                vals.append(v)
        return round(sum(vals), 2) if vals else None

    mercado_municipio = {
        "_metodo": "soma das UTCs do município, a partir de mat_anterior_x_atual_utc_crescimento",
        "receita_atual_total": somar("receita_atual_total"),
        "receita_anterior_total": somar("receita_anterior_total"),
        "receita_atual_farmarcas": somar("receita_atual_farmarcas"),
    }
    if mercado_municipio["receita_anterior_total"]:
        mercado_municipio["crescimento"] = round(
            mercado_municipio["receita_atual_total"] / mercado_municipio["receita_anterior_total"] - 1, 4
        )
        mercado_municipio["_use_este_crescimento"] = (
            "é o do município inteiro; o crescimento de faturamento_closeup_PARCIAL é de UMA UTC só"
        )
    if mercado_municipio["receita_atual_total"] and mercado_municipio["receita_atual_farmarcas"] is not None:
        mercado_municipio["share_farmarcas_inferido"] = round(
            mercado_municipio["receita_atual_farmarcas"] / mercado_municipio["receita_atual_total"], 4
        )
        mercado_municipio["_aviso_share"] = (
            "INFERIDO da receita, não medido: a base mat_atual_utc_market_share pode não ter "
            "a UTC (ver bloco lacunas). Share ausente e share zero são coisas diferentes."
        )

    precisao = (
        "exata — o município tem uma única UTC"
        if len(utcs) == 1
        else f"AGREGADA — o município tem {len(utcs)} UTCs e o dump não permite localizar o ponto dentro de uma delas"
    )

    B.emitir(
        {
            "codigo_ibge": codigo,
            "precisao_geografica": precisao,
            "qtd_utcs": len(utcs),
            "utcs": utcs,
            "mercado_municipio_somado_utcs": mercado_municipio,
            "faturamento_closeup_PARCIAL": fat,
            "_aviso_closeup": "uma linha por município carregando o id de UMA UTC — parcial, não é o total do município",

            "lacunas": lacunas,
            "_nota_brick": "share por brick IQVIA NÃO é alcançável: `bricks_iqvia` veio sem polígono e `mat_atual_brick_*` só tem o número do brick",
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
