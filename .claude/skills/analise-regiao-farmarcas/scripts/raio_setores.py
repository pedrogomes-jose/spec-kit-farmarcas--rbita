"""Indicadores de setor censitário dentro do raio, com rateio proporcional.

Uso:
    python raio_setores.py --lat -10.911123 --lng -37.049093 --raio 300 \
        --codigo-ibge 2800308
    python raio_setores.py ... --metodo inteiro     # soma o setor inteiro
    python raio_setores.py ... --metodo krigagem    # onde for aplicável

A geometria vem de `malha_setores.py` (acervo cartográfico do Órbita, cacheado
por município). Se o cache não existir, este script baixa antes de calcular.

MÉTODOS

`area` (padrão) — **rateio proporcional pela fração do setor dentro do raio**.
Cada setor entra pela parte dele que cai no círculo, não inteiro. É exato e
determinístico: não tem parâmetro para calibrar nem modelo para errar.

`inteiro` — soma o setor inteiro que toca o círculo. É o que o Órbita faz hoje
na versão de código conferida, e serve para comparar os dois resultados.

`krigagem` — interpolação geoestatística, **só onde é aplicável** (ver abaixo).

EXTENSIVO x INTENSIVO — a distinção que define tudo

- **Extensivo** (residentes, domicílios, potencial de consumo): é um total que
  se divide no espaço. Rateia-se multiplicando pela fração da área.
- **Intensivo** (renda média, densidade, percentuais): é uma taxa, não se
  soma nem se multiplica por fração. Entra como **média ponderada**, e o peso
  muda conforme o que a taxa descreve: renda por habitante pondera-se pela
  população dentro; percentual de domicílio, pelos domicílios dentro;
  densidade, pela área dentro.

Tratar os dois igual é o erro clássico do rateio areal, e produz renda média
que sobe ou desce só porque o raio mudou de tamanho.

PREMISSA DO RATEIO AREAL

Rateio por área assume **densidade uniforme dentro do setor**. Num setor
heterogêneo — metade quadra vazia, metade prédio — isso erra. O refinamento
usual é dasimétrico, ponderando por área construída, que o acervo não tem.
A krigagem ataca o mesmo problema por outro caminho, e só vale para o que é
intensivo.
"""

from __future__ import annotations

import argparse
import json
import sys

sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
import _bases as B  # noqa: E402
import _geo as G  # noqa: E402
import malha_setores  # noqa: E402

try:
    import krigagem as K
except ImportError:  # pragma: no cover
    K = None

# campo -> (base, natureza, peso)
#   natureza: "extensivo" rateia pela fração; "intensivo" entra em média ponderada
#   peso: o que pondera a média — "pessoas", "domicilios", "area" ou "potencial"
CAMPOS = {
    "residentes": ("densidade_demografica_do_setor_habkm", "Residentes", "extensivo", None),
    "domicilios": ("densidade_demografica_do_setor_habkm", "Domicilios", "extensivo", None),
    "densidade_hab_km2": ("densidade_demografica_do_setor_habkm", "densidadedemografica", "intensivo", "area"),
    "renda_por_habitante": ("renda_media", "Rendimentomediohab", "intensivo", "pessoas"),
    "renda_domiciliar": ("classe_economica_dos_domicilios", "RendimentoMedioDomicilio", "intensivo", "domicilios"),
    "moradores_por_domicilio": ("classe_economica_dos_domicilios", "Mediademor/dom", "intensivo", "domicilios"),
    "potencial_drogarias": ("potencial_de_consumo_setor_censitario", "PotencialdeconsumoDrogarias-SetorCensitario", "extensivo", None),
    "pct_medicamentos": ("potencial_de_consumo_setor_censitario", "Medicamentos(%)", "intensivo", "potencial"),
    "pct_higiene": ("potencial_de_consumo_setor_censitario", "Higieneecuidadospessoais(%)", "intensivo", "potencial"),
    "verticalizacao": ("indice_de_verticalizacao", "Verticalizacao%", "intensivo", "domicilios"),
    "agua": ("estrutura_saneamento", "Agua%", "intensivo", "domicilios"),
    "esgoto": ("estrutura_saneamento", "Esgoto%", "intensivo", "domicilios"),
    "lixo": ("estrutura_saneamento", "Lixo%", "intensivo", "domicilios"),
    "homens": ("populacao_por_genero", "Homens%", "intensivo", "pessoas"),
    "mulheres": ("populacao_por_genero", "Mulheres%", "intensivo", "pessoas"),
}

