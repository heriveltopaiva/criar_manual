# RELATÓRIO DE ANÁLISE PRÉVIA --- HSP VEHICLE INTELLIGENCE

**Código:** `AUD-HSP-VI-001`\
**Versão:** 1.0\
**Data:** 12/10/2026\
**Tipo:** Relatório de inventário e diagnóstico documental\
**Estado:** Análise preliminar concluída; análise semântica integral e
reorganização do manual ainda pendentes\
**Projeto:** HSP Vehicle Intelligence\
**Objetivo:** identificar fontes, contextos, problemas de organização e
defeitos de apresentação antes de reescrever o manual.

## 1. Escopo e limite desta análise

Esta etapa inventaria os arquivos disponíveis, mede sua estrutura,
inspeciona as seções centrais e compara a organização do manual
consolidado com os documentos de origem.

**Granularidade efetivamente realizada:** inventário por arquivo;
análise estrutural por contagem de linhas, títulos, tabelas e
delimitadores de código; leitura temática de seções e trechos
representativos; identificação de conflitos já registrados. A conversa
histórica foi perfilada estruturalmente e consultada por temas, mas
ainda não foi revisada semanticamente linha por linha. Portanto, este
relatório não afirma que cada informação da conversa já foi conferida
individualmente.

**Regra de execução:** não reescrever o manual principal antes de
concluir o mapeamento de contexto, as comparações de versões e a análise
das lacunas.

## 2. Inventário das fontes

  -------------------------------------------------------------------------------------------------------------------------------------
  ID da fonte            Arquivo                                                              Tamanho Extensão        Função
                                                                                           aproximado estrutural      
                                                                                                      observada       
  ---------------------- ---------------------------------------------------------- ----------------- --------------- -----------------
  `SRC-HSP-VI-001-001`   `estrutura-do-manual.md`                                     2 KB; 33 linhas 4 títulos; sem  Define as 11
                                                                                                      blocos de       seções
                                                                                                      código          obrigatórias, os
                                                                                                                      modos
                                                                                                                      CRIAR/ATUALIZAR e
                                                                                                                      a checagem final.

  `SRC-HSP-VI-001-002`   `Manual-desenvolvimento.md`                                 7 KB; 198 linhas 2 títulos;      Histórico de
                                                                                                      nenhum bloco    Node.js,
                                                                                                      cercado por     `package.json`,
                                                                                                      crases          Clasp,
                                                                                                                      autenticação,
                                                                                                                      sincronização e
                                                                                                                      `.claspignore`.

  `SRC-HSP-VI-001-003`   `Manual-HSP-Vehicle-Intelligence-v3.0-integral.md`         16 KB; 963 linhas 29 títulos; 78  Documento técnico
                                                                                                      blocos cercados organizado por
                                                                                                      por crases      fonte de
                                                                                                                      veículos,
                                                                                                                      arquitetura, Meta
                                                                                                                      Catalog,
                                                                                                                      histórico e
                                                                                                                      procedimentos.

  `SRC-HSP-VI-001-004`   `ChatGPT-Criar catálogo de veículos-20260927-0943(1).md`      931 KB; 39.385 1.684 títulos;  Histórico
                                                                                               linhas 1.896 pares de  cronológico
                                                                                                      delimitadores   extenso de
                                                                                                      de código       perguntas,
                                                                                                                      respostas,
                                                                                                                      investigações,
                                                                                                                      propostas, erros
                                                                                                                      e código.

  `SRC-HSP-VI-001-005`   `MAN-HSP-VI-001_v1.0.md`                                    1.047 KB; 43.962 1.784 títulos;  Manual
                                                                                               linhas 2.104 pares de  consolidado
                                                                                                      delimitadores   atual, com as 11
                                                                                                      de código       seções e os
                                                                                                                      documentos
                                                                                                                      históricos
                                                                                                                      anexados em
                                                                                                                      apêndices.
  -------------------------------------------------------------------------------------------------------------------------------------

**Observação:** os tamanhos são os dos arquivos disponíveis neste
ambiente e podem diferir de outras cópias locais. A presença de um
arquivo não prova que seja a versão atual do repositório de
desenvolvimento.

## 3. Mapa de contextos do projeto

