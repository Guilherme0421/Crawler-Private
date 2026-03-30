import pytest
from unittest.mock import patch, MagicMock
from src.network import requisicao, converter_https, get_crawl_delay, gerar_headers_realistas
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

@patch('src.network.requests.get')
@patch('src.network.time.sleep')  # Mock sleep to avoid waiting
def test_requisicao_429_retry(mock_sleep, mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 429
    mock_response.raise_for_status.side_effect = Exception("429 Too Many Requests")
    mock_get.return_value = mock_response

    with pytest.raises(RetryError):
        requisicao("http://example.com", {"User-Agent": "test"})

    # Verificar se foi chamado múltiplas vezes devido ao retry
    assert mock_get.call_count > 1

@patch('src.network.requests.get')
@patch('src.network.time.sleep')
def test_requisicao_success(mock_sleep, mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "OK"
    mock_get.return_value = mock_response

    result = requisicao("http://example.com", {"User-Agent": "test"})
    assert result == "OK"
    # Verificar se verify=True foi passado e URL convertida
    mock_get.assert_called_with("https://example.com", headers={"User-Agent": "test"}, timeout=10, verify=True)

@patch('src.network.RobotFileParser')
def test_get_crawl_delay(mock_rp):
    mock_instance = MagicMock()
    mock_instance.crawl_delay.return_value = 5
    mock_rp.return_value = mock_instance

    delay = get_crawl_delay("http://example.com", "test")
    assert delay == 5