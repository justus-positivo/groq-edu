import streamlit as st

def css():
    # CSS para estilizar o chat
    with open('./css/main.css') as f:
        css = f.read()
    # Adiciona o CSS ao app
    #st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Função para adicionar emoji inicial
def icon(emoji: str):
    st.write(f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',unsafe_allow_html=True,)