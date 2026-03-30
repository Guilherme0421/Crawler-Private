import threading
import queue
from datetime import datetime

from src.logger_config import logger

URL_QUEUE = queue.Queue()
SEEN_URLS = set()
CACHE_TELEFONES = set()
LOCK = threading.Lock()

class Telemetria:
    def __init__(self):
        self.urls_processadas = 0
        self.sucessos = 0
        self.falhas = 0
        self.telefones_encontrados = 0
        self.tempo_inicio = None
        self.tempo_fim = None

    def iniciar(self):
        self.tempo_inicio = datetime.now()

    def finalizar(self):
        self.tempo_fim = datetime.now()

    def relatorio(self):
        if self.tempo_fim and self.tempo_inicio:
            tempo_total = self.tempo_fim - self.tempo_inicio
        else:
            tempo_total = "N/A"
        rel = f"""
Relatório de Execução:
- URLs Processadas: {self.urls_processadas}
- Sucessos: {self.sucessos}
- Falhas: {self.falhas}
- Telefones Encontrados: {self.telefones_encontrados}
- Tempo Total: {tempo_total}
"""
        return rel

TELEMETRIA = Telemetria()


# urlAutomoveis = "https://django-anuncios.solyd.com.br/automoveis/"  