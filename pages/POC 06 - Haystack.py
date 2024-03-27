import streamlit as st
import utils.util as util
import os
from haystack import Pipeline, PredefinedPipeline




# Inicializa o cliente
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

def execute(url, pergunta):
    body()
    pipeline = Pipeline.from_template(PredefinedPipeline.CHAT_WITH_WEBSITE)
    with st.spinner('Executanto ...'):
        result = pipeline.run({
            "fetcher": {"urls": [url]},
            "prompt": {"query": pergunta}}
        )
        st.write(result["llm"]["replies"][0])

def body():
    st.title("Haystack")
    # Inicializa Page
    util.init_page()
    st.caption('Executanto teste com Haystack para responder uma pergunta sobre um site.')
    url = st.text_input('Digite a URL do site:', 'https://haystack.deepset.ai/overview/quick-start')
    pergunta = st.text_input('Digite a pergunta:', 'Which components do I need for a RAG pipeline?')
    st.button('Executar', on_click=execute, args=(url, pergunta))

body()
