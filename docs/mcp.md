# 🤖 Guia do Servidor MCP (Model Context Protocol)

O **Model Context Protocol (MCP)** é um protocolo aberto que padroniza a comunicação entre agentes de Inteligência Artificial (LLMs) e ferramentas ou fontes de contexto externas.

No projeto **Geo-Explorer**, o servidor MCP expõe as trilhas de estudos, os desafios de programação e o gerador de certificados como **Ferramentas (Tools)** e **Recursos (Resources)** acessíveis por agentes inteligentes, como o **IBM Bob**.

---

## 🛠️ Ferramentas Disponíveis (Tools)

O servidor MCP do Geo-Explorer disponibiliza 4 ferramentas:

| Nome da Ferramenta | Descrição | Parâmetros |
| :--- | :--- | :--- |
| `listar_tecnologias` | Retorna a lista resumida de todas as tecnologias e seus níveis. | Nenhum. |
| `consultar_trilha` | Retorna o plano de estudos detalhado (módulos, carga horária, tópicos). | `tecnologia` (obrigatório), `nivel` (opcional: iniciante, intermediario, avancado). |
| `gerar_desafio` | Retorna um desafio prático com template, critérios e dicas. | `tecnologia` (obrigatório), `nivel` (obrigatório). |
| `gerar_certificado` | Cria um certificado oficial fictício com hash de validação. | `nome_aluno` (obrigatório), `tecnologia` (obrigatório), `nivel` (obrigatório). |

---

## 📦 Recursos Expostos (Resources)

- `geo-explorer://trilhas/todas`: Fornece a base de conhecimento completa em formato JSON para que o agente possa absorver todo o contexto das trilhas em memória.

---

## ⚙️ Como Configurar em Agentes de IA

### 1. Configuração no Claude Desktop / IBM Bob (`claude_desktop_config.json`)

Adicione o servidor Geo-Explorer ao arquivo de configuração de servidores MCP da sua ferramenta:

```json
{
  "mcpServers": {
    "geo-explorer": {
      "command": "python3",
      "args": [
        "/home/maia/Documentos/Rafa/Projetos/geo-explorer/app/mcp_server.py"
      ]
    }
  }
}
```

### 2. Execução Direta via Terminal

Você também pode iniciar o servidor MCP manualmente pelo terminal:

```bash
python3 app/mcp_server.py
```
*(O servidor ficará em execução aguardando mensagens no padrão JSON-RPC 2.0 através da entrada padrão STDIN)*.

---

## 💬 Exemplos de Mensagens JSON-RPC 2.0

### Inicialização (`initialize`)
**Requisição:**
```json
{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
```
**Resposta:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
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
```

### Chamando a ferramenta `gerar_desafio` (`tools/call`)
**Requisição:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "gerar_desafio",
    "arguments": {
      "tecnologia": "python",
      "nivel": "iniciante"
    }
  }
}
```
**Resposta:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{ ... json com o desafio ... }"
      }
    ]
  }
}
```
