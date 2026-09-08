"""
Comando Listar - Geo-Explorer
Lista todas as tecnologias e trilhas disponíveis no sistema.
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

# Ajusta path para importar o módulo app
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.gerenciador import listar_tecnologias


def executar_comando_listar() -> int:
    """Exibe no terminal a listagem formatada de todas as trilhas."""
    try:
        tecnologias = listar_tecnologias()
        print("\n" + "=" * 70)
        print("  🌍 GEO-EXPLORER - TRILHAS DE APRENDIZAGEM DISPONÍVEIS")
        print("=" * 70)

        for i, t in enumerate(tecnologias, 1):
            niveis_formatados = ", ".join(t["niveis"])
            print(f"\n[{i}] {t['icone']} {t['nome']} (ID: '{t['id']}')")
            print(f"    📖 {t['descricao']}")
            print(f"    📶 Níveis disponíveis: {niveis_formatados}")

        print("\n" + "-" * 70)
        print("💡 Para explorar uma trilha, execute:")
        print("   python3 app/main.py trilha --tech <ID> --nivel <NÍVEL>")
        print("💡 Para ver o desafio prático de código, execute:")
        print("   python3 app/main.py desafio --tech <ID> --nivel <NÍVEL>")
        print("=" * 70 + "\n")
        return 0
    except Exception as e:
        print(f"\n❌ Erro ao listar trilhas: {e}\n", file=sys.stderr)
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Lista todas as tecnologias e trilhas de aprendizagem no Geo-Explorer."
    )
    parser.parse_args()
    sys.exit(executar_comando_listar())


if __name__ == "__main__":
    main()
