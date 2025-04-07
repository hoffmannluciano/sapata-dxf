# app.py

import streamlit as st
from gerar_sapata import gerar_sapata_dxf

st.set_page_config(page_title="Gerador de DXF - Sapata", layout="centered")

st.title("Gerador de Arquivo DXF - Sapata de Fundação")

st.subheader("Preencha os dados da sapata:")

largura = st.number_input("Largura da sapata (cm)", min_value=10.0, step=5.0)
comprimento = st.number_input("Comprimento da sapata (cm)", min_value=10.0, step=5.0)
h_ext = st.number_input("Altura externa da sapata (cm)", min_value=5.0, step=1.0)
h_int = st.number_input("Altura interna da sapata (cm)", min_value=5.0, step=1.0)
altura_pilar = st.number_input("Altura do pilar acima da sapata (cm)", min_value=5.0, step=1.0)

if st.button("Gerar DXF"):
    try:
        dxf_file = gerar_sapata_dxf(
            largura, comprimento, h_ext, h_int, altura_pilar
        )

        st.success("✅ Arquivo DXF gerado com sucesso!")
        st.download_button(
            label="📥 Baixar arquivo DXF",
            data=dxf_file,
            file_name="sapata.dxf",
            mime="application/dxf"
        )
    except Exception as e:
        st.error(f"❌ Ocorreu um erro ao gerar o arquivo DXF:\n\n{e}")

