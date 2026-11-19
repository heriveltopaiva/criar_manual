# Agente Documental — Progresso da V1

Atualizado em 2026-11-15.

## Ambiente
- Máquina: RTX 3060 12 GB, 30 GB RAM, Ubuntu, Python 3.14 em `.venv` (`~/criar_manual/.venv`).
- Projeto: `~/criar_manual/agente_documental/`
- Pastas: `entrada/`, `processados/`, `propostas/`, `historico/`, `vault_teste/` (simula o Obsidian).
- A pasta `~/criar_manual/entrada/` contém arquivos reais do usuário e NÃO é usada nos testes.

## Decisões
| Decisão | Motivo | Status |
|---|---|---|
| Construir o agente primeiro com `vault_teste/`; conectar ao Vault real depois | Testar sem risco aos documentos reais | Aprovada |
| Modelo: `gemma4:12b` via Ollama; plano B `llama3.1:8b` | Gemma foi o único completo nos dois testes; llama rápido e quase igual | Aprovada |
| Descartado `qwen3.5:9b` | Omitiu assunto (Docker) e projeto (Financeiro) | — |
| Classificação em JSON com `assuntos`, `conceitos`, `projetos` | Separar manual geral, seção do manual e documentação de projeto | Aprovada (pode mudar) |
| Formato garantido via `format=` (esquema JSON) do Ollama, `temperature=0` | JSON válido e resultados reproduzíveis | Implementada |
| Extensões aceitas na V1: `.md`, `.txt` | Começar simples | Implementada |

## Testes de modelos (classificação)
- Texto 1 (Docker + SQL + projeto Financeiro) e Texto 2 (ideia Python, sem projeto).
- gemma4:12b: completo nos dois (~10–16 s). llama3.1:8b e hermes3: Texto 1 completo, Texto 2 sem conceitos (~1–5 s). qwen3.5:9b: falhou no Texto 1 e devolveu `assuntos: ['']` em teste anterior.
- Lição: o esquema garante a estrutura, não o conteúdo — será necessária validação própria (ex.: listas com texto vazio).
- Observação: Ollama usa contexto padrão de 4K tokens em GPUs < 24 GB; ajustar quando comparar documentos.

## Implementado e testado (`agente.py`)
1. Listar arquivos `.md`/`.txt` da entrada (caminho baseado em `Path(__file__).parent`, funciona de qualquer diretório). ✅
2. Ler conteúdo em UTF-8. ✅
3. Classificar com o gemma e exibir assuntos/conceitos/projetos. ✅ (testado com `teste1.md` e `anotacoes_sql.txt`)

## Ainda não implementado
- Buscar documentos relacionados no `vault_teste/`.
- Gerar propostas; aprovação individual; aplicar alterações aprovadas.
- Mover originais para `processados/`; registrar em `historico/`.
- Validação do conteúdo classificado; tratamento de erros.
- Uso do `instrucoes.md` (decisão pendente).
