import ezdxf

def gerar_sapata_dxf(largura, comprimento, altura_base, altura_total, largura_pilar, comprimento_pilar):
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()

    # Layers
    doc.layers.new(name="linhas", dxfattribs={"color": 7})   # branco
    doc.layers.new(name="cotas", dxfattribs={"color": 1})    # vermelho
    doc.layers.new(name="textos", dxfattribs={"color": 7})   # branco

    # Base da planta
    base_x, base_y = 0, 0
    planta_offset = 10  # distância entre planta e corte

    # --- Planta ---
    pontos_sapata = [
        (base_x, base_y),
        (base_x + largura, base_y),
        (base_x + largura, base_y + comprimento),
        (base_x, base_y + comprimento),
    ]
    pontos_pilar = [
        (base_x + (largura - largura_pilar) / 2, base_y + (comprimento - comprimento_pilar) / 2),
        (base_x + (largura + largura_pilar) / 2, base_y + (comprimento - comprimento_pilar) / 2),
        (base_x + (largura + largura_pilar) / 2, base_y + (comprimento + comprimento_pilar) / 2),
        (base_x + (largura - largura_pilar) / 2, base_y + (comprimento + comprimento_pilar) / 2),
    ]
    msp.add_lwpolyline(pontos_sapata + [pontos_sapata[0]], dxfattribs={"layer": "linhas"})
    msp.add_lwpolyline(pontos_pilar + [pontos_pilar[0]], dxfattribs={"layer": "linhas"})
    for i in range(4):
        msp.add_line(pontos_sapata[i], pontos_pilar[i], dxfattribs={"layer": "linhas"})

    # --- Vista lateral (corte) ---
    corte_x = base_x + largura + planta_offset * 2
    pontos_corte = [
        (corte_x, base_y),
        (corte_x + largura, base_y),
        (corte_x + largura, base_y + altura_base),
        (corte_x + (largura + largura_pilar) / 2, base_y + altura_base),
        (corte_x + (largura + largura_pilar) / 2, base_y + altura_total),
        (corte_x + (largura - largura_pilar) / 2, base_y + altura_total),
        (corte_x + (largura - largura_pilar) / 2, base_y + altura_base),
        (corte_x, base_y + altura_base),
    ]
    msp.add_lwpolyline(pontos_corte + [pontos_corte[0]], dxfattribs={"layer": "linhas"})

    # --- Cotas planta ---
    def cota_horizontal(ponto1, ponto2, y):
        x1, _ = ponto1
        x2, _ = ponto2
        meio_x = (x1 + x2) / 2
        msp.add_line((x1, y), (x2, y), dxfattribs={"layer": "cotas"})
        msp.add_line((x1, y - 5), (x1, y + 5), dxfattribs={"layer": "cotas"})
        msp.add_line((x2, y - 5), (x2, y + 5), dxfattribs={"layer": "cotas"})
        msp.add_text(str(abs(int(x2 - x1))), dxfattribs={"height": 5, "layer": "cotas"}).set_placement((meio_x, y + 8))

    y_cota = base_y + comprimento + 20
    cota_horizontal((base_x, base_y), (base_x + largura, base_y), y_cota)
    cota_horizontal((pontos_pilar[0][0], base_y), (pontos_pilar[1][0], base_y), y_cota + 15)

    # --- Cotas corte (manuais) ---
    def cota_vertical(y1, y2, x):
        meio_y = (y1 + y2) / 2
        msp.add_line((x, y1), (x, y2), dxfattribs={"layer": "cotas"})
        msp.add_line((x - 5, y1), (x + 5, y1), dxfattribs={"layer": "cotas"})
        msp.add_line((x - 5, y2), (x + 5, y2), dxfattribs={"layer": "cotas"})
        msp.add_text(str(abs(int(y2 - y1))), dxfattribs={"height": 5, "layer": "cotas"}).set_placement((x + 8, meio_y))

    x_cota = corte_x + largura + 20
    cota_vertical(base_y, base_y + altura_base, x_cota)
    cota_vertical(base_y + altura_base, base_y + altura_total, x_cota + 15)

    # --- Título ---
    titulo_x = base_x + largura / 2
    titulo_y = base_y + comprimento + 40
    msp.add_text("S1", dxfattribs={"height": 12, "layer": "textos"}).set_placement((titulo_x, titulo_y), align='CENTER')

    # Salvar DXF
    doc.saveas("sapata.dxf")