As informações devem ser agrupadas nos contextos abaixo. A sequência
proposta é lógica, não cronológica.

  ------------------------------------------------------------------------------------------------------
  Contexto                                    Conteúdo que pertence a ele    Tratamento documental
  ------------------------------------------- ------------------------------ ---------------------------
  `CTX-01 — Objetivo e evolução`              Objetivo original de coletar   Visão Geral e histórico de
                                              anúncios; evolução para        evolução. Distinguir
                                              normalização, histórico,       objetivo, arquitetura
                                              análise de mercado e           planejada e estado
                                              integração com catálogo.       implementado.

  `CTX-02 — Arquitetura e fluxo de dados`     Fontes → coletores → dados     Mapa do Sistema. Rotular
                                              brutos → normalização →        como arquitetura-alvo onde
                                              validação → CSV/persistência → a integração real não foi
                                              API/análises/interface/feed.   verificada.

  `CTX-03 — Contrato de dados normalizados`   CSV comum com 11 campos,       Módulo próprio, antes dos
                                              regras de mapeamento, campos   módulos de cada fonte, pois
                                              ausentes, dados brutos e       todos dependem desse
                                              validação.                     padrão.

  `CTX-04 — Coletor D Motors`                 Endpoint `/stock`, paginação,  Um único módulo, reunindo
                                              resposta JSON, contagens       evidências, campos,
                                              históricas e investigação via  procedimento, resultados e
                                              Network.                       limites.

  `CTX-05 — Coletor Quitcar`                  Cartões HTML, seletor          Um único módulo. Não
                                              `.card.card-car`, URL,         misturar com filtros ou
                                              paginação e contagens          campos de outras lojas.
                                              históricas.                    

  `CTX-06 — Coletor Milani`                   Página de estoque, estado      Um único módulo; separar
                                              inicial de carregamento,       observação da página,
                                              termos de configuração,        chamada de rede e execução
                                              endpoint e campos observados.  do gerador.

  `CTX-07 — Coletor Localiza`                 `__NEXT_DATA__`, paginação     Um único módulo. Manter o
                                              regional e nacional, campos,   conflito `modeloDescricao`
                                              URLs, exemplo de veículo e     versus
                                              conflito de mapeamento de      `modeloFamiliaDescricao`
                                              modelo.                        aberto até verificar o
                                                                             código vigente.

  `CTX-08 — Coletor Super Novos`              Firestore, ID de revenda,      Um único módulo. Manter a
                                              consulta, filtros, campos,     sequência investigação →
                                              imagens, URL, tentativas REST, tentativas → erro →
                                              erros e execução com 169       correção → resultado; não
                                              documentos/16 ativos.          afirmar completude do
                                                                             estoque.

  `CTX-09 — Persistência e histórico`         Entidades `fontes`,            Módulo de dados históricos.
                                              `veiculos`, `anuncios`,        Diferenciar proposta
                                              `snapshots`; primeira/última   conceitual de implementação
                                              coleta; variações de preço;    validada.
                                              desaparecimento de anúncio.    

  `CTX-10 — Banco e camada de aplicação`      Supabase mencionado em         Registrar a evolução e
                                              registros anteriores;          manter o banco ativo como
                                              Neon/PostgreSQL, SQLAlchemy,   conflito/lacuna até haver
                                              Alembic, FastAPI, Flet e       evidência do ambiente
                                              Render mencionados em          atual.
                                              arquitetura posterior.         

  `CTX-11 — Meta Catalog/feed`                Requisitos do catálogo         Módulo de integração
                                              externo, campos, imagens,      independente. Não misturar
                                              regras de feed e separação     código Apps Script
                                              entre schema externo e         histórico com arquitetura
                                              inteligência interna.          atual sem marcar a relação.

  `CTX-12 — Node.js, Apps Script e Clasp`     `package.json`, instalação,    Tratar como histórico de
                                              login, clone/pull/push, IDs,   desenvolvimento/protótipo e
                                              erro de variável duplicada e   registrar seu estado atual
                                              `.claspignore`.                desconhecido.

  `CTX-13 — Escala e armazenamento`           Estimativa de 600.000          Manter os números
                                              anúncios, 500 bytes por        identificados como
                                              snapshot, GitHub, Object       estimativas conceituais,
                                              Storage, Parquet e DuckDB.     não medições de produção.

  `CTX-14 — Procedimentos reutilizáveis`      Investigar uma fonte nova,     Converter em procedimentos
                                              validar coletor, conferir CSV, independentes com
                                              medir arquivos, investigar     pré-requisitos, entradas,
                                              requisições e reproduzir       passos, saída, validação e
                                              erros.                         falhas.

  `CTX-15 — Linha do tempo e evidências`      Data, objetivo, ação, comando, Preservar em histórico
                                              resultado, erro, diagnóstico,  consultável; não usar a
                                              correção, decisão e            cronologia como estrutura
                                              aprendizado.                   principal dos módulos.
  ------------------------------------------------------------------------------------------------------

