import json
from pathlib import Path

from src.infra.database import salvar_telefones


def test_salvar_telefones_cria_arquivo_e_registra(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    salvar_telefones(["+5511999999999"], "https://site.com")

    data_file = tmp_path / 'data' / 'telefones_extraidos.json'
    assert data_file.exists()

    registros = json.loads(data_file.read_text(encoding='utf-8'))
    assert len(registros) == 1
    assert registros[0]['telefone'] == "+5511999999999"
    assert registros[0]['url_origem'] == "https://site.com"


def test_salvar_telefones_nao_duplica_telefone(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    salvar_telefones(["+5511999999999"], "https://site.com")
    salvar_telefones(["+5511999999999"], "https://site.com")

    data_file = tmp_path / 'data' / 'telefones_extraidos.json'
    registros = json.loads(data_file.read_text(encoding='utf-8'))
    assert len(registros) == 1


def test_salvar_telefones_nao_duplica_telefone_em_urls_diferentes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    salvar_telefones(["+5511999999999"], "https://site1.com")
    salvar_telefones(["+5511999999999"], "https://site2.com")

    data_file = tmp_path / 'data' / 'telefones_extraidos.json'
    registros = json.loads(data_file.read_text(encoding='utf-8'))
    assert len(registros) == 1


def test_salvar_telefones_reinicia_arquivo_corrompido(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    data_dir = tmp_path / 'data'
    data_dir.mkdir()
    arquivo = data_dir / 'telefones_extraidos.json'
    arquivo.write_text('isso não é um JSON válido', encoding='utf-8')

    salvar_telefones(["+5511999999999"], "https://site.com")

    registros = json.loads(arquivo.read_text(encoding='utf-8'))
    assert len(registros) == 1
    assert registros[0]['telefone'] == "+5511999999999"
