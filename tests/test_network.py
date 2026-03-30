import pytest
import urllib3
from unittest.mock import patch, MagicMock
import src.network as network
from src.network import requisicao, converter_https, get_crawl_delay, gerar_headers_realistas, criar_sessao
from tenacity import RetryError

def test_converter_https():
    assert converter_https("http://example.com") == "https://example.com"
    assert converter_https("https://example.com") == "https://example.com"

def test_gerar_headers_realistas():
    headers = gerar_headers_realistas()
    assert 'User-Agent' in headers
    assert 'Accept-Language' in headers
    assert 'Accept' in headers
    assert headers['Accept-Language'] == 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'

def test_criar_sessao_aplica_headers():
    session = criar_sessao({"User-Agent": "test-agent"})
    assert session.headers["User-Agent"] == "test-agent"

@patch('src.network.urllib3.disable_warnings')
def test_criar_sessao_insecure_disables_warnings(mock_disable):
    session = criar_sessao({"User-Agent": "test-agent"}, verify=False)
    assert session.verify is False
    mock_disable.assert_called_once_with(urllib3.exceptions.InsecureRequestWarning)

@patch('src.network.requests.Session')
@patch('src.network.time.sleep')
def test_requisicao_429_retry(mock_sleep, mock_session_cls):
    mock_session = MagicMock()
    mock_response = MagicMock()
    mock_response.status_code = 429
    mock_session.get.return_value = mock_response
    mock_session_cls.return_value = mock_session

    with pytest.raises(RetryError):
        requisicao("http://example.com")

    assert mock_session.get.call_count > 1

@patch('src.network.requests.Session')
@patch('src.network.time.sleep')
def test_requisicao_success(mock_sleep, mock_session_cls):
    mock_session = MagicMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "OK"
    mock_session.get.return_value = mock_response
    mock_session_cls.return_value = mock_session

    result = requisicao("http://example.com")
    assert result == "OK"
    mock_session.get.assert_called_with("https://example.com", timeout=10)

@patch('src.network.RobotFileParser')
def test_get_crawl_delay(mock_rp):
    mock_instance = MagicMock()
    mock_instance.crawl_delay.return_value = 5
    mock_rp.return_value = mock_instance

    delay = get_crawl_delay("http://example.com", "test")
    assert delay == 5

@patch('src.network._get_robot_parser')
def test_check_robots_denied(mock_get_parser):
    parser = MagicMock()
    parser.can_fetch.return_value = False
    mock_get_parser.return_value = parser

    assert network.check_robots("http://example.com", "test") is False

@patch('src.network._carregar_robot_parser')
def test_get_robot_parser_cache(mock_loader):
    network.ROBOTS_CACHE.clear()
    parser = MagicMock()
    mock_loader.return_value = parser

    parser1 = network._get_robot_parser("http://example.com/p1")
    parser2 = network._get_robot_parser("http://example.com/p2")

    assert parser1 is parser2
    assert mock_loader.call_count == 1