"""Confere, sem modelo nenhum, se o dossiê respeita as regras que são mecânicas.

A auditoria de um dossiê sempre teve duas metades. Uma é julgamento: a lente
fala da região ou da medição, o item passa no teste do "e daí?", duas medidas
diferentes foram pareadas como se fossem a mesma. Essa metade exige ler, e é
onde o auditor se paga. A outra metade é casamento de string e número — todo
valor do texto existe numa saída de script, nenhum nome de pessoa escapou,
nenhum score foi inventado, nenhum nome de ferramenta vazou para o corpo. Essa
metade não é tarefa de modelo: é comparação exata, e modelo que a faz erra de
vez em quando, gasta muito e não deixa rastro de como conferiu.

Este script faz a segunda metade. Ele não lê o dossiê — ele o confere.

O que ele NÃO faz, de propósito:

- Não repete os avisos que `montar_relatorio.py` já dá na geração (confiança
  escrita na lente, método duplicado, ressalva de base como oração, valor
  repetido em duas lentes, lacuna de script que não chegou ao entregável).
  Duas implementações da mesma regra divergem com o tempo, e aí não se sabe
  qual está certa.
- Não julga se o número está CERTO. Ele confere se o número tem ORIGEM. Um
  valor apurado por um script com a conta errada passa aqui — e tem de passar:
  conferir a conta é conferir o script, não o dossiê.
- Não substitui o auditor. Fechar sem achado quer dizer que a parte mecânica
  está limpa, e só isso.

Uso:

    python verificar_dossie.py --config outputs/dossies/x.json \\
                               --relatorio outputs/dossies/x.html

A apuração é procurada ao lado do relatório (`x.apuracao.json`), que é onde
`montar_relatorio.py` a grava. Sem ela o script para: conferir procedência
contra nada é teatro.
"""
from __future__ import annotations

import argparse
import html as _html
import json
import math
import os
import re
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

try:
    import _bases as B
except Exception:  # noqa: BLE001 — sem o módulo, a checagem de nome degrada
    B = None

import _parecer as PAR  # noqa: E402 — tabela de direção, sem dependência de base


# ---------------------------------------------------------------------------
# Números escritos em português
# ---------------------------------------------------------------------------

_MULTIPLICADOR = {
    "mil": 1e3,
    "mi": 1e6, "milhão": 1e6, "milhao": 1e6, "milhões": 1e6, "milhoes": 1e6,
    "bi": 1e9, "bilhão": 1e9, "bilhao": 1e9, "bilhões": 1e9, "bilhoes": 1e9,
}

_NUMERO = re.compile(
    r"(R\$\s*)?"
    r"(\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:,\d+)?)"
    r"\s*(%|mil\b|mi\b|milh[õo]es\b|milh[ãa]o\b|bi\b|bilh[õo]es\b|bilh[ãa]o\b)?",
    re.I,
)


class Escrito:
    """Um número como ele aparece no texto, com a precisão com que foi escrito.

    A precisão importa: "3,5" e "3,46" são o mesmo valor apurado escrito de dois
    jeitos, e só um deles é o que o script devolveu. Guardar quantas casas o
    autor escreveu é o que permite dizer qual.
    """

    __slots__ = ("bruto", "valor", "casas", "fator", "pct", "moeda", "onde")

    def __init__(self, bruto, valor, casas, fator, pct, moeda, onde):
        self.bruto, self.valor, self.casas = bruto, valor, casas
        self.fator, self.pct, self.moeda, self.onde = fator, pct, moeda, onde

    @property
    def tem_unidade(self) -> bool:
        return bool(self.moeda or self.pct or self.fator != 1)

    def __repr__(self):
        return f"<{self.bruto!r} = {self.valor}>"


def sem_marcacao(txt: str) -> str:
    return _html.unescape(re.sub(r"<[^>]+>", " ", txt or ""))


_DATA_DDMMAAAA = re.compile(
    r"\b(?:0?[1-9]|[12][0-9]|3[01])/(?:0?[1-9]|1[0-2])/(?:19|20)\d{2}\b"
)


def numeros_do_texto(txt: str, onde: str):
    """Extrai todo número escrito, com moeda, percentual e escala.

    Data em dd/mm/aaaa sai antes da extração. Ela não é medida: nomeia QUANDO
    algo foi dito ou extraído, e nenhum script devolve o dia e o mês de uma
    conversa. O ano solto já era tratado assim em `checar_procedencia`; o dia e
    o mês escapavam e voltavam como "sem origem" — medido em 2026-11-25, uma
    atribuição de sessão datada reprovou quatro vezes, duas por parágrafo. Deixar
    como estava ensinaria a tirar a data da frase para o documento fechar limpo,
    que é perder precisão de atribuição para agradar o conferidor.
    """
    achados = []
    for m in _NUMERO.finditer(_DATA_DDMMAAAA.sub(" — ", sem_marcacao(txt))):
        moeda, cru, sufixo = m.group(1), m.group(2), (m.group(3) or "").strip().lower()
        if "," in cru:
            casas = len(cru.split(",")[1])
        else:
            casas = 0
        valor = float(cru.replace(".", "").replace(",", "."))
        pct = sufixo == "%"
        fator = 1.0 if pct or not sufixo else _MULTIPLICADOR.get(
            unicodedata.normalize("NFC", sufixo), 1.0
        )
        achados.append(
            Escrito(m.group(0).strip(), valor, casas, fator, pct, bool(moeda), onde)
        )
    return achados