## 4. Problemas de formatação confirmados

### 4.1 `Manual-desenvolvimento.md`

-   O arquivo contém exemplos de JSON, Bash e texto, mas não utiliza
    cercas Markdown de código com três crases.
-   Rótulos como `json`, `bash` e `text` aparecem como texto separado do
    conteúdo.
-   Um leitor pode não distinguir com segurança a explicação do código a
    copiar.
-   A tabela de comandos do fluxo diário está escrita como texto
    separado por tabulações, não como tabela Markdown.

**Correção necessária:** preservar o conteúdo original como fonte; na
versão organizada, apresentar cada bloco com cercas e linguagem
apropriada, além de converter a tabela de comandos para uma tabela
Markdown real. Não modificar o código em si durante a mera formatação.

### 4.2 `Manual-HSP-Vehicle-Intelligence-v3.0-integral.md`

-   Foram encontrados 78 blocos de código cercados; muitos usam
    linguagem `text` ou não informam linguagem.
-   Trechos que são código executável devem receber a linguagem
    correspondente quando identificável. Exemplos de saída de terminal
    podem continuar identificados como `text`.
-   Há tabelas em Markdown, mas é necessário conferir sua consistência e
    alinhamento na auditoria final.

### 4.3 `MAN-HSP-VI-001_v1.0.md`

-   O documento contém os 11 títulos principais esperados, mas algumas
    tabelas aparecem no formato de tabela de grade do Pandoc, que não é
    compatível com todos os visualizadores Markdown, especialmente
    renderizadores que esperam a sintaxe de barras verticais.
-   A tabela do Glossário apresenta uma linha defeituosa: o termo está
    vazio e a explicação aparece como "o objetivo central.". Isso
    precisa ser corrigido somente após verificar o conteúdo de origem;
    não se deve adivinhar qual termo estava faltando.
-   Alguns passos aparecem em parágrafos corridos, por exemplo "Como
    reproduzir..." seguido de números na mesma linha, dificultando a
    execução passo a passo.
-   Regras que deveriam ser listas usam frases concatenadas após
    "Regras:", reduzindo a legibilidade.
-   Muitos blocos estão rotulados como `text` ou sem linguagem,
    inclusive em conteúdo que parece ser código. A classificação precisa
    ser feita bloco a bloco; não se deve converter saídas, JSON ou texto
    de exemplo em código executável por suposição.
-   O documento inclui a transcrição histórica completa como apêndice,
    elevando o arquivo a 43.962 linhas. Isso preserva a fonte, mas torna
    a consulta do manual principal muito pesada e repete conteúdo já
    resumido nas seções principais.

**Recomendação documental:** manter a transcrição original intacta em
arquivo de fonte independente e vinculá-la pela tabela de
rastreabilidade. O manual principal deve conter a informação organizada
e os trechos originais necessários para rastreabilidade; não é
obrigatório duplicar dezenas de milhares de linhas no mesmo arquivo. A
decisão final sobre manter uma cópia integral em apêndice deve respeitar
a regra de preservação do projeto e não apagar a fonte original.

### 4.4 Cabeçalho e exportação

-   O cabeçalho atual contém sequências como `---` e barras invertidas
    para quebras de linha, sinal de conversão/exportação que precisa ser
    normalizado para Markdown simples.
-   Títulos, tabelas, listas e cercas de código devem ser verificados no
    arquivo final, não apenas no texto intermediário.

