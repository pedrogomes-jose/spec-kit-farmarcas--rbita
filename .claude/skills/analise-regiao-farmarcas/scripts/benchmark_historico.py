"""Referência vinda do histórico real de análises, não de faixa inventada.

Uso:
    python benchmark_historico.py --lat -20.5386 --lng -47.4006 --vizinhanca 5000
    python benchmark_historico.py --panorama

Responde duas perguntas que nenhuma régua absoluta responde:
  1. O que já se analisou PERTO daqui, e o que se decidiu?
  2. Qual é a prática corrente — raio usado, camadas usadas, taxa de aprovação?

LGPD: nome e e-mail de consultor, analista e empresário existem na base e são
DESCARTADOS aqui. O texto do parecer só sai com --com-parecer, e mesmo assim
nunca deve ser copiado para o dossiê com nome de pessoa.
"""

from __future__ import annotations

import argparse
import collections
import sys

sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
import _bases as B  # noqa: E402

MAX_SOURCES = 40
MAX_COMENTARIOS = 6


def percentil(valores: list[float], alvo: float):
    """Em que percentil `alvo` cai na distribuição de `valores`."""
    limpos = sorted(v for v in valores if v is not None)
    if not limpos:
        return None
    abaixo = sum(1 for v in limpos if v < alvo)
    return round(100.0 * abaixo / len(limpos))


def camadas(linha: dict) -> list[str]:
    nomes = []
    for i in range(MAX_SOURCES):
        nome = (linha.get(f"map.sources[{i}].name") or "").strip()
        if nome:
            nomes.append(nome)
    return nomes


def parecer(linha: dict) -> str:
    partes = []
    for i in range(MAX_COMENTARIOS):
        txt = (linha.get(f"comment[{i}].text") or "").strip()
        if txt:
            partes.append(txt)
    return " || ".join(partes)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lat", type=float)
    ap.add_argument("--lng", type=float)
    ap.add_argument("--vizinhanca", type=float, default=5000.0, help="metros")
    ap.add_argument("--panorama", action="store_true")
    ap.add_argument("--com-parecer", action="store_true")
    ap.add_argument("--listar", type=int, default=10)
    args = ap.parse_args()

    if not args.panorama and (args.lat is None or args.lng is None):
        ap.error("informe --lat/--lng ou use --panorama")

    total = 0
    situacoes = collections.Counter()
    uso_camada = collections.Counter()
    raios: list[float] = []
    com_coord = 0
    perto = []

    for linha in B.ler("all_expansion.analysis_data"):
        total += 1
        situacoes[(linha.get("analysisSituationDescription") or "(vazio)").strip()] += 1
        for nome in camadas(linha):
            uso_camada[nome] += 1
        raio = B.num(linha.get("map.radius"))
        if raio:
            raios.append(raio)
        la, lo = B.num(linha.get("map.main.location.lat")), B.num(linha.get("map.main.location.lng"))
        if la is None or lo is None:
            continue
        com_coord += 1
        if args.lat is None:
            continue
        dist = B.haversine_m(args.lat, args.lng, la, lo)
        if dist <= args.vizinhanca:
            reg = {
                "distancia_m": round(dist),
                "situacao": (linha.get("analysisSituationDescription") or "").strip() or None,
                "status": (linha.get("analysisStatusDescription") or "").strip() or None,
                "bandeira": (linha.get("brandDescription") or "").strip() or None,
                "tipo": (linha.get("analysisType") or "").strip() or None,
                "raio_m": raio,
                "endereco": (linha.get("map.main.location.address") or "").strip() or None,
                "cidade": (linha.get("map.main.location.city") or "").strip() or None,
                "criada_em": (linha.get("createdAt") or "").strip() or None,
                "camadas_usadas": camadas(linha),
            }
            if args.com_parecer:
                reg["parecer_registrado"] = parecer(linha) or None
            perto.append(reg)

    perto.sort(key=lambda r: r["distancia_m"])
    raios_ordenados = sorted(raios)

    saida = {
        "panorama": {
            "analises_na_base": total,
            "com_coordenada": com_coord,
            "situacoes": dict(situacoes.most_common()),
            "camadas_mais_usadas": dict(uso_camada.most_common(20)),
            "raio_m": {
                "mediana": raios_ordenados[len(raios_ordenados) // 2] if raios_ordenados else None,
                "minimo": raios_ordenados[0] if raios_ordenados else None,
                "maximo": raios_ordenados[-1] if raios_ordenados else None,
                "n": len(raios_ordenados),
            },
        },
        "_leitura": (
            "A lista de camadas mais usadas é a régua tácita do time: é o que os analistas "
            "de fato abrem. Serve para escolher o que entra no dossiê sem exigir conhecimento prévio."
        ),
        "_aviso_preditivo": (
            "Parecer aprovado x reprovado NÃO tem poder preditivo medido sobre a sobrevivência "
            "da loja (log-rank p=0,8275, 101 fechamentos) — ver analise-ponto-orbita/README.md. "
            "Usar a vizinhança como CONTEXTO do que já se discutiu ali, nunca como prognóstico."
        ),
    }

    if args.lat is not None:
        aprov = sum(1 for r in perto if (r["situacao"] or "").upper().startswith("APROV"))
        repr_ = sum(1 for r in perto if (r["situacao"] or "").upper().startswith("REPROV"))
        saida["vizinhanca"] = {
            "raio_busca_m": args.vizinhanca,
            "analises_encontradas": len(perto),
            "aprovadas": aprov,
            "reprovadas": repr_,
            "mais_proximas": perto[: args.listar],
        }
        if raios_ordenados:
            saida["vizinhanca"]["_percentil_do_raio_padrao_300m"] = percentil(raios_ordenados, 300.0)

    B.emitir(saida)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
