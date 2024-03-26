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

#valida sessão do usuário
def check_session():
    if "authentication_status" not in st.session_state or st.session_state.authentication_status is None or st.session_state.authentication_status is False:
        #envia para página de login
        st.switch_page("./Home.py")

# Função para inicializar a página
def init_page():
    # Adiciona CSS ao app
    css()
    # valida login
    check_session()
    