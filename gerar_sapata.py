# gerar_sapata.py

import ezdxf
from io import BytesIO

def gerar_sapata_dxf(sapata_largura, sapata_comprimento, altura_externa, altura_interna, altura_pilar):
    doc = ezdxf.new()
    msp = doc.modelspace()

    # Layers
    doc.layers.add("01", color=7)   # branco
    doc.layers.add("02", color=1)   # vermelho
    doc.layers.add("textos", color=3)

    # Planta (esquerda)
    deslocamento_x = 0
    deslocamento_y = 0
    pilar_lado = 20  # cm (pilar 20x20)

    # Sapata
    x0, y0 = deslocamento_x, deslocamento_y
    x1, y1 = x0 + sapata_largura, y0 + sapata_comprimento

    msp.add_lwpolyline([
        (x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)
    ], dxfattribs={"layer": "01"})

    # Pilar
    px0 = x0 + (sapata_largura - pilar_lado) / 2
    py0 = y0 + (sapata_comprimento - pilar_lado) / 2
    px1 = px0 + pilar_lado
    py1 = py0 + pilar_lado

    msp.add_lwpolyline([
        (px0, py0), (px1, py0), (px1, py1), (px0, py1), (px0, py0)
    ], dxfattribs={"layer": "01"})

    # Diagonais da sapata até o pilar
    msp.add_line((x0, y0), (px0, py0), dxfattribs={"layer": "01"})
    msp.add_line((x1, y0), (px1, py0), dxfattribs={"layer": "01"})
    msp.add_line((x1, y1), (px1, py1), dxfattribs={"layer": "01"})
    msp.add_line((x0, y1), (px0, py1), dxfattribs={"layer": "01"})

    # Vista lateral (direita)
    dist_entre_vistas = sapata_largura + 100  # espaço entre planta e vista
    x_vl = deslocamento_x + dist_entre_vistas
    base_altura = deslocamento_y

    # Contorno da sapata
    msp.add_lwpolyline([
        (x_vl, base_altura),
        (x_vl + sapata_largura, base_altura),
        (x_vl + sapata_largura, base_altura + altura_externa),
        (x_vl + (sapata_largura - pilar_lado) / 2 + x_vl, base_altura + altura_interna),
        (x_vl + (sapata_largura + pilar_lado) / 2, base_altura + altura_interna),
        (x_vl + (sapata_largura + pilar_lado) / 2, base_altura + altura_interna + altura_pilar),
        (x_vl + (sapata_largura - pilar_lado) / 2 + x_vl, base_altura + altura_interna + altura_pilar),
        (x_vl + (sapata_largura - pilar_lado) / 2 + x_vl, base_altura + altura_interna),
        (x_vl, base_altura + altura_externa),
        (x_vl, base_altura)
    ], dxfattribs={"layer": "01"})

    # Título
    msp.add_text("S1", dxfattribs={
        "height": 12,
        "layer": "textos"
    }).set_placement((x0, y1 + 30), align='LEFT')

    # Cotas planta (à esquerda)
    msp.add_linear_dim(
        base=(x0 - 40, y0),
        p1=(x0, y0),
        p2=(x0, y1),
        angle=90,
        override={
            "dimtxsty": "Standard",
            "dimclrt": 1,
            "dimtxt": 10,
            "dimse1": 1,
            "dimse2": 1,
            "dimexe": 1
        },
        dxfattribs={"layer": "02"}
    ).render()

    msp.add_linear_dim(
        base=(x0, y0 - 40),
        p1=(x0, y0),
        p2=(x1, y0),
        angle=0,
        override={
            "dimtxsty": "Standard",
            "dimclrt": 1,
            "dimtxt": 10,
            "dimse1": 1,
            "dimse2": 1,
            "dimexe": 1
        },
        dxfattribs={"layer": "02"}
    ).render()

    # Cotas lateral (à direita)
    msp.add_linear_dim(
        base=(x_vl + sapata_largura + 40, base_altura),
        p1=(x_vl + sapata_largura, base_altura),
        p2=(x_vl + sapata_largura, base_altura + altura_externa),
        angle=90,
        override={
            "dimtxt": 10
        },
        dxfattribs={"layer": "02"}
    ).render()

    msp.add_linear_dim(
        base=(x_vl + sapata_largura + 70, base_altura),
        p1=(x_vl + sapata_largura, base_altura + altura_externa),
        p2=(x_vl + sapata_largura, base_altura + altura_externa + altura_pilar),
        angle=90,
        override={
            "dimtxt": 10
        },
        dxfattribs={"layer": "02"}
    ).render()

    # Exportar para buffer
    buffer = BytesIO()
    doc.write(buffer)
    buffer.seek(0)
    return buffer
