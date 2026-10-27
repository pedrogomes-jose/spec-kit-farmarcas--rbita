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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--uf", help="limita a uma UF (recomendado)")
    ap.add_argument("--excluir-municipio", help="código IBGE a tirar da lista")
    ap.add_argument("--limite", type=int, default=12)
    ap.add_argument("--min-receita", type=float, default=5_000_000.0)
    args = ap.parse_args()

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
    for loja in B.ler_cadastro_lojas():
        if (loja.get("Status") or "").strip() not in B.STATUS_OCUPA_VAGA:
            continue
        chave = (
            B.normalizar(loja.get("Cidade - Endereço Receita", "")),
            (loja.get("Estado - Endereço Receita") or "").strip().upper(),
        )
        lojas[chave] = lojas.get(chave, 0) + 1

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
        ativas = lojas.get((B.normalizar(meta["municipio"]), meta["uf"]), 0)

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
                "potencial_consumo_drogarias_ano_R$": pot_ano,
                "potencial_consumo_drogarias_mes_R$": pot.get("mes"),
                "_potencial_e": "do MUNICÍPIO inteiro — não existe potencial por UTC nas bases",
                "preco_medio_por_unidade_R$": precos.get(meta["codigo_ibge"]),
                "populacao_censo_2022": pop,
                "teto_de_lojas": teto,
                "zoneamento": (
                    "sem população em cache — rodar zoneamento.py"
                    if pop is None
                    else ("sem teto (acima de 200 mil)" if teto is None
                          else ("COM VAGA" if ativas < teto else "SEM VAGA"))
                ),
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
            "melhores": candidatos[: args.limite],
            "_ordenacao": "mercado não atendido = receita total da UTC menos a receita Farmarcas",
            "_leitura": (
                "lista de onde vale rodar um dossiê, não recomendação de abertura. "
                "Mercado grande sem nós pode ser oportunidade OU praça já testada e perdida — "
                "a coluna crescimento_farmarcas negativa é o segundo caso"
            ),
            "_limites": {
                "zoneamento": "só é conclusivo onde a população do Censo já está em cache; o resto pede zoneamento.py",
                "granularidade": "UTC não é raio nem bairro; serve para escolher a praça, não o ponto",
                "carteira": "a base IQVIA é a carteira ATUAL da Farmarcas, com histórico retroagido",
            },
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
