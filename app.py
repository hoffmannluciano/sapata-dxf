# app.py

import streamlit as st
from gerar_sapata import gerar_sapata_dxf

st.set_page_config(page_title="Gerador de Sapata DXF", layout="centered")

st.title("Gerador de Arquivo DXF - Sapata de Fundação")

with st.form("sapata_form"):
    st.subheader("Informe os dados da sapata:")
    sapata_largura = st.number_input("Dimensão X da sapata (cm)", min_value=10.0, step=5.0)
    sapata_comprimento = st.number_input("Dimensão Y da sapata (cm)", min_value=10.0, step=5.0)
    altura_externa = st.number_input("Altura externa da sapata (cm)", min_value=5.0, step=1.0)
    altura_interna = st.number_input("Altura interna da sapata (cm)", min_value=5.0, step=1.0)
    altura_pilar = st.number_input("Comprimento do pilar acima da sapata (cm)", min_value=5.0, step=1.0)

    submitted = st.form_submit_button("Gerar DXF")

if submitted:
    try:
        dxf_file = gerar_sapata_dxf(
            sapata_largura,
            sapata_comprimento,
            altura_externa,
            altura_interna,
            altura_pilar
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
