## Listar absolutamente tudo, incluindo arquivos ocultos (como .env, .git, .venv):

```Python

ls -la
```

## Ver a estrutura completa em formato de árvore (todas as pastas e subpastas):

```Python
find . -maxdepth 3 -not -path '*/.*'
```

## Contar quantos arquivos existem no projeto (ignorando o ambiente virtual .venv e o .git):

```Python
find . -type f -not -path '*/.venv/*' -not -path '*/.git/*' | wc -l
```

## Escreva **você** os comandos para criar a nova estrutura e mover 3 arquivos dela. Use só estes formatos:

```Python
mkdir -p caminho/novo
mv "nome com espaço.md" destino/nome_sem_espaco.md
```

## Fazer uma versionamento opra o github

```Python
git init
git add .
git commit -m "estrutura inicial do agente redator"

git remote add origin https://github.com/heriveltopaiva/criar_manual.git
git branch -M main
git push -u origin main
```

## A sequência está  **certa** . É a ordem do “...or create a new repository” que aparece no próprio GitHub, com o `.gitignore` entrando antes do `add`:

```Python


1. git init                 → transforma a pasta em repositório
2. (criar .gitignore)       → antes do add, para a .venv não entrar
3. git add .                → coloca os arquivos na "caixa"
4. git commit -m "..."      → fecha a caixa e etiqueta (cria o branch)
5. git remote add origin …  → anota o endereço do GitHub
6. git branch -M main       → renomeia master → main
7. git push -u origin main  → envia
```

## Criar past e arquivos

```Python
mkdir -p agentes/redator_manuais entrada manuais && touch agentes/redator_manuais/{instrucoes.md,template_manual.md.agente.py} AGENTS.md
```

## Sim, vamos seguir. Antes de escrever mais código, preciso conferir três coisas no seu computador.

### Passo 1: conferir as pastas e o primeiro código

Dentro de `~/agente_documental`, rode:

```Python
ls
python3 agente.py
```

O `ls` deve listar as pastas que você criou. O segundo comando deve imprimir `teste1.md`. Se você ainda não criou o `agente.py` com o código da mensagem anterior, crie agora.

### Passo 2: ver se o Ollama está rodando

```Python
ollama list
curl http://localhost:11434/api/tags
```

	`ollama list` mostra os modelos instalados. O `llama3.1:8b` precisa aparecer na lista.

`	curl` testa o endereço que o Python vai usar para falar com o modelo. A resposta esperada é um texto em JSON com os modelos, e não um erro de conexão.

### Passo 3: testar o português do modelo: aqui estou testando a resposta no ollama para ver qual vai ser o melhor para determinar o agente que vou colocar para execultar a minha tarefa.

```Python
ollama run llama3.1:8b "Responda em português do Brasil, em uma frase: o que é um JOIN em SQL?"
```

### Falta descobrir uma coisa

Os tipos `ideia`, `decisao` e `moc` não têm uma pasta óbvia. Rode:

```Python
grep -rHi "^tipo:" --include="*.md" . | sort
grep -rl "^topic:" --include="*.md" . | cut -d/ -f2 | sort | uniq -c
```

## Rodar

```Python
cd ~/criar_manual/agente_documental
python3 inventario.py
```

## Cole aqui o resumo que aparece no terminal. A planilha completa você pode abrir no LibreOffice Calc, ou ver um pedaço no terminal com:

```Python
column -s, -t historico/inventario.csv | head -30
```

## Conferir o resultado

```Python
cd "/home/herivelto-paiva/Obsidian Vault/Templates"
for f in *.md; do echo "===== $f"; head -8 "$f"; done
tail -3 "03 Estrutura.md"
grep -n -A3 "## Decisões" "08 Projeto.md"
```

## Se tiver dando erro a ativação do venv tente esse comando aqui:

```Python
source ../.venv/bin/activate
```

### Onde aparecem as saídas do teste 8 As propostas aparecem  **no terminal** , não nas notas. Rode:

```Python
cd ~/criar_manual/agente_documental
python3 agente.py
```

## Colocar nome no meu HD externo

```Python
sudo e2label /dev/sda1 NOME_QUE_VOCE_QUISER
```

## Confira se o nome foi gravado:

```Python
lsblk -f /dev/sda1
```

## Confira se o nome foi gravado:

```python
ls /run/media/herivelto-paiva/
```

## Ajuste a variável e siga o passo 2 da mensagem anterior:

