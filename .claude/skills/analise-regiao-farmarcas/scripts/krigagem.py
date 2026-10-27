"""Krigagem ordinária — só onde ela é aplicável, e dizendo quando não é.

Krigagem estima o valor de um campo contínuo num ponto não amostrado, usando a
estrutura espacial dos vizinhos descrita por um variograma. É mais informada que
a média ponderada por área, porque usa a correlação espacial observada em vez de
supor densidade uniforme — mas é um MODELO, com parâmetros ajustados, e por isso
só entra quando passa num teste explícito.

ONDE É APLICÁVEL

| Variável | Aplicável? | Por quê |
|---|---|---|
| Intensiva (renda média, densidade, percentuais) | **sim** | é um campo contínuo amostrado nos centroides dos setores |
| Extensiva (residentes, domicílios, potencial total) | **não diretamente** | não se interpola um total. O caminho correto é krigar a DENSIDADE e integrar sobre o círculo — feito aqui como estimativa alternativa, nunca como padrão |

LIMITE CONHECIDO, declarado em vez de escondido: o dado é areal e está sendo
tratado como amostra pontual no centroide. O tratamento rigoroso é krigagem
área-para-área, que exige desagregação do variograma pelo suporte; o que está
aqui é a aproximação usual por centroide, boa quando os setores têm tamanho
parecido e ruim quando não têm.

O TESTE DE APLICABILIDADE, em quatro portas

1. **Amostra**: pelo menos `MIN_AMOSTRAS` setores com valor na vizinhança.
2. **Estrutura espacial**: o variograma tem de mostrar estrutura — se o efeito
   pepita responde por quase toda a variância, não há o que interpolar.
3. **Ajuste**: o modelo tem de descrever o variograma empírico (R² mínimo).
4. **Validação cruzada**: deixando um de fora, a krigagem tem de errar menos
   que simplesmente usar a média dos vizinhos. Se não bate a média, não serve.

Falhando qualquer porta, devolve `aplicavel: False` com o motivo, e quem chamou
volta para o rateio por área.
"""

from __future__ import annotations

import math

MIN_AMOSTRAS = 12
MAX_AMOSTRAS = 60
RAIO_VIZINHANCA = 6.0  # múltiplos do raio de análise
MAX_PEPITA = 0.80  # acima disso o campo é ruído
MIN_R2 = 0.30
N_GRADE = 24  # pontos por eixo na integração sobre o círculo


# --------------------------------------------------------------------------- #
# variograma
# --------------------------------------------------------------------------- #
def _variograma_empirico(pontos: list, valores: list, n_bins: int = 12):
    n = len(pontos)
    pares = []
    for i in range(n):
        for j in range(i + 1, n):
            h = math.dist(pontos[i], pontos[j])
            pares.append((h, 0.5 * (valores[i] - valores[j]) ** 2))
    if not pares:
        return [], [], []
    hmax = max(p[0] for p in pares) * 0.6  # metade superior é ruidosa
    if hmax <= 0:
        return [], [], []
    largura = hmax / n_bins
    somas = [0.0] * n_bins
    contas = [0] * n_bins
    centros = [(k + 0.5) * largura for k in range(n_bins)]
    for h, g in pares:
        if h >= hmax:
            continue
        k = min(int(h / largura), n_bins - 1)
        somas[k] += g
        contas[k] += 1
    lags, gamas, pesos = [], [], []
    for k in range(n_bins):
        if contas[k] >= 5:
            lags.append(centros[k])
            gamas.append(somas[k] / contas[k])
            pesos.append(contas[k])
    return lags, gamas, pesos


def _modelo(tipo: str, h: float, pepita: float, patamar: float, alcance: float) -> float:
    if h <= 0:
        return 0.0
    if alcance <= 0:
        return pepita + patamar
    if tipo == "esferico":
        if h >= alcance:
            return pepita + patamar
        r = h / alcance
        return pepita + patamar * (1.5 * r - 0.5 * r**3)
    return pepita + patamar * (1.0 - math.exp(-3.0 * h / alcance))


