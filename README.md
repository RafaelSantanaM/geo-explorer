# 🌍 Geo-Explorer

> **Explorador de Trilhas de Aprendizagem, Desafios de Código e Certificação com Apoio do IBM Bob**  
> *Projeto desenvolvido para o Bootcamp IBM Bob da Digital Innovation One (DIO)*

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/Model_Context_Protocol-MCP-0284c7)](https://modelcontextprotocol.io/)
[![Testes](https://img.shields.io/badge/Testes-30%20Passando-34d399)](testes/)
[![Status](https://img.shields.io/badge/Status-Conclu%C3%ADdo-brightgreen)](#)
[![DIO](https://img.shields.io/badge/DIO-Bootcamp%20IBM%20Bob-E50914)](https://dio.me)

---

## 📖 O Que é o Geo-Explorer?

O **Geo-Explorer** é uma plataforma desenvolvida para proporcionar uma jornada imersiva de exploração do conhecimento tecnológico. Com o auxílio do agente de inteligência artificial **IBM Bob** em todo o ciclo de vida do desenvolvimento (planejamento, codificação, automação de testes e documentação), o projeto oferece:

1. **🧭 Trilhas de Estudos:** Planos de estudo detalhados com carga horária, objetivos pedagógicos, módulos e tópicos práticos divididos por nível (Iniciante, Intermediário e Avançado).
2. **🎯 Desafios de Código:** Exercícios práticos contextualizados com enunciados objetivos, exemplos de entrada e saída, código inicial (template), critérios de aceitação e dicas geradas por IA.
3. **📜 Certificados Fictícios de Conclusão:** Emissão de certificados personalizados com código de autenticidade criptográfico (hash SHA-256), exibição em moldura no terminal e exportação em formato **HTML visual** para impressão/PDF e **JSON**.
4. **🤖 Servidor MCP Integrado:** Um servidor nativo baseado no padrão aberto **Model Context Protocol (MCP)**, permitindo que agentes como o IBM Bob ou Claude acessem diretamente as funções do Geo-Explorer como ferramentas corporativas (*tool calling*).
5. **🌐 Interface Web Interativa:** Um painel web moderno e responsivo construído exclusivamente com a biblioteca padrão do Python, sem necessidade de dependências adicionais.

---

## 🗂️ Estrutura do Projeto

O projeto foi organizado de forma modular, separando responsabilidades de dados, regras de negócio, comandos, testes e documentação:

```text
geo-explorer/
├── app/
│   ├── gerenciador.py          # Camada de serviço, leitura de dados e hash do certificado
│   ├── main.py                 # Ponto de entrada CLI e Menu Interativo
│   ├── mcp_server.py           # Servidor MCP (JSON-RPC 2.0 via stdio)
│   ├── web.py                  # Servidor e interface Web local nativa
│   └── init.md                 # Registro de tecnologias e modelos de apoio
├── comandos/
│   ├── trilha.py               # Comando para consulta de trilhas de estudo
│   ├── desafio.py              # Comando para geração de desafios práticos
│   ├── certificado.py          # Comando para emissão de certificados fictícios
│   └── listar.py               # Comando para listagem de todas as tecnologias
├── dados/
│   └── trilhas.json            # Base de dados estruturada em JSON
├── docs/
│   ├── arquitetura.md          # Especificação técnica e fluxo do sistema
│   ├── mcp.md                  # Manual do Servidor MCP e integração com IA
│   └── comandos.md             # Documentação de referência da linha de comando
├── testes/
│   ├── test_dados.py           # Testes de integridade do arquivo JSON
│   ├── test_trilha.py          # Testes unitários do comando trilha
│   ├── test_desafio.py         # Testes unitários do comando desafio
│   ├── test_certificado.py     # Testes unitários do comando certificado
│   └── test_mcp.py             # Testes do Servidor MCP e JSON-RPC
├── certificados_emitidos/      # Pasta de saída para os certificados gerados
├── .gitignore                  # Regras de exclusão do Git
└── README.md                   # Documentação principal
```

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
- **Python 3.10** ou superior instalado em seu sistema operacional.
- *Não são necessárias dependências externas via pip! Todo o núcleo utiliza a rica biblioteca padrão do Python.*

### 1. Clonar o Repositório
```bash
git clone https://github.com/RafaelSantanaM/geo-explorer.git
cd geo-explorer
```

### 2. Executar no Modo Interativo (Recomendado)
Execute o comando principal sem argumentos para abrir o menu guiado:
```bash
python3 app/main.py
```

Você verá o menu interativo:
```text
   _____ ______ ____        ______ _____  _      ____  _____  ______ _____  
  / ____|  ____/ __ \      |  ____|  __ \| |    / __ \|  __ \|  ____|  __ \ 
 | |  __| |__ | |  | |_____| |__  | |__) | |   | |  | | |__) | |__  | |__) |
 | | |_ |  __|| |  | |_____|  __| |  ___/| |   | |  | |  _  /|  __| |  _  / 
 | |__| | |___| |__| |     | |____| |    | |___| |__| | | \ \| |____| | \ \ 
  \_____|______\____/      |______|_|    |______\____/|_|  \_\______|_|  \_\

============================================================
  🧭 MENU PRINCIPAL - SELECIONE UMA OPÇÃO:
============================================================
  [1] 📖 Consultar Trilha de Estudos
  [2] 🎯 Obter Desafio de Código
  [3] 📜 Emitir Certificado Fictício
  [4] 📋 Listar Todas as Trilhas e Tecnologias
  [5] 🤖 Iniciar Servidor MCP (Model Context Protocol)
  [6] 🌐 Iniciar Interface Web Local
  [0] ❌ Sair
------------------------------------------------------------
```

---

## 💻 Como Usar os Comandos (CLI)

O Geo-Explorer permite execução direta de cada funcionalidade via linha de comando:

### 1. Listar Tecnologias Disponíveis
```bash
python3 app/main.py listar
```
> *Tecnologias disponíveis:* `python`, `javascript`, `sql`, `geoprocessamento`, `ibm-bob`.

### 2. Consultar Trilha de Estudos (`trilha`)
Exibe os módulos, carga horária e ementa completa:
```bash
# Consultar trilha com todos os níveis:
python3 app/main.py trilha --tech python

# Consultar nível específico:
python3 app/main.py trilha --tech python --nivel iniciante
python3 app/main.py trilha --tech geoprocessamento --nivel intermediario
```

### 3. Gerar Desafio de Código (`desafio`)
Exibe o problema, exemplos de entrada/saída, código inicial e dicas de IA:
```bash
python3 app/main.py desafio --tech python --nivel iniciante
python3 app/main.py desafio --tech sql --nivel intermediario
python3 app/main.py desafio --tech ibm-bob --nivel avancado
```

### 4. Emitir Certificado Fictício (`certificado`)
Gera o certificado estilizado no terminal e salva cópias em **HTML** e **JSON**:
```bash
# Exibir no terminal e salvar em disco:
python3 app/main.py certificado --nome "Rafael Santana" --tech python --nivel iniciante --salvar
```
O arquivo HTML gerado em `certificados_emitidos/` possui layout pronto para impressão em PDF de alta qualidade.

### 5. Iniciar Interface Web Local (`web`)
Abre uma aplicação web no navegador:
```bash
python3 app/main.py web
```
Acesse em: `http://localhost:8000`

---

## 🤖 Servidor MCP (Model Context Protocol)

O projeto implementa um **Servidor MCP** completo baseado no protocolo aberto JSON-RPC 2.0 sobre `stdio`, viabilizando que agentes de IA corporativos integrem os recursos do Geo-Explorer.

### Ferramentas Expostas (Tools):
- `listar_tecnologias`: Retorna todas as trilhas cadastradas.
- `consultar_trilha`: Consulta detalhada de planos de estudo por tecnologia e nível.
- `gerar_desafio`: Fornece o desafio prático de código conforme o nível.
- `gerar_certificado`: Emite o certificado digital com validação criptográfica.

### Como Iniciar:
```bash
python3 app/main.py mcp
# ou
python3 app/mcp_server.py
```

Para integrar ao Claude Desktop ou outro cliente compatível, consulte o [Guia do Servidor MCP](docs/mcp.md).

---

## 🧪 Como Executar os Testes Automatizados

O projeto conta com uma suíte de **30 testes unitários automatizados** construídos com o framework nativo `unittest`, cobrindo integridade da base JSON, comandos CLI, validação de exceções e o Servidor MCP.

Para executar todos os testes, basta rodar no terminal:

```bash
python3 -m unittest discover -s testes -v
```

### Exemplo de Saída:
```text
test_campos_obrigatorios_por_trilha (test_dados.TestDadosTrilhas) ... ok
test_estrutura_dos_desafios (test_dados.TestDadosTrilhas) ... ok
test_estrutura_raiz (test_dados.TestDadosTrilhas) ... ok
test_obter_desafio_python_iniciante (test_desafio.TestComandoDesafio) ... ok
test_emitir_certificado_sucesso (test_certificado.TestComandoCertificado) ... ok
test_determinismo_hash_certificado (test_certificado.TestComandoCertificado) ... ok
test_initialize (test_mcp.TestServidorMCP) ... ok
test_tools_list (test_mcp.TestServidorMCP) ... ok
test_tools_call_consultar_trilha (test_mcp.TestServidorMCP) ... ok
...
Ran 30 tests in 0.027s

OK
```

---

## ✨ Quais Melhorias Foram Realizadas

Além dos requisitos básicos sugeridos no desafio da DIO, foram adicionadas evoluções significativas:

1. **Servidor MCP Nativo (Model Context Protocol):** Implementação completa em Python sobre JSON-RPC 2.0 (stdio) com ferramentas e recursos dinâmicos para agentes de IA.
2. **Certificado com Hash SHA-256 e Exportação HTML:** Algoritmo que gera um código verificador único (`GEO-...`) e renderiza um documento HTML estilizado, responsivo e preparado para impressão em PDF.
3. **Modo Interativo no Terminal (CLI Dashboard):** Além da passagem de argumentos tradicionais, o usuário pode navegar por um menu interativo acolhedor com banners e prompts passo a passo.
4. **Interface Web Local Embutida (`app/web.py`):** Interface visual no navegador utilizando `http.server` nativo, permitindo consultar trilhas, resolver desafios e emitir certificados visualmente com um clique.
5. **Base de Dados Ampliada e Temática:** Inclusão de 5 trilhas completas:
   - *Python Essentials & Data Explorer*
   - *JavaScript Full-Stack & Interatividade*
   - *SQL & Bancos de Dados Relacionais*
   - *Geotecnologias & Python Espacial (Geo-Python, Shapely, GeoPandas e Sensoriamento)*
   - *IBM Bob & Desenvolvimento com Agentes de IA (Engenharia de Prompt, Subagentes e MCP)*
6. **30 Testes Automatizados:** Testes cobrindo validação de schema, sanitização de inputs, regras de negócio e protocolo JSON-RPC.
7. **Documentação Técnica Completa:** Documentos dedicados em `docs/` para [Arquitetura](docs/arquitetura.md), [Servidor MCP](docs/mcp.md) e [Guia de Comandos](docs/comandos.md).

---

## 🧠 O Que Foi Aprendido Durante o Desafio

- **Atuação com o IBM Bob como Agente Pair-Programmer:** Utilização de técnicas de prompting, refinamento iterativo de código e automação de tarefas no ciclo SDLC com IA.
- **Model Context Protocol (MCP):** Entendimento profundo de como agentes LLM descobrem capacidades e executam ferramentas em sistemas externos usando JSON-RPC 2.0.
- **Arquitetura de Software Modular:** Separação estrita entre dados estruturados, regras de negócio, interfaces de usuário (CLI / Web) e protocolos de integração.
- **Testes Automatizados (TDD):** Criação de baterias de testes para garantir a integridade dos dados e prevenir regressões durante a evolução do projeto.
- **Segurança e Criptografia Fictícia:** Aplicação de hashing (SHA-256) e tratamento rigoroso de dados para prevenir vazamentos acidentais de credenciais no Git/GitHub.

---

## 👨‍💻 Autor

Desenvolvido por **Rafael Santana**  
- GitHub: [@RafaelSantanaM](https://github.com/RafaelSantanaM)  
- Repositório do Projeto: [geo-explorer](https://github.com/RafaelSantanaM/geo-explorer)  
- Bootcamp: *IBM Bob: IA de Nível Empresarial para Desenvolvedores e Tech Leaders (DIO)*
