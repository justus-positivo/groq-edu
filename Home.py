import streamlit as st
import streamlit_authenticator as stauth
import yaml
import time
import utils.util as util

from yaml.loader import SafeLoader

st.set_page_config(
    page_icon="🤖", 
    layout="wide",
    page_title="EDU.IA")

# Inicializa página
# util.init_page(False)


with open('./.streamlit/config.yaml', 'r') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Layout com 2 colunas
col1, col2 = st.columns([1,5])

with col1:
    # Adiciona imagem de bem vendo ao app
    st.image("./images/edu.webp", use_column_width="Auto", width=100)

with col2:
    # Adiciona título
    st.subheader("DIGITAL.EDU Labs 🧪", divider="rainbow", anchor=False)
    st.write("Bem vindo ao DIGITAL.EDU Labs")

#função para criar hash
def hash_passwords(pwd: str):
    # hash passwords
    hashed_passwords = stauth.Hasher([pwd]).generate()
    st.write(hashed_passwords)

# criar autenticação
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# form de autenticação
authenticator.login(fields={'Form name':'Acesso', 'Username':'Email', 'Password':'Senha', 'Login':'Login'})

# info
if st.session_state["authentication_status"]: 
    st.write('Usuário autenticado - acessar menu lateral')
elif st.session_state["authentication_status"] is False:
    st.error('Usuário/Senha incorretos')
elif st.session_state["authentication_status"] is None:
    st.warning('Entre com suas credenciais para acessar')


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
    # st.sidebar.page_link("pages/user.py", label="Your profile")
    # if st.session_state.role in ["admin", "super-admin"]:
    #     st.sidebar.page_link("pages/admin.py", label="Manage users")
    #     st.sidebar.page_link(
    #         "pages/super-admin.py",
    #         label="Manage admin access",
    #         disabled=st.session_state.role != "super-admin",
    #     )
    st.sidebar.button("Logout", on_click=authenticator.logout)


# Menu lateral para usuários não autenticados
def unauthenticated_menu():
    st.sidebar.write("Faça login para acessar o app")

# Menu lateral
def menu():
    if "authentication_status" not in st.session_state or st.session_state.authentication_status is None or st.session_state.authentication_status is False:
        unauthenticated_menu()
    else:
        authenticated_menu()

#executa menu lateral
menu()