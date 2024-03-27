import streamlit as st

def css():
    # CSS para estilizar o chat
    with open('./css/main.css') as f:
        css = f.read()
    # Adiciona o CSS ao app
    # st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Função para adicionar emoji inicial
def icon(emoji: str):
    st.write(f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',unsafe_allow_html=True,)

#valida sessão do usuário
def check_session():
    if "authentication_status" not in st.session_state or st.session_state.authentication_status is None or st.session_state.authentication_status is False:
        #envia para página de login
        st.switch_page("./Home.py")

# Função para inicializar a página
def init_page(show_menu=True):
    # Adiciona CSS ao app
    css()
    # valida login
    check_session()
    #executa menu lateral
    if show_menu:
        menu()

#volta para home
def click_home():
    st.experimental_rerun()

# Menu lateral para usuários autenticados
def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.title(st.session_state.name)
    st.sidebar.page_link("./pages/POC 01 - Groq 01.py", label="POC 01 - Groq")
    st.sidebar.page_link("./pages/POC 02 - OpenAI 01.py", label="POC 02 - OpenAI")
    st.sidebar.page_link("./pages/POC 03 - Gemini 01.py", label="POC 03 - Gemini 01")
    st.sidebar.page_link("./pages/POC 04 - AWS Bedrock.py", label="POC 04 - AWS Bedrock")
    st.sidebar.page_link("./pages/POC 05 - Groq 02 - RAG.py", label="POC 05 - Groq 02 - RAG")
    st.sidebar.page_link("./pages/POC 06 - Haystack.py", label="POC 06 - Haystack")
    st.sidebar.button("Home", on_click=click_home)


# Menu lateral para usuários não autenticados
def unauthenticated_menu():
    st.sidebar.write("Faça login para acessar o app")

# Menu lateral
def menu():
    if "authentication_status" not in st.session_state or st.session_state.authentication_status is None or st.session_state.authentication_status is False:
        unauthenticated_menu()
    else:
        authenticated_menu()
    