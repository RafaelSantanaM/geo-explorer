"""
Testes unitários para a emissão e gravação de certificados.
"""

import sys
import tempfile
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.gerenciador import (
    emitir_certificado,
    gerar_hash_certificado,
    salvar_certificado_html,
    salvar_certificado_json
)
from comandos.certificado import executar_comando_certificado


class TestComandoCertificado(unittest.TestCase):
    def test_emitir_certificado_sucesso(self):
        cert = emitir_certificado("Rafael Santana", "python", "iniciante")
        self.assertEqual(cert["aluno"], "Rafael Santana")
        self.assertEqual(cert["tecnologia_id"], "python")
        self.assertEqual(cert["nivel"], "Iniciante")
        self.assertTrue(cert["codigo_autenticidade"].startswith("GEO-"))
        self.assertEqual(len(cert["codigo_autenticidade"]), 20)  # GEO- + 16 chars
        self.assertGreater(cert["carga_horaria"], 0)
        self.assertGreater(len(cert["modulos_concluidos"]), 0)

    def test_emitir_certificado_nome_vazio(self):
        with self.assertRaises(ValueError):
            emitir_certificado("", "python", "iniciante")
        with self.assertRaises(ValueError):
            emitir_certificado("   ", "python", "iniciante")

    def test_determinismo_hash_certificado(self):
        h1 = gerar_hash_certificado("Alice", "sql", "iniciante", "2026-09-08 12:00:00")
        h2 = gerar_hash_certificado("Alice", "sql", "iniciante", "2026-09-08 12:00:00")
        h3 = gerar_hash_certificado("Bob", "sql", "iniciante", "2026-09-08 12:00:00")
        self.assertEqual(h1, h2, "O hash deve ser reproduzível para os mesmos parâmetros.")
        self.assertNotEqual(h1, h3, "Alunos diferentes devem gerar hashes distintos.")

    def test_salvar_certificado_html_e_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            cert = emitir_certificado("Rafael Santana", "geoprocessamento", "avancado")

            # Salva HTML
            caminho_html = salvar_certificado_html(cert, tmp_path)
            self.assertTrue(caminho_html.exists())
            self.assertEqual(caminho_html.suffix, ".html")
            with open(caminho_html, "r", encoding="utf-8") as f:
                html_txt = f.read()
                self.assertIn("Rafael Santana", html_txt)
                self.assertIn(cert["codigo_autenticidade"], html_txt)

            # Salva JSON
            caminho_json = salvar_certificado_json(cert, tmp_path)
            self.assertTrue(caminho_json.exists())
            self.assertEqual(caminho_json.suffix, ".json")
            with open(caminho_json, "r", encoding="utf-8") as f:
                json_txt = f.read()
                self.assertIn(cert["codigo_autenticidade"], json_txt)

    def test_executar_comando_cli(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            retorno = executar_comando_certificado(
                nome_aluno="Rafael Santana",
                tecnologia="python",
                nivel="iniciante",
                salvar=True,
                formato="ambos",
                diretorio=tmp_path
            )
            self.assertEqual(retorno, 0)


if __name__ == "__main__":
    unittest.main()