# ---------------------------------------------------------------------------
# Valores apurados
# ---------------------------------------------------------------------------

def valores_da_apuracao(apuracao: dict):
    """Todo número que algum script devolveu, com o caminho até ele.

    O caminho é o que torna o achado acionável: "não casou" sem dizer contra o
    que se procurou manda o leitor conferir à mão, que é o trabalho que este
    script existe para tirar.
    """
    encontrados = []

    def anda(no, caminho):
        if isinstance(no, dict):
            for k, v in no.items():
                anda(v, f"{caminho}.{k}" if caminho else k)
        elif isinstance(no, list):
            for i, v in enumerate(no):
                anda(v, f"{caminho}[{i}]")
        elif isinstance(no, bool):
            return
        elif isinstance(no, (int, float)):
            encontrados.append((float(no), caminho))
        elif isinstance(no, str):
            # Script que devolve número como texto ("1.303.403") continua sendo
            # origem legítima: o defeito seria o dossiê inventar, não o script
            # serializar diferente.
            for m in _NUMERO.finditer(no):
                try:
                    encontrados.append(
                        (float(m.group(2).replace(".", "").replace(",", ".")), caminho)
                    )
                except ValueError:
                    pass

    for chamada in apuracao.get("chamadas", []):
        anda(chamada.get("saida"), chamada.get("script", "?"))
    return encontrados


def casa(n: Escrito, valores, tolerancia_relativa=0.0):
    """Devolve o caminho do primeiro valor apurado que explica o número escrito.

    Quatro formas de o mesmo valor aparecer no texto, todas legítimas:
    o valor cru, o valor em escala ("R$ 143,05 mi" para 143.052.398), a fração
    escrita como percentual (0,1531 para "15,31%") e o percentual já em 0–100.
    O arredondamento é sempre feito na precisão em que o autor escreveu — é isso
    que separa "3,46", que o script devolveu, de "3,5", que ninguém devolveu.
    """
    alvo = n.valor
    for v, caminho in valores:
        escala = v / n.fator if n.fator else v
        if _mesma_origem(escala, alvo, n.casas):
            return caminho, "direto" if n.fator == 1 else "em escala"
        if n.pct:
            if _mesma_origem(v * 100.0, alvo, n.casas):
                return caminho, "fração 0–1 escrita em %"
            if _mesma_origem(v, alvo, n.casas):
                return caminho, "percentual já em 0–100"
    # Ultima tentativa, e ela vale um rotulo proprio: o valor apurado e negativo
    # e o texto escreveu o modulo. Normalmente esta certo — "perde populacao a
    # 0,25% ao ano" diz a direcao em palavras e o sinal no numero seria duplo.
    # Mas e a mesma forma de um crescimento virar queda sem ninguem notar, entao
    # nao passa calado: vira conferencia, nao reprovacao.
    for v, caminho in valores:
        if v < 0 and (
            _mesma_origem(abs(v) / (n.fator or 1), alvo, n.casas)
            or (n.pct and _mesma_origem(abs(v) * 100.0, alvo, n.casas))
            or (n.pct and _mesma_origem(abs(v), alvo, n.casas))
        ):
            return caminho, "módulo de valor negativo"
    return None, ""


def _mesma_origem(valor: float, escrito: float, casas: int) -> bool:
    """O valor apurado, escrito com essa precisão, dá o número do texto?

    Aceita arredondar e truncar. A diferença entre R$ 29.893 e R$ 29.893,52 é de
    cinquenta centavos numa mediana nacional: não é número sem origem, é a
    última casa. Acusá-la enterraria o achado que importa — o valor que nenhum
    script devolveu — debaixo de divergências de centavo, e um aviso que grita
    por tudo deixa de ser lido.

    O que ele NÃO perdoa é o salto de precisão para fora da faixa: 3,46 escrito
    como "3,5" passa, porque é arredondamento legítimo; escrito como "4" ou como
    "3,40" não passa, porque nenhuma dessas é a leitura daquele valor.
    """
    fator = 10.0 ** casas
    return (
        round(valor, casas) == escrito
        or math.floor(abs(valor) * fator) / fator * (1 if valor >= 0 else -1) == escrito
    )


# ---------------------------------------------------------------------------
# Texto da narrativa
# ---------------------------------------------------------------------------

