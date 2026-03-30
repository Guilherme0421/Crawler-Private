import re
import copy
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import phonenumbers

from src.config import logger

def parsing(resposta_html):
    try:
        soup = BeautifulSoup(resposta_html, 'html.parser')
        return soup
    except Exception as e:
        logger.error(f"Erro ao fazer o parsing HTML: {e}")
        

def encontrar_links(soup, dominio):
    links_uteis = set()
    dominio_base = urlparse(dominio).netloc

    try:
        tags_a = soup.find_all("a",href = True)
        for tag in tags_a:
            href = tag['href'].strip()

            if not href or href.startswith(('#','javascript:','mailto:','tel:')):
                continue

            url_completa = urljoin(dominio, href)
            if (urlparse(url_completa).netloc == dominio_base):
                links_uteis.add(url_completa)
    except Exception as e:
        logger.error(f"Erro ao processar links: {e}")
        
    return list(links_uteis)


def extrair_texto(soup):
    soup_limpo = copy.copy(soup)

    for script_or_style in soup_limpo(["script","style","header","footer","nav"]):
        script_or_style.decompose()

    texto = soup_limpo.get_text(separator=' ')

    lines = (line.strip() for line in texto.splitlines())
    texto_limpo = ' '.join(chunk for chunk in lines if chunk)

    return texto_limpo


def encontrar_telefones(texto):
    """
    Extrai e valida números de telefone do texto fornecido usando a biblioteca phonenumbers.
    
    Args:
        texto (str): O conteúdo HTML ou texto extraído pelo crawler.
    
    Returns:
        list or None: Lista de números de telefone normalizados no formato E.164, ou None se nenhum encontrado.
    """
    telefones_unicos = set()
    
    try:
        # Usar PhoneNumberMatcher para encontrar candidatos a números de telefone no padrão brasileiro
        for match in phonenumbers.PhoneNumberMatcher(texto, "BR"):
            numero = match.number
            
            # Validar o número
            if phonenumbers.is_valid_number(numero):
                # Normalizar para formato E.164
                numero_normalizado = phonenumbers.format_number(numero, phonenumbers.PhoneNumberFormat.E164)
                telefones_unicos.add(numero_normalizado)
        
        return list(telefones_unicos) if telefones_unicos else None
    
    except Exception as e:
        logger.error(f"Erro ao extrair telefones: {e}")
        return None


