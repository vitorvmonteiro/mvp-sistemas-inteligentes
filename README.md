# MVP de Previsão de Churn - Qualidade de Software, Segurança e Sistemas Inteligentes

Este projeto é um MVP (Minimum Viable Product) de uma aplicação full stack para previsão de churn de clientes. A aplicação utiliza um modelo de Machine Learning treinado para classificar se um cliente tem alta ou baixa probabilidade de cancelar seu serviço.

## ✨ Funcionalidades

  * **API RESTful:** Backend robusto com FastAPI para servir o modelo de previsão.
  * **Interface Web Interativa:** Frontend amigável construído com Streamlit para facilitar a entrada de dados.
  * **Previsão em Tempo Real:** Classifica clientes como "Churn: Sim" ou "Churn: Não" com base nos dados fornecidos.
  * **Histórico de Previsões:** Exibe as últimas previsões realizadas para fácil consulta.
  * **Testes Automatizados:** Garante a qualidade e o desempenho do modelo com PyTest.

## 🛠️ Tecnologias Utilizadas

### Backend:

  * **FastAPI:** Para criar uma API RESTful, rápida e robusta para servir o modelo.
  * **Uvicorn:** Como servidor ASGI para rodar a aplicação FastAPI.
  * **Scikit-learn:** Para carregar e utilizar o pipeline de Machine Learning.
  * **Pandas:** Para manipulação de dados na API.

### Frontend:

  * **Streamlit:** Para construir uma interface de usuário web interativa de forma rápida e simples.

### Testes:

  * **PyTest:** Para garantir a qualidade e o desempenho do modelo através de testes automatizados.

## 📂 Estrutura do Projeto

```
projeto_churn/
├── backend/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_model_performance.py    # Teste de desempenho do modelo
│   │   └── test_data.csv                # Dados para o teste
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

## 🚀 Como Executar o Projeto Localmente

Siga os passos abaixo para configurar e executar a aplicação em sua máquina.

### Pré-requisitos

  * Python 3.9+
  * Git

### 1\. Clonar o Repositório

Abra seu terminal (**PowerShell**) e clone o repositório do GitHub:

```powershell
git clone https://github.com/vitorvmonteiro/mvp-sistemas-inteligentes.git
cd mvp-sistemas-inteligentes
```

### 2\. Criar e Ativar um Ambiente Virtual

É uma boa prática criar um ambiente virtual para isolar as dependências do projeto.

```powershell
# Criar o ambiente virtual
python -m venv .venv

# Ativar o ambiente virtual (no PowerShell)
.\.venv\Scripts\Activate.ps1
```

### 3\. Instalar as Dependências

Com o ambiente virtual ativado, instale todas as bibliotecas necessárias listadas no arquivo `requirements.txt`.

```powershell
pip install -r requirements.txt
```

### 4\. Executar o Backend

Navegue até a pasta do backend e inicie a API com o Uvicorn.

```powershell
cd backend
uvicorn main:app --reload
```

A API estará rodando em `http://127.0.0.1:8000`. Você pode acessar a documentação interativa em `http://127.0.0.1:8000/docs`.

### 5\. Executar o Frontend

Abra um **novo terminal**, ative o ambiente virtual novamente (`.\.venv\Scripts\Activate.ps1`), navegue até a pasta do frontend e inicie a aplicação Streamlit.

```powershell
# Não se esqueça de ativar o ambiente virtual neste novo terminal!
.\.venv\Scripts\Activate.ps1

cd frontend
streamlit run app.py
```

A interface web estará acessível no seu navegador, geralmente em `http://localhost:8501`.

### 6\. Executar os Testes (Opcional)

Para verificar a performance do modelo, você pode rodar os testes automatizados com PyTest. No terminal, a partir da pasta `backend`, execute:

```powershell
# Certifique-se de estar na pasta 'backend'
pytest
```

## 💻 Como Usar a Aplicação

Com o backend e o frontend rodando, acesse a URL do Streamlit no seu navegador.

1.  **Preencha os campos** do formulário com os dados do cliente.
2.  Clique no botão **"Fazer Previsão"**.
3.  O **resultado será exibido** na tela, indicando se a previsão de churn é "Sim" ou "Não".
4.  Um **histórico das previsões** recentes será exibido na parte inferior da página.