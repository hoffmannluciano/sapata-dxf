import streamlit as st
from gerar_sapata import gerar_sapata_dxf

st.set_page_config(page_title="Gerador DXF - Sapata", layout="centered")

st.title("🧱 Gerador de Arquivo DXF - Sapata S1")

st.markdown("Preencha os dados abaixo para gerar a sapata:")

# Entradas do usuário
largura_sapata = st.number_input("Largura da sapata (cm)", value=100)
comprimento_sapata = st.number_input("Comprimento da sapata (cm)", value=100)
altura_base = st.number_input("Altura da base da sapata (cm)", value=25)
altura_total = st.number_input("Altura total da sapata (cm)", value=65)
largura_pilar = st.number_input("Largura do pilar (cm)", value=30)
comprimento_pilar = st.number_input("Comprimento do pilar (cm)", value=30)

# Botão para gerar DXF
if st.button("Gerar arquivo DXF"):
    try:
        gerar_sapata_dxf(
            largura_sapata,
            comprimento_sapata,
            altura_base,
            altura_total,
            largura_pilar,
            comprimento_pilar
        )

        with open("sapata.dxf", "rb") as file:
            st.success("✅ Arquivo DXF gerado com sucesso!")
            st.download_button(
                label="📥 Baixar DXF",
                data=file,
                file_name="sapata.dxf",
                mime="application/dxf"
            )

    except Exception as e:
        st.error(f"❌ Ocorreu um erro ao gerar o arquivo DXF:\n\n{e}")