def trechos_da_narrativa(cfg: dict):
    """Pares (rótulo, texto) de tudo que o modelo escreveu no dossiê.

    Só a narrativa entra. O que `montar_relatorio.py` formata a partir das
    saídas de script não precisa ser conferido aqui: ele não pode divergir da
    apuração, porque é a apuração passada por um formatador.
    """
    saida = []
    if cfg.get("resumo"):
        saida.append(("resumo", cfg["resumo"]))
    for campo in ("leitura", "o_que_mudaria", "alertas_cadastro", "nao_sabe", "campo"):
        for i, t in enumerate(cfg.get(campo) or []):
            saida.append((f"{campo}[{i}]", t if isinstance(t, str) else json.dumps(t, ensure_ascii=False)))
    for lente, conteudo in (cfg.get("lentes") or {}).items():
        if isinstance(conteudo, dict):
            if conteudo.get("abertura"):
                saida.append((f"{lente} — abertura", conteudo["abertura"]))
            itens = conteudo.get("itens") or []
        else:
            itens = conteudo or []
        for item in itens:
            rotulo = f"{lente} — {(item.get('titulo') or '(sem título)')[:48]}"
            saida.append((rotulo, " ".join(
                str(item.get(k) or "") for k in ("titulo", "texto", "fonte")
            )))
            par = item.get("parecer")
            if isinstance(par, dict):
                txt = " ".join(str(par.get(k) or "") for k in ("porque", "referente"))
                if txt.strip():
                    saida.append((f"{rotulo} — parecer", txt))
    # A seção para o empresário é narrativa como qualquer outra: o achado que
    # motiva a pergunta cita número, e número sem origem ali é o mesmo defeito
    # que em qualquer lente — com o agravante de ser dito em voz alta.
    for i, p in enumerate(cfg.get("provocacoes_empresario") or []):
        if isinstance(p, str):
            saida.append((f"provocacoes_empresario[{i}]", p))
        elif isinstance(p, dict):
            saida.append((f"provocacoes_empresario[{i}]", " ".join(
                str(p.get(k) or "") for k in ("tema", "achado", "pergunta", "o_que_muda")
            )))
    return saida


TETO_PROVOCACOES = 15  # decisão do PM em 2026-11-27: alvo 10–15, teto 15


def checar_pareceres(cfg: dict):
    """O rótulo de bom/ruim é reconferível, então se confere.

    Duas coisas reprovam: rótulo fora dos cinco da casa, e rótulo que contradiz
    a direção do indicador na tabela (`_parecer.py`). O gerador já troca o
    rótulo pelo da tabela no HTML; o JSON com o rótulo contraditório continua
    sendo o arquivo versionado, e a próxima geração herdaria a contradição.
    Bom/Ruim para indicador FORA da tabela também reprova: sem direção
    declarada, o rótulo seria palpite.
    """
    achados = []
    for lente, conteudo in (cfg.get("lentes") or {}).items():
        itens = conteudo.get("itens", []) if isinstance(conteudo, dict) else (conteudo or [])
        for item in itens:
            par = item.get("parecer")
            if not par:
                continue
            if isinstance(par, str):
                par = {"rotulo": par}
            onde = f"{lente} — {(item.get('titulo') or '')[:48]}"
            escrito = (par.get("rotulo") or "").strip()
            chave = (par.get("indicador") or "").strip()
            if escrito and escrito not in PAR.ROTULOS:
                achados.append((onde, f"rótulo '{escrito}' fora dos cinco da casa: {', '.join(PAR.ROTULOS)}"))
                continue
            if chave in PAR.DIRECAO:
                calc = PAR.rotulo(chave, par.get("percentil"), par.get("posicao"), cfg.get("modelo"))
                if escrito and escrito != calc:
                    achados.append((onde, f"'{escrito}' contradiz a direção de '{chave}', que dá '{calc}'"))
            elif escrito in (PAR.BOM, PAR.MEDIO, PAR.RUIM):
                achados.append((onde, f"'{escrito}' para indicador fora da tabela de direção ('{chave or 'sem indicador'}')"))
    n = len([p for p in (cfg.get("provocacoes_empresario") or []) if p])
    if n > TETO_PROVOCACOES:
        achados.append(("provocacoes_empresario", f"{n} provocações — o teto é {TETO_PROVOCACOES}"))
    return achados


def numeros_estruturais(cfg: dict):
    """Números que vêm do próprio pedido, não de apuração nenhuma.

    Coordenada, raio, código do município e o número da casa no endereço são
    entrada, não medida: cobrá-los de origem apontaria o endereço do ponto como
    número sem script.
    """
    fixos = set()
    # `raio_km` e `referencia` são a entrada do relatório de prospecção, que não
    # tem ponto: o raio é premissa declarada do pedido e a referência é de onde
    # a distância é medida. Cobrar origem deles acusaria o pedido de ser número
    # sem script, como já valeria para o endereço de um dossiê de ponto.
    for chave in ("lat", "lng", "raio_principal", "raio_amplo", "raio_km", "receita_por_m2"):
        v = cfg.get(chave)
        if isinstance(v, (int, float)):
            fixos.add(abs(float(v)))
            # O mesmo raio escrito em quilômetros continua sendo o raio: "5 km"
            # e 5.000 m são o mesmo pedido, e cobrar origem do segundo e não do
            # primeiro é acusar a unidade, não o número.
            if chave.startswith("raio"):
                fixos.add(abs(float(v)) / 1000.0)
    for chave in ("codigo_ibge", "endereco", "referencia"):
        for m in _NUMERO.finditer(str(cfg.get(chave) or "")):
            try:
                fixos.add(float(m.group(2).replace(".", "").replace(",", ".")))
            except ValueError:
                pass
    return fixos


