"""Faturamento **medido** por loja, por canal e UF — a régua para o concorrente.

Uso:
    python faturamento_canal.py --uf RN
    python faturamento_canal.py --uf RN --lat -5.752213 --lng -35.304588 --raio 300

POR QUE ESTE SCRIPT EXISTE

O campo de faturamento da camada Concorrentes é **estimado** e está preenchido
em menos da metade dos registros — num raio curto é comum sobrar um valor só,
ou nenhum. Dizer que a concorrência fatura X com base num único campo estimado
é frágil.

A planilha da IQVIA traz uma segunda via, independente e **medida**: receita e
quantidade de PDVs por **canal** e por **UF**.

    R$ por loja/mês = receita MAT do canal na UF ÷ PDVs do canal na UF ÷ 12

Os seis canais são ABRAFARMA, OUTRAS REDES CORPORATIVAS, GRUPO FARMARCAS,
FEBRAFAR, ASSOCIACOES + FRANQUIAS e INDEPENDENTES — e a camada Concorrentes
classifica cada loja num rótulo que mapeia para eles. Resultado: cada
concorrente do raio ganha um faturamento de referência medido, em vez de um
campo vazio.

O QUE ISSO **NÃO** É
Não é o faturamento daquela loja. É o que uma loja média do canal dela fatura
naquele estado. A dispersão dentro de um canal é grande e não está nesta base:
serve para dimensionar o mercado do raio e para situar um concorrente, nunca
para afirmar quanto a farmácia da esquina vende.

DUAS JANELAS DIFERENTES — a ressalva que não pode sumir
A receita é MAT (12 meses acumulados) e a contagem de PDVs é YTD (ano corrente
até a edição). São janelas distintas: canal que abriu muita loja no período
aparece com faturamento por loja subestimado, e o contrário para quem fechou.
O erro é de segunda ordem para canal estável, e vai declarado na saída.
"""

from __future__ import annotations

import argparse
import collections
import csv
import os
import sys

sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
import _bases as B  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
CPP = os.path.join(AQUI, "cache", "iqvia_canal_cpp.csv")
PDV = os.path.join(AQUI, "cache", "iqvia_canal_pdv.csv")
MESES_MAT = 12

PREPARO = (
    "bases de canal da IQVIA não preparadas. Rode uma vez, da raiz do projeto: "
    "python .claude/skills/analise-regiao-farmarcas/scripts/preparar_iqvia_canal.py"
)

# ---------------------------------------------------------------------------
# De rótulo da camada Concorrentes para canal da IQVIA.
#
# Três níveis de confiança, e a saída informa quanto do raio caiu em cada um:
#   alta   — o rótulo É a categoria (INDEPENDENTE, ASSOCIAÇÃO, FRANQUIA) ou
#            nomeia o próprio canal (FEBRAFAR, ABRAFARMA)
#   média  — rede corporativa nomeada, atribuída pelo porte conhecido dela.
#            Esta é a lista que o time de Expansão deve revisar se discordar;
#            trocar ABRAFARMA por OUTRAS REDES muda o valor de referência de
#            R$ 1,0 milhão para R$ 417 mil por loja/mês.
#   nenhuma — rótulo ausente, erro de planilha ou rede local não reconhecida.
#            Não recebe canal: entra na faixa min–max e vai declarado.
# ---------------------------------------------------------------------------

INDEPENDENTES = "INDEPENDENTES"
ASSOCIACOES = "ASSOCIACOES + FRANQUIAS"
FEBRAFAR = "FEBRAFAR"
ABRAFARMA = "ABRAFARMA"
OUTRAS_REDES = "OUTRAS REDES CORPORATIVAS"
FARMARCAS = "GRUPO FARMARCAS"

MAPA_ALTA = {
    "INDEPENDENTE": INDEPENDENTES,
    "INDEPENDENTES": INDEPENDENTES,
    "REDE INDEPENDENTE": INDEPENDENTES,
    "ASSOCIACAO": ASSOCIACOES,
    "ASSOCIACOES": ASSOCIACOES,
    "ASSOCIATIVISMO": ASSOCIACOES,
    "ASSOCIADAS": ASSOCIACOES,
    "FRANQUIA": ASSOCIACOES,
    "FRANQUIAS": ASSOCIACOES,
    "FEBRAFAR": FEBRAFAR,
    "ABRAFARMA": ABRAFARMA,
    "OUTRAS REDES": OUTRAS_REDES,
    "OUTRAS REDES CORPORATIVAS": OUTRAS_REDES,
    "FARMARCAS": FARMARCAS,
}

