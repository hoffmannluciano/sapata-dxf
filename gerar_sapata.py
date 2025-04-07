import ezdxf


def gerar_sapata_dxf(
    largura_sapata,
    comprimento_sapata,
    altura_base,
    altura_total,
    largura_pilar,
    comprimento_pilar
):
    doc = ezdxf.new()
    msp = doc.modelspace()

    # Definir layers
    doc.layers.new(name="01", dxfattribs={"color": 7})   # Linhas - branco
    doc.layers.new(name="02", dxfattribs={"color": 1})   # Cotas - vermelho
    doc.layers.new(name="textos", dxfattribs={"color": 2})  # Título - amarelo

    # Planta
    x0 = 0
    y0 = 0

    x1 = x0 + largura_sapata
    y1 = y0 + comprimento_sapata

    pilar_x0 = x0 + (largura_sapata - largura_pilar) / 2
    pilar_y0 = y0 + (comprimento_sapata - comprimento_pilar) / 2
    pilar_x1 = pilar_x0 + largura_pilar
    pilar_y1 = pilar_y0 + comprimento_pilar

    # Sapata
    msp.add_lwpolyline(
        [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)],
        dxfattribs={"layer": "01"}
    )

    # Pilar
    msp.add_lwpolyline(
        [(pilar_x0, pilar_y0), (pilar_x1, pilar_y0),
         (pilar_x1, pilar_y1), (pilar_x0, pilar_y1), (pilar_x0, pilar_y0)],
        dxfattribs={"layer": "01"}
    )

    # Linhas diagonais do pilar aos vértices da sapata
    msp.add_line((pilar_x0, pilar_y0), (x0, y0), dxfattribs={"layer": "01"})
    msp.add_line((pilar_x1, pilar_y0), (x1, y0), dxfattribs={"layer": "01"})
    msp.add_line((pilar_x1, pilar_y1), (x1, y1), dxfattribs={"layer": "01"})
    msp.add_line((pilar_x0, pilar_y1), (x0, y1), dxfattribs={"layer": "01"})

    # Cotas da planta (à esquerda e acima)
    def cota_horizontal(p1, p2, y_offset):
        msp.add_line((p1[0], p1[1] + y_offset), (p2[0], p2[1] + y_offset), dxfattribs={"layer": "02"})
        msp.add_line((p1[0], p1[1]), (p1[0], p1[1] + y_offset), dxfattribs={"layer": "02"})
        msp.add_line((p2[0], p2[1]), (p2[0], p2[1] + y_offset), dxfattribs={"layer": "02"})
        msp.add_text(
            f"{abs(p2[0] - p1[0]):.0f} cm",
            dxfattribs={"height": 10, "layer": "02"}
        ).set_pos(((p1[0] + p2[0]) / 2, p1[1] + y_offset + 5), align="CENTER")

    def cota_vertical(p1, p2, x_offset):
        msp.add_line((p1[0] + x_offset, p1[1]), (p2[0] + x_offset, p2[1]), dxfattribs={"layer": "02"})
        msp.add_line((p1[0], p1[1]), (p1[0] + x_offset, p1[1]), dxfattribs={"layer": "02"})
        msp.add_line((p2[0], p2[1]), (p2[0] + x_offset, p2[1]), dxfattribs={"layer": "02"})
        msp.add_text(
            f"{abs(p2[1] - p1[1]):.0f} cm",
            dxfattribs={"height": 10, "layer": "02"}
        ).set_pos((p1[0] + x_offset + 5, (p1[1] + p2[1]) / 2), align="LEFT")

    cota_horizontal((x0, y0), (x1, y0), y_offset=15)
    cota_vertical((x0, y0), (x0, y1), x_offset=-15)

    # Vista lateral
    deslocamento_x = largura_sapata + 60
    base_y = 0

    # Pontos principais
    topo = base_y + altura_total
    h_base = altura_base

    msp.add_lwpolyline(
        [(deslocamento_x, base_y),
         (deslocamento_x + largura_sapata, base_y),
         (deslocamento_x + largura_sapata, topo),
         (deslocamento_x, topo),
         (deslocamento_x, base_y)],
        dxfattribs={"layer": "01"}
    )

    # Linha horizontal da base
    msp.add_line(
        (deslocamento_x, base_y + h_base),
        (deslocamento_x + largura_sapata, base_y + h_base),
        dxfattribs={"layer": "01"}
    )

    # Cotas verticais da vista lateral (à direita)
    cota_vertical(
        (deslocamento_x + largura_sapata, base_y),
        (deslocamento_x + largura_sapata, base_y + h_base),
        x_offset=20
    )
    cota_vertical(
        (deslocamento_x + largura_sapata, base_y),
        (deslocamento_x + largura_sapata, base_y + altura_total),
        x_offset=40
    )

    # Título S1 no topo esquerdo da planta
    titulo_x = x0
    titulo_y = y1 + 40
    msp.add_text("S1", dxfattribs={"height": 12, "layer": "textos"}).set_pos((titulo_x, titulo_y), align='LEFT')

    # Salvar arquivo
    doc.saveas("sapata.dxf")
