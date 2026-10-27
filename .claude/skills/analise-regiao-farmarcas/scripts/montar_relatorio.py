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
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import _bases as B  # noqa: E402

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
        "se loja desativada passasse a ocupar vaga, o teto da cidade mudaria e o gate poderia barrar "
        "o ponto. Destrava a regra oficial dizer que status ocupa vaga"
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
        "são concorrentes que existem na base e não entram em nenhuma contagem por raio, "
        "então a concorrência medida é um piso. Destrava geocodificando esses registros"
    ),
    "registros_com_coordenada_fora_do_brasil_descartados": (
        "coordenada suja descartada na entrada: parte desses pontos pode ser desta região e "
        "está fora da contagem. Destrava corrigindo a coordenada na origem"
    ),
    "lojas_do_cadastro_sem_coordenada_preenchida": (
        "um terço do cadastro não entra em nenhuma checagem por distância, aqui ou em qualquer "
        "outra praça. Destrava geocodificando o cadastro"
    ),
    "lojas_do_cadastro_com_coordenada_fora_do_brasil": (
        "coordenada inválida no cadastro de lojas, que o cálculo descarta para não medir distância "
        "errada. Destrava corrigindo o cadastro"
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
    saida = re.sub(r"\s*\(\s*([^)]*)\s*\)", r" (\1)", saida)
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


def card(rotulo: str, valor: str, nota: str = "", cor: str = "#6b2fb5") -> str:
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


def bloco_lentes(lentes: dict, fontes: list) -> str:
    """Rende cada lente como TEXTO CORRIDO, não como lista de bullets.

    Bullet point empilha afirmações soltas; parágrafo obriga a ligar uma à
    outra, que é como o analista lê. Cada item vira um parágrafo com a frase
    de abertura em destaque. Uma lente pode trazer um `abertura` opcional, que
    vem antes dos parágrafos.
    """
    partes = []
    for nome, conteudo in lentes.items():
        if isinstance(conteudo, dict):
            abertura, itens = conteudo.get("abertura", ""), conteudo.get("itens", [])
        else:
            abertura, itens = "", conteudo
        if not itens and not abertura:
            continue
        cor, fundo = CORES.get(nome, ("#444", "#f4f4f4"))
        corpo = f'<p class="abertura">{e(limpar_tecnico(abertura))}</p>' if abertura else ""
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
                f'<p><b>{e(limpar_tecnico(i.get("titulo")))}</b> '
                f'{e(limpar_tecnico(i.get("texto")))}{marca}</p>'
            )
        partes.append(
            f'<div class="lente" style="border-color:{cor};background:{fundo}">'
            f'<div class="lente-tit" style="color:{cor}">{e(nome)}</div>'
            f"{corpo}</div>"
        )
    return "".join(partes)


