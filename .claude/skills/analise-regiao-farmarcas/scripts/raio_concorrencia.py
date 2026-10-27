"""Concorrência e canibalização dentro do raio.

Uso:
    python raio_concorrencia.py --lat -20.5386 --lng -47.4006 --raio 300

Canibalização sai do CADASTRO DE LOJAS (CNPJ + coordenada), não do nome de
bandeira dentro da camada Concorrentes — esse dá falso positivo. Caso real:
"FCIA FARMAVALE" a 112 m do centro de Franca/SP casa pelo nome e não existe no
cadastro; a única loja Farmarcas de Franca é uma Ultra Popular DESATIVADA a
4.784 m.

Única camada de ponto do dump que tem coordenada própria é `concorrentes_2025`.
As demais (farmácias/Receita, bancos, clínicas, barreiras) vieram SEM coordenada
— o export achatou `geometry` para o tipo. O script declara isso na saída em vez
de omitir, porque lacuna não declarada vira conclusão errada.
"""

from __future__ import annotations

import argparse
import sys

sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
import _bases as B  # noqa: E402

# Faixas fixas de faturamento MENSAL do produto, copiadas de
# api-agent-orbita/src/constants/competitorRevenueTiers.ts. São constantes de
# negócio: não variam com a localidade. A faixa 1 é aberta em cima e a 8 embaixo.
# O mesmo arquivo confirma que `fatMedio` é faturamento médio MENSAL estimado.
FAIXAS_FATURAMENTO = [
    (1, 1_336_854.12, None),
    (2, 846_655.41, 1_336_854.11),
    (3, 549_075.62, 846_655.40),
    (4, 388_442.64, 549_075.61),
    (5, 271_181.25, 388_442.63),
    (6, 162_244.26, 271_181.24),
    (7, 89_997.74, 162_244.25),
    (8, 0.0, 89_997.74),
]

# Camadas que o analista esperaria ver no raio e que o dump NÃO permite.
SEM_COORDENADA = {
    "farmacias": "cadastro Receita/QSA — só endereço; conferir via CNES (Fase 3)",
    "farmacias_populares_2025": "só endereço",
    "bancos": "só endereço",
    "clinicas_oftalmologicas": "só endereço",
    "barreiras_geograficas": "polígono/linha ficou no asset, não no CSV",
    "setor_censitario": "polígono ficou no asset — habilita na Fase 2 com a malha do IBGE",
}


def estatisticas_de_venda(valores: list) -> dict:
    """Mínimo, máximo e quartis do faturamento mensal estimado das lojas.

    Responde "quanto vende uma loja desta região" com a dispersão, não com uma
    média: em varejo farmacêutico a distribuição é de cauda longa, e a média
    sozinha descreve mal tanto o piso quanto o teto. O mínimo e o máximo são os
    extremos observados entre as lojas COM faturamento cadastrado — não são
    projeção para a loja nova, são o que as vizinhas faturam.
    """
    limpos = sorted(v for v in valores if v is not None and v > 0)
    if not limpos:
        return {"lojas_com_faturamento": 0, "_leitura": "nenhuma loja da amostra tem faturamento cadastrado"}

    def q(f):
        if len(limpos) == 1:
            return limpos[0]
        pos = f * (len(limpos) - 1)
        baixo = int(pos)
        alto = min(baixo + 1, len(limpos) - 1)
        return limpos[baixo] + (limpos[alto] - limpos[baixo]) * (pos - baixo)

    return {
        "lojas_com_faturamento": len(limpos),
        "minimo_R$": round(limpos[0], 2),
        "q1_R$": round(q(0.25), 2),
        "mediana_R$": round(q(0.50), 2),
        "q3_R$": round(q(0.75), 2),
        "maximo_R$": round(limpos[-1], 2),
        "_periodicidade": "faturamento médio MENSAL estimado por PDV",
        "_leitura": (
            "extremos observados entre as lojas vizinhas com faturamento cadastrado — "
            "não é projeção para a loja nova"
        ),
    }


