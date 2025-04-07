import streamlit as st
import tempfile
import os
from gerar_sapata import gerar_sapata_dxf

st.title("Gerador de Sapata em DXF")

# Entradas do usuário
st.subheader("📐 Dados da Sapata")
largura_sapata = st.number_input("Largura da sapata (cm)", value=100)
comprimento_sapata = st.number_input("Comprimento da sapata (cm)", value=120)
altura_sapata = st.number_input("Altura da sapata (cm)", value=40)

st.subheader("📏 Dados do Pilar")
largura_pilar = st.number_input("Largura do pilar (cm)", value=30)
comprimento_pilar = st.number_input("Comprimento do pilar (cm)", value=40)
altura_pilar = st.number_input("Altura do pilar (cm)", value=25)

if st.button("🎯 Gerar DXF"):
    try:
        with tempfile.TemporaryDirectory() as tmpdirname:
            dxf_path = os.path.join(tmpdirname, "sapata.dxf")

            gerar_sapata_dxf(
                largura_sapata,
                comprimento_sapata,
                altura_sapata,
                largura_pilar,
                comprimento_pilar,
                altura_pilar,
                output_path=dxf_path
            )

            with open(dxf_path, "rb") as f:
                st.download_button(
                    "📥 Baixar DXF",
                    f,
                    file_name="sapata.dxf",
                    mime="application/dxf"
                )

    except Exception as e:
        st.error(f"❌ Ocorreu um erro ao gerar o arquivo DXF:\n\n{e}")
