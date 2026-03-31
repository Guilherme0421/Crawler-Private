import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Crawler SOC - Extrator de numeros de telefone.",
        add_help=False,
    )
    parser.add_argument(
        "--help",
        "-h",
        action="help",
        help="Exibe esta mensagem de ajuda e sai.",
    )
    parser.add_argument(
        "--url",
        "-u",
        required=True,
        nargs="+",
        help="URL(s) iniciais do site alvo (com http/https). Suporta múltiplas URLs separadas por espaço.",
    )
    parser.add_argument(
        "--threads",
        "-t",
        type=int,
        default=3,
        help="Número de threads que serão usadas.",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Desativa verificação SSL (apenas para testes em ambientes de desenvolvimento).",
    )
    return parser.parse_args()
