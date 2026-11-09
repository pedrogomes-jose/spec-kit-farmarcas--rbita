"""Onde mais olhar: praças com mercado grande e pouca Farmarcas dentro.

Uso:
    python alternativas.py --uf SE --limite 12
    python alternativas.py --uf SE --excluir-municipio 2800308

Existe porque analisar só o ponto pedido responde "este serve?", e não "onde
seria melhor?". Cruza, por UTC:

  - receita total do mercado e crescimento  (mat_anterior_x_atual_utc_crescimento)
  - receita Farmarcas na UTC                (mesma base)
  - município da UTC                        (closeup_utc_varejo)
  - lojas Farmarcas ativas no município     (cadastro de lojas)
  - população do Censo 2022, quando em cache (faixa de zoneamento)

e devolve as praças ordenadas por mercado não atendido — receita total onde a
Farmarcas não fatura — já marcando se o zoneamento ainda tem vaga.

NÃO é recomendação de abertura: é lista de onde vale rodar um dossiê.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
import _bases as B  # noqa: E402

CACHE_CENSO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache", "censo2022.json")


CAMPO_POT_ANO = "1PotencialdeConsumoemR$-MedicamentoseHigieneecuidadospessoais-ANO"
CAMPO_POT_MES = "2PotencialdeConsumoemR$-Medicamentos+Higieneecuidadospessoais-MES"
CACHE_IQVIA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache", "iqvia_brick.csv")


def potencial_por_municipio() -> dict:
    """Potencial de consumo em drogarias por município — a base declara ANO e MÊS."""
    saida = {}
    for linha in B.ler("potencial_de_consumo"):
        cod = (linha.get("CODIGO") or "").strip()
        if not cod:
            continue
        saida[cod] = {
            "ano": B.num(linha.get(CAMPO_POT_ANO)),
            "mes": B.num(linha.get(CAMPO_POT_MES)),
        }
    return saida


def preco_por_municipio(uf: str) -> dict:
    """Preço médio por unidade dos bricks de cada município da UF.

    O nome do brick é `<num>-<UF>_<CIDADE>` e, nas cidades grandes, vem com o
    município abreviado (Aracaju = AJU). Então só casa onde o nome aparece
    inteiro — e é por isso que a saída devolve None em vez de forçar um número.
    """
    if not os.path.exists(CACHE_IQVIA):
        return {}
    import csv as _csv

    linhas = []
    with open(CACHE_IQVIA, encoding="utf-8", newline="") as fh:
        for r in _csv.DictReader(fh):
            if (r["codigo_uf"] or "").strip().upper() == uf and r["flag_mat"] == "MAT atual":
                linhas.append(r)

    nomes = {}
    for m in B.ler("municipios"):
        if (m.get("SIGLA_UF") or "").strip().upper() == uf:
            nomes[(m.get("CD_MUN") or "").strip()] = B.normalizar(m.get("NM_MUN", ""))

    saida = {}
    for cod, nome in nomes.items():
        uni = rec = 0.0
        for r in linhas:
            if nome and nome in B.normalizar(r["descricao_brick_rpe"]):
                u, pr = B.num(r["unidade"]), B.num(r["preco_consumidor"])
                if u and pr and u > 0:
                    uni += u
                    rec += pr
        saida[cod] = round(rec / uni, 2) if uni else None
    return saida


CACHE_CENTROIDES = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "cache", "centroides_municipios_v2.json"
)


def centroide_por_municipio() -> dict:
    """Centroide aproximado de cada município, por (UF, CIDADE) normalizados.

    O acervo NÃO traz coordenada de município: o polígono da UTC e o do setor
    ficaram no asset, e a coluna `geometry` do CSV guarda só a palavra "Polygon".
    A camada de concorrentes, porém, traz LAT/LONG por farmácia e cobre o país
    inteiro — farmácia existe em toda cidade. A MEDIANA das farmácias de uma
    cidade é, então, um centroide utilizável.

    Mediana e não média: a própria camada tem registros cadastrados numa cidade
    com coordenada em outra, e a média seria arrastada por eles. A mediana
    ignora o outlier sem precisar detectá-lo.

    MAS a mediana sozinha não basta, e o motivo custou uma praça falsa num
    dossiê (2026-11-06). Ela é calculada separadamente para latitude e
    longitude, então quando os registros da cidade se dividem entre dois
    lugares distantes o par (mediana_lat, mediana_lng) cai ENTRE os dois
    grupos — num lugar onde não existe farmácia nenhuma. Martins/RN tem 4
    registros: 2 em Martins/RN e 2 com coordenada de Presidente Médici/RO. A
    mediana devolvia -8,63/-49,91, no sul do Pará, e a cidade aparecia a 68 km
    de um ponto em Redenção/PA estando a ~2.000 km. Medido na camada inteira:
    81 dos 6.193 municípios com coordenada (1,3%) recebiam centroide num lugar
    sem farmácia alguma, até 1.675 km do registro mais próximo — 59 deles com
    exatamente 2 registros, que é a assinatura do defeito.

    Por isso a mediana é apenas a SEMENTE: o centroide devolvido é a farmácia
    real mais próxima dela. Assim o ponto é sempre um endereço que existe na
    camada, nunca um lugar interpolado. Em cidade com registro espalhado entre
    dois lugares, ele cai no grupo maior; no empate de 2 contra 2, cai num dos
    dois — e `dispersao_km` denuncia o caso, porque fica alta.

    É aproximação declarada, não geometria oficial: serve para ordenar praças
    por proximidade e para dizer a ordem de grandeza da distância, nunca para
    medir distância entre dois endereços.
    """
    if os.path.exists(CACHE_CENTROIDES):
        try:
            with open(CACHE_CENTROIDES, encoding="utf-8") as fh:
                return {tuple(k.split("\t")): v for k, v in json.load(fh).items()}
        except Exception:
            pass

    import statistics as _st

    pontos = {}
    for linha in B.ler("concorrentes_2025"):
        la, lo = B.num(linha.get("LAT")), B.num(linha.get("LONG"))
        if not B.coordenada_valida(la, lo):
            continue
        chave = (B.normalizar(linha.get("UF")), B.normalizar(linha.get("CIDADE")))
        if not chave[0] or not chave[1]:
            continue
        pontos.setdefault(chave, []).append((la, lo))

    saida = {}
    for k, v in pontos.items():
        sla = _st.median(p[0] for p in v)
        slo = _st.median(p[1] for p in v)
        # Encaixa a semente no registro real mais proximo: o centroide passa a
        # ser sempre uma farmacia que existe, nunca um ponto interpolado entre
        # dois grupos distantes. O(n) por cidade.
        la, lo = min(v, key=lambda p: B.haversine_m(sla, slo, p[0], p[1]))
        disp = round(_st.median(B.haversine_m(la, lo, p[0], p[1]) for p in v) / 1000.0, 1)
        saida[k] = [round(la, 6), round(lo, 6), len(v), disp]
    try:
        os.makedirs(os.path.dirname(CACHE_CENTROIDES), exist_ok=True)
        with open(CACHE_CENTROIDES, "w", encoding="utf-8") as fh:
            json.dump({"\t".join(k): v for k, v in saida.items()}, fh)
    except Exception:
        pass
    return saida


def partes_da_utc(nome: str) -> tuple:
    """Separa `UF-MUNICIPIO-LOCALIDADE` em (município, localidade).

    Município pequeno tem UTC única e nome sem localidade (`RN-ACARI`);
    município grande tem várias, cada uma com a sua (`RN-NATAL-CIDADE NOVA`).
    É a localidade que distingue uma linha da outra na mesma cidade — sem ela,
    Natal aparece onze vezes com números diferentes e nada explica a diferença.
    """
    pedacos = [p.strip() for p in (nome or "").split("-") if p.strip()]
    if len(pedacos) <= 1:
        return (nome or "").strip(), ""
    if len(pedacos) == 2:
        return pedacos[1], ""
    return pedacos[1], "-".join(pedacos[2:])


def teto_de_lojas(pop: int):
    if pop <= 60_000:
        return 1
    if pop <= 120_000:
        return 2
    if pop <= 200_000:
        return 3
    return None


def disponibilidade(pop, teto, n_grupos: int, modelo: str | None):
    """Cabe um grupo NOVO nesta praça? Devolve (bool|None, motivo legível).

    Conta GRUPOS, não lojas. Cidade com cinco lojas de um único dono e teto 2
    continua disponível: o que a regra protege é a convivência entre associados,
    e não há conflito onde só há um. Contar lojas aqui esconderia justamente as
    praças que a lista existe para mostrar.

    A faixa de 60 a 120 mil acrescenta uma condição que depende de QUEM pergunta:
    o 2º grupo a entrar tem de trazer bandeira popular. Uma praça dessa faixa com
    um grupo instalado está aberta para quem pretende bandeira popular e fechada
    para quem pretende convencional — a mesma linha, duas respostas.
    """
    if pop is None:
        return None, "sem população do Censo em cache — disponibilidade não apurada"
    if teto is None:
        return True, "sem teto (acima de 200 mil habitantes)"
    if n_grupos >= teto:
        return False, f"sem vaga — {n_grupos} grupo(s) para um teto de {teto}"
    # vaga existe; falta checar a exigência de bandeira popular do 2º grupo
    if teto == 2 and n_grupos == 1 and modelo == "convencional":
        return False, (
            "vaga existe, mas o 2º grupo desta faixa só entra com bandeira popular "
            "e o pedido é convencional"
        )
    sobra = teto - n_grupos
    return True, f"cabe grupo novo — {n_grupos} de {teto}, {sobra} vaga(s)"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--uf", help="limita a uma UF (recomendado)")
    ap.add_argument("--excluir-municipio", help="código IBGE a tirar da lista")
    ap.add_argument("--limite", type=int, default=12)
    ap.add_argument("--min-receita", type=float, default=5_000_000.0)
    ap.add_argument("--modelo", choices=["popular", "convencional"],
                    help="modelo pretendido; decide a faixa 60-120 mil, onde o 2o grupo tem de ser popular")
    ap.add_argument("--so-disponiveis", action="store_true",
                    help="devolve apenas pracas onde cabe um grupo novo pela regra vigente")
    # Sem ancora geografica a lista e funcao da UF, nao do pedido: medido em
    # 2026-11-05, Pouso Alegre e Ipatinga (mesma UF, 390 km entre si) recebiam
    # listas IDENTICAS, 15 de 15 pracas iguais, nenhuma a menos de 150 km de
    # qualquer um dos dois. Ordenar por mercado absoluto entrega sempre a capital.
    ap.add_argument("--perto-de", metavar="LAT,LNG",
                    help="coordenada do ponto pedido; calcula a distancia ate cada praca")
    ap.add_argument("--raio-km", type=float,
                    help="descarta pracas alem deste raio (exige --perto-de)")
    ap.add_argument("--ordenar", choices=["mercado", "distancia"], default="mercado",
                    help="criterio de ordenacao; distancia exige --perto-de")
    args = ap.parse_args()

    ancora = None
    if args.perto_de:
        try:
            _la, _lo = (float(x) for x in args.perto_de.replace(";", ",").split(",")[:2])
            ancora = (_la, _lo)
        except Exception:
            print("ERRO: --perto-de espera LAT,LNG (ex.: -22.21,-45.90)", file=sys.stderr)
            return 2
    if (args.ordenar == "distancia" or args.raio_km) and not ancora:
        print("ERRO: --ordenar distancia e --raio-km exigem --perto-de", file=sys.stderr)
        return 2

    # UTC -> município
    utc_para_mun = {}
    for linha in B.ler("closeup_utc_varejo"):
        uid = (linha.get("id_utc_var") or "").strip()
        if uid:
            utc_para_mun[uid] = {
                "codigo_ibge": (linha.get("codigo_mun") or "").strip(),
                "municipio": (linha.get("municipio") or "").strip(),
                "uf": (linha.get("uf") or "").strip().upper(),
                "nome_utc": (linha.get("nome_utc_v") or "").strip(),
            }

    # lojas ativas por município
    lojas = {}
    # GRUPOS, nao lojas: e o grupo que ocupa vaga no teto. A deduplicacao e por
    # NOME do responsavel normalizado, nao por CNPJ — mesma fragilidade do gate,
    # e aqui ela decide quais pracas aparecem na lista. Grafia divergente entre
    # duas lojas do mesmo dono inventa um grupo e esconde uma praca disponivel.
    grupos = {}
    # Bandeiras ja presentes: a faixa 60-120 mil exige que o 2o grupo entre com
    # bandeira popular, entao a praca pode ter vaga e mesmo assim estar fechada
    # para quem pretende bandeira convencional.
    for loja in B.ler_cadastro_lojas():
        if (loja.get("Status") or "").strip() not in B.STATUS_OCUPA_VAGA:
            continue
        chave = (
            B.normalizar(loja.get("Cidade - Endereço Receita", "")),
            (loja.get("Estado - Endereço Receita") or "").strip().upper(),
        )
        lojas[chave] = lojas.get(chave, 0) + 1
        ge = B.normalizar(loja.get("Nome do responsável pelo GE", ""))
        if ge:
            grupos.setdefault(chave, set()).add(ge)

    censo = {}
    if os.path.exists(CACHE_CENSO):
        try:
            with open(CACHE_CENSO, encoding="utf-8") as fh:
                censo = json.load(fh)
        except (OSError, ValueError):
            censo = {}

    potenciais = potencial_por_municipio()
    precos = preco_por_municipio(args.uf.strip().upper()) if args.uf else {}

    candidatos = []
    for linha in B.ler("mat_anterior_x_atual_utc_crescimento"):
        uid = (linha.get("utc_id_varejo") or "").strip()
        meta = utc_para_mun.get(uid)
        if not meta:
            continue
        if args.uf and meta["uf"] != args.uf.strip().upper():
            continue
        if args.excluir_municipio and meta["codigo_ibge"] == args.excluir_municipio.strip():
            continue

        total = B.num(linha.get("receita_atual_total")) or 0.0
        nosso = B.num(linha.get("receita_atual_farmarcas")) or 0.0
        if total < args.min_receita:
            continue

        pop = censo.get(meta["codigo_ibge"])
        teto = teto_de_lojas(pop) if pop else None
        _chave_mun = (B.normalizar(meta["municipio"]), meta["uf"])
        ativas = lojas.get(_chave_mun, 0)
        n_grupos = len(grupos.get(_chave_mun, ()))
        disp, motivo = disponibilidade(pop, teto, n_grupos, args.modelo)

        pot = potenciais.get(meta["codigo_ibge"]) or {}
        pot_ano = pot.get("ano")

        _mun_utc, _loc = partes_da_utc(meta["nome_utc"])
        candidatos.append(
            {
                "municipio": meta["municipio"],
                "localidade": _loc,
                "praca": f"{meta['municipio']} — {_loc}" if _loc else meta["municipio"],
                "uf": meta["uf"],
                "codigo_ibge": meta["codigo_ibge"],
                "utc": meta["nome_utc"],
                "receita_mercado_R$": round(total, 2),
                "receita_mercado_anterior_R$": round(B.num(linha.get("receita_anterior_total")) or 0.0, 2),
                "receita_farmarcas_R$": round(nosso, 2),
                "mercado_nao_atendido_R$": round(total - nosso, 2),
                "share_farmarcas": round(nosso / total, 4) if total else None,
                "crescimento_mercado": B.num(linha.get("crescimento_total")),
                "crescimento_farmarcas": B.num(linha.get("crescimento_farmarcas")),
                "lojas_farmarcas_no_municipio": ativas,
                "grupos_economicos_no_municipio": n_grupos,
                "potencial_consumo_drogarias_ano_R$": pot_ano,
                "potencial_consumo_drogarias_mes_R$": pot.get("mes"),
                "_potencial_e": "do MUNICÍPIO inteiro — não existe potencial por UTC nas bases",
                "preco_medio_por_unidade_R$": precos.get(meta["codigo_ibge"]),
                "populacao_censo_2022": pop,
                "teto_de_lojas": teto,
                "zoneamento": motivo,
                "disponivel_para_grupo_novo": disp,
            }
        )

    # CAPTURA É MUNICIPAL, e repete nas UTCs da mesma cidade. Dividir a receita
    # de UMA UTC pelo potencial do município inteiro dá razão sem sentido — era
    # o que acontecia, e fazia Natal parecer capturar 19%, 12%, 8% e 5% em
    # bairros diferentes. O numerador precisa ser a receita do município toda.
    receita_por_municipio: dict = {}
    for c in candidatos:
        k = c["codigo_ibge"]
        receita_por_municipio[k] = receita_por_municipio.get(k, 0.0) + (c["receita_mercado_R$"] or 0)
    for c in candidatos:
        pot_ano = c.get("potencial_consumo_drogarias_ano_R$")
        rec_mun = receita_por_municipio.get(c["codigo_ibge"], 0.0)
        c["receita_do_municipio_R$"] = round(rec_mun, 2)
        c["taxa_de_captura_do_municipio"] = round(rec_mun / pot_ano, 4) if pot_ano else None
        c["_taxa_de_captura"] = (
            "receita somada de todas as UTCs do município ÷ potencial anual do município — "
            "é indicador MUNICIPAL, igual para todas as linhas da mesma cidade"
        )
        c["potencial_nao_capturado_R$"] = round(pot_ano - rec_mun, 2) if pot_ano else None


    def escala(v):
        if v is None:
            return "—"
        if abs(v) >= 1e9:
            return f"R$ {v / 1e9:.2f} bilhões".replace(".", ",")
        if abs(v) >= 1e6:
            return f"R$ {v / 1e6:.1f} milhões".replace(".", ",")
        if abs(v) >= 1e3:
            return f"R$ {v / 1e3:.0f} mil".replace(".", ",")
        return f"R$ {v:.2f}".replace(".", ",")

    for c in candidatos:
        # Frase montada a partir dos próprios números — é recomposição, não
        # interpretação. Nenhum juízo entra aqui.
        onde = f"em {c['localidade']}" if c.get("localidade") else "no município"
        pedacos = [f"mercado de {escala(c['mercado_nao_atendido_R$'])} sem receita nossa dentro, {onde}"]
        if c["lojas_farmarcas_no_municipio"] == 0:
            pedacos.append("nenhuma loja Farmarcas na cidade")
        else:
            pedacos.append(f"{c['lojas_farmarcas_no_municipio']} loja(s) Farmarcas já na cidade")
        if c["crescimento_mercado"]:
            pedacos.append(f"mercado crescendo {c['crescimento_mercado'] * 100:.0f}%")
        if c["taxa_de_captura_do_municipio"]:
            pedacos.append(
                f"{c['taxa_de_captura_do_municipio'] * 100:.0f}% do potencial anual do município já capturado"
            )
        if c["preco_medio_por_unidade_R$"]:
            pedacos.append(f"preço médio de R$ {c['preco_medio_por_unidade_R$']:.2f} por unidade".replace(".", ","))
        if c["crescimento_farmarcas"] is not None and c["crescimento_farmarcas"] < 0:
            pedacos.append("ATENÇÃO: a receita Farmarcas caiu aqui — praça possivelmente já testada")
        c["escala_mercado_nao_atendido"] = escala(c["mercado_nao_atendido_R$"])
        c["motivo"] = "; ".join(pedacos) + "."

    # --- distancia ate o ponto pedido
    # Sem isto a lista responde a pergunta errada. Quem recebeu um "nao" precisa
    # de praca que consiga operar, e a praca mais rica da UF e sempre a capital:
    # a mesma lista servia para dois pedidos a 390 km um do outro.
    sem_centroide = 0
    if ancora:
        cen = centroide_por_municipio()
        for c in candidatos:
            ponto = cen.get((B.normalizar(c["uf"]), B.normalizar(c["municipio"])))
            if not ponto:
                c["distancia_km"] = None
                c["_distancia_ausente"] = "município sem farmácia com coordenada na camada de concorrentes"
                sem_centroide += 1
                continue
            c["distancia_km"] = round(
                B.haversine_m(ancora[0], ancora[1], ponto[0], ponto[1]) / 1000.0, 1
            )
            c["_centroide_do_municipio"] = {
                "lat": ponto[0], "lng": ponto[1], "farmacias_usadas": ponto[2],
                # Distancia mediana das farmacias da cidade ate o centroide. Alta
                # significa registro espalhado entre lugares distantes — a cidade
                # existe, mas a distancia ate ela e menos confiavel.
                "dispersao_km": ponto[3] if len(ponto) > 3 else None,
                "_metodo": "farmácia real mais próxima da mediana das coordenadas da cidade — aproximação, não geometria oficial",
            }
            if c.get("motivo"):
                c["motivo"] = f"a {c['distancia_km']:.0f} km do ponto pedido; " + c["motivo"]

    disponiveis_no_raio = None
    if args.raio_km:
        dentro = [c for c in candidatos if c.get("distancia_km") is not None
                  and c["distancia_km"] <= args.raio_km]
        # Contar o que SOBREVIVE ao filtro de disponibilidade, nao o que cai no
        # raio: medido em Araputanga/MT, havia 10 pracas a menos de 150 km e
        # NENHUMA disponivel — o raio era aplicado, a disponibilidade esvaziava
        # a lista depois, e o relatorio saia com tabela vazia e sem explicacao.
        uteis = [c for c in dentro if c["disponivel_para_grupo_novo"]] if args.so_disponiveis else dentro
        disponiveis_no_raio = len(uteis)
        # Raio que nao devolve nada e pior que raio nenhum: o leitor fica sem
        # caminho e sem saber por que. Cai para a lista inteira e DECLARA.
        raio_aplicado = disponiveis_no_raio >= 3
        if raio_aplicado:
            candidatos = dentro
    else:
        raio_aplicado = False

    if args.ordenar == "distancia":
        # None por ultimo: praca sem centroide nao e praca perto.
        candidatos.sort(key=lambda c: (c.get("distancia_km") is None,
                                       c.get("distancia_km") or 0.0,
                                       -c["mercado_nao_atendido_R$"]))
    else:
        candidatos.sort(key=lambda c: -c["mercado_nao_atendido_R$"])

    # Só os finalistas puxam o Censo da API — é uma chamada por município, e
    # sem ela a coluna de zoneamento fica inconclusiva justamente onde importa.
    for c in candidatos[: args.limite]:
        if c["populacao_censo_2022"] is None and c["codigo_ibge"]:
            pop, _origem = B.populacao_censo_2022(c["codigo_ibge"])
            if pop:
                c["populacao_censo_2022"] = pop
                c["teto_de_lojas"] = teto_de_lojas(pop)
                c["zoneamento"] = (
                    "sem teto (acima de 200 mil)"
                    if c["teto_de_lojas"] is None
                    else ("COM VAGA" if c["lojas_farmarcas_no_municipio"] < c["teto_de_lojas"] else "SEM VAGA")
                )

    B.emitir(
        {
            "filtro": {
                "uf": args.uf,
                "municipio_excluido": args.excluir_municipio,
                "receita_minima_R$": args.min_receita,
            },
            "utcs_avaliadas": len(candidatos),
            "melhores": [c for c in candidatos if c["disponivel_para_grupo_novo"]][: args.limite]
            if args.so_disponiveis
            else candidatos[: args.limite],
            "_disponibilidade": {
                "_regra": "cabe grupo novo quando os grupos econômicos com loja ativa na cidade são MENOS que o teto da faixa — e, na faixa de 60 a 120 mil, o 2º grupo só entra com bandeira popular",
                "_apuracao_do_grupo": "responsável pelo GE no cadastro, deduplicado por NOME normalizado e não por CNPJ. Grafia divergente entre duas lojas do mesmo dono inventa um grupo e esconde uma praça que está disponível",
                "_modelo_informado": args.modelo or "não informado — a restrição da faixa 60 a 120 mil não foi aplicada",
                "_filtro_aplicado": bool(args.so_disponiveis),
            },
            "_ordenacao": (
                "distância até o ponto pedido, pelo centroide do município; empate desfeito "
                "pelo mercado não atendido"
                if args.ordenar == "distancia"
                else "mercado não atendido = receita total da UTC menos a receita Farmarcas"
            ),
            "_proximidade": {
                "ancora": {"lat": ancora[0], "lng": ancora[1]} if ancora else None,
                "raio_km_pedido": args.raio_km,
                "raio_aplicado": raio_aplicado,
                "pracas_disponiveis_dentro_do_raio": disponiveis_no_raio,
                "_se_nao_aplicado": (
                    None if raio_aplicado or not args.raio_km else
                    f"só {disponiveis_no_raio} praça(s) disponível(is) dentro de "
                    f"{args.raio_km:.0f} km — menos que o mínimo de 3 para a lista ter valor. "
                    "O raio foi ignorado e a lista devolve a UF inteira; a distância de cada "
                    "linha continua declarada, e o fato de não haver praça perto É o achado"
                ),
                "pracas_sem_centroide": sem_centroide if ancora else None,
                "_metodo": (
                    "o acervo não traz coordenada de município — o polígono da UTC ficou no "
                    "asset e a coluna de geometria do CSV guarda só a palavra 'Polygon'. A "
                    "distância parte da MEDIANA das coordenadas de farmácia da cidade na "
                    "camada de concorrentes, que cobre o país inteiro, e usa a farmácia real "
                    "mais próxima dessa mediana — para que o centroide seja sempre um endereço "
                    "que existe, e nunca um ponto interpolado entre dois grupos distantes de "
                    "registros. É centroide aproximado: serve para ordenar praças e dar ordem "
                    "de grandeza, nunca para medir distância entre dois endereços."
                ) if ancora else "nenhuma âncora informada — a lista não considera distância",
            },
            "_leitura": (
                "lista de onde vale rodar um dossiê, não recomendação de abertura. "
                "Mercado grande sem nós pode ser oportunidade OU praça já testada e perdida — "
                "a coluna crescimento_farmarcas negativa é o segundo caso"
            ),
            "_limites": {
                "zoneamento": "só é conclusivo onde a população do Censo já está em cache; o resto pede zoneamento.py. A contagem é de GRUPOS econômicos, não de lojas",
                "granularidade": "UTC não é raio nem bairro; serve para escolher a praça, não o ponto",
                "carteira": "a base IQVIA é a carteira ATUAL da Farmarcas, com histórico retroagido",
            },
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