def _ajustar(lags: list, gamas: list, pesos: list):
    """Busca em grade pelos parâmetros que minimizam o erro ponderado."""
    if len(lags) < 4:
        return None
    var_total = max(gamas)
    melhor = None
    for tipo in ("esferico", "exponencial"):
        for f_pep in (0.0, 0.1, 0.2, 0.3, 0.5, 0.7):
            for f_pat in (0.6, 0.8, 1.0, 1.3):
                for f_alc in (0.3, 0.5, 0.7, 1.0, 1.5):
                    pepita = var_total * f_pep
                    patamar = var_total * f_pat
                    alcance = lags[-1] * f_alc
                    sq = sum(
                        p * (g - _modelo(tipo, h, pepita, patamar, alcance)) ** 2
                        for h, g, p in zip(lags, gamas, pesos)
                    )
                    if melhor is None or sq < melhor[0]:
                        melhor = (sq, tipo, pepita, patamar, alcance)
    sq, tipo, pepita, patamar, alcance = melhor
    media = sum(p * g for g, p in zip(gamas, pesos)) / sum(pesos)
    sst = sum(p * (g - media) ** 2 for g, p in zip(gamas, pesos))
    r2 = 1 - sq / sst if sst > 0 else 0.0
    return {
        "tipo": tipo,
        "pepita": round(pepita, 6),
        "patamar": round(patamar, 6),
        "alcance_m": round(alcance, 1),
        "r2": round(r2, 4),
        "fracao_pepita": round(pepita / (pepita + patamar), 4) if (pepita + patamar) > 0 else 1.0,
    }


# --------------------------------------------------------------------------- #
# sistema de krigagem
# --------------------------------------------------------------------------- #
def _resolver(matriz: list, vetor: list):
    """Eliminação de Gauss com pivoteamento parcial."""
    n = len(vetor)
    m = [linha[:] + [vetor[i]] for i, linha in enumerate(matriz)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[piv][col]) < 1e-12:
            return None
        m[col], m[piv] = m[piv], m[col]
        for r in range(col + 1, n):
            f = m[r][col] / m[col][col]
            for c in range(col, n + 1):
                m[r][c] -= f * m[col][c]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        s = m[r][n] - sum(m[r][c] * x[c] for c in range(r + 1, n))
        x[r] = s / m[r][r]
    return x


def _krigar(pontos: list, valores: list, mod: dict, alvo: tuple):
    n = len(pontos)
    teto = mod["pepita"] + mod["patamar"]

    def cov(h):
        return teto - _modelo(mod["tipo"], h, mod["pepita"], mod["patamar"], mod["alcance_m"])

    A = [[cov(math.dist(pontos[i], pontos[j])) for j in range(n)] + [1.0] for i in range(n)]
    A.append([1.0] * n + [0.0])
    b = [cov(math.dist(pontos[i], alvo)) for i in range(n)] + [1.0]
    sol = _resolver(A, b)
    if sol is None:
        return None
    return sum(sol[i] * valores[i] for i in range(n))