def bloco_fontes(fontes: list, dump: str) -> str:
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
    return f"""<section>
  <h2><span class="ic">§</span> Fontes</h2>
  {tabela}
  <h3>Procedência geral</h3>
  <ul class="proc">
    <li><b>Acervo de camadas do Órbita</b> — extração de {e(dump)}, sem atualização automática.</li>
    <li><b>Cadastro de lojas Farmarcas</b> — extração de 2026-10-23, três dias mais antiga.</li>
    <li><b>Geometria dos setores censitários</b> — acervo cartográfico do Órbita.</li>
    <li><b>População do Censo 2022</b> — API pública do IBGE, consultada em 2026-10-26.</li>
    <li><b>Faturamento, unidades e preço por brick e por UTC</b> — IQVIA e CloseUp.</li>
    <li><b>Geradores de fluxo no entorno</b> — OpenStreetMap.</li>
    <li><b>Histórico de análises e contratos</b> — base de análises do Órbita.</li>
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


def construir(cfg: dict) -> str:
    lat, lng = cfg["lat"], cfg["lng"]
    cod, uf, mun = cfg["codigo_ibge"], cfg["uf"], cfg["municipio"]
    r1, r2 = cfg.get("raio_principal", 300), cfg.get("raio_amplo", 5000)

    zon = rodar("zoneamento.py", "--lat", lat, "--lng", lng, "--municipio", mun,
                "--uf", uf, "--codigo-ibge", cod, "--bandeira", cfg.get("bandeira", ""),
                "--modelo", cfg.get("modelo", ""), "--perfil", cfg.get("perfil", ""),
                *(("--ge", cfg["ge"]) if cfg.get("ge") else ()))
    setores = rodar("raio_setores.py", "--lat", lat, "--lng", lng, "--raio", r1,
                    "--codigo-ibge", cod, "--metodo", cfg.get("metodo_setores", "area"))
    comp1 = rodar("raio_concorrencia.py", "--lat", lat, "--lng", lng, "--raio", r1,
                  "--listar", 0, "--municipio", mun)
    comp2 = rodar("raio_concorrencia.py", "--lat", lat, "--lng", lng, "--raio", r2,
                  "--listar", 0, "--municipio", mun)
    utc = rodar("mercado_utc.py", "--codigo-ibge", cod)
    brick = rodar("mercado_brick.py", "--uf", uf, "--codigo-ibge", cod, "--lat", lat, "--lng", lng)
    pois = rodar("pois_no_raio.py", "--lat", lat, "--lng", lng, "--raio", max(r1, 500), "--listar", 6)
    ctx = rodar("contexto_municipio.py", "--municipio", mun, "--uf", uf)
    alt = rodar("alternativas.py", "--uf", uf, "--excluir-municipio", cod, "--limite", 6)
    vlj = rodar("venda_por_loja.py", "--uf", uf,
                *(("--bandeira", cfg["bandeira"]) if cfg.get("bandeira") else ()),
                *(("--modelo", cfg["modelo"]) if cfg.get("modelo") else ()))

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
    nota_venda = (
        f"entre as {venda_cid.get('lojas_com_faturamento', 0)} lojas do município com "
        "faturamento cadastrado · fonte: camada Concorrentes 2025"
    )
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

    # --- cabeçalho e gate
    dump = B.DATA_DO_DUMP
    fontes: list = []
    partes = [f"""<header>
  <div class="marca">Órbita · Dossiê de Região</div>
  <div class="sub">Leitura de região para análise de ponto — <b>sem score</b> ·
    dump de {dump} · cadastro de lojas de 2026-10-23</div>
