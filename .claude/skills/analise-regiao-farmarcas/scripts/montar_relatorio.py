"""Monta o relatório HTML do dossiê, no layout do relatório do Órbita.

Uso:
    python montar_relatorio.py --config narrativa.json --saida relatorio.html

O script roda os scripts de dado, coleta o JSON de cada um e renderiza. A
narrativa (resumo e os itens das quatro lentes) vem do arquivo `--config`,
escrito pelo modelo. A divisão é a regra da casa:

    número  -> script          (este arquivo só formata)
    texto   -> modelo          (nunca inventa número)

Formato do `--config` (JSON):

{
  "endereco": "R. João Pessoa, 182 A - Centro, Aracaju/SE",
  "lat": -10.911123, "lng": -37.049093,
  "raio_principal": 300, "raio_amplo": 5000,
  "codigo_ibge": "2800308", "municipio": "Aracaju", "uf": "SE",
  "bandeira": "Ultra Popular", "modelo": "popular",
  "perfil": "novo", "ge": "",
  "receita_por_m2": null,
  "resumo": "frase única, factual",
  "lentes": {
    "Forças": {
      "abertura": "parágrafo que liga os itens da lente — opcional, recomendado",
      "itens": [{
        "titulo": "frase de abertura em destaque",
        "texto": "o resto do parágrafo, SEM citar a fonte",
        "fonte": "de onde o dado vem — vira referência numerada na seção Fontes"
      }]
    },
    "Fragilidades": {...}, "Oportunidades": {...}, "Dificuldades": {...}
  },
  "nao_sabe": ["item", "item"],
  "campo": ["item"]
}

O gate decide QUAL relatório sai, e o formato é HTML nos dois casos. Quando o
zoneamento devolve `impedimento`, nenhum script de mercado roda e a narrativa
troca `lentes` por quatro campos — lentes gravadas nesse caso são ignoradas,
com aviso:

{
  ...mesmos campos de identificação...,
  "resumo": "frase única: por que o ponto não passa",
  "leitura": ["parágrafo", "parágrafo"],
  "o_que_mudaria": ["o que, se fosse outro, destravaria"],
  "alertas_cadastro": ["o que no cadastro erraria o teto junto"],
  "nao_sabe": ["lacuna explicada"],
  "campo": ["o que confirmar, e o que muda conforme a resposta"]
}
"""

from __future__ import annotations

import argparse
import datetime
import html
import json
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import _bases as B  # noqa: E402

# Raio de busca das praças alternativas, em quilômetros. É PREMISSA DECLARADA,
# não medida: nenhuma fonte diz a que distância um empresário aceita operar.
# O número existe porque a alternativa era pior — sem âncora geográfica a lista
# vira função da UF e não do pedido. Medido em 2026-11-05: Pouso Alegre e
# Ipatinga, a 390 km uma da outra, recebiam listas IDÊNTICAS (15 de 15 praças),
# nenhuma a menos de 150 km de qualquer uma das duas; com o raio, a sobreposição
# entre elas caiu para zero. Quando não há praça disponível dentro do raio, o
# filtro se desliga sozinho e o relatório declara isso — ver `alternativas.py`.
RAIO_PRACAS_KM = 150.0

# Por que cada categoria traz gente para a calçada. É rótulo descritivo do
# equipamento, não afirmação sobre o ponto — nenhum número sai daqui.
POR_QUE_FLUXO = {
    "saude": "consulta e exame trazem paciente e acompanhante, muitos com receita na mão ao sair",
    "creche_escola": "entrada e saída concentram pais e responsáveis em horário fixo, todo dia útil",
    "mercado_supermercado": "compra de rotina puxa a mesma pessoa várias vezes por semana",
    "banco_loteria": "fila e pagamento prendem a pessoa no quarteirão, e o idoso é público de medicamento contínuo",
    "transporte": "ponto e terminal despejam fluxo de passagem — o passante que não mora nem trabalha aqui",
    "moradia_coletiva": "prédio concentra muita gente em pouca área, com compra de conveniência a pé",
    "moradia_individual": "casa indica bairro residencial, de compra planejada e menos passagem",
    "comercio_servicos": "densidade comercial é o que faz a rua ter movimento ao longo do dia",
    "lazer_culto": "igreja, praça e academia concentram fluxo em horários e dias específicos",
}

# ---------------------------------------------------------------------------
# O corpo do relatório não fala de ferramenta
# ---------------------------------------------------------------------------
# O relatório é lido por analista e por executivo de Expansão, não por quem
# mantém a skill. Nome de script, flag de linha de comando e nome de arquivo de
# base não dizem nada a eles — e dizem "isto é saída de robô", o que atrapalha
# justamente onde a confiança no número é o problema a resolver.
#
# A rastreabilidade NÃO cai: ela muda de endereço. O corpo cita a FONTE DE DADO
# ("camada Concorrentes 2025", "Censo 2022 do IBGE"); a ferramenta fica no
# rodapé e nos arquivos de origem.

NOMES_HUMANOS = {
    "all_expansion.analysis_data": "histórico de análises do Órbita",
    "analysis_data": "histórico de análises do Órbita",
    "mat_anterior_x_atual_utc_sem_cobertura": "base de cobertura de PDVs por UTC (IQVIA)",
    "mat_anterior_x_atual_utc_crescimento": "base de crescimento por UTC (IQVIA)",
    "mat_atual_utc_market_share": "base de market share por UTC (IQVIA)",
    "potencial_de_consumo_setor_censitario": "camada Potencial de Consumo por setor censitário",
    "densidade_demografica_do_setor_habkm": "camada Densidade Demográfica do Setor",
    "classe_economica_dos_domicilios": "camada Classe Econômica dos Domicílios",
    "indice_de_verticalizacao": "camada Índice de Verticalização",
    "clinicas_oftalmologicas": "camada Clínicas Oftalmológicas",
    "farmacias_populares_2025": "camada Farmácias Populares 2025",
    "barreiras_geograficas": "camada Barreiras Geográficas",
    "dados_farmacia_popular": "base do Farmácia Popular",
    "regic_2018_municipio": "REGIC 2018, do IBGE",
    "estrutura_saneamento": "camada Estrutura e Saneamento",
    "renda_media_municipio": "camada Renda Média por município",
    "populacao_por_genero": "camada População por Gênero",
    "potencial_de_consumo": "base municipal de Potencial de Consumo",
    "closeup_utc_varejo": "base de UTCs do varejo (CloseUp)",
    "concorrentes_2025": "camada Concorrentes 2025",
    "setor_censitario": "camada Setor Censitário",
    "qualidade_do_dado": "checagem de cadastro",
    "ranking_de_consumo": "Ranking de Consumo",
    "firjan_ifdm_geral": "índice Firjan (IFDM)",
    "iqvia_brick": "base de faturamento por brick (IQVIA)",
    "renda_media": "camada Renda Média",
    "municipios": "cadastro de municípios",
    "bairros": "camada Bairros",
    "farmacias": "camada Farmácias (cadastro da Receita)",
    "bancos": "camada Bancos",
    "do_solicitante": "vínculo com o solicitante",
}

SECOES_HUMANAS = {
    "zoneamento": "Zoneamento",
    "setores": "Setores censitários",
    "concorrência": "Concorrência",
    "mercado UTC": "Mercado por UTC",
    "contexto": "Contexto do município",
}

# O que se perde quando a base falta. Lacuna de uma linha não é acionável: o
# leitor precisa saber a consequência e o caminho, não só o nome do que faltou.
CONSEQUENCIA = {
    "mat_atual_utc_market_share": (
        "sem ela o share da rede na praça não é medido, só inferido pela receita — "
        "e share ausente não é share zero. Destrava quando a IQVIA passar a publicar a UTC"
    ),
    "mat_anterior_x_atual_utc_sem_cobertura": (
        "sem ela não se sabe se o crescimento da receita veio da mesma loja ou de abertura e "
        "fechamento de PDV. Destrava com a cobertura de PDVs da UTC na base da IQVIA"
    ),
    "farmacias": (
        "é a camada que permitiria conferir a contagem de concorrentes por uma segunda fonte; "
        "sem ela, a contagem fica sem checagem cruzada. Destrava com o CNES, que traz CNPJ e coordenada"
    ),
    "farmacias_populares_2025": (
        "sem ela não dá para localizar no raio quem já é credenciado ao Farmácia Popular. "
        "Destrava geocodificando os endereços da camada"
    ),
    "barreiras_geograficas": (
        "num ponto de passagem é o que diria se a via corta ou conecta os dois lados da área de "
        "influência. Destrava recuperando os polígonos da camada"
    ),
    "clinicas_oftalmologicas": (
        "sem ela falta um gerador de fluxo de saúde no entorno. Destrava geocodificando os endereços"
    ),
    "bancos": (
        "sem ela falta um gerador de fluxo relevante — fila de banco prende a pessoa no quarteirão. "
        "Destrava geocodificando os endereços"
    ),
    "setor_censitario": (
        "a geometria dos setores vem do asset do Órbita, não do próprio arquivo; é ela que sustenta "
        "população, renda e potencial no raio"
    ),
    "densidade_demografica": (
        "sem ela falta a densidade e a taxa de crescimento do município como referência para o raio"
    ),
    "limites_de_faixa": (
        "numa cidade logo acima ou logo abaixo de um corte, a faixa aplicada muda o teto de lojas "
        "e pode inverter o resultado do gate. Destrava a área de Expansão declarar se o limite é inclusivo"
    ),
    "premissa_status": (
        "quais status ocupam vaga é premissa adotada aqui: se loja desativada passasse a contar, "
        "o teto da cidade mudaria e o gate poderia barrar o ponto. Destrava com a regra oficial "
        "declarando que status ocupa vaga"
    ),
    "popular_x_convencional": (
        "é justamente a regra aplicável a este pedido, já que a loja pretendida é popular. "
        "Destrava a área de Expansão documentar a diferença entre os dois modelos"
    ),
    "lojas_da_cidade_sem_coordenada": (
        "sem a coordenada dessas lojas a distância mínima entre bandeiras não é verificável, "
        "e ela é a regra que poderia barrar o ponto. Destrava geocodificando os endereços do cadastro"
    ),
    "registros_sem_coordenada_em_concorrentes": (
        "registros da camada de concorrentes existem na base sem coordenada e por isso não "
        "entram em contagem por raio nenhuma — a concorrência medida aqui é um piso, não um "
        "total. Destrava com a geocodificação desses registros"
    ),
    "registros_com_coordenada_fora_do_brasil_descartados": (
        "registros da camada, em todo o país, foram descartados por coordenada fora do "
        "território brasileiro — parte deles pode ser desta região e está fora da contagem. "
        "Destrava com a correção da coordenada na origem"
    ),
    "lojas_do_cadastro_sem_coordenada_preenchida": (
        "lojas da rede — um terço do cadastro inteiro, não só desta praça — estão sem "
        "coordenada e ficam fora de qualquer checagem por distância. Destrava com a "
        "geocodificação do cadastro"
    ),
    "lojas_do_cadastro_com_coordenada_fora_do_brasil": (
        "lojas da rede, no cadastro inteiro, têm coordenada fora do território brasileiro e são "
        "descartadas para não medir distância errada. Destrava com a correção do cadastro"
    ),
    "renda_media": (
        "sem ela a renda por habitante do raio não é calculável, restando só a renda domiciliar"
    ),
}


def explicar_lacuna(secao: str, alvo: str, motivo: str) -> str:
    """Monta a lacuna como frase explicada: o que falta, por que importa, o que destrava."""
    nome = NOMES_HUMANOS.get(alvo, alvo)
    frase = f"{SECOES_HUMANAS.get(secao, secao)} — {nome}: {motivo}".rstrip(". ")
    extra = CONSEQUENCIA.get(alvo)
    return f"{frase}. {extra[0].upper()}{extra[1:]}." if extra else frase + "."


_RE_SCRIPT = re.compile(r"\s*(?:,?\s*(?:via|por|com|em|no|na)\s+)?`?\b[a-z_]+\.py\b`?")
_RE_FLAG = re.compile(r"\s*`?--[a-z0-9-]+`?")


def limpar_tecnico(texto: str) -> str:
    """Troca nome de base por nome humano e remove script e flag do texto.

    Rede de segurança: o modelo já deve escrever assim (ver a regra na SKILL),
    mas um deslize não pode vazar para o relatório que circula.
    """
    if not texto:
        return texto
    saida = str(texto)
    for tecnico, humano in sorted(NOMES_HUMANOS.items(), key=lambda kv: -len(kv[0])):
        saida = saida.replace(f"`{tecnico}`", humano).replace(tecnico, humano)
    saida = _RE_SCRIPT.sub("", saida)
    saida = _RE_FLAG.sub("", saida)
    saida = re.sub(r"\s{2,}", " ", saida)
    saida = re.sub(r"\s+([,.;])", r"\1", saida)
    # Sobras de quando a frase era construída em volta do nome do script.
    saida = re.sub(r"\s*\(\s*\)", "", saida)
    saida = re.sub(r"\s+e\s*\.", ".", saida)
    saida = re.sub(r"Fonte:\s*[,.;]\s*", "Fonte: ", saida)
    saida = re.sub(r"(?:^|\s)(?:lido|obtido|calculado)\s*\.", ".", saida)
    # Normaliza o espaco DENTRO do parentese sem criar um FORA dele: um
    # "loja(s)" colado na palavra tem de continuar colado, senao a saida do
    # relatorio vira "loja (s)".
    saida = re.sub(r"\(\s*([^)]*?)\s*\)", r"(\1)", saida)
    saida = re.sub(r"(?<=[,.;:])\(", " (", saida)
    saida = re.sub(r"\s{2,}", " ", saida)
    # Rótulo removido do formato: a ressalva tem de estar explicada na frase.
    # Se escapar, o texto dela é preservado e só o rótulo cai.
    saida = re.sub(r"(?i)\s*Muda a leitura se:\s*", " ", saida)
    saida = re.sub(r"(?i)\s*O que mudaria a leitura:\s*", " ", saida)
    # Caminho de arquivo de documentação é referência de ferramenta, não de dado.
    saida = re.sub(r"\s*(?:—|-)?\s*(?:gap|lacuna)?\s*documentad[oa]?\s*em\s+\S+\.md\b", "", saida)
    saida = re.sub(r"\s*\bdocs/\S+", "", saida)
    saida = re.sub(r"\s{2,}", " ", saida)
    return saida.strip(" ,;").strip()


