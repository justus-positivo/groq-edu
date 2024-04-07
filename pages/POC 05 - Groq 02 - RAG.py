import streamlit as st
from typing import Generator
from groq import Groq
import utils.util as util
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import torch


st.set_page_config(
    page_icon="🥷", 
    layout="wide",
    page_title="GROQ.EDU RAG")

# Inicializa Page
util.init_page()

# Inicializa o cliente Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
pc = Pinecone(api_key=st.secrets["PINECONE_API_KEY"])

#carrega o index do pinecone
pinecone_index = pc.Index('semantic-search-fast')

#valida tip ode device
device = 'cuda' if torch.cuda.is_available() else 'cpu'

#carrega modelo
model_name = 'sentence-transformers/all-MiniLM-L6-v2'
model = SentenceTransformer(model_name, device=device)

# Adiciona imagem de bem vindo ao app
st.subheader("GROQ.EDU RAG Demo", divider="rainbow", anchor=False)

# Initialize chat history and selected model 2
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Como posso ajudar?"}]

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
    st.text("Dispositivo: " + device)
    st.text("Trasformer: " + model._get_name())
    st.text("Modelo: " + model_name)

# Exibir mensagens do chat 
for message in st.session_state.messages:
    avatar = './images/edu.webp' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Conteúdo da resposta do chat"""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

if prompt := st.chat_input("Digite seu prompt aqui..."):
    # monta prompt do usuário passado sempre para o inglês TODO: traduzir para inglês
    query = prompt
    # create the query vector
    xq = model.encode(query).tolist()
    # now query
    result = pinecone_index.query(vector=xq, top_k=5, include_values=False, include_metadata=True)
    for r in result['matches']:
        st.text(f"{round(r['score'], 2)}: {r['metadata']['text']}")    
    # monta prompt do sistema
    matched_info = ' '.join(item['metadata']['text'] for item in result['matches'])
    context = f"Information: {matched_info}"
    sys_prompt = f"""
    Instructions:
    - Be helpful and answer questions concisely. If you don't know the answer, say 'I don't know'
    - Utilize the context provided for accurate and specific information.
    - Incorporate your preexisting knowledge to enhance the depth and relevance of your response.
    - Cite your sources
    Context: {context}
    """
    st.session_state.messages.append({
        "role": "user", 
        "content": "{user_prompt} {sys_prompt}".format(user_prompt=prompt, sys_prompt=sys_prompt)
        })
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
            stream=True
        )

        with st.chat_message("assistant", avatar="./images/edu.webp"):
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