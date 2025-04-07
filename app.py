import streamlit as st
from gerar_sapata import gerar_sapata_dxf

st.set_page_config(page_title="Gerador de Sapata DXF", layout="centered")

st.title("Gerador de Arquivo DXF - Sapata de Fundação")

st.markdown("Preencha os dados abaixo para gerar o arquivo DXF:")

# Entradas do usuário
dim_x = st.number_input("Dimensão X da sapata (cm)", min_value=10.0, value=100.0, step=5.0)
dim_y = st.number_input("Dimensão Y da sapata (cm)", min_value=10.0, value=100.0, step=5.0)
altura_ext = st.number_input("Altura externa da sapata (cm)", min_value=5.0, value=40.0, step=1.0)
altura_int = st.number_input("Altura interna da sapata (cm)", min_value=5.0, value=25.0, step=1.0)
alt_pilar = st.number_input("Comprimento do pilar acima da sapata (cm)", min_value=5.0, value=40.0, step=1.0)

if st.button("Gerar DXF"):
    with st.spinner("Gerando arquivo DXF..."):
        try:
            dxf_file = gerar_sapata_dxf(
                largura=dim_x,
                comprimento=dim_y,
                altura_ext=altura_ext,
                altura_int=altura_int,
                altura_pilar=alt_pilar
            )
            st.success("✅ Arquivo DXF gerado com sucesso!")
            st.download_button(
                label="📥 Clique para baixar o arquivo DXF",
                data=dxf_file,
                file_name="sapata.dxf",
                mime="application/dxf"
            )
        except Exception as e:
            st.error(f"❌ Ocorreu um erro ao gerar o arquivo DXF:\n\n{e}")
