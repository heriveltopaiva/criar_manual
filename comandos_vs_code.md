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
