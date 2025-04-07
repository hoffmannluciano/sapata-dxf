# app.py

import streamlit as st
from gerar_sapata import gerar_sapata_dxf

st.set_page_config(page_title="Gerador de DXF - Sapata", layout="centered")

st.title("Gerador de Arquivo DXF - Sapata de Fundação")

if st.button("Gerar arquivo DXF"):
    try:
        dxf_file = gerar_sapata_dxf()
        st.success("✅ Arquivo DXF gerado com sucesso!")
        st.download_button(
            label="📥 Baixar arquivo DXF",
            data=dxf_file,
            file_name="sapata.dxf",
            mime="application/dxf"
        )
    except Exception as e:
        st.error(f"❌ Ocorreu um erro ao gerar o arquivo DXF:\n\n{e}")
