"""Acesso determinístico ao dump local das bases do Órbita.

Regra da casa: TODO número do dossiê sai daqui ou de uma API pública.
O modelo lê a saída, compara e escreve — nunca calcula nem completa.

Armadilhas tratadas aqui (verificadas no dump de 2026-10-26):
- Encoding MISTO: 30 arquivos em UTF-8, 27 em cp1252. Detectado por arquivo.
- Coordenadas em `concorrentes_2025` usam VÍRGULA decimal ("-15,84696100000").
- Campos de erro de planilha vêm como '{"error":"#N/A"}' — valem como AUSENTE,
  nunca como zero.
- O export achatou `geometry` para o TIPO ("Point", "Polygon"). Não há polígono
  no dump; camadas de setor censitário só funcionam por raio na Fase 2, com a
  malha do IBGE.
"""

from __future__ import annotations

import csv
import glob
import json
import math
import os
import re
import sys
import unicodedata

csv.field_size_limit(10**9)

DEFAULT_DIR = r"C:\Users\zequi\Downloads\bases órbita"

# Data do dump. Todo dossiê carimba isto: o dado NÃO se atualiza sozinho.
DATA_DO_DUMP = "2026-10-26"

ERRO_PLANILHA = ('{"error":"#N/A"}', "#N/A", "---", "")

# Bandeiras do grupo Farmarcas, conforme as colunas de `mat_atual_brick_bandeira`.
# Servem para achar loja NOSSA dentro da camada Concorrentes — o caso documentado
# em docs/confluence/2025/evolucao-camadas/orbita-evolucao-camadas.md:12.
BANDEIRAS_FARMARCAS = (
    "AC FARMA",
    "BIGFORT",
    "ENTREFARMA",
    "FARMA 100",
    "FARMAVALE",
    "MAESTRA",
    "MAIS FARMA",
    "MAXI POPULAR",
    "MEGA POPULAR",
    "SUPER POPULAR",
    "ULTRA POPULAR",
    "CONECTADAS",
)


def base_dir() -> str:
    return os.environ.get("ORBITA_BASES", DEFAULT_DIR)


# Sufixo de timestamp que o export anexa a cada base: _AAAA-MM-DD_HH-MM.csv
_SUFIXO_DUMP = re.compile(r"^_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}\.csv$")


def achar(prefixo: str) -> str:
    """Resolve o caminho de uma base pelo nome, sem casar com bases vizinhas.

    CUIDADO que custou caro: um glob solto de `prefixo*` casa com nomes mais
    longos. `renda_media*` pega `renda_media_municipio`, e
    `densidade_demografica*` pega `densidade_demografica_uf` — e, como o `sorted`
    devolvia o último, as duas bases erradas eram lidas em silêncio. O sintoma
    era uma lacuna falsa ("município ausente nesta base"), não um erro.

    Aqui só vale o arquivo cujo resto do nome é o sufixo de timestamp do export,
    ou o nome exato com `.csv`.
    """
    diretorio = base_dir()
    candidatos = []
    for caminho in glob.glob(os.path.join(diretorio, prefixo + "*.csv")):
        resto = os.path.basename(caminho)[len(prefixo):]
        if resto == ".csv" or _SUFIXO_DUMP.match(resto):
            candidatos.append(caminho)
    if not candidatos:
        raise FileNotFoundError(
            f"base '{prefixo}' não encontrada em {diretorio!r}. "
            "Defina ORBITA_BASES se o dump estiver em outro lugar."
        )
    return sorted(candidatos)[-1]


def _encoding(caminho: str) -> str:
    with open(caminho, "rb") as fh:
        amostra = fh.read(5_000_000)
    try:
        amostra.decode("utf-8")
        return "utf-8-sig"
    except UnicodeDecodeError:
        return "cp1252"


def ler(prefixo: str):
    """Itera as linhas de uma base como dict. Streaming: não carrega na memória."""
    caminho = achar(prefixo)
    enc = _encoding(caminho)
    with open(caminho, encoding=enc, newline="", errors="replace") as fh:
        for linha in csv.DictReader(fh):
            yield linha


def num(valor, padrao=None):
    """Converte texto para float tolerando vírgula decimal e valores de erro.

    Retorna `padrao` (None) para ausente — NUNCA zero. Setor com dado suprimido
    e setor com valor zero são coisas diferentes.
    """
    if valor is None:
        return padrao
    texto = str(valor).strip()
    if texto in ERRO_PLANILHA or texto.startswith('{"error"'):
        return padrao
    texto = texto.replace("R$", "").replace("%", "").strip()
    if texto.count(",") == 1 and texto.count(".") == 0:
        texto = texto.replace(",", ".")
    else:
        texto = texto.replace(",", "")
    try:
        return float(texto)
    except ValueError:
        return padrao


def haversine_m(lat1, lon1, lat2, lon2) -> float:
    """Distância em metros. Nunca medir distância em graus."""
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


# Bounding box do Brasil. Mesma regra que o produto implementou para barrar
# coordenada suja vinda de Excel — ver docs/confluence/documentacao-tecnica/
# entendimento-indicadores-analises.md:92.
# Verificado em 2026-10-26: 3.700 dos 100.594 registros de `concorrentes_2025`
# (3,7%) caem FORA desta caixa. São dado sujo, não ponto no exterior.
BBOX_BR = {"lat": (-34.0, 6.0), "lng": (-74.0, -35.0)}


