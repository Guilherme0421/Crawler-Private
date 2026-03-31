import sys
import pytest
from src.app.cli.argparser import parse_args


def test_parse_args_single_url(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['main.py', '--url', 'https://example.com'])
    args = parse_args()

    assert args.url == ['https://example.com']
    assert args.threads == 3
    assert args.insecure is False


def test_parse_args_multiple_urls_and_insecure(monkeypatch):
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
            '--insecure',
        ],
    )
    args = parse_args()

    assert args.url == ['https://example.com', 'https://outroexemplo.com']
    assert args.threads == 4
    assert args.insecure is True


def test_help_argument_displays_usage(monkeypatch, capsys):
    monkeypatch.setattr(sys, 'argv', ['main.py', '--help'])

    with pytest.raises(SystemExit) as exc:
        parse_args()

    assert exc.value.code == 0
    captured = capsys.readouterr()
    assert 'usage:' in captured.out
    assert '--url' in captured.out
    assert '--threads' in captured.out
    assert '--insecure' in captured.out
