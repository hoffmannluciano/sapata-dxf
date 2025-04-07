import streamlit as st
import tempfile
from gerar_sapata import gerar_sapata_dxf

st.set_page_config(page_title="Gerador de Sapata DXF", layout="centered")

st.title("Gerador de Desenho DXF - Sapata")

with st.form("formulario_sapata"):
    st.subheader("🔹 Planta da Sapata")
    sapata_largura = st.number_input("Largura da Sapata (cm)", value=90)
    sapata_comprimento = st.number_input("Comprimento da Sapata (cm)", value=95)
    pilar_largura = st.number_input("Largura do Pilar (cm)", value=20)
    pilar_comprimento = st.number_input("Comprimento do Pilar (cm)", value=30)

    st.subheader("🔹 Vista Lateral")
    base_largura = st.number_input("Base da Sapata (cm)", value=90)
    topo_largura = st.number_input("Topo da Sapata (cm)", value=25)
    altura_base = st.number_input("Altura da Base (cm)", value=25)
    altura_chanfro = st.number_input("Altura do Chanfro (cm)", value=15)
    altura_pedestal = st.number_input("Altura do Pedestal (cm)", value=100)

    submit = st.form_submit_button("Gerar DXF")

if submit:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as tmpfile:
        gerar_sapata_dxf(
            caminho_saida=tmpfile.name,
            sapata_largura=sapata_largura,
            sapata_comprimento=sapata_comprimento,
            pilar_largura=pilar_largura,
            pilar_comprimento=pilar_comprimento,
            base_largura=base_largura,
            topo_largura=topo_largura,
            altura_base=altura_base,
            altura_chanfro=altura_chanfro,
            altura_pedestal=altura_pedestal
        )

        st.success("✅ Arquivo DXF gerado com sucesso!")
        st.download_button("📥 Baixar Arquivo DXF", data=open(tmpfile.name, "rb"),
                           file_name="sapata.dxf", mime="application/dxf")
