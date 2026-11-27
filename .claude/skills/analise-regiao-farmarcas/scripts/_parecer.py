"""Parecer por indicador: o número está bom ou ruim, contra o seu referente?

Decisão do PM em 2026-11-27. O analista recebia o número com o percentil ao
lado e precisava saber sozinho se "percentil 28" era bom ou ruim — e a resposta
depende do indicador: percentil 28 de renda é ruim; percentil 28 de um
indicador em que mais é pior seria bom. Esse é exatamente o conhecimento prévio
que o produto existe para tirar do analista (CLAUDE.md, "o que é um bom ou mau
resultado para cada uma").

O que este módulo É:
- uma tabela de DIREÇÃO por indicador (mais é melhor, menos é melhor, ou
  ambíguo), cada linha com o motivo escrito e a referência da casa que a
  sustenta;
- uma função que transforma (indicador, posição contra o referente) em rótulo
  + uma linha de porquê, de forma determinística.

O que ele NÃO é, e não pode virar:
- score, nota ou recomendação. O parecer é POR NÚMERO e nunca se soma,
  nunca se conta ("três indicadores bons"), nunca se tira média, e nunca ordena
  praças. A régua de viabilidade 0–20 continua com o produto;
- faixa absoluta ("renda boa é acima de R$ X"). O referente é sempre a
  distribuição (percentil nacional) ou um recorte da região (município, UF,
  anel maior) — nunca um valor fixo escrito aqui;
- palpite. Onde a casa não tem direção defensável, o rótulo é "Ambíguo"; onde
  não há referente coerente, "Sem referência". Os dois são respostas válidas.

Cortes por percentil — os tercis da distribuição nacional:
    percentil <= 33  -> terço de baixo
    34..66           -> terço do meio  -> "Na média"
    percentil >= 67  -> terço de cima
O corte é POSIÇÃO NA DISTRIBUIÇÃO, não valor absoluto, e vale igual para todo
indicador; o que muda de um para outro é a direção. Mudar os tercis é mudar as
duas constantes abaixo, num lugar só, e o conferidor acompanha sozinho.
"""
from __future__ import annotations

TERCO_BAIXO = 33  # percentil <= este -> terço de baixo da distribuição nacional
TERCO_ALTO = 67   # percentil >= este -> terço de cima

BOM = "Bom"
MEDIO = "Na média"
RUIM = "Ruim"
AMBIGUO = "Ambíguo"
SEM_REFERENCIA = "Sem referência"

ROTULOS = (BOM, MEDIO, RUIM, AMBIGUO, SEM_REFERENCIA)

# Classe CSS de cada rótulo — a cor é de leitura, não de nota: não há escala
# contínua, não há soma, e "Ambíguo" tem cor própria para não ser lido como
# "neutro bom".
CLASSE = {
    BOM: "p-bom",
    MEDIO: "p-medio",
    RUIM: "p-ruim",
    AMBIGUO: "p-ambiguo",
    SEM_REFERENCIA: "p-semref",
}

# chave -> (nome legível, direção, motivo da direção)
# direção: "maior" (mais é melhor), "menor" (menos é melhor), "ambiguo", "sem_referencia",
# ou um dict {modelo: direção} quando a direção depende do modelo da bandeira.
DIRECAO = {
    # --- poder de compra
    "renda_domiciliar_per_capita": (
        "renda domiciliar per capita", "maior",
        "renda abaixo da mediana é Fragilidade nas lentes da casa"),
    "renda_por_habitante": (
        "renda por habitante", "maior",
        "renda abaixo da mediana é Fragilidade nas lentes da casa"),
    "renda_domiciliar": (
        "renda domiciliar", "maior",
        "renda abaixo da mediana é Fragilidade nas lentes da casa"),
    "consumo_drogarias_por_habitante": (
        "consumo em drogarias por habitante", "maior",
        "gasto em medicamentos e potencial de consumo são Força nas lentes da casa"),
    "classes_ab": (
        "domicílios nas classes A, B1 e B2", "ambiguo",
        "concentração em D/E e concentração em A são, as duas, Fragilidade — o que serve depende da bandeira"),
    "ipc": (
        "índice de potencial de consumo (IPC) do município", "ambiguo",
        "é total, proxy de porte; porte do mercado local não prevê faturamento de loja (correlação medida −0,003)"),
    "pib_per_capita": (
        "PIB per capita", "ambiguo",
        "em cidade industrial ou de mineração mede a planta, não a carteira de quem entra na loja"),
    "potencial_de_consumo": (
        "potencial de consumo em drogarias", "ambiguo",
        "é total do raio, proxy de porte; potencial alto com concorrência instalada é disputa, não espaço"),
    # --- folga competitiva
    "habitantes_por_farmacia": (
        "habitantes por farmácia", "maior",
        "percentil alto = menos saturado; saturação é Fragilidade nas lentes — vale se a base de farmácias cobrir bem a cidade"),
    "captura": (
        "captura do potencial pelo varejo medido", "ambiguo",
        "baixa pode ser mercado não atendido ou cobertura fraca da medição; o acervo não separa os dois"),
    "credenciadas_fp": (
        "farmácias credenciadas ao Farmácia Popular", "ambiguo",
        "é perfil do parque, não folga"),
    "concorrentes_no_raio": (
        "concorrentes no raio", "sem_referencia",
        "não há distribuição de referência para contagem de farmácias num raio"),
    # --- dinamismo
    "crescimento_demografico": (
        "crescimento demográfico", "maior",
        "cidade encolhendo é Fragilidade nas lentes da casa"),
    "crescimento_mercado_municipal": (
        "crescimento do mercado farmacêutico do município", "maior",
        "mercado farmacêutico local crescendo é Força nas lentes da casa"),
    "crescimento_mercado_utc": (
        "crescimento do mercado farmacêutico da unidade territorial", "maior",
        "mercado farmacêutico local crescendo é Força nas lentes da casa"),
    "crescimento_farmarcas_vs_mercado": (
        "crescimento da rede contra o do mercado", "maior",
        "rede crescendo menos que o mercado é Fragilidade nas lentes da casa"),
    # --- centralidade
    "municipios_influenciados": (
        "municípios que a cidade influencia", "maior",
        "cidade que puxa público de fora é Força; em arranjo metropolitano a contagem é do arranjo"),
    "populacao_urbana": (
        "população urbana", "maior",
        "alta urbanização é Força nas lentes da casa"),
    "densidade_demografica": (
        "densidade demográfica", "maior",
        "mais gente por km² concentra a demanda a pé; leitura de centralidade, como a urbanização"),
    "papel_na_rede_urbana": (
        "papel na rede urbana", "sem_referencia",
        "categoria do IBGE; convertê-la em posição seria inventar escala"),
    "ifdm": (
        "desenvolvimento municipal (IFDM)", "maior",
        "desenvolvimento acima da mediana é Força nas lentes da casa"),
    # --- preço
    "preco_medio_brick": (
        "preço médio por unidade", {"popular": "menor"},
        "bandeira popular conversa melhor com preço baixo; para convencional a casa não tem direção"),
}