CORES = {
    "Forças": ("#0f7b45", "#e8f6ee"),
    "Fragilidades": ("#b4503c", "#fdeee9"),
    "Oportunidades": ("#1a5fb4", "#e9f0fb"),
    "Dificuldades": ("#8b3a62", "#fbeaf2"),
}


def rodar(script: str, *args) -> dict:
    """Executa um script da skill e devolve o JSON. Nunca levanta: erro vira dado."""
    cmd = [sys.executable, "-X", "utf8", "-I", os.path.join(AQUI, script), *map(str, args)]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=900)
        return json.loads(r.stdout) if r.stdout.strip().startswith("{") else {
            "erro": "saída não-JSON", "detalhe": (r.stderr or r.stdout)[-400:]
        }
    except (subprocess.TimeoutExpired, ValueError, OSError) as e:
        return {"erro": f"{type(e).__name__}", "detalhe": str(e)[:300]}


def brl(v, casas=2):
    if v is None:
        return "—"
    return "R$ " + f"{v:,.{casas}f}".replace(",", "@").replace(".", ",").replace("@", ".")


def num(v, casas=0, sufixo=""):
    if v is None:
        return "—"
    return f"{v:,.{casas}f}".replace(",", "@").replace(".", ",").replace("@", ".") + sufixo


def pct(v, casas=1, fracao=True):
    """Formata percentual. `fracao=True` quando a base guarda 0–1.

    Adivinhar a unidade pelo valor ("se <= 1 multiplica por 100") erra em
    silêncio quando um percentual legítimo é menor que 1. As bases setoriais do
    dump guardam FRAÇÃO (verificado: `Verticalizacao%` e `Agua%` vão de 0 a 1,
    sem nenhum valor acima de 1); as de share da IQVIA também. Quem chama diz.
    """
    if v is None:
        return "—"
    valor = v * 100 if fracao else v
    # 0,05% arredondado para uma casa vira 0,1% — o dobro. Quando o valor é
    # pequeno, a casa decimal a mais é a diferença entre informar e enganar.
    if 0 < abs(valor) < 0.5 and casas < 2:
        casas = 2
    return num(valor, casas, "%")


def e(s) -> str:
    return html.escape(str(s if s is not None else "—"))


# Tags de ENFASE que a narrativa pode usar. Formatacao, nunca estrutura: sem
# atributo, sem link, sem script.
_TAGS_RICAS = ("b", "i", "em", "strong")


def rico(s) -> str:
    """Escapa o texto e reabre APENAS as tags de enfase da narrativa.

    Os dois caminhos do relatorio divergiam aqui, e o defeito era silencioso.
    O dossie completo escapava tudo: `<b>` escrito na narrativa chegava ao
    analista como "<b>" IMPRESSO no meio da frase, e justamente na secao de
    lacunas, que e a que mais precisa ser lida. O relatorio de impedimento nao
    escapava nada: o mesmo texto saia em negrito, e de quebra qualquer string
    vinda de script entrava crua no HTML. Quem escrevia a narrativa acertava
    num caminho e errava no outro, sem nenhum aviso.

    Agora os dois passam pela mesma regua, e ela e a estrita: escapa-se tudo e
    reabre-se so a enfase. O caminho completo ganha o negrito que ja devia ter
    e o de impedimento perde a passagem livre que nunca devia ter tido.
    """
    saida = html.escape(str(s if s is not None else "—"))
    for tag in _TAGS_RICAS:
        saida = saida.replace(f"&lt;{tag}&gt;", f"<{tag}>")
        saida = saida.replace(f"&lt;/{tag}&gt;", f"</{tag}>")
    return saida


# Forma de identificador de registro de base: codigo com underscore em caixa
# alta ("1806-PR_IRATI"), nome de campo em snake_case, nome de script e flag de
# linha de comando. A nota de card e corpo do relatorio: ela leva a COMPARACAO e
# a FONTE DE DADO, nunca a chave com que duas tabelas casaram. Caso real: o card
# de preco no brick saia com "UF + nome do municipio (Irati) -> 1806-PR_IRATI".
_ID_DE_BASE = re.compile(r"[A-Z0-9]+_[A-Z0-9]{2,}|\b[a-z]+_[a-z_]+\b|\.py\b|(?:^|\s)--[a-z]")


def card(rotulo: str, valor: str, nota: str = "", cor: str = "#6b2fb5") -> str:
    if nota and _ID_DE_BASE.search(nota):
        print(
            f"AVISO: a nota do card '{rotulo}' carrega identificador de base, nome "
            f"de campo ou de ferramenta: \"{nota[:120]}\". A nota leva a comparacao "
            "e a fonte de dado; chave de casamento e nome de registro ficam na "
            "saida do script, e o que o leitor precisa saber vira lacuna.",
            file=sys.stderr,
        )
    extra = f'<div class="nota">{e(nota)}</div>' if nota else ""
    return (
        f'<div class="card" style="border-left-color:{cor}">'
        f'<div class="rot">{e(rotulo)}</div>'
        f'<div class="val">{valor}</div>{extra}</div>'
    )


def donut(pct_a: float, rotulo_a: str, rotulo_b: str) -> str:
    """Donut em SVG puro: sem biblioteca, imprime bem e funciona offline."""
    r, c = 70, 90
    circ = 2 * 3.141592653589793 * r
    a = circ * (pct_a / 100.0)
    return f"""<svg viewBox="0 0 180 180" width="190" height="190" role="img"
  aria-label="{e(rotulo_a)} {pct_a:.0f}%, {e(rotulo_b)} {100 - pct_a:.0f}%">
  <circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="#e8558f" stroke-width="34"/>
  <circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="#3b7ddd" stroke-width="34"
     stroke-dasharray="{a:.2f} {circ - a:.2f}" transform="rotate(-90 {c} {c})"/>
</svg>"""


def aluguel_comercial(cfg: dict) -> tuple:
    """Aluguel comercial por m². Só existe se o analista informar.

    Não há fonte pública de aluguel comercial por m² para a maioria dos
    municípios brasileiros: o índice de mercado mais usado cobre dez capitais,
    é publicado em PDF mensal e não tem interface de consulta. Para uma cidade
    fora dessas dez — a maioria das praças da rede — não existe número a buscar.
    Inventar média de portal de anúncio seria pior que deixar vazio.
    """
    v = cfg.get("aluguel_m2")
    if not v:
        return "—", (
            "não há fonte pública por município: o índice de mercado cobre dez capitais, "
            "em PDF mensal. Informe o valor pesquisado para habilitar o custo de ocupação"
        )
    return f"{brl(v)}/m²", f"informado pelo analista · referência: {e(cfg.get('aluguel_fonte') or 'não declarada')}"


def custo_de_ocupacao(cfg: dict, potencial, m2_texto: str) -> tuple:
    """Aluguel mensal estimado = área estimada × aluguel por m²."""
    aluguel = cfg.get("aluguel_m2")
    rpm = cfg.get("receita_por_m2")
    if not aluguel or not rpm or not potencial:
        return "—", "depende da área de venda estimada e do aluguel por m², ambos informados pelo analista"
    m2 = potencial / rpm
    mensal = m2 * aluguel
    return brl(mensal), f"{num(m2, 0)} m² × {brl(aluguel)}/m² — mensal"


def area_de_venda(potencial, receita_por_m2):
    """Área de venda estimada — só com régua de R$/m² informada.

    Não há benchmark de faturamento por m² nem no acervo interno nem em fonte
    pública localizada. Sem régua, o campo fica vazio, como no relatório do
    produto — inventar o número seria pior que deixar em branco.
    """
    if not receita_por_m2 or not potencial:
        return "—", "depende de uma referência de faturamento por m² que o analista informe; sem ela não há estimativa honesta"
    m2 = potencial / receita_por_m2
    return f"{num(m2, 0)} m²", f"potencial ÷ {brl(receita_por_m2)}/m² informado"


def bloco_implantacao(implant: dict) -> str:
    """Onde o ponto está na quadra — e só quando o dado sustenta a afirmação.

    Esquina e meio de quadra mudam a leitura de um ponto de rua mais que quase
    qualquer indicador de área: a esquina tem duas faces de exposição e recebe
    quem vem de duas vias. Mas isso só vale dito com certeza. Sem classificação,
    o bloco inteiro não é emitido — nem como lacuna. Dizer "não foi possível
    determinar se é esquina" não muda decisão nenhuma e gasta a atenção que as
    lacunas de verdade precisam.
    """
    classe = (implant or {}).get("classificacao")
    if not classe:
        return ""
    via = implant.get("via_do_ponto")
    porte = implant.get("porte_da_via")
    d = implant.get("distancia_ao_cruzamento_m")
    if classe == "esquina":
        vias = implant.get("vias_do_cruzamento") or []
        onde = " e ".join(e(v) for v in vias) if len(vias) >= 2 else e(via)
        texto = (
            f"<b>O ponto está em esquina</b>, no encontro de {onde}"
            + (f", a {num(d, 1)} m do cruzamento" if d is not None else "")
            + ". Esquina tem duas faces de exposição e recebe quem circula pelas duas vias — "
            "é a implantação que mais separa um ponto de rua de outro na mesma quadra."
        )
    else:
        texto = (
            f"<b>O ponto está em meio de quadra</b>"
            + (f", sobre {e(via)}" if via else "")
            + (f", a {num(d, 1)} m do cruzamento nomeado mais próximo" if d is not None else "")
            + ". Meio de quadra tem uma única face de exposição, e depende do fluxo que "
            "a própria via carrega em vez de somar o de duas."
        )
    if porte:
        texto += f" A via é classificada como {e(porte)}."
    return f'<p class="explica">{texto}</p>'


def bloco_influencia(ctx: dict) -> str:
    """As cidades que têm este município como polo, nomeadas e com população.

    A contagem sozinha ("atende 3 cidades do entorno") não informa tamanho de
    mercado. Nomear e somar a população transforma a frase num número que o
    analista usa: é o público que não mora no raio e que nenhum indicador de
    área deste relatório captura.
    """
    bloco = (ctx or {}).get("cidades_influenciadas") or {}
    cidades = bloco.get("cidades") or []
    if not cidades:
        return ""
    linhas = "".join(
        f"<tr><td>{e(c.get('municipio'))}/{e(c.get('uf'))}</td>"
        f"<td>{num(c.get('populacao'))}</td>"
        f"<td>{e(c.get('classificacao_regic'))}</td></tr>"
        for c in cidades
    )
    soma = bloco.get("populacao_somada")
    sem_pop = bloco.get("sem_populacao_na_base") or 0
    nota_soma = (
        f"<p class='vazio'>Somadas, essas cidades têm <b>{num(soma)} habitantes</b>"
        + (f", com {num(sem_pop)} sem população na base e fora da soma" if sem_pop else "")
        + ". É público que não mora no raio e que nenhum indicador de área deste "
        "relatório conta.</p>"
        if soma
        else ""
    )
    diverg = bloco.get("_divergencia")
    nota_div = f"<p class='vazio'>{e(diverg)}</p>" if diverg else ""
    return f"""<h3>Cidades que têm este município como polo</h3>
  <p class="explica"><b>Por que isto entra.</b> Toda medida de população, renda e
  potencial deste relatório conta apenas quem <b>mora</b> dentro do raio. Quando a
  cidade é polo de outras, parte do movimento do comércio vem de fora e não aparece
  em nenhum desses números. A lista abaixo dimensiona esse público: é a relação de
  polo invertida — municípios que registram este como seu centro.</p>
  <table><thead><tr><th>Município</th><th>População</th><th>Papel na rede urbana</th></tr></thead>
  <tbody>{linhas}</tbody></table>
  {nota_soma}{nota_div}"""


# A leitura da região é um QUADRANTE, e a ordem é fixa porque numa matriz quem
# informa é a POSIÇÃO, não o rótulo. Em cima, o que o ponto já é hoje; embaixo,
# o que ele pode vir a ser. À esquerda, o que joga a favor; à direita, o que
# joga contra. Lido assim, cada linha é um par que se contrapõe.
ORDEM_SWOT = ("Forças", "Fragilidades", "Oportunidades", "Dificuldades")


def bloco_lentes(lentes: dict, fontes: list) -> str:
    """Rende as quatro lentes como QUADRANTE SWOT de texto corrido.

    Texto corrido e não bullet: bullet empilha afirmações soltas; parágrafo
    obriga a ligar uma à outra, que é como o analista lê. Cada item vira um
    parágrafo com a frase de abertura em destaque, e a lente pode trazer uma
    `abertura` opcional antes deles.

    Quadrante e não pilha: empilhadas em coluna, as quatro lentes viravam
    quatro blocos de texto em sequência, e o par de cada linha — que é o
    contraste que o leitor precisa fazer — ficava separado por uma tela de
    rolagem. Em matriz, Forças e Fragilidades se leem lado a lado, e
    Oportunidades e Dificuldades também.

    Quadrante vazio continua desenhado, com a linha de ausência no lugar do
    texto: buraco na matriz é informação, e tirar a caixa desalinharia as
    outras três.
    """
    extras = [n for n in lentes if n not in ORDEM_SWOT]
    celulas = []
    for nome in list(ORDEM_SWOT) + extras:
        conteudo = lentes.get(nome)
        if isinstance(conteudo, dict):
            abertura, itens = conteudo.get("abertura", ""), conteudo.get("itens", [])
        else:
            abertura, itens = "", (conteudo or [])
        if not itens and not abertura and nome in extras:
            continue
        cor, fundo = CORES.get(nome, ("#444", "#f4f4f4"))
        corpo = f'<p class="abertura">{rico(limpar_tecnico(abertura))}</p>' if abertura else ""
        for i in itens:
            # A fonte sai do meio da frase e vira referência numerada, resolvida
            # na seção de Fontes no fim. O texto fica legível; a rastreabilidade
            # continua item a item.
            fonte = limpar_tecnico(i.get("fonte") or "")
            marca = ""
            if fonte:
                fontes.append((nome, limpar_tecnico(i.get("titulo", "")), fonte))
                marca = f'<sup class="ref">{len(fontes)}</sup>'
            corpo += (
                f'<p><b>{rico(limpar_tecnico(i.get("titulo")))}</b> '
                f'{rico(limpar_tecnico(i.get("texto")))}{marca}</p>'
            )
        if not corpo:
            corpo = '<p class="vazio">Nada a registrar nesta lente.</p>'
        celulas.append(
            f'<div class="lente" style="border-color:{cor};background:{fundo}">'
            f'<div class="lente-tit" style="color:{cor}">{e(nome)}</div>'
            f"{corpo}</div>"
        )
    if not celulas:
        return ""
    # Rótulo de eixo só com a matriz montada: em uma coluna (tela estreita) ele
    # some pelo CSS, porque "A favor | Contra" deixa de descrever a posição.
    eixo = '<div class="swot-eixo"><span>A favor</span><span>Contra</span></div>'
    return f'{eixo}<div class="swot">{"".join(celulas)}</div>'


