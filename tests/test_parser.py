import pytest
from src.parser import encontrar_telefones

def test_encontrar_telefones_com_ddd():
    texto = "Ligue para (11) 99999-9999 ou 11 99999-9999"
    telefones = encontrar_telefones(texto)
    assert telefones is not None
    assert "+5511999999999" in telefones

def test_encontrar_telefones_sem_ddd():
    texto = "Contato: 99999-9999"
    telefones = encontrar_telefones(texto)
    assert telefones is None  # Sem DDD, pode não ser válido

def test_ignorar_ceps():
    texto = "CEP: 01234-567"
    telefones = encontrar_telefones(texto)
    assert telefones is None

def test_normalizacao_e164():
    texto = "Telefone: (21) 98765-4321"
    telefones = encontrar_telefones(texto)
    assert telefones is not None
    assert "+5521987654321" in telefones

def test_multiplos_telefones():
    texto = "Tel1: (11) 99999-9999, Tel2: 21 98765-4321"
    telefones = encontrar_telefones(texto)
    assert len(telefones) == 2
    assert "+5511999999999" in telefones
    assert "+5521987654321" in telefones