# 💻 Manual de Comandos do Geo-Explorer

O **Geo-Explorer** oferece uma interface de linha de comando (CLI) intuitiva e rica em recursos.

---

## 🧭 Modo Interativo

Se você executar o programa sem passar parâmetros, ele abrirá um menu interativo guiado:

```bash
python3 app/main.py
```

Você verá o menu:
```text
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

## ⚡ Execução Direta por Linha de Comando

### 1. Listar Trilhas Disponíveis
Lista todas as tecnologias cadastradas, níveis e descrições.

```bash
python3 app/main.py listar
```
*Ou diretamente:*
```bash
python3 comandos/listar.py
```

---

### 2. Consultar Trilha de Aprendizagem (`trilha`)
Exibe o plano de estudos detalhado (carga horária, módulos, tópicos).

```bash
# Consultar todos os níveis de uma tecnologia
python3 app/main.py trilha --tech python

# Consultar um nível específico
python3 app/main.py trilha --tech python --nivel iniciante
python3 app/main.py trilha --tech geoprocessamento --nivel intermediario
python3 app/main.py trilha --tech ibm-bob --nivel avancado
```

---

### 3. Obter Desafio de Código (`desafio`)
Gera o desafio prático de programação com enunciado, exemplos de I/O, código base (template) e dicas do IBM Bob.

```bash
python3 app/main.py desafio --tech python --nivel iniciante
python3 app/main.py desafio --tech sql --nivel intermediario
python3 app/main.py desafio --tech ibm-bob --nivel avancado
```

---

### 4. Emitir Certificado Fictício (`certificado`)
Gera um certificado estilizado no terminal e opcionalmente exporta em arquivos HTML (pronto para visualização e impressão) e JSON.

```bash
# Exibir apenas no terminal
python3 app/main.py certificado --nome "Rafael Santana" --tech python --nivel iniciante

# Exibir no terminal e salvar em disco (HTML e JSON na pasta certificados_emitidos/)
python3 app/main.py certificado --nome "Rafael Santana" --tech python --nivel iniciante --salvar

# Salvar apenas em formato HTML
python3 app/main.py certificado --nome "Rafael Santana" --tech geoprocessamento --nivel avancado --salvar --formato html
```

---

### 5. Iniciar Interface Web Local (`web`)
Inicia uma aplicação web visual no navegador na porta 8000:

```bash
python3 app/main.py web
# ou customizando a porta:
python3 app/main.py web --porta 8080
```

---

### 6. Iniciar Servidor MCP (`mcp`)
Inicia o servidor Model Context Protocol via stdio para conexão com Claude, IBM Bob, etc.

```bash
python3 app/main.py mcp
# ou
python3 app/mcp_server.py
```
