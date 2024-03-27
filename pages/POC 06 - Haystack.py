import streamlit as st
import utils.util as util
import os
from haystack import Pipeline, PredefinedPipeline


st.title("Haystack")
# Inicializa Page
util.init_page()

# Inicializa o cliente
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

def execute(url, pergunta):
    pipeline = Pipeline.from_template(PredefinedPipeline.CHAT_WITH_WEBSITE)
    try:
        with st.spinner('Executanto ...'):
            result = pipeline.run({
                "fetcher": {"urls": [url]},
                "prompt": {"query": pergunta}}
            )
            st.write(result["llm"]["replies"][0])
    except Exception as e:
        st.error(f"Erro: {e}")

    
st.caption('Executanto teste com Haystack para responder uma pergunta sobre um site.')
url = st.text_input('Digite a URL do site:', 'https://educacional.com.br/')
pergunta = st.text_input('Digite a pergunta:', 'Quais são as soluções educacionais?')
st.button('Executar', on_click=execute, args=(url, pergunta))