# ---------------------------------------------------------------------------
# As quatro checagens
# ---------------------------------------------------------------------------

def checar_procedencia(cfg, apuracao):
    valores = valores_da_apuracao(apuracao)
    fixos = numeros_estruturais(cfg)
    sem_origem, fracos, sinais = [], [], []
    conferidos = 0

    for onde, texto in trechos_da_narrativa(cfg):
        for n in numeros_do_texto(texto, onde):
            # Ano solto não é medida: ele nomeia a safra do dado ("Censo 2022").
            if not n.tem_unidade and n.casas == 0 and 1990 <= n.valor <= 2030:
                continue
            if n.valor in fixos or (n.valor * n.fator) in fixos:
                continue
            conferidos += 1
            caminho, forma = casa(n, valores)
            if caminho is None:
                sem_origem.append((onde, n))
            elif forma == "módulo de valor negativo":
                sinais.append((onde, n, caminho))
            elif not n.tem_unidade and n.casas == 0 and n.valor < 100:
                # Inteiro pequeno casa por acaso: há centenas deles na apuração.
                # Dizer que casou seria dar por conferido o que não foi.
                fracos.append((onde, n, caminho))
    return conferidos, sem_origem, fracos, sinais


def nomes_do_cadastro():
    """Os nomes de pessoa que o cadastro de lojas realmente contém."""
    if B is None:
        return []
    try:
        brutos = {
            (linha.get("Nome do responsável pelo GE") or "").strip()
            for linha in B.ler_cadastro_lojas()
        }
    except Exception:  # noqa: BLE001 — cadastro ausente não derruba a conferência
        return []
    # Só nome completo: um sobrenome solto bate com nome de rua e de cidade, e
    # acusar o que não é nome ensina a ignorar o aviso que importa.
    return sorted(
        n for n in brutos
        if len(n) >= 10 and len(n.split()) >= 2 and not n.isdigit()
    )


def checar_nome_de_pessoa(texto_html: str, cfg: dict, ge: str):
    achados = []
    alvo = B.normalizar(texto_html) if B else texto_html.upper()
    candidatos = list(nomes_do_cadastro())
    if ge:
        candidatos.append(ge)
    if cfg.get("ge"):
        candidatos.append(cfg["ge"])
    vistos = set()
    for nome in candidatos:
        chave = B.normalizar(nome) if B else nome.upper()
        if chave and chave not in vistos and chave in alvo:
            vistos.add(chave)
            achados.append(nome)
    if cfg.get("ge"):
        achados.append(f"(campo 'ge' preenchido no config: {cfg['ge']})")
    return achados


