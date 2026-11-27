"""Monta o resumo de fechamento que o analista lê ANTES de autorizar o dossiê.

Uso:
    python resumo_fechamento.py --config narrativa.json --saida resumo.html

Por que existe
--------------
A skill /orbita pergunta "gero o dossiê?" no fim da Fase C. Perguntar isso sem
mostrar o que foi montado faz o analista decidir no escuro, logo depois do turno
mais denso da conversa. Este script renderiza, a partir da MESMA narrativa que
vai virar o dossiê, o que o documento vai afirmar, o que ele não vai saber e o
que fica para campo — mais as perguntas cuja resposta ainda mudaria o texto.

A divisão da casa continua valendo, e é o motivo de isto ser script e não prosa:

    número  -> script          (este arquivo só reorganiza o que está no JSON)
    texto   -> modelo          (nunca inventa número)

Todo número do resumo é, por construção, um número que já está na narrativa —
que é o que `verificar_dossie.py` confere depois. Resumo escrito à mão fica fora
desse alcance, e foi por isso que virou script.

Campos lidos de `--config`
--------------------------
Os mesmos da narrativa do dossiê, mais dois que só o resumo usa:

    "resumo_gate":      "frase única com o veredito do gate e a regra citada"
    "resumo_perguntas": [{"titulo": "...", "texto": "..."}]

`provocacoes_empresario` (o mesmo campo que o dossiê usa) sai aqui também, em
"O que vai para a conversa com o empresário": o analista aprova o roteiro antes
de levá-lo. E cada item de lente com `parecer` mostra o rótulo — calculado pela
tabela de direção da casa, igual ao dossiê. O rótulo é do indicador, nunca
do ponto ou da cidade.

`resumo_perguntas` é a seção que justifica o resumo existir: as outras descrevem,
essa convida. Sem ela o script avisa, porque um resumo que só descreve devolve o
mesmo "pode gerar" por cansaço que ele existe para evitar.

Os dois campos são ignorados por `montar_relatorio.py`.

O que o resumo NÃO é
--------------------
Não é o entregável e não pode parecer um. Ele sai marcado como pré-leitura, sem
a seção de Fontes e sem ter passado pela conferência nem pelo auditor — por isso
a faixa no topo e o rodapé dizem isso com todas as letras. O entregável é o HTML
que `montar_relatorio.py` gera.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _parecer as PAR  # noqa: E402

ORDEM_LENTES = ["Forças", "Fragilidades", "Oportunidades", "Dificuldades"]

# Cor por lente, na mesma família do relatório — o quadrante se lê pela posição,
# e a cor só reforça o par (a favor / contra).
COR_LENTE = {
    "Forças": "#0f7b45",
    "Fragilidades": "#b4503c",
    "Oportunidades": "#1a5fb4",
    "Dificuldades": "#8b3a62",
}

CSS = """
:root{
  --roxo:#5b2a8c; --texto:#1d1b22; --fraco:#6c6878; --linha:#e3e1e8;
  --fundo:#faf9fc; --papel:#ffffff;
  --rascunho:#8a5a00; --rascunho-fundo:#fdf3e8; --rascunho-linha:#e8c99a;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --texto:#ece9f2; --fraco:#a9a4b5; --linha:#35323d;
    --fundo:#17151c; --papel:#201d26; --roxo:#c4a2ef;
    --rascunho:#e8b765; --rascunho-fundo:#2a2113; --rascunho-linha:#5c4824;
  }
}
*{box-sizing:border-box}
body{margin:0;background:var(--fundo);color:var(--texto);
 font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}
.wrap{max-width:820px;margin:0 auto;padding:0 16px 56px}

.faixa{background:var(--rascunho-fundo);border:1px dashed var(--rascunho-linha);
 border-radius:8px;padding:10px 14px;margin:20px 0 22px;display:flex;gap:12px;
 align-items:baseline;flex-wrap:wrap}
.faixa .tag{font:600 11px/1 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
 letter-spacing:.12em;text-transform:uppercase;color:var(--rascunho);white-space:nowrap}
.faixa .txt{color:var(--rascunho);font-size:13.5px}

h1{font-size:23px;line-height:1.25;margin:0 0 6px;letter-spacing:-.015em}
.local{color:var(--fraco);font-size:14px;margin:0 0 20px}

.ficha{background:var(--papel);border:1px solid var(--linha);border-radius:10px;
 padding:14px 16px;margin:0 0 26px}
.ficha dl{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;margin:0}
.ficha dt{font:600 11px/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
 letter-spacing:.08em;text-transform:uppercase;color:var(--fraco);white-space:nowrap}
.ficha dd{margin:0}

h2{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--fraco);
 margin:30px 0 12px;font-weight:600}
h2 .n{color:var(--texto);font-weight:700}

