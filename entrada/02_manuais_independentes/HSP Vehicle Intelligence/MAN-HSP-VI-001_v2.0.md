# MANUAL DE ENGENHARIA — HSP VEHICLE INTELLIGENCE

**Código:** `MAN-HSP-VI-001`  
**Versão:** 2.0  
**Data:** 12/10/2026  
**Idioma:** pt-BR  
**Projeto:** HSP Vehicle Intelligence  
**Tipo:** Manual técnico vivo  
**Estado:** Em construção — reorganização contextual; componentes e integrações atuais não foram todos verificados.  
**Fontes principais:** `estrutura-do-manual.md`; `Manual-desenvolvimento.md`; `Manual-HSP-Vehicle-Intelligence-v3.0-integral.md`; `ChatGPT-Criar catálogo de veículos-20260927-0943(1).md`; `MAN-HSP-VI-001_v1.0.md`.  
**Relatórios relacionados:** `AUD-HSP-VI-001_v1.0.md`; `AUD-HSP-VI-002_v1.0.md`.

> **Nota de integridade:** esta versão reorganiza por contexto as informações encontradas nas fontes disponíveis. A transcrição histórica e os documentos anteriores devem permanecer preservados como arquivos-fonte separados. Esta versão não afirma que todo o histórico foi conferido linha a linha, que todos os códigos foram executados ou que a arquitetura descrita está implantada atualmente.

## Resumo do entendimento

O HSP Vehicle Intelligence começou com a geração de um feed automotivo para a Meta e evoluiu para uma plataforma proposta de coleta, normalização, consolidação e inteligência de anúncios de veículos. A investigação histórica abrange D Motors, Quitcar, Milani, Localiza e Super Novos. O projeto também registra uma arquitetura inicial com Supabase e entidades `sources`, `sellers`, `vehicles`, `listings` e `vehicle_images`, seguida por uma arquitetura posterior com PostgreSQL/Neon e entidades `fontes`, `veiculos`, `anuncios` e `snapshots`. Essas versões não devem ser fundidas sem uma decisão documentada. A implementação atual do banco, dos coletores, da API, da interface e do feed ainda precisa ser confirmada.

# 1. Visão Geral

## 1.1 Objetivo

**Descrição registrada:** “Plataforma de coleta, organização e inteligência de mercado de veículos anunciados em Uberlândia.”

**Objetivo técnico registrado:** construir uma base centralizada de veículos anunciados em Uberlândia, preservando fonte, anúncio, vendedor, preço, imagens e histórico.

O projeto pretende evoluir de uma coleta manual e geração de catálogo para um sistema capaz de:

- coletar anúncios de diferentes fontes;
- normalizar os dados em um contrato comum;
- validar e identificar registros duplicados;
- preservar observações históricas;
- analisar preços, tempo anunciado e comportamento de estoque;
- gerar, quando validado, um feed compatível com o catálogo automotivo da Meta.

Esses itens descrevem objetivos e componentes documentados; não comprovam que estejam todos implementados.

## 1.2 Evolução do projeto

A evolução registrada possui etapas diferentes:

1. **Feed automotivo Meta:** investigação de especificações de catálogo e criação de código Apps Script para transformar dados do estoque D Motors.
2. **Base centralizada:** proposta de separar fontes, veículos, anúncios, vendedores e imagens.
3. **Coletores por fonte:** investigação de HTML, APIs, JSON e Firestore para coletar anúncios de várias lojas.
4. **Normalização e consolidação:** definição de um CSV comum com 11 campos.
5. **Histórico e inteligência:** proposta de snapshots, evolução de preços, tempo de estoque e análises.
6. **Arquitetura de aplicação:** referências posteriores a PostgreSQL/Neon, FastAPI, Flet, GitHub e Render.
7. **Feed externo:** geração futura de um feed Meta a partir da base interna, sem misturar o schema externo com os campos internos de inteligência.

**Importante:** as etapas são uma reconstrução lógica da evolução documentada, não uma confirmação de que todas foram concluídas.

## 1.3 Princípios permanentes

1. Preservar dados brutos quando aplicável.
2. Não sobrescrever histórico sem política explícita.
3. Não concluir que um veículo foi vendido apenas porque desapareceu de uma coleta.
4. Não confundir a primeira observação do coletor com a data real de publicação do anúncio.
5. Não assumir que um endpoint contém todo o estoque.
6. Normalizar os campos antes de comparar fontes.
7. Distinguir fato, observação, hipótese, proposta, teste e validação.
8. Preservar erros e tentativas fracassadas.
9. Não declarar código validado sem evidência de teste.
10. Manter o schema do feed Meta separado do modelo interno HSP.
11. Não fundir versões de arquitetura sem registrar a decisão e a evidência.
12. Manter o histórico cronológico como fonte, mas organizar o manual operacional por contexto.

## 1.4 Estado conhecido pelas fontes

| Área | Estado registrado | Limite da evidência |
|---|---|---|
| D Motors | Endpoint e paginação investigados | Contagem histórica; precisa de nova coleta para afirmar estoque atual |
| Quitcar | Estrutura HTML, seletor e paginação investigados | Contagens históricas; precisa de nova coleta |
| Milani | Endpoint estruturado e campos investigados | Contagem histórica; execução atual não confirmada |
| Localiza | `__NEXT_DATA__`, campos, paginação e filtros investigados | Contagens mudaram durante a investigação; mapeamento de `modelo` está em conflito |
| Super Novos | Firestore investigado; execução histórica do gerador reportada | 169 documentos recebidos e 16 ativos após filtros; completude não comprovada |
| CSV HSP | Padrão de 11 campos registrado | Validar implementação atual dos geradores |
| Feed Meta | Modelo e erros históricos registrados na conversa | Arquivo-modelo, código atual e teste atual precisam ser confirmados |
| Banco de dados | Supabase aparece na arquitetura inicial; Neon/PostgreSQL aparece depois | Banco atualmente conectado não confirmado |
| FastAPI/Flet/Render | Aparecem em arquitetura posterior | Implantação e funcionamento atuais não confirmados |
| Histórico/snapshots | Modelo conceitual documentado | Schema real e política de retenção não confirmados |
| Rede de vendedores | Proposta de fase futura na arquitetura inicial | Escopo e implementação atuais não confirmados |

# 2. Mapa do Sistema

## 2.1 Arquitetura conceitual

```text
FONTES DE ANÚNCIOS
  ├── D Motors
  ├── Quitcar
  ├── Milani
  ├── Localiza
  └── Super Novos
          |
          v
INVESTIGAÇÃO DA FONTE
  HTML / API / JSON / Firestore / paginação
          |
          v
COLETOR ESPECÍFICO POR FONTE
          |
          v
DADOS BRUTOS (quando disponíveis)
          |
          v
ADAPTER / NORMALIZAÇÃO
          |
          v
VALIDAÇÃO -> DEDUPLICAÇÃO
          |
          v
CSV NORMALIZADO / PERSISTÊNCIA
          |
          v
BANCO INTERNO (tecnologia atual a confirmar)
  ├── veículos
  ├── anúncios
  ├── snapshots/histórico
  └── fontes e vendedores
          |
          ├── API / análises / interface (estado a confirmar)
          |
          v
GERADOR DE FEED
          |
          v
CATÁLOGO AUTOMOTIVO META (integração a validar)
```