def bloco_fontes(fontes: list, dump: str, origem_coord: str = "") -> str:
    """Seção única no fim: todas as fontes citadas, numeradas, mais a procedência.

    Fonte no meio do parágrafo interrompe a leitura e some do radar de quem
    quer conferir. Consolidada no fim, ela serve às duas coisas: o texto corre,
    e quem auditar acha tudo num lugar só.
    """
    linhas = "".join(
        f'<tr><td class="n">{i}</td><td>{e(lente)}</td><td>{e(titulo)}</td><td>{e(fonte)}</td></tr>'
        for i, (lente, titulo, fonte) in enumerate(fontes, start=1)
    )
    tabela = (
        '<table class="fontes"><thead><tr><th>#</th><th>Lente</th><th>Afirmação</th>'
        f"<th>Fonte do dado</th></tr></thead><tbody>{linhas}</tbody></table>"
        if fontes
        else "<p class='vazio'>Nenhuma fonte declarada nos itens.</p>"
    )
    origem_coord = origem_coord or (
        "origem não declarada nesta geração — toda distância deste relatório é medida "
        "a partir dela"
    )
    return f"""<section>
  <h2><span class="ic">§</span> Fontes</h2>
  {tabela}
  <h3>Procedência geral</h3>
  <ul class="proc">
    <li><b>Coordenada do ponto</b> — {origem_coord}</li>
    <li><b>Acervo de camadas do Órbita</b> — extração de {e(dump)}, sem atualização automática.</li>
    <li><b>Cadastro de lojas Farmarcas</b> — extração de {e(B.DATA_DO_CADASTRO)}, mais antiga que o acervo.</li>
    <li><b>Geometria dos setores censitários</b> — acervo cartográfico do Órbita.</li>
    <li><b>População do Censo 2022</b> — API pública do IBGE, extração de {e(data_censo())}.</li>
    <li><b>Faturamento, unidades e preço por brick e por UTC</b> — IQVIA e CloseUp.</li>
    <li><b>Receita e número de pontos de venda por canal e por estado</b> — IQVIA, receita acumulada de 12 meses (MAT 2026) sobre contagem de pontos de venda do ano corrente (YTD 2026).</li>
    <li><b>Geradores de fluxo no entorno</b> — OpenStreetMap.</li>
    <li><b>Regras de zoneamento e de expansão</b> — documentação de processo da Farmarcas.</li>
  </ul>
  <p class="vazio">Este dossiê não pontua o ponto: não há score, nota nem status de
  recomendação. A régua de viabilidade pertence ao produto.</p>
</section>"""


def tabela_faixas(faixas: list) -> str:
    if not faixas:
        return "<p class='vazio'>Sem faixas — nenhum concorrente do raio tem faturamento cadastrado.</p>"
    linhas = []
    for f in faixas:
        mx = brl(f["maxima_R$"]) if f["maxima_R$"] else "Acima"
        mn = brl(f["minima_R$"]) if f["minima_R$"] else "Abaixo"
        destaque = ' class="tem"' if f["lojas"] else ""
        linhas.append(
            f"<tr{destaque}><td>{mx}</td><td>{mn}</td>"
            f'<td><span class="faixa f{f["classificacao"]}">{f["classificacao"]}</span></td>'
            f'<td>{f["lojas"] or "—"}</td></tr>'
        )
    return (
        "<table><thead><tr><th>Máxima</th><th>Mínima</th>"
        "<th>Classificação</th><th>Lojas no raio</th></tr></thead>"
        f"<tbody>{''.join(linhas)}</tbody></table>"
    )


# A base grava o nome do canal em caixa alta e sem acento. Title-case sozinho
# estraga sigla ("Abrafarma") e não devolve o acento que o leitor espera.
NOME_DO_CANAL = {
    "ABRAFARMA": "ABRAFARMA",
    "FEBRAFAR": "FEBRAFAR",
    "ASSOCIACOES + FRANQUIAS": "Associações e franquias",
    "INDEPENDENTES": "Independentes",
    "OUTRAS REDES CORPORATIVAS": "Outras redes corporativas",
    "GRUPO FARMARCAS": "Grupo Farmarcas",
}


def tabela_canais(canal1: dict, canal2: dict, r1, r2) -> str:
    """Régua medida por canal na UF, com as lojas que cada raio encontrou."""
    bench = (canal1 or {}).get("benchmark_por_canal") or {}
    if not bench:
        return "<p class='vazio'>Régua de canal indisponível — ver lacunas.</p>"
    no1 = {k: v["lojas"] for k, v in ((canal1 or {}).get("por_canal") or {}).items()}
    no2 = {k: v["lojas"] for k, v in ((canal2 or {}).get("por_canal") or {}).items()}
    linhas = []
    for canal, dados in sorted(bench.items(), key=lambda kv: -kv[1]["valor_mes_R$"]):
        destaque = ' class="tem"' if no1.get(canal) or no2.get(canal) else ""
        fora = "" if dados["abrangencia"] != "Brasil" else " *"
        linhas.append(
            f"<tr{destaque}><td>{e(NOME_DO_CANAL.get(canal, canal.title()))}{fora}</td>"
            f'<td>{brl(dados["valor_mes_R$"])}</td>'
            f'<td>{no1.get(canal) or "—"}</td><td>{no2.get(canal) or "—"}</td></tr>'
        )
    nota = ""
    if any(v["abrangencia"] == "Brasil" for v in bench.values()):
        nota = ("<p class='explica'>* canal sem loja registrada neste estado — "
                "a referência cai para a média nacional.</p>")
    return (
        "<table><thead><tr><th>Canal</th><th>Por loja/mês</th>"
        f"<th>Lojas em {num(r1)} m</th><th>Lojas em {num(r2)} m</th></tr></thead>"
        f"<tbody>{''.join(linhas)}</tbody></table>{nota}"
    )


def avisar_referencia_cruzada(cfg: dict) -> list:
    """Alerta quando a narrativa menciona município de outro dossiê já feito.

    Um dossiê é lido isolado e dois casos não formam distribuição, então
    comparar com outra análise é anedota, não referência. Isto AVISA, não
    corrige: município vizinho legítimo também aparece no texto, e só quem
    escreveu sabe distinguir — mas ninguém deixa passar o que foi apontado.
    """
    pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "outputs", "dossies")
    pasta = os.path.normpath(pasta)
    if not os.path.isdir(pasta):
        return []
    atual = B.normalizar(cfg.get("municipio", ""))
    outros = set()
    for nome in os.listdir(pasta):
        if not nome.endswith(".json"):
            continue
        try:
            with open(os.path.join(pasta, nome), encoding="utf-8") as fh:
                mun = (json.load(fh) or {}).get("municipio", "")
        except (OSError, ValueError):
            continue
        if mun and B.normalizar(mun) != atual:
            outros.add(mun)

    texto = json.dumps(cfg, ensure_ascii=False)
    sem_acento = B.normalizar(texto)
    achados = [m for m in sorted(outros) if B.normalizar(m) in sem_acento]
    return achados


def rodar_gate(cfg: dict) -> dict:
    """Roda o gate de zoneamento. E ele que decide qual relatorio sera montado."""
    return rodar(
        "zoneamento.py", "--lat", cfg["lat"], "--lng", cfg["lng"],
        "--municipio", cfg["municipio"], "--uf", cfg["uf"],
        "--codigo-ibge", cfg["codigo_ibge"], "--bandeira", cfg.get("bandeira", ""),
        "--modelo", cfg.get("modelo", ""), "--perfil", cfg.get("perfil", ""),
        *(("--ge", cfg["ge"]) if cfg.get("ge") else ()),
    )


