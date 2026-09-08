"""
Comando Trilha - Geo-Explorer
Exibe o plano de estudos de acordo com a tecnologia e nível escolhidos.
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
    obter_plano_estudos,
    TrilhaNaoEncontradaError,
    NivelInvalidoError
)


def formatar_plano_terminal(plano: dict, nivel_especifico: bool = True) -> str:
    """Formata os dados do plano de estudos para exibição amigável no terminal."""
    linhas = []
    linhas.append("=" * 65)
    linhas.append(f"  {plano['icone']} TRILHA DE APRENDIZAGEM: {plano['tecnologia_nome']}")
    linhas.append("=" * 65)
    linhas.append(f"Descrição: {plano['descricao']}\n")

    if nivel_especifico:
        detalhes = plano["detalhes"]
        linhas.append(f"📍 NÍVEL: {plano['nivel'].upper()} - {detalhes.get('titulo')}")
        linhas.append(f"⏱️  Carga Horária Estimada: {detalhes.get('carga_horaria')} horas")
        linhas.append(f"🎯 Objetivo: {detalhes.get('objetivo')}\n")
        linhas.append("📚 MÓDULOS E CONTEÚDOS:")
        for i, mod in enumerate(detalhes.get("modulos", []), 1):
            linhas.append(f"  [{i}] {mod['nome']}")
            linhas.append(f"      Resumo: {mod['descricao']}")
            for topico in mod.get("topicos", []):
                linhas.append(f"      • {topico}")
            linhas.append("")
    else:
        for nivel_nome, detalhes in plano["niveis"].items():
            linhas.append(f"📍 NÍVEL: {nivel_nome.upper()} - {detalhes.get('titulo')}")
            linhas.append(f"⏱️  Carga Horária Estimada: {detalhes.get('carga_horaria')} horas")
            linhas.append(f"🎯 Objetivo: {detalhes.get('objetivo')}")
            linhas.append("📚 Módulos:")
            for i, mod in enumerate(detalhes.get("modulos", []), 1):
                linhas.append(f"    {i}. {mod['nome']} ({len(mod.get('topicos', []))} tópicos)")
            linhas.append("-" * 65)

    return "\n".join(linhas)


def executar_comando_trilha(tecnologia: str, nivel: str | None = None) -> int:
    """Executa a lógica de consulta da trilha e exibe no terminal."""
    try:
        plano = obter_plano_estudos(tecnologia, nivel)
        texto = formatar_plano_terminal(plano, nivel_especifico=(nivel is not None))
        print(texto)
        return 0
    except (TrilhaNaoEncontradaError, NivelInvalidoError) as e:
        print(f"\n❌ Erro: {e}\n", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\n❌ Ocorreu um erro inesperado: {e}\n", file=sys.stderr)
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Consulta o plano de estudos de uma tecnologia no Geo-Explorer."
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
        default=None,
        help="Nível desejado (iniciante, intermediario, avancado). Opcional."
    )

    args = parser.parse_args()
    sys.exit(executar_comando_trilha(args.tecnologia, args.nivel))


if __name__ == "__main__":
    main()
