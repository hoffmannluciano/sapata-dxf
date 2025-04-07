import ezdxf
from io import BytesIO

def gerar_sapata_dxf(largura, comprimento, altura_ext, altura_int, altura_pilar):
    doc = ezdxf.new()
    msp = doc.modelspace()

    # Layers
    doc.layers.new(name="01", dxfattribs={"color": 7})  # Linhas
    doc.layers.new(name="02", dxfattribs={"color": 1})  # Cotas
    doc.layers.new(name="textos", dxfattribs={"color": 2})  # Título

    # Planta
    x0, y0 = 0, 0
    x1, y1 = largura, comprimento
    cx, cy = largura / 2, comprimento / 2
    pilar_dim = min(largura, comprimento) / 3
    px0, py0 = cx - pilar_dim / 2, cy - pilar_dim / 2
    px1, py1 = cx + pilar_dim / 2, cy + pilar_dim / 2

    msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True, dxfattribs={"layer": "01"})
    msp.add_lwpolyline([(px0, py0), (px1, py0), (px1, py1), (px0, py1)], close=True, dxfattribs={"layer": "01"})

    msp.add_line((x0, y0), (px0, py0), dxfattribs={"layer": "01"})
    msp.add_line((x1, y0), (px1, py0), dxfattribs={"layer": "01"})
    msp.add_line((x1, y1), (px1, py1), dxfattribs={"layer": "01"})
    msp.add_line((x0, y1), (px0, py1), dxfattribs={"layer": "01"})

    # Vista lateral
    espacamento = largura * 1.5
    base_x = espacamento
    base_y = 0

    top = base_y + altura_pilar + altura_ext
    inter = base_y + altura_pilar + altura_int

    msp.add_lwpolyline([
        (base_x, base_y + altura_pilar),
        (base_x + largura, base_y + altura_pilar),
        (base_x + largura, top),
        (base_x, top)
    ], close=True, dxfattribs={"layer": "01"})

    msp.add_lwpolyline([
        (base_x + largura / 3, base_y),
        (base_x + 2 * largura / 3, base_y),
        (base_x + 2 * largura / 3, base_y + altura_pilar),
        (base_x + largura / 3, base_y + altura_pilar)
    ], close=True, dxfattribs={"layer": "01"})

    # Cotas da planta
    desloc = 20
    msp.add_linear_dim(
        base=(0, -desloc),
        p1=(0, 0),
        p2=(largura, 0),
        angle=0,
        override={"dimtxsty": "STANDARD", "dimclrd": 1, "dimtxt": 5}
    ).render()

    msp.add_linear_dim(
        base=(-desloc, 0),
        p1=(0, 0),
        p2=(0, comprimento),
        angle=90,
        override={"dimtxsty": "STANDARD", "dimclrd": 1, "dimtxt": 5}
    ).render()

    # Cotas da vista lateral
    msp.add_linear_dim(
        base=(base_x + largura + 20, base_y + altura_pilar),
        p1=(base_x + largura, base_y + altura_pilar),
        p2=(base_x + largura, top),
        angle=90,
        override={"dimtxsty": "STANDARD", "dimclrd": 1, "dimtxt": 5}
    ).render()

    msp.add_linear_dim(
        base=(base_x + largura + 40, base_y),
        p1=(base_x + largura, base_y),
        p2=(base_x + largura, base_y + altura_pilar),
        angle=90,
        override={"dimtxsty": "STANDARD", "dimclrd": 1, "dimtxt": 5}
    ).render()

    # Título
    msp.add_text("S1", dxfattribs={"height": 12, "layer": "textos"}).set_location((0, comprimento + 20), align='LEFT')

    # Salvar em buffer
    buffer = BytesIO()
    doc.write(buffer)
    buffer.seek(0)
    return buffer
