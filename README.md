# MVP de Previsão de Churn - Qualidade de Software, Segurança e Sistemas Inteligentes

Descrição: MVP (Minimum Viable Product) de uma aplicação full stack para previsão de churn de clientes. A aplicação utiliza um modelo de Machine Learning treinado para classificar se um cliente tem alta ou baixa probabilidade de cancelar seu serviço.

# Funcionalidades

  * **API RESTful:** Backend com FastAPI para servir o modelo de previsão.
  * **Interface Web Interativa:** Frontend amigável construído com Streamlit para facilitar a entrada de dados.
  * **Previsão:** Classifica clientes como "Churn: Sim" ou "Churn: Não" com base nos dados fornecidos.
  * **Histórico de previsões:** Exibe as últimas previsões realizadas para fácil consulta.
  * **Testes automatizados:** Garante a qualidade e o desempenho do modelo com PyTest.

# Estrutura do projeto

```
projeto_churn/
├── backend/
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_model_performance.py    # Teste de desempenho do modelo
│   ├── main.py                          # Lógica da API com FastAPI
│   └── modelo_churn.pkl                 # Arquivo do modelo treinado
│
├── frontend/
│   └── app.py                           # Interface com Streamlit
│
├── .gitignore                           # Arquivo para ignorar arquivos do Git
├── README.md                            # Este arquivo
└── requirements.txt                     # Dependências do projeto
```

# Como executar o projeto localmente

Siga os passos abaixo para configurar e executar a aplicação em sua máquina.

# Pré-requisitos

  * Python 3.9+
  * Git

# 1\. Clonar o Repositório

1.1 Abra seu terminal e clone o repositório do GitHub:

```
git clone https://github.com/vitorvmonteiro/mvp-sistemas-inteligentes.git
```
1.2 Entre na pasta do MVP

```
cd mvp-sistemas-inteligentes
```

# 2\. Criar e ativar um ambiente virtual

2.1 - Criação do ambiente virtual

```powershell
python -m venv .venv
```
2.2 - Ativação do ambiente virtual

Windows:
```powershell
.\.venv\Scripts\Activate.ps1
```

Linux:
```bash
source .venv/bin/activate
```

# 3\. Instalar as dependências

Com o ambiente virtual ativado, instale todas as bibliotecas necessárias listadas no arquivo `requirements.txt`.

```
pip install -r requirements.txt
```

# 4\. Executar o Backend

Navegue até a pasta do backend e inicie a API com o Uvicorn.

```
cd backend
```
```
uvicorn main:app --reload
```

A API estará rodando em `http://127.0.0.1:8000`. Você pode acessar a documentação interativa em `http://127.0.0.1:8000/docs`.

### 5\. Executar o Frontend

⚠️ Abra um **NOVO TERMINAL**, **ATIVE O AMBIENTE VIRTUAL** novamente e navegue até a pasta do frontend e inicie a aplicação Streamlit.

5.1 - Ativação do ambiente virtual:

 Windows
 ```powershell
 .\.venv\Scripts\Activate.ps1
 ```
 Linux
 ```bash
 source .venv/bin/activate
 ```
5.2 - Mude para pasta do frontend
 ```
 cd frontend
 ```
5.3 - Inicie o Streamlit
 ```
 streamlit run app.py
 ```

A interface web estará acessível no seu navegador, geralmente em `http://localhost:8501`.

# 6\. Executar os testes

Para verificar a performance do modelo, você pode rodar os testes automatizados com PyTest. No terminal, a partir da pasta `backend`, execute:

```
pytest
```

# Como usar a aplicação

Com o backend e o frontend rodando, acesse a URL do Streamlit no seu navegador.

1.  **Preencha os campos** do formulário com os dados do cliente.
2.  Clique no botão **"Fazer Previsão"**.
3.  O **resultado será exibido** na tela, indicando se a previsão de churn é "Sim" ou "Não".
4.  Um **histórico das previsões** recentes será exibido na parte inferior da página.
