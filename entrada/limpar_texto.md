## Passo 1: Limpeza Automatizada (No Terminal)

Remover linhas duplicadas idênticas:
Se houver blocos ou linhas de texto repetidas exatamente iguais, use este comando para criar um arquivo limpo chamado conteudo_sem_duplicadas.md:

```Python
awk '!seen[$0]++' todos_conteudo.md > conteudo_sem_duplicadas.md
```
awk '!seen[$0]++' todos_conteudo_original.md > todos_conteudo_limpo.md


## para ver o tamanho do arquivos

```Python
ls -lh "nome do "arquivo"
```
## Para mostrar exatamente a quantidade de linhas 

wc -l todos_conteudo_limpo.md && ls -lh todos_conteudo_limpo.md