# Redes corporativas nomeadas. Atribuição por porte conhecido da rede — é a
# parte revisável deste script, não um dado da base.
MAPA_MEDIA = {
    # grandes redes nacionais e regionais de capital aberto ou porte equivalente
    "DROGASIL": ABRAFARMA,
    "RAIA": ABRAFARMA,
    "DROGA RAIA": ABRAFARMA,
    "RAIA DROGASIL": ABRAFARMA,
    "PAGUE MENOS": ABRAFARMA,
    "EXTRAFARMA": ABRAFARMA,
    "DROGARIA SAO PAULO": ABRAFARMA,
    "DROGARIAS PACHECO": ABRAFARMA,
    "PACHECO": ABRAFARMA,
    "SAO JOAO": ABRAFARMA,
    "PANVEL": ABRAFARMA,
    "NISSEI": ABRAFARMA,
    "ARAUJO": ABRAFARMA,
    "VENANCIO": ABRAFARMA,
    "ONOFRE": ABRAFARMA,
    "INDIANA": ABRAFARMA,
    "DROGAL": ABRAFARMA,
    "CATARINENSE": ABRAFARMA,
    "ROSARIO": ABRAFARMA,
    "DROGASMIL": ABRAFARMA,
    "DROGAO SUPER": ABRAFARMA,
    "SANTA MARTA": ABRAFARMA,
    "NOSSA DROGARIA": ABRAFARMA,
    "A NOSSA DROGARIA": ABRAFARMA,
    "REDEPHARMA": ABRAFARMA,
    "PERMANENTE": ABRAFARMA,
    # varejo alimentar com farmácia dentro
    "WAL MART": OUTRAS_REDES,
    "GPA": OUTRAS_REDES,
    "ALIMENTAR": OUTRAS_REDES,
    "CARREFOUR": OUTRAS_REDES,
    # redes de médio porte e rótulos genéricos de rede
    "MEDIA REDE": OUTRAS_REDES,
    "GRANDE REDE": OUTRAS_REDES,
}

SEM_CLASSIFICACAO = {"", "-", "NAO INFORMADO", "NAO CLASSIFICADO", "N/A", "NA"}


def canal_do_rotulo(rotulo: str) -> tuple:
    """Devolve (canal, confiança). canal=None quando não dá para afirmar."""
    bruto = (rotulo or "").strip()
    if bruto in B.ERRO_PLANILHA or B.normalizar(bruto) in SEM_CLASSIFICACAO:
        return None, "nenhuma"
    chave = B.normalizar(bruto).upper().rstrip(",.").strip()
    if chave in MAPA_ALTA:
        return MAPA_ALTA[chave], "alta"
    if chave in MAPA_MEDIA:
        return MAPA_MEDIA[chave], "media"
    return None, "nenhuma"


# ---------------------------------------------------------------------------
# A régua: receita por loja/mês, por canal, na UF — com queda para o nacional.
# ---------------------------------------------------------------------------

def _ultimo_label(linhas: list) -> str:
    return sorted({r["label"] for r in linhas})[-1]


def benchmark_por_canal(uf: str) -> dict:
    """{canal: {valor_mes, pdvs, receita_ano, abrangencia}} para a UF."""
    if not (os.path.exists(CPP) and os.path.exists(PDV)):
        raise FileNotFoundError(PREPARO)

    with open(CPP, encoding="utf-8", newline="") as fh:
        cpp = list(csv.DictReader(fh))
    with open(PDV, encoding="utf-8", newline="") as fh:
        pdv = list(csv.DictReader(fh))

    label_cpp, label_pdv = _ultimo_label(cpp), _ultimo_label(pdv)
    uf = (uf or "").strip().upper()

    receita_uf: dict = collections.defaultdict(float)
    receita_br: dict = collections.defaultdict(float)
    for r in cpp:
        if r["label"] != label_cpp:
            continue
        v = B.num(r["soma_cpp"]) or 0.0
        receita_br[r["grupo"]] += v
        if r["uf"].strip().upper() == uf:
            receita_uf[r["grupo"]] += v

    pdvs_uf: dict = collections.defaultdict(float)
    pdvs_br: dict = collections.defaultdict(float)
    for r in pdv:
        if r["label"] != label_pdv:
            continue
        v = B.num(r["qtd_pdvs"]) or 0.0
        pdvs_br[r["grupo"]] += v
        if r["uf"].strip().upper() == uf:
            pdvs_uf[r["grupo"]] += v

    saida = {}
    for canal in sorted(set(receita_br) | set(pdvs_br)):
        if pdvs_uf.get(canal, 0) > 0 and receita_uf.get(canal, 0) > 0:
            rec, n, onde = receita_uf[canal], pdvs_uf[canal], uf
        elif pdvs_br.get(canal, 0) > 0 and receita_br.get(canal, 0) > 0:
            # a UF não tem loja deste canal (ou não tem receita): cai no nacional
            rec, n, onde = receita_br[canal], pdvs_br[canal], "Brasil"
        else:
            continue
        saida[canal] = {
            "valor_mes_R$": round(rec / n / MESES_MAT, 2),
            "receita_ano_R$": round(rec / n, 2),
            "pdvs": int(n),
            "receita_total_R$": round(rec, 2),
            "abrangencia": onde,
        }
    return {
        "uf": uf,
        "label_receita": label_cpp,
        "label_pdvs": label_pdv,
        "canais": saida,
    }


