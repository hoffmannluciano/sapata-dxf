import ezdxf
from ezdxf import units
from ezdxf.math import Vec2
from io import BytesIO

def gerar_sapata_dxf(dim_x, dim_y, altura_ext, altura_int, comp_pilar):
    # Inicializa o documento
    doc = ezdxf.new()
    doc.units = units.CENTIMETER
    msp = doc.modelspace()

    # Layers
    doc.layers.new(name="linhas", dxfattribs={"color": 7})  # branco
    doc.layers.new(name="cotas", dxfattribs={"color": 1})   # vermelho
    doc.layers.new(name="textos", dxfattribs={"color": 2})  # amarelo

    # Dimensões da sapata
    largura = dim_x
    comprimento = dim_y
    h_ext = altura_ext
    h_int = altura_int
    comp_pilar = comp_pilar

    # Pilar centrado
    largura_pilar = 30
    comprimento_pilar = 30

    x0 = 0
    y0 = 0
    x1 = largura
    y1 = comprimento

    xp0 = (largura - largura_pilar) / 2
    yp0 = (comprimento - comprimento_pilar) / 2
    xp1 = xp0 + largura_pilar
    yp1 = yp0 + comprimento_pilar

    # Planta - contorno da sapata
    msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True, dxfattribs={"layer": "linhas"})
    # Planta - contorno do pilar
    msp.add_lwpolyline([(xp0, yp0), (xp1, yp0), (xp1, yp1), (xp0, yp1)], close=True, dxfattribs={"layer": "linhas"})
    # Planta - diagonais
    msp.add_line((x0, y0), (xp0, yp0), dxfattribs={"layer": "linhas"})
    msp.add_line((x1, y0), (xp1, yp0), dxfattribs={"layer": "linhas"})
    msp.add_line((x1, y1), (xp1, yp1), dxfattribs={"layer": "linhas"})
    msp.add_line((x0, y1), (xp0, yp1), dxfattribs={"layer": "linhas"})

    # Vista lateral (direita)
    desloc_x = largura + 40
    base_y = 0
    topo_sapata = base_y + h_ext
    topo_pilar = topo_sapata + comp_pilar

    largura_vista = largura

    # Vista - contorno da sapata
    msp.add_lwpolyline([
        (desloc_x, base_y),
        (desloc_x + largura_vista, base_y),
        (desloc_x + largura_vista / 2 + 20, topo_sapata),
        (desloc_x + largura_vista / 2 - 20, topo_sapata)
    ], close=True, dxfattribs={"layer": "linhas"})

    # Vista - pilar
    msp.add_lwpolyline([
        (desloc_x + largura_vista / 2 - 15, topo_sapata),
        (desloc_x + largura_vista / 2 + 15, topo_sapata),
        (desloc_x + largura_vista / 2 + 15, topo_pilar),
        (desloc_x + largura_vista / 2 - 15, topo_pilar)
    ], close=True, dxfattribs={"layer": "linhas"})

    # Cotas planta (esquerda)
    def cota_horizontal(p1, p2, y):
        x0, _ = p1
        x1, _ = p2
        msp.add_line((x0, y), (x1, y), dxfattribs={"layer": "cotas"})
        msp.add_line((x0, y - 2), (x0, y + 2), dxfattribs={"layer": "cotas"})
        msp.add_line((x1, y - 2), (x1, y + 2), dxfattribs={"layer": "cotas"})
        msp.add_text(f"{abs(x1 - x0):.0f}cm", dxfattribs={"height": 6, "layer": "cotas"}).dxf.insert = ((x0 + x1) / 2 - 5, y + 2)

    def cota_vertical(p1, p2, x):
        _, y0 = p1
        _, y1 = p2
        msp.add_line((x, y0), (x, y1), dxfattribs={"layer": "cotas"})
        msp.add_line((x - 2, y0), (x + 2, y0), dxfattribs={"layer": "cotas"})
        msp.add_line((x - 2, y1), (x + 2, y1), dxfattribs={"layer": "cotas"})
        msp.add_text(f"{abs(y1 - y0):.0f}cm", dxfattribs={"height": 6, "layer": "cotas"}).dxf.insert = (x - 15, (y0 + y1) / 2)

    cota_horizontal((x0, y0), (x1, y0), y0 - 10)  # largura
    cota_vertical((x0, y0), (x0, y1), x0 - 10)    # comprimento

    # Cotas vista lateral (direita)
    cota_vertical((0, 0), (0, h_ext), desloc_x + largura_vista + 20)
    cota_vertical((0, h_ext), (0, h_ext + comp_pilar), desloc_x + largura_vista + 30)

    # Título
    msp.add_text("S1", dxfattribs={"height": 12, "layer": "textos", "halign": 0, "valign": 2}).dxf.insert = (0, comprimento + 20)

    # Salvar em memória
    buffer = BytesIO()
    doc.write(buffer)
    buffer.seek(0)
    return buffer
