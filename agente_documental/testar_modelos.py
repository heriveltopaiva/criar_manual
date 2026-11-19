import json
import time
import ollama

TEXTO = [
    "Configurei o Docker no servidor do projeto Financeiro e descobri que o volume precisa de permissão 755. Também testei uma query SQL com GROUP BY que estava lenta.",
    "Ideia: usar Python para gerar relatórios automáticos em PDF.",
]

LISTA_DE_TEXTOS = {"type": "array", "items": {"type": "string"}}

ESQUEMA = {
    "type": "object",
    "properties": {
        "assuntos": LISTA_DE_TEXTOS,
        "conceitos": LISTA_DE_TEXTOS,
        "projetos": LISTA_DE_TEXTOS,
    },
    "required": ["assuntos", "conceitos", "projetos"],
}

# MODELOS = ["gemma4:12b",  "hermes3:latest", "llama3.1:8b"]
# MODELOS = ["llama3.1:8b", "hermes3:latest", "qwen3.5:9b-q4_K_M", "gemma4:12b"]
# MODELOS = ["llama3.1:8b"]
# MODELOS = ["hermes3:latest"]
# MODELOS = ["qwen3.5:9b-q4_K_M"]
MODELOS = ["gemma4:12b"]
# MODELOS = ["qwen3.5:9b-q4_K_M", "gemma4:12b"]
# MODELOS = ["qwen3.5:9b-q4_K_M", "gemma4:12b"]
# MODELOS = ["hermes3:latest", "gemma4:12b"]

for modelo in MODELOS:
    for texto in TEXTO:
        PERGUNTA = f"""Classifique o texto abaixo.
        - assuntos: temas gerais que teriam um manual próprio (ex.: SQL, Python).
        - conceitos: detalhes dentro de um assunto (ex.: JOIN).
        - projetos: nomes de projetos onde algo foi aplicado.
        - Se o nome do projeto não estiver escrito LITERALMENTE no texto, deixe a lista de projetos vazia. Não deduza projetos pelo contexto.
        Texto: "{texto}" """
        
        inicio = time.time()
        try:
            resposta = ollama.chat(
                model=modelo,
                messages=[{"role": "user", "content": PERGUNTA}],
            format=ESQUEMA,
            options={"temperature": 0},
            think=False if modelo.startswith("qwen") else None,
        )
            dados = json.loads(resposta.message.content)
            print(f"{modelo} ({time.time() - inicio:.1f}s): {dados}")
        except Exception as erro:
            print(f"{modelo}: ERRO -> {erro}")


            ## python3 agente_documental/testar_modelos.py


        
        