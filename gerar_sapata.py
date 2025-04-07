import ezdxf
import io

def gerar_sapata_dxf(largura_sapata, comprimento_sapata, altura_sapata,
                     largura_pilar, comprimento_pilar, altura_pilar):
    doc = ezdxf.new(dxfversion="R2010")
    msp = doc.modelspace()

    # Layers
    doc.layers.new(name="linhas", dxfattribs={"color": 7})     # branco
    doc.layers.new(name="cotas", dxfattribs={"color": 1})      # vermelho
    doc.layers.new(name="textos", dxfattribs={"color": 5})     # azul

    # Planta da sapata
    x0, y0 = 0, 0
    x1, y1 = largura_sapata, comprimento_sapata
    msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True, dxfattribs={"layer": "linhas"})

    # Pilar centralizado
    xp0 = (largura_sapata - largura_pilar) / 2
    yp0 = (comprimento_sapata - comprimento_pilar) / 2
    xp1 = xp0 + largura_pilar
    yp1 = yp0 + comprimento_pilar
    msp.add_lwpolyline([(xp0, yp0), (xp1, yp0), (xp1, yp1), (xp0, yp1)], close=True, dxfattribs={"layer": "linhas"})

    # Linhas diagonais
    msp.add_line((x0, y0), (xp0, yp0), dxfattribs={"layer": "linhas"})
    msp.add_line((x1, y0), (xp1, yp0), dxfattribs={"layer": "linhas"})
    msp.add_line((x1, y1), (xp1, yp1), dxfattribs={"layer": "linhas"})
    msp.add_line((x0, y1), (xp0, yp1), dxfattribs={"layer": "linhas"})

    # Vista lateral ao lado (com espaçamento horizontal)
    deslocamento = largura_sapata + 40
    msp.add_lwpolyline([
        (deslocamento, 0),
        (deslocamento + largura_sapata, 0),
        (deslocamento + largura_sapata, altura_sapata),
        (deslocamento, altura_sapata)
    ], close=True, dxfattribs={"layer": "linhas"})

    # Pilar na vista lateral
    x_p = deslocamento + (largura_sapata - largura_pilar) / 2
    msp.add_lwpolyline([
        (x_p, altura_sapata),
        (x_p + largura_pilar, altura_sapata),
        (x_p + largura_pilar, altura_sapata + altura_pilar),
        (x_p, altura_sapata + altura_pilar)
    ], close=True, dxfattribs={"layer": "linhas"})

    # Cotas (simples, apenas para testes)
    msp.add_text("S1", dxfattribs={"height": 12, "layer": "textos"}).set_dxf_attrib("insert", (0, comprimento_sapata + 20))

    # Salva em memória
    buffer = io.BytesIO()
    doc.write(buffer)
    buffer.seek(0)
    return buffer