# Rótulo do painel de perfil por cidade -> chave da tabela. O painel já tem
# rótulos próprios (alternativas.py, INDICADORES_DO_PERFIL); o casamento é aqui,
# num lugar só, para que renomear um rótulo quebre alto e não em silêncio.
CHAVE_DO_ROTULO_DO_PAINEL = {
    "renda domiciliar per capita": "renda_domiciliar_per_capita",
    "consumo em drogarias por habitante": "consumo_drogarias_por_habitante",
    "domicílios nas classes A, B1 e B2": "classes_ab",
    "habitantes por farmácia": "habitantes_por_farmacia",
    "captura do potencial pelo varejo medido": "captura",
    "farmácias credenciadas ao Farmácia Popular": "credenciadas_fp",
    "crescimento demográfico": "crescimento_demografico",
    "crescimento do mercado farmacêutico do município": "crescimento_mercado_municipal",
    "municípios que este influencia": "municipios_influenciados",
    "população urbana": "populacao_urbana",
    "densidade demográfica": "densidade_demografica",
}

# Percentis que o dossiê de ponto recebe da camada municipal -> chave da tabela.
CHAVE_DO_PERCENTIL_MUNICIPAL = {
    "renda_media_domic_per_capita": "renda_domiciliar_per_capita",
    "ipc": "ipc",
    "pib_per_capita": "pib_per_capita",
    "ifdm": "ifdm",
}


def direcao(chave: str, modelo: str | None = None) -> str:
    linha = DIRECAO.get(chave)
    if not linha:
        return "sem_referencia"
    d = linha[1]
    if isinstance(d, dict):
        return d.get((modelo or "").strip().lower(), "ambiguo")
    return d


def _lado(percentil=None, posicao=None):
    """'alto', 'medio', 'baixo' ou None, a partir do percentil OU da posição."""
    if percentil is not None:
        try:
            p = float(percentil)
        except (TypeError, ValueError):
            return None
        if p >= TERCO_ALTO:
            return "alto"
        if p <= TERCO_BAIXO:
            return "baixo"
        return "medio"
    pos = (posicao or "").strip().lower()
    if pos in ("acima", "alto", "maior"):
        return "alto"
    if pos in ("abaixo", "baixo", "menor"):
        return "baixo"
    if pos in ("igual", "na_media", "na média", "medio", "médio"):
        return "medio"
    return None


def rotulo(chave: str, percentil=None, posicao=None, modelo: str | None = None) -> str:
    """O rótulo, determinístico: direção da tabela x lado da distribuição."""
    d = direcao(chave, modelo)
    if d == "sem_referencia":
        return SEM_REFERENCIA
    if d == "ambiguo":
        return AMBIGUO
    lado = _lado(percentil, posicao)
    if lado is None:
        return SEM_REFERENCIA
    if lado == "medio":
        return MEDIO
    favoravel = (lado == "alto") == (d == "maior")
    return BOM if favoravel else RUIM


def parecer(chave: str, percentil=None, posicao=None, modelo: str | None = None,
            referente: str = "municípios do país") -> dict:
    """Rótulo + uma linha de porquê. Nenhum número novo: só o percentil recebido."""
    linha = DIRECAO.get(chave)
    nome = linha[0] if linha else chave
    motivo = linha[2] if linha else "o indicador não está na tabela de direção da casa"
    r = rotulo(chave, percentil, posicao, modelo)
    if r == SEM_REFERENCIA:
        porque = f"sem referente coerente — {motivo}"
    elif r == AMBIGUO:
        porque = f"bom ou ruim depende do contexto — {motivo}"
    else:
        lado = _lado(percentil, posicao)
        if percentil is not None:
            onde = {"alto": "no terço de cima", "baixo": "no terço de baixo",
                    "medio": "no terço do meio"}[lado]
        else:
            onde = {"alto": "acima", "baixo": "abaixo", "medio": "em linha"}[lado]
        pos = f"{onde} (referente: {referente})"
        d = direcao(chave, modelo)
        sentido = "mais é melhor" if d == "maior" else "menos é melhor"
        porque = f"{pos}; aqui {sentido}"
        if r == RUIM:
            porque += " — possível dificuldade"
    return {"rotulo": r, "porque": porque, "motivo": motivo, "indicador": chave}
