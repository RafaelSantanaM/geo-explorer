"""
Módulo de Gerenciamento de Trilhas, Desafios e Certificados do Geo-Explorer.
Responsável por carregar dados, processar consultas e emitir certificados fictícios.
"""

from __future__ import annotations
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
DADOS_PATH = BASE_DIR / "dados" / "trilhas.json"
CERTIFICADOS_DIR = BASE_DIR / "certificados_emitidos"


class TrilhaNaoEncontradaError(Exception):
    """Exceção levantada quando uma tecnologia ou trilha solicitada não existe."""
    pass


class NivelInvalidoError(Exception):
    """Exceção levantada quando o nível informado não pertence à trilha."""
    pass


def carregar_dados() -> Dict[str, Any]:
    """
    Carrega os dados das trilhas a partir do arquivo JSON.

    Retorna:
        Dicionário com os dados carregados de dados/trilhas.json.

    Lança:
        FileNotFoundError: caso o arquivo de dados não exista.
        json.JSONDecodeError: caso o arquivo contenha JSON inválido.
    """
    if not DADOS_PATH.exists():
        raise FileNotFoundError(f"Arquivo de dados não encontrado em: {DADOS_PATH}")

    with open(DADOS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def normalizar_chave(texto: str) -> str:
    """Normaliza texto para busca insensível a maiúsculas e espaços extras."""
    return texto.strip().lower()


def listar_tecnologias() -> List[Dict[str, Any]]:
    """
    Retorna uma lista resumida de todas as tecnologias disponíveis.
    """
    dados = carregar_dados()
    resultado = []
    for trilha in dados.get("trilhas", []):
        niveis_disponiveis = list(trilha.get("niveis", {}).keys())
        resultado.append({
            "id": trilha.get("id"),
            "nome": trilha.get("nome"),
            "descricao": trilha.get("descricao"),
            "icone": trilha.get("icone", "📌"),
            "niveis": niveis_disponiveis
        })
    return resultado


def obter_trilha(tecnologia: str) -> Dict[str, Any]:
    """
    Busca uma trilha pelo ID ou nome da tecnologia.
    """
    dados = carregar_dados()
    tech_normalizada = normalizar_chave(tecnologia)

    for trilha in dados.get("trilhas", []):
        if (normalizar_chave(trilha.get("id", "")) == tech_normalizada or
                normalizar_chave(trilha.get("nome", "")) == tech_normalizada):
            return trilha

    # Tentativa de correspondência parcial
    for trilha in dados.get("trilhas", []):
        if (tech_normalizada in normalizar_chave(trilha.get("id", "")) or
                tech_normalizada in normalizar_chave(trilha.get("nome", ""))):
            return trilha

    tecnologias_disponiveis = [t["id"] for t in dados.get("trilhas", [])]
    raise TrilhaNaoEncontradaError(
        f"Tecnologia '{tecnologia}' não encontrada. "
        f"Tecnologias disponíveis: {', '.join(tecnologias_disponiveis)}"
    )


def obter_plano_estudos(tecnologia: str, nivel: Optional[str] = None) -> Dict[str, Any]:
    """
    Obtém o plano de estudos para uma tecnologia.
    Se o nível for especificado, retorna apenas aquele nível.
    Caso contrário, retorna todos os níveis da tecnologia.
    """
    trilha = obter_trilha(tecnologia)
    niveis = trilha.get("niveis", {})

    if nivel:
        nivel_norm = normalizar_chave(nivel)
        if nivel_norm not in niveis:
            raise NivelInvalidoError(
                f"Nível '{nivel}' inválido para {trilha['nome']}. "
                f"Níveis disponíveis: {', '.join(niveis.keys())}"
            )
        return {
            "tecnologia_id": trilha["id"],
            "tecnologia_nome": trilha["nome"],
            "icone": trilha.get("icone", "📌"),
            "descricao": trilha.get("descricao"),
            "nivel": nivel_norm,
            "detalhes": niveis[nivel_norm]
        }

    return {
        "tecnologia_id": trilha["id"],
        "tecnologia_nome": trilha["nome"],
        "icone": trilha.get("icone", "📌"),
        "descricao": trilha.get("descricao"),
        "niveis": niveis
    }


def obter_desafio(tecnologia: str, nivel: str) -> Dict[str, Any]:
    """
    Obtém o desafio de código para uma tecnologia e nível especificados.
    """
    plano = obter_plano_estudos(tecnologia, nivel)
    detalhes = plano["detalhes"]
    desafio = detalhes.get("desafio")

    if not desafio:
        raise ValueError(f"Nenhum desafio cadastrado para {plano['tecnologia_nome']} ({nivel}).")

    return {
        "tecnologia_id": plano["tecnologia_id"],
        "tecnologia_nome": plano["tecnologia_nome"],
        "icone": plano["icone"],
        "nivel": plano["nivel"],
        "titulo_nivel": detalhes.get("titulo"),
        "desafio": desafio
    }


def gerar_hash_certificado(nome_aluno: str, tecnologia_id: str, nivel: str, data_emissao_iso: str) -> str:
    """
    Gera um hash SHA-256 fictício para autenticidade do certificado.
    """
    salt = "GEO_EXPLORER_DIO_IBM_BOB_2026"
    conteudo = f"{nome_aluno.strip().upper()}|{tecnologia_id}|{nivel}|{data_emissao_iso}|{salt}"
    return hashlib.sha256(conteudo.encode("utf-8")).hexdigest()[:16].upper()


def emitir_certificado(nome_aluno: str, tecnologia: str, nivel: str) -> Dict[str, Any]:
    """
    Cria um certificado fictício estruturado para uma trilha concluída.
    """
    if not nome_aluno or not nome_aluno.strip():
        raise ValueError("O nome do aluno é obrigatório para emitir o certificado.")

    plano = obter_plano_estudos(tecnologia, nivel)
    detalhes = plano["detalhes"]
    agora = datetime.now()
    data_iso = agora.strftime("%Y-%m-%d %H:%M:%S")
    data_formatada = agora.strftime("%d/%m/%Y")

    codigo_autenticidade = gerar_hash_certificado(
        nome_aluno=nome_aluno,
        tecnologia_id=plano["tecnologia_id"],
        nivel=plano["nivel"],
        data_emissao_iso=data_iso
    )

    certificado = {
        "projeto": "Geo-Explorer",
        "instituicao": "DIO & IBM Bob Academy",
        "codigo_autenticidade": f"GEO-{codigo_autenticidade}",
        "aluno": nome_aluno.strip(),
        "tecnologia_id": plano["tecnologia_id"],
        "tecnologia_nome": plano["tecnologia_nome"],
        "icone": plano["icone"],
        "nivel": plano["nivel"].capitalize(),
        "titulo_trilha": detalhes.get("titulo"),
        "carga_horaria": detalhes.get("carga_horaria", 20),
        "data_emissao": data_formatada,
        "data_emissao_iso": data_iso,
        "objetivo_atingido": detalhes.get("objetivo"),
        "modulos_concluidos": [m["nome"] for m in detalhes.get("modulos", [])],
        "desafio_concluido": detalhes.get("desafio", {}).get("titulo", "Desafio Prático Integrador")
    }

    return certificado


def salvar_certificado_html(certificado: Dict[str, Any], diretorio_destino: Optional[Path] = None) -> Path:
    """
    Gera um arquivo HTML elegante e pronto para impressão do certificado emitido.
    """
    destino = diretorio_destino or CERTIFICADOS_DIR
    destino.mkdir(parents=True, exist_ok=True)

    nome_seguro = "".join(c if c.isalnum() else "_" for c in certificado["aluno"].lower())
    tech_segura = certificado["tecnologia_id"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"certificado_{nome_seguro}_{tech_segura}_{timestamp}.html"
    caminho_arquivo = destino / nome_arquivo

    modulos_html = "".join(f"<li>{m}</li>" for m in certificado["modulos_concluidos"])

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Certificado Geo-Explorer - {certificado['aluno']}</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Inter:wght@300;400;600;700&display=swap');
    
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      font-family: 'Inter', sans-serif;
      background: #0f172a;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 30px;
      color: #1e293b;
    }}
    .cert-card {{
      background: #ffffff;
      width: 960px;
      padding: 50px 60px;
      border-radius: 16px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4);
      position: relative;
      border: 8px double #0284c7;
      background-image: radial-gradient(#e0f2fe 1px, transparent 1px);
      background-size: 20px 20px;
    }}
    .header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 20px;
      margin-bottom: 30px;
    }}
    .header-logo {{
      font-size: 26px;
      font-weight: 800;
      color: #0369a1;
      letter-spacing: 1px;
    }}
    .header-tag {{
      background: #0284c7;
      color: #ffffff;
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 13px;
      font-weight: 600;
      text-transform: uppercase;
    }}
    .title {{
      font-family: 'Cinzel', serif;
      font-size: 38px;
      text-align: center;
      color: #0f172a;
      letter-spacing: 2px;
      margin-bottom: 12px;
    }}
    .subtitle {{
      text-align: center;
      font-size: 16px;
      color: #64748b;
      margin-bottom: 35px;
    }}
    .student-name {{
      text-align: center;
      font-size: 32px;
      font-weight: 700;
      color: #0369a1;
      border-bottom: 2px solid #0284c7;
      display: inline-block;
      margin: 0 auto 25px auto;
      padding: 0 30px 8px 30px;
    }}
    .student-wrapper {{
      text-align: center;
    }}
    .body-text {{
      font-size: 16px;
      line-height: 1.8;
      text-align: center;
      color: #334155;
      max-width: 800px;
      margin: 0 auto 30px auto;
    }}
    .highlight {{
      font-weight: 700;
      color: #0f172a;
    }}
    .meta-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      background: #f8fafc;
      padding: 20px;
      border-radius: 12px;
      border: 1px solid #e2e8f0;
      margin-bottom: 30px;
    }}
    .meta-col h4 {{
      font-size: 14px;
      color: #0369a1;
      text-transform: uppercase;
      margin-bottom: 8px;
    }}
    .meta-col ul {{
      list-style-type: square;
      padding-left: 20px;
      font-size: 13px;
      color: #475569;
      line-height: 1.6;
    }}
    .footer {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-top: 2px solid #e2e8f0;
      padding-top: 25px;
      margin-top: 20px;
    }}
    .signature {{
      text-align: center;
    }}
    .signature-line {{
      width: 220px;
      border-top: 1px solid #334155;
      margin-bottom: 6px;
    }}
    .signature-title {{
      font-size: 12px;
      color: #64748b;
      font-weight: 600;
    }}
    .auth-box {{
      text-align: right;
    }}
    .auth-code {{
      font-family: monospace;
      font-weight: 700;
      font-size: 15px;
      color: #0284c7;
      letter-spacing: 1px;
    }}
    .auth-desc {{
      font-size: 11px;
      color: #94a3b8;
    }}
    @media print {{
      body {{
        background: none;
        padding: 0;
      }}
      .cert-card {{
        box-shadow: none;
        width: 100%;
      }}
    }}
  </style>
