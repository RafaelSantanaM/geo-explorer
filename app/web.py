"""
Interface Web Interativa do Geo-Explorer.
Implementada com a biblioteca padrão http.server do Python (sem necessidade de instalar Flask ou frameworks externos).
Permite explorar trilhas, desafios e emitir certificados diretamente no navegador!
"""

from __future__ import annotations
import http.server
import json
import socketserver
import sys
import urllib.parse
import webbrowser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.gerenciador import (
    listar_tecnologias,
    obter_plano_estudos,
    obter_desafio,
    emitir_certificado,
    salvar_certificado_html,
    carregar_dados
)

HTML_PAGE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Geo-Explorer | Trilhas & Desafios com IBM Bob</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-dark: #090d16;
      --bg-card: #131b2e;
      --bg-hover: #1c2742;
      --primary: #38bdf8;
      --primary-accent: #0284c7;
      --secondary: #818cf8;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --border: #1e293b;
      --success: #34d399;
      --radius: 12px;
    }
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      font-family: 'Inter', sans-serif;
      background: var(--bg-dark);
      color: var(--text-main);
      line-height: 1.6;
      padding: 0;
    }
    header {
      background: rgba(19, 27, 46, 0.8);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border);
      padding: 20px 40px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 100;
    }
    .logo {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 22px;
      font-weight: 800;
      color: var(--primary);
    }
    .logo span {
      color: #ffffff;
    }
    .badge-bob {
      background: linear-gradient(135deg, #0284c7, #6366f1);
      color: #fff;
      font-size: 12px;
      padding: 4px 12px;
      border-radius: 9999px;
      font-weight: 600;
      letter-spacing: 0.5px;
    }
    .container {
      max-width: 1200px;
      margin: 40px auto;
      padding: 0 20px;
    }
    .hero {
      text-align: center;
      margin-bottom: 40px;
    }
    .hero h1 {
      font-size: 40px;
      font-weight: 800;
      margin-bottom: 12px;
      background: linear-gradient(90deg, #38bdf8, #818cf8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .hero p {
      font-size: 18px;
      color: var(--text-muted);
      max-width: 700px;
      margin: 0 auto;
    }
    .nav-tabs {
      display: flex;
      justify-content: center;
      gap: 12px;
      margin-bottom: 30px;
    }
    .tab-btn {
      background: var(--bg-card);
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 10px 24px;
      border-radius: 9999px;
      font-weight: 600;
      font-size: 15px;
      cursor: pointer;
      transition: all 0.2s;
    }
    .tab-btn:hover, .tab-btn.active {
      background: var(--primary-accent);
      color: #ffffff;
      border-color: var(--primary);
      box-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
    }
    .view-panel {
      display: none;
    }
    .view-panel.active {
      display: block;
    }
    .grid-cards {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
      gap: 20px;
    }
    .card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 24px;
      transition: all 0.2s;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .card:hover {
      border-color: var(--primary);
      transform: translateY(-3px);
      box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
    .card-icon {
      font-size: 32px;
      margin-bottom: 12px;
    }
    .card-title {
      font-size: 20px;
      font-weight: 700;
      margin-bottom: 8px;
      color: #ffffff;
    }
    .card-desc {
      font-size: 14px;
      color: var(--text-muted);
      margin-bottom: 20px;
      flex-grow: 1;
    }
    .level-tags {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }
    .tag {
      background: rgba(56, 189, 248, 0.1);
      color: var(--primary);
      border: 1px solid rgba(56, 189, 248, 0.2);
      font-size: 11px;
      padding: 3px 8px;
      border-radius: 6px;
      text-transform: capitalize;
    }
    .modal-backdrop {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.7);
      backdrop-filter: blur(5px);
      z-index: 200;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    .modal-backdrop.active {
      display: flex;
    }
    .modal-content {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      width: 100%;
      max-width: 800px;
      max-height: 85vh;
      overflow-y: auto;
      padding: 30px;
      position: relative;
    }
    .modal-close {
      position: absolute;
      top: 20px;
      right: 20px;
      background: none;
      border: none;
      color: var(--text-muted);
      font-size: 24px;
      cursor: pointer;
    }
    .form-group {
      margin-bottom: 18px;
    }
    .form-group label {
      display: block;
      margin-bottom: 6px;
      font-size: 14px;
      font-weight: 600;
      color: var(--text-main);
    }
    .form-control {
      width: 100%;
      background: #0b111e;
      border: 1px solid var(--border);
      color: #ffffff;
      padding: 12px 16px;
      border-radius: 8px;
      font-size: 15px;
      font-family: inherit;
    }
    .form-control:focus {
      outline: none;
      border-color: var(--primary);
    }
    .btn-submit {
      background: linear-gradient(135deg, #0284c7, #38bdf8);
      color: #04101e;
      border: none;
      padding: 12px 28px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 16px;
      cursor: pointer;
      width: 100%;
      transition: opacity 0.2s;
    }
    .btn-submit:hover {
      opacity: 0.9;
    }
    pre {
      background: #090d16;
      border: 1px solid var(--border);
      padding: 16px;
      border-radius: 8px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      overflow-x: auto;
      margin: 12px 0;
      color: #7dd3fc;
    }
    .cert-result {
      margin-top: 20px;
      padding: 20px;
      background: #0f172a;
      border: 1px solid var(--border);
      border-radius: 8px;
    }
  </style>
</head>
<body>

  <header>
    <div class="logo">
      🌍 <span>Geo-Explorer</span>
    </div>
    <div class="badge-bob">IBM Bob + DIO Project</div>
  </header>

  <div class="container">
    <div class="hero">
      <h1>Explorador de Trilhas & Desafios</h1>
      <p>Desenvolva habilidades, enfrente desafios práticos de código e emita certificados com suporte de agentes de Inteligência Artificial.</p>
    </div>

    <div class="nav-tabs">
      <button class="tab-btn active" onclick="mostrarAba('trilhas')">📚 Trilhas de Estudos</button>
      <button class="tab-btn" onclick="mostrarAba('desafio')">🎯 Desafio de Código</button>
      <button class="tab-btn" onclick="mostrarAba('certificado')">📜 Emitir Certificado</button>
    </div>

    <!-- ABA 1: TRILHAS -->
    <div id="aba-trilhas" class="view-panel active">
      <div id="cards-container" class="grid-cards">
        <p style="color: var(--text-muted);">Carregando trilhas...</p>
      </div>
    </div>

    <!-- ABA 2: DESAFIOS -->
    <div id="aba-desafio" class="view-panel">
      <div style="max-width: 600px; margin: 0 auto; background: var(--bg-card); padding: 30px; border-radius: var(--radius); border: 1px solid var(--border);">
        <h2 style="margin-bottom: 20px; color: var(--primary);">Buscar Desafio de Código</h2>
        <div class="form-group">
          <label>Tecnologia:</label>
          <select id="desafio-tech" class="form-control"></select>
        </div>
        <div class="form-group">
          <label>Nível:</label>
          <select id="desafio-nivel" class="form-control">
            <option value="iniciante">Iniciante</option>
            <option value="intermediario">Intermediário</option>
            <option value="avancado">Avançado</option>
          </select>
        </div>
        <button class="btn-submit" onclick="carregarDesafio()">Visualizar Desafio</button>
      </div>
      <div id="resultado-desafio" style="margin-top: 30px; display: none;"></div>
    </div>

    <!-- ABA 3: CERTIFICADO -->
    <div id="aba-certificado" class="view-panel">
      <div style="max-width: 600px; margin: 0 auto; background: var(--bg-card); padding: 30px; border-radius: var(--radius); border: 1px solid var(--border);">
        <h2 style="margin-bottom: 20px; color: var(--primary);">Gerar Certificado Oficial Fictício</h2>
        <div class="form-group">
          <label>Nome Completo do Aluno:</label>
          <input type="text" id="cert-nome" class="form-control" placeholder="Ex: Rafael Santana" required>
        </div>
        <div class="form-group">
          <label>Tecnologia Concluída:</label>
          <select id="cert-tech" class="form-control"></select>
        </div>
        <div class="form-group">
          <label>Nível:</label>
          <select id="cert-nivel" class="form-control">
            <option value="iniciante">Iniciante</option>
            <option value="intermediario">Intermediário</option>
            <option value="avancado">Avançado</option>
          </select>
        </div>
        <button class="btn-submit" onclick="emitirCertificado()">Gerar & Emitir Certificado</button>
      </div>
      <div id="resultado-cert" style="margin-top: 30px; display: none;"></div>
    </div>
  </div>

  <!-- Modal Detalhe da Trilha -->
  <div id="modal-trilha" class="modal-backdrop">
    <div class="modal-content">
      <button class="modal-close" onclick="fecharModal()">&times;</button>
      <div id="modal-corpo"></div>
    </div>
  </div>

  <script>
    let tecnologiasCache = [];

    async function init() {
      const resp = await fetch('/api/trilhas');
      tecnologiasCache = await resp.json();
      renderizarCards(tecnologiasCache);
      popularSelects(tecnologiasCache);
    }

    function popularSelects(techs) {
      const s1 = document.getElementById('desafio-tech');
      const s2 = document.getElementById('cert-tech');
      s1.innerHTML = '';
      s2.innerHTML = '';
      techs.forEach(t => {
        s1.innerHTML += `<option value="${t.id}">${t.icone} ${t.nome}</option>`;
        s2.innerHTML += `<option value="${t.id}">${t.icone} ${t.nome}</option>`;
      });
    }

    function renderizarCards(techs) {
      const container = document.getElementById('cards-container');
      container.innerHTML = '';
      techs.forEach(t => {
        const card = document.createElement('div');
        card.className = 'card';
        card.onclick = () => abrirDetalhesTrilha(t.id);
        card.innerHTML = `
          <div>
            <div class="card-icon">${t.icone}</div>
            <div class="card-title">${t.nome}</div>
            <div class="card-desc">${t.descricao}</div>
          </div>
          <div class="level-tags">
            ${t.niveis.map(n => `<span class="tag">${n}</span>`).join('')}
          </div>
        `;
        container.appendChild(card);
      });
    }

    function mostrarAba(aba) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.view-panel').forEach(p => p.classList.remove('active'));
      event.target.classList.add('active');
      document.getElementById('aba-' + aba).classList.add('active');
    }

    async function abrirDetalhesTrilha(techId) {
      const resp = await fetch('/api/plano?tech=' + techId);
      const data = await resp.json();
      const corpo = document.getElementById('modal-corpo');

      let htmlNiveis = '';
      for (const [niv, det] of Object.entries(data.niveis)) {
        htmlNiveis += `
          <div style="background:#0b111e; padding:18px; border-radius:8px; margin-top:16px; border:1px solid var(--border)">
            <h3 style="color:var(--primary); text-transform:uppercase; font-size:16px;">📍 Nível ${niv} - ${det.titulo}</h3>
            <p style="color:var(--text-muted); font-size:13px; margin:4px 0 10px 0;">⏱️ ${det.carga_horaria} horas | 🎯 ${det.objetivo}</p>
            <h4 style="font-size:14px; margin-top:10px;">Módulos:</h4>
            <ul style="padding-left:20px; font-size:13px; color:#cbd5e1;">
              ${det.modulos.map(m => `<li><strong>${m.nome}</strong>: ${m.topicos.join(', ')}</li>`).join('')}
            </ul>
          </div>
        `;
      }

      corpo.innerHTML = `
        <h2 style="font-size:24px; color:#fff; margin-bottom:8px;">${data.icone} ${data.tecnologia_nome}</h2>
        <p style="color:var(--text-muted); margin-bottom:15px;">${data.descricao}</p>
        ${htmlNiveis}
      `;
      document.getElementById('modal-trilha').classList.add('active');
    }

    function fecharModal() {
      document.getElementById('modal-trilha').classList.remove('active');
    }

    async function carregarDesafio() {
      const tech = document.getElementById('desafio-tech').value;
      const nivel = document.getElementById('desafio-nivel').value;
      const resp = await fetch(`/api/desafio?tech=${tech}&nivel=${nivel}`);
      const data = await resp.json();
      const resDiv = document.getElementById('resultado-desafio');
      resDiv.style.display = 'block';

      const d = data.desafio;
      resDiv.innerHTML = `
        <div style="background:var(--bg-card); border:1px solid var(--border); padding:30px; border-radius:var(--radius);">
          <h2 style="color:var(--primary);">${data.icone} ${d.titulo}</h2>
          <p style="color:var(--text-muted); font-size:14px; margin-bottom:15px;">Nível: ${data.nivel.toUpperCase()} (${data.titulo_nivel})</p>
          <p style="margin-bottom:15px;"><strong>Enunciado:</strong> ${d.enunciado}</p>
          <p style="font-size:13px; color:var(--text-muted);"><strong>Entrada:</strong> <code>${d.entrada_exemplo}</code></p>
          <p style="font-size:13px; color:var(--text-muted); margin-bottom:15px;"><strong>Saída esperada:</strong> <code>${d.saida_exemplo}</code></p>
          <h4>Template de Código:</h4>
          <pre><code>${d.template_codigo}</code></pre>
          <h4>Critérios de Aceite:</h4>
          <ul style="padding-left:20px; font-size:14px; color:#cbd5e1; margin-bottom:15px;">
            ${d.criterios_aceite.map(c => `<li>${c}</li>`).join('')}
          </ul>
          <h4>💡 Dica do Bob:</h4>
          <p style="font-size:13px; color:#38bdf8;">${d.dicas.join(' | ')}</p>
        </div>
      `;
    }

    async function emitirCertificado() {
      const nome = document.getElementById('cert-nome').value.trim();
      const tech = document.getElementById('cert-tech').value;
      const nivel = document.getElementById('cert-nivel').value;

      if (!nome) {
        alert('Por favor, informe seu nome!');
        return;
      }

      const resp = await fetch('/api/certificado', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome_aluno: nome, tecnologia: tech, nivel: nivel })
      });
      const data = await resp.json();
      const resDiv = document.getElementById('resultado-cert');
      resDiv.style.display = 'block';

      resDiv.innerHTML = `
        <div style="background:var(--bg-card); border:2px solid var(--primary); padding:30px; border-radius:var(--radius); text-align:center;">
          <h2 style="color:var(--success); margin-bottom:10px;">🎉 Certificado Emitido com Sucesso!</h2>
          <p style="font-size:16px;">Parabéns, <strong>${data.aluno}</strong>!</p>
          <p style="color:var(--text-muted); margin:10px 0;">Trilha: <strong>${data.tecnologia_nome} (${data.nivel})</strong></p>
          <div style="margin:20px 0; background:#0b111e; padding:15px; border-radius:8px; font-family:monospace; color:var(--primary); font-size:16px;">
            Código Autenticador: ${data.codigo_autenticidade}
          </div>
          <p style="font-size:13px; color:var(--text-muted); margin-bottom:20px;">Carga Horária: ${data.carga_horaria}h | Emitido em: ${data.data_emissao}</p>
          <button class="tab-btn active" onclick="window.open('/certificados/' + encodeURIComponent('${data.arquivo_html}'), '_blank')">
            📄 Abrir Certificado Oficial para Impressão / PDF
          </button>
        </div>
      `;
    }

    window.onload = init;
  </script>