def classificar_faturamento(valor):
    """Faixa 1..8 do produto para um faturamento mensal. None se inválido."""
    if valor is None or valor <= 0:
        return None
    for classificacao, minimo, maximo in FAIXAS_FATURAMENTO:
        if valor >= minimo and (maximo is None or valor <= maximo):
            return classificacao
    return None


def vendas_da_regiao(municipio: str):
    """Soma de `fatMedio` de todos os concorrentes **do município do ponto**.

    DIVERGÊNCIA DELIBERADA do produto, decidida pelo PM em 2026-10-27. O produto
    agrega as **cidades tocadas pelo raio** (`microterritory.regionTotalSales`),
    o que num ponto perto de divisa soma mercados que não são a praça analisada:
    em São Gonçalo do Amarante/RN o raio de 5 km alcançava seis municípios e o
    número virava o mercado da macrorregião de Natal, não o da cidade.

    "Região" aqui é sempre **a cidade do ponto** — nem o raio, nem a macrorregião.
    """
    alvo = B.normalizar(municipio)
    total, valores = 0.0, []
    for linha in B.ler("concorrentes_2025"):
        if B.normalizar(linha.get("CIDADE") or "") != alvo:
            continue
        v = B.num(linha.get("fatMedio"))
        if v is not None and v > 0:
            total += v
            valores.append(v)
    return (round(total, 2) if valores else None), len(valores), valores


