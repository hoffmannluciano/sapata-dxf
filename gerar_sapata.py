# gerar_sapata.py

import ezdxf
from io import BytesIO

def gerar_sapata_dxf(largura, comprimento, h_ext, h_int, altura_pilar):
    doc = ezdxf.new()
    msp = doc.modelspace()

    # Geometria base
    sapata = [(0, 0), (largura, 0), (largura, comprimento), (0, comprimento), (0, 0)]
    pilar = [(largura/2 - 10, comprimento/2 - 10), (largura/2 + 10, comprimento/2 - 10),
             (largura/2 + 10, comprimento/2 + 10), (largura/2 - 10, comprimento/2 + 10),
             (largura/2 - 10, comprimento/2 - 10)]

    # Desenhar planta
    msp.add_lwpolyline(sapata)
    msp.add_lwpolyline(pilar)

    # Desenhar vista lateral da sapata (contorno simplificado)
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
    ])

    # Título da sapata
    msp.add_text("S1", dxfattribs={"height": 12}).set_placement((0, comprimento + 30), align='LEFT')

    # Gerar arquivo para buffer
    buffer = BytesIO()
    doc.write(buffer)
    buffer.seek(0)
    return buffer
