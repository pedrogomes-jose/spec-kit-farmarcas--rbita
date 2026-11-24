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


# Abaixo deste número de equipamentos etiquetados, a contagem do raio não
# distingue "bairro sem comércio" de "bairro sem mapeamento" — e o script abre o
# anel mais largo para mostrar o que existe um pouco além. PREMISSA declarada,
# não medida: nenhuma fonte diz quantos equipamentos descrevem um entorno.
POUCOS_EQUIPAMENTOS = 5
RAIO_AMPLIADO_M = 1500.0


def consulta(lat: float, lng: float, raio: float) -> str:
    partes = []
    for filtros in CATEGORIAS.values():
        for f in filtros:
            for tipo in ("node", "way"):
                partes.append(f'{tipo}{f}(around:{int(raio)},{lat},{lng});')
    corpo = "".join(partes)
    return f"[out:json][timeout:60];({corpo});out tags center;"


def consulta_de_controle(lat: float, lng: float, raio: float) -> str:
    """Conta TUDO que o OSM tem na área, com etiqueta ou sem.

    É o que separa as duas leituras que a contagem de equipamentos sozinha
    confunde: área sem comércio e área sem mapeamento devolvem o mesmo zero.
    Medido em Simões Filho/BA em 2026-11-12: 859 objetos dentro de 500 m e
    UM equipamento etiquetado. O bairro está mapeado; o que falta é etiqueta.
    Sem este número o relatório só podia dizer "ausência aqui não é ausência no
    mundo", que é verdade e não ajuda ninguém a decidir.
    """
    return f"[out:json][timeout:60];nwr(around:{int(raio)},{lat},{lng});out count;"


def buscar(pergunta: str, tentativas: int = 3):
    """Roda uma consulta no Overpass, com espelhos e backoff.

    Devolve (dados, origem). Resposta com `remark` é DESCARTADA: o Overpass
    responde HTTP 200 com resultado PARCIAL quando a consulta estoura tempo ou
    cota, e aceitá-la grava silêncio como se fosse dado — ainda por cima no
    cache, que não expira. Melhor tentar o próximo espelho e, se nenhum
    responder inteiro, devolver lacuna declarada.
    """
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
                if not bruto.lstrip().startswith("{"):
                    continue
                dados = json.loads(bruto)
                if dados.get("remark"):
                    continue
                return dados, url
            except (urllib.error.URLError, TimeoutError, ValueError):
                continue
        time.sleep(espera)
        espera *= 2
    return None, None


def com_cache(pergunta: str, chave: str):
    """Busca com cache em disco. Só grava resposta inteira — ver `buscar`."""
    arquivo = os.path.join(CACHE, f"{chave}.json")
    if os.path.exists(arquivo):
        with open(arquivo, encoding="utf-8") as fh:
            return json.load(fh), "cache local"
    dados, url = buscar(pergunta)
    if dados is None:
        return None, None
    with open(arquivo, "w", encoding="utf-8") as fh:
        json.dump(dados, fh)
    return dados, url


def marca_de(lat: float, lng: float, raio: float, sufixo: str = "") -> str:
    return hashlib.md5(f"{lat},{lng},{raio}{sufixo}".encode()).hexdigest()[:12]


