import streamlit as st
from utils.util import css
import numpy as np

st.set_page_config(
    page_icon="🤖", 
    layout="wide",
    page_title="EDU.IA")

# Adiciona CSS ao app
css()

st.title("EDU.IA🤖🧠")
st.write("Acesse as demos no menu lateral")

# Adiciona imagem de bem vendo ao app


st.image("./images/edu 01.png", use_column_width="Auto", width=350)

message = st.chat_message("assistant")
message.write("Hello human")
message.bar_chart(np.random.randn(30, 3))

st.balloons()