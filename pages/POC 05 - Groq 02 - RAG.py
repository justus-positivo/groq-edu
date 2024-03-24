import streamlit as st
import utils.util as util

st.set_page_config(
    page_icon="🥷", 
    layout="wide",
    page_title="GROQ.EDU POC 02")

# Adiciona CSS ao app
util.css()

st.title("Groq & RAG")
st.image("https://media.giphy.com/media/3o7TKz9bX9v6ZvzUxy/giphy.gif", use_column_width=True)