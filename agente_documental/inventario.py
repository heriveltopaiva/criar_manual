import csv
from pathlib import Path

PASTA_VAULT = Path("/home/herivelto-paiva/Obsidian Vault")
PASTAS_PERMITIDAS = ("Inbox", "Knowledge", "Reference", "Pesquisa", "Projects", "Zettelkasten")
ARQUIVO_SAIDA = Path(__file__).parent / "historico" / "inventario.csv"


def ler_cabecalho(texto):
    if not texto.startswith("---"):
        return None
    partes = texto.split("---", 2)
    if len(partes) < 3:
        return None
    campos = {}
    for linha in partes[1].splitlines():
        nome, separador, valor = linha.partition(":")
        if separador:
            campos[nome.strip().lower()] = valor.strip()
    return campos


def descrever_nota(nota, pasta):
    texto = nota.read_text(encoding="utf-8", errors="replace")
    cabecalho = ler_cabecalho(texto)
    return {
        "caminho": str(nota.relative_to(PASTA_VAULT)),
        "pasta": pasta,
        "tem_cabecalho": "sim" if cabecalho is not None else "não",
        "tipo": (cabecalho or {}).get("tipo", ""),
        "palavras": len(texto.split()),
    }


if __name__ == "__main__":
    linhas = []
    for nota in sorted(PASTA_VAULT.glob("*.md")):
        linhas.append(descrever_nota(nota, "(raiz)"))
    for pasta in PASTAS_PERMITIDAS:
        for nota in sorted((PASTA_VAULT / pasta).rglob("*.md")):
            linhas.append(descrever_nota(nota, pasta))

    with ARQUIVO_SAIDA.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(linhas[0].keys()))
        escritor.writeheader()
        escritor.writerows(linhas)

    com_cabecalho = sum(1 for l in linhas if l["tem_cabecalho"] == "sim")
    com_tipo = sum(1 for l in linhas if l["tipo"])
    print(f"Notas analisadas: {len(linhas)}")
    print(f"Com cabeçalho:    {com_cabecalho}")
    print(f"Com tipo:         {com_tipo}")
    for pasta in ("(raiz)",) + PASTAS_PERMITIDAS:
        total = sum(1 for l in linhas if l["pasta"] == pasta)
        print(f"  {pasta:<14} {total}")
    print(f"Planilha salva em: {ARQUIVO_SAIDA}")