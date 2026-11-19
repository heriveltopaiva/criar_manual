import json
import unicodedata                      # NOVO
from pathlib import Path

import ollama

PASTA_BASE = Path(__file__).parent
PASTA_ENTRADA = PASTA_BASE / "entrada"
PASTA_VAULT = PASTA_BASE / "vault_teste"   # NOVO
ARQUIVO_INSTRUCOES = PASTA_BASE / "instrucoes.md"
EXTENSOES_ACEITAS = (".md", ".txt")
MODELO = "gemma4:12b"
TIPOS = ["conhecimento", "referencia", "estudo", "pesquisa", "ideia", "decisao", "projeto"]

LISTA_DE_TEXTOS = {"type": "array", "items": {"type": "string"}}

ESQUEMA_CLASSIFICACAO = {
    "type": "object",
    "properties": {
        "tipo": {"type": "string", "enum": TIPOS},
        "assuntos": LISTA_DE_TEXTOS,
        "conceitos": LISTA_DE_TEXTOS,
        "projetos": LISTA_DE_TEXTOS,
    },
    "required": ["tipo", "assuntos", "conceitos", "projetos"],
}


def listar_arquivos_novos():
    arquivos = []
    for arquivo in sorted(PASTA_ENTRADA.iterdir()):
        if arquivo.is_file() and arquivo.suffix in EXTENSOES_ACEITAS:
            arquivos.append(arquivo)
    return arquivos


def ler_arquivo(arquivo):
    return arquivo.read_text(encoding="utf-8")


def carregar_instrucao(nome_da_secao):
    texto = ARQUIVO_INSTRUCOES.read_text(encoding="utf-8")
    for bloco in texto.split("\n## "):
        titulo, _, corpo = bloco.partition("\n")
        if titulo.strip() == nome_da_secao:
            return corpo.strip()
    raise ValueError(f"Seção '{nome_da_secao}' não encontrada em {ARQUIVO_INSTRUCOES.name}")


def classificar(conteudo):
    pergunta = carregar_instrucao("classificar").replace("{texto}", conteudo)
    resposta = ollama.chat(
        model=MODELO,
        messages=[{"role": "user", "content": pergunta}],
        format=ESQUEMA_CLASSIFICACAO,
        options={"temperature": 0},
    )
    return json.loads(resposta.message.content)


def normalizar(texto):                                   # NOVO
    decomposto = unicodedata.normalize("NFD", texto)
    sem_acento = "".join(c for c in decomposto if unicodedata.category(c) != "Mn")
    return sem_acento.lower().strip()


def buscar_notas(termo):                                 # NOVO
    termo_normalizado = normalizar(termo)
    encontradas = []
    for nota in sorted(PASTA_VAULT.rglob("*.md")):
        nome = normalizar(nota.stem)
        if termo_normalizado in nome or nome in termo_normalizado:
            encontradas.append(nota)
    return encontradas


def relacionar(classificacao):                           # NOVO
    relacionadas = {}
    for campo in ("assuntos", "conceitos", "projetos"):
        for termo in classificacao[campo]:
            for nota in buscar_notas(termo):
                relacionadas.setdefault(nota, []).append(f"{campo}: {termo}")
    return relacionadas


if __name__ == "__main__":
    for arquivo in listar_arquivos_novos():
        conteudo = ler_arquivo(arquivo)
        classificacao = classificar(conteudo)
        print(f"=== {arquivo.name}")
        print(f"  tipo:      {classificacao['tipo']}")
        print(f"  assuntos:  {classificacao['assuntos']}")
        print(f"  conceitos: {classificacao['conceitos']}")
        print(f"  projetos:  {classificacao['projetos']}")
        relacionadas = relacionar(classificacao)                     # NOVO
        print("  notas relacionadas:")
        if not relacionadas:
            print("    (nenhuma)")
        for nota, motivos in relacionadas.items():
            print(f"    {nota.relative_to(PASTA_VAULT)}  ← {', '.join(motivos)}")