# Importações necessárias
import streamlit as st
import requests
import pandas as pd

# --- CONFIGURAÇÕES DA PÁGINA E URL DO BACKEND ---
BACKEND_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="Previsão de Churn",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- TÍTULO E DESCRIÇÃO ---
st.title("🤖 Sistema de Previsão de Churn de Clientes")
st.write(
    "Esta ferramenta utiliza um modelo de Machine Learning para prever se um cliente "
    "está propenso a cancelar seu serviço (churn). Preencha os dados abaixo para obter a previsão."
)
st.markdown("---")

# --- INICIALIZAÇÃO DO HISTÓRICO DE PREVISÕES ---
# Usamos o st.session_state para manter o histórico entre as interações do usuário.
if 'prediction_history' not in st.session_state:
    st.session_state['prediction_history'] = []

# --- FORMULÁRIO DE ENTRADA DE DADOS ---
# st.form agrupa os widgets de entrada e só envia os dados quando o botão é pressionado.
with st.form("input_form"):
    st.header("Insira os dados do cliente:")

    # Mapeamento de opções amigáveis para os valores numéricos que a API espera (0 ou 1)
    plan_options = {"Não": 0, "Sim": 1}
    selected_plan_label = st.selectbox(
        "O cliente possui plano internacional?",
        options=list(plan_options.keys()),
        help="Selecione 'Sim' se o cliente tiver um plano internacional ativo."
    )
    international_plan_value = plan_options[selected_plan_label]

    total_day_charge = st.number_input(
        "Custo total das chamadas diurnas ($)",
        min_value=0.0, step=0.01, format="%.2f",
        help="Valor total cobrado do cliente por chamadas realizadas durante o dia."
    )

    total_eve_charge = st.number_input(
        "Custo total das chamadas noturnas ($)",
        min_value=0.0, step=0.01, format="%.2f",
        help="Valor total cobrado do cliente por chamadas realizadas durante a noite."
    )

    customer_service_calls = st.number_input(
        "Nº de chamadas para o atendimento ao cliente",
        min_value=0, step=1,
        help="Quantas vezes o cliente contatou o serviço de atendimento ao cliente."
    )
    
    # Botão para submeter o formulário e fazer a predição
    submit_button = st.form_submit_button(label="Fazer Previsão")

# --- LÓGICA DE PREDIÇÃO E EXIBIÇÃO DO RESULTADO ---
if submit_button:
    # Dicionário com os dados para enviar à API (nomes das chaves devem ser idênticos aos da API)
    feature_data = {
        "international_plan": international_plan_value,
        "total_day_charge": total_day_charge,
        "total_eve_charge": total_eve_charge,
        "customer_service_calls": customer_service_calls,
    }

    # MELHORIA: Adiciona um spinner para melhorar a experiência do usuário
    with st.spinner("Analisando dados e fazendo previsão..."):
        try:
            # Faz a requisição POST para o backend
            response = requests.post(BACKEND_URL, json=feature_data)
            # Levanta um erro HTTP para respostas mal-sucedidas (código 4xx ou 5xx)
            response.raise_for_status() 

            # Extrai o resultado da resposta JSON
            prediction_result = response.json()
            churn_prediction = prediction_result.get("churn_prediction", "Erro na resposta")
            
            # Exibe o resultado com um alerta colorido e um ícone
            st.markdown("---")
            st.subheader("Resultado da Previsão")
            if churn_prediction == "Sim":
                st.error(f"**Previsão de Churn: {churn_prediction}**", icon="🚨")
                st.warning("Este cliente tem uma alta probabilidade de cancelar o serviço.")
            else:
                st.success(f"**Previsão de Churn: {churn_prediction}**", icon="✅")
                st.info("Este cliente provavelmente não cancelará o serviço.")

            # Adiciona a previsão ao histórico para exibição
            history_entry = {
                "Plano Internacional": selected_plan_label,
                "Custo Diurno ($)": total_day_charge,
                "Custo Noturno ($)": total_eve_charge,
                "Chamadas ao Suporte": customer_service_calls,
                "Previsão de Churn": churn_prediction
            }
            st.session_state.prediction_history.insert(0, history_entry)

        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao conectar com a API. Verifique se o backend está rodando. Detalhes: {e}")

# --- EXIBIÇÃO DO HISTÓRICO DE PREVISÕES ---
if st.session_state.prediction_history:
    st.markdown("---")
    st.subheader("Histórico de Previsões Recentes")
    
    # Cria o DataFrame diretamente do histórico
    history_df = pd.DataFrame(st.session_state.prediction_history)
    st.dataframe(history_df)

