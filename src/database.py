from src.config import logger, CACHE_TELEFONES, LOCK, TELEFONES

def verificar_existencia_numero(numero):
    with LOCK:
        if numero in CACHE_TELEFONES:
            return False
        else:
            CACHE_TELEFONES.add(numero)
            return True
        
def salvar_telefones():
    try:
        with open("./data/telefones.csv","a") as arquivo:
            for telefone in TELEFONES:
                arquivo.write(f"{telefone}\n")
            print("Telefones salvos com sucesso em telefones.csv")
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")