def construir(cfg: dict, zon: dict | None = None) -> str:
    lat, lng = cfg["lat"], cfg["lng"]
    cod, uf, mun = cfg["codigo_ibge"], cfg["uf"], cfg["municipio"]
    r1, r2 = cfg.get("raio_principal", 300), cfg.get("raio_amplo", 5000)

    # O gate ja pode ter sido rodado por main(), que precisa do veredito para
    # escolher o relatorio. Rodar de novo custaria tempo e abriria a porta para
    # dois vereditos diferentes no mesmo documento.
    zon = zon if zon is not None else rodar_gate(cfg)
    setores = rodar("raio_setores.py", "--lat", lat, "--lng", lng, "--raio", r1,
                    "--codigo-ibge", cod, "--metodo", cfg.get("metodo_setores", "area"))
    comp1 = rodar("raio_concorrencia.py", "--lat", lat, "--lng", lng, "--raio", r1,
                  "--listar", 0, "--municipio", mun, "--uf", uf)
    comp2 = rodar("raio_concorrencia.py", "--lat", lat, "--lng", lng, "--raio", r2,
                  "--listar", 0, "--municipio", mun, "--uf", uf)
    utc = rodar("mercado_utc.py", "--codigo-ibge", cod)
    brick = rodar("mercado_brick.py", "--uf", uf, "--codigo-ibge", cod, "--lat", lat, "--lng", lng)
    # Caminhada, não o raio de estudo: 300 m é curto demais para geradores de
    # fluxo, então o piso é 500 m. O raio usado é outro e o relatório diz qual —
    # misturar 59 moradores de 300 m com oito pontos de ônibus de 500 m sem
    # avisar faz o leitor somar dois recortes diferentes.
    raio_pois = max(r1, 500)
    pois = rodar("pois_no_raio.py", "--lat", lat, "--lng", lng, "--raio", raio_pois, "--listar", 6)
    implant = rodar("implantacao.py", "--lat", lat, "--lng", lng)
    ctx = rodar("contexto_municipio.py", "--municipio", mun, "--uf", uf)
    # Mesma ancoragem geografica do relatorio de impedimento: sem ela "Onde mais
    # olhar" devolvia a capital da UF em todo dossie, qualquer que fosse o ponto.
    alt = rodar("alternativas.py", "--uf", uf, "--excluir-municipio", cod, "--limite", 6,
                "--perto-de", f"{lat},{lng}", "--raio-km", RAIO_PRACAS_KM,
                *(("--modelo", cfg["modelo"]) if cfg.get("modelo") else ()))
    vlj = rodar("venda_por_loja.py", "--uf", uf,
                *(("--bandeira", cfg["bandeira"]) if cfg.get("bandeira") else ()),
                *(("--modelo", cfg["modelo"]) if cfg.get("modelo") else ()))

    # Sem brick casado nao ha card: um card de destaque que so diz '—' gasta
    # a atencao do leitor e ainda poe o preco da UF ao lado, convidando a ler
    # o agregado estadual como se fosse o preco deste ponto.
    _brick_do_ponto = (brick.get("brick") or {}).get("preco_medio_por_unidade_R$")
    # A nota do card carrega a COMPARACAO e a FONTE, e nada mais. O criterio de
    # casamento vinha junto e trazia o codigo cru do brick ("UF + nome do
    # municipio (Irati) -> 1806-PR_IRATI"): identificador de base no corpo do
    # relatorio, que nao diz nada a analista nem a executivo e ainda sinaliza
    # saida de robo bem onde o problema e confianca no numero. O criterio nao
    # sumiu do dossie — ele e lacuna obrigatoria, escrita em linguagem de
    # negocio, porque o que o leitor precisa saber e que NAO se sabe em qual
    # brick o ponto cai, e nao por qual chave as duas tabelas casaram.
    card_brick = (
        card("Preço médio no brick", brl(_brick_do_ponto),
             f"UF: {brl((brick.get('uf_inteira') or {}).get('preco_medio_por_unidade_R$'))} · "
             "receita a preço de consumidor ÷ unidades vendidas · fonte: base de "
             "faturamento por brick da IQVIA", "#6b2fb5")
        if _brick_do_ponto is not None
        else ""
    )
    micro = comp1.get("microterritorio", {})
    venda_cid = (comp2.get("venda_por_loja") or {}).get("na_cidade") or {}
    recortes = {r.get("recorte", ""): r for r in (vlj.get("recortes") or [])}
    def _mes(chave_parcial):
        for k, r in recortes.items():
            if chave_parcial.lower() in k.lower() and r.get("receita_mes_R$"):
                return r["receita_mes_R$"]
        return None
    uf_sigla = (cfg.get("uf") or "").upper()
    medido = _mes(f"na UF {uf_sigla}") or _mes(f"UF {uf_sigla}")
    # "rede inteira" casa tanto com o recorte de todas as bandeiras quanto com o
    # da bandeira pretendida. O card fala da bandeira, então ela vem primeiro.
    medido_nac = (
        _mes(f"{cfg.get('bandeira', '')} na rede inteira") if cfg.get("bandeira") else None
    ) or _mes("rede inteira")
    _band = cfg.get("bandeira") or "a rede"
    medido_rotulo = f" · {e(_band)} em {e(uf_sigla)}" if medido else ""
    nota_medido = (
        f"{(medido or {}).get('lojas', 0)} loja(s) do grupo em {e(uf_sigla)}, receita apurada por "
        "instituto e cruzada por CNPJ · fonte: base de faturamento da IQVIA e cadastro de lojas"
    )
    nota_nacional = (
        f"mediana de {(medido_nac or {}).get('lojas', 0)} loja(s) · mesma fonte, recorte nacional"
    )
    # O campo de faturamento da camada assume 8 valores em toda a base, um por
    # faixa — sete são o ponto médio exato da faixa. Não é estimativa por loja: é
    # o rótulo da classe. O card precisa dizer isso, senão o leitor compara dois
    # rótulos de faixa e acha que mediu a distância entre duas lojas.
    nota_venda = (
        f"faixa, entre as {venda_cid.get('lojas_com_faturamento', 0)} lojas do município "
        "classificadas · o campo tem 8 valores, um por faixa — não mede a loja"
    )
    canal1 = comp1.get("mercado_por_canal") or {}
    canal2 = comp2.get("mercado_por_canal") or {}
    def _nota_canal(bloco, raio):
        n_sem = bloco.get("lojas_sem_canal")
        resto = (f" · {n_sem} sem canal reconhecido, fora da soma"
                 if n_sem else "")
        return (f"{bloco.get('lojas_com_canal', 0)} de {bloco.get('lojas', 0)} lojas em "
                f"{num(raio)} m{resto} · fonte: receita e PDVs por canal da IQVIA")
    nota_canal1 = _nota_canal(canal1, r1)
    nota_canal2 = _nota_canal(canal2, r2)
    # Zero aqui pode significar "nenhuma loja nossa" OU "loja nossa sem coordenada".
    # Sem a nota, o card contradiz a lente que explica a lacuna.
    sem_coord_cidade = (zon.get("lacunas") or {}).get("lojas_da_cidade_sem_coordenada") or 0
    nota_lojas = "pelo cadastro de lojas (CNPJ + coordenada)"
    if sem_coord_cidade:
        nota_lojas += f" — atenção: {sem_coord_cidade} loja(s) do município estão sem coordenada e não entram nesta conta"
    split = setores.get("potencial_consumo_split") or {}
    pot = setores.get("potencial_consumo_drogarias_R$")
    av, av_nota = area_de_venda(pot, cfg.get("receita_por_m2"))
    alu, alu_nota = aluguel_comercial(cfg)
    occ, occ_nota = custo_de_ocupacao(cfg, pot, av)

    veredito = zon.get("veredito", "—")
    cor_gate = {"liberado": "#0f7b45", "alerta": "#b07d00", "impedimento": "#b4503c"}.get(veredito, "#444")
    # O rotulo do gate sozinho nao informa: num alerta de densidade o que o
    # analista precisa ler e POR QUE alertou. O gate ja devolve o constatado.
    _motivos = [i.get("constatado") for i in (zon.get("impedimentos") or [])] or [
        a.get("constatado") for a in (zon.get("alertas") or [])
    ]
    _motivos = [m for m in _motivos if m]
    motivo_do_gate = (
        f'<div class="nota" style="margin-top:6px;color:{cor_gate}">{e(limpar_tecnico(_motivos[0]))}</div>'
        if _motivos
        else ""
    )

    # --- cabeçalho e gate
    dump = B.DATA_DO_DUMP
    fontes: list = []
    partes = [f"""<header>
  <div class="marca">Órbita · Dossiê de Região</div>
  <div class="sub">Leitura de região para análise de ponto — <b>sem score</b> ·
    dump de {dump} · cadastro de lojas de {B.DATA_DO_CADASTRO}</div>
</header>
<div class="faixa-end">{e(cfg['endereco'])}</div>
<section class="topo">
  <div class="gate" style="border-color:{cor_gate}">
    <div class="rot">Zoneamento</div>
    <div class="val" style="color:{cor_gate}">{e(veredito.capitalize())}</div>
    <div class="nota">{e(zon.get('faixa_aplicada'))}</div>
    {motivo_do_gate}
  </div>
  <div class="resumo">
    <div class="rot">Em uma linha</div>
    <p>{rico(limpar_tecnico(cfg.get('resumo')))}</p>
    <div class="meta">Solicitante: <b>{e(PERFIL_HUMANO.get(cfg.get("perfil"), cfg.get("perfil") or "não informado"))}</b> ·
      Bandeira: <b>{e(cfg.get('bandeira') or '—')}</b> ({e(cfg.get('modelo') or '—')}) ·
      População do município (Censo 2022): <b>{num(zon.get('populacao_censo_2022'))}</b></div>
  </div>
</section>"""]

    # --- leitura (4 lentes)
    partes.append(f"""<section>
  <h2><span class="ic">◆</span> Leitura da região</h2>
  {bloco_lentes(cfg.get('lentes', {}), fontes)}
</section>""")

    # --- detalhes da região
    partes.append(f"""<section>
  <h2><span class="ic">◉</span> Detalhes da região analisada</h2>
  <div class="cards">
    {card("População na área", num(setores.get("populacao_na_area")) + " habitantes", f"{setores.get('setores_encontrados','—')} setores censitários no raio")}
    {card("Raio de estudo", f"{num(r1)} m", f"comparado também a {num(r2)} m")}
    {card("Domicílios", num(setores.get("domicilios")), f"{num(setores.get('moradores_por_domicilio'),2)} moradores por domicílio")}
    {card("Potencial de consumo", brl(pot), "drogarias, rateado pela fração de cada setor no raio")}
    {card("Método de rateio", e({"area": "proporcional por área", "inteiro": "setor inteiro", "krigagem": "krigagem onde aplicável"}.get(setores.get("metodo"), "—")), f"cobertura do círculo: {pct(setores.get('cobertura_do_circulo'))} · {setores.get('setores_encontrados','—')} setores", "#6b2fb5")}
  </div>
</section>""")

    # --- contexto macro
    partes.append(f"""<section>
  <h2><span class="ic">↗</span> Contexto macroeconômico</h2>
  <p class="explica"><b>Como ler a renda.</b> São valores <b>mensais aproximados</b>,
  média dos setores censitários <b>ponderada pela população e pelos domicílios que
  cada setor tem dentro do raio</b> — setor que só encosta na borda pesa pouco — não a renda de quem compra na
  loja, e sim a de quem <b>mora</b> ali. Renda por habitante divide o rendimento do
  domicílio por todos os moradores, inclusive quem não tem renda; por isso fica bem
  abaixo da renda domiciliar. Num ponto de passagem, as duas descrevem a vizinhança
  residencial, não a clientela — que pode ser outra.</p>
  <div class="cards">
    {card("Densidade demográfica", num(setores.get("densidade_demografica_media_hab_km2"), 0, " hab/km²"), "média dos setores do raio", "#1a5fb4")}
    {card("Renda média por habitante", brl(setores.get("renda_media_por_habitante_R$")), "setores do raio", "#0f7b45")}
    {card("Renda média domiciliar", brl(setores.get("renda_media_domiciliar_R$")), "setores do raio", "#0f7b45")}
    {card("Verticalização", pct(setores.get("verticalizacao_pct")), "domicílios em apartamento — casas x apartamentos", "#6b2fb5")}
    {card("Área de venda estimada", av, av_nota, "#b07d00")}
    {card("Aluguel comercial", alu, alu_nota, "#b07d00")}
    {card("Custo de ocupação estimado", occ, occ_nota, "#b07d00")}
  </div>
  {bloco_influencia(ctx)}
</section>""")

    # --- microterritório
    partes.append(f"""<section>
  <h2><span class="ic">$</span> Microterritório e concorrência</h2>
  <div class="cards">
    {card("Vendas totais na cidade", brl(micro.get("vendas_totais_na_regiao_R$")), f'{micro.get("lojas_com_faturamento_na_regiao","—")} lojas com faixa declarada no município · soma de rótulos de faixa — o campo tem 8 valores, um por faixa, e classifica a loja em vez de medir a venda', "#c0397a")}
    {card("Média da faixa por loja", brl(micro.get("media_de_faturamento_por_loja_R$")), "média mensal dos rótulos de faixa das lojas do raio — não é faturamento medido", "#1a5fb4")}
    {card("Vendas totais no raio", brl(micro.get("vendas_totais_no_raio_R$")), (lambda n: f"soma das faixas de {n} loja{'s' if (isinstance(n, int) and n != 1) else ''} classificada{'s' if (isinstance(n, int) and n != 1) else ''} · o campo tem 8 valores, um por faixa — classifica a loja, não mede a venda")(micro.get('lojas_com_faturamento_no_raio','—')), "#c0397a")}
    {card(f"Concorrentes em {num(r1)} m", num(comp1.get("concorrentes", {}).get("total")), f"{num(comp2.get('concorrentes', {}).get('total'))} em {num(r2)} m", "#b4503c")}
    {card("Lojas Farmarcas no raio", num(comp1.get("lojas_farmarcas_no_raio", {}).get("total")), nota_lojas, "#0f7b45")}
    {card_brick}
  </div>
  <h3>Quanto vende uma loja — três fontes independentes</h3>
  <p class="explica"><b>Elas não medem a mesma coisa.</b> A primeira é a
  <b>faixa de faturamento dos concorrentes</b> da praça: classifica cada loja numa de
  oito faixas, está preenchida em menos da metade dos cadastros e — importante — não
  traz valor por loja, só o rótulo da faixa. A segunda é a <b>régua medida por canal</b>: receita e
  número de pontos de venda por canal e por estado, apurados por instituto, aplicados
  ao canal em que cada concorrente está classificado. É ela que <b>dimensiona o
  mercado do raio</b>, porque cobre também as lojas de campo vazio. A terceira é a
  <b>receita medida das lojas do grupo</b>, cruzada loja a loja pelo CNPJ — responde
  quanto <b>a nossa bandeira</b> fatura numa praça assim. Em varejo farmacêutico a
  distribuição tem cauda longa, então mínimo, mediana e máximo dizem mais que média: a
  distância entre os extremos mede o quanto o resultado depende de execução e de
  ponto, não da região.</p>
  <h4>Concorrentes da praça — em que faixa de faturamento eles caem</h4>
  <p class="explica"><b>Estes três números são rótulos de faixa, não faturamento de
  loja.</b> O campo da camada de concorrentes assume <b>oito valores em toda a base</b>,
  um para cada faixa da régua que aparece no fim desta seção — sete deles são o ponto
  médio exato da faixa, e o mais baixo é o teto da faixa aberta embaixo. Então o que
  está abaixo é a faixa mais baixa ocupada, a faixa mediana e a mais alta ocupada
  entre as lojas da cidade: descrevem <b>como as lojas se distribuem entre as
  faixas</b>. A distância entre dois deles é a distância entre faixas, não entre duas
  lojas, e nenhum deles é o faturamento de nenhum estabelecimento.</p>
  <div class="cards">
    {card("Faixa mais baixa ocupada", brl((venda_cid or {}).get("minimo_R$")), nota_venda, "#1a5fb4")}
    {card("Faixa mediana", brl((venda_cid or {}).get("mediana_R$")), nota_venda, "#0f7b45")}
    {card("Faixa mais alta ocupada", brl((venda_cid or {}).get("maximo_R$")), nota_venda, "#c0397a")}
  </div>
  <h4>Mercado do raio — régua medida por canal</h4>
  <div class="cards">
    {card(f"Mercado em {num(r1)} m", brl(canal1.get("mercado_mes_R$")), nota_canal1, "#6b2fb5")}
    {card(f"Mercado em {num(r2)} m", brl(canal2.get("mercado_mes_R$")), nota_canal2, "#b4503c")}
  </div>
  {tabela_canais(canal1, canal2, r1, r2)}
  <p class="explica"><b>O que este número é e o que não é.</b> Cada valor da coluna
  por loja é o que uma loja <b>média</b> daquele canal fatura neste estado — não o
  faturamento da farmácia observada, que nenhuma base traz. A fonte não registra a
  dispersão dentro do canal: duas independentes no mesmo quarteirão podem diferir
  várias vezes entre si, e isso não aparece aqui. Some-se a isso que a receita é
  acumulada de doze meses enquanto a contagem de pontos de venda é do ano corrente,
  o que enviesa canal que abriu ou fechou muita loja no período. Serve para
  dimensionar o mercado do entorno e para situar um concorrente pelo porte da rede a
  que ele pertence; não serve para afirmar quanto um endereço vende.</p>

  <h4>Lojas do grupo — receita medida{medido_rotulo}</h4>
  <div class="cards">
    {card("Menor receita medida", brl((medido or {}).get("minimo")), nota_medido, "#1a5fb4")}
    {card("Receita mediana medida", brl((medido or {}).get("mediana")), nota_medido, "#0f7b45")}
    {card("Maior receita medida", brl((medido or {}).get("maximo")), nota_medido, "#c0397a")}
    {card("Mesma bandeira, rede inteira", brl((medido_nac or {}).get("mediana")), nota_nacional, "#6b2fb5")}
  </div>

  <h3>Venda mensal aproximada — raio de estudo</h3>
  {tabela_faixas(comp1.get("venda_mensal_por_faixa", []))}
</section>""")

    # --- potencial de consumo
    med_pct = split.get("medicamentos_pct")
    bloco_split = "<p class='vazio'>Split indisponível — ver lacunas.</p>"
    if med_pct is not None:
        bloco_split = f"""<div class="split">
    <div class="split-cards">
      {card("Potencial de consumo total", brl(pot), "médio potencial de captura")}
      {card("Medicamentos", brl(split.get("medicamentos_R$")), f"{num(med_pct,1)}% do total", "#3b7ddd")}
      {card("Higiene, Beleza & Nutrição", brl(split.get("higiene_beleza_nutricao_R$")), f"{num(split.get('higiene_beleza_nutricao_pct'),1)}% do total", "#e8558f")}
    </div>
    <div class="split-graf">
      {donut(med_pct, "Medicamentos", "Higiene, Beleza & Nutrição")}
      <div class="legenda"><span class="p azul"></span>Medicamentos
        <span class="p rosa"></span>Higiene, Beleza &amp; Nutrição</div>
    </div>
  </div>"""
    partes.append(f"""<section>
  <h2><span class="ic">◷</span> Potencial de consumo da região analisada</h2>
  <p class="explica"><b>O que este número é.</b> É quanto os moradores dos setores do
  raio <b>poderiam</b> gastar em itens de drogaria — demanda potencial estimada, não
  venda realizada. Cada setor censitário entra pela <b>fração que de fato cai dentro
  do círculo</b>, não inteiro: um setor que só encosta na borda contribui com a parte
  dele que está dentro. <b>A base não declara a periodicidade</b>: o teste de ordem de
  grandeza aponta valor anual (ver as lacunas), embora o relatório do produto rotule o
  mesmo campo como mensal. Nenhuma loja captura o potencial inteiro — ele se divide
  entre todos os concorrentes do entorno e o que vaza para fora da região.</p>
  {bloco_split}
</section>""")

    # --- geradores de fluxo
    cats = (pois.get("categorias") or {})
    if cats:
        linhas = []
        for k, v in cats.items():
            # Equipamento sem nome no OSM existe e conta; só não tem nome. Mostrar
            # "(sem nome)" polui a coluna de exemplos sem informar nada.
            exemplos = [i["nome"] for i in v["itens"] if i["nome"] and i["nome"] != "(sem nome)"]
            linhas.append(
                f"<tr><td><b>{e(k.replace('_', ' ').title())}</b><div class='nota'>"
                f"{e(POR_QUE_FLUXO.get(k, ''))}</div></td><td>{v['total']}</td>"
                f"<td>{num(v['mais_proximo_m'], 0, ' m') if v['mais_proximo_m'] is not None else '—'}</td>"
                f"<td>{e(', '.join(exemplos[:3]))}</td></tr>"
            )
        bloco_pois = (
            "<p class='explica'><b>Por que isto importa.</b> Farmácia de rua vive de "
            "quem passa, e quem passa é atraído por outra coisa — consulta, escola, "
            "banco, ônibus, compra do dia. Cada categoria abaixo é um motivo para "
            "alguém estar nesta calçada. A contagem diz que os geradores existem e a "
            "que distância; <b>não diz quanta gente passa</b>, que continua sendo o "
            "dado ausente.</p>"
            f"<table><thead><tr><th>Categoria e por que gera fluxo</th>"
            f"<th>Em {num(raio_pois)} m</th>"
            f"<th>Mais próximo</th><th>Exemplos nomeados</th></tr></thead>"
            f"<tbody>{''.join(linhas)}</tbody></table>"
            "<p class='vazio'>Equipamento sem nome no mapa entra "
            "na contagem e fica fora da coluna de exemplos. Cobertura é colaborativa: "
            "ausência aqui não é ausência no mundo.</p>"
        )
    else:
        bloco_pois = f"<p class='vazio'>Indisponível: {e(pois.get('erro', 'sem dados'))}. É lacuna, não ausência de equipamentos.</p>"
    aviso_raio_pois = (
        f"<p class='explica'><b>Recorte diferente do resto do dossiê.</b> Os números "
        f"desta seção são de um raio de {num(raio_pois)} m, e não dos {num(r1)} m do "
        "raio de estudo: 300 metros é curto demais para descrever o que atrai gente "
        "para a calçada, e uma caminhada de cinco minutos é o recorte que o pedestre "
        "de fato percorre. Não some estas contagens com a população do raio de "
        f"estudo.</p>" if raio_pois != r1 else ""
    )
    partes.append(f"""<section>
  <h2><span class="ic">⚑</span> Geradores de fluxo em {num(raio_pois)} m</h2>
  {bloco_implantacao(implant)}
  {aviso_raio_pois}
  {bloco_pois}
</section>""")

    # --- alternativas
    melhores = alt.get("melhores") or []
    if melhores:
        linhas = []
        for c in melhores:
            vaga = c.get("zoneamento", "")
            cor_vaga = "#0f7b45" if "COM VAGA" in vaga else ("#b4503c" if "SEM VAGA" in vaga else "#6c6878")
            linhas.append(
                f"<tr><td><b>{e(c['municipio'])}/{e(c['uf'])}"
                f"{' — ' + e(c['localidade']) if c.get('localidade') else ''}</b>"
                f"<div class='nota'>{e(c.get('motivo', ''))}</div></td>"
                # Escala por extenso: "R$ 133,1 milhões" não se confunde com
                # "133,1 mil" na leitura rápida de uma tabela.
                f"<td><b>{e(c.get('escala_mercado_nao_atendido'))}</b>"
                f"<div class='nota'>{brl(c['mercado_nao_atendido_R$'], 0)}</div></td>"
                f"<td>{brl(c.get('potencial_consumo_drogarias_ano_R$'), 0)}"
                f"<div class='nota'>potencial anual do município · captura de "
                f"{pct(c.get('taxa_de_captura_do_municipio'))} pelo município</div></td>"
                f"<td>{brl(c.get('preco_medio_por_unidade_R$'))}"
                f"<div class='nota'>por unidade</div></td>"
                f"<td>{pct(c['crescimento_mercado'])}</td>"
                f"<td>{c['lojas_farmarcas_no_municipio']}</td>"
                f"<td style='color:{cor_vaga};font-weight:600'>{e(vaga)}</td></tr>"
            )
        bloco_alt = (
            "<p class='explica'><b>Como ler.</b> <b>Mercado não atendido</b> é a receita "
            "medida na praça menos a receita Farmarcas — o que circula hoje sem passar "
            "por nós. Cada linha é uma <b>UTC</b>, a unidade de mercado do varejo, por "
            "isso a mesma cidade pode aparecer mais de uma vez — sempre com a localidade "
            "nomeada para distinguir uma da outra. <b>Potencial e captura são do município "
            "inteiro</b> e repetem nas linhas da mesma cidade, porque não existe potencial "
            "por UTC nas bases. <b>Captura</b> é quanto desse potencial o mercado já realiza: "
            "captura baixa com mercado grande é demanda represada; captura alta é praça "
            "madura, onde entrar significa tirar de alguém. <b>Preço médio por unidade</b> "
            "mostra se a praça é de ticket alto ou de volume — e a bandeira popular "
            "conversa melhor com preço baixo.</p>"
            "<table><thead><tr><th>Praça (município — localidade) e por que olhar</th>"
            "<th>Mercado não atendido</th><th>Potencial e captura do município</th><th>Preço médio</th><th>Cresc.</th>"
            "<th>Lojas</th><th>Zoneamento</th></tr></thead>"
            f"<tbody>{''.join(linhas)}</tbody></table>"
            "<p class='vazio'>Lista de onde vale rodar um dossiê, não recomendação de "
            "abertura. Mercado grande sem a rede dentro pode ser praça aberta ou praça já "
            "testada e perdida — crescimento Farmarcas negativo é o segundo caso. "
            "UTC não é raio nem bairro: serve para escolher a praça, não o ponto.</p>"
            + (
                f"<p class='vazio'><b>A lista está limitada a "
                f"{num((alt.get('_proximidade') or {}).get('raio_km_pedido'))} km deste "
                "endereço</b>, medidos até o centro aproximado de cada município — premissa "
                "desta análise, não regra da casa. Sem esse limite a lista devolveria as "
                "maiores praças da UF para qualquer ponto do estado.</p>"
                if (alt.get("_proximidade") or {}).get("raio_aplicado")
                else f"<p class='vazio'><b>Não há praça com mercado relevante a menos de "
                f"{num((alt.get('_proximidade') or {}).get('raio_km_pedido'))} km deste "
                "endereço</b>, então a lista volta a cobrir a UF inteira e a distância de cada "
                "uma vai declarada na própria linha.</p>"
                if (alt.get("_proximidade") or {}).get("raio_km_pedido")
                else ""
            )
            + ("<p class='vazio'>Preço médio em branco quando o nome do município aparece "
               "abreviado na base de preço e o casamento por nome falha — é ausência da "
               "chave, não do dado. Atinge sobretudo as capitais.</p>"
               if any(c.get("preco_medio_por_unidade_R$") is None for c in melhores) else "")
        )
    else:
        bloco_alt = "<p class='vazio'>Sem alternativas calculadas.</p>"
    partes.append(f"""<section>
  <h2><span class="ic">↗</span> Onde mais olhar — mesma UF</h2>
  {bloco_alt}
</section>""")

    # --- lacunas
    escritas_lista = list(cfg.get("nao_sabe", []))
    lacunas = []
    # Quem recebe o HTML não tem o JSON: a lacuna do script tem de vir legível aqui,
    # não como "ver JSON".
    for rotulo, bloco in (("zoneamento", zon), ("setores", setores), ("concorrência", comp1),
                          ("mercado UTC", utc), ("contexto", ctx)):
        lac = bloco.get("lacunas")
        if isinstance(lac, list):
            for item in lac[:6]:
                if isinstance(item, dict):
                    texto = item.get("motivo") or item.get("_impacto") or ""
                    alvo = item.get("base") or item.get("utc") or item.get("campo") or ""
                    detalhe = f"{alvo}: {texto}".strip(": ")
                else:
                    detalhe = str(item)
                if detalhe:
                    lacunas.append(explicar_lacuna(rotulo, item.get("base") or item.get("utc") or "", texto)
                                   if isinstance(item, dict) else str(item))
        elif isinstance(lac, dict):
            for k, v in lac.items():
                if k.startswith("_") or not v:
                    continue
                # Alguns valores são dicionários (camada -> motivo). Despejar o
                # dict cru no HTML é ilegível; abrimos item por item.
                if isinstance(v, dict):
                    for camada, motivo in v.items():
                        lacunas.append(explicar_lacuna(rotulo, camada, motivo))
                else:
                    # Lacuna de uma linha nao e acionavel. O relatorio de
                    # impedimento ja explica as do gate; o completo passa a
                    # usar a mesma explicacao, em vez de despejar a chave.
                    # Explicacao por chave, venha ela do mapa do gate ou do
                    # mapa geral. Sem isso a lacuna sai como "chave: valor" —
                    # e "3700" sozinho nao diz nem a consequencia nem o caminho.
                    explicada = (LACUNAS_DO_GATE.get(k) if rotulo == "zoneamento" else None) or CONSEQUENCIA.get(k)
                    if explicada:
                        # A explicacao SUBSTITUI o motivo cru. Repeti-lo entre
                        # parenteses logo depois de "Destrava com" fazia a
                        # repeticao parecer o caminho de destrava, e em dois
                        # casos saia com parenteses aninhados.
                        prefixo = f"{num(v)} " if isinstance(v, (int, float)) else ""
                        lacunas.append(f"{SECOES_HUMANAS.get(rotulo, rotulo)} — {prefixo}{explicada}.")
                    else:
                        lacunas.append(f"{SECOES_HUMANAS.get(rotulo, rotulo)} — {k.replace('_', ' ')}: {v}")
    # A mesma lacuna costuma vir repetida (uma por UTC, uma por setor). Repetir
    # a linha idêntica vira ruído e esconde as outras; agrupamos com contagem.
    agrupadas, ordem = {}, []
    # A narrativa explica a lacuna melhor que o script. Quando o tema já está
    # na seção escrita pelo modelo, o item automático só repetiria pior — então
    # o filtro vale SÓ para as automáticas, nunca para as escritas.
    escritas = " ".join(escritas_lista).lower()

    def ja_explicada(linha: str) -> bool:
        depois = linha.split("—", 1)[-1].split(":", 1)[0].strip().lower()
        termos = [p for p in depois.replace("(", " ").replace(")", " ").split() if len(p) > 5]
        return bool(termos) and all(p in escritas for p in termos[:3])

    automaticas = [limpar_tecnico(x) for x in lacunas]
    automaticas = [x for x in automaticas if not ja_explicada(x)]
    lacunas = [limpar_tecnico(x) for x in escritas_lista] + automaticas
    for x in lacunas:
        if x not in agrupadas:
            agrupadas[x] = 0
            ordem.append(x)
        agrupadas[x] += 1
    itens_lac = "".join(
        f"<li>{rico(x)}{f' <b>({agrupadas[x]}×)</b>' if agrupadas[x] > 1 else ''}</li>"
        for x in ordem
    )
    campo = "".join(f"<li>{rico(limpar_tecnico(x))}</li>" for x in cfg.get("campo", []))
    # A secao continua existindo e continua completa: o que muda e que ela nasce
    # RECOLHIDA. Lacuna aberta ocupa uma tela inteira perto do fim do documento e
    # empurra as Fontes para fora da vista; recolhida, ela segue a um clique e o
    # contador no titulo impede que o leitor ache que nao ha lacuna nenhuma.
    # Nao e omissao: omitir quebraria a regra de declarar toda lacuna.
    n_lac = len(ordem)
    partes.append(f"""<details class="lacunas">
  <summary><span class="ic">!</span> O que este dossiê NÃO sabe
    <span class="qtd">{n_lac} {'item' if n_lac == 1 else 'itens'}</span><span class="seta"></span></summary>
  <div class="corpo-lac"><ul>{itens_lac}</ul></div>
</details>
<section>
  <h2><span class="ic">✓</span> Para confirmar em campo</h2>
  <ul class="proc">{campo or "<li>—</li>"}</ul>
</section>
"""); partes.append(bloco_fontes(fontes, dump, limpar_tecnico(cfg.get("origem_da_coordenada")) or "")); partes.append(f"""<footer>
  Órbita · Dossiê de Região · {e(cfg['endereco'])}
</footer>""")

    corpo = "\n".join(partes)
    return PAGINA.replace("{{CORPO}}", corpo).replace("{{TITULO}}", e(cfg["endereco"]))


