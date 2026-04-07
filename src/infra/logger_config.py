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
    backupCount=5,
    encoding='utf-8'
)

# Formatação: [Timestamp] [Level] [Módulo] - Mensagem
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s')
console_formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)

# Configurar logger
logger = logging.getLogger("SOC_Crawler")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Adicionar handler para console também
console_handler = logging.StreamHandler()
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)


class DefaultConsoleFilter(logging.Filter):
    def filter(self, record):
        if getattr(record, 'phone_output', False):
            return True

        message = record.getMessage()
        keywords = [
            'Relatório de Execução',
            'Fim da execução',
        ]

        return any(keyword in message for keyword in keywords)


def set_console_verbosity(verbose: bool):
    console_handler.filters = []
    if verbose:
        console_handler.setFormatter(formatter)
    else:
        console_handler.setFormatter(console_formatter)
        console_handler.addFilter(DefaultConsoleFilter())
