"""
Servidor MCP (Model Context Protocol) para o Geo-Explorer.
Permite que agentes de Inteligência Artificial (como IBM Bob, Claude, ChatGPT, etc.)
acessem as ferramentas e recursos do Geo-Explorer via protocolo JSON-RPC 2.0 sobre stdio.
"""

from __future__ import annotations
import json
import sys
from pathlib import Path
from typing import Any, Dict

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.gerenciador import (
    listar_tecnologias,
    obter_plano_estudos,
    obter_desafio,
    emitir_certificado,
    carregar_dados,
    TrilhaNaoEncontradaError,
    NivelInvalidoError
)

# Definição das Ferramentas MCP (Tools)
MCP_TOOLS = [
    {
        "name": "listar_tecnologias",
        "description": "Lista todas as tecnologias e trilhas de aprendizagem disponíveis no Geo-Explorer.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "consultar_trilha",
        "description": "Apresenta o plano de estudos detalhado de acordo com a tecnologia e nível escolhidos no Geo-Explorer.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "tecnologia": {
                    "type": "string",
                    "description": "Identificador ou nome da tecnologia (ex: 'python', 'javascript', 'sql', 'geoprocessamento', 'ibm-bob')"
                },
                "nivel": {
                    "type": "string",
                    "description": "Nível de aprendizado desejado: 'iniciante', 'intermediario' ou 'avancado'. Se omitido, retorna todos os níveis.",
                    "enum": ["iniciante", "intermediario", "avancado"]
                }
            },
            "required": ["tecnologia"]
        }
    },
    {
        "name": "gerar_desafio",
        "description": "Gera um desafio prático de código conforme a tecnologia e o nível de complexidade informados.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "tecnologia": {
                    "type": "string",
                    "description": "Tecnologia do desafio (ex: 'python', 'javascript', 'sql', 'geoprocessamento', 'ibm-bob')"
                },
                "nivel": {
                    "type": "string",
                    "description": "Nível do desafio: 'iniciante', 'intermediario' ou 'avancado'",
                    "enum": ["iniciante", "intermediario", "avancado"]
                }
            },
            "required": ["tecnologia", "nivel"]
        }
    },
    {
        "name": "gerar_certificado",
        "description": "Cria um certificado de conclusão fictício com código hash criptográfico de validação para o aluno.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "nome_aluno": {
                    "type": "string",
                    "description": "Nome completo da pessoa aluna para emissão do certificado"
                },
                "tecnologia": {
                    "type": "string",
                    "description": "Tecnologia concluída (ex: 'python', 'javascript', 'sql', 'geoprocessamento', 'ibm-bob')"
                },
                "nivel": {
                    "type": "string",
                    "description": "Nível concluído: 'iniciante', 'intermediario' ou 'avancado'",
                    "enum": ["iniciante", "intermediario", "avancado"]
                }
            },
            "required": ["nome_aluno", "tecnologia", "nivel"]
        }
    }
]


def executar_ferramenta(nome: str, argumentos: Dict[str, Any]) -> str:
    """Executa a função correspondente e devolve a resposta em string formatada."""
    try:
        if nome == "listar_tecnologias":
            techs = listar_tecnologias()
            return json.dumps(techs, indent=2, ensure_ascii=False)

        elif nome == "consultar_trilha":
            tech = argumentos.get("tecnologia", "")
            nivel = argumentos.get("nivel")
            plano = obter_plano_estudos(tech, nivel)
            return json.dumps(plano, indent=2, ensure_ascii=False)

        elif nome == "gerar_desafio":
            tech = argumentos.get("tecnologia", "")
            nivel = argumentos.get("nivel", "")
            desafio = obter_desafio(tech, nivel)
            return json.dumps(desafio, indent=2, ensure_ascii=False)

        elif nome == "gerar_certificado":
            nome_aluno = argumentos.get("nome_aluno", "")
            tech = argumentos.get("tecnologia", "")
            nivel = argumentos.get("nivel", "")
            cert = emitir_certificado(nome_aluno, tech, nivel)
            return json.dumps(cert, indent=2, ensure_ascii=False)

        else:
            raise ValueError(f"Ferramenta desconhecida: {nome}")

    except (TrilhaNaoEncontradaError, NivelInvalidoError, ValueError) as e:
        return f"Erro na operação: {e}"
    except Exception as e:
        return f"Erro inesperado ao executar '{nome}': {e}"


def processar_mensagem_mcp(mensagem: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Processa uma mensagem JSON-RPC 2.0 e retorna a resposta apropriada.
    """
    msg_id = mensagem.get("id")
    metodo = mensagem.get("method")
    params = mensagem.get("params", {})

    # Notificações que não exigem resposta (como initialized)
    if msg_id is None:
        return None

    # 1. Ciclo de Inicialização
    if metodo == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                    "resources": {}
                },
                "serverInfo": {
                    "name": "geo-explorer-mcp-server",
                    "version": "1.0.0"
                }
            }
        }

    # 2. Ping de Verificação de Conexão
    elif metodo == "ping":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {}
        }

    # 3. Listagem de Ferramentas
    elif metodo == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "tools": MCP_TOOLS
            }
        }

    # 4. Execução de Ferramentas (Tool Call)
    elif metodo == "tools/call":
        tool_name = params.get("name")
        tool_args = params.get("arguments", {})

        saida_texto = executar_ferramenta(tool_name, tool_args)

        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": saida_texto
                    }
                ]
            }
        }

    # 5. Listagem de Recursos (Resources)
    elif metodo == "resources/list":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "resources": [
                    {
                        "uri": "geo-explorer://trilhas/todas",
                        "name": "Todas as Trilhas do Geo-Explorer",
                        "mimeType": "application/json",
                        "description": "Base de dados completa em JSON contendo tecnologias, níveis, módulos e desafios."
                    }
                ]
            }
        }

    # 6. Leitura de Recursos (Resources Read)
    elif metodo == "resources/read":
        uri = params.get("uri")
        if uri == "geo-explorer://trilhas/todas":
            dados = carregar_dados()
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "contents": [
                        {
                            "uri": uri,
                            "mimeType": "application/json",
                            "text": json.dumps(dados, indent=2, ensure_ascii=False)
                        }
                    ]
                }
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {
                    "code": -32602,
                    "message": f"Recurso não encontrado para a URI: {uri}"
                }
            }

    # Método não suportado
    else:
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {
                "code": -32601,
                "message": f"Método não suportado: {metodo}"
            }
        }


def iniciar_servidor_mcp():
    """
    Loop principal do servidor MCP sobre STDIN e STDOUT.
    """
    # Garante encoding UTF-8 nas streams
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")

    # Log informativo em stderr (para não interferir com o JSON-RPC no stdout)
    sys.stderr.write("🚀 Servidor MCP Geo-Explorer iniciado e aguardando conexões via stdio...\n")
    sys.stderr.flush()

    for linha in sys.stdin:
        linha = linha.strip()
        if not linha:
            continue

        try:
            requisicao = json.loads(linha)
            resposta = processar_mensagem_mcp(requisicao)
            if resposta is not None:
                sys.stdout.write(json.dumps(resposta, ensure_ascii=False) + "\n")
                sys.stdout.flush()
        except json.JSONDecodeError:
            erro = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error: JSON inválido"}
            }
            sys.stdout.write(json.dumps(erro, ensure_ascii=False) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Erro interno no servidor MCP: {e}\n")
            sys.stderr.flush()


if __name__ == "__main__":
    iniciar_servidor_mcp()
