"""
Testes automatizados de integridade e validação do arquivo de dados dados/trilhas.json.
"""

import json
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DADOS_PATH = BASE_DIR / "dados" / "trilhas.json"


class TestDadosTrilhas(unittest.TestCase):
    def setUp(self):
        self.assertTrue(DADOS_PATH.exists(), "O arquivo dados/trilhas.json deve existir.")
        with open(DADOS_PATH, "r", encoding="utf-8") as f:
            self.dados = json.load(f)

    def test_estrutura_raiz(self):
        """Valida que o JSON possui a estrutura básica esperada."""
        self.assertIn("versao", self.dados)
        self.assertIn("projeto", self.dados)
        self.assertIn("trilhas", self.dados)
        self.assertIsInstance(self.dados["trilhas"], list)
        self.assertGreaterEqual(len(self.dados["trilhas"]), 3, "Deve haver no mínimo 3 trilhas cadastradas.")

    def test_campos_obrigatorios_por_trilha(self):
        """Valida que todas as trilhas contêm campos essenciais."""
        campos_obrigatorios = ["id", "nome", "descricao", "niveis"]
        niveis_esperados = {"iniciante", "intermediario", "avancado"}

        ids_vistos = set()
        for trilha in self.dados["trilhas"]:
            for campo in campos_obrigatorios:
                self.assertIn(campo, trilha, f"Trilha {trilha.get('id')} deve conter o campo '{campo}'.")

            # Verifica IDs duplicados
            trilha_id = trilha["id"]
            self.assertNotIn(trilha_id, ids_vistos, f"ID duplicado detectado: {trilha_id}")
            ids_vistos.add(trilha_id)

            # Verifica se os níveis estão presentes
            niveis_trilha = set(trilha["niveis"].keys())
            self.assertTrue(
                niveis_esperados.issubset(niveis_trilha),
                f"A trilha {trilha_id} deve contemplar os níveis: {niveis_esperados}"
            )

    def test_estrutura_dos_desafios(self):
        """Valida se cada nível possui desafio de código com enunciado e template."""
        for trilha in self.dados["trilhas"]:
            for nivel_nome, nivel_dados in trilha["niveis"].items():
                self.assertIn("desafio", nivel_dados, f"Nível {nivel_nome} da trilha {trilha['id']} deve ter desafio.")
                desafio = nivel_dados["desafio"]
                self.assertIn("titulo", desafio)
                self.assertIn("enunciado", desafio)
                self.assertIn("template_codigo", desafio)
                self.assertIn("criterios_aceite", desafio)
                self.assertIsInstance(desafio["criterios_aceite"], list)
                self.assertGreater(len(desafio["criterios_aceite"]), 0)


if __name__ == "__main__":
    unittest.main()
