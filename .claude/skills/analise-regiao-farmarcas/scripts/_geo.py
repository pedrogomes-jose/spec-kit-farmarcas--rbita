"""Geometria em stdlib puro: área, recorte por círculo e fração de interseção.

Existe porque `shapely` não está disponível sob `python -I`, que é como os
scripts de análise rodam, e porque o rateio proporcional — a fração do setor
censitário que cai dentro do raio — é a diferença entre somar o setor inteiro
e medir a parte que interessa.

Método:
  1. Projeção local equirretangular em metros, centrada no ponto de análise.
     Nas escalas aqui (centenas de metros a poucos km) a distorção de área é
     menor que 0,1% — e a mesma projeção vale para o setor e para o círculo,
     então a RAZÃO entre as áreas, que é o que o rateio usa, cancela o resto.
  2. Recorte de Sutherland–Hodgman do polígono do setor contra um polígono
     regular que aproxima o círculo. O algoritmo exige que o RECORTE seja
     convexo — o círculo é — e aceita setor côncavo, que é o caso comum.
  3. Área por fórmula do shoelace, descontando os anéis internos (buracos).

Validado contra o campo `area_km2` da camada de densidade: ver `validar_area`.
"""

from __future__ import annotations

import math

RAIO_TERRA_M = 6_371_008.8
LADOS_CIRCULO = 360  # erro de área do polígono regular < 0,01%


def projetar(lon: float, lat: float, lat0: float, lon0: float) -> tuple:
    """Graus para metros, no plano local centrado em (lat0, lon0)."""
    k = math.pi / 180.0 * RAIO_TERRA_M
    return ((lon - lon0) * k * math.cos(math.radians(lat0)), (lat - lat0) * k)


def area_shoelace(pts: list) -> float:
    """Área absoluta do polígono simples, em m². Lista de (x, y)."""
    n = len(pts)
    if n < 3:
        return 0.0
    s = 0.0
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2.0


def _dentro(p: tuple, a: tuple, b: tuple) -> bool:
    """p está do lado interno da aresta dirigida a->b? (sentido anti-horário)"""
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) >= 0


def _intersecao(p1: tuple, p2: tuple, a: tuple, b: tuple) -> tuple:
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = a
    x4, y4 = b
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if den == 0:
        return p2
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


def recortar(poligono: list, recorte_convexo: list) -> list:
    """Sutherland–Hodgman. `recorte_convexo` em sentido anti-horário."""
    saida = poligono
    n = len(recorte_convexo)
    for i in range(n):
        if not saida:
            return []
        a, b = recorte_convexo[i], recorte_convexo[(i + 1) % n]
        entrada, saida = saida, []
        for j in range(len(entrada)):
            atual, anterior = entrada[j], entrada[j - 1]
            if _dentro(atual, a, b):
                if not _dentro(anterior, a, b):
                    saida.append(_intersecao(anterior, atual, a, b))
                saida.append(atual)
            elif _dentro(anterior, a, b):
                saida.append(_intersecao(anterior, atual, a, b))
    return saida


def circulo_projetado(raio_m: float, lados: int = LADOS_CIRCULO) -> list:
    """Polígono regular que aproxima o círculo, já em metros e anti-horário."""
    return [
        (raio_m * math.cos(2 * math.pi * i / lados), raio_m * math.sin(2 * math.pi * i / lados))
        for i in range(lados)
    ]


def _aneis(geom: dict) -> list:
    """Anéis de um Polygon ou MultiPolygon: [(anel, eh_buraco), ...]."""
    tipo = geom.get("type")
    coords = geom.get("coordinates") or []
    saida = []
    if tipo == "Polygon":
        for i, anel in enumerate(coords):
            saida.append((anel, i > 0))
    elif tipo == "MultiPolygon":
        for parte in coords:
            for i, anel in enumerate(parte):
                saida.append((anel, i > 0))
    return saida


def area_m2(geom: dict, lat0: float = None, lon0: float = None) -> float:
    """Área do polígono em m², descontando buracos.

    Sem (lat0, lon0) a projeção é centrada no próprio polígono — é assim que se
    mede a área total de um setor em qualquer lugar do país sem distorção.
    """
    aneis = _aneis(geom)
    if not aneis:
        return 0.0
    if lat0 is None or lon0 is None:
        pts = [p for anel, _ in aneis for p in anel]
        lon0 = sum(p[0] for p in pts) / len(pts)
        lat0 = sum(p[1] for p in pts) / len(pts)
    total = 0.0
    for anel, eh_buraco in aneis:
        proj = [projetar(p[0], p[1], lat0, lon0) for p in anel]
        a = area_shoelace(proj)
        total += -a if eh_buraco else a
    return max(total, 0.0)


def fracao_no_circulo(geom: dict, lat0: float, lon0: float, raio_m: float) -> tuple:
    """Devolve (fração dentro do círculo, área total m², área dentro m²).

    Fração 0 quando não há interseção, 1 quando o setor está inteiro dentro.
    """
    aneis = _aneis(geom)
    if not aneis:
        return 0.0, 0.0, 0.0
    recorte = circulo_projetado(raio_m)
    total = dentro = 0.0
    for anel, eh_buraco in aneis:
        proj = [projetar(p[0], p[1], lat0, lon0) for p in anel]
        a_total = area_shoelace(proj)
        a_dentro = area_shoelace(recortar(proj, recorte))
        if eh_buraco:
            total -= a_total
            dentro -= a_dentro
        else:
            total += a_total
            dentro += a_dentro
    total = max(total, 0.0)
    dentro = max(min(dentro, total), 0.0)
    return (dentro / total if total > 0 else 0.0), total, dentro


def validar_area(geom: dict, area_km2_declarada: float) -> dict:
    """Compara a área calculada com a declarada na base. Teste de sanidade."""
    calc = area_m2(geom) / 1_000_000.0
    if not area_km2_declarada:
        return {"area_calculada_km2": round(calc, 6), "declarada": None, "erro_pct": None}
    return {
        "area_calculada_km2": round(calc, 6),
        "declarada": area_km2_declarada,
        "erro_pct": round(100 * (calc - area_km2_declarada) / area_km2_declarada, 3),
    }
