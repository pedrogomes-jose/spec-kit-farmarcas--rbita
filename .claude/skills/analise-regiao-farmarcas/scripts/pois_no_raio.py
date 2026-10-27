"""Geradores de fluxo no raio: hospitais, creches, escolas, mercados e afins.

Uso:
    python pois_no_raio.py --lat -10.911123 --lng -37.049093 --raio 500

Responde à pergunta "o que existe em volta que traz gente para cá?" — que o
dump não responde, porque `bancos`, `clinicas_oftalmologicas` e `farmacias`
vieram sem coordenada e `barreiras_geograficas` sem polígono.

Fonte: **OpenStreetMap**, via Overpass API pública e gratuita. Cobertura é
irregular fora dos grandes centros: ausência no OSM NÃO é ausência no mundo.
O resultado é cacheado por ponto+raio para não repetir consulta.

Isto não substitui fluxo de passantes. Contagem de equipamentos é um proxy
fraco: diz que há geradores de fluxo, não quanta gente passa.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
import _bases as B  # noqa: E402

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache", "pois")

ESPELHOS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.osm.jp/api/interpreter",
]

# categoria -> lista de filtros OSM. Escolhidas por serem geradoras de fluxo
# relevantes para farmácia de rua.
CATEGORIAS = {
    "saude": ['["amenity"~"^(hospital|clinic|doctors|health_post)$"]'],
    "creche_escola": ['["amenity"~"^(kindergarten|school|college|university)$"]'],
    "mercado_supermercado": ['["shop"~"^(supermarket|convenience|greengrocer)$"]'],
    "banco_loteria": ['["amenity"~"^(bank|bureau_de_change)$"]', '["shop"="lottery"]'],
    "transporte": ['["amenity"="bus_station"]', '["railway"~"^(station|tram_stop)$"]', '["highway"="bus_stop"]'],
    "moradia_coletiva": ['["building"~"^(apartments|residential)$"]'],
    "moradia_individual": ['["building"~"^(house|detached|semidetached_house)$"]'],
    "comercio_servicos": ['["shop"]', '["amenity"~"^(restaurant|cafe|fast_food|pharmacy)$"]'],
    "lazer_culto": ['["amenity"~"^(place_of_worship|gym)$"]', '["leisure"~"^(park|fitness_centre|stadium)$"]'],
}


def consulta(lat: float, lng: float, raio: float) -> str:
    partes = []
    for filtros in CATEGORIAS.values():
        for f in filtros:
            for tipo in ("node", "way"):
                partes.append(f'{tipo}{f}(around:{int(raio)},{lat},{lng});')
    corpo = "".join(partes)
    return f"[out:json][timeout:60];({corpo});out tags center;"


def buscar(lat: float, lng: float, raio: float, tentativas: int = 3):
    """Consulta o Overpass com espelhos e backoff. Devolve (dados, origem)."""
    pergunta = consulta(lat, lng, raio)
    dados_post = urllib.parse.urlencode({"data": pergunta}).encode("utf-8")
    espera = 4
    for tentativa in range(tentativas):
        for url in ESPELHOS:
            req = urllib.request.Request(
                url,
                data=dados_post,
                headers={
                    "User-Agent": "orbita-analise-regiao/1.0 (uso interno Farmarcas)",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )
            try:
                with urllib.request.urlopen(req, timeout=90) as resp:
                    bruto = resp.read().decode("utf-8", errors="replace")
                if bruto.lstrip().startswith("{"):
                    return json.loads(bruto), url
            except (urllib.error.URLError, TimeoutError, ValueError):
                continue
        time.sleep(espera)
        espera *= 2
    return None, None


def categorizar(tags: dict) -> list:
    saida = []
    amenity = tags.get("amenity", "")
    shop = tags.get("shop", "")
    building = tags.get("building", "")
    railway = tags.get("railway", "")
    leisure = tags.get("leisure", "")
    highway = tags.get("highway", "")
    if amenity in ("hospital", "clinic", "doctors", "health_post"):
        saida.append("saude")
    if amenity in ("kindergarten", "school", "college", "university"):
        saida.append("creche_escola")
    if shop in ("supermarket", "convenience", "greengrocer"):
        saida.append("mercado_supermercado")
    if amenity in ("bank", "bureau_de_change") or shop == "lottery":
        saida.append("banco_loteria")
    if amenity == "bus_station" or railway in ("station", "tram_stop") or highway == "bus_stop":
        saida.append("transporte")
    if building in ("apartments", "residential"):
        saida.append("moradia_coletiva")
    if building in ("house", "detached", "semidetached_house"):
        saida.append("moradia_individual")
    if shop or amenity in ("restaurant", "cafe", "fast_food", "pharmacy"):
        saida.append("comercio_servicos")
    if amenity in ("place_of_worship", "gym") or leisure in ("park", "fitness_centre", "stadium"):
        saida.append("lazer_culto")
    return saida


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lat", type=float, required=True)
    ap.add_argument("--lng", type=float, required=True)
    ap.add_argument("--raio", type=float, default=500.0)
    ap.add_argument("--listar", type=int, default=10)
    args = ap.parse_args()

    os.makedirs(CACHE, exist_ok=True)
    marca = hashlib.md5(f"{args.lat},{args.lng},{args.raio}".encode()).hexdigest()[:12]
    arquivo = os.path.join(CACHE, f"{marca}.json")

    origem = "cache local"
    if os.path.exists(arquivo):
        with open(arquivo, encoding="utf-8") as fh:
            dados = json.load(fh)
    else:
        dados, url = buscar(args.lat, args.lng, args.raio)
        if dados is None:
            B.emitir(
                {
                    "erro": "Overpass indisponível nas tentativas feitas",
                    "_leitura": "LACUNA, não ausência de equipamentos. Repetir mais tarde.",
                    "espelhos_tentados": ESPELHOS,
                    "ponto": {"lat": args.lat, "lng": args.lng, "raio_m": args.raio},
                }
            )
            return 1
        with open(arquivo, "w", encoding="utf-8") as fh:
            json.dump(dados, fh)
        origem = url

    por_categoria: dict[str, list] = {c: [] for c in CATEGORIAS}
    vistos = set()
    for el in dados.get("elements", []):
        tags = el.get("tags") or {}
        if not tags:
            continue
        centro = el.get("center") or {"lat": el.get("lat"), "lon": el.get("lon")}
        la, lo = centro.get("lat"), centro.get("lon")
        if la is None or lo is None:
            continue
        chave = (round(la, 6), round(lo, 6), tags.get("name", ""))
        if chave in vistos:
            continue
        vistos.add(chave)
        dist = round(B.haversine_m(args.lat, args.lng, la, lo))
        item = {
            # Equipamento sem nome no OSM existe e conta; o nome é que falta.
            "nome": tags.get("name") or "",
            "tipo": tags.get("amenity") or tags.get("shop") or tags.get("building") or tags.get("railway") or tags.get("leisure") or tags.get("highway"),
            "distancia_m": dist,
        }
        for cat in categorizar(tags):
            por_categoria[cat].append(item)

    resumo = {}
    for cat, itens in por_categoria.items():
        itens.sort(key=lambda x: x["distancia_m"])
        resumo[cat] = {
            "total": len(itens),
            "mais_proximo_m": itens[0]["distancia_m"] if itens else None,
            "itens": itens[: args.listar],
        }

    B.emitir(
        {
            "ponto": {"lat": args.lat, "lng": args.lng, "raio_m": args.raio},
            "_fonte": "OpenStreetMap via Overpass API",
            "_origem_da_consulta": origem,
            "categorias": resumo,
            "_limites": {
                "cobertura": "o OSM é colaborativo; ausência aqui não é ausência no mundo real",
                "fluxo": "contagem de equipamentos é proxy FRACO de fluxo — não substitui contagem de passantes",
                "moradia": "contagem de edificações depende de mapeamento de prédios, muito irregular no Brasil",
            },
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
