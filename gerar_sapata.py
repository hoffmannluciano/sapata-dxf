import ezdxf

def gerar_sapata_dxf(
    caminho_saida,
    sapata_largura,
    sapata_comprimento,
    pilar_largura,
    pilar_comprimento,
    base_largura,
    topo_largura,
    altura_base,
    altura_chanfro,
    altura_pedestal
):
    doc = ezdxf.new()
    msp = doc.modelspace()

    # Layers
    doc.layers.add(name="01", color=7)  # Linhas (branco)
    doc.layers.add(name="02", color=1)  # Cotas (vermelho)
    doc.layers.add(name="textos", color=7)  # Título

    # PLANTA
    x_offset = 0
    y_offset = 0

    def retangulo(x, y, largura, comprimento):
        return [
            (x, y),
            (x + largura, y),
            (x + largura, y + comprimento),
            (x, y + comprimento),
            (x, y)
        ]

    sapata_pts = retangulo(x_offset, y_offset, sapata_largura, sapata_comprimento)
    pilar_x = x_offset + (sapata_largura - pilar_largura) / 2
    pilar_y = y_offset + (sapata_comprimento - pilar_comprimento) / 2
    pilar_pts = retangulo(pilar_x, pilar_y, pilar_largura, pilar_comprimento)

    msp.add_lwpolyline(sapata_pts, dxfattribs={"layer": "01"})
    msp.add_lwpolyline(pilar_pts, dxfattribs={"layer": "01"})

    # Diagonais da planta
    for i in range(4):
        msp.add_line(sapata_pts[i], pilar_pts[i], dxfattribs={"layer": "01"})

    # COTAS PLANTA
    cotas = doc.blocks.new(name="DIM_BLOCK")
    dimstyle = doc.dimstyles.get("Standard")
    dimstyle.dxf.dimtxt = 5  # Tamanho do texto

    def cota_horizontal(p1, p2, y_cota):
        msp.add_linear_dim(
            base=(0, 0),
            p1=p1,
            p2=p2,
            location=(0, y_cota),
            override={"dimtxt": 5, "dimclrt": 1},
        ).render()

    def cota_vertical(p1, p2, x_cota):
        msp.add_linear_dim(
            base=(0, 0),
            p1=p1,
            p2=p2,
            location=(x_cota, 0),
            rotation=90,
            override={"dimtxt": 5, "dimclrt": 1},
        ).render()

    # Cotas da planta
    cota_horizontal((0, 0), (sapata_largura, 0), y_offset - 10)
    cota_vertical((0, 0), (0, sapata_comprimento), x_offset - 10)

    # VISTA LATERAL
    espaco_entre_vistas = sapata_largura * 2  # afastamento horizontal
    x0 = x_offset + espaco_entre_vistas
    y0 = y_offset

    # Base da sapata (parte inferior)
    base_esq = x0
    base_dir = x0 + base_largura
    topo_esq = x0 + (base_largura - topo_largura) / 2
    topo_dir = topo_esq + topo_largura

    y_base = y0
    y_topo_chanfro = y_base + altura_base
    y_topo_pedestal = y_topo_chanfro + altura_chanfro

    # Polilinha da vista lateral
    vista_pts = [
        (base_esq, y_base),
        (topo_esq, y_topo_chanfro),
        (topo_esq, y_topo_pedestal),
        (topo_dir, y_topo_pedestal),
        (topo_dir, y_topo_chanfro),
        (base_dir, y_base),
        (base_esq, y_base)
    ]

    msp.add_lwpolyline(vista_pts, dxfattribs={"layer": "01"})

    # Cotas da vista lateral
    cota_vertical((base_dir + 10, y_base), (base_dir + 10, y_topo_chanfro), base_dir + 15)
    cota_vertical((base_dir + 10, y_topo_chanfro), (base_dir + 10, y_topo_pedestal), base_dir + 15)

    # TÍTULO
    titulo_x = x_offset
    titulo_y = max(y_topo_pedestal, sapata_comprimento) + 15
    msp.add_text("S1", dxfattribs={"height": 12, "layer": "textos"}).set_location((titulo_x, titulo_y), align='LEFT')

    doc.saveas(caminho_saida)
