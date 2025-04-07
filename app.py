import streamlit as st
from gerar_sapata import gerar_sapata_dxf

st.set_page_config(page_title="Gerador de Sapata DXF", layout="centered")

st.title("Gerador de Arquivo DXF - Sapata de Fundação")

st.markdown("Preencha os dados abaixo para gerar o desenho em DXF:")

# Entradas do usuário
sapata_largura = st.number_input("Dimensão X da sapata (cm)", min_value=10.0, value=100.0)
sapata_comprimento = st.number_input("Dimensão Y da sapata (cm)", min_value=10.0, value=120.0)
sapata_altura_ext = st.number_input("Altura externa da sapata (cm)", min_value=5.0, value=40.0)
sapata_altura_int = st.number_input("Altura interna da sapata (cm)", min_value=5.0, value=25.0)
altura_pilar = st.number_input("Comprimento do pilar acima da sapata (cm)", min_value=10.0, value=50.0)

# Botão para gerar o arquivo
if st.button("Gerar DXF"):
    try:
        dxf_file = gerar_sapata_dxf(
            sapata_largura=sapata_largura,
            sapata_comprimento=sapata_comprimento,
            sapata_altura_ext=sapata_altura_ext,
            sapata_altura_int=sapata_altura_int,
            altura_pilar=altura_pilar,
        )

        st.success("✅ Arquivo DXF gerado com sucesso!")

        # Botão para download do arquivo
        st.download_button(
            label="📥 Baixar arquivo DXF",
            data=dxf_file,
            file_name="sapata.dxf",
            mime="application/dxf"
        )

    except Exception as e:
        st.error(f"❌ Ocorreu um erro ao gerar o arquivo DXF:\n\n{e}")