</head>
<body>
  <div class="cert-card">
    <div class="header">
      <div class="header-logo">🌍 GEO-EXPLORER</div>
      <div class="header-tag">Certificado Oficial Fictício</div>
    </div>
    
    <div class="title">CERTIFICADO DE CONCLUSÃO</div>
    <div class="subtitle">Certificamos com distinção acadêmica que</div>
    
    <div class="student-wrapper">
      <div class="student-name">{certificado['aluno']}</div>
    </div>
    
    <p class="body-text">
      concluiu com êxito todos os módulos e o desafio prático integrador da trilha
      <span class="highlight">{certificado['icone']} {certificado['tecnologia_nome']}</span> 
      no nível <span class="highlight">{certificado['nivel']}</span>, totalizando uma carga horária estimada de
      <span class="highlight">{certificado['carga_horaria']} horas</span> de aprendizado acelerado com apoio de IA.
    </p>

    <div class="meta-grid">
      <div class="meta-col">
        <h4>Módulos Concluídos</h4>
        <ul>
          {modulos_html}
        </ul>
      </div>
      <div class="meta-col">
        <h4>Desafio Integrador Superado</h4>
        <p style="font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 8px;">
          {certificado['desafio_concluido']}
        </p>
        <p style="font-size: 12px; color: #64748b;">
          <strong>Objetivo Alcançado:</strong> {certificado['objetivo_atingido']}
        </p>
      </div>
    </div>
    
    <div class="footer">
      <div class="signature">
        <div class="signature-line"></div>
        <div class="signature-title">IBM Bob Academy</div>
        <div style="font-size: 10px; color: #94a3b8;">Agente de Inteligência Artificial</div>
      </div>
      
      <div class="signature">
        <div class="signature-line"></div>
        <div class="signature-title">Digital Innovation One (DIO)</div>
        <div style="font-size: 10px; color: #94a3b8;">Plataforma de Aprendizagem</div>
      </div>
      
      <div class="auth-box">
        <div class="auth-code">{certificado['codigo_autenticidade']}</div>
        <div class="auth-desc">Código de Validação Digital</div>
        <div class="auth-desc">Emitido em: {certificado['data_emissao']}</div>
      </div>
    </div>
  </div>
</body>
</html>
"""

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(html_content)

    return caminho_arquivo


def salvar_certificado_json(certificado: Dict[str, Any], diretorio_destino: Optional[Path] = None) -> Path:
    """
    Salva os dados do certificado emitido em formato JSON.
    """
    destino = diretorio_destino or CERTIFICADOS_DIR
    destino.mkdir(parents=True, exist_ok=True)

    nome_seguro = "".join(c if c.isalnum() else "_" for c in certificado["aluno"].lower())
    tech_segura = certificado["tecnologia_id"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"certificado_{nome_seguro}_{tech_segura}_{timestamp}.json"
    caminho_arquivo = destino / nome_arquivo

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(certificado, f, indent=2, ensure_ascii=False)

    return caminho_arquivo
