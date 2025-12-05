import threading
import time
import random
from src.config import logger, LINKS, LOCK, TELEFONES
from src.network import requisicao
from src.parser import parsing, encontrar_telefones
from src.database import verificar_existencia_numero

def descobrir_telefones(headers):
    thread_name = threading.current_thread().name
    logger.info(f"{thread_name} Iniciando Trabalho!")

    while True:
        delay = random.uniform(2.0, 5.0)
        time.sleep(delay)
        
        link_anuncio = None
        
        with LOCK:
            try:
                if len(LINKS) > 0:
                    link_anuncio = LINKS.pop()
                else:
                    logger.warning(f"[{thread_name}] Lista vazia. Encerrando.")
                    break
            except:
                break
        if link_anuncio is None:
            break
        
        logger.info(f"[{thread_name}] Acessando: {link_anuncio}")

        resposta_anuncio = requisicao(link_anuncio, headers)
        
        if resposta_anuncio:
            soup_anuncio = parsing(resposta_anuncio)
            if soup_anuncio:
                telefones = encontrar_telefones(soup_anuncio)
                if telefones:
                    for telefone in telefones:
                        if(verificar_existencia_numero(telefone)):
                            with LOCK:
                                logger.info(f"{thread_name} 📞 Encontrado: {telefone}")
                                TELEFONES.append(f"{telefone}; {link_anuncio}")
                        else:
                            logger.info(f"[{thread_name}] ❌ Ignorando repetido: {telefone}")
                else:
                    logger.info(f"[{thread_name}] ⚠️ Nenhum padrão de telefone encontrado: {link_anuncio}")
                    pass
            