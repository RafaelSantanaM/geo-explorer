"""
Testes unitários para o comando e gerenciador de desafios de código.
"""

import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.gerenciador import (
    obter_desafio,
    TrilhaNaoEncontradaError,
    NivelInvalidoError
)
from comandos.desafio import executar_comando_desafio


class TestComandoDesafio(unittest.TestCase):
    def test_obter_desafio_python_iniciante(self):
        dados = obter_desafio("python", "iniciante")
        self.assertEqual(dados["tecnologia_id"], "python")
        self.assertEqual(dados["nivel"], "iniciante")
        self.assertIn("desafio", dados)

        desafio = dados["desafio"]
        self.assertTrue(len(desafio["titulo"]) > 0)
        self.assertTrue(len(desafio["enunciado"]) > 0)
        self.assertIn("template_codigo", desafio)

    def test_obter_desafio_geoprocessamento(self):
        dados = obter_desafio("geoprocessamento", "intermediario")
        self.assertEqual(dados["tecnologia_id"], "geoprocessamento")
        self.assertEqual(dados["nivel"], "intermediario")
        self.assertIn("GeoJSON", dados["desafio"]["titulo"])

    def test_obter_desafio_ibm_bob(self):
        dados = obter_desafio("ibm-bob", "avancado")
        self.assertEqual(dados["tecnologia_id"], "ibm-bob")
        self.assertIn("MCP", dados["desafio"]["titulo"])

    def test_obter_desafio_tecnologia_invalida(self):
        with self.assertRaises(TrilhaNaoEncontradaError):
            obter_desafio("rust_inexistente", "iniciante")

    def test_obter_desafio_nivel_invalido(self):
        with self.assertRaises(NivelInvalidoError):
            obter_desafio("python", "ninja_expert")

    def test_execucao_comando_cli(self):
        self.assertEqual(executar_comando_desafio("sql", "iniciante"), 0)
        self.assertEqual(executar_comando_desafio("nao_existe", "iniciante"), 1)


if __name__ == "__main__":
    unittest.main()
