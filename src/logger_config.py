import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

# Criar pasta logs se não existir
if not os.path.exists('logs'):
    os.makedirs('logs')

# Nome do arquivo baseado na data atual
log_filename = datetime.now().strftime('logs/crawler_%Y-%m-%d.log')

# Configurar RotatingFileHandler
handler = RotatingFileHandler(
    log_filename,
    maxBytes=5 * 1024 * 1024,  # 5MB
    backupCount=5
)

# Formatação: [Timestamp] [Level] [Módulo] - Mensagem
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s')
handler.setFormatter(formatter)

# Configurar logger
logger = logging.getLogger("SOC_Crawler")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Adicionar handler para console também
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)