"""Converte o cadastro de lojas (.xlsx) para CSV, uma vez.

Uso (rodar a partir da raiz do projeto, SEM -I, porque precisa de openpyxl):
    python .claude/skills/analise-regiao-farmarcas/scripts/preparar_cadastro_lojas.py

Por que existe: `openpyxl` está no site-packages de usuário e não é visível sob
`python -I`, que é como os scripts de análise rodam. Em vez de afrouxar o
isolamento de todo mundo, convertemos uma vez e os scripts de análise leem CSV
com a biblioteca padrão.

Saída: `cache/cadastro_lojas.csv` dentro da pasta da skill (fora do git), mais
`cache/cadastro_lojas.meta.json` com a data da exportação e o arquivo de origem.
Rodar de novo sempre que o cadastro for reexportado.

Por que a escolha do arquivo é exigente, e não "o mais recente que achar":
medido em 2026-11-25, o cache em uso tinha 2.808 lojas (exportação de 10/11,
passada à mão como argumento) enquanto o arquivo mais novo na pasta das bases
era o de 23/10, com 2.804 e SEM a coluna `Grupo Econômico`. Rodar o comando
documentado, sem argumento, rebaixaria o cache em 18 dias e perderia a coluna —
e a data do cadastro, escrita à mão em `_bases.py`, continuaria anunciando
10/11. Erro silencioso, do tipo que o próprio dossiê existe para evitar. Agora
o conversor procura a exportação mais recente que tenha TODAS as colunas
exigidas, e aborta dizendo o que falta em vez de aceitar a velha.
"""

from __future__ import annotations

import csv
import datetime
import json
import os
import re
import sys

COLUNAS = [
    "Id",
    "Data de Inauguração",
    "Rede",
    "Razão Social",
    "Nome Fantasia",
    "CNPJ",
    "Bandeira",
    "Modelo de Negócio",
    "Tipo",
    "Status",
    "Situação",
    "Data de Desativação",
    "Cidade - Endereço Receita",
    "Estado - Endereço Receita",
    "Bairro - Endereço Receita",
    "Latitude - Endereço Receita",
    "Longitude - Endereço Receita",
    # Cidade do endereço POPULAR, só cidade e estado. A contagem de lojas por
    # praça usa o endereço da Receita, que é fiscal; quando o popular aponta
    # para outro município, a loja pode estar contada na praça errada — nos dois
    # sentidos. Medido em 2026-11-25: 60 das 1.934 lojas ativas divergiam.
    # Logradouro, CEP, número e coordenada do popular NÃO entram: coluna que
    # chega e não é consumida vira dívida.
    "Cidade - Endereço Popular",
    "Estado - Endereço Popular",
    # Identificador numérico do grupo econômico. É a chave de contagem do teto
    # de zoneamento. Até 2026-11-25 o grupo era deduplicado pelo NOME do
    # responsável, que é dado pessoal e quebra com grafia divergente — duas
    # lojas do mesmo dono escritas de dois jeitos viravam dois grupos, e um
    # grupo a mais barra um pedido que caberia. O id não tem esse modo de falha.
    "Grupo Econômico",
    "Nome do responsável pelo GE",
]

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "cache", "cadastro_lojas.csv")
META = os.path.join(AQUI, "cache", "cadastro_lojas.meta.json")

# relatorio-lojas-DD_MM_AAAA_HH_MM_SS.xlsx
_NOME = re.compile(r"relatorio-lojas-(\d{2})_(\d{2})_(\d{4})_(\d{2})_(\d{2})_(\d{2})\.xlsx$", re.I)


def data_da_exportacao(caminho: str):
    """Data no nome do arquivo, como AAAA-MM-DD. É ela que o relatório carimba."""
    m = _NOME.search(os.path.basename(caminho))
    if not m:
        return None
    d, mes, a = m.group(1), m.group(2), m.group(3)
    try:
        return datetime.date(int(a), int(mes), int(d)).isoformat()
    except ValueError:
        return None


def _colunas_do_xlsx(caminho: str, openpyxl) -> list:
    wb = openpyxl.load_workbook(caminho, read_only=True)
    try:
        ws = wb[wb.sheetnames[0]]
        for linha in ws.iter_rows(min_row=1, max_row=1, values_only=True):
            return [c for c in linha]
        return []
    finally:
        wb.close()


