import streamlit as st
import requests
import uuid

# CONFIGURAÇÕES DA PÁGINA E URL DO BACKEND
BACKEND_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="MVP - Sistemas Inteligentes",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# TÍTULO E DESCRIÇÃO
st.title("SISTEMA DE PREVISÃO DE CHURN DE CLIENTES")
st.write(
    "Esta ferramenta utiliza um modelo de Machine Learning para prever se um cliente"
    " está propenso a cancelar seu serviço (churn). Preencha os dados abaixo para obter a previsão."
)
st.markdown("---")

# INICIALIZAÇÃO DO HISTÓRICO DE PREVISÕES
# st.session_state mantém o histórico entre as interações do usuário.
if 'prediction_history' not in st.session_state:
    st.session_state['prediction_history'] = []

# FORMULÁRIO DE ENTRADA DE DADOS
# st.form agrupa os widgets de entrada e só envia os dados quando o botão é pressionado.
with st.form("input_form"):
    st.header("Insira os dados do cliente:")

    # Nome do cliente
    client_name = st.text_input(
        "Nome do cliente",
        help="Insira o nome completo do cliente para identificação no histórico."
    )

    # Mapeamento de opções para os valores numéricos que a API espera (0 ou 1)
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
    submit_button = st.form_submit_button(label="Fazer Previsão", use_container_width=True)

# LÓGICA DE PREDIÇÃO E EXIBIÇÃO DO RESULTADO
if submit_button:
    # Dicionário com os dados para enviar à API (nomes das chaves são idênticos aos da API)
    feature_data = {
        "international_plan": international_plan_value,
        "total_day_charge": total_day_charge,
        "total_eve_charge": total_eve_charge,
        "customer_service_calls": customer_service_calls,
    }

    # Adiciona um spinner para melhorar a experiência do usuário em casos de lentidão
    with st.spinner("Analisando dados e fazendo previsão..."):
        try:
            # Faz a requisição POST para o backend
            response = requests.post(BACKEND_URL, json=feature_data)
            # Levanta um erro HTTP para respostas mal-sucedidas (código 4xx ou 5xx)
            response.raise_for_status() 

            # Extrai o resultado da resposta JSON
            prediction_result = response.json()
            churn_prediction = prediction_result.get("churn_prediction", "Erro na resposta")
            
            # Exibição do resultado
            st.markdown("---")
            st.subheader("Resultado da Previsão")
            if churn_prediction == "Sim":
                st.error(f"**Previsão de Churn: {churn_prediction}**", icon="🔴")
                st.warning("⚠️ Cliente com alta probabilidade de cancelar o serviço. Melhore a oferta!")
            else:
                st.success(f"**Previsão de Churn: {churn_prediction}**", icon="🟢")
                st.info("Cliente com baixa probabilidade de cancelar o serviço.")

            # Adiciona a previsão ao histórico para exibição
            history_entry = {
                # INSERÇÃO DE ID ÚNICO PARA PERMITIR A EXCLUSÃO SEGURA
                "id": str(uuid.uuid4()),
                "Nome do Cliente": client_name if client_name else "Não informado",
                "Plano Internacional": selected_plan_label,
                "Custo Diurno ($)": total_day_charge,
                "Custo Noturno ($)": total_eve_charge,
                "Chamadas ao Suporte": customer_service_calls,
                "Previsão de Churn": churn_prediction
            }
            st.session_state.prediction_history.insert(0, history_entry)

        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao conectar com a API. Verifique se o backend está rodando. Detalhes: {e}")

# DELETAR UMA ENTRADA DO HISTÓRICO
def delete_entry(entry_id):
    """Função para remover uma entrada do histórico com base em seu ID único."""
    st.session_state.prediction_history = [
        entry for entry in st.session_state.prediction_history if entry.get("id") != entry_id
    ]

# EXIBIÇÃO DO HISTÓRICO DE PREVISÕES
if st.session_state.prediction_history:
    st.markdown("---")
    st.subheader("Histórico de Previsões Recentes")
    
    # Cabeçalho da tabela do histórico
    cols = st.columns((2, 2, 2, 2, 2, 2, 1))
    headers = ["Nome do cliente", "Plano Intl.", "Custo diurno ($)", "Custo noturno ($)", "Chamadas ao suporte", "Previsão", "Deletar?"]
    for col, header in zip(cols, headers):
        col.write(f"**{header}**")

    # Itera sobre o histórico para exibir cada entrada com um botão de exclusão
    for entry in st.session_state.prediction_history:
        col1, col2, col3, col4, col5, col6, col7 = st.columns((2, 2, 2, 2, 2, 2, 1))
        with col1:
            st.write(entry["Nome do Cliente"])
        with col2:
            st.write(entry["Plano Internacional"])
        with col3:
            st.write(f"{entry['Custo Diurno ($)']:.2f}")
        with col4:
            st.write(f"{entry['Custo Noturno ($)']:.2f}")
        with col5:
            # CORRIGIDO: Garante que o número seja exibido como texto simples, sem cor.
            st.write(str(entry["Chamadas ao Suporte"]))
        with col6:
            # ALTERADO: Usa st.markdown com cores para remover o fundo.
            if entry["Previsão de Churn"] == "Sim":
                st.markdown(":red[Sim]")
            else:
                st.markdown(":green[Não]")
        with col7:
            # Botão para chamar a função de exclusão
            st.button("❌", key=f"del_{entry['id']}", on_click=delete_entry, args=(entry['id'],))
