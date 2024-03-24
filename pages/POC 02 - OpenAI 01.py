import streamlit as st
from openai import OpenAI
import utils.util as util

st.set_page_config(
    page_icon="🥷", 
    layout="wide",
    page_title="OPENAI.EDU POC 01")

# Adiciona CSS ao app
util.css()

# Adiciona imagem de bem vindo ao app
st.subheader("OPENAI.EDU Demo - v1", divider="rainbow", anchor=False)

# Inicializa o cliente Groq
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize chat history and selected model 2
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

# modelos do demo
models = {
    "gpt-3.5-turbo": {"name": "GPT 3.5 Turbo", "tokens": 8192, "developer": "OpenAi"},
    "gpt-4-turbo-preview": {"name": "GPT 4.0 Turbo Preview", "tokens": 8192, "developer": "OpenAi"},
}

model_option = st.selectbox(
    "Modelo:",
    options=list(models.keys()),
    format_func=lambda x: models[x]["name"],
    index=0 
)

# Detecta mudança do modelo e limpe chat
if st.session_state.selected_model != model_option:
    st.session_state.messages = []
    st.session_state.selected_model = model_option

# Exibir mensagens do chat 
for message in st.session_state.messages:
    avatar = './images/edu 01.png' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


if prompt := st.chat_input("Digite seu prompt aqui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar='👨‍💻'):
        st.markdown(prompt)

    # Resposta da API Groq
    try:
        chat_completion = client.chat.completions.create(
            model=model_option,
            messages=[
                {
                    "role": m["role"],
                    "content": m["content"]
                }
                for m in st.session_state.messages
            ]
        )
        msg = chat_completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
    except Exception as e:
        st.error(e, icon="🚨")