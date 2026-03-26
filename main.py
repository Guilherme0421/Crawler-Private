import argparse
import threading
import sys
from src.config import logger, LINKS, TELEMETRIA
from src.network import get_random_user_agent, check_robots, requisicao
from src.parser import parsing, encontrar_links
from src.worker import descobrir_telefones

def main():
    # Configuração de argumentos(CLI)
    parser = argparse.ArgumentParser(description="Crawler SOC - Extrator de numeros de telefone.")
    parser.add_argument("--url", required=True, help="URL Inicial do site alvo (com http/https)")
    parser.add_argument("--threads", type=int, default=3, help="Número de threads que serão usadas.")
    
    args = parser.parse_args()
    url_alvo = args.url
    num_threads = args.threads
    
    logger.info("---- INICIANDO CRAWLER ----")
    logger.info(f"Alvo: {url_alvo}")
    logger.info(f"Threads: {num_threads}")
    
    TELEMETRIA.iniciar()
    
    agent = get_random_user_agent()
    header = {'User-Agent': agent}
    
    if not check_robots(url_alvo, agent):
        logger.error("🔴 Acesso negado pelo robots.txt. Encerrando operação!")
        sys.exit(1)
    else:
        logger.info("Permissão concedida pelo robots.txt")
        
    html_inicial = requisicao(url_alvo, header)
    
    if not html_inicial:
        logger.critical("Falha ao baixar a página inicial. Encerrando!")
        sys.exit(1)
        
    soup = parsing(html_inicial)
    if soup:
        novos_links = encontrar_links(soup, url_alvo)
        LINKS.extend(novos_links)
        
        logger.info(f"Seed inicial: {len(LINKS)} encontrados para processament.")
        
        if len(LINKS) == 0:
            logger.warning("Nenhum link interno encontrado.")
            sys.exit(0)
            
        threads = []
        for i in range(num_threads):
            t = threading.Thread(target=descobrir_telefones, args=(header,), name=f"Worker - {i+1}")
            threads.append(t)
            t.start()
            
        for t in threads:
            t.join()
            
        TELEMETRIA.finalizar()
        logger.info("Fim da execução. Logs salvos na pasta /logs.")
        logger.info(TELEMETRIA.relatorio())
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Interrupção manual (Ctrl + C). Encerrando...")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Erro não tratado no main: {e}")