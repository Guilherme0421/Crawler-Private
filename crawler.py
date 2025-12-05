import threading
import copy
import re
import requests
import time
import random
from urllib.parse import urlparse, urljoin
from urllib.robotparser import RobotFileParser
from users_agent import get_random_user_agent, robots_parser,filtrar_url
from bs4 import BeautifulSoup

# dominio = "https://django-anuncios.solyd.com.br"
# urlAutomoveis = "https://django-anuncios.solyd.com.br/automoveis/"

LINKS = []
TELEFONES = []
LOCK = threading.Lock()

def requisicao(url, headers):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if(response.status_code == 200):
            return response.text    
        else:
            print("Erro ao fazer requisição HTTP", response.status_code)
    except Exception as e:
        print(f"Erro ao fazer a requisição: {e}")
        
def parsing(resposta_html):
    try:
        soup = BeautifulSoup(resposta_html, 'html.parser')
        return soup
    except Exception as e:
        print("Erro ao fazer o parsing HTML", e)
        
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
        print(f"Erro ao processar links: {e}")
        
    return list(links_uteis)

def extrair_texto(soup):
    soup_limpo = copy.copy(soup)

    for script_or_style in soup_limpo(["script","style","header","footer","nav"]):
        script_or_style.decompose()

    texto = soup_limpo.get_text(separator=' ')

    lines = (line.strip() for line in texto.splitlines())
    texto_limpo = ' '.join(chunk for chunk in lines if chunk)

    return texto_limpo
        
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
        print("Número inválido")
        
    return numero
        
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

def descobrir_telefones(headers):
    thread_name = threading.current_thread().name
    print(f"{thread_name} Iniciando Trabalho!")

    while True:
        delay = random.uniform(2.0, 5.0)
        time.sleep(delay)
        
        link_anuncio = None
        
        with LOCK:
            try:
                if len(LINKS) > 0:
                    link_anuncio = LINKS.pop()
                else:
                    print(f"[{thread_name}] Lista vazia. Encerrando.")
                    break
            except:
                break
        if link_anuncio is None:
            break
        
        print(f"[{thread_name}] Acessando: {link_anuncio}")

        resposta_anuncio = requisicao(link_anuncio, headers)
        
        if resposta_anuncio:
            soup_anuncio = parsing(resposta_anuncio)
            if soup_anuncio:
                telefones = encontrar_telefones(soup_anuncio)
                if telefones:
                    for telefone in telefones:
                        with LOCK:
                            print(f"{thread_name} 📞 Encontrado: {telefone}")
                            TELEFONES.append(f"{telefone}; {link_anuncio}")
                else:
                    print(f"[{thread_name}] ⚠️ Nenhum padrão de telefone encontrado: {link_anuncio}")
                    pass
                    
   
def salvar_telefones():
    try:
        with open("telefones.csv","a") as arquivo:
            for telefone in TELEFONES:
                arquivo.write(f"{telefone}\n")
            print("Telefones salvos com sucesso em telefones.csv")
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")
   
   
                    
if __name__ == "__main__":
    agent = get_random_user_agent()
    headers = {
        'User-Agent': agent
    }

    url_alvo = input("Digite a url do site alvo: ")

    # Debugging
    print(f"Alvo: {url_alvo}")
    print(f"Agente: {agent[:30]}")

    if robots_parser(url_alvo, agent):
        print("✅ Permissão concedida!")
        response = requisicao(url_alvo, headers)

        if response:
            soup_busca = parsing(response)
            if soup_busca:
                LINKS = encontrar_links(soup_busca, url_alvo)
                print(f"Links internos encontrados para varredura: {len(LINKS)}")
                
                if len(LINKS) > 0:
                    THREADS = []
                    for i in range(3):
                        t = threading.Thread(target=descobrir_telefones, args=(headers,))
                        THREADS.append(t)
                        
                    for t in THREADS:
                        t.start()
                    
                    for t in THREADS:
                        t.join()
                
                    print(f"\nFim de execução. {len(TELEFONES)} coletados.")
                    #salvar_telefones()
                else:
                    print("Nenhum link interno encontrado na página inicial.")
    else:
        print("❌ Acesso negado pelo Robots.txt")
    