</header>
<div class="faixa-end">{e(cfg['endereco'])}</div>
<section class="topo">
  <div class="gate" style="border-color:{cor_gate}">
    <div class="rot">Zoneamento</div>
    <div class="val" style="color:{cor_gate}">{e(veredito.capitalize())}</div>
    <div class="nota">{e(zon.get('faixa_aplicada'))}</div>
  </div>
  <div class="resumo">
    <div class="rot">Em uma linha</div>
    <p>{e(limpar_tecnico(cfg.get('resumo')))}</p>
    <div class="meta">Solicitante: <b>{e(cfg.get('perfil') or 'não informado')}</b> ·
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
</section>""")

    # --- microterritório
    partes.append(f"""<section>
  <h2><span class="ic">$</span> Microterritório e concorrência</h2>
  <div class="cards">
    {card("Vendas totais na cidade", brl(micro.get("vendas_totais_na_regiao_R$")), (lambda n: f"{n} loja{'s' if (isinstance(n, int) and n != 1) else ''} cadastrada{'s' if (isinstance(n, int) and n != 1) else ''} no município")(micro.get('lojas_com_faturamento_na_regiao','—')), "#c0397a")}
    {card("Média de faturamento por loja", brl(micro.get("media_de_faturamento_por_loja_R$")), "mensal estimado, no raio", "#1a5fb4")}
    {card("Vendas totais no raio", brl(micro.get("vendas_totais_no_raio_R$")), (lambda n: f"{n} loja{'s' if (isinstance(n, int) and n != 1) else ''} com faturamento")(micro.get('lojas_com_faturamento_no_raio','—')), "#c0397a")}
    {card(f"Concorrentes em {num(r1)} m", num(comp1.get("concorrentes", {}).get("total")), f"{num(comp2.get('concorrentes', {}).get('total'))} em {num(r2)} m", "#b4503c")}
    {card("Lojas Farmarcas no raio", num(comp1.get("lojas_farmarcas_no_raio", {}).get("total")), nota_lojas, "#0f7b45")}
    {card("Preço médio no brick", brl((brick.get("brick") or {}).get("preco_medio_por_unidade_R$")), f"UF: {brl((brick.get('uf_inteira') or {}).get('preco_medio_por_unidade_R$'))} · {e(brick.get('criterio_de_casamento'))}", "#6b2fb5")}
  </div>
  <h3>Quanto vende uma loja — duas fontes independentes</h3>
  <p class="explica"><b>Elas não medem a mesma coisa.</b> A primeira linha é o
  <b>faturamento estimado dos concorrentes</b> da praça: descreve o mercado, mas é
  estimativa e está preenchida em menos da metade dos cadastros. A segunda é a
  <b>receita medida das lojas do grupo</b>, apurada por instituto e cruzada loja a
  loja pelo CNPJ — responde quanto <b>a nossa bandeira</b> fatura numa praça assim.
  Em varejo farmacêutico a distribuição tem cauda longa, então mínimo, mediana e
  máximo dizem mais que média: a distância entre os extremos mede o quanto o
  resultado depende de execução e de ponto, não da região.</p>
  <h4>Concorrentes da praça — faturamento estimado</h4>
  <div class="cards">
    {card("Menor venda estimada", brl((venda_cid or {}).get("minimo_R$")), nota_venda, "#1a5fb4")}
    {card("Venda mediana estimada", brl((venda_cid or {}).get("mediana_R$")), nota_venda, "#0f7b45")}
    {card("Maior venda estimada", brl((venda_cid or {}).get("maximo_R$")), nota_venda, "#c0397a")}
  </div>
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
            "<table><thead><tr><th>Categoria e por que gera fluxo</th><th>No raio</th>"
            f"<th>Mais próximo</th><th>Exemplos nomeados</th></tr></thead>"
            f"<tbody>{''.join(linhas)}</tbody></table>"
            "<p class='vazio'>Equipamento sem nome no mapa entra "
            "na contagem e fica fora da coluna de exemplos. Cobertura é colaborativa: "
            "ausência aqui não é ausência no mundo.</p>"
        )
    else:
        bloco_pois = f"<p class='vazio'>Indisponível: {e(pois.get('erro', 'sem dados'))}. É lacuna, não ausência de equipamentos.</p>"
    partes.append(f"""<section>
  <h2><span class="ic">⚑</span> Geradores de fluxo no entorno</h2>
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
        f"<li>{e(x)}{f' <b>({agrupadas[x]}×)</b>' if agrupadas[x] > 1 else ''}</li>"
        for x in ordem
    )
    campo = "".join(f"<li>{e(limpar_tecnico(x))}</li>" for x in cfg.get("campo", []))
    partes.append(f"""<section class="lacunas">
  <h2><span class="ic">!</span> O que este dossiê NÃO sabe</h2>
  <ul>{itens_lac}</ul>
  <h3>Para confirmar em campo</h3>
  <ul>{campo}</ul>
</section>
"""); partes.append(bloco_fontes(fontes, dump)); partes.append(f"""<footer>
  Órbita · Dossiê de Região · {e(cfg['endereco'])}
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
footer{color:var(--fraco);font-size:12px;text-align:center;padding:10px 4px}
@media(max-width:760px){.topo,.split{grid-template-columns:1fr}}
@media print{body{background:#fff}section{break-inside:avoid;box-shadow:none}}
</style></head>
<body><div class="pag">{{CORPO}}</div></body></html>
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--saida", required=True)
    args = ap.parse_args()

    with open(args.config, encoding="utf-8") as fh:
        cfg = json.load(fh)

    cruzadas = avisar_referencia_cruzada(cfg)
    if cruzadas:
        print(
            "AVISO: a narrativa menciona município(s) com dossiê próprio — "
            + ", ".join(cruzadas)
            + ". Um dossiê não se apoia em outro: confirme que é contexto "
            "geográfico legítimo, não comparação com outra análise.",
            file=sys.stderr,
        )

    pagina = construir(cfg)
    os.makedirs(os.path.dirname(os.path.abspath(args.saida)), exist_ok=True)
    with open(args.saida, "w", encoding="utf-8") as fh:
        fh.write(pagina)
    print(f"relatório gravado: {args.saida} ({len(pagina):,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