## 5. Conflitos e lacunas identificados nas fontes

  -----------------------------------------------------------------------------------------
  ID                     Item                 Evidência disponível        Estado e ação
                                                                          necessária
  ---------------------- -------------------- --------------------------- -----------------
  `CON-HSP-VI-001-001`   Supabase versus      Supabase aparece em         Não afirmar qual
                         Neon/PostgreSQL      registros anteriores;       banco está
                                              Neon/PostgreSQL aparece em  conectado hoje.
                                              arquitetura posterior.      Conferir
                                                                          configuração e
                                                                          ambiente atual.

  `CON-HSP-VI-001-002`   Campo `modelo` da    Há referências a            Comparar com o
                         Localiza             `modeloDescricao` e         coletor vigente e
                                              `modeloFamiliaDescricao`.   preservar a
                                                                          alternativa não
                                                                          selecionada no
                                                                          histórico.

  `CON-HSP-VI-001-003`   Completude do Super  Uma execução registrou 169  Não interpretar
                         Novos                documentos, 16 ativos e 153 16 como estoque
                                              ignorados.                  completo.
                                                                          Investigar
                                                                          revendas,
                                                                          filtros,
                                                                          paginação e
                                                                          agregação.

  `LAC-HSP-VI-001-001`   Repositório/branch   A árvore atual do           Solicitar ou
                         atual                repositório não foi         inspecionar
                                              verificada nesta análise.   arquivos atuais
                                                                          antes de declarar
                                                                          caminhos e
                                                                          versões vigentes.

  `LAC-HSP-VI-001-002`   Execução atual dos   Os resultados registrados   Executar ou obter
                         coletores            são históricos.             logs recentes
                                                                          antes de declarar
                                                                          os coletores
                                                                          validados.

  `LAC-HSP-VI-001-003`   Código integral      O código atual completo não Localizar a
                         atual do Super Novos está comprovado pelas       versão real do
                                              fontes inventariadas.       arquivo antes de
                                                                          publicar código
                                                                          completo.

  `LAC-HSP-VI-001-004`   Estado da aplicação  FastAPI, Flet, Render e     Separar
                         e do feed            feed Meta aparecem como     arquitetura
                                              arquitetura/objetivos, mas  proposta de
                                              o estado atual não foi      serviço
                                              validado.                   implementado e
                                                                          testado.

  `LAC-HSP-VI-001-005`   Retenção e volume    Existem estimativas de      Definir retenção
                         real                 armazenamento e snapshots,  e medir volume
                                              não medições de produção.   real quando
                                                                          houver coleta
                                                                          histórica.
  -----------------------------------------------------------------------------------------

## 6. Sequência recomendada para o manual reorganizado

1.  Visão Geral: objetivo, escopo e estado confirmado.
2.  Mapa do Sistema: arquitetura atual confirmada e arquitetura-alvo
    explicitamente separadas.
3.  Glossário: termos realmente utilizados no documento, sem linhas
    vazias ou definições inventadas.
4.  Módulos/Componentes:
    -   contrato de dados normalizados;
    -   coletores por fonte, cada um com seu próprio contexto;
    -   persistência e snapshots;
    -   banco e camada de aplicação;
    -   feed Meta;
    -   ferramentas históricas Node.js/Apps Script/Clasp.
5.  Procedimentos reutilizáveis, ordenados por pré-requisitos e
    dependências.
6.  Decisões e Aprendizados, com motivo, evidência, alternativas e
    estado.
7.  Padrões Reutilizáveis, separados dos módulos concretos.
8.  Itens Não Classificados.
9.  Lacunas e Conflitos.
10. Tabela de Rastreabilidade.
11. Histórico de Atualizações.

A cronologia original deve ser mantida como fonte de auditoria, mas os
fatos devem aparecer no módulo a que pertencem. Quando uma correção
posterior alterar um assunto antigo, o conteúdo atualizado fica junto do
assunto e o histórico registra quando e por que a mudança ocorreu.

## 7. Próxima etapa da análise

Antes de redigir a nova versão do manual, falta concluir a comparação
semântica das fontes por contexto:

1.  Confrontar os módulos do manual v3.0 com os trechos correspondentes
    da transcrição.
2.  Identificar informações, erros, comandos, resultados e decisões
    presentes no histórico e ausentes ou incompletos no manual v3.0.
3.  Comparar o manual v3.0 com a consolidação v1.0, distinguindo
    informação incorporada, duplicada, deslocada ou potencialmente
    perdida.
4.  Verificar os códigos, tabelas, exemplos e comandos sem alterar sua
    lógica.
5.  Fechar o mapa de destino e a rastreabilidade antes da reescrita.

## 8. Checagem desta etapa

-   [x] Fontes acessíveis inventariadas.
-   [x] Tamanhos e extensão estrutural registrados quando disponíveis.
-   [x] Problemas concretos de formatação identificados.
-   [x] Contextos do projeto mapeados preliminarmente.
-   [x] Conflitos e lacunas existentes preservados.
-   [ ] Transcrição revisada semanticamente linha por linha.
-   [ ] Comparação completa entre todos os fatos das fontes e o manual
    consolidado.
-   [ ] Manual principal reescrito e validado.

**Estado final desta etapa:** diagnóstico preliminar concluído. A
reescrita do manual ainda não começou.
