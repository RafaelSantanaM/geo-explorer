"""
Ponto de Entrada Principal (CLI) do Geo-Explorer.
Permite executar os comandos via argumentos de terminal ou através de um menu interativo.
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from comandos.trilha import executar_comando_trilha
from comandos.desafio import executar_comando_desafio
from comandos.certificado import executar_comando_certificado
from comandos.listar import executar_comando_listar
from app.gerenciador import listar_tecnologias


def exibir_banner():
    banner = r"""
   _____ ______ ____        ______ _____  _      ____  _____  ______ _____  
  / ____|  ____/ __ \      |  ____|  __ \| |    / __ \|  __ \|  ____|  __ \ 
 | |  __| |__ | |  | |_____| |__  | |__) | |   | |  | | |__) | |__  | |__) |
 | | |_ |  __|| |  | |_____|  __| |  ___/| |   | |  | |  _  /|  __| |  _  / 
 | |__| | |___| |__| |     | |____| |    | |___| |__| | | \ \| |____| | \ \ 
  \_____|______\____/      |______|_|    |______\____/|_|  \_\______|_|  \_\
    """
    print(banner)
    print("      🚀 Explorador de Trilhas, Desafios & Certificados com IBM Bob")
    print("      Digital Innovation One (DIO) | Bootcamp IBM Bob\n")


def menu_interativo():
    """Modo interativo amigável quando nenhum argumento é passado."""
    exibir_banner()

    while True:
        print("=" * 60)
        print("  🧭 MENU PRINCIPAL - SELECIONE UMA OPÇÃO:")
        print("=" * 60)
        print("  [1] 📖 Consultar Trilha de Estudos")
        print("  [2] 🎯 Obter Desafio de Código")
        print("  [3] 📜 Emitir Certificado Fictício")
        print("  [4] 📋 Listar Todas as Trilhas e Tecnologias")
        print("  [5] 🤖 Iniciar Servidor MCP (Model Context Protocol)")
        print("  [6] 🌐 Iniciar Interface Web Local")
        print("  [0] ❌ Sair")
        print("-" * 60)

        escolha = input("Digite a opção desejada [0-6]: ").strip()

        if escolha == "0":
            print("\n👋 Até logo e bons estudos com o Geo-Explorer e IBM Bob!\n")
            break

        elif escolha == "1":
            print("\n--- Consultar Trilha ---")
            techs = listar_tecnologias()
            print("Tecnologias disponíveis: " + ", ".join(t["id"] for t in techs))
            tech = input("Informe a tecnologia: ").strip()
            nivel = input("Informe o nível (iniciante/intermediario/avancado ou deixe em branco): ").strip() or None
            executar_comando_trilha(tech, nivel)

        elif escolha == "2":
            print("\n--- Obter Desafio de Código ---")
            tech = input("Informe a tecnologia (ex: python, geoprocessamento, ibm-bob): ").strip()
            nivel = input("Informe o nível (iniciante/intermediario/avancado): ").strip()
            executar_comando_desafio(tech, nivel)

        elif escolha == "3":
            print("\n--- Emitir Certificado ---")
            nome = input("Nome completo do aluno: ").strip()
            tech = input("Tecnologia concluída: ").strip()
            nivel = input("Nível concluído (iniciante/intermediario/avancado): ").strip()
            salvar_input = input("Deseja salvar arquivo HTML/JSON? (s/N): ").strip().lower()
            salvar = salvar_input in ("s", "sim", "y", "yes")
            executar_comando_certificado(nome, tech, nivel, salvar=salvar, formato="ambos")

        elif escolha == "4":
            executar_comando_listar()

        elif escolha == "5":
            print("\n🤖 Iniciando Servidor MCP no modo stdio...")
            from app.mcp_server import iniciar_servidor_mcp
            iniciar_servidor_mcp()
            break

        elif escolha == "6":
            print("\n🌐 Iniciando servidor web...")
            from app.web import iniciar_servidor_web
            iniciar_servidor_web(porta=8000)
            break

        else:
            print("\n⚠️ Opção inválida! Escolha entre 0 e 6.\n")


def main():
    parser = argparse.ArgumentParser(
        prog="geo-explorer",
        description="Geo-Explorer: Plataforma de Trilhas, Desafios de Código e Certificação com IBM Bob (DIO)"
    )

    subparsers = parser.add_subparsers(dest="comando", help="Comando a ser executado")

    # Subcomando: trilha
    parser_trilha = subparsers.add_parser("trilha", help="Consulta o plano de estudos de uma tecnologia")
    parser_trilha.add_argument("-t", "--tech", "--tecnologia", required=True, help="Nome ou ID da tecnologia")
    parser_trilha.add_argument("-n", "--nivel", default=None, help="Nível (iniciante, intermediario, avancado)")

    # Subcomando: desafio
    parser_desafio = subparsers.add_parser("desafio", help="Gera um desafio de código conforme tecnologia e nível")
    parser_desafio.add_argument("-t", "--tech", "--tecnologia", required=True, help="Nome ou ID da tecnologia")
    parser_desafio.add_argument("-n", "--nivel", required=True, help="Nível (iniciante, intermediario, avancado)")

    # Subcomando: certificado
    parser_cert = subparsers.add_parser("certificado", help="Gera um certificado fictício de conclusão")
    parser_cert.add_argument("-a", "--aluno", "--nome", required=True, help="Nome completo do aluno")
    parser_cert.add_argument("-t", "--tech", "--tecnologia", required=True, help="Nome ou ID da tecnologia")
    parser_cert.add_argument("-n", "--nivel", required=True, help="Nível (iniciante, intermediario, avancado)")
    parser_cert.add_argument("-s", "--salvar", action="store_true", help="Salva os arquivos HTML/JSON em disco")
    parser_cert.add_argument("-f", "--formato", choices=["html", "json", "ambos"], default="ambos", help="Formato de salvamento")

    # Subcomando: listar
    subparsers.add_parser("listar", help="Lista todas as tecnologias e trilhas disponíveis")

    # Subcomando: mcp
    subparsers.add_parser("mcp", help="Inicia o Servidor MCP (Model Context Protocol)")

    # Subcomando: web
    parser_web = subparsers.add_parser("web", help="Inicia a interface web local do Geo-Explorer")
    parser_web.add_argument("-p", "--porta", type=int, default=8000, help="Porta para o servidor web (padrão: 8000)")

    args = parser.parse_args()

    if args.comando is None:
        menu_interativo()
        return 0

    if args.comando == "trilha":
        return executar_comando_trilha(args.tech, args.nivel)

    elif args.comando == "desafio":
        return executar_comando_desafio(args.tech, args.nivel)

    elif args.comando == "certificado":
        return executar_comando_certificado(
            nome_aluno=args.aluno,
            tecnologia=args.tech,
            nivel=args.nivel,
            salvar=args.salvar,
            formato=args.formato
        )

    elif args.comando == "listar":
        return executar_comando_listar()

    elif args.comando == "mcp":
        from app.mcp_server import iniciar_servidor_mcp
        iniciar_servidor_mcp()
        return 0

    elif args.comando == "web":
        from app.web import iniciar_servidor_web
        iniciar_servidor_web(porta=args.porta)
        return 0


if __name__ == "__main__":
    sys.exit(main())
