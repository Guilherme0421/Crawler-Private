import logging

from src.infra import logger_config


def test_default_console_filter_allows_found_info():
    logger_config.set_console_verbosity(False)
    filters = logger_config.console_handler.filters
    assert len(filters) == 1

    found_record = logging.LogRecord(
        name='SOC_Crawler',
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg='https://example.com: +5511999999999',
        args=(),
        exc_info=None,
    )
    found_record.phone_output = True
    assert filters[0].filter(found_record) is True

    other_record = logging.LogRecord(
        name='SOC_Crawler',
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg='Seed inicial [https://example.com]: 5 links únicos enfileirados para processamento.',
        args=(),
        exc_info=None,
    )
    assert filters[0].filter(other_record) is False

    save_record = logging.LogRecord(
        name='SOC_Crawler',
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg='Telefones salvos com sucesso em data/telefones_extraidos.json. Adicionados: 2',
        args=(),
        exc_info=None,
    )
    assert filters[0].filter(save_record) is False


def test_verbose_console_removes_filter():
    logger_config.set_console_verbosity(True)
    assert logger_config.console_handler.filters == []


def test_console_formatter_plain_message_when_not_verbose():
    logger_config.set_console_verbosity(False)
    record = logging.LogRecord(
        name='SOC_Crawler',
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg='https://example.com: +5511999999999',
        args=(),
        exc_info=None,
    )
    record.phone_output = True
    formatted = logger_config.console_handler.format(record)

    assert formatted == 'https://example.com: +5511999999999'
