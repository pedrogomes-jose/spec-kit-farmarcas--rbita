"""Gate de zoneamento Farmarcas — roda ANTES da análise de mercado.

Uso:
    python zoneamento.py --lat -20.5386 --lng -47.4006 \
        --municipio "Franca" --uf SP --codigo-ibge 3516200 \
        --bandeira "Ultra Popular" --modelo popular --perfil novo
    # empresário que já tem loja:
    #   --perfil existente --ge "<nome do responsável pelo GE>"

Fonte da regra: Confluence "4.5 Regras de Zoneamento e Regras de Expansão"
(espaço Gestão Farmarcas, página 3755245621, v5 de 2026-02-24) e "6.1 Regras de
Expansão" (3755769865). Ver references/zoneamento-e-perfil.md para o que a
página NÃO diz e foi decidido fora dela.

Fonte de verdade de "loja nossa": o CADASTRO DE LOJAS (CNPJ + coordenada),
nunca o nome de bandeira dentro da camada Concorrentes — esse dá falso positivo.
"""

from __future__ import annotations

import argparse
import sys

sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
import _bases as B  # noqa: E402

# Distâncias mínimas entre lojas Farmarcas.
# A página 4.5 escreve apenas "raio 300m". A regra vigente, confirmada com o PM
# em 2026-10-27, é 300 m para a MESMA bandeira e 500 m para bandeira DIFERENTE.
# Divergência registrada: a página do Confluence está desatualizada.
DIST_MIN_MESMA_BANDEIRA = 300.0
DIST_MIN_OUTRA_BANDEIRA = 500.0

# Teto de LOJAS por cidade (não de empresários distintos — decisão do PM em
# 2026-10-27; a página fala em "empresários").
FAIXAS = [
    (60_000, 1, "Até 60 mil → 1 loja, sem expansão adicional"),
    (120_000, 2, "60–120 mil → até 2 lojas, a 2ª de bandeira popular, distância mínima"),
    (200_000, 3, "120–200 mil → até 3 lojas, alternância de bandeiras, distância mínima"),
    (None, None, "Acima de 200 mil → sem teto de lojas, ocupação por market share"),
]


def centroides_de_bairro(municipio: str) -> dict:
    """Centroide de cada bairro do município, da camada `bairros` (Lat_C/Lon_C).

    Serve de FALLBACK quando a loja não tem coordenada — 931 das 2.804 não têm.
    Centroide de bairro não é o endereço da loja: só diz a ordem de grandeza.
    Nunca derruba um impedimento sozinho; só evita que a checagem fique cega.
    """
    alvo = B.normalizar(municipio)
    saida = {}
    try:
        for bairro in B.ler("bairros"):
            if B.normalizar(bairro.get("Nm_municip", "")) != alvo:
                continue
            la, lo = B.num(bairro.get("Lat_C")), B.num(bairro.get("Lon_C"))
            if B.coordenada_valida(la, lo):
                saida[B.normalizar(bairro.get("NOME", ""))] = (la, lo)
    except FileNotFoundError:
        pass
    return saida


