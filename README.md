# 🕷️ PyCrawler - Extrator de números telefonicos
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

---

## 🛠️ Tecnologias Utilizadas
| Tecnologia | Função |
|Data | Descrição |
| :--- | :--- |
| **Python** | Linguagem Núcleo |
| **BeautifulSoup4** | Parsing de HTML (Web Scraping) |
| **Requests** | Requisições HTTP |
| **Threading** | Concorrência e Paralelismo |

---

## Como rodar ?
#### Pré-requisitos
Certifique-se de ter o Python instalado.
#### Passo a passo
####    1 - Clone o repositório
    git clone https://github.com/Guilherme0421/Crawler----Iniciante/tree/aprimoramento-craw

####    2 - Crie um ambiente virtual (Recomendado):
    pip install virtualenv | virtualenv venv | source venv/bin/activate
    
####    3 - Instale as dependências:
    pip install -r requirements.txt
        
## Exemplos de como rodar o código direto pelo terminal (CLI)
#### Comando para rodar o programa com uso de threads padrão = 3.
    python main.py --url <URL>

#### Comando para definir a quantidade de threads
    python main.py --url <URL> --threads <VALOR>