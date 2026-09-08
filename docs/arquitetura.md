# 🏛️ Arquitetura do Geo-Explorer

O **Geo-Explorer** é uma plataforma desenvolvida com o apoio do agente de Inteligência Artificial **IBM Bob**, desenhada para proporcionar uma experiência interativa de exploração de trilhas de aprendizagem, desafios práticos de código e emissão de certificados fictícios de conclusão.

---

## 📂 Estrutura de Diretórios

A estrutura do projeto foi organizada de forma modular e desacoplada:

```text
geo-explorer/
├── app/
│   ├── gerenciador.py       # Regras de negócio, acesso a dados e emissão de certificados
│   ├── main.py              # Ponto de entrada CLI e menu interativo
│   ├── mcp_server.py        # Servidor Model Context Protocol (JSON-RPC 2.0 via stdio)
│   ├── web.py               # Interface Web nativa em Python (http.server)
│   └── init.md              # Registro das tecnologias e modelos do bootcamp
├── comandos/
│   ├── trilha.py            # Comando CLI para consulta de trilhas e planos de estudo
│   ├── desafio.py           # Comando CLI para geração de desafios de código
│   ├── certificado.py       # Comando CLI para emissão e exportação de certificados
│   └── listar.py            # Comando CLI para listagem resumida de tecnologias
├── dados/
│   └── trilhas.json         # Base de dados estruturada das tecnologias, níveis e desafios
├── docs/
│   ├── arquitetura.md       # Visão técnica e design da solução
│   ├── mcp.md               # Guia do Servidor MCP e integração com IA
│   └── comandos.md          # Manual de uso dos comandos CLI
├── testes/
│   ├── test_dados.py        # Validação do schema e integridade do trilhas.json
│   ├── test_trilha.py       # Testes unitários para o comando trilha
│   ├── test_desafio.py      # Testes unitários para o comando desafio
│   ├── test_certificado.py  # Testes unitários para geração e hash de certificados
│   └── test_mcp.py          # Testes do protocolo JSON-RPC e tools do MCP
├── certificados_emitidos/   # Pasta de saída dos certificados gerados (HTML / JSON)
├── .gitignore               # Configuração de arquivos ignorados no versionamento
└── README.md                # Apresentação do projeto e instruções gerais
```

---

## 🧩 Componentes Principais

### 1. Camada de Dados (`dados/trilhas.json`)
Armazena de forma centralizada todas as informações sobre:
- **Tecnologias**: `python`, `javascript`, `sql`, `geoprocessamento`, `ibm-bob`.
- **Níveis de Proficiência**: `iniciante`, `intermediario`, `avancado`.
- **Módulos**: Títulos, descrições detalhadas e lista de tópicos.
- **Desafios Práticos**: Enunciado, entrada de exemplo, saída esperada, código base (template), critérios de aceitação e dicas orientadas por IA.

### 2. Camada de Negócio (`app/gerenciador.py`)
Centraliza as operações de leitura, filtragem e transformação dos dados:
- Normalização de buscas (insensível a maiúsculas/minúsculas).
- Validação estrita de tecnologias e níveis.
- Algoritmo de hash criptográfico para validação digital do certificado.
- Renderizador de certificados em HTML visual para impressão/PDF.

### 3. Camada de Interface CLI (`comandos/` e `app/main.py`)
Permite duas formas de interação:
- **Modo Argumentos**: `python3 app/main.py trilha -t python -n iniciante`
- **Modo Interativo**: `python3 app/main.py` exibe um menu guiado no terminal.

### 4. Camada de Integração com IA (`app/mcp_server.py`)
Implementa o padrão **Model Context Protocol (MCP)** sobre entrada e saída padrão (`stdio`), expondo ferramentas que permitem a qualquer LLM consultar trilhas, solicitar desafios e emitir certificados diretamente para os usuários.

### 5. Camada Web (`app/web.py`)
Disponibiliza um painel visual moderno no navegador utilizando apenas a biblioteca padrão `http.server` do Python, garantindo portabilidade máxima sem necessidade de dependências pesadas.

---

## 🔐 Autenticidade do Certificado

Para garantir que os certificados gerados no Geo-Explorer tenham um identificador único e verificável, o sistema gera uma assinatura baseada em SHA-256:

$$\text{Hash} = \text{SHA256}(\text{ALUNO} \parallel \text{TECH} \parallel \text{NÍVEL} \parallel \text{DATA} \parallel \text{SALT})[0:16]$$

O código gerado tem o formato `GEO-<16_HEX_UPPERCASE>`, garantindo que cada certificado emitido seja rastreável e único.
