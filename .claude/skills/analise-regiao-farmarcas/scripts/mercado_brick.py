"""Preço médio por unidade e tamanho de mercado no brick IQVIA.

Uso:
    python mercado_brick.py --codigo-ibge 2800308 --uf SE \
        --lat -10.911123 --lng -37.049093
    python mercado_brick.py --uf SE --brick "994-SE_AJU_CENTRO"

Fonte: `cache/iqvia_brick.csv`, gerado por `preparar_iqvia_brick.py` a partir da
aba `DADOS POR BRICK E UTC`. É a única base do acervo com **unidades vendidas**,
e por isso a única que permite preço:

    preço médio por unidade = preco_consumidor / unidade

`preco_consumidor` é RECEITA a preço de consumidor, não preço unitário.

COMO O BRICK É LOCALIZADO — e por que não é exato:
O dump não permite dizer em qual brick um ponto cai (`bricks_iqvia` veio sem
polígono). O nome do brick traz UF e, nas cidades grandes, o BAIRRO:
`994-SE_AJU_CENTRO`. Em cidade grande o município vem abreviado (Aracaju = AJU,
Belo Horizonte = BH), então casar pelo nome do município falha. Casamos por
**UF + bairro do ponto**, e devolvemos também o agregado da UF como referência.
Toda a saída diz qual critério casou.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys

sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
import _bases as B  # noqa: E402
import alternativas as ALT  # noqa: E402 — só por centroide_por_municipio()

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache", "iqvia_brick.csv")


def ler_iqvia():
    if not os.path.exists(CACHE):
        raise FileNotFoundError(
            "base IQVIA por brick não preparada. Rode uma vez, da raiz do projeto: "
            "python .claude/skills/analise-regiao-farmarcas/scripts/preparar_iqvia_brick.py"
        )
    with open(CACHE, encoding="utf-8", newline="") as fh:
        for linha in csv.DictReader(fh):
            yield linha


def bairro_do_ponto(lat: float, lng: float, codigo_ibge: str):
    """Bairro cujo centroide está mais perto do ponto, dentro do município."""
    alvo_mun = str(codigo_ibge).strip()
    melhor = None
    for b in B.ler("bairros"):
        if (b.get("CODMUN") or "").strip() != alvo_mun:
            continue
        la, lo = B.num(b.get("Lat_C")), B.num(b.get("Lon_C"))
        if not B.coordenada_valida(la, lo):
            continue
        d = B.haversine_m(lat, lng, la, lo)
        if melhor is None or d < melhor[0]:
            melhor = (d, (b.get("NOME") or "").strip())
    if not melhor:
        return None, None
    return melhor[1], round(melhor[0])


def agregar(linhas, so_mat_atual=True):
    """Soma unidades e receita, e devolve o preço médio por unidade."""
    uni = rec = 0.0
    n = 0
    por_grupo = {}
    for r in linhas:
        if so_mat_atual and r["flag_mat"] != "MAT atual":
            continue
        u, p = B.num(r["unidade"]), B.num(r["preco_consumidor"])
        if u is None or p is None or u <= 0:
            continue
        uni += u
        rec += p
        n += 1
        g = r["provedor_descricao_grupo"]
        acc = por_grupo.setdefault(g, [0.0, 0.0])
        acc[0] += u
        acc[1] += p
    if not n:
        return None
    saida = {
        "unidades": round(uni),
        "receita_R$": round(rec, 2),
        "preco_medio_por_unidade_R$": round(rec / uni, 2),
        "linhas_agregadas": n,
    }
    saida["por_grupo"] = {
        g: {
            "unidades": round(v[0]),
            "receita_R$": round(v[1], 2),
            "preco_medio_por_unidade_R$": round(v[1] / v[0], 2) if v[0] else None,
        }
        for g, v in sorted(por_grupo.items())
    }
    return saida


def municipio_do_brick(descricao: str, uf: str):
    """Município que dá nome ao brick, ou None quando não dá para saber.

    `1271-CE_CARIUS` → CARIUS. `1262-CE_JUAZEIRO DO NORTE_JARDIM GONZAGA` →
    JUAZEIRO DO NORTE: nome de município tem espaço, nunca underscore, então o
    primeiro `_` depois do prefixo separa a cidade do bairro.

    Devolve None para o brick de capital abreviada (`CE_CEC_ALDEOTA`,
    `SE_AJU_CENTRO`). A abreviação não está em base nenhuma, e adivinhá-la é a
    mesma aposta que trocou o Centro de Lagarto pelo Centro de Aracaju e
    inverteu a conclusão de preço de um dossiê inteiro. Brick que não resolve
    fica FORA da vizinhança, e a saída declara quantos ficaram.
    """
    texto = (descricao or "").strip().upper()
    prefixo = re.match(r"^\s*\d+\s*-\s*" + re.escape(uf.upper()) + r"_", texto)
    if not prefixo:
        return None
    nome = texto[prefixo.end():].split("_", 1)[0].strip()
    return nome or None


def bricks_vizinhos(da_uf, uf, lat, lng, limite=5):
    """Bricks mais próximos do ponto, para quando NENHUM casou por nome.

    Isto NÃO é o brick do ponto, e nada na saída o chama assim. O acervo não
    tem o polígono do brick, então continua sem haver como saber em qual deles
    o endereço cai — e é bem possível que caia justamente num destes, já que um
    brick pode cobrir mais de um município. A pergunta que isto responde é
    outra, mais modesta e ainda útil: qual é o patamar de preço da vizinhança,
    quando a cidade não tem brick com o nome dela.

    Por que não basta pegar o mais próximo e chamá-lo de brick do ponto: foi
    exatamente esse atalho, por sufixo de bairro, que fez um dossiê afirmar
    preço acima da média do estado onde o valor real estava abaixo. Proximidade
    não é pertencimento, e a diferença entre as duas coisas é uma conclusão
    invertida.

    A distância é entre o ponto e o CENTROIDE do município de cada brick, e
    esse centroide é a farmácia real mais próxima da mediana das farmácias da
    cidade. Serve para ordem de grandeza, nunca para medir trajeto.
    """
    try:
        centroides = ALT.centroide_por_municipio()
    except Exception as e:  # noqa: BLE001 — sem centroide, declara e segue
        return None, {"_erro": f"centroides indisponíveis ({type(e).__name__})"}

    por_brick = {}
    for r in da_uf:
        por_brick.setdefault(r["descricao_brick_rpe"].strip(), []).append(r)

    achados, sem_municipio, sem_centroide = [], [], []
    for nome_brick, linhas in por_brick.items():
        mun = municipio_do_brick(nome_brick, uf)
        if not mun:
            sem_municipio.append(nome_brick)
            continue
        ponto = centroides.get((uf.upper(), B.normalizar(mun)))
        if not ponto:
            sem_centroide.append(nome_brick)
            continue
        la, lo = ponto[0], ponto[1]
        if not B.coordenada_valida(la, lo):
            sem_centroide.append(nome_brick)
            continue
        agregado = agregar(linhas)
        if not agregado:
            continue
        achados.append(
            {
                "brick": nome_brick,
                "municipio_do_brick": mun,
                "distancia_km": round(B.haversine_m(lat, lng, la, lo) / 1000.0, 1),
                "farmacias_no_centroide": ponto[2] if len(ponto) > 2 else None,
                **agregado,
            }
        )
    achados.sort(key=lambda c: c["distancia_km"])
    nota = {
        "_o_que_e": (
            "bricks mais próximos do ponto entre os que foi possível localizar — "
            "proximidade entre centroides, NÃO o brick em que o ponto cai"
        ),
        "_por_que_existe": (
            "cidade sem brick com o nome dela ficava só com o agregado da UF, que "
            "mistura capital e interior; a vizinhança diz o patamar da região"
        ),
        "_como_ler": (
            "compare os vizinhos entre si e contra a UF: cidade pequena costuma ficar "
            "abaixo da média do estado e polo regional acima. O valor de um vizinho não "
            "é o preço desta praça"
        ),
        "bricks_da_uf": len(por_brick),
        "bricks_sem_municipio_no_nome": len(sem_municipio),
        "bricks_sem_centroide": len(sem_centroide),
    }
    # Quem ficou de fora precisa ser inspecionável, não só contado: brick
    # excluido por nome que o cache de centroides nao conhece pode ser um
    # vizinho PROXIMO, e aí a vizinhança mente por omissão. Com a lista, quem
    # lê confere se o que sobrou faz sentido geográfico.
    if sem_municipio:
        nota["_fora_sem_municipio_no_nome"] = sorted(sem_municipio)[:8]
    if sem_centroide:
        nota["_fora_sem_centroide"] = sorted(sem_centroide)[:8]
    return achados[:limite], nota


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--uf", required=True)
    ap.add_argument("--codigo-ibge")
    ap.add_argument("--lat", type=float)
    ap.add_argument("--lng", type=float)
    ap.add_argument("--brick", help="nome exato do brick, se já souber")
    args = ap.parse_args()

    uf = args.uf.strip().upper()
    try:
        todas = list(ler_iqvia())
    except FileNotFoundError as e:
        B.emitir({"erro": str(e)})
        return 1

    da_uf = [r for r in todas if (r["codigo_uf"] or "").strip().upper() == uf]
    if not da_uf:
        B.emitir({"erro": f"nenhum brick da UF {uf} na base IQVIA"})
        return 1

    bairro = dist = None
    if args.lat is not None and args.lng is not None and args.codigo_ibge:
        bairro, dist = bairro_do_ponto(args.lat, args.lng, args.codigo_ibge)

    # ORDEM: município ANTES de bairro — e a inversão disso era um defeito grave.
    # O nome do município é sinal forte: brick chamado pelo município É o
    # município. "Centro" é sinal fraco: quase toda cidade tem um, e o nome do
    # brick de bairro traz a capital abreviada (Aracaju = AJU, Belo Horizonte =
    # BH), então o casamento por sufixo cruza cidades sem avisar.
    #
    # Caso real, 2026-10-29: ponto no Centro de Lagarto/SE casou com
    # `994-SE_AJU_CENTRO`, o Centro de Aracaju, a 63 km — porque era o único
    # brick da UF terminado em "_CENTRO". O relatório afirmou preço de R$ 33,22
    # acima da média do estado, quando o brick de Lagarto (`1003-SE_LAGARTO`)
    # devolve R$ 29,02, ABAIXO dela. A conclusão saiu invertida.
    #
    # O bairro continua útil, mas só DEPOIS do município, para refinar quando a
    # cidade tem vários bricks — e, quando o município não casa, o fallback por
    # bairro declara o risco de cruzar cidade em vez de escondê-lo.
    criterio = None
    alvo = []
    nome_municipio = None
    if args.codigo_ibge:
        for m in B.ler("municipios"):
            if (m.get("CD_MUN") or "").strip() == str(args.codigo_ibge).strip():
                nome_municipio = m.get("NM_MUN")
                break

    if args.brick:
        alvo = [r for r in da_uf if r["descricao_brick_rpe"].strip().upper() == args.brick.strip().upper()]
        criterio = f"nome exato do brick informado ({args.brick})"

    if not alvo and nome_municipio:
        chave = B.normalizar(nome_municipio)
        alvo = [r for r in da_uf if chave in B.normalizar(r["descricao_brick_rpe"])]
        if alvo:
            criterio = f"UF + nome do município ({nome_municipio})"
            # Cidade com vários bricks: o bairro refina DENTRO do município.
            nomes = {r["descricao_brick_rpe"] for r in alvo}
            if len(nomes) > 1 and bairro:
                chave_b = B.normalizar(bairro)
                refinado = [r for r in alvo if B.normalizar(r["descricao_brick_rpe"]).endswith("_" + chave_b)]
                if refinado:
                    alvo = refinado
                    criterio = (
                        f"UF + município ({nome_municipio}) + bairro do ponto "
                        f"({bairro}, centroide a {dist} m)"
                    )

    if not alvo and bairro:
        chave = B.normalizar(bairro)
        alvo = [r for r in da_uf if B.normalizar(r["descricao_brick_rpe"]).endswith("_" + chave)]
        if alvo:
            criterio = (
                f"UF + bairro do ponto ({bairro}, centroide a {dist} m) — "
                "SEM casamento por município: o brick pode ser de OUTRA cidade do estado"
            )

    # Nenhum brick casou por nome: em vez de devolver só o agregado da UF — que
    # mistura capital e interior e, no Ceará, vai de R$ 21,29 a R$ 44,17 por
    # unidade —, levanta a vizinhança. Só roda quando o casamento FALHOU: onde
    # há brick nomeado, ele é a resposta e a vizinhança seria ruído.
    vizinhos = nota_vizinhanca = None
    if not alvo and args.lat is not None and args.lng is not None:
        vizinhos, nota_vizinhanca = bricks_vizinhos(da_uf, uf, args.lat, args.lng)

    bricks = sorted({r["descricao_brick_rpe"] for r in alvo})
    # O critério tem de dizer em QUE brick caiu. Sem isso ninguém percebe um
    # casamento cruzado: foi exatamente o que deixou passar o brick de Aracaju.
    if criterio and bricks:
        criterio = f"{criterio} → {', '.join(bricks)}"

    B.emitir(
        {
            "uf": uf,
            "bairro_do_ponto": bairro,
            "distancia_ao_centroide_do_bairro_m": dist,
            "criterio_de_casamento": criterio or (
                "nenhum — nenhum brick leva o nome deste município. O ponto segue SEM "
                "brick conhecido; o que há é a vizinhança, que é proximidade e não "
                "pertencimento"
                if vizinhos
                else "nenhum — só o agregado da UF está disponível"
            ),
            "bricks_casados": bricks,
            "brick": agregar(alvo) if alvo else None,
            "bricks_vizinhos": vizinhos,
            "_vizinhanca": nota_vizinhanca,
            "uf_inteira": agregar(da_uf),
            "_leitura": (
                "preço médio por unidade = receita a preço de consumidor ÷ unidades vendidas, "
                "no MAT atual. Compare o brick contra a UF: preço acima da UF indica mix mais caro "
                "ou menos pressão de desconto na região"
            ),
            "_limites": {
                "localizacao": "o dump não diz em qual brick o ponto cai; o casamento é por nome",
                "vizinhanca": (
                    "quando nenhum brick casa, `bricks_vizinhos` traz os mais próximos por "
                    "centroide de município. É patamar da região, nunca o preço desta praça: "
                    "um brick pode cobrir várias cidades, e o ponto pode estar dentro de um "
                    "deles sem que a base diga qual"
                ),
                "abreviacao": "cidade grande vem abreviada no nome do brick (Aracaju=AJU, Belo Horizonte=BH)",
                "carteira": "a base IQVIA é a carteira ATUAL da Farmarcas, com histórico retroagido",
            },
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
