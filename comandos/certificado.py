"""
Comando Certificado - Geo-Explorer
Cria e emite um certificado fictício para uma trilha e nível concluídos.
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
    emitir_certificado,
    salvar_certificado_html,
    salvar_certificado_json,
    TrilhaNaoEncontradaError,
    NivelInvalidoError
)


def formatar_certificado_terminal(cert: dict) -> str:
    """Formata o certificado em uma moldura visual elegante para o terminal."""
    largura = 70
    linha_div = "╔" + "═" * (largura - 2) + "╗"
    linha_fim = "╚" + "═" * (largura - 2) + "╝"
    linha_sep = "╟" + "─" * (largura - 2) + "╢"

    def centralizar(texto: str) -> str:
        tamanho_visivel = len(texto)
        # Ajuste simples se contiver emojis de 2 bytes de exibição
        espacos = max(0, largura - 4 - tamanho_visivel)
        esq = espacos // 2
        dir_ = espacos - esq
        return f"║ {' ' * esq}{texto}{' ' * dir_} ║"

    def alinhar_esq(texto: str) -> str:
        espacos = max(0, largura - 4 - len(texto))
        return f"║ {texto}{' ' * espacos} ║"

    linhas = []
    linhas.append(linha_div)
    linhas.append(centralizar("🌍 PROJETO GEO-EXPLORER 🌍"))
    linhas.append(centralizar("CERTIFICADO OFICIAL FICTÍCIO DE CONCLUSÃO"))
    linhas.append(linha_sep)
    linhas.append(centralizar(""))
    linhas.append(centralizar("Certificamos com distinção que"))
    linhas.append(centralizar(f">>> {cert['aluno'].upper()} <<<"))
    linhas.append(centralizar(""))
    linhas.append(centralizar(f"concluiu com êxito a trilha de aprendizagem"))
    linhas.append(centralizar(f"{cert['icone']} {cert['tecnologia_nome']} - Nível {cert['nivel']}"))
    linhas.append(centralizar(f"({cert['titulo_trilha']})"))
    linhas.append(centralizar(""))
    linhas.append(centralizar(f"Carga Horária Estimada: {cert['carga_horaria']} Horas"))
    linhas.append(centralizar(f"Desafio Superado: {cert['desafio_concluido']}"))
    linhas.append(centralizar(""))
    linhas.append(linha_sep)
    linhas.append(alinhar_esq(f" 🔑 Código Autenticador: {cert['codigo_autenticidade']}"))
    linhas.append(alinhar_esq(f" 📅 Data de Emissão:     {cert['data_emissao']}"))
    linhas.append(alinhar_esq(f" 🏛️  Instituição:         {cert['instituicao']}"))
    linhas.append(linha_fim)

    return "\n".join(linhas)


def executar_comando_certificado(
    nome_aluno: str,
    tecnologia: str,
    nivel: str,
    salvar: bool = False,
    formato: str = "ambos",
    diretorio: Path | None = None
) -> int:
    """Executa a emissão e eventual salvamento do certificado."""
    try:
        cert = emitir_certificado(nome_aluno, tecnologia, nivel)
        texto = formatar_certificado_terminal(cert)
        print("\n" + texto + "\n")

        if salvar:
            arquivos_gerados = []
            if formato in ("html", "ambos"):
                arq_html = salvar_certificado_html(cert, diretorio)
                arquivos_gerados.append(f"📄 HTML: {arq_html}")
            if formato in ("json", "ambos"):
                arq_json = salvar_certificado_json(cert, diretorio)
                arquivos_gerados.append(f"📦 JSON: {arq_json}")

            print("💾 Certificado salvo com sucesso:")
            for arq in arquivos_gerados:
                print(f"   {arq}")
            print("💡 Dica: Você pode abrir o arquivo HTML em qualquer navegador para visualizá-lo ou imprimi-lo em PDF!\n")

        return 0
    except (TrilhaNaoEncontradaError, NivelInvalidoError, ValueError) as e:
        print(f"\n❌ Erro na emissão do certificado: {e}\n", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\n❌ Ocorreu um erro inesperado: {e}\n", file=sys.stderr)
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Gera e emite um certificado fictício no Geo-Explorer."
    )
    parser.add_argument(
        "-a", "--aluno", "--nome",
        dest="nome",
        required=True,
        help="Nome completo da pessoa aluna para constar no certificado"
    )
    parser.add_argument(
        "-t", "--tech", "--tecnologia",
        dest="tecnologia",
        required=True,
        help="Nome ou identificador da tecnologia"
    )
    parser.add_argument(
        "-n", "--nivel",
        dest="nivel",
        required=True,
        help="Nível da trilha concluída (iniciante, intermediario, avancado)"
    )
    parser.add_argument(
        "-s", "--salvar",
        dest="salvar",
        action="store_true",
        help="Salva os arquivos do certificado gerado (HTML / JSON) em disco"
    )
    parser.add_argument(
        "-f", "--formato",
        dest="formato",
        choices=["html", "json", "ambos"],
        default="ambos",
        help="Formato do arquivo ao salvar (padrão: ambos)"
    )

    args = parser.parse_args()
    sys.exit(
        executar_comando_certificado(
            nome_aluno=args.nome,
            tecnologia=args.tecnologia,
            nivel=args.nivel,
            salvar=args.salvar,
            formato=args.formato
        )
    )


if __name__ == "__main__":
    main()