def coordenada_valida(lat, lng) -> bool:
    if lat is None or lng is None:
        return False
    return (
        BBOX_BR["lat"][0] <= lat <= BBOX_BR["lat"][1]
        and BBOX_BR["lng"][0] <= lng <= BBOX_BR["lng"][1]
    )


def chave_municipio(linha: dict):
    """Acha a coluna de código IBGE do município, que varia de base para base."""
    for col in ("CODIGO", "CD_MUN", "codigoIbge", "codigo_mun", "CODMUN", "cod_MMMM"):
        if col in linha and linha[col]:
            return str(linha[col]).strip()
    return None


def indexar_por_municipio(prefixo: str) -> dict:
    """Carrega uma base municipal indexada pelo código IBGE (7 dígitos)."""
    saida = {}
    for linha in ler(prefixo):
        cod = chave_municipio(linha)
        if cod:
            saida[cod] = linha
    return saida


def eh_farmarcas(nome_pdv: str) -> bool:
    alvo = (nome_pdv or "").upper()
    return any(b in alvo for b in BANDEIRAS_FARMARCAS)


# ---------------------------------------------------------------------------
# Cadastro de lojas Farmarcas — fonte de verdade para "loja nossa"
# ---------------------------------------------------------------------------
# NÃO usar `BANDEIRAS_FARMARCAS` sobre a camada Concorrentes para decidir se uma
# loja é nossa: isso dá falso positivo. Caso real verificado em 2026-10-27 —
# "FCIA FARMAVALE" a 112 m do centro de Franca/SP casa pelo nome da bandeira e
# NÃO existe no cadastro; a única loja Farmarcas de Franca é uma Ultra Popular
# DESATIVADA a 4.784 m. O match por nome vale como suspeita, nunca como fato.

CADASTRO_LOJAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache", "cadastro_lojas.csv")

# Status que ocupam vaga de zoneamento. Loja desativada não canibaliza ninguém.
# Premissa declarada (não está escrita na regra oficial) — ver
# references/zoneamento-e-perfil.md.
STATUS_OCUPA_VAGA = ("Ativado", "Montando", "Transição")


def ler_cadastro_lojas():
    """Itera o cadastro de lojas convertido por preparar_cadastro_lojas.py."""
    if not os.path.exists(CADASTRO_LOJAS):
        raise FileNotFoundError(
            "cadastro de lojas não preparado. Rode uma vez, a partir da raiz do projeto: "
            "python .claude/skills/analise-regiao-farmarcas/scripts/preparar_cadastro_lojas.py"
        )
    with open(CADASTRO_LOJAS, encoding="utf-8", newline="") as fh:
        for linha in csv.DictReader(fh):
            yield linha


def normalizar(texto: str) -> str:
    """Maiúsculas sem acento — para comparar nome de cidade entre bases."""
    t = unicodedata.normalize("NFKD", (texto or "").upper())
    return "".join(c for c in t if not unicodedata.combining(c)).strip()


# ---------------------------------------------------------------------------
# População do Censo 2022 — a fonte que decide a faixa de zoneamento
# ---------------------------------------------------------------------------
# Decisão de produto (2026-10-27): a faixa de zoneamento é cortada pelo CENSO
# 2022 do IBGE, não pela população do dump. O dump é estimativa com ano de
# referência não declarado e difere em ~4% (Franca: 366.566 × 352.536) — perto
# dos cortes de 60k/120k/200k isso muda a regra aplicada.

CACHE_CENSO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache", "censo2022.json")
URL_CENSO = (
    "https://servicodados.ibge.gov.br/api/v3/agregados/4714/periodos/2022"
    "/variaveis/93?localidades=N6%5B{codigo}%5D"
)


def populacao_censo_2022(codigo: str):
    """Devolve (populacao, origem). Consulta a API do IBGE e guarda em cache.

    Nunca estima: se a API não responder e não houver cache, devolve (None, motivo).
    """
    codigo = str(codigo).strip()
    cache = {}
    if os.path.exists(CACHE_CENSO):
        try:
            with open(CACHE_CENSO, encoding="utf-8") as fh:
                cache = json.load(fh)
        except (OSError, ValueError):
            cache = {}
    if codigo in cache:
        return cache[codigo], "cache local da API do IBGE"

    import urllib.error
    import urllib.request

    try:
        with urllib.request.urlopen(URL_CENSO.format(codigo=codigo), timeout=25) as resp:
            dados = json.loads(resp.read().decode("utf-8"))
        valor = dados[0]["resultados"][0]["series"][0]["serie"]["2022"]
        pop = int(valor)
    except (urllib.error.URLError, KeyError, IndexError, ValueError, TimeoutError) as e:
        return None, f"API do IBGE indisponível e sem cache ({type(e).__name__})"

    cache[codigo] = pop
    os.makedirs(os.path.dirname(CACHE_CENSO), exist_ok=True)
    with open(CACHE_CENSO, "w", encoding="utf-8") as fh:
        json.dump(cache, fh)
    return pop, "IBGE, Censo 2022, agregado 4714 variável 93"


def emitir(payload: dict) -> None:
    """Imprime JSON na stdout. É isto que o modelo lê."""
    payload.setdefault("_fonte", "dump local das bases do Órbita")
    payload.setdefault("_data_do_dump", DATA_DO_DUMP)
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
