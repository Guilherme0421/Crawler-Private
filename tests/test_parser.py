import pytest
from src.domain.parser import parsing, encontrar_links, extrair_texto, encontrar_telefones

def test_parsing_html_retorna_soup():
    html = '<html><head><title>Teste</title></head><body><p>Olá</p></body></html>'
    soup = parsing(html)
    assert soup is not None
    assert soup.title.string == 'Teste'

def test_encontrar_links_filtra_dominio_e_tipos_invalidos():
    html = '''
    <html><body>
        <a href="/pagina1">Link interno</a>
        <a href="https://example.com/pagina2">Outro interno</a>
        <a href="https://outro.com">Externo</a>
        <a href="mailto:contato@example.com">Email</a>
        <a href="tel:123">Telefone</a>
        <a href="#ancora">Ancora</a>
    </body></html>
    '''
    soup = parsing(html)
    links = encontrar_links(soup, 'https://example.com')
    assert 'https://example.com/pagina1' in links
    assert 'https://example.com/pagina2' in links
    assert all('outro.com' not in link for link in links)
    assert all('mailto:' not in link for link in links)
    assert all('tel:' not in link for link in links)

def test_extrair_texto_remove_scripts_e_styles():
    html = '''
    <html><head><style>body {}</style></head>
    <body><script>console.log('x')</script><p>Conteúdo útil</p></body>
    </html>
    '''
    soup = parsing(html)
    texto = extrair_texto(soup)
    assert 'Conteúdo útil' in texto
    assert 'console.log' not in texto
    assert 'body {}' not in texto


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