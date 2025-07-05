import pytest
import pickle
import pandas as pd
from sklearn.metrics import accuracy_score
import os

# CONSTANTES E CONFIGURAÇÕES DO TESTE

# Limiar de desempenho: 
ACCURACY_THRESHOLD = 0.80

# Caminhos para o modelo e para os dados de teste.
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'modelo_churn.pkl')
DATA_PATH = os.path.join(os.path.dirname(__file__), 'test_data.csv')


# Estruturas de Suporte

@pytest.fixture(scope="session")
def model():
    """
    Carrega o modelo de machine learning uma única vez por sessão de teste.
    Se o arquivo não for encontrado, o teste falha imediatamente com uma mensagem clara.
    """
    try:
        with open(MODEL_PATH, "rb") as f:
            loaded_model = pickle.load(f)
        return loaded_model
    except FileNotFoundError:
        pytest.fail(f"Arquivo do modelo não encontrado em: '{MODEL_PATH}'. Verifique o caminho.")

@pytest.fixture(scope="session")
def test_data():
    """
    Carrega os dados de teste uma única vez por sessão.
    Falha de forma controlada se o arquivo de dados não existir.
    """
    try:
        data = pd.read_csv(DATA_PATH)
        return data
    except FileNotFoundError:
        pytest.fail(f"Arquivo de dados de teste não encontrado em: '{DATA_PATH}'.")


# TESTE DE DESEMPENHO

def test_model_accuracy_above_threshold(model, test_data):
    """
    Verifica se a acurácia do modelo nos dados de teste é superior ao limiar definido.

    Este é o único teste de desempenho, focado em garantir que a performance do
    modelo atenda ao requisito mínimo de acurácia.
    """
    # 1. Separa as features (X) da variável alvo (y)
    X_test = test_data.drop("churn", axis=1)
    y_test = test_data["churn"]

    # 2. Realiza as predições com o modelo
    predictions = model.predict(X_test)

    # 3. Mede a acurácia comparando predições com os valores reais
    accuracy = accuracy_score(y_test, predictions)

    # Logs para facilitar a depuração no terminal
    print(f"\nAcurácia Calculada: {accuracy:.2%}")
    print(f"Limiar Mínimo de Acurácia: {ACCURACY_THRESHOLD:.2%}")

    # 4. Verificação (Assert): O teste passa se a acurácia for igual ou maior ao limiar
    assert accuracy >= ACCURACY_THRESHOLD, (
        f"Desempenho de acurácia do modelo abaixo do esperado! "
        f"Obtido: {accuracy:.2%}, Limiar Mínimo: {ACCURACY_THRESHOLD:.2%}"
    )
