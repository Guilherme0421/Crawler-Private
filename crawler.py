import threading
import copy
import re
import requests
from users_agent import get_random_user_agent, robots_parser,filtrar_url
from bs4 import BeautifulSoup

# dominio = "https://django-anuncios.solyd.com.br"
# urlAutomoveis = "https://django-anuncios.solyd.com.br/automoveis/"

LINKS = []
TELEFONES = []

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
        
def encontrar_links(soup):
    try:
        cards_pais = soup.find("div", class_="ui three doubling link cards")
        cards = cards_pais.find_all("a")
    except Exception as e:
        print(f"Erro ao encontrar links: {e}")
      
    links = []
    for card in cards:
        try:
            link = card['href']
            links.append(link)
        except Exception:
            pass
        
    return links

def extrair_texto(soup):
    soup_limpo = copy.copy(soup)

    for script_or_style in soup_limpo(["script","style","header","footer","nav"]):
        script_or_style.decompose()

    texto = soup_limpo.get_text(separator=' ')

    lines = (line.strip() for line in texto.splitlines())
    texto_limpo = ' '.join(chunk for chunk in lines if chunk)

    return texto_limpo

# def acessar_anuncio(link):
#     try:
#         response = requests.get(dominio + link)
#         if(response.status_code == 200):
#             return response.text    
#         else:
#             print("Erro ao fazer requisição de busca de telefones")
#     except Exception as e:
#         print(f"Erro ao fazer a requisição de busca de telefones: {e}")
        
def encontrar_telefones(soup):

    try:
        descricao = soup.find_all("div", class_="sixteen wide column")[2].p.get_text().strip()
    except Exception as e:
        print(f"Erro ao encontrar descrição: {e}")
    
    regex = re.findall(r"((?:\+?\d{2}\s?)?(?:\(?\d{2}\)?\s?)?\d{4,5}[-\s]?\d{4})", descricao)
    if(regex): 
        return regex
    else:
        return None

def descobrir_telefones(dominio, headers):
    thread_name = threading.current_thread().name
    print(f"{thread_name} Iniciando Trabalho!")

    while True:
        try:
            if len(LINKS) > 0:
                link_anuncio = LINKS.pop()
            else:
                print(f"[{thread_name}] Lista vazia. Encerrando.")
                break
        except:
            break
        
        url_completa = dominio + link_anuncio
        print(f"[{thread_name}] Acessando: {link_anuncio}")

        resposta_anuncio = requisicao(url_completa, headers)
        
        if resposta_anuncio:
            soup_anuncio = parsing(resposta_anuncio)
        
            if soup_anuncio:
                telefones = encontrar_telefones(soup_anuncio)
                if telefones:
                    for telefone in telefones:
                        print(f"Encontrado: {telefone}")
                        TELEFONES.append(telefone)
                else:
                    print(f"[{thread_name}] ⚠️ Regex falhou no link: {link_anuncio}")
                    
   
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
    dominio = filtrar_url(url_alvo)

    if robots_parser(url_alvo, agent):
        print("✅ Permissão concedida!")
        response = requisicao(url_alvo, headers)

        if response:
            soup_busca = parsing(response)
            if soup_busca:
                LINKS = encontrar_links(soup_busca)
                print(f"Links encontrados: {len(LINKS)}")
                
                THREADS = []
                for i in range(5):
                    t = threading.Thread(target=descobrir_telefones, args=(dominio, headers))
                    THREADS.append(t)
                    
                for t in THREADS:
                    t.start()
                
                for t in THREADS:
                    t.join()
                
                print(f"Fim de execução. {len(TELEFONES)} coletados.")
                salvar_telefones()
    else:
        print("❌ Acesso negado pelo Robots.txt")
    