import queue
import threading
from unittest.mock import MagicMock

from src import worker


def test_descobrir_telefones_sem_links(monkeypatch):
    fila = queue.Queue()
    monkeypatch.setattr(worker, 'URL_QUEUE', fila)
    monkeypatch.setattr(worker, 'time', MagicMock(sleep=lambda *_: None))
    monkeypatch.setattr(worker, 'random', MagicMock(uniform=lambda *_: 0))

    session = MagicMock()
    worker.descobrir_telefones('agent', session)

    assert fila.empty()


def test_descobrir_telefones_processa_link_e_salva(monkeypatch):
    fila = queue.Queue()
    fila.put('https://example.com/anuncio')
    monkeypatch.setattr(worker, 'URL_QUEUE', fila)
    monkeypatch.setattr(worker, 'LOCK', threading.Lock())
    monkeypatch.setattr(worker, 'time', MagicMock(sleep=lambda *_: None))
    monkeypatch.setattr(worker, 'random', MagicMock(uniform=lambda *_: 0))

    telemetria = MagicMock(urls_processadas=0, sucessos=0, falhas=0, telefones_encontrados=0)
    monkeypatch.setattr(worker, 'TELEMETRIA', telemetria)
    monkeypatch.setattr(worker, 'get_crawl_delay', lambda url, agente: None)
    monkeypatch.setattr(worker, 'requisicao', lambda url, session, delay: '<html></html>')
    monkeypatch.setattr(worker, 'parsing', lambda html: MagicMock())
    monkeypatch.setattr(worker, 'extrair_texto', lambda soup: 'Contato: (11) 99999-9999')
    monkeypatch.setattr(worker, 'encontrar_telefones', lambda texto: ["+5511999999999"])

    salvar_mock = MagicMock()
    monkeypatch.setattr(worker, 'salvar_telefones', salvar_mock)

    session = MagicMock()
    worker.descobrir_telefones('agent', session)

    assert telemetria.urls_processadas == 1
    assert telemetria.sucessos == 1
    assert telemetria.falhas == 0
    assert telemetria.telefones_encontrados == 1
    salvar_mock.assert_called_once_with(["+5511999999999"], 'https://example.com/anuncio')


def test_descobrir_telefones_falha_incrementa_falhas(monkeypatch):
    fila = queue.Queue()
    fila.put('https://example.com/anuncio')
    monkeypatch.setattr(worker, 'URL_QUEUE', fila)
    monkeypatch.setattr(worker, 'LOCK', threading.Lock())
    monkeypatch.setattr(worker, 'time', MagicMock(sleep=lambda *_: None))
    monkeypatch.setattr(worker, 'random', MagicMock(uniform=lambda *_: 0))

    telemetria = MagicMock(urls_processadas=0, sucessos=0, falhas=0, telefones_encontrados=0)
    monkeypatch.setattr(worker, 'TELEMETRIA', telemetria)
    monkeypatch.setattr(worker, 'get_crawl_delay', lambda url, agente: None)
    monkeypatch.setattr(worker, 'requisicao', lambda url, session, delay: None)

    session = MagicMock()
    worker.descobrir_telefones('agent', session)

    assert telemetria.urls_processadas == 1
    assert telemetria.sucessos == 0
    assert telemetria.falhas == 1
    assert telemetria.telefones_encontrados == 0
