import pytest
import pickle
import pandas as pd
from sklearn.metrics import f1_score
import os

# --- CONSTANTES E CONFIGURAÇÕES DO TESTE ---

# Definimos um limiar de desempenho. Se o F1-Score do modelo for menor que isso, o teste falha.
# Este valor deve ser definido com base nos requisitos de negócio.
F1_THRESHOLD = 0.75 

# Caminho para o modelo e para os dados de teste.
# Usamos caminhos relativos para funcionar em qualquer máquina.
# O '..' sobe um nível de diretório (de 'tests' para 'backend').
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'modelo_churn.pkl')
DATA_PATH = os.path.join(os.path.dirname(__file__), 'test_data.csv')


# --- FIXTURES DO PYTEST ---

@pytest.fixture(scope="session")
def model():
    """
    Carrega o modelo de machine learning do arquivo .pkl.
    A fixture com scope="session" garante que o modelo seja carregado apenas uma vez
    para todos os testes da sessão, economizando tempo.
    """
    try:
        with open(MODEL_PATH, "rb") as f:
            loaded_model = pickle.load(f)
        return loaded_model
    except FileNotFoundError:
        pytest.fail(f"Modelo não encontrado em '{MODEL_PATH}'. Certifique-se de que o arquivo existe.")

@pytest.fixture(scope="session")
def test_data():
    """
    Carrega os dados de teste do arquivo CSV.
    Esses dados contêm as features e a variável alvo real ('churn').
    """
    try:
        data = pd.read_csv(DATA_PATH)
        return data
    except FileNotFoundError:
        pytest.fail(f"Arquivo de dados de teste não encontrado em '{DATA_PATH}'.")


# --- TESTES DE DESEMPENHO ---

def test_model_f1_score(model, test_data):
    """
    Testa se o F1-Score do modelo nos dados de teste atinge o limiar mínimo esperado.
    
    Este teste é crucial para a integração contínua (CI): se um novo modelo for treinado
    e seu desempenho for inferior ao esperado, este teste falhará, impedindo o deploy.
    """
    # Separa as features (X) da variável alvo (y)
    X_test = test_data.drop("churn", axis=1)
    y_test = test_data["churn"]

    # Faz a predição com o modelo carregado
    predictions = model.predict(X_test)

    # Calcula o F1-Score comparando as predições com os valores reais
    f1 = f1_score(y_test, predictions)

    print(f"F1-Score calculado: {f1:.4f}")
    print(f"Limiar mínimo esperado: {F1_THRESHOLD}")

    # A asserção principal: o teste passa se o F1-Score for maior ou igual ao limiar.
    assert f1 >= F1_THRESHOLD, (
        f"Desempenho do modelo abaixo do esperado! "
        f"F1-Score foi de {f1:.4f}, mas o mínimo aceitável é {F1_THRESHOLD}."
    )

def test_prediction_output_type(model, test_data):
    """
    Testa se a saída do modelo é do tipo esperado (0 ou 1).
    Isso garante que o modelo não está produzindo saídas em formatos inesperados.
    """
    X_test = test_data.drop("churn", axis=1).head(1) # Pega apenas uma linha para o teste
    prediction = model.predict(X_test)
    
    # Verifica se a predição é um dos valores esperados
    assert prediction[0] in [0, 1], f"A predição retornou um valor inesperado: {prediction[0]}"