O desenho é conceitual. Não representa uma prova de que todos os componentes estejam conectados em execução.

## 2.2 Responsabilidade de cada camada

| Camada | Responsabilidade | O que não deve fazer |
|---|---|---|
| Fonte | Publicar anúncios e dados de estoque | Não é controlada pelo HSP |
| Investigação | Descobrir origem dos dados, filtros e paginação | Não presumir uma API sem evidência |
| Coletor | Obter dados de uma fonte específica | Não misturar regras de todas as lojas em um único scraper genérico |
| Adapter/normalização | Converter campos da fonte para o padrão HSP | Não inventar valores ausentes |
| Validação | Verificar tipos, IDs, preço, URL, imagem e campos exigidos | Não afirmar completude só porque o processo terminou |
| Deduplicação | Identificar anúncios ou veículos potencialmente repetidos | Não unir veículos somente por marca/modelo/ano |
| Persistência | Gravar dados e manter relações | Não substituir histórico sem regra explícita |
| Snapshot | Registrar o estado observado em uma data/hora | Não chamar a data de observação de data de publicação |
| Gerador de feed | Mapear dados internos para o formato externo da Meta | Não alterar o modelo interno para imitar o feed |
| API/interface | Expor e apresentar os dados | Estado atual precisa ser confirmado |

## 2.3 Arquiteturas históricas distintas

### Arquitetura inicial — proposta com Supabase

O histórico inicial propôs:

```text
coletores
  -> normalização
  -> validação
  -> deduplicação
  -> Supabase / PostgreSQL
  -> pesquisa / inteligência / API
  -> rede de vendedores
```

A estrutura de projeto proposta incluía `config/`, `collectors/`, `processors/`, `models/`, `database/`, `services/`, `api/`, `dashboard/`, `tests/` e `main.py`.

### Arquitetura posterior — proposta com PostgreSQL/Neon

O manual integral posterior registrou:

```text
Flet
  -> HTTP/API
  -> FastAPI
  -> SQLAlchemy
  -> Alembic
  -> PostgreSQL / Neon
```

GitHub foi associado ao código e versionamento. Object Storage foi proposto para HTML, JSON bruto, imagens e exportações grandes. Parquet/DuckDB foram citados como opções futuras para análises de maior volume.

**CON-HSP-VI-001-001 — Supabase versus Neon/PostgreSQL:** não escolher qual banco está ativo apenas pela cronologia dos documentos. Conferir o repositório e a configuração atuais.

# 3. Glossário

| Termo | Explicação |
|---|---|
| API | Interface pela qual um programa solicita dados ou operações a outro sistema. |
| Endpoint | Endereço específico de uma API. |
| HTML | Estrutura de uma página web. |
| JavaScript | Linguagem usada para comportamento interativo e carregamento de dados em páginas. |
| JSON | Formato de texto para dados estruturados. |
| CSV | Arquivo de texto com campos separados por delimitadores. |
| Coletor | Programa que busca dados em uma fonte. |
| Adapter | Componente que converte o formato de uma fonte para um padrão comum. |
| Normalização | Transformação de dados para um padrão comum. |
| Validação | Verificação de que os dados atendem a regras esperadas. |
| Deduplicação | Identificação e tratamento de registros repetidos. |
| ID | Identificador de um registro. |
| Paginação | Divisão de uma lista em páginas menores. |
| DevTools | Ferramentas do navegador usadas para investigar páginas e requisições. |
| Network | Aba do DevTools que mostra requisições de rede. |
| Fetch/XHR | Categoria de requisições usada para buscar dados sem recarregar a página inteira. |
| Firestore | Banco de dados de documentos investigado na fonte Super Novos. |
| Snapshot | Registro do estado observado de um anúncio em determinada data/hora. |
| Schema | Estrutura de campos e tipos de dados. |
| Listing/anúncio | Oferta publicada por uma fonte ou vendedor para um veículo. Um mesmo veículo pode ter vários anúncios. |
| Vehicle/veículo | Entidade que representa o veículo físico, potencialmente relacionado a vários anúncios. |
| Source/fonte | Site, marketplace ou origem dos dados. |
| Seller/vendedor | Empresa ou pessoa que publica ou oferece um veículo, conforme dados disponíveis. |
| VIN | Número de identificação do veículo. Não deve ser preenchido com um ID interno inventado. |
| Feed | Arquivo estruturado enviado a uma plataforma externa para importar itens. |
| Meta Catalog | Catálogo externo usado pela plataforma Meta; os requisitos devem ser conferidos na especificação aplicável. |
| PostgreSQL | Sistema de banco de dados relacional. |
| Neon | Serviço de PostgreSQL hospedado na nuvem, citado na arquitetura posterior. |
| Supabase | Plataforma de dados citada na arquitetura inicial. |
| FastAPI | Framework Python para criar APIs. |
| Flet | Framework para construir interfaces usando Python. |
| SQLAlchemy | Biblioteca Python para acesso a bancos relacionais. |
| Alembic | Ferramenta para versionar mudanças na estrutura do banco. |
| Git/GitHub | Controle de versões e hospedagem de repositórios. |
| Render | Plataforma de hospedagem mencionada no projeto. |
| Google Apps Script | Ambiente do Google para executar scripts integrados a serviços Google. |
| Clasp | Ferramenta de linha de comando para gerenciar projetos Google Apps Script. |
| Object Storage | Armazenamento de arquivos/objetos, inclusive arquivos grandes. |
| Parquet/DuckDB | Tecnologias mencionadas como opções para análises de maior volume. |
| Pricing Engine | Módulo proposto para inteligência de preços. |
| MVP | Primeira versão mínima que entrega o objetivo central. |

# 4. Módulos / Componentes

## 4.1 Modelo de dados e evolução arquitetural

### 4.1.1 Modelo inicial proposto

A arquitetura inicial descreveu um modelo conceitual com cinco entidades:

| Entidade histórica | Finalidade registrada | Campos/relacionamentos citados |
|---|---|---|
| `sources` | Fontes de dados | `id`, `name`, `type`, `base_url`, `active`, `created_at` |
| `sellers` | Vendedores/empresas | `id`, `name`, `company`, `phone`, `whatsapp`, `city`, `state`, `source_id`, `created_at` |
| `vehicles` | Veículo físico | `id`, `make`, `model`, `version`, `year`, `mileage`, `price`, `fuel`, `transmission`, `body_style`, `color`, `city`, `state`, `created_at`, `updated_at` |
| `listings` | Anúncio de um veículo em uma fonte | `id`, `vehicle_id`, `source_id`, `seller_id`, `external_id`, `url`, `title`, `price`, `status`, `first_seen`, `last_seen`, `created_at`, `updated_at` |
| `vehicle_images` | Imagens relacionadas a veículo/anúncio | `id`, `vehicle_id`, `listing_id`, `url`, `position`, `created_at` |

