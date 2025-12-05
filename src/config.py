import logging
import os
import threading
from datetime import datetime

if not os.path.exists('logs'):
    os.makedirs('logs')
    
log_filename = datetime.now().strftime('logs/crawler_%Y-%m-%d.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(threadName)s] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("SOC_Crawler")

LINKS = []
TELEFONES = []
CACHE_TELEFONES = set()
LOCK = threading.Lock()


# urlAutomoveis = "https://django-anuncios.solyd.com.br/automoveis/"  