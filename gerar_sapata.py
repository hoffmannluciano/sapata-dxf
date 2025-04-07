# gerar_sapata.py

import ezdxf
from io import BytesIO

def gerar_sapata_dxf():
    doc = ezdxf.new()
    msp = doc.modelspace()

    # Parâmetros fixos usados na versão V0.2
    largura = 100
    comprimento = 150
    h_ext = 40
    h_int = 25
    altura_pilar = 50

    # Criar layers
    doc.layers.new(name="01", dxfattribs={"color": 7})     # Linhas em branco
    doc.layers.new(name="02", dxfattribs={"color": 1})     # Cotas em vermelho
    doc.layers.new(name="textos", dxfattribs={"color": 7}) # Texto do título

    # Planta da sapata
    msp.add_lwpolyline([
        (0, 0), (largura, 0), (largura, comprimento), (0, comprimento), (0, 0)
    ], dxfattribs={"layer": "01"})

    # Pilar na planta
    msp.add_lwpolyline([
        (largura/2 - 10, comprimento/2 - 10),
        (largura/2 + 10, comprimento/2 - 10),
        (largura/2 + 10, comprimento/2 + 10),
        (largura/2 - 10, comprimento/2 + 10),
        (largura/2 - 10, comprimento/2 - 10),
    ], dxfattribs={"layer": "01"})

    # Cotas da planta – acima e à esquerda
    msp.add_aligned_dim(
        p1=(0, comprimento + 10),
        p2=(largura, comprimento + 10),
        distance=10,
        override={"dimclrd": 1}
    ).render()

    msp.add_aligned_dim(
        p1=(-10, 0),
        p2=(-10, comprimento),
        distance=10,
        override={"dimclrd": 1}
    ).render()

    # Vista lateral
    base_x = largura + 100
    msp.add_lwpolyline([
        (base_x, 0),
        (base_x + largura, 0),
        (base_x + largura, h_ext),
        (base_x + largura/2 + 10, h_ext),
        (base_x + largura/2 + 10, h_ext + altura_pilar),
        (base_x + largura/2 - 10, h_ext + altura_pilar),
        (base_x + largura/2 - 10, h_ext),
        (base_x, h_ext),
        (base_x, 0)
    ], dxfattribs={"layer": "01"})

    # Cotas da vista lateral – à direita
    msp.add_aligned_dim(
        p1=(base_x + largura + 10, 0),
        p2=(base_x + largura + 10, h_int),
        distance=10,
        override={"dimclrd": 1}
    ).render()

    msp.add_aligned_dim(
        p1=(base_x + largura + 20, 0),
        p2=(base_x + largura + 20, h_ext),
        distance=10,
        override={"dimclrd": 1}
    ).render()

    # Título “S1” no topo da planta
    msp.add_text("S1", dxfattribs={
        "height": 12,
        "layer": "textos"
    }).set_placement((0, comprimento + 30), align='LEFT')

    # Gerar buffer para download
    buffer = BytesIO()
    doc.write(buffer)
    buffer.seek(0)
    return buffer