O histórico explica que um mesmo veículo pode aparecer em D Motors, OLX, Webmotors e sites de revendas. Por isso, veículo e anúncio não devem ser tratados automaticamente como a mesma entidade.

**Estado:** proposta histórica; não prova que essas tabelas tenham sido criadas no banco atual.

### 4.1.2 Modelo posterior registrado

O manual técnico posterior descreve:

| Entidade posterior | Finalidade conceitual |
|---|---|
| `fontes` | Cadastro das fontes |
| `veiculos` | Cadastro interno dos veículos |
| `anuncios` | Anúncios publicados nas fontes |
| `snapshots` | Observações históricas de anúncios ao longo do tempo |

A relação conceitual registrada é:

```text
fonte
  -> coleta
  -> comparar com observação anterior
  -> novo anúncio: criar registro
  -> anúncio existente: registrar snapshot
  -> preço alterado: registrar mudança
  -> anúncio ausente: registrar ausência observada
```

**CON-HSP-VI-001-002 — evolução do modelo de dados:** o modelo inicial `sources/sellers/vehicles/listings/vehicle_images` e o modelo posterior `fontes/veiculos/anuncios/snapshots` são versões documentais distintas. Não são sinônimos exatos e não devem ser mesclados como se coexistissem no banco sem consultar o schema real.

### 4.1.3 Deduplicação

O histórico propôs um `vehicle_fingerprint` baseado em várias evidências, incluindo VIN, ID externo, URL, placa parcial, marca, modelo, ano, quilometragem, preço e imagens.

**Ponto de atenção:** marca, modelo e ano, isoladamente, não identificam um veículo de forma única. A estratégia real de deduplicação ainda precisa ser definida e validada.

## 4.2 Contrato de dados normalizados

**Código:** `COD-HSP-VI-001-001`  
**Estado:** padrão registrado; implementação atual precisa ser conferida.

O CSV comum deve conter exatamente estes 11 campos e nesta ordem:

```text
fonte
id_veiculo
marca
modelo
descricao
ano_fabricacao
ano_modelo
km
preco
url
imagem
```

| Regra | Aplicação |
|---|---|
| Manter o contrato comum | Não acrescentar campos exclusivos de uma fonte ao CSV comum sem decisão formal. |
| Preservar dados específicos | Guardar campos adicionais no JSON bruto ou em estrutura própria quando necessário. |
| Não inventar valores | Campo ausente deve permanecer ausente ou seguir regra explícita de normalização. |
| Validar os registros | Conferir IDs, tipos, URLs, imagens e duplicados. |
| Registrar a coleta | Registrar data, fonte e escopo da coleta. |
| Distinguir código de validação | A existência de um arquivo gerador não prova que esteja funcional. |

Estrutura de pastas histórica:

```text
saida/
├── dados_dmotors/
│   ├── dmotors_gerador.py
│   ├── dmotors.json
│   └── dmotors.csv
├── dados_quitcar/
├── dados_milani/
├── dados_localiza/
└── dados_superNovos/
```

Trecho registrado para definir a pasta de saída:

```python
PASTA_SAIDA = Path(__file__).resolve().parent
```

Este trecho é apenas uma linha de configuração, não um programa completo. Ele pressupõe que `Path` esteja importado. Não adicionar imports a uma versão histórica sem marcar a alteração.

## 4.3 Coletor D Motors

**Código:** `INF-HSP-VI-001-001`  
**Estado:** investigação registrada; resultados históricos.

**Site:** `https://dmotorsudi.com.br`  
**Estoque:** `https://dmotorsudi.com.br/estoque/`

Endpoint observado:

```http
GET https://dmotorsudi.com.br/stock?pagina=1&registros_por_pagina=18
```

Resposta histórica observada: status `200`, JSON com `data`, `total`, `pagina` e `total_paginas`. Também foram mencionados `unifiedStock`, `count` e `filteredCount`.

Um teste histórico encontrou `total = 45` e `total_paginas = 3`. Esse total não é uma contagem atual garantida.

**Procedimento de investigação:** abrir o estoque, abrir DevTools → Network, recarregar, localizar a requisição `/stock`, examinar a resposta, conferir os campos de paginação e comparar a quantidade coletada com a contagem retornada.

## 4.4 Coletor Quitcar

**Código:** `INF-HSP-VI-001-002`  
**Estado:** investigação HTML registrada; resultados históricos.

**Site:** `https://quitcar.com.br`  
**Estoque:** `https://quitcar.com.br/estoque`

Seletor CSS observado:

```css
.card.card-car
```

Campos identificados historicamente: marca, modelo, descrição, ano, quilometragem, preço, imagem e URL. O ID era obtido do final da URL.

Exemplo de URL de paginação:

```text
https://quitcar.com.br/estoque?registros_por_pagina=18&pagina=2
```

Contagens históricas registradas:

| Página | Registros observados |
|---:|---:|
| 3 | 18 |
| 4 | 18 |
| 5 | 17 |
| 6 | 0 |
| Total histórico citado | 89 |

Outra etapa da conversa registrou 87 veículos em um HTML examinado. As contagens 87 e 89 ocorreram em momentos/contextos diferentes; não devem ser tratadas como uma única contagem atual.

Informações de contato registradas no histórico:

```text
João Pinheiro, 2875
Nossa Senhora Aparecida
Uberlândia/MG
CEP 38400712
(34) 3235-3324
```

**Procedimento:** inspecionar os cartões HTML, identificar os campos, localizar o ID na URL, verificar paginação, normalizar e registrar data/resultado. Não afirmar que a loja usa uma API pública apenas porque existe JavaScript no site.

## 4.5 Coletor Milani

**Código:** `INF-HSP-VI-001-003`  
**Estado:** investigação registrada; resultados históricos.

**Site:** `https://milaniveiculos.com/estoque/`

O HTML inicial apresentava `Carregando estoque...`. Foram observados os termos:

```text
StockClient
stockVersion: v1
stockPagination: paginacao
vehicleSegment: car
hidePrice: false
```

Endpoint observado:

```http
GET /stock?pagina=1&registros_por_pagina=18
```

Contagem histórica: `total = 102`, `total_paginas = 6`.

Campos encontrados:

```text
id
modelo_nome
marca_name
tipo_name
cor_name
combustivel_name
cambio_name
carroceria_name
anofabricacao
anomodelo
km
foto
valorvenda
valorproposta
versao_descricao
publicacao
atualizacao
revenda_name
fotos
```

O campo `fotos` continha objetos de imagem.

**Aprendizado:** quando o HTML inicial é dinâmico, investigar scripts e requisições Network antes de decidir como coletar. A contagem 102 é histórica.

## 4.6 Coletor Localiza

**Código:** `INF-HSP-VI-001-004`  
**Estado:** investigação registrada; contagens históricas variáveis.

**Site nacional:** `https://seminovos.localiza.com/carros`  
**Página regional:** `https://seminovos.localiza.com/carros/mg-uberlandia`

A página continha `__NEXT_DATA__`.

Observação histórica regional:

```text
_pagina: 1
_total: 245
_totalPaginas: 11
_tamanhoPaginaAtual: 23
```

Contagens registradas:

