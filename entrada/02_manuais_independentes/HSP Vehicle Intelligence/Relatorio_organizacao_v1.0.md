# RELATÓRIO DE REORGANIZAÇÃO — HSP VEHICLE INTELLIGENCE

**Código:** `AUD-HSP-VI-003`  
**Versão:** 1.0  
**Data:** 12/10/2026  
**Projeto:** HSP Vehicle Intelligence  
**Documento de destino:** `MAN-HSP-VI-001_v2.0.md`  
**Estado:** Reorganização documental produzida; validação de implementação e auditoria linha a linha pendentes.

## 1. Objetivo

Aplicar o mapa de comparação `AUD-HSP-VI-002_v1.0.md` ao manual principal, reorganizando os conteúdos por contexto e preservando as fontes históricas separadas. A reestruturação mantém o código permanente `MAN-HSP-VI-001` e adota a versão `2.0` porque houve mudança importante na organização do documento.

## 2. Fontes consideradas

| Fonte | Uso nesta reorganização | Limite |
|---|---|---|
| `estrutura-do-manual.md` | Estrutura obrigatória de 11 seções | Consultada; mantida como referência de estrutura |
| `Manual-desenvolvimento.md` | Histórico Node.js, Apps Script, Clasp e `.claspignore` | Conteúdo relacionado resumido no módulo histórico; arquivo-fonte preservado |
| `Manual-HSP-Vehicle-Intelligence-v3.0-integral.md` | Arquitetura posterior, coletores, CSV, Super Novos e escala | Comparação por seção/tema, não linha a linha |
| `ChatGPT-Criar catálogo de veículos-20260927-0943(1).md` | Modelo inicial, Meta Feed, tentativas, erros, decisões e contexto cronológico | Comparação temática; não revisão humana de todas as linhas |
| `MAN-HSP-VI-001_v1.0.md` | Base do manual anterior e rastreabilidade já existente | Mantido intacto |
| `AUD-HSP-VI-001_v1.0.md` e `AUD-HSP-VI-002_v1.0.md` | Diagnóstico estrutural e comparação semântica | Usados como mapa de trabalho |

## 3. Mudanças: antes → depois

| Antes — v1.0 | Depois — v2.0 | Motivo |
|---|---|---|
| O modelo de dados posterior aparecia depois dos coletores. | A evolução do modelo de dados foi movida para o início dos módulos, antes do contrato CSV e dos coletores. | Conceitos e dependências vêm antes da implementação específica. |
| O modelo inicial `sources`, `sellers`, `vehicles`, `listings`, `vehicle_images` estava principalmente na transcrição histórica. | O modelo inicial foi incorporado como modelo histórico e comparado com `fontes`, `veiculos`, `anuncios`, `snapshots`. | Tornar visível a evolução sem fundir schemas por suposição. |
| O feed Meta aparecia de forma resumida, com detalhes relevantes no apêndice histórico. | Foi criado o módulo 4.8 para registrar objetivo, campos relatados, problemas históricos, plano de teste e estado não validado. | Colocar o contexto Meta junto das decisões e falhas que pertencem a ele. |
| O problema de `vehicle_id` usado como VIN e os erros genéricos de importação estavam na cronologia. | Foram integrados ao módulo Meta e às decisões técnicas. | Permitir consulta direta sem percorrer a transcrição inteira. |
| A arquitetura inicial e a posterior eram resumidas sem um mapa comparativo próprio. | Foram separadas em subseções e marcadas como versões documentais distintas. | Evitar afirmar que Supabase e Neon/PostgreSQL são simultaneamente o banco ativo. |
| A transcrição completa estava anexada ao final do mesmo arquivo de manual. | O manual v2.0 referencia as fontes históricas separadamente; o arquivo histórico original deve continuar preservado. | Reduzir o peso de consulta do manual operacional sem apagar a fonte. |
| Algumas tabelas estavam em formato de grade e alguns procedimentos em texto corrido. | As tabelas do v2.0 usam sintaxe Markdown com barras verticais; procedimentos foram estruturados em passos numerados. | Melhorar compatibilidade, leitura e repetibilidade. |
| Estados históricos podiam ser interpretados como estado atual. | Estados, propostas, hipóteses, testes e lacunas são diferenciados explicitamente. | Evitar declarações de implementação ou validação sem evidência. |

