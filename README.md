# 🕷️ PyCrawler - Extrator de números telefonicos v1.0.1
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/status-em_desenvolvimento-orange?style=for-the-badge)

> Um web crawler focado em extração de dados (telefones) de anúncios classificados, utilizando processamento paralelo para obter melhor eficiência.
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

#### Comando para rodar o programa com 5 threads.
    python main.py --url <URL> --threads 5

#### Exemplo prático:
    python main.py --url https://example.com --threads 4

---

## 🏗️ Arquitetura do Projeto

O projeto é estruturado em módulos para facilitar manutenção e extensibilidade:

- **`main.py`**: Ponto de entrada da aplicação. Gerencia argumentos CLI, inicializa telemetria e coordena threads.
- **`src/config.py`**: Contém configurações globais, como locks para thread-safety e telemetria.
- **`src/network.py`**: Responsável por requisições HTTP, verificação de robots.txt, rate limiting e retry logic.
- **`src/parser.py`**: Parsing de HTML, extração de links e telefones usando BeautifulSoup e phonenumbers.
- **`src/worker.py`**: Lógica dos workers que processam URLs em paralelo.
- **`src/database.py`**: Persistência de dados extraídos.
- **`src/logger_config.py`**: Configuração de logging estruturado.
- **`data/`**: Armazenamento de dados extraídos (JSON).
- **`logs/`**: Arquivos de log rotativos.
- **`tests/`**: Testes unitários com Pytest.

A comunicação entre módulos ocorre via imports e compartilhamento de estruturas de dados thread-safe (como listas e locks).

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

#### Comando para definir a quantidade de threads
    python main.py --url <URL> --threads <VALOR>