| Escopo/página | Resultado histórico |
|---|---:|
| Uberlândia, páginas 1–10 | 23 veículos por página |
| Uberlândia, página 11 | 15 veículos |
| Uberlândia, total citado | 245 |
| Duplicados na comparação citada | 0 |
| Nacional, total observado em uma etapa | 23187 |
| Nacional, páginas observadas | 1009 |
| Página 1009 em outro momento | `_total = 23188`, tamanho 4, IDs 468262–468265 |

Os valores nacionais mudaram durante a investigação. Não são contagens atuais garantidas.

Comando histórico para salvar a página 2:

```bash
curl -L "https://seminovos.localiza.com/carros?page=2" -o ./localiza_brasil_pagina2.html
```

Campos observados:

```text
id
marcaDescricao
modeloDescricao
versaoDescricao
corDescricao
anoModelo
anoFabricacao
odometro
preco
precoDe
desconto
cidadeDescricao
siglaEstado
siglaLoja
fotoUrl
pdpUrl
premium
blindado
bonus
origem
caracteristicas
```

Exemplo histórico de veículo:

| Campo | Valor registrado |
|---|---|
| ID | `429003` |
| Marca/modelo | Volkswagen T-Cross Highline |
| Ano modelo | 2025 |
| Ano fabricação | 2024 |
| Quilometragem | 47.950 km |
| Preço | R$ 138.990 |
| Cidade | Uberlândia |
| Loja | `VCUDI` |

Mapeamento histórico proposto:

| Campo HSP | Campo Localiza |
|---|---|
| `fonte` | `localiza` |
| `id_veiculo` | `id` |
| `marca` | `marcaDescricao` |
| `modelo` | `modeloDescricao` em uma versão; `modeloFamiliaDescricao` em outra |
| `descricao` | `modeloDescricao` |
| `ano_fabricacao` | `anoFabricacao` |
| `ano_modelo` | `anoModelo` |
| `km` | `odometro` |
| `preco` | `preco` |
| `url` | `pdpUrl` |
| `imagem` | `fotoUrl` |

**CON-HSP-VI-001-003 — mapeamento `modelo`:** as fontes contêm as alternativas `modeloDescricao` e `modeloFamiliaDescricao`. Não selecionar uma regra definitiva sem inspecionar o coletor vigente e exemplos de resposta atuais.

A investigação de `searchToUrl` registrou filtros para veículos, categorias, câmbios, combustíveis, cores, motores, portas, anos, quilometragem, preços, cidade, blindado, ofertas, premium, placa, opcionais e lojas.

Ordenações observadas:

```text
mais_relevantes
menor_km
ano_mais_recente
mais_recente
mais_proximos
menor_preco
maior_preco
```

A rota regional usa slug específico, como `mg-uberlandia`. Não inferir filtros apenas pela aparência da URL.

## 4.7 Coletor Super Novos / Firestore

**Código:** `INF-HSP-VI-001-005`  
**Estado:** investigação e execução histórica registradas; completude pendente.

Arquivos de investigação citados:

```text
supernovos.html
supernovos_main.js
investigacao_api.txt
investigacao_firebase.txt
supernovos_firestore_teste.json
supernovos_campos.txt
supernovos_amostra_campos.txt
investigacao_url.txt
investigacao_url2.txt
```

Configuração encontrada:

```text
projectId = intermedio-1513801146022
databaseURL = https://intermedio-1513801146022.firebaseio.com
```

ID de revenda investigada:

```text
oewBLc6dFJ3wis0UQ6pZ
```

Caminho de coleção observado:

```text
revenda/
└── oewBLc6dFJ3wis0UQ6pZ/
    └── veiculos/
```

Consulta encontrada no JavaScript do site:

```javascript
collection("revenda")
  .doc(ID)
  .collection("veiculos")
  .where("veremovido", "==", 0)
  .where("vevendido", "==", 0)
  .orderBy("updated_at", "desc")
```

A interface também aplicava o filtro:

```javascript
veexibir_site !== false
```

Comando REST histórico:

```bash
curl -L "https://firestore.googleapis.com/v1/projects/intermedio-1513801146022/databases/(default)/documents/revenda/oewBLc6dFJ3wis0UQ6pZ/veiculos?pageSize=5" -o supernovos_firestore_teste.json
```

O teste foi registrado como funcional e salvou aproximadamente 198 KB.

Campos observados:

```text
id
imagens
created_at
updated_at
veano_fabricacao
veblindado
vecambio
vecarroceria
vecor
veobservacao
vequilometragem
vevalor
vefipe_marca
vefipe_name
vefipe_ano_modelo
vevendido
veremovido
veexibir_site
opcionais
locais_anuncio
```

Amostra histórica:

| Campo | Valor |
|---|---|
| `vefipe_marca` | `CHEVROLET` |
| `vefipe_name` | `ONIX HATCH LT 1.4 8V FLEXPOWER 5P MEC.` |
| `veano_fabricacao` | `2016` |
| `vefipe_ano_modelo` | `2016` |
| `vequilometragem` | `107500` |
| `vevalor` | `49900.0` |

As imagens continham `fileUrl` em Cloudinary.

Mapeamento proposto para o CSV HSP:

| Campo HSP | Campo Firestore ou regra |
|---|---|
| `fonte` | `supernovos` |
| `id_veiculo` | `id` |
| `marca` | `vefipe_marca` |
| `modelo` | `vefipe_name` |
| `descricao` | `veobservacao` |
| `ano_fabricacao` | `veano_fabricacao` |
| `ano_modelo` | `vefipe_ano_modelo` |
| `km` | `vequilometragem` |
| `preco` | `vevalor` |
| `url` | `https://supernovos.com.br/veiculo/{id}` |
| `imagem` | primeira `imagens[].fileUrl` |

Tentativas históricas de `runQuery`:

| Caminho tentado | Resultado registrado |
|---|---|
| `/databases/(default):runQuery` | `404` |
| `/databases/(default)/documents:runQuery` | `403 PERMISSION_DENIED` |

Decisão histórica: usar o GET da coleção já testado até haver nova evidência; não insistir nas rotas que falharam sem investigar a causa.

Erros registrados durante a criação do gerador:

1. Um wrapper tentou abrir `/mnt/data/supernovos_gerador.py` e ocorreu `FileNotFoundError`.
2. Uma versão de arquivo estava incompleta e terminava em `documento_firestore(...)`.
3. Havia um delimitador `'''` residual no final.

Comando de execução histórico:

```bash
python3 saida/dados_superNovos/supernovos_gerador.py
```

Saída registrada:

```text
[1/4] Consultando Firestore...
       Documentos recebidos: 169
       Ativos após filtros: 16
       Ignorados pelos filtros: 153
[2/4] Normalizando dados...
       Veículos normalizados: 16
[3/4] Salvando JSON...
[4/4] Salvando CSV...

Concluído.
Total: 16
Problemas: 0
```

Arquivos de saída registrados:

```text
saida/dados_superNovos/supernovos_estoque.json
saida/dados_superNovos/supernovos_estoque.csv
```

