# app.py
import streamlit as st
import traceback
from gerar_sapata import gerar_sapata_dxf

st.set_page_config(page_title="Gerador de Sapata DXF", layout="centered")
st.title("📐 Gerador de Sapata em DXF")

st.markdown("Preencha os dados abaixo para gerar o desenho DXF da sapata de fundação.")

# Entradas do usuário
with st.form("form_sapata"):
    col1, col2 = st.columns(2)

    with col1:
        largura_sapata = st.number_input("Largura da sapata (cm)", value=100)
        comprimento_sapata = st.number_input("Comprimento da sapata (cm)", value=120)
        altura_sapata = st.number_input("Altura da sapata (cm)", value=40)

    with col2:
        largura_pilar = st.number_input("Largura do pilar (cm)", value=30)
        comprimento_pilar = st.number_input("Comprimento do pilar (cm)", value=40)
        altura_pilar = st.number_input("Altura do pilar (cm)", value=25)

    gerar = st.form_submit_button("Gerar DXF")

if gerar:
    try:
        filepath = gerar_sapata_dxf(
            largura_sapata,
            comprimento_sapata,
            altura_sapata,
            largura_pilar,
            comprimento_pilar,
            altura_pilar,
        )
        with open(filepath, "rb") as f:
            st.success("✅ Arquivo DXF gerado com sucesso!")
            st.download_button("📥 Baixar arquivo DXF", f, file_name="sapata.dxf")
    except Exception:
        st.error("❌ Ocorreu um erro ao gerar o arquivo DXF:")
        st.code(traceback.format_exc())