_PONTUACAO = (
    (r"\bscores?\b", "a régua 0–20 tem dono e vive no produto"),
    (r"\bpontua[çc][ãa]o\b", "a régua 0–20 tem dono e vive no produto"),
    (r"\b\d{1,2}\s*(?:/|de)\s*20\b", "nota na escala do produto"),
    (r"\bnota\s+(?:do|da)\s+(?:ponto|regi[ãa]o|endere[çc]o)\b", "o dossiê não pontua"),
    (r"\bponto\s+(?:aprovado|recomendado|reprovado)\b", "o dossiê não recomenda"),
    (r"\b(?:recomendamos|recomenda-se)\s+(?:abrir|a abertura)", "o dossiê não recomenda"),
    (r"\bviabilidade\s+(?:alta|m[ée]dia|baixa)\b", "é a régua com outro nome"),
    # Composição do painel de percentis, em número OU em palavras.
    #
    # O painel se recusa a emitir agregado: não há média de percentis, não há
    # contagem de dimensões "ganhas", não há tfoot. Mas a prosa alcança o que o
    # script não emite, e "lidera em três das quatro dimensões" é exatamente o
    # número composto que a decisão de produto proíbe — escrito por extenso,
    # passa por toda checagem de procedência, porque nenhum dígito é inventado.
    #
    # As duas últimas famílias são as que mais pegam: ordinal de painel e
    # contagem de dimensões. Foram a forma que o ranking tomou em 2026-11-25,
    # quando a auditoria o tirou da prosa duas vezes.
    (r"\bm[ée]dia\s+dos\s+percentis\b", "o painel não compõe"),
    (r"\bpercentil\s+m[ée]dio\b", "o painel não compõe"),
    (r"\bsoma\s+dos\s+percentis\b", "o painel não compõe"),
    (r"\b[íi]ndice\s+de\s+(?:atratividade|qualidade|potencial(?!\s+de\s+consumo))\b",
     "é a régua com outro nome"),
    (r"\b(?:melhor|pior)\s+(?:pra[çc]a|cidade|munic[íi]pio)\b", "o documento não ordena por qualidade"),
    (r"\blidera\s+em\s+(?:uma|duas|tr[êe]s|quatro|\d)\b", "contagem de dimensões é composição"),
    (r"\b(?:uma|duas|tr[êe]s|quatro|\d)\s+d(?:as|e)\s+(?:quatro|4)\s+dimens[õo]es\b", "contagem de dimensões é composição"),
    (r"\bno\s+topo\s+do\s+painel\b", "o painel é alfabético — não há topo"),
    (r"\branking\s+de\s+(?:munic[íi]pios|cidades|pra[çc]as)\b", "o documento não ranqueia"),
    # O parecer por número (2026-11-27) é permitido; somá-lo não. "Bom" e
    # "ruim" soltos passam — o que reprova é contar, saldar ou tirar maioria
    # dos pareceres, que é a nota reintroduzida por extenso. Juízo sobre o
    # ponto, a cidade, a praça, o município ou a região ("cidade boa", "o
    # ponto é ruim") é a mesma proibição e mora em checar_juizo_do_lugar.
    (r"\b(?:\d+|uma|um|dois|duas|tr[êe]s|quatro|cinco|seis|sete|oito|nove|dez|maioria\s+dos)\s+indicadores?\s+(?:s[ãa]o\s+|est[ãa]o\s+)?(?:bons|ruins|positivos|negativos|favor[áa]veis|desfavor[áa]veis)\b",
     "parecer é por número: contar pareceres é nota"),
    (r"\bsaldo\s+(?:positivo|negativo|dos\s+pareceres|dos\s+indicadores)\b", "parecer é por número: saldo é nota"),
    (r"\bmaioria\s+dos\s+(?:indicadores|pareceres)\b", "parecer é por número: maioria é nota"),
    (r"\bno\s+geral[,]?\s+(?:os\s+)?(?:indicadores|n[úu]meros)\s+(?:s[ãa]o|est[ãa]o)\s+(?:bons|ruins)\b", "parecer é por número: leitura geral é nota"),
)

_FERRAMENTA = (
    (r"\b[a-z_]{3,}\.py\b", "nome de script"),
    (r"(?<![\w-])--[a-z][a-z-]{2,}", "flag de linha de comando"),
    (r"\b[a-zA-Z_]{3,}\.(?:csv|xlsx|parquet)\b", "nome de arquivo de base"),
    (r"\b(?:fatMedio|codigo_ibge|densidadedemografica|coverageRatio)\b", "nome de campo de base"),
    (r"\b\d{4}-[A-Z]{2}_[A-Z]{2,}\b", "identificador de brick"),
)


def corpo_do_relatorio(texto_html: str) -> str:
    """O que o analista lê — sem o rodapé, onde a ferramenta pode aparecer."""
    sem_rodape = re.sub(r"<footer\b.*?</footer>", " ", texto_html, flags=re.S | re.I)
    sem_estilo = re.sub(r"<(style|script)\b.*?</\1>", " ", sem_rodape, flags=re.S | re.I)
    return sem_marcacao(sem_estilo)


# A frase que DIZ que o dossie nao pontua contem a palavra que se esta
# procurando. Sem esta guarda o verificador acusa justamente o paragrafo que o
# gerador escreve para declarar a regra — e um verificador que reprova a propria
# regra ensina a ignorar o aviso.
_NEGADO = re.compile(
    r"(?:n[ãa]o\s+(?:h[áa]|tem|traz|existe|pontua|atribui|d[áa]|julga)|sem|nem|nenhum[ao]?)"
    r"[^.;:]{0,40}$",
    re.I,
)


# Parecer é só do indicador. Frases que julgam o ponto, a cidade, a praça, o
# município ou a região como um todo ("cidade boa", "o ponto é ruim", "a praça
# é favorável") são a nota com outro nome. O conferidor pega a forma escrita;
# "A renda do município é ruim" passa, porque o juízo é do indicador.
_LUGAR = r"(?:pontos?|endere[çc]os?|cidades?|munic[íi]pios?|pra[çc]as?|regi[õo]es|regioes|regi[ãa]o)"
_JUIZO_LUGAR = (
    r"(?:bom|boa|bons|boas|ruim|ruins|"
    r"favor[áa]vel(?:es)?|desfavor[áa]vel(?:es)?|"
    r"positiv[oa]s?|negativ[oa]s?|"
    r"promissor(?:a|es)?|atrativ[oa]s?|"
    r"vi[áa]vel(?:es)?|invi[áa]vel(?:es)?|"
    r"melhor(?:es)?|pior(?:es)?)"
)
_AGREGADO_LUGAR = (
    r"(?:perfil|panorama|quadro|leitura|conjunto|saldo|veredito|veredicto|nota|placar)"
)