def lojas_farmarcas_no_raio(lat: float, lng: float, raio: float):
    """Lojas Farmarcas dentro do raio, pelo cadastro. Fonte de verdade."""
    dentro, vazias, invalidas = [], 0, 0
    for loja in B.ler_cadastro_lojas():
        la = B.num(loja.get("Latitude - Endereço Receita"))
        lo = B.num(loja.get("Longitude - Endereço Receita"))
        if la is None or lo is None:
            vazias += 1
            continue
        if not B.coordenada_valida(la, lo):
            invalidas += 1
            continue
        dist = B.haversine_m(lat, lng, la, lo)
        if dist > raio:
            continue
        dentro.append(
            {
                "bandeira": (loja.get("Bandeira") or "").strip(),
                "modelo": (loja.get("Modelo de Negócio") or "").strip(),
                "status": (loja.get("Status") or "").strip(),
                "cidade": (loja.get("Cidade - Endereço Receita") or "").strip(),
                "bairro": (loja.get("Bairro - Endereço Receita") or "").strip(),
                "cnpj": (loja.get("CNPJ") or "").strip(),
                "distancia_m": round(dist),
                "ocupa_vaga_de_zoneamento": (loja.get("Status") or "").strip() in B.STATUS_OCUPA_VAGA,
            }
        )
    dentro.sort(key=lambda r: r["distancia_m"])
    return dentro, vazias, invalidas


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lat", type=float, required=True)
    ap.add_argument("--lng", type=float, required=True)
    ap.add_argument("--raio", type=float, default=300.0, help="metros (padrão do Órbita: 300)")
    ap.add_argument("--listar", type=int, default=15)
    ap.add_argument("--municipio", default="", help="município do ponto; é a referência de cadastro")
    args = ap.parse_args()

    cidade_ref = None

    dentro, nossas, suspeitos = [], [], []
    sem_coord = 0
    coord_invalida = 0
    for linha in B.ler("concorrentes_2025"):
        la, lo = B.num(linha.get("LAT")), B.num(linha.get("LONG"))
        if la is None or lo is None:
            sem_coord += 1
            continue
        if not B.coordenada_valida(la, lo):
            coord_invalida += 1
            continue
        dist = B.haversine_m(args.lat, args.lng, la, lo)
        if dist > args.raio:
            continue
        pdv = (linha.get("MDM-PDV") or "").strip()
        reg = {
            "pdv": pdv,
            "cidade": (linha.get("CIDADE") or "").strip(),
            "classificacao": (linha.get("MDM-ClassifdoPDV") or "").strip(),
            "bairro": (linha.get("BAIRRO") or "").strip(),
            "endereco": (linha.get("ENDERECO") or "").strip(),
            "cnpj": (linha.get("CNPJ") or "").strip(),
            "situacao": (linha.get("SITUACAO") or "").strip() or None,
            "fat_medio": B.num(linha.get("fatMedio")),
            "distancia_m": round(dist),
        }
        (nossas if B.eh_farmarcas(pdv) else dentro).append(reg)

    # A referência de cadastro é o MUNICÍPIO DO PONTO, não a cidade mais comum
    # do raio. Usar a modal parece razoável e erra feio perto de divisa: num raio
    # de 5 km sobre a divisa de São Gonçalo do Amarante com Natal, a modal era
    # Natal (53 de 96), e 36 lojas do próprio município do ponto foram marcadas
    # como "cidade divergente". A modal só entra se o município não for passado,
    # e a saída diz qual critério valeu.
    criterio_ref = None
    if args.municipio:
        cidade_ref = B.normalizar(args.municipio)
        criterio_ref = f"município do ponto ({args.municipio})"
    elif dentro or nossas:
        import collections as _c

        contagem = _c.Counter(B.normalizar(r["cidade"]) for r in (dentro + nossas) if r["cidade"])
        if contagem:
            cidade_ref = contagem.most_common(1)[0][0]
            criterio_ref = (
                f"cidade mais frequente do raio ({cidade_ref}) — município do ponto não informado, "
                "leitura imprecisa perto de divisa"
            )
    if cidade_ref:
        suspeitos = [
            r for r in (dentro + nossas) if r["cidade"] and B.normalizar(r["cidade"]) != cidade_ref
        ]

    # A cidade dominante entre os achados é a referência; quem destoa é suspeito
    # de coordenada ou cadastro errado (verificado: há registro de Grão Mogol/MG
    # caindo a menos de 2 km do centro de Franca/SP).
    dentro.sort(key=lambda r: r["distancia_m"])
    nossas.sort(key=lambda r: r["distancia_m"])

    com_fat = [r["fat_medio"] for r in dentro if r["fat_medio"] is not None]
    por_rede: dict[str, int] = {}
    for r in dentro:
        por_rede[r["pdv"] or "(sem nome)"] = por_rede.get(r["pdv"] or "(sem nome)", 0) + 1

    r_total = round(sum(com_fat), 2) if com_fat else None
    r_media = round(r_total / len(com_fat), 2) if com_fat else None

    contagem = {c: 0 for c, _, _ in FAIXAS_FATURAMENTO}
    for reg in dentro + nossas:
        f = classificar_faturamento(reg["fat_medio"])
        if f:
            contagem[f] += 1
    faixas = [
        {
            "classificacao": c,
            "minima_R$": minimo if minimo > 0 else None,
            "maxima_R$": maximo,
            "lojas": contagem[c],
        }
        for c, minimo, maximo in FAIXAS_FATURAMENTO
    ]

    cidades_raio = {r["cidade"].upper() for r in (dentro + nossas) if r.get("cidade")}
    # Cidade vizinha é a que aparece várias vezes no raio: uma divisa produz
    # muitos registros, um erro de cadastro produz um ou dois soltos.
    import collections as _c2

    _freq = _c2.Counter(r["cidade"] for r in (dentro + nossas) if r.get("cidade"))
    cidades_vizinhas = {c for c, n in _freq.items() if n >= 3}
    reg_total, reg_lojas, reg_valores = (
        vendas_da_regiao(args.municipio) if args.municipio else (None, 0, [])
    )

    try:
        cadastro, lojas_vazias, lojas_invalidas = lojas_farmarcas_no_raio(args.lat, args.lng, args.raio)
        erro_cadastro = None
    except FileNotFoundError as e:
        cadastro, lojas_vazias, lojas_invalidas, erro_cadastro = [], 0, 0, str(e)

    B.emitir(
        {
            "ponto": {"lat": args.lat, "lng": args.lng, "raio_m": args.raio},
            "concorrentes": {
                "total": len(dentro),
                "com_fat_medio": len(com_fat),
                "fat_medio_somado_R$": round(sum(com_fat), 2) if com_fat else None,
                "fat_medio_maior_R$": round(max(com_fat), 2) if com_fat else None,
                "por_rede": dict(sorted(por_rede.items(), key=lambda kv: -kv[1])),
                "mais_proximos": dentro[: args.listar],
            },
            "microterritorio": {
                "_definicoes": "mesmas do produto (api-agent-orbita, radiusSearch)",
                "vendas_totais_no_raio_R$": r_total,
                "media_de_faturamento_por_loja_R$": r_media,
                "lojas_com_faturamento_no_raio": len(com_fat),
                "vendas_totais_na_regiao_R$": reg_total,
                "lojas_com_faturamento_na_regiao": reg_lojas,
                "_regiao_e": (
                    f"o município do ponto ({args.municipio})" if args.municipio
                    else "indisponível: informe --municipio, senão não há cidade de referência"
                ),
                "_divergencia_do_produto": (
                    "o produto soma as cidades tocadas pelo raio; aqui é só a cidade do ponto, "
                    "por decisão de 2026-10-27 — perto de divisa a soma do raio vira macrorregião"
                ),
                "cidades_presentes_no_raio": sorted(cidades_raio),
                "_periodicidade": "fatMedio é faturamento médio MENSAL estimado por PDV",
            },
            "venda_mensal_por_faixa": faixas,
            "venda_por_loja": {
                "no_raio": estatisticas_de_venda(com_fat),
                "na_cidade": estatisticas_de_venda(reg_valores),
                "_fonte": "campo de faturamento médio estimado da camada Concorrentes 2025",
            },
            "lojas_farmarcas_no_raio": {
                "total": len(cadastro),
                "_fonte": "cadastro de lojas (CNPJ + coordenada) — fonte de verdade",
                "ocupando_vaga_de_zoneamento": sum(1 for x in cadastro if x["ocupa_vaga_de_zoneamento"]),
                "itens": cadastro,
                "_erro_cadastro": erro_cadastro,
            },
            "suspeitas_por_nome_de_bandeira": {
                "total": len(nossas),
                "_leitura": (
                    "registros da camada Concorrentes cujo nome casa com bandeira Farmarcas. "
                    "NÃO é prova de que a loja é nossa — confirmar CNPJ no cadastro antes de "
                    "chamar de canibalização."
                ),
                "itens": nossas,
            },
            "qualidade_do_dado": {
                "registros_com_cidade_divergente": len(suspeitos),
                "_criterio": criterio_ref or "sem referência de cidade",
                "_leitura": (
                    "cidade do cadastro diferente do município do ponto. Num raio que cruza divisa "
                    "isso é esperado e NÃO é defeito — só vira suspeita quando a cidade cadastrada "
                    "fica longe demais para o raio alcançar"
                ),
                "implausiveis": [
                    r for r in suspeitos
                    if r["distancia_m"] is not None and r["cidade"] not in cidades_vizinhas
                ],
                "_implausiveis_leitura": "cadastrados em cidade que o raio não alcança — aí sim, erro provável",
                "itens": suspeitos,
            },
            "lacunas": {
                "registros_sem_coordenada_em_concorrentes": sem_coord,
                "lojas_do_cadastro_sem_coordenada_preenchida": lojas_vazias,
                "lojas_do_cadastro_com_coordenada_fora_do_brasil": lojas_invalidas,
                "registros_com_coordenada_fora_do_brasil_descartados": coord_invalida,
                "camadas_indisponiveis_no_raio": SEM_COORDENADA,
                "fluxo_de_passantes": "NÃO existe no dump nem no produto — gap documentado em docs/confluence/ia/analises/estudo-peso-populacao-score-viabilidade.md",
            },
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
