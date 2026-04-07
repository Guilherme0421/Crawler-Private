import builtins
import sys
from unittest.mock import MagicMock

import main


def test_parse_args_single_url(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['main.py', '--url', 'https://example.com', '--threads', '2'])
    args = main.parse_args()

    assert args.url == ['https://example.com']
    assert args.threads == 2


def test_parse_args_multiple_urls(monkeypatch):
    monkeypatch.setattr(
        sys,
        'argv',
        [
            'main.py',
            '--url',
            'https://example.com',
            'https://outroexemplo.com',
            '--threads',
            '4',
        ],
    )
    args = main.parse_args()

    assert args.url == ['https://example.com', 'https://outroexemplo.com']
    assert args.threads == 4


def test_executar_crawler_com_multiplas_urls(monkeypatch):
    session = MagicMock()
    telemetria = MagicMock()
    telemetria.iniciar = MagicMock()
    telemetria.finalizar = MagicMock()
    telemetria.relatorio = MagicMock(return_value='relatorio')

    monkeypatch.setattr(main, 'TELEMETRIA', telemetria)
    monkeypatch.setattr(main, 'preparar_headers', lambda: ({'User-Agent': 'test-agent'}, 'agent'))
    monkeypatch.setattr(main, 'criar_sessao', lambda headers, verify=True: session)
    monkeypatch.setattr(
        main,
        'validar_acesso_robots',
        lambda url, agente: url != 'https://bloqueado.example.com',
    )
    monkeypatch.setattr(
        main,
        'obter_links_iniciais',
        lambda url, session_obj, agente: [f'{url}/link1'],
    )
    chamadas_enfileirar = []

    def fake_enfileirar_links(links):
        chamadas_enfileirar.append(list(links))
        return len(links)

    monkeypatch.setattr(main, 'enfileirar_links', fake_enfileirar_links)
    monkeypatch.setattr(main, 'iniciar_workers', lambda num_threads, agente, sess: None)

    exit_code = main.executar_crawler(
        ['https://example.com', 'https://bloqueado.example.com'],
        3,
        insecure=True,
    )

    assert exit_code == 0
    assert chamadas_enfileirar == [['https://example.com/link1']]
    telemetria.iniciar.assert_called_once()
    telemetria.finalizar.assert_called_once()
    session.close.assert_called_once()


def test_informar_inicio_buscas_exibe_mensagem_quando_nao_verbose(monkeypatch, capsys):
    monkeypatch.setattr(builtins, 'print', lambda msg: sys.stdout.write(msg + '\n'))

    main.informar_inicio_buscas(False)
    captured = capsys.readouterr()

    assert 'Iniciando Buscas' in captured.out


def test_informar_inicio_buscas_nao_exibe_mensagem_quando_verbose(monkeypatch, capsys):
    monkeypatch.setattr(builtins, 'print', lambda msg: sys.stdout.write(msg + '\n'))

    main.informar_inicio_buscas(True)
    captured = capsys.readouterr()

    assert captured.out == ''


def test_executar_crawler_nao_exibe_total_quando_todos_os_seeds_sao_bloqueados(monkeypatch):
    session = MagicMock()
    telemetria = MagicMock()
    telemetria.iniciar = MagicMock()
    telemetria.finalizar = MagicMock()
    telemetria.relatorio = MagicMock(return_value='relatorio')

    fake_logger = MagicMock()
    monkeypatch.setattr(main, 'logger', fake_logger)
    monkeypatch.setattr(main, 'TELEMETRIA', telemetria)
    monkeypatch.setattr(main, 'preparar_headers', lambda: ({}, 'agent'))
    monkeypatch.setattr(main, 'criar_sessao', lambda headers, verify=True: session)
    monkeypatch.setattr(main, 'validar_acesso_robots', lambda url, agente: False)
    monkeypatch.setattr(main, 'obter_links_iniciais', lambda url, session_obj, agente: ['https://example.com/link1'])
    monkeypatch.setattr(main, 'enfileirar_links', lambda links: len(links))
    monkeypatch.setattr(main, 'iniciar_workers', lambda num_threads, agente, sess: None)

    exit_code = main.executar_crawler(['https://bloqueado.example.com'], 2, insecure=False)

    assert exit_code == 0
    fake_logger.info.assert_any_call('Fim da execução. Logs salvos na pasta /logs.')
    fake_logger.info.assert_any_call('relatorio')
    assert not any('Total de links únicos enfileirados a partir das seeds:' in args[0] for args in fake_logger.info.call_args_list)
    assert fake_logger.warning.assert_any_call('Nenhum dos alvos pôde ser processado porque todos foram negados pelo robots.txt.')
    session.close.assert_called_once()
