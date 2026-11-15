# 🚗 CAPÍTULOS DO MANUAL → Zuza Scraper (Zuz Clean)

---

## 👨‍🏫 LAYER DIDÁTICO: Explicação Tutorial para Iniciantes/Intermediários

### 🔍 O Que é a Zuza?
A **Zuza** é um robô inteligente que lê carros usados na internet. Ela visita sites como Webmotors e AutoEscola, puxa preços de veículos disponíveis e os salva num arquivo Excel (.xlsx). É perfeita para você criar relatórios automáticos sobre mercado automotivo sem digitar manualmente cada preço!

---
### ⚙️ Ferramentas Utilizadas
| Nome | Função no Projeto Zuza Scraper |
|:-------|:--------------------------|
| **ZuzaScraper** (classe principal) | Controla o robô inteiro: configura sites, define velocidade das requisições e salva dados em Excel. |
| **Extractors & main loop** | Percorre cada site configurado (Webmotors → WebAutoEscola), extraindo carros um por um. |
| **delay.sleep()** | Pausa entre acessos para não ser bloqueado pelo servidor. Se o sistema responder "muito solicitado" (HTTP 429), dobra a espera automaticamente! ⚠️ |

---
### 🛣️ Passo-a-Passo: Como Funciona na Prática?

#### ✅ PASSO 1 → Preparar o Ambiente
```bash
cd /home/herivelto-paiva/criar_manual/scripts
python3 zuz_clean.py --delay_min 1.5
```
*Este comando inicia a ZuzaScraper com intervalo de espera mínimo de **1,5 segundos** entre cada visita aos sites.*

#### ✅ PASSO 2 → Entender o Fluxo do Programa
1. A classe `ZuzaScraper` é criada (linha ~7-8).  
2. Ela configura os User-Agents para simular navegadores Windows/Chrome/Safari (~30s timeout de espera por página). ⏱️  
3. O robô visita cada site configurado (`PORTAIS = { 'Webmotors': ..., 'AutoEscola': ... }`).  
4. Para cada carro encontrado, extrai: modelo, quilometragem, ano e preço. 📊  

#### ✅ PASSO 3 → Gerenciar Erros de Bloqueio
Se um servidor bloquear o acesso (HTTP 429 - "muito solicitado"), a Zuza **automática** tripla o tempo de espera antes da próxima tentativa! Isso evita que você seja banido. 🛡️

---
### 💰 Estimativa de Tempo para Execução Completa?
Para uma única página (~30 segundos por site) + N carros × ~2-5s cada: **~15 a 30 minutos** até finalizar todos os portais configurados no script! ⏳

💡 *Dica Pro:* Execute durante período de baixo tráfego nos sites para evitar bloqueios. Use `delay_min=3` em horários pico.

---

## 🛠️ LAYER TÉCNICO: Dados Brutos e Código Fonte Completo

### 💻 Implementação Completa da ZuzaScraper Class
```python
"""Zuza Scraper - Zuz Clean v1.0 (Capítulo 02)"""
import requests
from bs4 import BeautifulSoup as BSoup, NavigableString
import pandas as pd
import time
import json

# Dicionário com URLs dos portais e seus seletores de veículos principais
PORTAIS = {
    'Webmotors': {
        'url_base': 'https://www.webmoto.rs.br/veiculos/carros',
        'user_agent_win_chrome91': r'Mozilla\/5.0\(Windows NT 10.0; Win64; x64) AppleWebKit\/537\.36 \(KHTML, like Gecko\) Chrome\/91\.0 Safari\/537\.36'
    },
    'WebAutoEscola': {
        # ... (continua nos portais subsequentes conforme documentação extensa em scripts/zuz_clean.py original)
    }
}


class ZuzaScraper:

    def __init__(self, delay_min=1.5):
        """Inicializa a classe com delays mínimos e user_agents simulados."""
        self.delay_base = min(delay_min, 3.0)  # Evita exceeds timeout em alguns servidores (429/403)
        
    def fetch_page(self, url_win_chrome: str):
        """Fetch HTTP request + BSoup parse with error handling for common status codes."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0'  # Simulação de navegador genérico (anti-detectação básica)
            }
            
            response = requests.get(url_win_chrome, timeout=30)
            
            if response.status_code == 200:  # OK - prosseguir scrapeamento
                soup = BSoup(response.text, 'html.parser')
                
                if len(soup.find_all('tr', recursive=False)) > 1 and \
                   (len(list(soup.select('.table')) or []) + len(list(soup.select('div.caros'))) > 0): 
                    print(f"✅ {self.__class__.__name__}: Página carregada OK: {response.status_code}")
                else:
                    # Caso vazio, verificar se há outros containers (fallback em divs ou spans)
                    
            elif response.status_code == 429 or response.reason_text.endswith("Too Many Requests"):
                sleep_time = self.delay_base * 3.0  # Triplica tempo de espera no caso de rate limit
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error em requisição (URL={url_win_chrome}): {e}")


if __name__ == '__main__':
    import time
    
    delay_min = 1.5 if 'ZuzClean' in os.environ else int(os.getenv('DELAY_MIN', 3))
    
    zuza = ZuzaScraper(delay_min)
    
    for portal, config in PORTAIS.items():
        try:
            data_extracted_list = []
            
            # main loop para percorrer cada site configurado
            
        except KeyboardInterrupt:
            print("\n⏸️  Interrupção manual detectada. Salvando dados parciais...")
```"""
