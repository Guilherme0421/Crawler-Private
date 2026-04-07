import os
import json
from datetime import datetime
from src.config import logger

def salvar_telefones(telefones_novos, url_origem):
    """
    Salva telefones extraídos em um arquivo JSON estruturado.
    
    Args:
        telefones_novos (list): Lista de strings com números de telefone no formato E.164.
        url_origem (str): URL de onde os telefones foram extraídos.
    """
    # Verificar e criar pasta data/ se não existir
    data_dir = os.path.join(os.getcwd(), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        logger.info("Pasta 'data/' criada.")
    
    arquivo_path = os.path.join(data_dir, 'telefones_extraidos.json')
    
    # Carregar dados existentes
    dados_existentes = []
    if os.path.exists(arquivo_path):
        try:
            with open(arquivo_path, 'r', encoding='utf-8') as f:
                dados_existentes = json.load(f)
        except json.JSONDecodeError:
            logger.warning("Arquivo JSON corrompido, iniciando novo.")
            dados_existentes = []
    
    # Adicionar novos telefones
    timestamp = datetime.now().isoformat()
    novos_dados = []
    existentes_por_telefone = {d['telefone'] for d in dados_existentes}

    for telefone in telefones_novos:
        if telefone in existentes_por_telefone:
            continue

        entrada = {
            "telefone": telefone,
            "url_origem": url_origem,
            "data_coleta": timestamp
        }
        novos_dados.append(entrada)
        dados_existentes.append(entrada)
        existentes_por_telefone.add(telefone)
    
    # Salvar arquivo atualizado
    try:
        with open(arquivo_path, 'w', encoding='utf-8') as f:
            json.dump(dados_existentes, f, indent=4, ensure_ascii=False)
        logger.info(f"Telefones salvos com sucesso em {arquivo_path}. Adicionados: {len(novos_dados)}")
    except Exception as e:
        logger.critical(f"Erro ao salvar arquivo: {e}")