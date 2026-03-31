# 🕷️ PyCrawler - Extrator de números telefonicos v1.1.3
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/status-em_desenvolvimento-orange?style=for-the-badge)

> Um web crawler focado em extração de dados (telefones) de anúncios classificados, utilizando processamento paralelo para obter melhor eficiência.

> **Versão 1.1.3:** adicionada opção `-v/--verbose` e suporte para mais de uma URL.
---
## Funcionalidades
* **⚡ Multi-threading:** Utiliza o módulo `threading` para rodar múltiplos workers simultaneamente, acelerando a coleta de dados.
* **🛡️ Comportamento "Humano":** Implementa `random.uniform` para delays aleatórios entre requisições, evitando bloqueios de IP (Anti-Bot evasion).
* **🔒 Thread-Safe:** Uso de `LOCK` para garantir que a leitura/escrita no banco de dados não gere conflitos (Race Conditions).
* **📝 Logging Detalhado:** Sistema de logs colorido e estruturado para monitorar o status de cada worker em tempo real.
* **💾 Persistência de Dados:** Verificação automática de duplicidade no banco de dados antes de salvar novos registros.
* **🤖 Verificação de Robots.txt:** Verifica automaticamente se o acesso ao site é permitido antes de iniciar o crawling.
* **📊 Telemetria Integrada:** Coleta métricas em tempo real (URLs processadas, sucessos, falhas, telefones encontrados e tempo total).
* **🎯 Introdução Visual:** Exibe um banner introdutório no console ao iniciar, mostrando informações sobre a solução e status de inicialização.

---

## 🛠️ Tecnologias Utilizadas
| Tecnologia | Função |
| :--- | :--- |
| **Python** | Linguagem Núcleo |
| **BeautifulSoup4** | Parsing de HTML (Web Scraping) |
| **Requests** | Requisições HTTP |
| **Threading** | Concorrência e Paralelismo |
| **PyInstaller** | Geração de Executáveis Standalone |

---

## Como rodar ?
#### Pré-requisitos
Certifique-se de ter o Python instalado (versão 3.9+).
#### Passo a passo
####    1 - Clone o repositório
    git clone https://github.com/Guilherme0421/Crawler----Iniciante.git

####    2 - Crie um ambiente virtual (Recomendado):
    python -m venv crawler
    # No Windows:
    .\crawler\Scripts\activate
    # No Linux/Mac:
    source crawler/bin/activate
    
####    3 - Instale as dependências:
    pip install -r requierements.txt

####    4 - Execute os testes (opcional, mas recomendado):
    python -m pytest tests/
        
## Exemplos de como rodar o código direto pelo terminal (CLI)
#### Comando para rodar o programa com uso de threads padrão = 3.
    python main.py --url <URL>

#### Comando para rodar o programa com múltiplas seeds.
    python main.py --url <URL1> <URL2> <URL3>

#### Comando para rodar o programa com 5 threads.
    python main.py --url <URL> --threads 5

#### Exemplo prático:
    python main.py --url https://example.com https://outroexemplo.com --threads 4

---

## 🏗️ Arquitetura do Projeto

O projeto é estruturado em módulos para facilitar manutenção e extensibilidade:

- **`main.py`**: Ponto de entrada da aplicação. Gerencia argumentos CLI, inicializa telemetria, configura o logger e coordena os workers.
- **`src/config.py`**: Define estado global compartilhado, como `URL_QUEUE`, `SEEN_URLS`, `LOCK` e `TELEMETRIA`.
- **`src/app/cli/argparser.py`**: Centraliza a definição dos argumentos de linha de comando (`--url`, `--threads`, `--insecure`, `--verbose`).
- **`src/app/worker.py`**: Implementa a lógica dos workers que consomem a fila de URLs e extraem telefones em paralelo.
- **`src/domain/parser.py`**: Contém parsing de HTML, extração de links internos, limpezas de texto e extração/normalização de telefones.
- **`src/infra/network.py`**: Responsável por requisições HTTP, verificação de `robots.txt`, controle de crawl-delay, sessões e cabeçalhos realistas.
- **`src/infra/logger_config.py`**: Configura logs em arquivo e console, incluindo o modo silencioso padrão e o modo `-v/--verbose`.
- **`src/infra/database.py`**: Grava resultados extraídos em JSON e garante persistência segura.
- **`logs/`**: Armazena arquivos de log rotativos gerados durante a execução.
- **`tests/`**: Contém testes unitários para validar parsing, rede, CLI e comportamento do crawler.

A comunicação entre módulos ocorre via imports e compartilhamento de estruturas de dados thread-safe, com processamento paralelo coordenado pelo `main.py` e `src/app/worker.py`.

---

## 🧪 Testes

Execute os testes unitários para validar funcionalidades:

    python -m pytest tests/

Casos de teste incluem:
- Validação de extração de telefones (com/sem DDD, ignorando CEPs).
- Simulação de rate limiting (429) e retry.
- Conversão HTTP para HTTPS.

---

## 🤝 Contribuição

Contribuições são bem-vindas! Siga estes passos:

1. Fork o repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`).
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`).
4. Push para a branch (`git push origin feature/nova-funcionalidade`).
5. Abra um Pull Request.

Antes de contribuir, execute os testes e certifique-se de que o código segue as boas práticas.

---

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.