</body>
</html>
"""


class GeoExplorerHandler(http.server.BaseHTTPRequestHandler):
    def _enviar_json(self, status: int, dados: any):
        resposta = json.dumps(dados, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(resposta)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(resposta)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        caminho = parsed.path
        params = urllib.parse.parse_qs(parsed.query)

        if caminho in ("/", "/index.html"):
            conteudo = HTML_PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(conteudo)))
            self.end_headers()
            self.wfile.write(conteudo)

        elif caminho == "/api/trilhas":
            techs = listar_tecnologias()
            self._enviar_json(200, techs)

        elif caminho == "/api/plano":
            tech = params.get("tech", [""])[0]
            nivel = params.get("nivel", [None])[0]
            try:
                plano = obter_plano_estudos(tech, nivel)
                self._enviar_json(200, plano)
            except Exception as e:
                self._enviar_json(404, {"erro": str(e)})

        elif caminho == "/api/desafio":
            tech = params.get("tech", [""])[0]
            nivel = params.get("nivel", ["iniciante"])[0]
            try:
                desafio = obter_desafio(tech, nivel)
                self._enviar_json(200, desafio)
            except Exception as e:
                self._enviar_json(404, {"erro": str(e)})

        elif caminho.startswith("/certificados/"):
            nome_arquivo = caminho.replace("/certificados/", "")
            caminho_real = BASE_DIR / "certificados_emitidos" / nome_arquivo
            if caminho_real.exists() and caminho_real.suffix in (".html", ".json"):
                with open(caminho_real, "rb") as f:
                    conteudo = f.read()
                self.send_response(200)
                tipo = "text/html; charset=utf-8" if caminho_real.suffix == ".html" else "application/json"
                self.send_header("Content-Type", tipo)
                self.send_header("Content-Length", str(len(conteudo)))
                self.end_headers()
                self.wfile.write(conteudo)
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Certificado nao encontrado")

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Rota nao encontrada")

    def do_POST(self):
        if self.path == "/api/certificado":
            tamanho = int(self.headers.get("Content-Length", 0))
            corpo = self.rfile.read(tamanho)
            dados = json.loads(corpo.decode("utf-8"))

            nome = dados.get("nome_aluno", "")
            tech = dados.get("tecnologia", "")
            nivel = dados.get("nivel", "iniciante")

            try:
                cert = emitir_certificado(nome, tech, nivel)
                arq_html = salvar_certificado_html(cert)
                cert["arquivo_html"] = arq_html.name
                self._enviar_json(201, cert)
            except Exception as e:
                self._enviar_json(400, {"erro": str(e)})
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Silencia logs automáticos para deixar o terminal limpo
        pass


def iniciar_servidor_web(porta: int = 8000, abrir_navegador: bool = True):
    """Inicia o servidor HTTP local na porta especificada."""
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", porta), GeoExplorerHandler) as httpd:
        url = f"http://localhost:{porta}"
        print(f"\n🌐 Servidor Web do Geo-Explorer rodando em: {url}")
        print("💡 Pressione Ctrl+C para encerrar o servidor.\n")
        if abrir_navegador:
            try:
                webbrowser.open(url)
            except Exception:
                pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Servidor web finalizado com sucesso.")


if __name__ == "__main__":
    iniciar_servidor_web()
