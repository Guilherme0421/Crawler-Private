from fake_useragent import UserAgent
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

def get_random_user_agent():
    ua = UserAgent(platforms=["desktop"], browsers=["Chrome"])
    agent = ua.random
    return agent

def robots_parser(url):
    url_filtered = urlparse(url)
    url_base = f"{url_filtered.scheme}://{url_filtered.netloc}"
    robots_url=f"{url_base}/robots.txt"

    print(f"Ferificando regras em: {robots_url}")

    rp = RobotFileParser()
    rp.set_url(robots_url)

    userAgent = get_random_user_agent()

    try:
        rp.read()
    except Exception as e:
        print(f"Erro ao ler o arquivo robots.txt: {e}")
        return False
    
    if(rp.can_fetch(url, userAgent)):
        return True
    else:
        return False


