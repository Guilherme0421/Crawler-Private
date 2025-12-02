

import time
import threading


def fazer_requisicao_web():
    print("Iniciando requisição web...")
    time.sleep(3)
    print("Requisição web concluída.")
    

thread01 = threading.Thread(target=fazer_requisicao_web)
thread01.start()

thread02 = threading.Thread(target=fazer_requisicao_web)
thread02.start()

thread03 = threading.Thread(target=fazer_requisicao_web)
thread03.start()















response = requisicao(urlAutomoveis)
if(response):
    soup_busca = parsing(response)
    if(soup_busca):
        links = encontrar_links(soup_busca)
        
        for link in links:
            resposta_anuncio = requisicao(dominio + link)
            print(f"Acessando o link: {dominio + link}")
            if resposta_anuncio:
                soup_anuncio = parsing(resposta_anuncio)
            
                if soup_anuncio:
                    print(encontrar_telefones(soup_anuncio))
    