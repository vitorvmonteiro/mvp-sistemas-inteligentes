import uvicorn
import pickle
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# INICIALIZAÇÃO DA API
# Adicionando docstrings e metadados para documentação automática (Swagger/ReDoc)
app = FastAPI(
    title="API de Predição de Churn de clientes",
    version="1.0.0",
    description="Uma API para prever o churn de clientes usando um modelo de Machine Learning."
)

# CARREGAMENTO DO MODELO
# O arquivo 'modelo_churn.pkl' é um pipeline que já contém o scaler e o modelo.
try:
    with open("modelo_churn.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    # Se o arquivo do modelo não for encontrado, a API não pode funcionar.
    # Exceção que interrompe a inicialização se o modelo estiver ausente.
    raise RuntimeError("Arquivo de modelo 'modelo_churn.pkl' não encontrado. A API não pode iniciar.")

# DEFINIÇÃO DO MODELO DE DADOS DE ENTRADA
class ChurnFeatures(BaseModel):
    """
    Define a estrutura e os tipos de dados esperados para uma única predição.
    Isso garante a validação automática dos dados de entrada pela FastAPI.
    """
    international_plan: int
    total_day_charge: float
    total_eve_charge: float
    customer_service_calls: int

    class Config:
        # Exemplo de como os dados devem ser formatados no JSON
        schema_extra = {
            "example": {
                "international_plan": 0,
                "total_day_charge": 45.07,
                "total_eve_charge": 18.55,
                "customer_service_calls": 3
            }
        }

# ENDPOINT DE PREDIÇÃO
@app.post("/predict")
def predict(features: ChurnFeatures):
    """
    Recebe os dados de um cliente, utiliza o modelo de ML para prever o churn
    e retorna o resultado.

    Args:
        features (ChurnFeatures): Um objeto contendo os dados do cliente.

    Returns:
        dict: Um dicionário JSON com a previsão de churn ("Sim" ou "Não").
    """
    # Conversão dos dados de entrada Pydantic para um DataFrame do Pandas
    input_data = pd.DataFrame([features.dict()])

    try:
        # O pipeline 'model' aplica a padronização e a predição em uma única etapa.
        prediction = model.predict(input_data)
        
        # O resultado de .predict() é um array (ex: [0]).
        prediction_value = int(prediction[0])
        
        # Mapeamento do resultado numérico para uma string clara para o frontend.
        churn_result = "Sim" if prediction_value == 1 else "Não"
        
        return {"churn_prediction": churn_result}

    except Exception as e:
        # Captura qualquer erro inesperado durante a predição.
        raise HTTPException(status_code=500, detail=f"Erro durante a predição: {e}")

# PONTO DE ENTRADA PARA EXECUÇÃO DA API
# Permite executar a API diretamente com 'python main.py'
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