def agrupar(dados: dict, lat: float, lng: float, listar: int, raio: float) -> dict:
    """Distribui os elementos nas categorias, já ordenados por distância.

    O corte por raio é refeito AQUI, contra a distância que o script publica, e
    não só pelo `around:` do Overpass. Os dois não medem a mesma coisa: o
    Overpass aceita o objeto cuja GEOMETRIA encosta no círculo, e `out center`
    devolve o CENTROIDE, que pode cair bem mais longe. Um polígono grande —
    praça, estádio, quadra de prédios — entrava na contagem do raio com a
    distância publicada maior que o próprio raio. Medido em Gurupi/TO em
    2026-11-23: "Praça Santo Antônio" contava dentro de 500 m com 513 m
    publicados, e por ser a única nomeada da categoria virava o exemplo da
    linha — o relatório nomeava, como gerador de fluxo do raio, justamente o
    equipamento de fora.

    Contar pelo número que o documento mostra é o que mantém contagem e
    distância conferíveis entre si. O que sai pelo corte não some: vai
    declarado em `fora_do_raio_pelo_centroide`.
    """
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
        item = {
            # Equipamento sem nome no OSM existe e conta; o nome é que falta.
            "nome": tags.get("name") or "",
            "tipo": tags.get("amenity") or tags.get("shop") or tags.get("building")
            or tags.get("railway") or tags.get("leisure") or tags.get("highway"),
            "distancia_m": round(B.haversine_m(lat, lng, la, lo)),
        }
        for cat in categorizar(tags):
            por_categoria[cat].append(item)

    resumo = {}
    for cat, itens in por_categoria.items():
        itens.sort(key=lambda x: x["distancia_m"])
        dentro = [x for x in itens if x["distancia_m"] <= raio]
        fora = len(itens) - len(dentro)
        resumo[cat] = {
            "total": len(dentro),
            "mais_proximo_m": dentro[0]["distancia_m"] if dentro else None,
            "itens": dentro[:listar],
        }
        if fora:
            resumo[cat]["fora_do_raio_pelo_centroide"] = fora
            resumo[cat]["_fora_do_raio_leitura"] = (
                f"{fora} equipamento(s) encostam no círculo de {int(raio)} m pela geometria, "
                "mas têm o centro além dele e ficam fora da contagem e dos exemplos — o "
                "mapa só devolve o centro, e contar aqui o que a distância publicada "
                "coloca fora deixaria as duas colunas em desacordo"
            )
    return resumo


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

    dados, origem = com_cache(
        consulta(args.lat, args.lng, args.raio), marca_de(args.lat, args.lng, args.raio)
    )
    if dados is None:
        B.emitir(
            {
                "erro": "Overpass indisponível ou resposta parcial nas tentativas feitas",
                "_leitura": "LACUNA, não ausência de equipamentos. Repetir mais tarde.",
                "espelhos_tentados": ESPELHOS,
                "ponto": {"lat": args.lat, "lng": args.lng, "raio_m": args.raio},
            }
        )
        return 1

    resumo = agrupar(dados, args.lat, args.lng, args.listar, args.raio)
    etiquetados = sum(1 for el in dados.get("elements", []) if el.get("tags"))

    # --- quanto do entorno está mapeado, com etiqueta ou sem
    controle, _ = com_cache(
        consulta_de_controle(args.lat, args.lng, args.raio),
        marca_de(args.lat, args.lng, args.raio, "-controle"),
    )
    tags_controle = (controle or {}).get("elements", [{}])
    tags_controle = (tags_controle[0].get("tags") or {}) if tags_controle else {}
    objetos = int(tags_controle.get("total") or 0) if controle else None
    cobertura = {
        "objetos_mapeados_no_raio": objetos,
        "nos": int(tags_controle.get("nodes") or 0) if controle else None,
        "vias": int(tags_controle.get("ways") or 0) if controle else None,
        "relacoes": int(tags_controle.get("relations") or 0) if controle else None,
        "equipamentos_etiquetados": etiquetados,
        "_leitura": (
            "objetos mapeados conta TUDO que o OSM tem na área — traçado de rua, "
            "edificação, nó solto —, com etiqueta de equipamento ou sem. Muitos "
            "objetos e poucos equipamentos quer dizer área mapeada e sem etiqueta, "
            "não área vazia. Poucos objetos quer dizer área não mapeada, e aí a "
            "contagem de equipamentos não descreve coisa nenhuma."
        ),
        "_diagnostico": (
            None if objetos is None else
            "área mapeada, equipamentos sem etiqueta" if objetos >= 100 and etiquetados < POUCOS_EQUIPAMENTOS
            else "área pouco mapeada — a contagem de equipamentos não é conclusiva" if objetos < 100
            else "área mapeada e com equipamentos etiquetados"
        ),
    }

    # --- anel mais largo, quando o raio pedido volta quase vazio
    ampliado = None
    if etiquetados < POUCOS_EQUIPAMENTOS and args.raio < RAIO_AMPLIADO_M:
        d2, _ = com_cache(
            consulta(args.lat, args.lng, RAIO_AMPLIADO_M),
            marca_de(args.lat, args.lng, RAIO_AMPLIADO_M),
        )
        if d2 is not None:
            ampliado = {
                "raio_m": RAIO_AMPLIADO_M,
                "equipamentos_etiquetados": sum(1 for el in d2.get("elements", []) if el.get("tags")),
                "categorias": agrupar(d2, args.lat, args.lng, args.listar, RAIO_AMPLIADO_M),
                "_por_que": (
                    f"o raio de {int(args.raio)} m devolveu menos de {POUCOS_EQUIPAMENTOS} "
                    "equipamentos etiquetados, o que não descreve o entorno. Este anel é "
                    "RECORTE DIFERENTE e não se soma ao outro: ele mostra o que existe um "
                    "pouco além, não o que está na calçada do ponto."
                ),
                "_premissa": (
                    f"o corte de {POUCOS_EQUIPAMENTOS} equipamentos e o raio de "
                    f"{int(RAIO_AMPLIADO_M)} m são premissa desta análise, não medida"
                ),
            }

    B.emitir(
        {
            "ponto": {"lat": args.lat, "lng": args.lng, "raio_m": args.raio},
            "_fonte": "OpenStreetMap via Overpass API",
            "_origem_da_consulta": origem,
            "categorias": resumo,
            "cobertura_do_mapa": cobertura,
            "anel_ampliado": ampliado,
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