def faixa_de(pop: int):
    for limite, teto, texto in FAIXAS:
        if limite is None or pop <= limite:
            return limite, teto, texto
    return FAIXAS[-1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lat", type=float, required=True)
    ap.add_argument("--lng", type=float, required=True)
    ap.add_argument("--municipio", required=True)
    ap.add_argument("--uf", required=True)
    ap.add_argument("--codigo-ibge", required=True)
    ap.add_argument("--bandeira", default="", help="bandeira pretendida")
    ap.add_argument("--modelo", default="", choices=["", "popular", "convencional"])
    ap.add_argument("--perfil", default="", choices=["", "novo", "existente"])
    ap.add_argument("--ge", default="", help="responsável pelo GE, quando --perfil existente")
    ap.add_argument("--raio-vizinhanca", type=float, default=1000.0,
                    help="metros; procura loja nossa por COORDENADA, independente da cidade cadastrada")
    ap.add_argument("--populacao", type=int, help="sobrescreve o Censo (use só se a API falhar)")
    args = ap.parse_args()

    # ---- população: é ela que corta a faixa -------------------------------
    if args.populacao:
        pop, origem_pop = args.populacao, "informada na linha de comando"
    else:
        pop, origem_pop = B.populacao_censo_2022(args.codigo_ibge)

    if pop is None:
        B.emitir(
            {
                "veredito": "indeterminado",
                "motivo": "sem população do Censo 2022 não há como aplicar a faixa de zoneamento",
                "detalhe": origem_pop,
                "como_resolver": "rodar com rede disponível, ou passar --populacao com o valor do Censo 2022",
            }
        )
        return 1

    limite, teto, texto_regra = faixa_de(pop)

    # ---- lojas da cidade no cadastro --------------------------------------
    cidade_alvo = B.normalizar(args.municipio)
    uf_alvo = args.uf.strip().upper()
    ocupam, desativadas, sem_coord = [], [], 0
    ges = set()
    # Loja fisicamente perto do ponto mas cadastrada em OUTRA cidade. Caso real
    # verificado em 2026-10-27: loja cadastrada em Patrocínio Paulista/SP a 342 m
    # do centro de Franca/SP (~25 km de distância real entre as duas cidades).
    # O filtro por nome de cidade sozinho não enxerga esses casos.
    vizinhas_de_outra_cidade = []
    bairros = centroides_de_bairro(args.municipio)

    for loja in B.ler_cadastro_lojas():
        mesma_cidade = (
            B.normalizar(loja.get("Cidade - Endereço Receita", "")) == cidade_alvo
            and (loja.get("Estado - Endereço Receita", "") or "").strip().upper() == uf_alvo
        )

        if not mesma_cidade:
            la = B.num(loja.get("Latitude - Endereço Receita"))
            lo = B.num(loja.get("Longitude - Endereço Receita"))
            if B.coordenada_valida(la, lo):
                d = B.haversine_m(args.lat, args.lng, la, lo)
                if d <= args.raio_vizinhanca:
                    vizinhas_de_outra_cidade.append(
                        {
                            "bandeira": (loja.get("Bandeira") or "").strip(),
                            "status": (loja.get("Status") or "").strip(),
                            "cidade_cadastrada": (loja.get("Cidade - Endereço Receita") or "").strip(),
                            "uf_cadastrada": (loja.get("Estado - Endereço Receita") or "").strip(),
                            "distancia_m": round(d),
                        }
                    )
            continue

        lat = B.num(loja.get("Latitude - Endereço Receita"))
        lng = B.num(loja.get("Longitude - Endereço Receita"))
        dist = (
            round(B.haversine_m(args.lat, args.lng, lat, lng))
            if B.coordenada_valida(lat, lng)
            else None
        )
        if dist is None:
            sem_coord += 1

        aprox = None
        if dist is None:
            centro = bairros.get(B.normalizar(loja.get("Bairro - Endereço Receita", "")))
            if centro:
                aprox = round(B.haversine_m(args.lat, args.lng, centro[0], centro[1]))

        ge_loja = (loja.get("Nome do responsável pelo GE", "") or "").strip()
        registro = {
            "bandeira": (loja.get("Bandeira", "") or "").strip(),
            "modelo": (loja.get("Modelo de Negócio", "") or "").strip(),
            "status": (loja.get("Status", "") or "").strip(),
            "bairro": (loja.get("Bairro - Endereço Receita", "") or "").strip(),
            "distancia_m": dist,
            "distancia_aproximada_por_centroide_do_bairro_m": aprox,
            # LGPD: o nome do GE entra só como relação, nunca como texto de saída.
            "do_solicitante": bool(args.ge) and B.normalizar(ge_loja) == B.normalizar(args.ge),
        }
        if registro["status"] in B.STATUS_OCUPA_VAGA:
            ocupam.append(registro)
            if ge_loja:
                ges.add(B.normalizar(ge_loja))
        else:
            desativadas.append(registro)

    ocupam.sort(key=lambda r: (r["distancia_m"] is None, r["distancia_m"]))
    desativadas.sort(key=lambda r: (r["distancia_m"] is None, r["distancia_m"]))

    impedimentos, alertas = [], []

    # ---- teto de lojas -----------------------------------------------------
    # A regra vigente conta LOJAS (decisão do PM, 2026-10-27). A página 4.5
    # escreve "empresários". As duas leituras divergem MUITO na prática: sobre
    # 830 cidades com loja ativa e código IBGE resolvido, 207 (25%) estouram o
    # teto contando lojas e apenas 34 (4%) contando empresários distintos.
    # Exemplo: Passos/MG, teto 2, tem 7 lojas de 1 único empresário.
    # Por isso a saída SEMPRE mostra as duas contagens.
    if teto is not None and len(ocupam) >= teto:
        impedimentos.append(
            {
                "regra": texto_regra,
                "constatado": f"a cidade já tem {len(ocupam)} loja(s) Farmarcas ocupando vaga; o teto da faixa é {teto}",
                "fonte": "Confluence 4.5 Regras de Zoneamento + cadastro de lojas",
                "leitura": "teto conta LOJAS (regra vigente confirmada com o PM em 2026-10-27)",
            }
        )
        if len(ges) <= teto:
            alertas.append(
                {
                    "regra": "as duas leituras do teto discordam neste caso",
                    "constatado": (
                        f"{len(ocupam)} lojas (acima do teto {teto}) mas apenas {len(ges)} "
                        f"empresário(s) distinto(s) (dentro do teto)"
                    ),
                    "ressalva": (
                        "a página 4.5 escreve 'empresários'; a regra aplicada conta lojas. "
                        "Na rede inteira, 25% das cidades estouram o teto por lojas contra 4% por empresários"
                    ),
                }
            )

    # ---- 2ª loja tem de ser popular (faixa 60–120 mil) ---------------------
    if limite == 120_000 and len(ocupam) == 1 and args.modelo == "convencional":
        impedimentos.append(
            {
                "regra": "60–120 mil → a 2ª loja deve ser de bandeira popular",
                "constatado": "a loja pretendida é Convencional",
                "fonte": "Confluence 4.5 Regras de Zoneamento",
            }
        )

    # ---- distância mínima --------------------------------------------------
    if pop > 60_000:
        alvo = B.normalizar(args.bandeira)
        for loja in ocupam:
            if loja["distancia_m"] is None:
                continue
            mesma = alvo and B.normalizar(loja["bandeira"]) == alvo
            minimo = DIST_MIN_MESMA_BANDEIRA if mesma else DIST_MIN_OUTRA_BANDEIRA
            if loja["distancia_m"] < minimo:
                item = {
                    "regra": f"distância mínima {int(minimo)} m ({'mesma' if mesma else 'outra'} bandeira)",
                    "constatado": f"loja {loja['bandeira']} a {loja['distancia_m']} m",
                    "de_quem": "do próprio solicitante" if loja["do_solicitante"] else "de outro associado",
                    "fonte": "regra vigente confirmada com o PM em 2026-10-27 (a página 4.5 só cita 300 m)",
                }
                if pop > 200_000:
                    item["ressalva"] = "a página não declara distância mínima acima de 200 mil — tratado como ALERTA"
                    alertas.append(item)
                else:
                    impedimentos.append(item)
        if not alvo:
            alertas.append(
                {
                    "regra": "distância mínima depende da bandeira pretendida",
                    "constatado": "bandeira não informada — aplicado o critério de outra bandeira (500 m)",
                }
            )

    # ---- alternância de bandeiras (faixa 120–200 mil) ----------------------
    if limite == 200_000 and args.bandeira:
        repetida = [l for l in ocupam if B.normalizar(l["bandeira"]) == B.normalizar(args.bandeira)]
        if repetida:
            alertas.append(
                {
                    "regra": "120–200 mil → alternância de bandeiras",
                    "constatado": f"a cidade já tem {len(repetida)} loja(s) da bandeira pretendida",
                    "ressalva": "a página não diz se a alternância é obrigatória — tratado como ALERTA",
                }
            )

    # ---- acima de 200 mil: ocupação por market share -----------------------
    if limite is None:
        alertas.append(
            {
                "regra": "Acima de 200 mil → ocupação por market share",
                "constatado": "não há teto de lojas; a decisão é por share, que o zoneamento não quantifica",
                "ressalva": "rodar mercado_utc.py e decidir com a área de Expansão",
            }
        )

    sem_distancia_real = [l for l in ocupam if l["distancia_m"] is None]
    if pop > 60_000 and sem_distancia_real:
        aproximadas = [l for l in sem_distancia_real if l["distancia_aproximada_por_centroide_do_bairro_m"]]
        mais_perto = min(
            (l["distancia_aproximada_por_centroide_do_bairro_m"] for l in aproximadas), default=None
        )
        alertas.append(
            {
                "regra": "distância mínima NÃO pôde ser checada",
                "constatado": (
                    f"{len(sem_distancia_real)} loja(s) Farmarcas da cidade estão sem coordenada no cadastro"
                    + (
                        f"; pelo centroide do bairro a mais próxima fica a ~{mais_perto} m"
                        if mais_perto is not None
                        else ""
                    )
                ),
                "ressalva": (
                    "centroide de bairro não é o endereço da loja — indica ordem de grandeza, "
                    "não substitui a checagem. Geocodificar os endereços resolve"
                ),
                "itens": sem_distancia_real,
            }
        )

    if vizinhas_de_outra_cidade:
        alertas.append(
            {
                "regra": "checagem de cadastro, não de zoneamento",
                "constatado": (
                    f"{len(vizinhas_de_outra_cidade)} loja(s) Farmarcas a até {int(args.raio_vizinhanca)} m do ponto "
                    f"estão cadastradas em OUTRA cidade"
                ),
                "ressalva": (
                    "o teto de zoneamento é contado por cidade cadastrada; se o cadastro estiver errado, "
                    "o teto desta cidade está errado junto. Confirmar antes de concluir"
                ),
                "itens": vizinhas_de_outra_cidade,
            }
        )

    veredito = "impedimento" if impedimentos else ("alerta" if alertas else "liberado")

    leitura_perfil = None
    if args.perfil == "existente":
        proprias = [l for l in ocupam if l["do_solicitante"]]
        leitura_perfil = {
            "perfil": "empresário que já opera loja(s) Farmarcas",
            "lojas_do_solicitante_nesta_cidade": len(proprias),
            "_leitura": (
                "Sobreposição com loja DO PRÓPRIO solicitante pode ser escolha estratégica "
                "(fechar mercado, ganhar share e poder de negociação) — mas o zoneamento NÃO "
                "abre exceção para isso: o teto conta lojas, de quem quer que sejam. "
                "Sobreposição com loja de OUTRO associado é o conflito que a regra existe para evitar."
            ),
        }
    elif args.perfil == "novo":
        leitura_perfil = {
            "perfil": "empresário novo, sem loja Farmarcas",
            "_leitura": "canibalização aqui é sempre com loja de terceiro — nenhuma sobreposição é estratégica para ele.",
        }

    B.emitir(
        {
            "veredito": veredito,
            "municipio": {"nome": args.municipio, "uf": uf_alvo, "codigo_ibge": args.codigo_ibge},
            "populacao_censo_2022": pop,
            "_origem_populacao": origem_pop,
            "faixa_aplicada": texto_regra,
            "teto_de_lojas": teto,
            "lojas_ocupando_vaga": len(ocupam),
            "empresarios_distintos_na_cidade": len(ges),
            "_duas_leituras_do_teto": {
                "contando_lojas": {"valor": len(ocupam), "acima_do_teto": teto is not None and len(ocupam) > teto},
                "contando_empresarios": {"valor": len(ges), "acima_do_teto": teto is not None and len(ges) > teto},
                "_aplicada": "contando lojas",
                "_nota": "na rede inteira: 207 de 830 cidades (25%) estouram por lojas, 34 (4%) por empresários",
            },
            "impedimentos": impedimentos,
            "alertas": alertas,
            "perfil_do_solicitante": leitura_perfil,
            "lojas_farmarcas_na_cidade": ocupam,
            "lojas_desativadas_na_cidade": desativadas,
            "lojas_proximas_cadastradas_em_outra_cidade": vizinhas_de_outra_cidade,
            "lacunas": {
                "lojas_da_cidade_sem_coordenada": sem_coord,
                "_impacto": "sem coordenada não dá para checar distância mínima dessas lojas",
                "cobertura_de_coordenada_no_cadastro": "1.841 de 2.804 lojas (66%) têm coordenada utilizável; 931 vazias e 32 fora do Brasil (dump de 2026-10-23)",
                "premissa_status": f"ocupam vaga: {', '.join(B.STATUS_OCUPA_VAGA)} — desativada não ocupa (premissa, não está na regra)",
                "limites_de_faixa": "a página escreve faixas sobrepostas (60, 120 e 200 mil habitantes); aqui os cortes são tratados como fechados em 60.000, 120.000 e 200.000",
                "popular_x_convencional": "a página diz que as regras diferem entre loja popular e convencional, sem detalhar a diferença",
            },
            "_fonte_da_regra": "Confluence 3755245621 (4.5) v5 2026-02-24 e 3755769865 (6.1) v8 2026-02-24",
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
