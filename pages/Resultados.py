import streamlit.components.v1 as components
import streamlit as st
import utils.util as util

# Adiciona CSS ao app
util.css()

st.title("Resultados")
st.write("Aqui você encontra alguns resultados das POCs até agora")

st.subheader("POC Bedrock", divider="blue", anchor=False)
components.iframe("https://doc.clickup.com/464509/p/h/e5kx-489733/1de15d05618997f", height=500)