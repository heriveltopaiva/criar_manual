import json
from datetime import datetime
import re
import unicodedata
from pathlib import Path

import ollama

from inventario import ler_cabecalho

PASTA_BASE = Path(__file__).parent
PASTA_ENTRADA = PASTA_BASE / "entrada"
PASTA_VAULT = PASTA_BASE / "vault_teste"
PASTA_PROPOSTAS = PASTA_BASE / "propostas"
PASTA_TEMPLATES = Path("/home/herivelto-paiva/Obsidian Vault/Templates")
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

ESQUEMA_PROPOSTA = {
    "type": "object",
    "properties": {
        "alterar": {"type": "boolean"},
        "secao": {"type": "string"},
        "texto": {"type": "string"},
        "motivo": {"type": "string"},
    },
    "required": ["alterar", "secao", "texto", "motivo"],
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


def montar_pergunta(nome_da_secao, valores):
    pergunta = carregar_instrucao(nome_da_secao)
    for marcador, valor in valores.items():
        chave = "{" + marcador + "}"
        if chave not in pergunta:
            raise ValueError(
                f"Marcador {chave} não encontrado na seção '{nome_da_secao}' de {ARQUIVO_INSTRUCOES.name}"
            )
        pergunta = pergunta.replace(chave, valor)
    return pergunta


def perguntar_ao_modelo(pergunta, esquema):
    resposta = ollama.chat(
        model=MODELO,
        messages=[{"role": "user", "content": pergunta}],
        format=esquema,
        options={"temperature": 0, "num_ctx": 8192},
    )
    return json.loads(resposta.message.content)


def classificar(conteudo):
    pergunta = montar_pergunta("classificar", {"texto": conteudo})
    return perguntar_ao_modelo(pergunta, ESQUEMA_CLASSIFICACAO)


def normalizar(texto):
    decomposto = unicodedata.normalize("NFD", texto)
    sem_acento = "".join(c for c in decomposto if unicodedata.category(c) != "Mn")
    return sem_acento.lower().strip()


def buscar_notas(termo):
    termo_normalizado = normalizar(termo)
    encontradas = []
    for nota in sorted(PASTA_VAULT.rglob("*.md")):
        nome = normalizar(nota.stem)
        if termo_normalizado in nome or nome in termo_normalizado:
            encontradas.append(nota)
    return encontradas


def relacionar(classificacao):
    relacionadas = {}
    for campo in ("assuntos", "conceitos", "projetos"):
        for termo in classificacao[campo]:
            for nota in buscar_notas(termo):
                relacionadas.setdefault(nota, []).append(f"{campo}: {termo}")
    return relacionadas


def secoes_do_template(tipo):
    tipo_normalizado = normalizar(tipo)
    if not tipo_normalizado:
        return []
    for modelo in sorted(PASTA_TEMPLATES.glob("*.md")):
        if tipo_normalizado in normalizar(modelo.stem):
            linhas = modelo.read_text(encoding="utf-8").splitlines()
            return [linha[3:].strip() for linha in linhas if linha.startswith("## ")]
    return []


def secoes_da_nota(texto):
    return [linha[3:].strip() for linha in texto.splitlines() if linha.startswith("## ")]


def propor_alteracao(conteudo, nota, todas_relacionadas):
    texto_nota = nota.read_text(encoding="utf-8")
    tipo = (ler_cabecalho(texto_nota) or {}).get("tipo", "")
    outras = [f"[[{n.stem}]]" for n in todas_relacionadas if n != nota]
    pergunta = montar_pergunta("propor_alteracao", {
        "outras_notas": ", ".join(outras) or "(nenhuma)",
        "secoes_template": ", ".join(secoes_do_template(tipo)) or "(sem template)",
        "nome_nota": nota.stem,
        "nota": texto_nota,
        "texto": conteudo,
    })
    return perguntar_ao_modelo(pergunta, ESQUEMA_PROPOSTA)


def validar_proposta(proposta, nota):
    problemas = []
    if not proposta["motivo"].strip():
        problemas.append("motivo vazio")
    if not proposta["alterar"]:
        return problemas
    if not proposta["texto"].strip():
        problemas.append("alteração sem texto")

    texto_nota = nota.read_text(encoding="utf-8")
    tipo = (ler_cabecalho(texto_nota) or {}).get("tipo", "")
    secoes_validas = secoes_da_nota(texto_nota) + secoes_do_template(tipo)
    secao = proposta["secao"].strip().lstrip("#").strip()
    if normalizar(secao) not in [normalizar(s) for s in secoes_validas]:
        problemas.append(f"seção '{secao}' não existe na nota nem no template")

    nomes_existentes = {normalizar(n.stem) for n in PASTA_VAULT.rglob("*.md")}
    for link in re.findall(r"\[\[([^\]|#]+)", proposta["texto"]):
        if normalizar(link) not in nomes_existentes:
            problemas.append(f"link para nota inexistente: [[{link}]]")
    return problemas


def caminho_registro(arquivo):
    return PASTA_PROPOSTAS / f"{arquivo.name}.json"


def analisar_arquivo(arquivo):
    conteudo = ler_arquivo(arquivo)
    classificacao = classificar(conteudo)
    print(f"=== {arquivo.name}")
    print(f"  tipo:      {classificacao['tipo']}")
    print(f"  assuntos:  {classificacao['assuntos']}")
    print(f"  conceitos: {classificacao['conceitos']}")
    print(f"  projetos:  {classificacao['projetos']}")
    relacionadas = relacionar(classificacao)
    if not relacionadas:
        print("  notas relacionadas: (nenhuma)")

    propostas = []
    for numero, (nota, motivos) in enumerate(relacionadas.items(), start=1):
        caminho_nota = str(nota.relative_to(PASTA_VAULT))
        print(f"  --- {caminho_nota}  ← {', '.join(motivos)}")
        proposta = propor_alteracao(conteudo, nota, relacionadas)
        problemas = validar_proposta(proposta, nota)
        if problemas:
            status = "descartada"
            print(f"      ⚠ PROPOSTA DESCARTADA: {'; '.join(problemas)}")
        elif proposta["alterar"]:
            status = "pendente"
            print(f"      PROPOSTA na seção '## {proposta['secao']}':")
            print(f"        {proposta['texto'].strip()}")
            print(f"      motivo: {proposta['motivo']}")
        else:
            status = "sem_alteracao"
            print("      sem alteração")
            print(f"      motivo: {proposta['motivo']}")
        propostas.append({
            "id": numero,
            "nota": caminho_nota,
            "selecionada_por": motivos,
            "secao": proposta["secao"].strip().lstrip("#").strip(),
            "texto": proposta["texto"].strip(),
            "motivo": proposta["motivo"],
            "status": status,
            "problemas": problemas,
        })

    return {
        "origem": arquivo.name,
        "analisado_em": datetime.now().isoformat(timespec="seconds"),
        "modelo": MODELO,
        "classificacao": classificacao,
        "propostas": propostas,
    }


def salvar_registro(arquivo, registro):
    destino = caminho_registro(arquivo)
    destino.write_text(json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8")
    return destino


if __name__ == "__main__":
    PASTA_PROPOSTAS.mkdir(exist_ok=True)
    for arquivo in listar_arquivos_novos():
        if caminho_registro(arquivo).exists():
            print(f"=== {arquivo.name}: já analisado, pulei")
            continue
        registro = analisar_arquivo(arquivo)
        destino = salvar_registro(arquivo, registro)
        print(f"  → registro salvo em {destino.relative_to(PASTA_BASE)}")
