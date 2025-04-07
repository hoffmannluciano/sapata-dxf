import ezdxf

def gerar_sapata_dxf(
    sapata_largura,
    sapata_comprimento,
    sapata_altura,
    pilar_largura,
    pilar_comprimento,
    pilar_altura,
    output_path="sapata.dxf"
):
    doc = ezdxf.new()
    msp = doc.modelspace()

    # Layers
    doc.layers.add(name="01", color=7)  # branco
    doc.layers.add(name="02", color=1)  # vermelho
    doc.layers.add(name="03", color=2)  # verde para textos

    # Planta da sapata
    p1 = (0, 0)
    p2 = (sapata_largura, 0)
    p3 = (sapata_largura, sapata_comprimento)
    p4 = (0, sapata_comprimento)

    planta = [p1, p2, p3, p4, p1]
    msp.add_lwpolyline(planta, dxfattribs={"layer": "01", "closed": True})

    # Pilar na planta
    px1 = (sapata_largura / 2 - pilar_largura / 2, sapata_comprimento / 2 - pilar_comprimento / 2)
    px2 = (px1[0] + pilar_largura, px1[1])
    px3 = (px2[0], px2[1] + pilar_comprimento)
    px4 = (px1[0], px3[1])
    pilar_planta = [px1, px2, px3, px4, px1]
    msp.add_lwpolyline(pilar_planta, dxfattribs={"layer": "01", "closed": True})

    # Linhas diagonais (da sapata ao pilar)
    for sap, pil in zip([p1, p2, p3, p4], [px1, px2, px3, px4]):
        msp.add_line(sap, pil, dxfattribs={"layer": "01"})

    # Vista lateral - deslocamento em x
    dx = sapata_largura + 60

    # Sapata em vista lateral
    v1 = (dx, 0)
    v2 = (dx + sapata_largura, 0)
    v3 = (dx + sapata_largura, sapata_altura)
    v4 = (dx, sapata_altura)
    msp.add_lwpolyline([v1, v2, v3, v4, v1], dxfattribs={"layer": "01", "closed": True})

    # Pilar em vista lateral
    pv1 = (dx + sapata_largura / 2 - pilar_largura / 2, sapata_altura)
    pv2 = (pv1[0] + pilar_largura, sapata_altura)
    pv3 = (pv2[0], sapata_altura + pilar_altura)
    pv4 = (pv1[0], sapata_altura + pilar_altura)
    msp.add_lwpolyline([pv1, pv2, pv3, pv4, pv1], dxfattribs={"layer": "01", "closed": True})

    # Cotas planta
    texto_altura = 6

    def cota_horizontal(p1, p2, y):
        msp.add_line(p1, (p1[0], y), dxfattribs={"layer": "02"})
        msp.add_line(p2, (p2[0], y), dxfattribs={"layer": "02"})
        msp.add_line((p1[0], y), (p2[0], y), dxfattribs={"layer": "02"})
        meio = ((p1[0] + p2[0]) / 2, y + 2)
        msp.add_text(
            f"{abs(p2[0] - p1[0]):.0f} cm",
            dxfattribs={"height": texto_altura, "layer": "02"}
        ).set_placement(meio, align="MIDDLE_CENTER")

    def cota_vertical(p1, p2, x):
        msp.add_line(p1, (x, p1[1]), dxfattribs={"layer": "02"})
        msp.add_line(p2, (x, p2[1]), dxfattribs={"layer": "02"})
        msp.add_line((x, p1[1]), (x, p2[1]), dxfattribs={"layer": "02"})
        meio = (x - 2, (p1[1] + p2[1]) / 2)
        msp.add_text(
            f"{abs(p2[1] - p1[1]):.0f} cm",
            dxfattribs={"height": texto_altura, "layer": "02"}
        ).set_placement(meio, align="MIDDLE_CENTER")

    cota_horizontal((0, 0), (sapata_largura, 0), -10)
    cota_vertical((0, 0), (0, sapata_comprimento), -10)

    # Cotas da vista lateral (apenas alturas)
    cota_vertical((dx, 0), (dx, sapata_altura), dx + sapata_largura + 10)
    cota_vertical((dx, sapata_altura), (dx, sapata_altura + pilar_altura), dx + sapata_largura + 10)

    # Título "S1"
    pos_x = sapata_largura / 2
    pos_y = max(sapata_comprimento, sapata_altura + pilar_altura) + 15
    msp.add_text(
        "S1",
        dxfattribs={"height": 12, "layer": "03"}
    ).set_placement((pos_x, pos_y), align="MIDDLE_CENTER")

    # Salvar
    doc.saveas(output_path)
