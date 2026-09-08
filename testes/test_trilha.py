"""
Testes unitários para o comando e gerenciador de trilhas.
"""

import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.gerenciador import (
    listar_tecnologias,
    obter_trilha,
    obter_plano_estudos,
    TrilhaNaoEncontradaError,
    NivelInvalidoError
)
from comandos.trilha import executar_comando_trilha


class TestComandoTrilha(unittest.TestCase):
    def test_listar_tecnologias(self):
        techs = listar_tecnologias()
        self.assertIsInstance(techs, list)
        self.assertGreaterEqual(len(techs), 3)
        chaves = {t["id"] for t in techs}
        self.assertIn("python", chaves)
        self.assertIn("javascript", chaves)
        self.assertIn("sql", chaves)

    def test_obter_trilha_valida(self):
        trilha = obter_trilha("python")
        self.assertEqual(trilha["id"], "python")
        self.assertIn("niveis", trilha)

    def test_obter_trilha_case_insensitive(self):
        trilha = obter_trilha("PyThOn")
        self.assertEqual(trilha["id"], "python")

    def test_obter_trilha_inexistente(self):
        with self.assertRaises(TrilhaNaoEncontradaError):
            obter_trilha("tecnologia_inexistente_xyz_123")

    def test_obter_plano_estudos_todos_niveis(self):
        plano = obter_plano_estudos("sql")
        self.assertEqual(plano["tecnologia_id"], "sql")
        self.assertIn("niveis", plano)
        self.assertIn("iniciante", plano["niveis"])

    def test_obter_plano_estudos_nivel_especifico(self):
        plano = obter_plano_estudos("sql", "iniciante")
        self.assertEqual(plano["tecnologia_id"], "sql")
        self.assertEqual(plano["nivel"], "iniciante")
        self.assertIn("detalhes", plano)
        self.assertIn("modulos", plano["detalhes"])

    def test_obter_plano_estudos_nivel_invalido(self):
        with self.assertRaises(NivelInvalidoError):
            obter_plano_estudos("python", "nivel_impossivel")

    def test_executar_comando_retorno(self):
        # Deve retornar código de saída 0 para sucesso e 1 para erro
        self.assertEqual(executar_comando_trilha("python", "iniciante"), 0)
        self.assertEqual(executar_comando_trilha("nao_existe"), 1)


if __name__ == "__main__":
    unittest.main()