**Interpretação correta:** o processo reportou zero problemas durante aquela execução, mas isso não prova que o estoque inteiro do site foi coletado. A existência de outras revendas, filtros, agregação ou paginação permanece hipótese a investigar.

**LAC-HSP-VI-001-001:** o código completo atual do coletor Super Novos não foi confirmado nas fontes disponíveis para esta consolidação. Não reconstruir nem inventar o restante do arquivo.

## 4.8 Feed automotivo Meta

**Código:** `MOD-HSP-VI-001-META`  
**Estado:** histórico técnico e tentativas preservados; especificação/arquivo de feed vigente e integração atual ainda precisam ser verificados.

### 4.8.1 Objetivo e separação de responsabilidades

A fase inicial do projeto tinha como objetivo ler o estoque D Motors e gerar uma planilha/arquivo no formato de catálogo automotivo da Meta. O histórico inclui Google Apps Script, um `package.json` para Clasp e código com funções de consulta, transformação, geração de planilha, diagnóstico e resumo.

A arquitetura pretendida deve manter separados:

```text
DADOS DA FONTE
  -> normalização HSP
  -> validação
  -> mapeamento para o schema externo Meta
  -> validação do feed
  -> envio/teste no catálogo Meta
```

O CSV comum HSP com 11 campos não é o mesmo artefato que o feed Meta. O feed externo pode exigir campos e formatos próprios.

### 4.8.2 Histórico de modelo e campos

A conversa registra que foi analisado um arquivo chamado `catalog_vehicles.csv`, descrito no histórico como um modelo de 98 colunas e três linhas relevantes: uma linha de descrição/obrigatoriedade, outra de nomes técnicos e uma linha de exemplo.

O histórico lista como campos obrigatórios identificados naquela análise:

| Campo | Finalidade registrada |
|---|---|
| `vehicle_id` | ID do veículo |
| `title` | Título |
| `description` | Descrição |
| `price` | Preço |
| `image[0].url` | Imagem principal |
| `image[0].tag[0]` | Tag da imagem |
| `url` | Link do anúncio |
| `address.addr1` | Endereço |
| `address.city` | Cidade |
| `address.region` | Estado/região |
| `address.country` | País |
| `latitude` | Latitude |
| `longitude` | Longitude |
| `neighborhood[0]` | Bairro |
| `make` | Marca |
| `model` | Modelo |
| `year` | Ano |
| `body_style` | Carroceria |
| `state_of_vehicle` | Estado do veículo |
| `mileage.unit` | Unidade da quilometragem |
| `mileage.value` | Quilometragem |

**Limite da evidência:** o arquivo `catalog_vehicles.csv` não está entre os arquivos-fonte disponíveis nesta consolidação. Portanto, os campos acima são reproduzidos como resultados registrados na conversa, não como uma nova verificação independente do arquivo ou da especificação atual da Meta.

### 4.8.3 Erros históricos do feed

A conversa registra uma análise de um CSV com 45 veículos:

| Verificação histórica | Resultado registrado |
|---|---:|
| Veículos | 45 |
| Com imagens | 35 |
| Sem imagens | 10 |
| IDs duplicados | 0 |
| URLs duplicadas | 0 |
| URLs HTTPS válidas | 45 |
| VIN preenchido | 45 |

Foi registrado que `vin` estava preenchido com o mesmo valor de `vehicle_id` nos 45 veículos. Isso não é um VIN real e não deve ser repetido como se fosse. O campo `vehicle_registration_plate` estava vazio nos 45 registros.

Um relatório de erros Meta foi descrito assim:

| Verificação | Resultado registrado |
|---|---:|
| Linhas de erro | 88 |
| Veículos únicos com erro | 44 |
| Resultado | `Item não carregado` |
| Problema reportado | `Valores inválidos` |
| Veículo que não aparecia no relatório | 1 |

O relatório foi descrito como genérico e não apontava qual campo específico era inválido. Logo, não há base para afirmar que VIN, placa ou imagem foi a única causa da rejeição.

### 4.8.4 Plano de teste histórico

A proposta registrada para a versão seguinte do feed foi:

1. remover o VIN falso, em vez de reutilizar `vehicle_id` como VIN;
2. retirar `vehicle_registration_plate` enquanto não for necessário e não houver valor válido;
3. excluir veículos sem imagem para o primeiro teste, se o campo for obrigatório na especificação aplicável;
4. manter os dados básicos;
5. validar campos e formatos antes de gerar o arquivo;
6. testar com poucos veículos antes de gerar o feed completo.

Esse plano é uma proposta histórica; as fontes disponíveis não comprovam que o teste posterior tenha sido concluído com sucesso.

### 4.8.5 Código Apps Script e versões

A transcrição histórica contém versões de `Código.gs`/`Código.js` com constantes como `CAMPOS_META` e funções como `_buscarTodoEstoque()`, `_transformarVeiculo()`, `_obterFotos()`, `diagnosticarVeiculoMeta()` e `resumoFeedMeta()`. O histórico registra várias substituições e ajustes de código.

**Regra:** não selecionar um bloco histórico como versão definitiva sem comparar com o arquivo atual do projeto. O código completo histórico permanece na fonte `ChatGPT-Criar catálogo de veículos-20260927-0943(1).md`; esta versão do manual não reproduz todos os rascunhos para não apresentar uma variante antiga como código vigente.

**LAC-HSP-VI-001-002:** o arquivo-modelo Meta e os arquivos de erro citados no histórico precisam ser localizados novamente para uma comparação independente.  
**LAC-HSP-VI-001-003:** o código atual do feed, a especificação vigente e um teste atual no Commerce Manager não foram verificados.

## 4.9 Google Apps Script, Node.js e Clasp — componente histórico

**Código:** `INF-HSP-VI-001-006`  
**Estado:** histórico preservado; relação com a arquitetura atual a confirmar.

O projeto usou Node.js e Clasp para integração local com Google Apps Script. O histórico registra:

- Node.js não utiliza `source .venv/bin/activate` como o ambiente virtual Python;
- dependências locais ficam normalmente em `node_modules`;
- `package.json` registra scripts e dependências;
- NVM foi mencionado para isolar versões de Node.js;
- Clasp foi instalado localmente;
- a API do Google Apps Script precisava ser ativada nas configurações da conta;
- `.claspignore` foi discutido para evitar o envio de arquivos locais indevidos ao Apps Script.

Comando histórico:

```bash
npm install --save-dev @google/clasp
```

`package.json` histórico:

```json
{
  "name": "hsp-vehicle-intelligence",
  "version": "1.0.0",
  "description": "",
  "main": "gerador_feed.js",
  "scripts": {
    "login": "clasp login",
    "clone": "clasp clone",
    "push": "clasp push",
    "pull": "clasp pull",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "type": "commonjs",
  "devDependencies": {
    "@google/clasp": "^2.5.1"
  }
}
```

Atalhos registrados:

```bash
npm run login
npm run clone
npm run push
npm run pull
```

Eles executam, conforme o `package.json` histórico, `clasp login`, `clasp clone`, `clasp push` e `clasp pull`.

**Risco:** `push` envia arquivos ao Apps Script. Conferir o projeto de destino e a lista de arquivos antes de executar. A configuração histórica não prova que esse fluxo ainda seja utilizado.

