import argparse
import threading
import sys
import os
import time
from src.config import logger, URL_QUEUE, SEEN_URLS, TELEMETRIA
from src.network import (
    get_random_user_agent,
    check_robots,
    requisicao,
    get_crawl_delay,
    gerar_headers_realistas,
    criar_sessao,
)
from src.parser import parsing, encontrar_links
from src.worker import descobrir_telefones


def exibir_introducao():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 60)
    print("      CRAWLER PROFISSIONAL - SOLUÇÃO DE EXTRAÇÃO v1.1.0")
    print("=" * 60)
    print("  Desenvolvido por: Killi")
    print("  Status: Sistema Inicializado...")
    print("  Segurança: HTTPS & Stealth Mode Ativados")
    print("=" * 60)
    print("\n")
    time.sleep(1)


def parse_args():
    parser = argparse.ArgumentParser(description="Crawler SOC - Extrator de numeros de telefone.")
    parser.add_argument("--url", required=True, help="URL inicial do site alvo (com http/https)")
    parser.add_argument("--threads", type=int, default=3, help="Número de threads que serão usadas.")
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Desativa verificação SSL (apenas para testes em ambientes de desenvolvimento).",
    )
    return parser.parse_args()


def preparar_headers():
    agent = get_random_user_agent()
    return gerar_headers_realistas(agent), agent


def validar_acesso_robots(url_alvo, agente):
    if not check_robots(url_alvo, agente):
        logger.error("🔴 Acesso negado pelo robots.txt. Encerrando operação!")
        return False

    logger.info("Permissão concedida pelo robots.txt")
    return True


def obter_crawl_delay(url_alvo, agente):
    return get_crawl_delay(url_alvo, agente)


def obter_links_iniciais(url_alvo, session, agente):
    html_inicial = requisicao(url_alvo, session, obter_crawl_delay(url_alvo, agente))
    if not html_inicial:
        logger.critical("Falha ao baixar a página inicial. Encerrando!")
        return []

    soup = parsing(html_inicial)
    if not soup:
        logger.critical("Erro ao realizar parsing da página inicial. Encerrando!")
        return []

    return encontrar_links(soup, url_alvo)


def enfileirar_links(links):
    adicionados = 0
    for link in links:
        if link not in SEEN_URLS:
            URL_QUEUE.put(link)
            SEEN_URLS.add(link)
            adicionados += 1
    return adicionados


def iniciar_workers(num_threads, agente, session):
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(
            target=descobrir_telefones,
            args=(agente, session),
            name=f"Worker - {i + 1}",
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def executar_crawler(url_alvo, num_threads, insecure=False):
    TELEMETRIA.iniciar()

    headers, agente = preparar_headers()
    session = criar_sessao(headers, verify=not insecure)

    if insecure:
        logger.warning("Modo inseguro ativado: verificação SSL desabilitada.")

    try:
        if not validar_acesso_robots(url_alvo, agente):
            return 1

        novos_links = obter_links_iniciais(url_alvo, session, agente)
        adicionados = enfileirar_links(novos_links)

        logger.info(f"Seed inicial: {adicionados} links únicos enfileirados para processamento.")

        if URL_QUEUE.empty():
            logger.warning("Nenhum link interno encontrado.")
            return 0

        iniciar_workers(num_threads, agente, session)

        TELEMETRIA.finalizar()
        logger.info("Fim da execução. Logs salvos na pasta /logs.")
        logger.info(TELEMETRIA.relatorio())
        return 0
    finally:
        session.close()


def main():
    exibir_introducao()
    args = parse_args()

    logger.info("---- INICIANDO CRAWLER ----")
    logger.info(f"Alvo: {args.url}")
    logger.info(f"Threads: {args.threads}")
    logger.info(f"Verificação SSL: {'desabilitada' if args.insecure else 'ativa'}")

    exit_code = executar_crawler(args.url, args.threads, insecure=args.insecure)
    sys.exit(exit_code)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Interrupção manual (Ctrl + C). Encerrando...")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Erro não tratado no main: {e}")
        sys.exit(1)
