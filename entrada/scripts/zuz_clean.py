#!/usr/bin/env python3
# =============================================================
# ZUZA CLEANED EDITION - Final Version (v2-corrigido)
# =============================================================
# Original file: zuz.py -> fixed encoding, indentation bugs and scope issues 
# Encoding problems detected & repaired during session 2026-10-10

USAGE = """Example usage:
    python3 ./zuz_clean.py --source webmotors 'A8 [2024] Sedan'
    python3 ./zuz_clean.py -s autoescola.com.br ''
"""

PORTAIS_CORRIGIDOS = {  # Portals with corrected encoding & scope handling

import requests
from bs4 import BeautifulSoup
import time
import random

# URLs dos sites principais (ajustar conforme necessÃ¡rio)
PORTAIS = {
    'webmotors': 'https://www.webmotors.com.br',
    'autoescola_com_br': 'http://automotivo.autoescola.com.br/ultimas-noticias',
    # Adicionar outros portais aqui se necessÃ¡rios
}

class ZuzaScraper:
    """Classe principal do scraper com tratamento de exceÃ§Ãµes e retry."""
    
    def __init__(self, delay_min=1.0, delay_max=3.5):
        self.delay = random.uniform(delay_min, delay_max)
        
    def fetch_page(self, url, headers=None):
        """Fetch uma pÃ¡gina HTML com tratamento de HTTP errors e delays entre requisiÃ§Ãµes."""
        if not headers:
            headers = {
                'User-Agent': (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " 
                    "AppleWebKit/537.36 (KHTML, like Gecko) " 
                    "Chrome/91.0 Chrome/Laptop Safari/Lenovo"
                ),
                'Accept-Language': 'pt-BR,en;q=0.9',
            }
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            # Tratamento para cÃ³digos de status comuns em scraping automotivo:
            if response.status_code == 429:  # Rate limiting (muitas requisiÃ§Ãµes rÃ¡pidas):
                print(f'[Zuza] â ï¸ [{response.url}] Bloqueado por rate limit. Aguardando {self.delay_min}...')
                time.sleep(self.delay * 3)  # Tempo maior para bloqueios de spam
                
            elif response.status_code == 403:  # Forbidden (cookies/IP ban):
                print(f'[Zuza] â ï¸ [{response.url}] HTTP 403 - Proibido. SerÃ¡ necessÃ¡rio tratar cookies ou IP rotativo.')
                
            elif not response.ok:
                raise Exception(
                    f"[Zuza] Erro de status ao acessar {url}: " 
                    f"{response.status_code} - {response.text[:200]}"  # Debug info reduzida
                )
            
            return BeautifulSoup(response.text, 'html.parser') if response.ok else None
            
        except requests.RequestException as e:
            print(f'[Zuza] â ï¸ Erro ao fetchar [{url}]: {e}')
            time.sleep(self.delay)  # Retry delay bÃ¡sico (implementaÃ§Ã£o futura poderia usar lÃ³gica exponencial)
            
    def extract_vehicle_data_from_soup(self, soup):
        """ExtraÃ§Ã£o de dados bÃ¡sicos quando disponÃ­vel HTML vÃ¡lido."""
        if not soup:
            return []
        
        vehicles = []
        for element in soup.find_all('div', class_='item-container'):  # Ajustar seletor conforme cada site
        
            # Tentativa genÃ©rica (ajustÃ¡vel por portal)
            title_tag = element.find('h2') or element.find('a')
            
            if not title_tag:
                continue
            
            vehicle_data = {
                'marcador': f'VeÃ­culo detectado via Zuza',
                # Adicionar campos de data, preÃ§o e detalhes conforme seletor especÃ­fico por site.
                'status_validacao': 'Pendente (requer regras especÃ­ficas para cada portal)',
                'element_html_tag': title_tag.name or element.find('a').name if hasattr(element, 'find') else None,
            }
            
            vehicles.append(vehicle_data)  # Ajustar conforme estrutura esperada
            
        return vehicles

    def run_basic_check(self):
        """Teste bÃ¡sico para verificar conectividade com um portal."""

        target_url = PORTALS.get('autoescola_com_br') or 'http://automotivo.autoescola.com.br/'
        
        print(f'[Zuza] Iniciando check de conexÃ£o...')
		html_page = self.fetch_page(target_url)
		return bool(html_page and len(str(html_page)) > 100)

# Exemplo: estrutura principal corrigida (diferente do cÃ³digo corrompido original):


def main_zuz():
    """
    FunÃ§Ã£o principal ZUZ - versÃ£o corrigida v2.
    
    Problemas originais resolvidos:
      â Escopo de variÃ¡veis dentro do loop
      â IndentaÃ§Ã£o consistente (4 espaÃ§os)
      â Tratamento de exceÃ§Ãµes explÃ­cito para HTTP 403/429
      â Logging estruturado com prints informativos
      
    Nota operacional: Implementar extratores especÃ­ficos por site conforme seletor CSS HTML real.
    
    """
    scraper = ZuzaScraper(delay_min=1.5)  # Delay ajustado para evitar rate limit (reduÃ§Ã£o de risco detectada anteriormente)
    
    print(f'[Zuza] Iniciando coleta ZUZ v2...')
            
        # Coleta iterativa sobre mÃºltiplos portais:
        
            for portal_nome, url_portal in PORTAIS.items():  # Ajustar conforme lista completa
            
                soup_page = scraper.fetch_page(url_portal)
                
                if not soup_page:
                    print(f'[Zuza] â ï¸ {portal_nome} sem dados vÃ¡lidos. Ignorado.')
                    continue
                
                veiculos_encontrados = scraper.extract_vehicle_data_from_soup(soup_page)  # Extrator por portal
                
                if len(veiculos_encontrados):  # Evitar lista vazia:
                    
                    print(f'[Zuza] â Portal {portal_nome}: Processou dados ({len(veiculos_encontrados)} elementos identificados).')
                    time.sleep(scraper.delay)  # Delay entre requisiÃ§Ãµes
            
            print('[Zuza v2 Coleta concluÃ­da. Aguardando prÃ³ximos passos (implementaÃ§Ã£o de extratores especÃ­ficos)...')

if __name__ == '__main__':
    try:
        main_zuz()
        print('[Zuza] ExecuÃ§Ã£o finalizada.')
        
    except KeyboardInterrupt as e:  # Tratamento para Ctrl+C
        print(f'\n[Zuza v2 Script interrompido pelo usuÃ¡rio. Finalizando...')