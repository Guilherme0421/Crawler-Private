import re
import copy
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

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


def encontrar_telefones(soup):
    telefones_unicos = set()

    texto_pagina = extrair_texto(soup)
    
    regex_padrao = r"\b(?:\(?([1-9][0-9])\)?\s?)?(?:((?:9\d|[2-5])\d{3})[-\s]?(\d{4}))\b"
    matches = re.finditer(regex_padrao, texto_pagina)

    for match in matches:
        numero_completo = match.group(0)
        
        apenas_digitos = re.sub(r'\D', '', numero_completo)
        
        if len(apenas_digitos) in [8, 9, 10, 11]:
            numero_formatado = formatar_numero_telefone(apenas_digitos)
            
            telefones_unicos.add(numero_formatado)

    return list(telefones_unicos) if telefones_unicos else None


def formatar_numero_telefone(numero):
    tamanho = len(numero)
    
    if tamanho == 11:
        return f"({numero[:2]}) {numero[2:7]}-{numero[7:]}"
    elif tamanho == 10:
        return f"({numero[:2]}) {numero[2:6]}-{numero[6:]}"
    elif tamanho == 9:
        return f"{numero[:5]}-{numero[5:]}"
    elif tamanho == 8:
        return f"{numero[:4]}-{numero[4:]}"
    else:
        logger.error("Número inválido")
        
    return numero