# "renda do município é ruim" — o juízo é do indicador, não do lugar.
_INDICADOR_ANTES_DO_LUGAR = re.compile(
    r"(?:renda|pib|ipc|ifdm|pre[çc]o|consumo|potencial|captura|densidade|"
    r"popula[çc][ãa]o|habitantes|crescimento|percentil|posi[çc][ãa]o|"
    r"n[úu]mero|indicador|valor|m[ée]dia|mediana|faixa|classes?|"
    r"faturamento|receita|share|satura[çc][ãa]o|mercado|aluguel|"
    r"credenciadas?|farm[áa]cias?|lojas?|concorrentes?|dist[âa]ncia|"
    r"fluxo|implanta[çc][ãa]o|desenvolvimento|"
    r"poder\s+de\s+compra|folga\s+competitiva|dinamismo|centralidade)"
    r"(?:[^.;:]{0,40})"
    r"\s+(?:do|da|no|na|de|em|pelo|pela|deste|desta|desse|dessa)\s+$",
    re.I,
)

_LUGAR_VERBO_JUIZO = re.compile(
    r"\b(?:(?:o|a|os|as|este|esta|estes|estas|esse|essa|esses|essas|"
    r"aquele|aquela|aqueles|aquelas|deste|desta|desse|dessa|"
    r"neste|nesta|nesse|nessa)\s+)?(?P<lugar>" + _LUGAR + r")"
    r"\s+(?:é|s[ãa]o|est[áa]|est[ãa]o|foi|foram|parece(?:m)?|saiu|sa[ií]ram|saem|"
    r"fica(?:m)?|anda(?:m)?|revela-se|mostra-se|mostrou-se|revelou-se)"
    r"\s+(?:(?:um|uma|muito|bem|bastante|pouco)\s+)*(?P<juizo>" + _JUIZO_LUGAR + r")\b",
    re.I,
)
_LUGAR_JUIZO = re.compile(
    r"\b(?P<lugar>" + _LUGAR + r")\s+(?P<juizo>" + _JUIZO_LUGAR + r")\b", re.I,
)
_JUIZO_DEPOIS_LUGAR = re.compile(
    r"\b(?P<juizo>" + _JUIZO_LUGAR + r")\s+(?P<lugar>" + _LUGAR + r")\b", re.I,
)
_E_UM_LUGAR_JUIZO = re.compile(
    r"\bé\s+uma?\s+(?:(?P<juizo1>" + _JUIZO_LUGAR + r")\s+)?(?P<lugar>" + _LUGAR + r")"
    r"(?:\s+(?P<juizo2>" + _JUIZO_LUGAR + r"))?\b",
    re.I,
)
_AGREGADO_JUIZO_DO_LUGAR = re.compile(
    r"\b" + _AGREGADO_LUGAR + r"\s+(?P<juizo>" + _JUIZO_LUGAR + r")\s+"
    r"(?:do|da|de|deste|desta|desse|dessa)\s+(?P<lugar>" + _LUGAR + r")\b",
    re.I,
)
_AGREGADO_DO_LUGAR_E_JUIZO = re.compile(
    r"\b" + _AGREGADO_LUGAR + r"\s+(?:do|da|de|deste|desta|desse|dessa)\s+(?P<lugar>" + _LUGAR + r")"
    r"\s+(?:é|est[áa]|parece|saiu|fica)\s+(?P<juizo>" + _JUIZO_LUGAR + r")\b",
    re.I,
)

_MOTIVO_JUIZO_LUGAR = (
    "parecer é só do indicador: não se julga ponto, cidade, praça, município nem região"
)


def _sem_acento(txt: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", txt.lower())
        if unicodedata.category(c) != "Mn"
    )


def _lugar_genero_numero(lugar: str) -> tuple[str, str]:
    l = _sem_acento(lugar)
    if l in {"cidades", "pracas", "regioes"}:
        return "f", "p"
    if l in {"pontos", "enderecos", "municipios"}:
        return "m", "p"
    if l in {"cidade", "praca", "regiao"}:
        return "f", "s"
    if l in {"ponto", "endereco", "municipio"}:
        return "m", "s"
    return "?", "?"


def _juizo_combina_com_lugar(juizo: str, lugar: str) -> bool:
    """Evita casar o chip 'Bom' com o indicador seguinte 'municípios que…'."""
    g, n = _lugar_genero_numero(lugar)
    j = _sem_acento(juizo)
    inv_s = {"ruim", "favoravel", "desfavoravel", "viavel", "inviavel", "melhor", "pior"}
    inv_p = {"ruins", "favoraveis", "desfavoraveis", "viaveis", "inviaveis", "melhores", "piores"}
    masc_s = {"bom", "positivo", "negativo", "promissor", "atrativo"} | inv_s
    fem_s = {"boa", "positiva", "negativa", "promissora", "atrativa"} | inv_s
    masc_p = {"bons", "positivos", "negativos", "promissores", "atrativos"} | inv_p
    fem_p = {"boas", "positivas", "negativas", "promissoras", "atrativas"} | inv_p
    if n == "s" and g == "m":
        return j in masc_s
    if n == "s" and g == "f":
        return j in fem_s
    if n == "p" and g == "m":
        return j in masc_p
    if n == "p" and g == "f":
        return j in fem_p
    return True