# ---------------------------------------------------------------------------
# Dossiê de impedimento
# ---------------------------------------------------------------------------
# Quando o gate barra, o entregável continua sendo HTML — é a regra da casa, e
# abrir exceção criaria dois formatos para a mesma skill, um deles escrito à
# mão. O que muda é o CONTEÚDO: nenhum script de mercado roda, porque dossiê de
# mercado em ponto barrado sugere ao leitor que há número a negociar, e não há.

# Como ler cada lacuna que o gate devolve. Linha solta não é acionável: o leitor
# precisa da consequência e do caminho, não só do nome do que faltou.
# O config guarda o perfil no vocabulario do script; o relatorio e lido por
# analista e por executivo de Expansao, que nao chamam ninguem de "existente".
PERFIL_HUMANO = {
    "novo": "empresário novo",
    "existente": "já associado",
}

LACUNAS_DO_GATE = {
    "lojas_da_cidade_sem_coordenada": (
        "loja(s) Farmarcas do município sem coordenada no cadastro — a distância "
        "mínima até o ponto não pode ser checada nessas, e isso é lacuna, não "
        "ausência de risco. Destrava com a coordenada no cadastro ou com "
        "conferência do endereço em campo"
    ),
    "cobertura_de_coordenada_no_cadastro": (
        "cobertura de coordenada no cadastro de lojas — fora dessa fatia não há "
        "como medir distância entre lojas, nem confirmar em que cidade cada uma "
        "está. Destrava com o preenchimento da coordenada no cadastro, que é "
        "base interna e não depende de fonte externa"
    ),
    "distancia_abaixo_de_60_mil": (
        "abaixo de 60 mil habitantes a distância mínima entre lojas não é checada — premissa "
        "herdada de quando o teto contava lojas e barrava antes. Com o teto contando grupos, "
        "uma cidade desta faixa pode passar no gate e seguir sem a checagem, e então a segunda regra de "
        "zoneamento fica sem veredito e o resultado do gate não avisa. Destrava com a regra "
        "oficial declarando se a distância vale em toda faixa"
    ),
    "premissa_status": (
        "quais status ocupam vaga no teto é premissa adotada aqui, não texto da "
        "regra — se loja desativada passasse a contar, cidades hoje dentro do teto "
        "passariam a estourá-lo. Destrava com a definição escrita na regra"
    ),
    "limites_de_faixa": (
        "a regra escreve as faixas de população com limites sobrepostos — "
        "exatamente nos cortes, duas faixas descrevem a mesma cidade e o teto fica "
        "ambíguo. Destrava com a correção da página"
    ),
    "popular_x_convencional": (
        "a regra afirma que popular e convencional seguem critérios diferentes sem "
        "dizer quais — só a exigência explícita da faixa de 60 a 120 mil habitantes "
        "foi aplicada. Destrava com o detalhamento da página"
    ),
}


