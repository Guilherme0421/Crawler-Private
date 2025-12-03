import threading
import re
import requests
from bs4 import BeautifulSoup

dominio = "https://django-anuncios.solyd.com.br"
urlAutomoveis = "https://django-anuncios.solyd.com.br/automoveis/"

LINKS = []
TELEFONES = []

def requisicao(url):
    try:
        response = requests.get(url)
        if(response.status_code == 200):
            return response.text    
        else:
            print("Erro ao fazer requisição")
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

def acessar_anuncio(link):
    try:
        response = requests.get(dominio + link)
        if(response.status_code == 200):
            return response.text    
        else:
            print("Erro ao fazer requisição de busca de telefones")
    except Exception as e:
        print(f"Erro ao fazer a requisição de busca de telefones: {e}")
        
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


def descobrir_telefones():
    while True:
        try:
            link_anuncio = LINKS.pop(0)
        except:
            break
        
        resposta_anuncio = requisicao(dominio + link_anuncio)
        
        if resposta_anuncio:
            soup_anuncio = parsing(resposta_anuncio)
        
            if soup_anuncio:
                telefones = encontrar_telefones(soup_anuncio)
                if telefones:
                    for telefone in telefones:
                        print("Total de telefones encontrados:", len(TELEFONES) + 1)
                        TELEFONES.append(telefone)
                    
   
def salvar_telefones():
    try:
        with open("telefones.csv","a") as arquivo:
            for telefone in TELEFONES:
                arquivo.write(f"{telefone}\n")
            print("Telefones salvos com sucesso em telefones.csv")
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")
   
   
                    
if __name__ == "__main__":
    response = requisicao(urlAutomoveis)
    if response:
        soup_busca = parsing(response)
        if soup_busca:
            LINKS = encontrar_links(soup_busca)
            
            THREADS = []
            for i in range(5):
                t = threading.Thread(target=descobrir_telefones)
                THREADS.append(t)
                
            for t in THREADS:
                t.start()
            
            for t in THREADS:
                t.join()
            
            print(TELEFONES)
            
            salvar_telefones()
    