## 4.10 Histórico, snapshots e inteligência de preços

**Código:** `DEC-HSP-VI-001-001`  
**Estado:** proposta conceitual; schema real e persistência atual não confirmados.

Campos históricos potenciais:

```text
id_veiculo
data_primeira_coleta
data_ultima_coleta
preco_primeira_coleta
preco_ultima_coleta
quantidade_alteracoes_preco
maior_preco
menor_preco
data_saida_estoque
```

Análises propostas:

- dias em estoque;
- tempo médio até saída por modelo/faixa de preço;
- redução de preço versus tempo;
- giro por marca/modelo;
- comportamento por loja;
- evolução histórica de preços.

**Regra de interpretação:** a primeira coleta é a primeira observação conhecida pelo sistema, não necessariamente a data de publicação do anúncio. Se o anúncio desaparecer, registrar a ausência observada; não inferir venda automaticamente.

## 4.11 Escala e armazenamento

O histórico considerou uma escala conceitual de aproximadamente 600.000 anúncios e uma média hipotética de 500 bytes por snapshot.

| Estimativa histórica | Valor |
|---|---:|
| Uma coleta de 600.000 anúncios | ~300 MB |
| Coleta diária | ~9 GB/mês |
| Um ano | ~110 GB |
| Quatro coletas por dia | ~36 GB/mês |

São estimativas conceituais, não medições de produção. O volume real depende dos campos, índices, JSON, imagens, retenção e compressão.

Tecnologias citadas:

| Tecnologia/camada | Uso considerado |
|---|---|
| GitHub | Código, versionamento e configuração |
| Banco relacional | Dados estruturados |
| Object Storage | HTML, JSON bruto, imagens e exportações grandes |
| Parquet/DuckDB | Análises de grande volume, se necessário |

## 4.12 Rede de vendedores — proposta histórica

A arquitetura inicial incluiu uma fase futura de rede de vendedores, com possibilidade de relacionar vendedores, anúncios e oportunidades. A proposta não é evidência de implementação.

**Estado:** ideia/proposta histórica. Confirmar se continua dentro do escopo atual antes de tratá-la como módulo ativo.

# 5. Procedimentos

## 5.1 PROC-HSP-VI-001-001 — Investigar uma nova fonte

**Objetivo:** descobrir como o site disponibiliza os anúncios antes de escrever um coletor.  
**Quando usar:** ao adicionar um novo site ou quando a fonte muda sua estrutura.  
**Pré-requisitos:** URL da fonte, navegador e acesso às ferramentas de desenvolvedor.  
**Entradas:** página inicial e página de estoque.  
**Saída:** evidências sobre HTML/API/JSON, paginação, campos e filtros.

1. Abra o site no navegador.
2. Registre a URL da página de estoque.
3. Abra as ferramentas de desenvolvedor do navegador.
4. Selecione a aba **Network**.
5. Recarregue a página.
6. Examine as requisições `Fetch/XHR`.
7. Se não houver dados de estoque, examine a requisição `Doc` e o HTML.
8. Registre a URL da requisição, parâmetros, status e estrutura de resposta.
9. Identifique como a paginação funciona.
10. Mapeie os campos da fonte para o contrato HSP.
11. Salve evidências e a data da investigação.
12. Só então implemente ou altere o coletor.

**Validação:** outra pessoa deve conseguir localizar a requisição e reconhecer os campos usando as evidências registradas.  
**Falhas:** se não houver requisição clara, não presumir API; investigar HTML, JavaScript e dados carregados no cliente.  
**Risco:** não compartilhar cookies, tokens, cabeçalhos de autenticação ou credenciais.

## 5.2 PROC-HSP-VI-001-002 — Validar um coletor

**Objetivo:** verificar se a execução gerou dados utilizáveis, sem confundir execução sem erro com coleta completa.

1. Registrar o comando e a versão do arquivo executado.
2. Registrar data/hora e fonte consultada.
3. Conferir a quantidade de registros recebidos.
4. Conferir a quantidade de registros após filtros.
5. Comparar a contagem com a fonte, quando disponível.
6. Verificar os 11 campos do CSV HSP.
7. Conferir IDs, URLs, preços, anos, quilometragem e imagens.
8. Procurar registros duplicados.
9. Registrar mensagens de erro e avisos.
10. Guardar o resultado bruto e o CSV produzido.
11. Marcar o estado como testado ou validado somente conforme as evidências.

**Saída esperada:** log de execução, dados gerados e checklist de validação.  
**Falha comum:** um coletor pode terminar sem exceções e ainda assim coletar apenas parte do estoque.

## 5.3 PROC-HSP-VI-001-003 — Tratar anúncio ausente em uma coleta

1. Registrar que o anúncio não apareceu na coleta atual.
2. Conferir se a fonte estava acessível e se a coleta terminou.
3. Conferir paginação e filtros.
4. Comparar o resultado com a coleta anterior.
5. Registrar a ausência observada sem marcar venda automaticamente.
6. Só definir `data_saida_estoque` quando existir uma regra explícita e evidência suficiente.

**Saída:** evento de ausência observada e evidência da coleta.  
**Estado:** regra conceitual; persistência real a confirmar.

## 5.4 PROC-HSP-VI-001-004 — Medir arquivos CSV

Comando histórico:

```bash
find . -type f -name "*.csv" -exec ls -lh {} \;
```

**Objetivo:** listar arquivos CSV e seus tamanhos no diretório atual e subdiretórios.  
**Terminal/pasta:** terminal, na raiz do projeto que se deseja inspecionar.  
**Saída histórica registrada:**

| Arquivo | Tamanho citado |
|---|---:|
| `localiza_estoque.csv` | 93 KB |
| `dmotors.csv` | 18 KB |
| `dados_dmotors/dmotors.csv` | 18 KB |
| `milani_estoque.csv` | 120 KB |
| `quitcar_estoque.csv` | 26 KB |

Esses tamanhos são registros históricos, não resultados atuais.  
**Validação:** confirmar que os caminhos e arquivos listados pertencem ao diretório correto.

## 5.5 PROC-HSP-VI-001-005 — Baixar uma página da Localiza

Comando histórico:

```bash
curl -L "https://seminovos.localiza.com/carros?page=2" -o ./localiza_brasil_pagina2.html
```

**Objetivo:** salvar a resposta da página 2 para inspeção local.  
**Saída:** `localiza_brasil_pagina2.html` no diretório atual.  
**Validação:** confirmar que o arquivo existe e contém HTML da página esperada. O comando não valida por si só o número total de veículos.

## 5.6 PROC-HSP-VI-001-006 — Instalar e usar Clasp no projeto histórico

**Pré-requisito:** Node.js/npm instalados e acesso autorizado à conta Google usada pelo projeto.  
**Comando de instalação:**

```bash
npm install --save-dev @google/clasp
```

Comandos históricos:

```bash
npm run login
npm run clone
npm run push
npm run pull
```

