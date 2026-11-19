import shutil
from pathlib import Path

PASTA_TEMPLATES = Path("/home/herivelto-paiva/Obsidian Vault/Templates")
PASTA_BACKUP = Path(__file__).parent / "historico" / "templates_backup"

TIPOS = {
    "01 Conhecimento.md": "conhecimento",
    "02 Decisao.md": "decisao",
    "03 Estrutura.md": "estrutura",
    "04 Ideia.md": "ideia",
    "05 Inbox.md": "inbox",
    "06 MOC.md": "moc",
    "07 Pesquisa.md": "pesquisa",
    "08 Projeto.md": "projeto",
    "09 Referencia.md": "referencia",
    "10 Estudo.md": "estudo",
}

if not PASTA_BACKUP.exists():
    shutil.copytree(PASTA_TEMPLATES, PASTA_BACKUP)
    print(f"Backup criado em: {PASTA_BACKUP}")

for nome, tipo in TIPOS.items():
    arquivo = PASTA_TEMPLATES / nome
    texto = arquivo.read_text(encoding="utf-8")

    if "origem:" in texto:
        print(f"já corrigido, pulei: {nome}")
        continue

    novas_linhas = []
    for linha in texto.split("\n"):
        if linha.startswith("tipo:"):
            novas_linhas.append(f"tipo: {tipo}")
        elif linha.startswith("topic:"):
            novas_linhas.append(linha)
            if nome == "10 Estudo.md":
                novas_linhas.append("status: em andamento")
            novas_linhas.append("origem: ")
        else:
            novas_linhas.append(linha)
    texto = "\n".join(novas_linhas)

    if nome == "10 Estudo.md":
        texto = texto.replace("\n---\nstatus: em andamento\n---\n", "\n", 1)
    if nome == "03 Estrutura.md" and texto.count("```") % 2 == 1:
        texto = texto.rstrip("\n") + "\n```\n"
    if nome == "08 Projeto.md":
        texto = texto.replace("## Implementação", "## Ideias\n\n- \n\n## Implementação", 1)

    arquivo.write_text(texto, encoding="utf-8")
    print(f"corrigido: {nome}")