def _validacao_cruzada(pontos: list, valores: list, mod: dict) -> dict:
    """Deixa um de fora e compara com o preditor trivial, a média dos outros."""
    erros_k, erros_m = [], []
    passo = max(1, len(pontos) // 30)
    for i in range(0, len(pontos), passo):
        resto_p = pontos[:i] + pontos[i + 1 :]
        resto_v = valores[:i] + valores[i + 1 :]
        est = _krigar(resto_p, resto_v, mod, pontos[i])
        if est is None:
            continue
        erros_k.append((est - valores[i]) ** 2)
        erros_m.append((sum(resto_v) / len(resto_v) - valores[i]) ** 2)
    if not erros_k:
        return {"rmse_krigagem": None, "rmse_media": None, "ganho": None}
    rk = math.sqrt(sum(erros_k) / len(erros_k))
    rm = math.sqrt(sum(erros_m) / len(erros_m))
    return {
        "rmse_krigagem": round(rk, 4),
        "rmse_media": round(rm, 4),
        "ganho": round(1 - rk / rm, 4) if rm > 0 else None,
        "n_testes": len(erros_k),
    }


# --------------------------------------------------------------------------- #
def _centroide(geom: dict) -> tuple:
    coords = geom.get("coordinates") or []
    if geom.get("type") == "MultiPolygon":
        coords = [a for p in coords for a in p]
    anel = coords[0] if coords else []
    if not anel:
        return None
    return (sum(p[0] for p in anel) / len(anel), sum(p[1] for p in anel) / len(anel))


def _grade_no_circulo(raio: float, n: int) -> list:
    pts = []
    passo = 2 * raio / n
    for i in range(n):
        for j in range(n):
            x = -raio + (i + 0.5) * passo
            y = -raio + (j + 0.5) * passo
            if x * x + y * y <= raio * raio:
                pts.append((x, y))
    return pts


def estimar(setores: list, atributos: dict, campos: dict, lat0: float, lon0: float,
            raio: float, referencia_area: dict) -> dict:
    """Krigagem das variáveis intensivas e, como alternativa, da densidade."""
    import _geo as G

    # Amostras: centroides dos setores do município dentro da vizinhança.
    amostras = {}
    for s in setores:
        c = _centroide(s.get("geometria") or {})
        if c:
            amostras[s["codigo"]] = G.projetar(c[0], c[1], lat0, lon0)

    # Os setores do raio sozinhos não dão amostra para um variograma. Puxamos a
    # vizinhança do município e carregamos os atributos dela também — sem isso os
    # vizinhos entram como ponto sem valor e a krigagem recusa por falta de amostra.
    vizinhos = _carregar_vizinhanca(lat0, lon0, raio, setores)
    amostras.update(vizinhos)
    atributos = dict(atributos)
    atributos.update(_atributos_da_vizinhanca(set(vizinhos) - set(atributos), campos))

    intensivas = [n for n, (_b, _c, nat, _p) in campos.items() if nat == "intensivo"]
    valores_por_campo = {}
    for nome in intensivas:
        base, campo, _nat, _peso = campos[nome]
        pts, vals = [], []
        for cod, xy in amostras.items():
            v = atributos.get(cod, {}).get(f"{base}.{campo}")
            if v is not None:
                pts.append(xy)
                vals.append(v)
        valores_por_campo[nome] = (pts, vals)

    n_max = max((len(v[0]) for v in valores_por_campo.values()), default=0)
    if n_max < MIN_AMOSTRAS:
        return {
            "aplicavel": False,
            "motivo": (
                f"amostra insuficiente: {n_max} setores com valor na vizinhança, "
                f"mínimo de {MIN_AMOSTRAS}. Krigagem precisa de vizinhos para estimar a "
                "estrutura espacial; com poucos, o variograma é ruído"
            ),
            "porta": "amostra",
        }

    grade = _grade_no_circulo(raio, N_GRADE)
    saida, diagnostico, recusados = {}, {}, {}

    for nome, (pts, vals) in valores_por_campo.items():
        if len(pts) < MIN_AMOSTRAS:
            recusados[nome] = f"só {len(pts)} amostras"
            continue
        if len(pts) > MAX_AMOSTRAS:
            pts_ord = sorted(range(len(pts)), key=lambda i: math.hypot(*pts[i]))[:MAX_AMOSTRAS]
            pts = [pts[i] for i in pts_ord]
            vals = [vals[i] for i in pts_ord]
        lags, gamas, pesos = _variograma_empirico(pts, vals)
        mod = _ajustar(lags, gamas, pesos)
        if mod is None:
            recusados[nome] = "variograma empírico sem pontos suficientes"
            continue
        if mod["fracao_pepita"] > MAX_PEPITA:
            recusados[nome] = (
                f"sem estrutura espacial: efeito pepita responde por "
                f"{mod['fracao_pepita']:.0%} da variância"
            )
            continue
        if mod["r2"] < MIN_R2:
            recusados[nome] = f"modelo não descreve o variograma (R² {mod['r2']:.2f})"
            continue
        vc = _validacao_cruzada(pts, vals, mod)
        if vc["ganho"] is None or vc["ganho"] <= 0:
            recusados[nome] = (
                f"não supera a média dos vizinhos na validação cruzada "
                f"(ganho {vc['ganho']})"
            )
            continue
        est = [_krigar(pts, vals, mod, g) for g in grade]
        est = [x for x in est if x is not None]
        if not est:
            recusados[nome] = "sistema de krigagem singular"
            continue
        saida[nome] = round(sum(est) / len(est), 4)
        diagnostico[nome] = {"variograma": mod, "validacao_cruzada": vc, "amostras": len(pts)}

    if not saida:
        return {
            "aplicavel": False,
            "motivo": "nenhuma variável passou no teste de aplicabilidade",
            "recusas": recusados,
            "porta": "teste",
        }

    # Extensivas: nunca krigadas direto. Quando a densidade passou, dá para
    # estimar a população integrando o campo krigado sobre o círculo.
    alternativa = None
    if "densidade_hab_km2" in saida:
        area_km2 = math.pi * raio**2 / 1_000_000.0
        alternativa = {
            "populacao_por_densidade_krigada": round(saida["densidade_hab_km2"] * area_km2, 1),
            "_leitura": (
                "densidade krigada × área do círculo. É estimativa alternativa, não o valor "
                "padrão: o rateio por área é exato e esta depende do modelo"
            ),
            "populacao_por_rateio_de_area": referencia_area.get("residentes"),
        }

    valores = dict(referencia_area)
    valores.update(saida)

    return {
        "aplicavel": True,
        "campos_krigados": sorted(saida),
        "campos_recusados": recusados,
        "_extensivas": (
            "residentes, domicílios e potencial continuam vindo do rateio por área: "
            "não se interpola um total"
        ),
        "estimativa_alternativa_de_populacao": alternativa,
        "diagnostico": diagnostico,
        "valores": valores,
        "_limite": (
            "o dado é areal e está sendo tratado como amostra pontual no centroide; "
            "o rigoroso seria krigagem área-para-área"
        ),
    }


def _atributos_da_vizinhanca(codigos: set, campos: dict) -> dict:
    """Valores das bases setoriais para os setores vizinhos, só o necessário."""
    import _bases as B

    if not codigos:
        return {}
    bases: dict[str, set] = {}
    for _n, (base, campo, nat, _p) in campos.items():
        if nat == "intensivo":
            bases.setdefault(base, set()).add(campo)
    saida: dict[str, dict] = {}
    for base, cols in bases.items():
        try:
            for linha in B.ler(base):
                k = None
                for c in ("Cod_setor", "CD_GEOCODI"):
                    if linha.get(c):
                        k = str(linha[c]).strip()
                        break
                if k in codigos:
                    alvo = saida.setdefault(k, {})
                    for col in cols:
                        alvo[f"{base}.{col}"] = B.num(linha.get(col))
        except FileNotFoundError:
            continue
    return saida


def _carregar_vizinhanca(lat0: float, lon0: float, raio: float, setores: list) -> dict:
    """Centroides projetados dos setores do município dentro da vizinhança."""
    import json

    import _bases as B
    import _geo as G
    import malha_setores

    codigo = None
    for s in setores:
        codigo = s["codigo"][:7]
        break
    if not codigo:
        return {}
    try:
        caminho = malha_setores.construir(codigo, verbose=False)
        with open(caminho, encoding="utf-8") as fh:
            malha = json.load(fh)
    except Exception:
        return {}

    limite = raio * RAIO_VIZINHANCA
    saida = {}
    for f in malha.get("features", []):
        cod = (f.get("properties") or {}).get("CD_GEOCODI")
        c = _centroide(f.get("geometry") or {})
        if not cod or not c:
            continue
        xy = G.projetar(c[0], c[1], lat0, lon0)
        if math.hypot(*xy) <= limite:
            saida[str(cod).strip()] = xy
    return saida
