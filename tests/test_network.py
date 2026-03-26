import pytest
from unittest.mock import patch, MagicMock
from src.network import requisicao, converter_https, get_crawl_delay
from tenacity import RetryError

def test_converter_https():
    assert converter_https("http://example.com") == "https://example.com"
    assert converter_https("https://example.com") == "https://example.com"

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

@patch('src.network.RobotFileParser')
def test_get_crawl_delay(mock_rp):
    mock_instance = MagicMock()
    mock_instance.crawl_delay.return_value = 5
    mock_rp.return_value = mock_instance

    delay = get_crawl_delay("http://example.com", "test")
    assert delay == 5