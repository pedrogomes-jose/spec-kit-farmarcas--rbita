"""Busca cirúrgica da geometria dos setores censitários de um município.

Uso:
    python malha_setores.py --codigo-ibge 2800308          # baixa e cacheia
    python malha_setores.py --codigo-ibge 2800308 --info    # só mostra o cache

Por que existe: o export do Órbita achatou `geometry` para o tipo. Os polígonos
ficaram no asset público `radar.farmarcas.com.br/orbita-assets/Setor
censitário.<ts>.<N>.json`, partido em fatias de ~4,5 MB. São ~220 partes,
~1 GB no total — baixar tudo para analisar um ponto é desperdício.

Como a busca é cirúrgica:
  1. As features do asset vêm na MESMA ordem do CSV `setor_censitario` do dump,
     e cada feature traz só `_id` + `geometry` (nenhum atributo).
  2. Os `_id` (ObjectId do Mongo) são monotonicamente crescentes.
  3. Logo dá para achar a parte que contém um `_id` alvo com busca binária,
     lendo só os ~300 primeiros bytes de cada parte candidata (HTTP Range).
  4. Baixamos apenas as partes que cobrem os setores do município.

O resultado é um GeoJSON por município em `cache/malha/<codigo>.geojson`, com
`CD_GEOCODI` já anexado em `properties` (vem do CSV, via `_id`).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
import _bases as B  # noqa: E402

ASSET_BASE = (
    "https://radar.farmarcas.com.br/orbita-assets/"
    "Setor%20censit%C3%A1rio.1631307285283.{parte}.json"
)
MAX_PARTES = 400  # limite superior da busca; partes inexistentes devolvem XML
CACHE_PARTES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache", "malha", "partes")
CACHE_MUNICIPIOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache", "malha")


def _url(parte: int) -> str:
    return ASSET_BASE.format(parte=parte)


def primeiro_id(parte: int):
    """Lê só o começo da parte e devolve o `_id` da primeira feature."""
    req = urllib.request.Request(_url(parte), headers={"Range": "bytes=0-400"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            cabeca = resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, TimeoutError):
        return None
    if "FeatureCollection" not in cabeca:
        return None
    marca = '"features": [{"_id":"'
    i = cabeca.find(marca)
    if i < 0:
        return None
    j = i + len(marca)
    return cabeca[j : cabeca.find('"', j)]


def ultima_parte_existente() -> int:
    """Busca binária pelo índice da última parte que existe."""
    baixo, alto = 0, MAX_PARTES
    while baixo < alto:
        meio = (baixo + alto + 1) // 2
        if primeiro_id(meio):
            baixo = meio
        else:
            alto = meio - 1
    return baixo


def baixar_parte(parte: int) -> dict:
    os.makedirs(CACHE_PARTES, exist_ok=True)
    destino = os.path.join(CACHE_PARTES, f"{parte:04d}.json")
    if os.path.exists(destino):
        with open(destino, encoding="utf-8") as fh:
            return json.load(fh)
    with urllib.request.urlopen(_url(parte), timeout=180) as resp:
        bruto = resp.read().decode("utf-8")
    with open(destino, "w", encoding="utf-8") as fh:
        fh.write(bruto)
    return json.loads(bruto)


def ids_do_municipio(codigo: str) -> dict:
    """Mapa `_id` -> CD_GEOCODI dos setores do município, lido do CSV do dump."""
    alvo = str(codigo).strip()
    saida = {}
    for linha in B.ler("setor_censitario"):
        if (linha.get("CD_GEOCODM") or "").strip() == alvo:
            oid = (linha.get("_id") or "").strip()
            if oid:
                saida[oid] = (linha.get("CD_GEOCODI") or "").strip()
    return saida


def parte_do_id(oid: str, ultima: int) -> int:
    """Busca binária: índice da parte cuja primeira feature é <= oid."""
    baixo, alto = 0, ultima
    while baixo < alto:
        meio = (baixo + alto + 1) // 2
        pid = primeiro_id(meio)
        if pid is None or pid > oid:
            alto = meio - 1
        else:
            baixo = meio
    return baixo


def construir(codigo: str, verbose: bool = True) -> str:
    destino = os.path.join(CACHE_MUNICIPIOS, f"{codigo}.geojson")
    if os.path.exists(destino):
        if verbose:
            print(f"já em cache: {destino}")
        return destino

    alvos = ids_do_municipio(codigo)
    if not alvos:
        raise SystemExit(f"nenhum setor com CD_GEOCODM={codigo} no CSV `setor_censitario`")

    ordenados = sorted(alvos)
    if verbose:
        print(f"setores do município no CSV: {len(alvos)}")

    ultima = ultima_parte_existente()
    inicio = parte_do_id(ordenados[0], ultima)
    if verbose:
        print(f"partes existentes: 0..{ultima} | varredura a partir da parte {inicio}")

    encontrados, features, parte = {}, [], inicio
    os.makedirs(CACHE_MUNICIPIOS, exist_ok=True)
    while parte <= ultima and len(encontrados) < len(alvos):
        dados = baixar_parte(parte)
        achou_nesta = 0
        for f in dados.get("features", []):
            oid = f.get("_id")
            if oid in alvos and oid not in encontrados:
                encontrados[oid] = True
                achou_nesta += 1
                features.append(
                    {
                        "type": "Feature",
                        "properties": {"_id": oid, "CD_GEOCODI": alvos[oid]},
                        "geometry": f.get("geometry"),
                    }
                )
        if verbose:
            print(f"  parte {parte}: {achou_nesta} setores | acumulado {len(encontrados)}/{len(alvos)}")
        # Passou do trecho do município e nada foi achado: para.
        if achou_nesta == 0 and encontrados:
            break
        parte += 1

    saida = {
        "type": "FeatureCollection",
        "_codigo_ibge": codigo,
        "_setores_no_csv": len(alvos),
        "_setores_com_geometria": len(features),
        "_fonte": "asset público do Órbita (radar.farmarcas.com.br/orbita-assets)",
        "features": features,
    }
    with open(destino, "w", encoding="utf-8") as fh:
        json.dump(saida, fh)
    if verbose:
        print(f"gravado: {destino} ({len(features)} de {len(alvos)} setores)")
    return destino


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--codigo-ibge", required=True)
    ap.add_argument("--info", action="store_true")
    args = ap.parse_args()

    destino = os.path.join(CACHE_MUNICIPIOS, f"{args.codigo_ibge}.geojson")
    if args.info:
        if not os.path.exists(destino):
            B.emitir({"em_cache": False, "caminho": destino})
            return 1
        with open(destino, encoding="utf-8") as fh:
            d = json.load(fh)
        B.emitir(
            {
                "em_cache": True,
                "caminho": destino,
                "setores_no_csv": d.get("_setores_no_csv"),
                "setores_com_geometria": d.get("_setores_com_geometria"),
            }
        )
        return 0

    construir(args.codigo_ibge)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