# ---------------------------------------------------------------------------
# Aplicando a régua aos concorrentes de um raio.
# ---------------------------------------------------------------------------

def estimar_mercado(concorrentes: list, bench: dict, campo_rotulo: str = "classificacao") -> dict:
    """Soma o faturamento de referência dos concorrentes de uma lista.

    `concorrentes` são dicionários com o rótulo de classificação no campo
    indicado. Loja sem canal não vira zero nem vira média: entra numa faixa
    entre o canal mais barato e o mais caro da UF, e a saída diz quantas são.
    """
    canais = bench["canais"]
    if not canais:
        return {"lojas": 0, "_leitura": "sem régua de canal para esta UF"}

    valores = [c["valor_mes_R$"] for c in canais.values()]
    piso, teto = min(valores), max(valores)

    por_canal: dict = collections.defaultdict(lambda: {"lojas": 0, "total_mes_R$": 0.0})
    confianca = collections.Counter()
    sem_canal: list = []
    rotulos_sem_canal = collections.Counter()
    total = 0.0

    for c in concorrentes:
        canal, conf = canal_do_rotulo(c.get(campo_rotulo, ""))
        confianca[conf] += 1
        if canal is None or canal not in canais:
            sem_canal.append(c)
            rotulos_sem_canal[(c.get(campo_rotulo) or "").strip() or "(vazio)"] += 1
            continue
        v = canais[canal]["valor_mes_R$"]
        por_canal[canal]["lojas"] += 1
        por_canal[canal]["total_mes_R$"] += v
        total += v

    n_sem = len(sem_canal)
    return {
        "lojas": len(concorrentes),
        "lojas_com_canal": len(concorrentes) - n_sem,
        "lojas_sem_canal": n_sem,
        "mercado_mes_R$": round(total, 2),
        "mercado_mes_min_R$": round(total + n_sem * piso, 2),
        "mercado_mes_max_R$": round(total + n_sem * teto, 2),
        "mercado_ano_R$": round(total * MESES_MAT, 2),
        "por_canal": {
            k: {"lojas": v["lojas"], "total_mes_R$": round(v["total_mes_R$"], 2),
                "por_loja_mes_R$": canais[k]["valor_mes_R$"],
                "abrangencia": canais[k]["abrangencia"]}
            for k, v in sorted(por_canal.items(), key=lambda kv: -kv[1]["total_mes_R$"])
        },
        "confianca_do_mapeamento": dict(confianca),
        "rotulos_sem_canal": dict(rotulos_sem_canal.most_common(10)),
        "_faixa": (
            f"{n_sem} loja(s) sem canal reconhecido entram como faixa, entre "
            f"R$ {piso:,.0f} e R$ {teto:,.0f} por mês cada"
        ) if n_sem else "todas as lojas receberam canal",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--uf", required=True)
    ap.add_argument("--lat", type=float)
    ap.add_argument("--lng", type=float)
    ap.add_argument("--raio", type=float, default=300.0, help="metros, quando --lat/--lng")
    args = ap.parse_args()

    try:
        bench = benchmark_por_canal(args.uf)
    except FileNotFoundError as e:
        B.emitir({"erro": str(e)})
        return 1

    resultado = {
        "uf": bench["uf"],
        "_fonte": "receita e quantidade de PDVs por canal da base da IQVIA",
        "_o_que_e": (
            "faturamento de uma loja MÉDIA do canal neste estado — não o "
            "faturamento da loja observada, que esta base não traz"
        ),
        "_janelas": (
            f"receita de {bench['label_receita']} (12 meses acumulados) sobre "
            f"contagem de PDVs de {bench['label_pdvs']} (ano corrente); são "
            "janelas diferentes, e canal que abriu ou fechou muita loja no "
            "período sai enviesado"
        ),
        "benchmark_por_canal": bench["canais"],
    }

    if args.lat is not None and args.lng is not None:
        concorrentes = []
        for r in B.ler("concorrentes_2025"):
            lat, lng = B.num(r.get("LAT")), B.num(r.get("LONG"))
            if not B.coordenada_valida(lat, lng):
                continue
            if B.haversine_m(args.lat, args.lng, lat, lng) > args.raio:
                continue
            concorrentes.append({
                "classificacao": r.get("MDM-ClassifdoPDV", ""),
                "situacao": (r.get("SITUACAO") or "").strip(),
            })
        resultado["raio_m"] = args.raio
        resultado["mercado_no_raio"] = estimar_mercado(concorrentes, bench)

    resultado["lacunas"] = [
        "A base de canal não traz dispersão dentro do canal: não há mínimo, "
        "máximo nem quartil por loja, só a média. Duas farmácias independentes "
        "no mesmo quarteirão podem diferir várias vezes entre si, e isso não "
        "aparece aqui.",
        "A atribuição de canal das redes corporativas nomeadas é julgamento "
        "declarado no script, não campo da base. Trocar uma rede de ABRAFARMA "
        "para OUTRAS REDES muda a referência dela em mais de duas vezes.",
    ]
    B.emitir(resultado)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
