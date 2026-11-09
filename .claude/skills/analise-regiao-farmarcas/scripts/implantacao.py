"""Implantação do ponto na malha viária: esquina, meio de quadra, cruzamento.

Uso:
    python implantacao.py --lat -15.468705 --lng -58.352849

Responde "onde exatamente este endereço está na quadra?", que muda a leitura de
um ponto de rua mais do que quase qualquer indicador de área: esquina tem duas
faces de exposição e recebe fluxo de duas vias; meio de quadra tem uma.

Fonte: **OpenStreetMap**, via Overpass API pública. A geometria viária do OSM é
boa em cidade e irregular em distrito pequeno.

REGRA DE SAÍDA: este script só afirma com **confiança alta**. Quando a
geometria não sustenta uma classificação, devolve `classificacao: null` e quem
consome **omite o assunto** — não escreve "não foi possível determinar". Uma
linha dizendo que não se sabe onde o ponto está na quadra não ajuda ninguém a
decidir, e gasta a atenção que as lacunas reais precisam.

As três portas que precisam estar abertas para afirmar:

1. **Ancoragem** — o ponto tem de estar a no máximo `--max-ancoragem` metros de
   uma via mapeada. Mais longe que isso, ou a coordenada está errada, ou a via
   não está no mapa, e nos dois casos a classificação descreveria outra coisa.
2. **Separação** — esquina e meio de quadra são afirmados em faixas que não se
   tocam. Entre elas há uma zona morta, deliberada: ponto a 35 m de um
   cruzamento é "perto da esquina" na fala do analista e não tem classificação
   defensável no dado.
3. **Nomeação** — um cruzamento só conta quando as vias que se cruzam têm nome
   e os nomes diferem. Nó compartilhado por dois trechos da mesma rua é
   continuidade de via, não esquina.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
import _bases as B  # noqa: E402

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache", "viario")

ESPELHOS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.osm.jp/api/interpreter",
]

# Vias que carregam gente a pé ou de carro até uma farmácia. Fora dessa lista
# ficam trilha, ciclovia, servidão e via de acesso restrito, que não definem a
# implantação comercial de um ponto.
VIAS = (
    "motorway|trunk|primary|secondary|tertiary|unclassified|residential|"
    "living_street|pedestrian|motorway_link|trunk_link|primary_link|"
    "secondary_link|tertiary_link"
)

# Hierarquia OSM -> como o analista chama. "avenida" aqui é porte da via, não o
# nome dela: uma via secundária chamada "Rua X" continua sendo via de porte.
PORTE = {
    "motorway": "via expressa",
    "trunk": "via expressa",
    "primary": "avenida principal",
    "secondary": "avenida",
    "tertiary": "via coletora",
    "residential": "rua residencial",
    "living_street": "rua de convívio",
    "pedestrian": "calçadão",
    "unclassified": "via local",
}

# Os cortes que separam as duas afirmações, com a zona morta entre elas.
#
# Calibrados contra a geometria de quadra, não contra o que seria conveniente
# afirmar. A quadra urbana brasileira tem tipicamente 80 a 120 m, então um ponto
# em meio de quadra fica a 40–60 m da esquina mais próxima. A primeira
# calibração exigia 60 m para afirmar meio de quadra — e com isso excluía o caso
# normal por construção: testada em quatro endereços reais, abstinha-se em todos,
# inclusive num calçadão a 55 m do cruzamento. O corte estava errado, não o dado.
#
# Esquina é o lote de canto: até 20 m do nó de cruzamento. Acima de 40 m o ponto
# claramente não ocupa canto. Entre os dois fica a zona morta, onde a fala do
# analista diria "perto da esquina" e o dado não sustenta nenhuma das duas.
MAX_ANCORAGEM = 20.0   # distância máxima do ponto à via mapeada mais próxima
CORTE_ESQUINA = 20.0   # até aqui o ponto ocupa o lote de canto
CORTE_MEIO = 40.0      # a partir daqui o ponto claramente não ocupa canto


def consulta(lat: float, lng: float, raio: float) -> str:
    return (
        f"[out:json][timeout:60];"
        f'way["highway"~"^({VIAS})$"](around:{int(raio)},{lat},{lng});'
        f"out tags geom;"
    )


def buscar(lat: float, lng: float, raio: float, tentativas: int = 3):
    """Consulta o Overpass com espelhos e backoff. Devolve (dados, origem)."""
    os.makedirs(CACHE, exist_ok=True)
    chave = hashlib.sha1(f"{lat:.6f},{lng:.6f},{int(raio)}".encode()).hexdigest()[:16]
    arq = os.path.join(CACHE, f"{chave}.json")
    if os.path.exists(arq):
        with open(arq, encoding="utf-8") as fh:
            guardado = json.load(fh)
        return guardado.get("dados"), guardado.get("origem")

    pergunta = consulta(lat, lng, raio)
    dados_post = urllib.parse.urlencode({"data": pergunta}).encode("utf-8")
    espera = 4
    for _ in range(tentativas):
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
                    dados = json.loads(bruto)
                    with open(arq, "w", encoding="utf-8") as fh:
                        json.dump({"dados": dados, "origem": url}, fh)
                    return dados, url
            except (urllib.error.URLError, TimeoutError, ValueError, OSError):
                continue
        time.sleep(espera)
        espera *= 2
    return None, None


def dist_ponto_segmento(plat, plng, alat, alng, blat, blng) -> float:
    """Distância do ponto ao segmento AB, em metros.

    Projeta em plano local antes de medir. Em escala de quarteirão o erro da
    projeção é muito menor que a precisão da própria geometria do OSM.
    """
    coslat = math.cos(math.radians(plat))
    px, py = plng * coslat, plat
    ax, ay = alng * coslat, alat
    bx, by = blng * coslat, blat
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return B.haversine_m(plat, plng, alat, alng)
    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    qx, qy = ax + t * dx, ay + t * dy
    return B.haversine_m(plat, plng, qy, qx / coslat if coslat else qx)


def nome_da_via(tags: dict) -> str:
    return (tags.get("name") or "").strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lat", type=float, required=True)
    ap.add_argument("--lng", type=float, required=True)
    ap.add_argument("--raio", type=float, default=120.0)
    ap.add_argument("--max-ancoragem", type=float, default=MAX_ANCORAGEM)
    args = ap.parse_args()

    dados, origem = buscar(args.lat, args.lng, args.raio)
    if not dados:
        # Overpass fora do ar nao e lacuna do ponto: e indisponibilidade de
        # ferramenta, e o assunto simplesmente nao entra no relatorio.
        B.emitir({
            "classificacao": None,
            "_motivo_interno": "Overpass indisponível",
            "_fonte": "OpenStreetMap",
        })
        return 0

    elementos = [e for e in dados.get("elements", []) if e.get("type") == "way" and e.get("geometry")]

    # --- via de ancoragem: a mais próxima do ponto
    melhor, melhor_d = None, float("inf")
    for w in elementos:
        g = w["geometry"]
        for i in range(len(g) - 1):
            d = dist_ponto_segmento(args.lat, args.lng, g[i]["lat"], g[i]["lon"],
                                    g[i + 1]["lat"], g[i + 1]["lon"])
            if d < melhor_d:
                melhor_d, melhor = d, w

    if melhor is None or melhor_d > args.max_ancoragem:
        B.emitir({
            "classificacao": None,
            "_motivo_interno": "ponto distante de qualquer via mapeada",
            "distancia_a_via_mais_proxima_m": round(melhor_d, 1) if melhor else None,
            "_fonte": "OpenStreetMap",
        })
        return 0

    via_nome = nome_da_via(melhor.get("tags", {}))
    via_porte = PORTE.get((melhor.get("tags", {}) or {}).get("highway", ""), "via")

    # --- cruzamentos: nó compartilhado por vias de nomes DIFERENTES
    por_no = {}
    for w in elementos:
        nome = nome_da_via(w.get("tags", {}))
        if not nome:
            continue
        for p in w["geometry"]:
            chave = (round(p["lat"], 7), round(p["lon"], 7))
            por_no.setdefault(chave, set()).add(nome)

    cruzamentos = []
    for (la, lo), nomes in por_no.items():
        if len(nomes) >= 2:
            cruzamentos.append({
                "distancia_m": round(B.haversine_m(args.lat, args.lng, la, lo), 1),
                "vias": sorted(nomes),
            })
    cruzamentos.sort(key=lambda c: c["distancia_m"])

    saida = {
        "via_do_ponto": via_nome or None,
        "porte_da_via": via_porte,
        "distancia_a_via_m": round(melhor_d, 1),
        "cruzamentos_proximos": cruzamentos[:4],
        "_cortes": {
            "esquina_ate_m": CORTE_ESQUINA,
            "meio_de_quadra_a_partir_de_m": CORTE_MEIO,
            "_zona_morta": (
                f"entre {CORTE_ESQUINA:.0f} e {CORTE_MEIO:.0f} m não há classificação "
                "defensável, e o assunto é omitido"
            ),
        },
        "_fonte": "OpenStreetMap",
        "_origem_da_consulta": origem,
    }

    if not cruzamentos:
        saida["classificacao"] = None
        saida["_motivo_interno"] = "nenhum cruzamento nomeado no raio consultado"
        B.emitir(saida)
        return 0

    perto = cruzamentos[0]
    if perto["distancia_m"] <= CORTE_ESQUINA:
        saida["classificacao"] = "esquina"
        saida["confianca"] = "alta"
        saida["vias_do_cruzamento"] = perto["vias"]
        saida["distancia_ao_cruzamento_m"] = perto["distancia_m"]
        saida["_leitura"] = (
            "o ponto está no encontro de duas vias nomeadas, com duas faces de exposição"
        )
    elif perto["distancia_m"] >= CORTE_MEIO:
        saida["classificacao"] = "meio de quadra"
        saida["confianca"] = "alta"
        saida["distancia_ao_cruzamento_m"] = perto["distancia_m"]
        saida["_leitura"] = (
            "o cruzamento nomeado mais próximo está longe o bastante para que o ponto "
            "tenha uma única face de exposição"
        )
    else:
        saida["classificacao"] = None
        saida["_motivo_interno"] = (
            f"cruzamento a {perto['distancia_m']} m cai na zona morta entre os cortes"
        )

    B.emitir(saida)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