def checar_juizo_do_lugar(corpo: str):
    """Reprova frase que dá parecer ao ponto, à cidade, à praça ou à região."""
    achados = []
    vistos = set()
    padroes = (
        (_LUGAR_VERBO_JUIZO, False),
        (_LUGAR_JUIZO, True),
        (_JUIZO_DEPOIS_LUGAR, True),
        (_E_UM_LUGAR_JUIZO, True),
        (_AGREGADO_JUIZO_DO_LUGAR, False),
        (_AGREGADO_DO_LUGAR_E_JUIZO, False),
    )
    for pat, exige_acordo in padroes:
        for m in pat.finditer(corpo):
            gd = m.groupdict()
            juizos = [gd[k] for k in ("juizo", "juizo1", "juizo2") if gd.get(k)]
            if pat is _E_UM_LUGAR_JUIZO and not juizos:
                continue
            lugar = gd.get("lugar") or ""
            if exige_acordo and lugar and juizos and not any(
                _juizo_combina_com_lugar(j, lugar) for j in juizos
            ):
                continue
            inicio, fim = max(0, m.start() - 60), min(len(corpo), m.end() + 60)
            prefixo = corpo[inicio:m.start()]
            if _NEGADO.search(prefixo):
                continue
            if _INDICADOR_ANTES_DO_LUGAR.search(corpo[max(0, m.start() - 80):m.start()]):
                continue
            chave = (m.start(), m.group(0).lower())
            if chave in vistos:
                continue
            vistos.add(chave)
            contexto = re.sub(r"\s+", " ", corpo[inicio:fim]).strip()
            achados.append((m.group(0), _MOTIVO_JUIZO_LUGAR, contexto))
    return achados


def checar_padroes(corpo: str, padroes, respeitar_negacao=False):
    achados = []
    for padrao, porque in padroes:
        for m in re.finditer(padrao, corpo, re.I):
            inicio, fim = max(0, m.start() - 60), min(len(corpo), m.end() + 60)
            if respeitar_negacao and _NEGADO.search(corpo[inicio:m.start()]):
                continue
            contexto = re.sub(r"\s+", " ", corpo[inicio:fim]).strip()
            achados.append((m.group(0), porque, contexto))
    return achados


# ---------------------------------------------------------------------------
# Relato
# ---------------------------------------------------------------------------