.quad{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media (max-width:640px){.quad{grid-template-columns:1fr}}
.lente{background:var(--papel);border:1px solid var(--linha);border-radius:10px;
 padding:12px 14px;border-top:3px solid var(--c)}
.lente h3{margin:0 0 8px;font-size:13px;letter-spacing:.02em;color:var(--c)}
.lente h3 .c{color:var(--fraco);font-weight:500}
.lente ul{margin:0;padding-left:17px}
.lente li{margin:0 0 6px}
.lente li:last-child{margin-bottom:0}
.vazia{color:var(--fraco);font-style:italic;margin:0}

.linhas{background:var(--papel);border:1px solid var(--linha);border-radius:10px;
 padding:12px 16px}
.linhas ul{margin:0;padding-left:17px}
.linhas li{margin:0 0 6px}
.linhas li:last-child{margin-bottom:0}

.perg{border-left:3px solid var(--roxo);background:var(--papel);
 border-radius:0 10px 10px 0;padding:12px 16px;margin:0 0 10px}
.perg .t{font-weight:600;display:block;margin-bottom:4px}
.perg .d{color:var(--fraco);font-size:14px}
.parecer{font-size:12px;color:var(--fraco);font-weight:600}
.sem-perg{border-left:3px dashed var(--rascunho-linha);background:var(--rascunho-fundo);
 color:var(--rascunho);border-radius:0 10px 10px 0;padding:12px 16px;font-size:14px}

footer{margin-top:34px;padding-top:14px;border-top:1px solid var(--linha);
 color:var(--fraco);font-size:12.5px}
"""


def e(x) -> str:
    return html.escape(str(x if x is not None else ""))


def primeira_frase(t: str) -> str:
    """A primeira frase da lacuna é o que ela é; o resto é por que importa e o
    que destravaria, que o dossiê traz inteiro."""
    t = (t or "").strip()
    m = re.search(r"^(.+?[.!?])(\s|$)", t)
    s = m.group(1) if m else t
    return s[:-1] if s.endswith(".") else s


def bloco_lentes(lentes: dict, modelo=None) -> str:
    out = ['<div class="quad">']
    for nome in ORDEM_LENTES:
        l = lentes.get(nome) or {}
        itens = l.get("itens") or []
        cor = COR_LENTE.get(nome, "#5b2a8c")
        out.append(f'<section class="lente" style="--c:{cor}">')
        out.append(f'<h3>{e(nome)} <span class="c">({len(itens)})</span></h3>')
        if itens:
            out.append("<ul>")
            for i in itens:
                out.append(f'<li>{e(i.get("titulo"))}{_rotulo_do_item(i, modelo)}</li>')
            out.append("</ul>")
        else:
            out.append('<p class="vazia">Sem item nesta lente.</p>')
        out.append("</section>")
    out.append("</div>")
    return "\n".join(out)


def _rotulo_do_item(item: dict, modelo=None) -> str:
    par = item.get("parecer")
    if not par:
        return ""
    if isinstance(par, str):
        par = {"rotulo": par}
    chave = (par.get("indicador") or "").strip()
    if chave in PAR.DIRECAO:
        r = PAR.rotulo(chave, par.get("percentil"), par.get("posicao"), modelo)
    else:
        r = par.get("rotulo") if par.get("rotulo") in (PAR.AMBIGUO, PAR.SEM_REFERENCIA) else PAR.SEM_REFERENCIA
    return f' <span class="parecer">[{e(r)}]</span>'


def bloco_provocacoes(provs) -> str:
    provs = [p for p in (provs or []) if p]
    cab = f'<h2>O que vai para a conversa com o empresário <span class="n">({len(provs)})</span></h2>'
    if not provs:
        return cab + (
            '<div class="sem-perg">A narrativa não traz provocações ao empresário. '
            "O que o analista não sabe responder — história da praça, concorrência "
            "vista de dentro, intenção do empresário — some do documento sem elas.</div>"
        )
    out = [cab]
    for p in provs:
        if isinstance(p, str):
            out.append(f'<div class="perg"><span class="t">{e(p)}</span></div>')
            continue
        out.append(
            '<div class="perg">'
            f'<span class="t">{e(p.get("pergunta"))}</span>'
            f'<span class="d">{e(p.get("achado"))}</span>'
            "</div>"
        )
    return "\n".join(out)


def bloco_lista(titulo: str, itens, vazio: str) -> str:
    itens = itens or []
    cab = f'<h2>{e(titulo)} <span class="n">({len(itens)})</span></h2>'
    if not itens:
        return cab + f'<div class="linhas"><p class="vazia">{e(vazio)}</p></div>'
    li = "\n".join(f"<li>{e(primeira_frase(x))}</li>" for x in itens)
    return cab + f'<div class="linhas"><ul>{li}</ul></div>'


def bloco_perguntas(perguntas) -> str:
    cab = "<h2>Onde ainda cabe pergunta</h2>"
    if not perguntas:
        return cab + (
            '<div class="sem-perg">A narrativa não declarou nenhuma pergunta em '
            "aberto. Um resumo que só descreve devolve o mesmo “pode gerar” por "
            "cansaço que ele existe para evitar — reveja se nenhuma lacuna teria "
            "resposta capaz de mudar o documento.</div>"
        )
    out = [cab]
    for p in perguntas:
        if isinstance(p, str):
            out.append(f'<div class="perg"><span class="t">{e(p)}</span></div>')
            continue
        out.append(
            '<div class="perg">'
            f'<span class="t">{e(p.get("titulo"))}</span>'
            f'<span class="d">{e(p.get("texto"))}</span>'
            "</div>"
        )
    return "\n".join(out)


def montar(cfg: dict) -> str:
    municipio = cfg.get("municipio") or ""
    uf = cfg.get("uf") or ""
    local = " · ".join(x for x in [municipio and f"{municipio}/{uf}", cfg.get("codigo_ibge") and f"IBGE {cfg['codigo_ibge']}"] if x)

    perfil = {"novo": "empresário novo", "existente": "já associado"}.get(
        (cfg.get("perfil") or "").strip(), cfg.get("perfil") or "—"
    )
    ficha = [
        ("Gate", cfg.get("resumo_gate") or "veredito não declarado na narrativa"),
        ("Solicitante", perfil),
        ("Bandeira", cfg.get("bandeira") or "a decidir"),
        ("Modelo", cfg.get("modelo") or "a decidir"),
        ("Raio", f'{cfg.get("raio_principal", "—")} m'),
    ]
    dl = "\n".join(f"<dt>{e(k)}</dt><dd>{e(v)}</dd>" for k, v in ficha)

    if cfg.get("lentes"):
        miolo = "<h2>O que o dossiê vai afirmar</h2>" + bloco_lentes(cfg["lentes"], cfg.get("modelo"))
    else:
        # Gate em impedimento ou lista de praças: não há quadrante.
        partes = []
        for campo, rotulo in (
            ("leitura", "A leitura"),
            ("o_que_mudaria", "O que mudaria"),
            ("alertas_cadastro", "Alertas de cadastro"),
        ):
            if cfg.get(campo):
                partes.append(bloco_lista(rotulo, cfg[campo], "—"))
        miolo = "\n".join(partes) or "<h2>Sem lentes nesta narrativa</h2>"

    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Antes de gerar — {e(cfg.get('endereco'))}</title>
<style>{CSS}</style></head><body><div class="wrap">

<div class="faixa">
  <span class="tag">Pré-leitura</span>
  <span class="txt">Isto não é o relatório. É o que a narrativa vai virar, para
  você conferir antes de autorizar. Número só vale no dossiê, que ainda passa
  pela conferência mecânica e pelo auditor de evidência.</span>
</div>

<h1>{e(cfg.get('endereco') or 'Ponto sem endereço declarado')}</h1>
<p class="local">{e(local)}</p>

<div class="ficha"><dl>{dl}</dl></div>

{miolo}

{bloco_lista("O que o dossiê NÃO vai saber", cfg.get("nao_sabe"), "Nenhuma lacuna declarada — o que, num dossiê de ponto, é sinal de que faltou declarar.")}

{bloco_lista("O que fica para confirmar em campo", cfg.get("campo"), "Nenhum item de campo declarado.")}

{bloco_provocacoes(cfg.get("provocacoes_empresario"))}

{bloco_perguntas(cfg.get("resumo_perguntas"))}

<footer>Pré-leitura montada a partir da narrativa do dossiê. As lacunas aparecem
aqui pela primeira frase; o documento traz cada uma inteira, com o que falta, por
que importa neste ponto e o que destravaria.</footer>

</div></body></html>
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="JSON da narrativa do dossiê")
    ap.add_argument("--saida", required=True, help="caminho do HTML de saída")
    a = ap.parse_args()

    with open(a.config, encoding="utf-8") as f:
        cfg = json.load(f)

    if not cfg.get("resumo_gate"):
        print("AVISO: narrativa sem `resumo_gate` — o resumo sai sem o veredito "
              "do gate, que é a primeira coisa que o analista procura.", file=sys.stderr)
    if not cfg.get("resumo_perguntas"):
        print("AVISO: narrativa sem `resumo_perguntas` — a seção que convida o "
              "analista a perguntar sai vazia, e o resumo vira só descrição.",
              file=sys.stderr)

    destino = os.path.abspath(a.saida)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8", newline="\n") as f:
        f.write(montar(cfg))

    print(f"resumo gravado: {a.saida} ({os.path.getsize(destino):,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