1. Conferir a pasta atual do projeto.
2. Conferir o `package.json` e o projeto Apps Script de destino.
3. Executar `npm run login` para autenticar, se esse fluxo ainda for usado.
4. Conferir o ID e o conteúdo local antes de clonar ou sincronizar.
5. Antes de `npm run push`, revisar `.claspignore` e a lista de arquivos que serão enviados.
6. Após a operação, conferir o resultado no terminal e no Apps Script.

**Risco:** `push` altera o conteúdo do projeto remoto. Não executar sem conferir o destino e os arquivos incluídos.  
**Estado:** procedimento histórico; uso atual não confirmado.

## 5.7 PROC-HSP-VI-001-007 — Validar o feed Meta

1. Localizar a especificação ou arquivo-modelo efetivamente usado.
2. Confirmar cabeçalhos e campos obrigatórios no modelo correspondente.
3. Separar os campos internos HSP dos campos externos Meta.
4. Não preencher VIN com `vehicle_id`.
5. Verificar se os veículos possuem imagens quando a especificação exigir imagem.
6. Validar endereço, localização, preço, ano, quilometragem e estado do veículo conforme a especificação aplicável.
7. Gerar um arquivo pequeno de teste.
8. Registrar o arquivo enviado, data, resultado e erros do catálogo.
9. Corrigir uma categoria de problema por vez.
10. Só declarar o feed validado após evidência de importação aceita.

**Estado:** procedimento proposto a partir do histórico; não há comprovação de uma validação atual bem-sucedida.

# 6. Decisões e Aprendizados

| Código | Decisão/aprendizado | Motivo/evidência | Estado |
|---|---|---|---|
| `DEC-HSP-VI-001-001` | Preservar histórico de anúncios/snapshots | Permite comparar preço e tempo anunciado | Proposta conceitual |
| `DEC-HSP-VI-001-002` | Separar schema Meta do modelo interno HSP | Feed é contrato externo; dados internos têm outros objetivos | Princípio arquitetural registrado |
| `DEC-HSP-VI-001-003` | Usar CSV HSP comum com 11 campos | Facilita consolidação entre fontes | Padrão registrado; implementação atual a conferir |
| `DEC-HSP-VI-001-004` | Preservar JSON bruto quando aplicável | Mantém campos da fonte para reprocessamento | Padrão registrado |
| `DEC-HSP-VI-001-005` | Ausência de anúncio não prova venda | Pode haver mudança de página, filtro, falha ou estoque alterado | Princípio registrado |
| `DEC-HSP-VI-001-006` | Endpoint não prova completude | Paginação, filtros e escopo podem limitar os resultados | Princípio registrado |
| `DEC-HSP-VI-001-007` | Investigar a requisição real antes de escrever coletor | Evita escolher método de extração por suposição | Procedimento registrado |
| `DEC-HSP-VI-001-008` | Manter Apps Script/Clasp como trilha histórica até confirmar o uso atual | O projeto evoluiu para coletores Python e outra arquitetura | Estado atual desconhecido |
| `DEC-HSP-VI-001-009` | Não reutilizar `vehicle_id` como VIN | O histórico do feed registra esse erro nos 45 registros | Correção necessária em qualquer feed futuro |
| `DEC-HSP-VI-001-010` | Não declarar o estoque Super Novos completo com base em 16 registros | Teste recebeu 169 documentos, 16 ativos após filtros | Completude não comprovada |

# 7. Padrões Reutilizáveis

## 7.1 Padrão de novo coletor

1. Investigar a fonte.
2. Registrar URL, método de coleta e paginação.
3. Preservar a resposta bruta quando aplicável.
4. Implementar um adaptador específico para a fonte.
5. Mapear para os 11 campos HSP.
6. Validar tipos, campos, URLs, imagens e IDs.
7. Deduplicar conforme regra explícita.
8. Gerar JSON/CSV.
9. Registrar log, contagens e data.
10. Documentar falhas e limites.

## 7.2 Padrão de registro de erro

Cada erro deve ter:

- código `ERR`;
- fonte/arquivo e versão;
- mensagem exata;
- comando ou ação executada;
- resultado observado;
- tentativas anteriores;
- causa confirmada ou hipótese;
- solução aplicada, se houver;
- teste realizado;
- estado de validação;
- relação com o módulo e procedimento.

Erros históricos do Super Novos, por exemplo, incluem `FileNotFoundError`, arquivo incompleto terminando em `documento_firestore(...)` e delimitador `'''` residual. O histórico integral deve ser consultado antes de afirmar que essas ocorrências representam a versão atual.

## 7.3 Padrão de decisão técnica

Registrar o que foi decidido, por que, alternativas, evidências, data, estado e códigos relacionados. Se uma decisão for substituída, manter o registro anterior marcado como substituído, sem apagar a história.

## 7.4 Padrão de linha do tempo

A linha do tempo deve preservar cronologia, enquanto o manual principal agrupa as informações por contexto. Cada evento importante deve conter, quando disponível:

- data/hora;
- objetivo;
- arquivo/componente;
- ação ou comando;
- resultado observado;
- erro;
- diagnóstico;
- correção;
- decisão;
- próximo passo;
- referência à fonte.

# 8. Itens Não Classificados

## 8.1 Rede de vendedores

A rede de vendedores aparece como uma fase futura na arquitetura inicial. Não há evidência suficiente nesta consolidação para afirmar que faça parte do escopo ativo ou esteja implementada. Manter como proposta histórica até decisão explícita.

## 8.2 Arquivos de investigação individuais

A transcrição cita arquivos como `supernovos.html`, `supernovos_main.js`, `investigacao_api.txt`, `investigacao_firebase.txt`, `supernovos_firestore_teste.json`, `supernovos_campos.txt`, `supernovos_amostra_campos.txt`, `investigacao_url.txt` e `investigacao_url2.txt`. Nem todos estão disponíveis individualmente nas fontes desta consolidação. Não inventar o conteúdo deles.

## 8.3 Arquivos de feed e relatórios Meta

O histórico cita `catalog_vehicles.csv`, um CSV de feed com 45 veículos e `full_errors_for_feed_upload-2026-09-21-072246.xlsx`. Esses arquivos não estão disponíveis individualmente entre as fontes desta consolidação. As informações sobre eles são registros da conversa e precisam de revalidação se forem usadas para gerar o feed atual.

## 8.4 Código integral atual do Super Novos

O histórico registra a execução do gerador, mas o código executável atual completo não foi confirmado nas fontes disponíveis. Anexar ou localizar o arquivo vigente antes de documentar seu conteúdo linha a linha.

# 9. Lacunas e Conflitos