def main() -> int:
    # Mesma causa que derrubava o gate: no Windows a stdout sai em cp1252, que
    # não tem "←" nem "→" — e este relatório usa os dois para apontar o valor
    # apurado que explica cada número. A conferência quebrava DEPOIS de achar
    # os problemas, imprimindo meio relatório e um traceback no lugar do
    # veredito. Quem roda a conferência roda da linha de comando, sem -X utf8.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--config", required=True, help="JSON da narrativa do dossiê")
    ap.add_argument("--relatorio", required=True, help="HTML gerado")
    ap.add_argument("--apuracao", default="", help="padrão: ao lado do relatório")
    ap.add_argument("--ge", default="", help="responsável usado na geração, para conferir se vazou")
    ap.add_argument("--json", action="store_true", help="saída estruturada")
    args = ap.parse_args()

    with open(args.config, encoding="utf-8") as fh:
        cfg = json.load(fh)
    with open(args.relatorio, encoding="utf-8") as fh:
        pagina = fh.read()

    caminho_apuracao = args.apuracao or (
        re.sub(r"\.html?$", "", args.relatorio) + ".apuracao.json"
    )
    if not os.path.exists(caminho_apuracao):
        print(
            "ERRO: apuração não encontrada em " + caminho_apuracao + ".\n"
            "Ela é gravada por montar_relatorio.py junto com o HTML. Sem ela não "
            "há contra o que conferir procedência, e conferir contra nada passa "
            "por conferência sem ser uma. Regere o relatório.",
            file=sys.stderr,
        )
        return 2
    with open(caminho_apuracao, encoding="utf-8") as fh:
        apuracao = json.load(fh)

    conferidos, sem_origem, fracos, sinais = checar_procedencia(cfg, apuracao)
    corpo = corpo_do_relatorio(pagina)
    nomes = checar_nome_de_pessoa(corpo, cfg, args.ge)
    pontuacao = checar_padroes(corpo, _PONTUACAO, respeitar_negacao=True)
    pontuacao.extend(checar_juizo_do_lugar(corpo))
    ferramenta = checar_padroes(corpo, _FERRAMENTA)
    pareceres = checar_pareceres(cfg)

    reprova = len(sem_origem) + len(nomes) + len(pontuacao) + len(ferramenta) + len(pareceres)

    if args.json:
        json.dump(
            {
                "numeros_conferidos": conferidos,
                "sem_origem": [
                    {"onde": o, "escrito": n.bruto, "valor": n.valor} for o, n in sem_origem
                ],
                "escrito_em_modulo": [
                    {"onde": o, "escrito": n.bruto, "casou_com": c} for o, n, c in sinais
                ],
                "casamento_fraco": [
                    {"onde": o, "escrito": n.bruto, "casou_com": c} for o, n, c in fracos
                ],
                "nome_de_pessoa": nomes,
                "pontuacao": [{"trecho": a, "porque": p} for a, p, _ in pontuacao],
                "ferramenta_no_corpo": [{"trecho": a, "tipo": p} for a, p, _ in ferramenta],
                "parecer_e_provocacoes": [{"onde": o, "porque": p} for o, p in pareceres],
                "reprovados": reprova,
            },
            sys.stdout, ensure_ascii=False, indent=1,
        )
        print()
        return 1 if reprova else 0

    larg = 78
    print("=" * larg)
    print("CONFERÊNCIA MECÂNICA — " + os.path.basename(args.relatorio))
    print("=" * larg)
    print(
        f"{len(apuracao.get('chamadas', []))} chamada(s) de script na apuração · "
        f"{len(valores_da_apuracao(apuracao)):,} valores apurados · "
        f"{conferidos} número(s) da narrativa conferidos".replace(",", ".")
    )
    print()

    print(f"1. PROCEDÊNCIA DOS NÚMEROS — {len(sem_origem)} sem origem")
    if sem_origem:
        for onde, n in sem_origem:
            print(f"   REPROVA  {n.bruto:>18}  em {onde}")
        print("   Nenhuma saída de script devolve esses valores, em nenhuma escala")
        print("   nem precisão. Ou o número foi calculado na narrativa, ou foi")
        print("   arredondado para longe do que o script devolveu.")
    else:
        print("   Todo número da narrativa tem um valor apurado que o explica.")
    print()

    if sinais:
        print(f"2. SINAL — {len(sinais)} valor(es) escritos em módulo")
        for onde, n, caminho in sinais:
            print(f"   confira  {n.bruto:>18}  em {onde}  ← {caminho}")
        print("   O valor apurado é negativo e o texto escreve o módulo. Em geral")
        print("   está certo (a direção vai em palavras: \"perde população a 0,25%\"),")
        print("   mas é por aqui que uma queda vira crescimento sem ninguém notar.")
        print()

    if fracos:
        print(f"3. CASAMENTO FRACO — {len(fracos)} inteiro(s) pequeno(s)")
        for onde, n, caminho in fracos:
            print(f"   confira  {n.bruto:>18}  em {onde}  ← {caminho}")
        print("   Inteiro pequeno sem unidade casa por acaso: a apuração tem")
        print("   centenas deles. Casou, mas isso não é conferência — olhe se o")
        print("   caminho indicado é mesmo o que a frase está afirmando.")
        print()

    print(f"4. NOME DE PESSOA NO ENTREGÁVEL — {len(nomes)} achado(s)")
    if nomes:
        for n in nomes:
            print(f"   REPROVA  {n}")
        print("   As bases trazem dado pessoal (LGPD) e nome de pessoa não entra")
        print("   em entregável. O responsável pelo GE serve ao gate e para aí.")
    elif B is None:
        print("   Não conferido: o cadastro de lojas não pôde ser lido.")
    else:
        print("   Nenhum dos nomes do cadastro de lojas aparece no corpo.")
    print()

    print(f"5. PONTUAÇÃO — {len(pontuacao)} achado(s)")
    for trecho, porque, contexto in pontuacao:
        print(f"   REPROVA  {trecho!r} — {porque}")
        print(f"            …{contexto}…")
    if not pontuacao:
        print("   O dossiê não pontua, não nota, não recomenda, não soma pareceres")
        print("   e não julga o ponto, a cidade, a praça, o município nem a região.")
    print()

    print(f"6. FERRAMENTA NO CORPO — {len(ferramenta)} achado(s)")
    for trecho, tipo, contexto in ferramenta:
        print(f"   REPROVA  {trecho!r} — {tipo}")
        print(f"            …{contexto}…")
    if not ferramenta:
        print("   O corpo cita fonte de dado, não ferramenta.")
    print()

    n_prov = len([p for p in (cfg.get("provocacoes_empresario") or []) if p])
    print(f"7. PARECER POR NÚMERO E PROVOCAÇÕES — {len(pareceres)} achado(s) · {n_prov} provocação(ões) ao empresário")
    for onde, porque in pareceres:
        print(f"   REPROVA  {onde} — {porque}")
    if not pareceres:
        print("   Todo rótulo de parecer bate com a direção da tabela da casa, e as")
        print(f"   provocações estão dentro do teto de {TETO_PROVOCACOES}.")
    print()

    print("-" * larg)
    if reprova:
        print(f"{reprova} reprovação(ões). O dossiê não deve sair assim.")
    else:
        print("Nada reprovado na parte mecânica.")
    print(
        "Isto é metade da auditoria. A outra metade — a lente fala da região ou\n"
        "da medição, o item passa no teste do \"e daí?\", duas medidas foram\n"
        "pareadas como se fossem a mesma — exige leitura e continua com o\n"
        "auditor."
    )
    return 1 if reprova else 0


if __name__ == "__main__":
    raise SystemExit(main())
