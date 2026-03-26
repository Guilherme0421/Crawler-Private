import requests
import sys
import random
import time
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from fake_useragent import UserAgent
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from src.config import logger

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=2, max=8),
    retry=retry_if_exception_type((requests.exceptions.RequestException, requests.exceptions.Timeout)),
    before_sleep=lambda retry_state: logger.warning(f"Tentativa {retry_state.attempt_number} falhou: {retry_state.outcome.exception()}. Tentando novamente em {retry_state.next_action.sleep} segundos.")
)
def requisicao(url, headers, crawl_delay=None):
    # Aplicar delay aleatório se crawl_delay estiver definido
    if crawl_delay:
        delay = random.uniform(crawl_delay, 2 * crawl_delay)
        logger.info(f"Aplicando delay de {delay:.2f} segundos")
        time.sleep(delay)

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
        elif response.status_code == 429:
            logger.warning(f"Erro 429 (Too Many Requests) ao acessar: {url}. Pausando por 60 segundos.")
            time.sleep(60)  # Pausa maior para 429
            raise requests.exceptions.RequestException(f"429 Too Many Requests: {url}")
        else:
            logger.warning(f"Status Code {response.status_code} ao acessar: {url}")
            raise requests.exceptions.RequestException(f"HTTP {response.status_code}: {url}")
    except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
        logger.error(f"Falha de conexão em: {url}: {e}")
        raise
        
def get_random_user_agent():
    try:
        ua = UserAgent(platforms=["desktop"], browsers=["Chrome"])
        agent = ua.random
        return agent
    except Exception as e:
        logger.critical("Falha ao criar o UserAgent. Encerrando...")
        sys.exit(0)
  
def filtrar_url(url):
    url_filtered = urlparse(url)
    dominio = f"{url_filtered.scheme}://{url_filtered.netloc}"
    return dominio  

def converter_https(url):
    parsed = urlparse(url)
    if parsed.scheme == 'http':
        return parsed._replace(scheme='https').geturl()
    return url  

def get_crawl_delay(url, agent):
    dominio = filtrar_url(url)
    robots_url = f"{dominio}/robots.txt"

    logger.info(f"Verificando Crawl-delay em: {robots_url}")

    rp = RobotFileParser()
    rp.set_url(robots_url)

    try:
        rp.read()
        delay = rp.crawl_delay(agent)
        if delay:
            logger.info(f"Crawl-delay encontrado: {delay} segundos")
            return delay
        else:
            logger.info("Nenhum Crawl-delay especificado")
            return None
    except Exception as e:
        logger.error(f"Erro ao ler o arquivo robots.txt para delay: {e}")
        return None  
      
def check_robots(url, agent):
    dominio = filtrar_url(url)
    robots_url=f"{dominio}/robots.txt"

    logger.info(f"Verificando regras em: {robots_url}")

    rp = RobotFileParser()
    rp.set_url(robots_url)

    try:
        rp.read()
    except Exception as e:
        logger.error(f"Erro ao ler o arquivo robots.txt: {e}")
        return False
    
    if(rp.can_fetch(agent, url)):
        return True
    else:
        return False