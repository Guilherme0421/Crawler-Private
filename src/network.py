import requests
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from fake_useragent import UserAgent
from src.config import logger

def requisicao(url, headers):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if(response.status_code == 200):
            return response.text    
        else:
            logger.warning(f"Status Code {response.status_code} ao acessar: {url}")
    except Exception as e:
        logger.error(f"Falha de conexão em: {url}: {e}")
        
def get_random_user_agent():
    ua = UserAgent(platforms=["desktop"], browsers=["Chrome"])
    agent = ua.random
    return agent
  
def filtrar_url(url):
    url_filtered = urlparse(url)
    dominio = f"{url_filtered.scheme}://{url_filtered.netloc}"
    return dominio  
      
def check_robots(url, agent):
    dominio = filtrar_url(url)
    robots_url=f"{dominio}/robots.txt"

    print(f"Verificando regras em: {robots_url}")

    rp = RobotFileParser()
    rp.set_url(robots_url)

    try:
        rp.read()
    except Exception as e:
        print(f"Erro ao ler o arquivo robots.txt: {e}")
        return False
    
    if(rp.can_fetch(agent, url)):
        return True
    else:
        return False