def achar_xlsx(base_dir: str, openpyxl) -> str:
    """A exportação mais recente que tenha TODAS as colunas exigidas.

    Procura na pasta das bases e também na pasta acima dela, porque é comum a
    exportação nova cair no Downloads e nunca ser movida — foi exatamente assim
    que o cache ficou mais novo que o arquivo da pasta oficial.
    """
    import glob

    pastas = [base_dir]
    acima = os.path.dirname(base_dir.rstrip("\\/"))
    if acima and os.path.isdir(acima) and acima not in pastas:
        pastas.append(acima)

    hits = []
    for pasta in pastas:
        hits.extend(glob.glob(os.path.join(pasta, "relatorio-lojas-*.xlsx")))
    if not hits:
        raise FileNotFoundError(f"nenhum relatorio-lojas-*.xlsx em {pastas!r}")

    # Mais recente primeiro, pela data do NOME — não pelo mtime, que muda ao
    # copiar o arquivo e já fez a ordenação mentir.
    hits.sort(key=lambda p: (data_da_exportacao(p) or "", os.path.basename(p)), reverse=True)

    recusados = []
    for caminho in hits:
        try:
            colunas = _colunas_do_xlsx(caminho, openpyxl)
        except Exception as e:  # arquivo aberto no Excel, corrompido, etc.
            recusados.append(f"  {os.path.basename(caminho)}: não abriu ({type(e).__name__})")
            continue
        faltando = [c for c in COLUNAS if c not in colunas]
        if not faltando:
            return caminho
        recusados.append(f"  {os.path.basename(caminho)}: sem {faltando}")

    raise SystemExit(
        "nenhuma exportação de lojas tem todas as colunas exigidas.\n"
        + "\n".join(recusados[:10])
        + "\n\nExporte o relatório de lojas novamente, com a coluna 'Grupo Econômico',"
        "\nou passe o arquivo certo como argumento."
    )


def main() -> int:
    try:
        import openpyxl
    except ImportError:
        print(
            "openpyxl não encontrado. Rode SEM a flag -I, ou instale com:\n"
            "    python -m pip install --user openpyxl",
            file=sys.stderr,
        )
        return 1

    base_dir = os.environ.get("ORBITA_BASES", r"C:\Users\zequi\Downloads\bases órbita")
    caminho = sys.argv[1] if len(sys.argv) > 1 else achar_xlsx(base_dir, openpyxl)

    wb = openpyxl.load_workbook(caminho, read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]
    linhas = ws.iter_rows(values_only=True)
    cabecalho = next(linhas)
    indice = {nome: i for i, nome in enumerate(cabecalho)}

    faltando = [c for c in COLUNAS if c not in indice]
    if faltando:
        print(f"colunas ausentes no xlsx: {faltando}", file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    total = 0
    with open(SAIDA, "w", encoding="utf-8", newline="") as fh:
        escritor = csv.writer(fh)
        escritor.writerow(COLUNAS)
        for linha in linhas:
            if linha is None or all(v is None for v in linha):
                continue
            escritor.writerow(
                ["" if linha[indice[c]] is None else str(linha[indice[c]]).strip() for c in COLUNAS]
            )
            total += 1

    # A data do cadastro sai do NOME do arquivo e vai para o lado do CSV. Ela
    # era literal em `_bases.py`: reexportar o cadastro sem editar a constante
    # fazia todo relatório carimbar data velha, e foi o que aconteceu — o cache
    # era de 10/11 e o comando documentado teria trazido o de 23/10 por cima,
    # com a constante intacta.
    data = data_da_exportacao(caminho)
    with open(META, "w", encoding="utf-8") as fh:
        json.dump(
            {
                "data_do_cadastro": data,
                "origem": os.path.basename(caminho),
                "lojas": total,
                "_leitura": "data lida do nome do arquivo de exportação; é ela que os relatórios carimbam",
            },
            fh,
            ensure_ascii=False,
            indent=2,
        )

    print(f"origem : {caminho}")
    print(f"destino: {SAIDA}")
    print(f"lojas  : {total}")
    print(f"data   : {data or 'NÃO RECONHECIDA no nome do arquivo'}")
    if not data:
        print(
            "AVISO: sem data no nome do arquivo, os relatórios voltam a usar a data literal "
            "de _bases.py, que pode estar velha.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
