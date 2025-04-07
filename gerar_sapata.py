import ezdxf
import os

def criar_documento():
    doc = ezdxf.new()

    # Layers
    doc.layers.add("01", color=7)  # Branco
    doc.layers.add("02", color=1)  # Vermelho
    doc.layers.add("textos", color=3)  # Verde para texto

    return doc

def adicionar_linhas_planta(msp, largura, comprimento, largura_pilar, comprimento_pilar):
    base_x, base_y = 0, 0
    x1, y1 = base_x, base_y
    x2, y2 = base_x + largura, base_y + comprimento

    # Contorno da sapata
    msp.add_lwpolyline([
        (x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)
    ], close=True, dxfattribs={"layer": "01"})

    # Contorno do pilar
    px1 = base_x + (largura - largura_pilar) / 2
    py1 = base_y + (comprimento - comprimento_pilar) / 2
    px2 = px1 + largura_pilar
    py2 = py1 + comprimento_pilar
    msp.add_lwpolyline([
        (px1, py1), (px2, py1), (px2, py2), (px1, py2), (px1, py1)
    ], close=True, dxfattribs={"layer": "01"})

    # Linhas diagonais
    msp.add_line((x1, y1), (px1, py1), dxfattribs={"layer": "01"})
    msp.add_line((x2, y1), (px2, py1), dxfattribs={"layer": "01"})
    msp.add_line((x2, y2), (px2, py2), dxfattribs={"layer": "01"})
    msp.add_line((x1, y2), (px1, py2), dxfattribs={"layer": "01"})

def adicionar_linhas_vista_lateral(msp, largura, altura_base, altura_total, deslocamento_x):
    base_x = deslocamento_x
    base_y = 0

    # Contorno externo da sapata em vista
    pontos = [
        (base_x, base_y),
        (base_x + largura, base_y),
        (base_x + largura, base_y + altura_total),
        (base_x, base_y + altura_total),
        (base_x, base_y)
    ]
    msp.add_lwpolyline(pontos, close=True, dxfattribs={"layer": "01"})

    # Linha horizontal separando a base
    msp.add_line(
        (base_x, base_y + altura_base),
        (base_x + largura, base_y + altura_base),
        dxfattribs={"layer": "01"}
    )

def adicionar_cotas_planta(msp, largura, comprimento):
    texto_altura = 10
    deslocamento = 20

    # Cota horizontal
    msp.add_line((0, -deslocamento), (largura, -deslocamento), dxfattribs={"layer": "02"})
    msp.add_line((0, 0), (0, -deslocamento), dxfattribs={"layer": "02"})
    msp.add_line((largura, 0), (largura, -deslocamento), dxfattribs={"layer": "02"})
    texto = msp.add_text(f"{largura} cm", dxfattribs={"height": texto_altura, "layer": "02"})
    texto.dxf.insert = (largura / 2, -deslocamento - 5)
    texto.dxf.align = "CENTER"

    # Cota vertical
    msp.add_line((-deslocamento, 0), (-deslocamento, comprimento), dxfattribs={"layer": "02"})
    msp.add_line((0, 0), (-deslocamento, 0), dxfattribs={"layer": "02"})
    msp.add_line((0, comprimento), (-deslocamento, comprimento), dxfattribs={"layer": "02"})
    texto = msp.add_text(f"{comprimento} cm", dxfattribs={"height": texto_altura, "layer": "02"})
    texto.dxf.insert = (-deslocamento - 5, comprimento / 2)
    texto.dxf.align = "CENTER"

def adicionar_cotas_vista_lateral(msp, altura_base, altura_total, deslocamento_x, largura):
    texto_altura = 10
    x = deslocamento_x + largura + 20

    # Cota altura base
    msp.add_line((x, 0), (x, altura_base), dxfattribs={"layer": "02"})
    msp.add_line((deslocamento_x + largura, 0), (x, 0), dxfattribs={"layer": "02"})
    msp.add_line((deslocamento_x + largura, altura_base), (x, altura_base), dxfattribs={"layer": "02"})
    texto = msp.add_text(f"{altura_base} cm", dxfattribs={"height": texto_altura, "layer": "02"})
    texto.dxf.insert = (x + 5, altura_base / 2)
    texto.dxf.align = "CENTER"

    # Cota altura total
    msp.add_line((x + 15, 0), (x + 15, altura_total), dxfattribs={"layer": "02"})
    msp.add_line((deslocamento_x + largura, 0), (x + 15, 0), dxfattribs={"layer": "02"})
    msp.add_line((deslocamento_x + largura, altura_total), (x + 15, altura_total), dxfattribs={"layer": "02"})
    texto = msp.add_text(f"{altura_total} cm", dxfattribs={"height": texto_altura, "layer": "02"})
    texto.dxf.insert = (x + 15 + 5, altura_total / 2)
    texto.dxf.align = "CENTER"

def adicionar_titulo(msp, largura):
    texto = msp.add_text("S1", dxfattribs={"height": 12, "layer": "textos"})
    texto.dxf.insert = (0, largura + 50)
    texto.dxf.align = 'LEFT'

def gerar_sapata_dxf(largura, comprimento, largura_pilar, comprimento_pilar, altura_base, altura_total):
    try:
        doc = criar_documento()
        msp = doc.modelspace()

        # Planta
        adicionar_linhas_planta(msp, largura, comprimento, largura_pilar, comprimento_pilar)
        adicionar_cotas_planta(msp, largura, comprimento)

        # Vista lateral
        deslocamento_x = largura + 60
        adicionar_linhas_vista_lateral(msp, largura, altura_base, altura_total, deslocamento_x)
        adicionar_cotas_vista_lateral(msp, altura_base, altura_total, deslocamento_x, largura)

        adicionar_titulo(msp, largura)

        caminho_arquivo = "sapata.dxf"
        doc.saveas(caminho_arquivo)
        return caminho_arquivo
    except Exception as e:
        return None
