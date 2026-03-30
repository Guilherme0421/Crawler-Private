import queue
import threading
import time
import random
from src.config import logger, URL_QUEUE, LOCK, TELEMETRIA
from src.network import requisicao, get_crawl_delay
from src.parser import parsing, encontrar_telefones, extrair_texto
from src.database import salvar_telefones


def descobrir_telefones(agente, session):
    thread_name = threading.current_thread().name
    logger.info(f"{thread_name} Iniciando Thread!")

    while True:
        delay = random.uniform(2.0, 5.0)
        time.sleep(delay)

        try:
            link_alvo = URL_QUEUE.get_nowait()
        except queue.Empty:
            logger.info(f"[{thread_name}] Fila vazia. Encerrando thread.")
            break

        try:
            with LOCK:
                TELEMETRIA.urls_processadas += 1

            logger.info(f"[{thread_name}] Acessando: {link_alvo}")

            crawl_delay = get_crawl_delay(link_alvo, agente)
            resposta_html = requisicao(link_alvo, session, crawl_delay)

            if resposta_html:
                with LOCK:
                    TELEMETRIA.sucessos += 1

                soup_anuncio = parsing(resposta_html)
                if soup_anuncio:
                    texto_anuncio = extrair_texto(soup_anuncio)
                    telefones = encontrar_telefones(texto_anuncio)

                    if telefones:
                        logger.info(f"[{thread_name}] Encontrados {len(telefones)} telefone(s) em {link_alvo}")
                        salvar_telefones(telefones, link_alvo)
                        with LOCK:
                            TELEMETRIA.telefones_encontrados += len(telefones)
                    else:
                        logger.info(f"[{thread_name}] Nenhum padrão de telefone encontrado: {link_alvo}")
            else:
                with LOCK:
                    TELEMETRIA.falhas += 1
                logger.warning(f"[{thread_name}] Falha ao acessar: {link_alvo}")
        finally:
            URL_QUEUE.task_done()
            