CHAVES_SETOR = ("Cod_setor", "CD_GEOCODI")


def chave(linha: dict):
    for c in CHAVES_SETOR:
        if linha.get(c):
            return str(linha[c]).strip()
    return None


def carregar_atributos(codigos: set) -> dict:
    """Valores brutos por setor, de todas as bases setoriais."""
    por_base: dict[str, dict] = {}
    lacunas = []
    bases = {}
    for _nome, (base, campo, _nat, _peso) in CAMPOS.items():
        bases.setdefault(base, set()).add(campo)
    for base, campos in bases.items():
        vistos = set()
        try:
            for linha in B.ler(base):
                k = chave(linha)
                if k in codigos:
                    vistos.add(k)
                    alvo = por_base.setdefault(k, {})
                    for campo in campos:
                        alvo[f"{base}.{campo}"] = B.num(linha.get(campo))
        except FileNotFoundError as e:
            lacunas.append({"base": base, "motivo": str(e)})
            continue
        faltam = len(codigos) - len(vistos)
        if faltam:
            lacunas.append({"base": base, "setores_sem_registro": faltam, "de": len(codigos)})
    return por_base, lacunas


def agregar(setores: list, atributos: dict, metodo: str) -> dict:
    """Agrega os campos aplicando rateio e ponderação corretos por natureza."""
    saida, detalhe = {}, {}

    # Pesos por setor, já rateados — é com eles que as taxas são ponderadas.
    pesos = {}
    for s in setores:
        cod, fr = s["codigo"], (1.0 if metodo == "inteiro" else s["fracao"])
        at = atributos.get(cod, {})
        pes = (at.get("densidade_demografica_do_setor_habkm.Residentes") or 0.0) * fr
        dom = (at.get("densidade_demografica_do_setor_habkm.Domicilios") or 0.0) * fr
        pot = (at.get("potencial_de_consumo_setor_censitario.PotencialdeconsumoDrogarias-SetorCensitario") or 0.0) * fr
        pesos[cod] = {"pessoas": pes, "domicilios": dom, "area": s["area_dentro_m2"] if metodo != "inteiro" else s["area_total_m2"], "potencial": pot}

    for nome, (base, campo, natureza, peso_de) in CAMPOS.items():
        chave_campo = f"{base}.{campo}"
        if natureza == "extensivo":
            total = 0.0
            achou = False
            for s in setores:
                v = atributos.get(s["codigo"], {}).get(chave_campo)
                if v is None:
                    continue
                achou = True
                total += v * (1.0 if metodo == "inteiro" else s["fracao"])
            saida[nome] = round(total, 2) if achou else None
        else:
            num = den = 0.0
            for s in setores:
                v = atributos.get(s["codigo"], {}).get(chave_campo)
                if v is None:
                    continue
                w = pesos[s["codigo"]].get(peso_de, 0.0)
                if w <= 0:
                    continue
                num += v * w
                den += w
            saida[nome] = round(num / den, 4) if den > 0 else None
            detalhe[nome] = f"média ponderada por {peso_de} dentro do raio"
    return saida, detalhe


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lat", type=float, required=True)
    ap.add_argument("--lng", type=float, required=True)
    ap.add_argument("--raio", type=float, default=300.0)
    ap.add_argument("--codigo-ibge", required=True)
    ap.add_argument("--metodo", default="area", choices=["area", "inteiro", "krigagem"])
    ap.add_argument("--comparar", action="store_true", help="mostra os três métodos lado a lado")
    args = ap.parse_args()

    caminho = malha_setores.construir(args.codigo_ibge, verbose=False)
    with open(caminho, encoding="utf-8") as fh:
        malha = json.load(fh)

    setores = []
    for f in malha.get("features", []):
        cod = (f.get("properties") or {}).get("CD_GEOCODI")
        if not cod:
            continue
        fr, a_total, a_dentro = G.fracao_no_circulo(f.get("geometry") or {}, args.lat, args.lng, args.raio)
        if fr <= 0:
            continue
        setores.append(
            {
                "codigo": str(cod).strip(),
                "fracao": round(fr, 6),
                "area_total_m2": round(a_total),
                "area_dentro_m2": round(a_dentro),
                "geometria": f.get("geometry"),
            }
        )

    if not setores:
        B.emitir(
            {
                "erro": "nenhum setor censitário intersecta o raio",
                "detalhe": "confira se o código IBGE corresponde ao ponto informado",
                "ponto": {"lat": args.lat, "lng": args.lng, "raio_m": args.raio},
            }
        )
        return 1

    codigos = {s["codigo"] for s in setores}
    atributos, lacunas = carregar_atributos(codigos)

    por_area, pesos_txt = agregar(setores, atributos, "area")
    por_inteiro, _ = agregar(setores, atributos, "inteiro")

    resultado = {"area": por_area, "inteiro": por_inteiro}
    krig = None
    if args.metodo == "krigagem" or args.comparar:
        if K is None:
            krig = {"aplicavel": False, "motivo": "módulo de krigagem indisponível"}
        else:
            krig = K.estimar(setores, atributos, CAMPOS, args.lat, args.lng, args.raio, por_area)
            if krig.get("aplicavel"):
                resultado["krigagem"] = krig["valores"]

    escolhido = args.metodo
    if escolhido == "krigagem" and not (krig or {}).get("aplicavel"):
        escolhido = "area"

    vals = resultado[escolhido]
    pot = vals.get("potencial_drogarias")
    pm, ph = vals.get("pct_medicamentos"), vals.get("pct_higiene")
    split = None
    if pot is not None and pm is not None and ph is not None and (pm + ph) > 0:
        split = {
            "medicamentos_R$": round(pot * pm / (pm + ph), 2),
            "medicamentos_pct": round(100 * pm / (pm + ph), 1),
            "higiene_beleza_nutricao_R$": round(pot * ph / (pm + ph), 2),
            "higiene_beleza_nutricao_pct": round(100 * ph / (pm + ph), 1),
        }

    area_circulo = 3.141592653589793 * args.raio**2
    cobertura = sum(s["area_dentro_m2"] for s in setores) / area_circulo

    B.emitir(
        {
            "ponto": {"lat": args.lat, "lng": args.lng, "raio_m": args.raio},
            "metodo": escolhido,
            "_metodo_leitura": {
                "area": "rateio proporcional: cada setor entra pela fração que cai dentro do raio",
                "inteiro": "soma o setor inteiro que toca o raio — é o que o produto faz hoje",
                "krigagem": "interpolação geoestatística, só para variáveis intensivas e com teste de aplicabilidade",
            }[escolhido],
            "setores_encontrados": len(setores),
            "cobertura_do_circulo": round(cobertura, 4),
            "_cobertura_leitura": "quanto da área do círculo é coberta por setor com geometria; abaixo de 1 há vazio cartográfico",
            "populacao_na_area": vals.get("residentes"),
            "domicilios": vals.get("domicilios"),
            "densidade_demografica_media_hab_km2": vals.get("densidade_hab_km2"),
            "renda_media_por_habitante_R$": vals.get("renda_por_habitante"),
            "renda_media_domiciliar_R$": vals.get("renda_domiciliar"),
            "moradores_por_domicilio": vals.get("moradores_por_domicilio"),
            "potencial_consumo_drogarias_R$": pot,
            "potencial_consumo_split": split,
            "verticalizacao_pct": vals.get("verticalizacao"),
            "saneamento": {
                "agua_pct": vals.get("agua"),
                "esgoto_pct": vals.get("esgoto"),
                "lixo_pct": vals.get("lixo"),
            },
            "populacao_por_genero": {
                "homens_pct": vals.get("homens"),
                "mulheres_pct": vals.get("mulheres"),
            },
            "ponderacao_das_taxas": pesos_txt,
            "comparacao_de_metodos": resultado if args.comparar else None,
            "krigagem": krig,
            "setores": [
                {k: v for k, v in s.items() if k != "geometria"} for s in sorted(setores, key=lambda x: -x["fracao"])
            ],
            "_aviso_metodo": (
                "rateio por área assume densidade uniforme dentro do setor; num setor "
                "heterogêneo isso erra, e o refinamento dasimétrico por área construída "
                "não está disponível no acervo"
            ),
            "lacunas": lacunas,
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