```python
HD="/run/media/herivelto-paiva/BACKUP_IA/backup_ia"
sudo mkdir -p "$HD"
sudo chown "$USER": "$HD"
ls -ld "$HD"
```

## 1. Confira se o Git está instalado e configure seu nome:

```python
git --version
git config --global user.name "Seu Nome"
git config --global user.email "seuemail@exemplo.com"
```

## 1. Atalho de teclado personalizado no VS Code (Mais rápido)

Você pode configurar um atalho (como Ctrl + ; ou Alt + c) para inserir as três crases e já deixar o cursor no meio delas, tanto no editor quanto no terminal.

1. No VS Code, pressione Ctrl + Shift + P.
2. Digite Open Keyboard Shortcuts (JSON) e aperte Enter.
3. Adicione o código abaixo dentro dos colchetes [ ]:

```python
[
    {
        "key": "shift+enter",
        "command": "workbench.action.terminal.sendSequence",
        "args": {
            "text": "\u001b\r"
        },
        "when": "terminalFocus"
    },
    {
        "key": "alt+c",
        "command": "editor.action.insertSnippet",
        "args": {
            "snippet": "```$1\n$0\n```"
        },
        "when": "editorTextFocus"
    },
    {
        "key": "alt+c",
        "command": "workbench.action.terminal.sendSequence",
        "args": {
            "text": "``````\u001b[D\u001b[D\u001b[D"
        },
        "when": "terminalFocus"
    }
]
```

Aqui eu consigo colocar alguns atalho para que possa ter mais falidade no meu uso no dia a dia.


>
> Resposta direta: não, sua pasta ainda não está igual ao Git. O git status mostra três tipos de diferença. O seu último commit já está no GitHub (up to date with 'origin/main'), mas essas mudanças ainda não foram commitadas.
>
> Como ler o resultado
> Seção	Significado	No seu caso
> Mudanças a serem submetidas (staged)	Preparadas para o próximo commit	27 itens, quase todos new file de agente_documental/
> Changes not staged	Alteradas, mas ainda não preparadas	.gitignore e 28 arquivos apagados de entrada/
> Arquivos não monitorados (untracked)	O Git ainda não conhece	a pasta agente_documental/entrada/
>
> O .gitignore aparece nas duas primeiras porque foi alterado de novo depois de preparado.
>
> O que chama atenção
>
> 1. O diff ficou preso no less. As linhas :...skipping... são o leitor de páginas do terminal. Aperte q para sair. Para ver só o resumo, use git diff --stat.
> 2. A pasta entrada/ foi apagada do disco. Os 28 deleted são arquivos que já estavam no Git e no GitHub (manuais, prompts, scripts zuz*.py). Também sumiu a linha entrada/ do .gitignore, e apareceu agente_documental/entrada/ como pasta nova. Parece que você moveu a pasta de lugar. Se foi de propósito, está certo. Se foi sem querer, recupere com:
>
> bash
> git restore entrada/
>
> 3. Um .pyc está entre os arquivos preparados: agente_documental/__pycache__/inventario.cpython-314.pyc. É lixo gerado pelo Python e não deve subir. Corrija assim:
>
> bash
> git rm --cached agente_documental/__pycache__/inventario.cpython-314.pyc
>
> E acrescente ao .gitignore:
>
> __pycache__/
> *.pyc
>
> 4. Decida sobre agente_documental/entrada/. Se for material pessoal ou pesado, coloque agente_documental/entrada/ no .gitignore. Se quiser versionar, ela entra no git add.
> 5. Os arquivos de entrada/ já foram ao GitHub. Se o repositório for público, esse conteúdo já está visível, e apagar agora não remove do histórico. Confira em github.com se o repositório está como Private.
>
> Passo a passo para fechar
> bash
>
> # 1. sair do less, se ainda estiver nele: tecla q
>
> # 2. editar o .gitignore (acrescentar __pycache__/ e *.pyc)
>
> nano .gitignore
>
> # 3. tirar o .pyc da fila
>
> git rm --cached agente_documental/__pycache__/inventario.cpython-314.pyc
>
> # 4. preparar tudo, inclusive as exclusões
>
> git add -A
>
> # 5. conferir antes de salvar
>
> git status
>
> # 6. salvar a versão
>
> git commit -m "Reorganiza entrada para agente_documental e adiciona agente"
>
> # 7. enviar ao GitHub
>
> git push
>
> No passo 5, confira que a lista só tem o que você quer enviar. Depois do push, git status deve mostrar nothing to commit, working tree clean.
>
> Se o passo 5 trouxer algo que você não reconhece, cole a saída aqui.
