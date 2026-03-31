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
        msg='[Worker] Encontrados 2 telefone(s) em https://example.com',
        args=(),
        exc_info=None,
    )
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


def test_verbose_console_removes_filter():
    logger_config.set_console_verbosity(True)
    assert logger_config.console_handler.filters == []