def data_censo() -> str:
    """Data de extracao da populacao do Censo, lida do proprio cache.

    A populacao do Censo NAO vem do acervo de camadas: vem da API do IBGE, com
    data propria. Carimba-la com a data do dump atribuiria ao acervo justamente
    o numero que corta a faixa do teto — o mais importante do documento.
    """
    caminho = os.path.join(AQUI, "cache", "censo2022.json")
    try:
        return datetime.date.fromtimestamp(os.path.getmtime(caminho)).isoformat()
    except OSError:
        return "data nao recuperavel"


def tabela_lojas_da_cidade(zon: dict, vinculo_apurado: bool = True) -> str:
    """Lojas Farmarcas do município: as que ocupam vaga e as desativadas.

    A distância só aparece quando existe coordenada. Preencher com o centroide do
    bairro sem dizer transformaria aproximação de bairro em medida de quarteirão,
    que é a diferença entre passar e não passar na distância mínima.
    """
    linhas = []
    grupos = (
        ("grupo ocupa vaga", zon.get("lojas_farmarcas_na_cidade") or []),
        ("não ocupa vaga", zon.get("lojas_desativadas_na_cidade") or []),
    )
    for papel, lojas in grupos:
        for lj in lojas:
            d = lj.get("distancia_m")
            aprox = lj.get("distancia_aproximada_por_centroide_do_bairro_m")
            if d is not None:
                dist = f"{num(d)} m"
            elif aprox is not None:
                dist = f"~{num(aprox)} m <span class=\"nota\">pelo centro do bairro</span>"
            else:
                dist = "<b>não medida</b> <span class=\"nota\">sem coordenada no cadastro</span>"
            if not lj.get("responsavel_no_cadastro", True):
                # Terceiro estado: o cadastro nao registra responsavel por esta
                # loja. Dizer "de outro associado" aqui converteria ausencia de
                # dado em afirmacao — e contradiria a coluna de grupo ao lado.
                vinculo = ("<b>não apurado</b> <span class=\"nota\">o cadastro não registra "
                           "responsável para esta loja</span>")
            elif vinculo_apurado:
                vinculo = "do próprio solicitante" if lj.get("do_solicitante") else "de outro associado"
            else:
                # Sem o responsavel informado na geracao, TODA loja sai como de
                # outro associado — silenciosamente, e trocando o sentido do
                # documento. Campo vazio com motivo e melhor que valor errado.
                vinculo = "<b>não apurado</b> <span class=\"nota\">responsável não informado nesta geração</span>"
            destaque = " class=\"tem\"" if papel.endswith("ocupa vaga") and not papel.startswith("não") else ""
            linhas.append(
                f"<tr{destaque}><td>{e(lj.get('bandeira'))}</td><td>{e(lj.get('modelo'))}</td>"
                f"<td>{e(lj.get('status'))}</td><td>{e(lj.get('bairro'))}</td>"
                f"<td>{dist}</td><td>{e(lj.get('grupo_economico'))}</td>"
                f"<td>{vinculo}</td><td>{e(papel)}</td></tr>"
            )
    if not linhas:
        return (
            "<p class=\"vazio\">Nenhuma loja Farmarcas cadastrada neste município. "
            "Se o impedimento não vem do teto, ele vem de outra regra — veja acima.</p>"
        )
    return (
        "<table><thead><tr><th>Bandeira</th><th>Modelo</th><th>Status</th>"
        "<th>Bairro</th><th>Distância até o ponto</th><th>Grupo</th><th>Vínculo</th>"
        "<th>No teto</th></tr></thead><tbody>" + "".join(linhas) + "</tbody></table>"
    )


def bloco_duas_leituras(zon: dict, vinculo_apurado: bool = True) -> str:
    """O teto da praça, medido em grupos econômicos, com a densidade de lojas ao lado.

    A regra refinada em 2026-10-29 barra a entrada de um NOVO grupo econômico na
    praça, não a quantidade de lojas: cidade cujas lojas respondem todas ao mesmo
    grupo não tem conflito entre associados, que é o que a regra protege. A
    contagem de lojas continua à vista, como alerta de densidade — ela diz quanto
    o mesmo mercado vai ser dividido, e isso é efeito econômico a dimensionar.

    As duas contagens são sempre sobre a cidade DEPOIS do pedido. Comparar o
    estado atual responde outra pergunta que a do analista, que é se esta loja
    cabe.
    """
    teto = zon.get("teto_de_lojas")
    if teto is None:
        return ""
    depois = (zon.get("_duas_leituras_do_teto") or {}).get("com_o_pedido") or {}
    lojas = zon.get("lojas_ocupando_vaga") or 0
    grupos = zon.get("empresarios_distintos_na_cidade") or 0
    lojas_depois = depois.get("contando_lojas")
    grupos_depois = depois.get("contando_grupos_economicos")
    excede_lojas = bool(depois.get("excede_contando_lojas"))
    excede_grupos = bool(depois.get("excede_contando_grupos"))

    if not vinculo_apurado:
        # Sem saber se o solicitante ja responde por loja nesta cidade, a contagem
        # de grupos — que agora e a que BARRA — sai errada e com cara de certa.
        return f"""<h3>O teto da praça</h3>
  <div class="cards">
    {card("Teto da faixa", num(teto) + " grupo(s) econômico(s)", "definido pela população do município")}
    {card("Grupos econômicos", "—", "não apurado: o responsável pelo solicitante não foi informado nesta geração", "#6c6878")}
    {card("Lojas na cidade", f"{num(lojas)} hoje &rarr; {num(lojas_depois)} com o pedido",
          "acima do que a faixa dimensiona" if excede_lojas else "dentro do que a faixa dimensiona",
          "#b07d00" if excede_lojas else "#0f7b45")}
  </div>
  <p class="explica"><b>A contagem que decide não foi apurada.</b> O teto da praça conta
  <b>grupos econômicos</b>, não lojas: ela depende de saber se o solicitante já responde por
  alguma loja desta cidade. Se já responde, o pedido não traz grupo novo e não há o que barrar;
  se não responde, traz, e o teto pode ser estourado. Como o vínculo não foi informado na
  geração deste relatório, essa comparação está em aberto.</p>"""

    if excede_grupos:
        leitura = (
            "<b>O pedido traz um grupo econômico novo para uma praça que já está no teto.</b> "
            "É isso que a regra barra: o que ela protege é a convivência entre associados, e "
            "cada grupo a mais é um associado a mais disputando o mesmo mercado."
        )
    elif excede_lojas:
        leitura = (
            "<b>A praça fica com mais lojas do que a faixa dimensiona, mas sem grupo econômico "
            "novo — e isso não barra.</b> A regra existe para evitar conflito e concorrência "
            "desleal entre associados, e não há conflito entre associados onde as lojas "
            "respondem ao mesmo grupo. O que sobra é risco econômico do próprio grupo: mais "
            "pontos dividindo o mesmo mercado, decisão que é dele."
        )
    else:
        leitura = (
            "<b>O pedido cabe no teto da praça pelas duas contagens.</b> Não traz grupo "
            "econômico novo além do que a faixa comporta, e a cidade também não fica com mais "
            "lojas do que ela dimensiona."
        )

    return f"""<h3>O teto da praça</h3>
  <div class="cards">
    {card("Teto da faixa", num(teto) + " grupo(s) econômico(s)", "definido pela população do município")}
    {card("Grupos econômicos", f"{num(grupos)} hoje &rarr; {num(grupos_depois)} com o pedido",
          "excede o teto — é o que barra" if excede_grupos else "dentro do teto",
          "#b4503c" if excede_grupos else "#0f7b45")}
    {card("Lojas na cidade", f"{num(lojas)} hoje &rarr; {num(lojas_depois)} com o pedido",
          "acima do que a faixa dimensiona — alerta, não impedimento" if excede_lojas
          else "dentro do que a faixa dimensiona",
          "#b07d00" if excede_lojas else "#0f7b45")}
  </div>
  <p class="explica">{leitura} O teto conta <b>grupos econômicos</b>: o pedido sempre
  acrescenta uma loja, mas só acrescenta um grupo quando o solicitante ainda não responde por
  loja nesta cidade. Os grupos são apurados pelo responsável registrado no cadastro, comparado
  por nome e não por CNPJ — duas lojas do mesmo dono com grafia divergente contariam como dois
  grupos, e um grupo a mais aqui barra um pedido que caberia. Na rede inteira, 207 das 830
  cidades com loja ativa ficam acima do teto contando lojas, contra 34 contando grupos
  econômicos.</p>"""


def bloco_onde_mais_olhar(alt: dict, cfg: dict) -> str:
    """Praças onde a regra de zoneamento não barra — só no relatório de impedimento.

    Não é análise de mercado do ponto barrado, e a distinção precisa estar na
    tela: estudar o endereço reprovado sugere que há número a negociar ali;
    listar praças onde a regra não barra é o próximo passo, e não afirma nada
    sobre o endereço pedido.

    A disponibilidade conta GRUPOS ECONÔMICOS, nunca lojas. Cidade com cinco
    lojas de um único dono e teto 2 continua disponível — contar lojas esconderia
    justamente as praças que esta seção existe para mostrar.
    """
    linhas_dados = (alt or {}).get("melhores") or []
    if not linhas_dados:
        return ""
    disp = (alt or {}).get("_disponibilidade") or {}
    modelo = cfg.get("modelo") or ""
    corpo = "".join(
        f"<tr><td><b>{e(m.get('municipio'))}/{e(m.get('uf'))}</b>"
        + (f"<div class=\"nota\">{e(m.get('localidade'))}</div>" if m.get("localidade") else "")
        + f"</td><td>{(str(int(m['distancia_km'])) + ' km') if m.get('distancia_km') is not None else '—'}</td>"
        + f"<td>{e(m.get('escala_mercado_nao_atendido'))}</td>"
        + (
            f"<td>{num(m.get('grupos_economicos_no_municipio'))} de {num(m.get('teto_de_lojas'))}"
            if m.get("teto_de_lojas") is not None
            else f"<td>{num(m.get('grupos_economicos_no_municipio'))} grupo(s)<div class=\"nota\">a cidade não tem teto</div>"
        )
        + f"<div class=\"nota\">{e(m.get('zoneamento'))}</div></td>"
        f"<td>{pct(m.get('crescimento_mercado'))}</td></tr>"
        for m in linhas_dados
    )
    nota_modelo = (
        f"A lista já considera que a bandeira pretendida é <b>{e(modelo)}</b>."
        if modelo
        else "O modelo pretendido não foi informado, então a exigência de bandeira popular "
        "do 2º grupo na faixa de 60 a 120 mil <b>não</b> foi aplicada ao filtro."
    )
    # Sem declarar o raio, o leitor nao sabe se "as melhores do estado" foram
    # filtradas por alcance ou nao — e quando NAO ha praca perto, esse fato e o
    # achado mais importante da secao, nao uma nota de rodape.
    prox = (alt or {}).get("_proximidade") or {}
    if prox.get("raio_aplicado"):
        nota_raio = (
            f"<b>A lista está limitada a {num(prox.get('raio_km_pedido'))} km do endereço "
            f"analisado</b>, medidos até o centro aproximado de cada município. Esse raio é "
            f"premissa desta análise, não regra da casa: nenhuma fonte diz a que distância um "
            f"empresário aceita operar. Sem ele, a lista devolveria as maiores praças da UF "
            f"para qualquer ponto do estado."
        )
    elif prox.get("raio_km_pedido"):
        nota_raio = (
            f"<b>Não há praça disponível a menos de {num(prox.get('raio_km_pedido'))} km deste "
            f"endereço</b> — foram encontradas {num(prox.get('pracas_disponiveis_dentro_do_raio'))}. "
            f"Isso é achado, não falha da busca: significa que o caminho mais próximo exige "
            f"mudar de região. A lista abaixo volta a cobrir a UF inteira, com a distância de "
            f"cada praça declarada para que a decisão seja consciente."
        )
    else:
        nota_raio = (
            "A lista cobre a UF inteira, sem filtro de distância — as praças podem estar "
            "longe do endereço analisado."
        )
    return f"""<section>
  <h2><span class="ic">→</span> Onde mais olhar — praças onde a regra não barra</h2>
  <p class="explica"><b>Isto não é análise de mercado deste ponto.</b> Levantar renda,
  concorrência e potencial do endereço reprovado sugeriria que há número a negociar ali, e
  não há — o que existe para resolver é decisão de quem é dono da regra. A lista abaixo não
  afirma nada sobre o endereço pedido: são praças da mesma UF onde a entrada de um grupo
  novo <b>cabe no teto</b>, ordenadas pelo mercado que hoje circula sem passar pela rede.
  Cada linha é uma unidade de mercado, por isso a mesma cidade pode aparecer mais de uma vez,
  sempre com a localidade nomeada. {nota_modelo}</p>
  <p class="explica">{nota_raio}</p>
  <table><thead><tr><th>Praça</th><th>Distância</th><th>Mercado não atendido</th>
  <th>Grupos / teto</th><th>Cresc.</th></tr></thead><tbody>{corpo}</tbody></table>
  <p class="vazio"><b>Como a disponibilidade é apurada.</b> {e(disp.get("_regra"))}
  {e(disp.get("_apuracao_do_grupo"))} — ou seja, uma praça pode aparecer como indisponível
  por grafia divergente no cadastro, e o caminho para confirmar é o CNPJ. Esta lista escolhe
  a <b>praça</b>, não o ponto: cada uma ainda precisa do seu próprio dossiê.</p>
</section>"""