## 4. Mapa dos contextos na versão 2.0

- **Arquitetura:** seção 2.
- **Glossário:** seção 3.
- **Evolução do modelo de dados:** seção 4.1.
- **Contrato de dados HSP/CSV:** seção 4.2.
- **Coletores:** seções 4.3 a 4.7.
- **Feed Meta:** seção 4.8.
- **Node.js/Apps Script/Clasp:** seção 4.9.
- **Histórico e inteligência:** seção 4.10.
- **Escala e armazenamento:** seção 4.11.
- **Rede de vendedores:** seção 4.12.
- **Procedimentos:** seção 5.
- **Decisões e aprendizados:** seção 6.
- **Padrões reutilizáveis:** seção 7.
- **Itens sem destino confirmado:** seção 8.
- **Lacunas e conflitos:** seção 9.
- **Rastreabilidade:** seção 10.
- **Histórico de atualizações:** seção 11.

## 5. Auditoria de formatação realizada

Verificações automatizadas no arquivo `MAN-HSP-VI-001_v2.0.md`:

| Verificação | Resultado |
|---|---|
| Arquivo existe após gravação | Confirmado |
| Tamanho | 52.918 bytes |
| Linhas | 1.262 |
| Seções obrigatórias principais | 11 de 11 |
| Blocos cercados por crases | 38 pares |
| Tabelas Markdown identificadas | 24 |
| Inconsistências de quantidade de colunas nas tabelas verificadas | 0 |
| Conversão para tabelas de grade Pandoc | Não identificada |
| Código atual executado como parte desta reorganização | Não |
| Auditoria humana linha a linha da transcrição | Não realizada |

A validação automatizada verifica a estrutura básica do Markdown. Ela não substitui a renderização em todos os visualizadores nem a validação de cada comando/código.

## 6. Conteúdo preservado fora do manual principal

A fonte cronológica e os documentos anteriores não devem ser excluídos. Eles permanecem necessários para recuperar mensagens exatas, variantes de código, tentativas fracassadas e contexto histórico. O manual v2.0 é a camada organizada para consulta; as fontes são a camada de evidência.

Arquivos de referência:
- `ChatGPT-Criar catálogo de veículos-20260927-0943(1).md`
- `Manual-HSP-Vehicle-Intelligence-v3.0-integral.md`
- `Manual-desenvolvimento.md`
- `MAN-HSP-VI-001_v1.0.md`
- `AUD-HSP-VI-001_v1.0.md`
- `AUD-HSP-VI-002_v1.0.md`

## 7. Pendências antes de declarar o manual validado

1. Confirmar o repositório e a branch atuais.
2. Confirmar o banco ativo e o schema real.
3. Localizar os arquivos atuais dos coletores e do gerador de feed.
4. Recuperar o arquivo-modelo Meta e o relatório de erros citados.
5. Resolver o campo `modelo` da Localiza com base no coletor atual.
6. Investigar a completude do Super Novos.
7. Verificar o estado atual de FastAPI, Flet, Render e do feed.
8. Fazer auditoria semântica linha a linha se o objetivo for rastreabilidade completa do histórico.
9. Conferir a renderização final do Markdown em um visualizador de destino.

## 8. Checagem final

- [x] Comparação temática anterior utilizada como mapa.
- [x] Conteúdo reorganizado por contexto, não pela ordem cronológica de chegada.
- [x] Fontes históricas preservadas como arquivos independentes.
- [x] Conflitos e lacunas mantidos abertos sem solução por suposição.
- [x] Código e comandos delimitados em blocos identificados quando possível.
- [x] Tabelas convertidas para Markdown com cabeçalhos.
- [x] Código permanente preservado.
- [x] Mudança estrutural registrada como versão 2.0.
- [ ] Execução de códigos atuais.
- [ ] Confirmação de arquitetura implantada.
- [ ] Auditoria integral linha a linha do histórico.

**Conclusão:** o manual v2.0 está reorganizado para revisão técnica. A formatação estrutural foi verificada automaticamente, mas a validação da implementação e a auditoria integral do histórico continuam pendentes.
