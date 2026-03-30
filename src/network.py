import requests
import random
import time
import threading
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from src.config import logger

ROBOTS_CACHE = {}
ROBOTS_CACHE_LOCK = threading.Lock()


def _filtrar_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def _carregar_robot_parser(dominio):
    robots_url = f"{dominio}/robots.txt"
    logger.info(f"Carregando robots.txt em: {robots_url}")

    rp = RobotFileParser()
    rp.set_url(robots_url)

    try:
        rp.read()
        return rp
    except Exception as e:
        logger.error(f"Erro ao ler robots.txt ({robots_url}): {e}")
        return None


def _get_robot_parser(url):
    dominio = _filtrar_url(url)

    with ROBOTS_CACHE_LOCK:
        if dominio in ROBOTS_CACHE:
            return ROBOTS_CACHE[dominio]

        parser = _carregar_robot_parser(dominio)
        ROBOTS_CACHE[dominio] = parser
        return parser


def criar_sessao(headers=None):
    session = requests.Session()
    session.verify = True
    if headers:
        session.headers.update(headers)
    return session

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=2, max=8),
    retry=retry_if_exception_type((requests.exceptions.RequestException, requests.exceptions.Timeout)),
    before_sleep=lambda retry_state: logger.warning(
        f"Tentativa {retry_state.attempt_number} falhou: {retry_state.outcome.exception()}. "
        f"Tentando novamente em {retry_state.next_action.sleep} segundos."
    )
)
def requisicao(url, session=None, crawl_delay=None):
    url = converter_https(url)

    if session is None:
        session = criar_sessao()

    if crawl_delay is None:
        crawl_delay = random.uniform(1, 3)

    delay = random.uniform(crawl_delay, 2 * crawl_delay)
    logger.info(f"Aplicando delay de {delay:.2f} segundos")
    time.sleep(delay)

    try:
        response = session.get(url, timeout=10)

        if response.status_code == 200:
            return response.text
        if response.status_code == 429:
            logger.warning(f"Erro 429 (Too Many Requests) ao acessar: {url}. Pausando por 60 segundos.")
            time.sleep(60)
            raise requests.exceptions.RequestException(f"429 Too Many Requests: {url}")

        logger.warning(f"Status Code {response.status_code} ao acessar: {url}")
        raise requests.exceptions.RequestException(f"HTTP {response.status_code}: {url}")

    except (
        requests.exceptions.SSLError,
        requests.exceptions.ConnectionError,
        requests.exceptions.TooManyRedirects,
        requests.exceptions.RequestException,
        requests.exceptions.Timeout,
    ) as e:
        logger.error(f"Falha de conexão em: {url}: {e}")
        raise


def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]
    return random.choice(user_agents)


def gerar_headers_realistas(user_agent=None):
    if user_agent is None:
        user_agent = get_random_user_agent()

    headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    }
    return headers


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
    parser = _get_robot_parser(url)
    if parser is None:
        return None

    delay = parser.crawl_delay(agent)
    if delay:
        logger.info(f"Crawl-delay encontrado: {delay} segundos")
        return delay

    logger.info("Nenhum Crawl-delay especificado")
    return None


def check_robots(url, agent):
    parser = _get_robot_parser(url)
    if parser is None:
        return False

    can_fetch = parser.can_fetch(agent, url)
    if can_fetch:
        return True

    logger.warning(f"Acesso negado pelo robots.txt para {url} com agente {agent}")
    return False