def construir_impedimento(cfg: dict, zon: dict) -> str:
    """Relatório curto de ponto barrado pelo zoneamento. Nenhum dado de mercado.

    Narrativa esperada no config: `resumo`, `leitura` (lista de parágrafos),
    `o_que_mudaria`, `alertas_cadastro`, `nao_sabe` e `campo`. Todos os números
    vêm do gate — o modelo não formata nem recalcula nenhum deles.
    """
    dump = B.DATA_DO_DUMP
    cor = "#b4503c"
    imps = zon.get("impedimentos") or []
    pop = zon.get("populacao_censo_2022")
    # Para empresario NOVO, nenhuma loja da cidade e dele e o vinculo sai certo
    # sem informar responsavel. Para quem JA opera, o vinculo depende do
    # responsavel passado na geracao — que, por LGPD, nao fica gravado no JSON.
    # Sem ele, o relatorio regerado a partir do mesmo JSON afirmaria o CONTRARIO
    # deste: e o tipo de numero que o analista nao consegue conferir, que e a
    # causa raiz que o produto existe para resolver.
    # UNICO script alem do gate que roda num ponto barrado. Nao levanta nada
    # sobre o endereco reprovado: ranqueia pracas da UF onde a regra nao barra.
    alt = rodar(
        "alternativas.py", "--uf", cfg["uf"], "--excluir-municipio", cfg["codigo_ibge"],
        # Limite 15, nao 6. A ordenacao e por mercado ABSOLUTO nao atendido, entao
        # as primeiras linhas de qualquer UF sao sempre a capital: com 6, todo
        # relatorio de impedimento de MG devolvia Belo Horizonte, Juiz de Fora e
        # Montes Claros, independentemente de onde o solicitante opera. Quem recebeu
        # um "nao" precisa de caminho, e caminho que ignora a regiao dele nao e
        # caminho. Alargar a janela nao corrige o vies da ordenacao — so reduz o
        # estrago dele ate existir um criterio de proximidade.
        "--so-disponiveis", "--limite", 15,
        "--perto-de", f"{cfg['lat']},{cfg['lng']}", "--raio-km", RAIO_PRACAS_KM,
        *(("--modelo", cfg["modelo"]) if cfg.get("modelo") else ()),
    )
    vinculo_apurado = cfg.get("perfil") == "novo" or bool(cfg.get("ge"))
    if not vinculo_apurado:
        print(
            "AVISO: o solicitante ja opera loja(s) da rede e nenhum responsavel foi "
            "informado nesta geracao. O vinculo de cada loja com ele NAO foi apurado: "
            "a contagem por empresarios e a coluna de vinculo saem como nao apuradas.",
            file=sys.stderr,
        )
    # Toda distancia do relatorio e medida A PARTIR da coordenada do ponto. Se ela
    # nao foi resolvida por fonte publica, isso e a lacuna de baixo de toda a
    # secao de distancia — e era o unico numero do documento sem origem declarada.
    origem_coord = limpar_tecnico(cfg.get("origem_da_coordenada")) or (
        "origem não declarada nesta geração — toda distância deste relatório é medida a "
        "partir dela"
    )
    carimbo_vinculo = (
        "O vínculo de cada loja com o solicitante é apurado pelo responsável informado "
        "na geração deste relatório, comparado por nome contra o cadastro, não por CNPJ."
        if vinculo_apurado and cfg.get("ge")
        else (
            "O solicitante é empresário novo, então nenhuma loja da cidade é dele."
            if cfg.get("perfil") == "novo"
            else "O vínculo das lojas com o solicitante não foi apurado nesta geração."
        )
    )

    partes = [f"""<header>
  <div class="marca">Órbita · Impedimento de Zoneamento</div>
  <div class="sub">Checagem de regra de expansão — <b>sem score e sem análise de
    mercado</b> · acervo de camadas de {dump} · cadastro de lojas de {B.DATA_DO_CADASTRO} ·
    população do Censo extraída em {data_censo()}</div>
</header>
<div class="faixa-end">{e(cfg['endereco'])}</div>
<section class="topo">
  <div class="gate" style="border-color:{cor}">
    <div class="rot">Zoneamento</div>
    <div class="val" style="color:{cor}">Impedimento</div>
    <div class="nota">{e(zon.get('faixa_aplicada'))}</div>
  </div>
  <div class="resumo">
    <div class="rot">Em uma linha</div>
    <p>{rico(limpar_tecnico(cfg.get('resumo')))}</p>
    <div class="meta">Solicitante: <b>{e(PERFIL_HUMANO.get(cfg.get("perfil"), cfg.get("perfil") or "não informado"))}</b> ·
      Bandeira pretendida: <b>{e(cfg.get('bandeira') or '—')}</b> ({e(cfg.get('modelo') or '—')}) ·
      População do município (Censo 2022): <b>{num(pop)}</b></div>
  </div>
</section>"""]

    itens_imp = "".join(
        f"<tr><td>{e(limpar_tecnico(i.get('regra')))}</td>"
        f"<td>{e(limpar_tecnico(i.get('constatado')))}</td></tr>"
        for i in imps
    ) or "<tr><td colspan=\"2\">—</td></tr>"
    partes.append(f"""<section>
  <h2><span class="ic">■</span> O ponto não passa no zoneamento</h2>
  <p class="explica"><b>Por que o relatório termina aqui.</b> O zoneamento é
  <b>gate</b>, não indicador: a consulta acontece antes de prosseguir com a análise.
  Um estudo de mercado completo sobre um ponto que a regra barra sugere ao leitor que
  há número a negociar — e o que existe para resolver aqui não é número, é decisão de
  quem é dono da regra. Por isso nenhuma camada de mercado foi levantada.</p>
  <table><thead><tr><th>Regra</th><th>Constatado</th></tr></thead>
  <tbody>{itens_imp}</tbody></table>
  <div class="cards" style="margin-top:12px">
    {card("População do município", num(pop) + " habitantes", "Censo 2022 — é ela que corta a faixa do teto")}
    {card("População no acervo interno", num(zon.get("populacao_acervo_interno")) + " habitantes", "ano de referência não declarado na base; a faixa é cortada pelo Censo")}
    {card("Faixa aplicada", e(zon.get("faixa_aplicada")), "regra de zoneamento vigente")}
    {card("Lojas ativas na cidade hoje", num(zon.get("lojas_ocupando_vaga")), "ativas, montando ou em transição — quem ocupa vaga no teto é o grupo, não a loja")}
  </div>
  {bloco_duas_leituras(zon, vinculo_apurado)}
</section>""")

    leitura = "".join(f"<p>{rico(limpar_tecnico(p))}</p>" for p in (cfg.get("leitura") or []))
    if leitura:
        partes.append(f"""<section>
  <h2><span class="ic">◆</span> Leitura do impedimento</h2>
  <div class="lente" style="border-color:#b4503c;background:#fdeee9">{leitura}</div>
</section>""")

    partes.append(f"""<section>
  <h2><span class="ic">◉</span> Lojas Farmarcas no município</h2>
  <p class="explica"><b>Esta tabela sai do cadastro de lojas da rede.</b>
  Nome de bandeira encontrado na camada de concorrentes não prova que a loja é da rede —
  é suspeita a confirmar, e não entra aqui. O vínculo com o solicitante é apurado pelo
  responsável registrado no cadastro, comparado por nome e não por CNPJ: grafia divergente
  ou homônimo inverteria de quem é cada loja. Loja do próprio solicitante aparece separada
  de loja de outro associado: sobreposição com a própria operação é efeito econômico a
  dimensionar, enquanto sobreposição com a de outro associado é o conflito entre
  associados que a regra existe para evitar. <b>Para o teto, é esta distinção que vale: ele
  conta grupos econômicos, e o pedido só acrescenta um quando o solicitante ainda não
  responde por loja nesta cidade.</b> A coluna de grupo usa rótulo anônimo e serve para
  conferir a contagem: duas linhas com o mesmo rótulo são um grupo só.</p>
  {tabela_lojas_da_cidade(zon, vinculo_apurado)}
</section>""")

    muda = "".join(f"<li>{rico(limpar_tecnico(x))}</li>" for x in (cfg.get("o_que_mudaria") or []))
    if muda:
        partes.append(f"""<section>
  <h2><span class="ic">↻</span> O que mudaria o resultado</h2>
  <ul class="proc">{muda}</ul>
</section>""")

    partes.append(bloco_onde_mais_olhar(alt, cfg))

    alertas = [limpar_tecnico(x) for x in (cfg.get("alertas_cadastro") or [])]
    for a in zon.get("alertas") or []:
        # A comparação entre as duas contagens já tem bloco próprio, calculado
        # sobre a cidade depois do pedido. Repetir aqui o alerta genérico do gate
        # afirmaria divergência mesmo onde as duas leituras coincidem.
        if a.get("id") == "duas_leituras_do_teto" or "duas leituras" in (a.get("regra") or ""):
            continue
        alertas.append(
            limpar_tecnico(f"{a.get('regra')} — {a.get('constatado')}. {a.get('ressalva') or ''}")
        )
    for lj in zon.get("lojas_proximas_cadastradas_em_outra_cidade") or []:
        alertas.append(
            f"Loja cadastrada em {e(lj.get('cidade_cadastrada') or 'outra cidade')} aparece a "
            f"{num(lj.get('distancia_m'))} m deste ponto — como o teto é contado por cidade "
            "cadastrada, cadastro errado erra o teto junto."
        )
    if alertas:
        itens = "".join(f"<li>{rico(x)}</li>" for x in alertas)
        partes.append(f"""<section>
  <h2><span class="ic">⚑</span> Alertas de cadastro</h2>
  <ul class="proc">{itens}</ul>
</section>""")

    lacunas = [limpar_tecnico(x) for x in (cfg.get("nao_sabe") or [])]
    for chave, valor in (zon.get("lacunas") or {}).items():
        if chave.startswith("_") or not valor:
            continue
        explicacao = LACUNAS_DO_GATE.get(chave)
        if not explicacao:
            continue
        if isinstance(valor, (int, float)):
            lacunas.append(f"{num(valor)} {explicacao}.")
        else:
            lacunas.append(f"{explicacao} ({valor}).")
    if not vinculo_apurado:
        lacunas.append(
            "<b>De quem são as lojas Farmarcas já instaladas nesta cidade.</b> O "
            "solicitante já opera na rede, mas o responsável por ele não foi informado "
            "na geração deste relatório, então não dá para separar sobreposição com a "
            "própria operação — efeito econômico a dimensionar — de conflito com outro "
            "associado, que é o que a regra existe para evitar. É também o que decide a "
            "contagem do teto por empresários. Destrava regerando o relatório com o "
            "responsável registrado no cadastro."
        )
    # Incondicional: o leitor precisa saber que nada de mercado foi levantado,
    # senão o silêncio das camadas é lido como ausência de problema nelas.
    lacunas.append(
        "Fluxo de passantes não existe no acervo nem no produto, e nenhuma camada de "
        "mercado foi levantada para este ponto — população no raio, renda, concorrência "
        "e potencial de consumo seguem desconhecidos aqui. Destrava se o impedimento for "
        "resolvido por quem é dono da regra e o pedido voltar para análise."
    )
    # Deduplicar: a lacuna escrita na narrativa responde as tres perguntas, a do
    # gate vem em uma linha. Concatenar as duas mostrava o mesmo assunto duas
    # vezes, e a versao pobre contaminava a boa. A da narrativa vence.
    vistas, unicas = set(), []
    for x in lacunas:
        chave = " ".join(re.sub(r"<[^>]+>", " ", x).lower().split())[:60]
        if chave in vistas:
            continue
        vistas.add(chave)
        unicas.append(x)
    lacunas = unicas
    campo = "".join(f"<li>{rico(limpar_tecnico(x))}</li>" for x in (cfg.get("campo") or []))
    itens_lac = "".join(f"<li>{rico(x)}</li>" for x in lacunas)
    # Mesma decisao do dossie completo: recolhida por padrao, nunca omitida.
    n_lac = len(lacunas)
    partes.append(f"""<details class="lacunas">
  <summary><span class="ic">!</span> O que esta checagem NÃO sabe
    <span class="qtd">{n_lac} {'item' if n_lac == 1 else 'itens'}</span><span class="seta"></span></summary>
  <div class="corpo-lac"><ul>{itens_lac}</ul></div>
</details>
<section>
  <h2><span class="ic">✓</span> Para confirmar em campo</h2>
  <ul class="proc">{campo or "<li>—</li>"}</ul>
</section>""")

    partes.append(f"""<section>
  <h2><span class="ic">§</span> Fontes</h2>
  <ul class="proc">
    <li><b>Regras de zoneamento e de expansão</b> — documentação de processo da Farmarcas,
      páginas 4.5 e 6.1, versões de 24/02/2026. A contagem do teto por <b>grupos
      econômicos</b>, confirmada com a área dona da regra em 29/10/2026, <b>substitui a
      contagem por lojas</b> que vigorou até então e <b>aproxima a regra do que a página
      escreve</b>, já que a página fala em empresários. O mínimo de distância por bandeira,
      confirmado em 27/10/2026, é o que <b>diverge</b> da página, que escreve apenas 300 m
      sem distinguir bandeira.</li>
    <li><b>Coordenada do ponto</b> — {origem_coord}</li>
    <li><b>População do município</b> — Censo 2022 do IBGE, pela API pública, extração de
      {e(data_censo())}. Não vem do acervo de camadas. A data é a da gravação local da
      resposta: copiar esse arquivo entre máquinas a reescreve.</li>
    <li><b>Lojas da rede, status, bandeira, modelo e vínculo com o solicitante</b> —
      cadastro de lojas Farmarcas, extração de {e(B.DATA_DO_CADASTRO)}. {carimbo_vinculo}</li>
    <li><b>Contexto do município</b> — acervo de camadas do Órbita, extração de {e(dump)},
      sem atualização automática.</li>
    <li><b>Praças onde a regra não barra</b> — receita por unidade de mercado da IQVIA para
      ordenar, e cadastro de lojas mais Censo 2022 para a disponibilidade de zoneamento.</li>
  </ul>
  <p class="vazio">Este documento não pontua o ponto e não analisa o mercado dele: não há
  score, nota nem status de recomendação. A régua de viabilidade pertence ao produto.</p>
</section>""")

    partes.append(f"""<footer>
  Órbita · Impedimento de Zoneamento · {e(cfg['endereco'])} ·
  insumo para o comentário da análise, não substitui o parecer do analista
</footer>""")

    corpo = "\n".join(partes)
    return PAGINA.replace("{{CORPO}}", corpo).replace("{{TITULO}}", e(cfg["endereco"]))


