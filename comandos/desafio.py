"""
Comando Desafio - Geo-Explorer
Gera e exibe um desafio de código conforme a tecnologia e nível especificados.
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

# Ajusta path para importar o módulo app
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.gerenciador import (
    obter_desafio,
    TrilhaNaoEncontradaError,
    NivelInvalidoError
)


def formatar_desafio_terminal(info_desafio: dict) -> str:
    """Formata o desafio de código para exibição visual no terminal."""
    desafio = info_desafio["desafio"]
    linhas = []
    linhas.append("=" * 68)
    linhas.append(f"  🎯 DESAFIO DE CÓDIGO [{info_desafio['icone']} {info_desafio['tecnologia_nome']}]")
    linhas.append(f"  Nível: {info_desafio['nivel'].upper()} - {info_desafio['titulo_nivel']}")
    linhas.append("=" * 68)
    linhas.append(f"\n📌 TÍTULO: {desafio['titulo']}\n")
    linhas.append("📝 ENUNCIADO:")
    linhas.append(f"   {desafio['enunciado']}\n")

    linhas.append("📥 EXEMPLO DE ENTRADA:")
    linhas.append(f"   {desafio.get('entrada_exemplo', 'N/A')}\n")

    linhas.append("📤 EXEMPLO DE SAÍDA ESPERADA:")
    linhas.append(f"   {desafio.get('saida_exemplo', 'N/A')}\n")

    linhas.append("💻 CÓDIGO BASE / TEMPLATE:")
    linhas.append("-" * 68)
    for linha_codigo in desafio.get("template_codigo", "").splitlines():
        linhas.append(f"   {linha_codigo}")
    linhas.append("-" * 68)

    criterios = desafio.get("criterios_aceite", [])
    if criterios:
        linhas.append("\n✅ CRITÉRIOS DE ACEITAÇÃO:")
        for c in criterios:
            linhas.append(f"   • {c}")

    dicas = desafio.get("dicas", [])
    if dicas:
        linhas.append("\n💡 DICAS DO IBM BOB:")
        for d in dicas:
            linhas.append(f"   💡 {d}")

    linhas.append("\n" + "=" * 68)
    linhas.append("🚀 Dica: Após resolver o desafio, gere seu certificado oficial com:")
    linhas.append(f"   python3 app/main.py certificado --nome \"Seu Nome\" --tech {info_desafio['tecnologia_id']} --nivel {info_desafio['nivel']}")
    linhas.append("=" * 68)

    return "\n".join(linhas)


def executar_comando_desafio(tecnologia: str, nivel: str) -> int:
    """Executa a geração do desafio e imprime no terminal."""
    try:
        dados_desafio = obter_desafio(tecnologia, nivel)
        texto = formatar_desafio_terminal(dados_desafio)
        print(texto)
        return 0
    except (TrilhaNaoEncontradaError, NivelInvalidoError, ValueError) as e:
        print(f"\n❌ Erro: {e}\n", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\n❌ Ocorreu um erro inesperado: {e}\n", file=sys.stderr)
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Gera um desafio de código conforme tecnologia e nível no Geo-Explorer."
    )
    parser.add_argument(
        "-t", "--tech", "--tecnologia",
        dest="tecnologia",
        required=True,
        help="Nome ou identificador da tecnologia (ex: python, javascript, sql, geoprocessamento, ibm-bob)"
    )
    parser.add_argument(
        "-n", "--nivel",
        dest="nivel",
        required=True,
        help="Nível do desafio (iniciante, intermediario, avancado)"
    )

    args = parser.parse_args()
    sys.exit(executar_comando_desafio(args.tecnologia, args.nivel))


if __name__ == "__main__":
    main()
