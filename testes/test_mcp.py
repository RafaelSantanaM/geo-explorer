"""
Testes automatizados para o Servidor MCP (Model Context Protocol).
Valida especificações JSON-RPC 2.0, inicialização, tools/list, tools/call e resources.
"""

import json
import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.mcp_server import processar_mensagem_mcp, MCP_TOOLS


class TestServidorMCP(unittest.TestCase):
    def test_initialize(self):
        req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "clientInfo": {"name": "test-client", "version": "1.0"}
            }
        }
        res = processar_mensagem_mcp(req)
        self.assertIsNotNone(res)
        self.assertEqual(res["id"], 1)
        self.assertEqual(res["jsonrpc"], "2.0")
        self.assertIn("serverInfo", res["result"])
        self.assertEqual(res["result"]["serverInfo"]["name"], "geo-explorer-mcp-server")

    def test_ping(self):
        req = {"jsonrpc": "2.0", "id": 10, "method": "ping"}
        res = processar_mensagem_mcp(req)
        self.assertEqual(res["id"], 10)
        self.assertEqual(res["result"], {})

    def test_tools_list(self):
        req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
        res = processar_mensagem_mcp(req)
        self.assertEqual(res["id"], 2)
        tools = res["result"]["tools"]
        nomes = [t["name"] for t in tools]
        self.assertIn("listar_tecnologias", nomes)
        self.assertIn("consultar_trilha", nomes)
        self.assertIn("gerar_desafio", nomes)
        self.assertIn("gerar_certificado", nomes)

    def test_tools_call_consultar_trilha(self):
        req = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "consultar_trilha",
                "arguments": {"tecnologia": "python", "nivel": "iniciante"}
            }
        }
        res = processar_mensagem_mcp(req)
        self.assertEqual(res["id"], 3)
        conteudo = res["result"]["content"][0]["text"]
        dados_plano = json.loads(conteudo)
        self.assertEqual(dados_plano["tecnologia_id"], "python")
        self.assertEqual(dados_plano["nivel"], "iniciante")

    def test_tools_call_gerar_desafio(self):
        req = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "gerar_desafio",
                "arguments": {"tecnologia": "sql", "nivel": "intermediario"}
            }
        }
        res = processar_mensagem_mcp(req)
        self.assertEqual(res["id"], 4)
        conteudo = res["result"]["content"][0]["text"]
        dados_desafio = json.loads(conteudo)
        self.assertIn("desafio", dados_desafio)
        self.assertIn("titulo", dados_desafio["desafio"])

    def test_tools_call_gerar_certificado(self):
        req = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "gerar_certificado",
                "arguments": {
                    "nome_aluno": "Rafael Santana",
                    "tecnologia": "ibm-bob",
                    "nivel": "avancado"
                }
            }
        }
        res = processar_mensagem_mcp(req)
        self.assertEqual(res["id"], 5)
        conteudo = res["result"]["content"][0]["text"]
        cert = json.loads(conteudo)
        self.assertEqual(cert["aluno"], "Rafael Santana")
        self.assertTrue(cert["codigo_autenticidade"].startswith("GEO-"))

    def test_metodo_desconhecido(self):
        req = {"jsonrpc": "2.0", "id": 99, "method": "metodo_fantasma"}
        res = processar_mensagem_mcp(req)
        self.assertEqual(res["id"], 99)
        self.assertIn("error", res)
        self.assertEqual(res["error"]["code"], -32601)

    def test_resources_list_and_read(self):
        req_list = {"jsonrpc": "2.0", "id": 6, "method": "resources/list"}
        res_list = processar_mensagem_mcp(req_list)
        self.assertGreater(len(res_list["result"]["resources"]), 0)

        uri = res_list["result"]["resources"][0]["uri"]
        req_read = {"jsonrpc": "2.0", "id": 7, "method": "resources/read", "params": {"uri": uri}}
        res_read = processar_mensagem_mcp(req_read)
        self.assertIn("contents", res_read["result"])
        texto = res_read["result"]["contents"][0]["text"]
        dados = json.loads(texto)
        self.assertIn("trilhas", dados)


if __name__ == "__main__":
    unittest.main()