PAGINA = """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dossiê de Região</title>
<style>
:root{--roxo:#5b2a8c;--linha:#e3e1e8;--texto:#1d1b22;--fraco:#6c6878;--fundo:#f6f5f8}
*{box-sizing:border-box}
body{margin:0;background:var(--fundo);color:var(--texto);
 font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}
.pag{max-width:1040px;margin:0 auto;padding:24px 16px 60px}
header{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;margin-bottom:14px}
.marca{font-size:22px;font-weight:700;color:var(--roxo)}
.sub{color:var(--fraco);font-size:13px}
.faixa-end{background:var(--roxo);color:#fff;padding:11px 16px;border-radius:8px;
 font-weight:600;font-size:13.5px;letter-spacing:.2px}
.topo{display:grid;grid-template-columns:minmax(200px,260px) 1fr;gap:14px;margin:14px 0 26px}
.gate,.resumo{background:#fff;border:1px solid var(--linha);border-radius:10px;padding:14px 16px}
.gate{border-left:5px solid #444}
.gate .val{font-size:24px;font-weight:700;margin:2px 0}
.resumo p{margin:4px 0 10px;font-size:16px}
.meta{font-size:12.5px;color:var(--fraco)}
section{background:#fff;border:1px solid var(--linha);border-radius:10px;padding:18px;margin-bottom:16px}
h2{font-size:17px;margin:0 0 14px;display:flex;align-items:center;gap:9px}
h3{font-size:14px;margin:20px 0 8px;color:var(--fraco);text-transform:uppercase;letter-spacing:.6px}
h4{font-size:12.5px;margin:16px 0 7px;color:var(--roxo);font-weight:700}
.ic{display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;
 border-radius:7px;background:var(--roxo);color:#fff;font-size:13px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:11px}
.card{background:#fff;border:1px solid var(--linha);border-left:4px solid var(--roxo);
 border-radius:8px;padding:11px 13px}
.rot{font-size:11.5px;color:var(--fraco);text-transform:uppercase;letter-spacing:.5px}
.val{font-size:19px;font-weight:700;margin-top:3px;word-break:break-word}
.nota{font-size:11.5px;color:var(--fraco);margin-top:4px}
.lente{border:1px solid;border-left-width:4px;border-radius:8px;padding:11px 14px;margin-bottom:10px}
.lente-tit{font-weight:700;font-size:13px;text-transform:uppercase;letter-spacing:.5px}
.lente p{margin:9px 0 0;text-align:justify}
.lente p.abertura{font-size:15.5px;margin-top:7px}
.lente b{font-weight:700}
.swot{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.swot .lente{margin-bottom:0}
.swot .lente p{text-align:left;font-size:14.5px}
.swot .lente p.abertura{font-size:15px}
.swot-eixo{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:7px}
.swot-eixo span{font-size:11px;color:var(--fraco);text-transform:uppercase;letter-spacing:.6px}
table{width:100%;border-collapse:collapse;font-size:13.5px}
th{background:var(--roxo);color:#fff;text-align:left;padding:8px 10px;font-weight:600}
td{padding:7px 10px;border-bottom:1px solid var(--linha)}
tr.tem td{background:#fbf9ff;font-weight:600}
.faixa{display:inline-block;min-width:26px;text-align:center;border-radius:4px;
 padding:1px 7px;color:#fff;font-weight:700;font-size:12px;background:#888}
.f1{background:#e3b505}.f2{background:#1f9d55}.f3{background:#e8730c}.f4{background:#2563eb}
.f5{background:#06b6d4}.f6{background:#dc2626}.f7{background:#7c3aed}.f8{background:#a3a635}
.split{display:grid;grid-template-columns:1fr auto;gap:22px;align-items:center}
.split-cards{display:grid;gap:10px}
.split-graf{text-align:center}
.legenda{font-size:12px;color:var(--fraco);margin-top:6px}
.p{display:inline-block;width:10px;height:10px;border-radius:2px;margin:0 5px 0 12px}
.azul{background:#3b7ddd}.rosa{background:#e8558f}
.vazio{color:var(--fraco);font-size:12.5px;margin-top:9px}
sup.ref{color:var(--roxo);font-weight:700;font-size:11px;margin-left:2px}
table.fontes td{vertical-align:top;font-size:13px}
table.fontes td.n{color:var(--roxo);font-weight:700;width:34px}
ul.proc{margin:0;padding-left:19px;font-size:13.5px}
ul.proc li{margin:4px 0}
.explica{background:#faf9fc;border-left:3px solid var(--roxo);border-radius:0 6px 6px 0;
 padding:10px 13px;margin:0 0 14px;font-size:13.5px;color:#3a3744;text-align:justify}
td .nota{margin-top:2px;max-width:330px}
.lacunas ul{margin:0;padding-left:19px}.lacunas li{margin:5px 0}
details.lacunas{background:#fff;border:1px solid var(--linha);border-radius:10px;
 padding:18px;margin-bottom:16px}
details.lacunas>summary{font-size:17px;font-weight:700;display:flex;align-items:center;
 gap:9px;cursor:pointer;list-style:none;margin:0}
details.lacunas>summary::-webkit-details-marker{display:none}
details.lacunas>summary .qtd{font-size:12px;font-weight:600;color:var(--fraco)}
details.lacunas>summary .seta{margin-left:auto;font-size:12px;font-weight:600;color:var(--roxo)}
details.lacunas:not([open])>summary .seta::after{content:"mostrar ▸"}
details.lacunas[open]>summary .seta::after{content:"ocultar ▾"}
details.lacunas>.corpo-lac{margin-top:14px}
/* Impressao abre o bloco: em PDF nao ha clique, e lacuna que some do papel
   volta a ser lacuna silenciada. */
@media print{details.lacunas>.corpo-lac{display:block!important;
 content-visibility:visible!important}details.lacunas>summary .seta{display:none}}
footer{color:var(--fraco);font-size:12px;text-align:center;padding:10px 4px}
@media(max-width:760px){.topo,.split,.swot{grid-template-columns:1fr}.swot-eixo{display:none}}
@media print{body{background:#fff}section{break-inside:avoid;box-shadow:none}
 .swot .lente{break-inside:avoid}}
</style></head>
<body><div class="pag">{{CORPO}}</div></body></html>
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--saida", required=True)
    # O responsável pelo GE é nome de pessoa e serve só para separar loja do
    # solicitante de loja de outro associado no gate de zoneamento. Entra pela
    # linha de comando e NÃO é gravado no config — o JSON é metade do entregável
    # e vai para outputs/ junto com o HTML.
    ap.add_argument("--ge", default="", help="responsável pelo GE; não gravar no config (LGPD)")
    args = ap.parse_args()

    with open(args.config, encoding="utf-8") as fh:
        cfg = json.load(fh)

    # O aviso olha o que estava GRAVADO no config, antes de o argumento entrar —
    # senão o próprio --ge, que é a correção, dispara o alerta.
    if cfg.get("ge"):
        print(
            "AVISO LGPD: o config traz nome de pessoa no campo 'ge'. Esse arquivo "
            "vai para outputs/ junto com o relatório. Passe o responsável por "
            "--ge e deixe o campo vazio no JSON.",
            file=sys.stderr,
        )
    if args.ge:
        cfg["ge"] = args.ge

    cruzadas = avisar_referencia_cruzada(cfg)
    if cruzadas:
        print(
            "AVISO: a narrativa menciona município(s) com dossiê próprio — "
            + ", ".join(cruzadas)
            + ". Um dossiê não se apoia em outro: confirme que é contexto "
            "geográfico legítimo, não comparação com outra análise.",
            file=sys.stderr,
        )

    # A narrativa e escrita sob a premissa de que o vinculo de cada loja com o
    # solicitante foi apurado. Sem o responsavel, os blocos gerados por script
    # degradam para "nao apurado", mas a PROSA continua afirmando de quem e cada
    # loja — e o aviso que explicaria isso sai em stderr, que quem le o HTML nao
    # ve. Meio relatorio honesto com meia prosa afirmando demais e pior que
    # relatorio nenhum, e regerar com o argumento certo custa zero.
    if cfg.get("perfil") == "existente" and not cfg.get("ge"):
        print(
            "ERRO: o solicitante ja opera loja(s) da rede, entao o vinculo de cada "
            "loja com ele decide a leitura de canibalizacao e a contagem do teto por "
            "empresarios. Informe o responsavel pelo GE na geracao (nao grave o nome "
            "no config, por LGPD). Nada foi gerado.",
            file=sys.stderr,
        )
        return 2

    # A nota de confianca decide se o item ENTRA na leitura da regiao; ela nunca
    # vira texto. Escrita, ela repetia a mesma formula em todo paragrafo, dobrava
    # o tamanho do quadrante e ensinava o leitor a pular justamente a frase que
    # carrega a ressalva. O limite do metodo continua obrigatorio — mudou de
    # lugar: vai para "O que este dossie NAO sabe", que e onde se procura por ele.
    suspeitos = [
        i.get("titulo", "(sem titulo)")[:60]
        for conteudo in (cfg.get("lentes") or {}).values()
        for i in (conteudo.get("itens", []) if isinstance(conteudo, dict) else conteudo or [])
        if re.search(r"confian[çc]a", f"{i.get('titulo', '')} {i.get('texto', '')}", re.I)
    ]
    if suspeitos:
        print(
            "AVISO: {} item(ns) da leitura da regiao ainda escrevem a nota de "
            "confianca no texto. Ela decide a ENTRADA do item, nao vira frase: "
            "corte a nota e leve a ressalva para 'O que este dossie NAO sabe'. "
            "Itens: {}".format(len(suspeitos), " | ".join(suspeitos)),
            file=sys.stderr,
        )

    # Mesma familia de defeito, outra causa: a lente explicando o METODO que o
    # proprio relatorio ja declara. O card "Metodo de rateio" carrega a cobertura
    # do circulo e a contagem de setores, e os paragrafos explicativos da renda e
    # do potencial ja dizem que cada setor entra pela fracao dentro do circulo e
    # que as taxas sao media ponderada. Repetido na lente isso nao declara nada:
    # dobra o paragrafo e empurra o numero — que e o que o analista procura —
    # para o fim. Fica na lente a ressalva que muda QUAL numero se le (media do
    # canal na UF, MAT de 12 meses, potencial municipal); sai a que descreve como
    # a conta foi feita.
    _METODO_NA_LENTE = (
        r"fra[çc][ãa]o (de |da )?[áa]rea",
        r"m[ée]dia ponderada",
        r"cobert[ao] por setor",
        r"cobertura do c[íi]rculo",
        r"entra(m)? pela fra[çc][ãa]o",
        r"casamento (foi )?por nome",
    )
    metodo = [
        i.get("titulo", "(sem titulo)")[:60]
        for conteudo in (cfg.get("lentes") or {}).values()
        for i in (conteudo.get("itens", []) if isinstance(conteudo, dict) else conteudo or [])
        for padrao in _METODO_NA_LENTE
        if re.search(padrao, f"{i.get('titulo', '')} {i.get('texto', '')}", re.I)
    ]
    if metodo:
        print(
            "AVISO: {} item(ns) da leitura da regiao explicam o METODO de calculo "
            "(rateio por fracao de area, ponderacao das taxas, cobertura do circulo, "
            "criterio de casamento do brick). O relatorio ja declara isso no card de "
            "metodo e nos paragrafos explicativos: na lente e duplicacao, e empurra o "
            "numero para o fim do paragrafo. Itens: {}".format(
                len(dict.fromkeys(metodo)), " | ".join(dict.fromkeys(metodo))
            ),
            file=sys.stderr,
        )

    # O formato do entregavel e sempre HTML; o que o gate decide e QUAL relatorio.
    # A escolha fica aqui, no script, e nao com quem escreve a narrativa: ponto
    # barrado que recebesse o relatorio completo gastaria paginas de mercado
    # sugerindo ao leitor que ha numero a negociar.
    zon = rodar_gate(cfg)
    if zon.get("veredito") == "impedimento":
        if cfg.get("lentes"):
            print(
                "AVISO: o gate barrou o ponto e a narrativa traz as quatro lentes. "
                "Elas foram ignoradas: dossie de impedimento nao leva analise de "
                "mercado. Use os campos leitura, o_que_mudaria e alertas_cadastro.",
                file=sys.stderr,
            )
        pagina = construir_impedimento(cfg, zon)
    else:
        if cfg.get("leitura") and not cfg.get("lentes"):
            print(
                "AVISO: a narrativa esta no formato de impedimento, mas o gate "
                f"devolveu '{zon.get('veredito')}'. O relatorio completo sera montado "
                "e as quatro lentes virao vazias.",
                file=sys.stderr,
            )
        pagina = construir(cfg, zon)
    os.makedirs(os.path.dirname(os.path.abspath(args.saida)), exist_ok=True)
    with open(args.saida, "w", encoding="utf-8") as fh:
        fh.write(pagina)
    print(f"relatório gravado: {args.saida} ({len(pagina):,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
