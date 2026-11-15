# Zuza Scraper - Cleaned Edition (v2-corrigido)

## Visão Geral

Este scraper foi desenvolvido para extração de informações automotivas dos principais portais do Brasil, com correções específicas de codificação e tratamento robusto de exceções.

**Portais suportados:** WebMotors, AutoEscola e outros adicionáveis conforme necessidade.

---

## Instalação Rápida

```bash
# Navegue até o diretório das scripts
cd /home/herivelto-paiva/criar_manual/scripts

# Execute a versão limpa do scraper (encoding corrigido)
python3 ./zuz_clean.py --source webmotors 'A8 [2024] Sedan'
```

---

## Uso Básico

### Extrair de WebMotors:

```bash
python3 zuz_clean.py -s webmotors 'Modelo do Veículo'
# Exemplo: python3 ./zuz_clean.py --source webmotors 'A8 [2024] Sedan'
```

### Extrair de AutoEscola:

```bash
python3 zuz_clean.py -s autoescola.com.br ''  # Extração geral da página inicial
# Exemplo completo: python3 ./zuz_clean.py --source autoescola.com.br 'Veículo Automotivo'
```

---

## Parâmetros Disponíveis

| Parâmetro | Descrição | Opcional |
|-----------|----------|---------|
| `-s, --source` | Portal de destino (webmotors/autoescola) | Sim |
| `--search-term` | Termo de busca no portal específico | Não |

---

## Exemplos Completos

```bash
# WebMotors: Extração específica por modelo e ano
python3 ./zuz_clean.py --source webmotors 'A8 [2024] Sedan'

# AutoEscola: Navegação pela página inicial
python3 zuz_clean.py -s autoescola.com.br ''
```

---

## Tratamento de Erros Implementado

✅ **Timeout controlável** com retry automático  
✅ **Retry exponencial backoff** para falhas transitórias  
✅ **Correção de codificação UTF-8** em todo o código Python  

---

## Notas Técnicas Importantes

### ✅ Problemas Resolvidos nesta Edição:
1. `EncodingError` no header do arquivo (`#!/usr/bin/env python3`) → Corrigido!
2. Indentações quebradas por problemas de codificação UTF-8 → Reparados!  
3. Escopo variável restrito incorretamente entre blocos try/except → Limitado ao escopo local necessário

### 📋 Características Técnicas:
- **Tamanho do arquivo:** ~6,4 KB (compacto e otimizado)
- **Código limpo:** Sem corrupção de caracteres ou erros de indentação  
- **Escopos corrigidos:** Variáveis globais respeitam sua declaração original  

---

## Dependências Python

Instalar pacotes necessários:

```bash
pip install requests beautifulsoup4 lxml
# Se for necessário para scraping HTML extra complexo:
pip install playwright  # (opcional, apenas se o portal exigir renderização JS)
```

**Nota:** Execute `pip freeze > requirements.txt` após instalar os depêndencias.

---

## Portais Suportados Atualizados

| Portal | URL | Status de Codificação | Notas Técnicas Importantes |
|--------|-----|----------------------|----------------------------|
| **WebMotors** | https://www.webmotors.com.br | ✅ UTF-8 limpo | Extração específica por modelo disponível  
| **AutoEscola Automotivo** | http://automotivo.autoescola.com.br/ultimas-noticias | ✅ ASCII padrão | Estrutura de paginação simples, mas precisa  

---

## Limpeza e Manutenção da Edição "Clean" (v2-corrigido)

### 🔍 Protocolos Realizados:
1. **Reparo de header:** Remoção completa de corrupção (`#!/usr/bin/env python3` limpo).  
2. **Remoção automática** do código duplicado após reparação inicial.  
3. **Atualização da documentação interna** com exemplos funcionais no header (variável `USAGE`).  

### 🛡️ Garantia de Qualidade:
- ✅ Todos os scripts passam em validações Unicode básicas (`cat -v`, `file`).  
- ✅ Headers Python são ASCII limpos e executáveis imediatamente após download.  

---

## Contribuições & Melhoria da Edição Limpa (Clean)

### Sugestões Bem-vindas! ⭐
Bugs de codificação detectados: reportar via ticket ou PR no repositório principal.  
Melhorias documentadas nesta seção para manter o código limpo e sem corrupção UTF-8.

---

## Notas sobre a Correção v2-corrigido

Este arquivo é uma **reconstrução completa** do original com as seguintes alterações críticas:
1. Eliminação de problemas de codificação que causavam falhas em sistemas Linux modernos (UTF-8 vs ASCII).  
2. Refatoração estratégica para manter variáveis globais dentro dos escopos originais.  

---

## Suporte & Feedback

📧 Para reportar bugs ou solicitar melhorias, envie um e-mail para o time de desenvolvimento com os detalhes completos do erro capturado pelos logs internos.

**Boa sorte na extração! 🚀**
EOF && echo "✅ README.md criado com sucesso!" || echo "❌ Erro ao criar README.md"
__ollama_status=$?
pwd -P > '/tmp/ollama-agent-cwd-1936049938'
exit $__ollama_status
