import streamlit as st
from typing import Generator
from groq import Groq

st.set_page_config(page_icon="🥷", layout="wide",
                   page_title="GROQ.EDU Demo")

# CSS para estilizar o chat
with open('./css/main.css') as f:
    css = f.read()

# Adiciona o CSS ao app
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Função para adicionar emoji inicial
def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


icon("🥷")

st.subheader("GROQ.EDU Demo", divider="rainbow", anchor=False)

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"],
)

# Initialize chat history and selected model 2
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

# modelos do demo
models = {
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
    "llama2-70b-4096": {"name": "LLaMA2-70b-chat", "tokens": 4096, "developer": "Meta"},
    "gemma-7b-it": {"name": "Gemma-7b-it", "tokens": 8192, "developer": "Google"}
}

# Layout com 2 colunas
col1, col2 = st.columns(2)

with col1:
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

max_tokens_range = models[model_option]["tokens"]

with col2:
    # slider com tamanho máximo de tokens com base no modelo
    max_tokens = st.slider(
        "Máximo de Tokens:",
        min_value=512, 
        max_value=max_tokens_range,
        # valor padrão
        value=min(32768, max_tokens_range),
        step=512,
        help=f"Ajuste o número máximo de tokens (palavras) para a resposta. Máximo para o modelo selecionado: {max_tokens_range}"
    )

# Exibir mensagens do chat 
for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Conteúdo da resposta do chat"""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


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
            ],
            max_tokens=max_tokens,
            stream=True
        )

        with st.chat_message("assistant", avatar="🤖"):
            chat_responses_generator = generate_chat_responses(chat_completion)
            full_response = st.write_stream(chat_responses_generator)
    except Exception as e:
        st.error(e, icon="🚨")

    # Resposta completa a session_state.messages
    if isinstance(full_response, str):
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response})
    else:
        # Caso Full_Response não seja string
        combined_response = "\n".join(str(item) for item in full_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": combined_response})