| Código | Item | Impacto | Como resolver | Estado |
|---|---|---|---|---|
| `CON-HSP-VI-001-001` | Supabase versus Neon/PostgreSQL | Pode levar a instruções de banco incorretas | Conferir repositório, variáveis de configuração e conexão atual | Aberto |
| `CON-HSP-VI-001-002` | Modelo inicial versus posterior | Entidades e relações podem ser confundidas | Comparar com schema real e registrar migração/decisão | Aberto |
| `CON-HSP-VI-001-003` | `modeloDescricao` versus `modeloFamiliaDescricao` na Localiza | Afeta normalização do campo `modelo` | Inspecionar coletor vigente e resposta atual | Aberto |
| `CON-HSP-VI-001-004` | Completude do Super Novos | 16 ativos podem não representar o site inteiro | Investigar revendas, filtros, paginação e agregação | Aberto |
| `LAC-HSP-VI-001-001` | Repositório/branch atual | Caminhos e versões podem estar desatualizados | Conferir Git e arquivos atuais | Aberta |
| `LAC-HSP-VI-001-002` | Código atual do feed Meta | Não é possível apontar versão definitiva | Localizar arquivo atual e comparar com histórico | Aberta |
| `LAC-HSP-VI-001-003` | Modelo CSV Meta e relatório de erros | Requisitos e falhas não podem ser revalidados independentemente | Localizar os arquivos originais citados | Aberta |
| `LAC-HSP-VI-001-004` | Estado de FastAPI, Flet e Render | Arquitetura mencionada pode não estar implantada | Conferir código, serviços e logs atuais | Aberta |
| `LAC-HSP-VI-001-005` | Retenção de JSON e snapshots | Afeta custo, reprocessamento e volume | Definir política de retenção baseada no uso real | Aberta |
| `LAC-HSP-VI-001-006` | Contagens históricas | Estoques mudam ao longo do tempo | Fazer nova coleta e registrar data/escopo | Aberta |
| `LAC-HSP-VI-001-007` | Política de deduplicação | Pode fundir veículos diferentes ou duplicar anúncios | Definir chave e critérios com evidências | Aberta |

## 9.1 Perguntas prioritárias para fechar o estado atual

1. Qual repositório e branch são a fonte oficial atual do HSP Vehicle Intelligence?
2. O banco em uso hoje é Supabase, Neon/PostgreSQL ou outro?
3. O arquivo-modelo Meta e o relatório de erros ainda estão disponíveis?
4. Quais são os arquivos atuais dos coletores Python e do gerador do feed?
5. A rede de vendedores continua dentro do escopo ativo ou permanece como ideia futura?

# 10. Tabela de Rastreabilidade

**Granularidade desta versão:** rastreabilidade por arquivo, assunto e seção. Não é uma auditoria linha a linha de todo o histórico.

| Código da fonte | Fonte | Informação/escopo | Destino nesta versão | Estado |
|---|---|---|---|---|
| `SRC-HSP-VI-001-001` | `estrutura-do-manual.md` | Estrutura obrigatória, modos e checagem | Seções 1–11 | Consultada |
| `SRC-HSP-VI-001-002` | `Manual-desenvolvimento.md` | Node.js, Clasp, comandos e `.claspignore` | 4.9, 5.6, 7.2 | Consultada; formatação da fonte original ainda precisa ser corrigida em versão própria |
| `SRC-HSP-VI-001-003` | `Manual-HSP-Vehicle-Intelligence-v3.0-integral.md` | Coletores, arquitetura, dados, escala e Super Novos | Seções 1–9 | Consultada por tema/seção |
| `SRC-HSP-VI-001-004` | `ChatGPT-Criar catálogo de veículos-20260927-0943(1).md` | Feed Meta, modelo inicial, coletores, erros, tentativas e linha do tempo | Seções 1–9; fonte histórica preservada separadamente | Comparada por tema; não linha a linha |
| `SRC-HSP-VI-001-005` | `MAN-HSP-VI-001_v1.0.md` | Consolidação anterior e códigos já existentes | Seções 1–11; histórico de versão | Usada como base de reorganização |
| `SRC-HSP-VI-001-006` | `AUD-HSP-VI-001_v1.0.md` | Diagnóstico estrutural e lacunas | Seções 8–10 e revisão de formato | Incorporada |
| `SRC-HSP-VI-001-007` | `AUD-HSP-VI-002_v1.0.md` | Comparação semântica temática | Seções 2, 4, 8, 9 e 10 | Incorporada |

## 10.1 Relações de registros

| Registro | Relação |
|---|---|
| `COD-HSP-VI-001-001` | Contrato CSV de 11 campos; relacionado a todos os coletores |
| `INF-HSP-VI-001-001` a `INF-HSP-VI-001-005` | Investigações D Motors, Quitcar, Milani, Localiza e Super Novos |
| `INF-HSP-VI-001-006` | Histórico Node.js/Apps Script/Clasp |
| `DEC-HSP-VI-001-001` | Snapshots e histórico; schema atual a confirmar |
| `DEC-HSP-VI-001-002` | Separação do schema externo Meta |
| `DEC-HSP-VI-001-003` | CSV HSP comum de 11 campos |
| `CON-HSP-VI-001-001` a `CON-HSP-VI-001-004` | Conflitos de banco, modelo de dados, campo Localiza e completude Super Novos |
| `LAC-HSP-VI-001-001` a `LAC-HSP-VI-001-007` | Lacunas de repositório, feed, arquivos, implantação, retenção, contagens e deduplicação |

# 11. Histórico de Atualizações

| Data | Versão | Alteração |
|---|---|---|
| 12/10/2026 | 1.0 | Primeira consolidação estruturada; fontes históricas anexadas ao mesmo arquivo. |
| 12/10/2026 | 2.0 | Reestruturação documental importante da arquitetura e evolução do modelo de dados; criação de módulo próprio para Meta Feed; distinção entre histórico, proposta e estado atual; revisão de tabelas, código e procedimentos; fontes históricas referenciadas separadamente. |

## Apêndice A — Fontes e arquivos históricos

Os seguintes arquivos devem permanecer preservados como fontes independentes:

- `estrutura-do-manual.md`
- `Manual-desenvolvimento.md`
- `Manual-HSP-Vehicle-Intelligence-v3.0-integral.md`
- `ChatGPT-Criar catálogo de veículos-20260927-0943(1).md`
- `MAN-HSP-VI-001_v1.0.md`
- `AUD-HSP-VI-001_v1.0.md`
- `AUD-HSP-VI-002_v1.0.md`

A fonte histórica da conversa deve ser consultada para recuperar versões de código, mensagens exatas, tentativas e decisões cronológicas. Não se deve substituir a fonte original pela síntese deste manual.

## Apêndice B — Estado da auditoria

- [x] Estrutura obrigatória de 11 seções aplicada.
- [x] Arquitetura inicial e posterior separadas.
- [x] Modelo inicial e modelo posterior documentados sem fusão por suposição.
- [x] Coletores organizados em módulos próprios.
- [x] Feed Meta integrado como contexto próprio.
- [x] Código e comandos presentes delimitados em blocos com linguagem quando identificável.
- [x] Tabelas apresentadas em Markdown com cabeçalhos.
- [x] Conflitos e lacunas identificados.
- [x] Rastreabilidade declarada por arquivo/assunto/seção.
- [ ] Repositório, banco, coletores, API, interface e feed atuais verificados.
- [ ] Código atual do Super Novos anexado e conferido.
- [ ] Arquivo-modelo Meta e relatório de erros conferidos diretamente.
- [ ] Auditoria linha a linha da transcrição histórica.
- [ ] Execução e validação dos códigos atuais.

**Estado final:** versão 1.1 reorganizada e pronta para revisão técnica; não declarada como validada em execução.
