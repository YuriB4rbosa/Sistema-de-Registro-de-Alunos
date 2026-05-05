import os
import datetime


def gerar_ficha_pdf(dados_aluno, output_path):
    """
    Gera ficha de matrícula em PDF.
    dados_aluno: tupla (id, name, email, tel, sexo, data, end, curso, foto)
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Table, TableStyle, HRFlowable,
                                    Image as RLImage)
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_CENTER

    AZUL   = colors.HexColor("#042C53")
    AZUL_M = colors.HexColor("#185FA5")
    AZUL_C = colors.HexColor("#E6F1FB")
    CINZA  = colors.HexColor("#5F5E5A")
    BRANCO = colors.white

    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    s_titulo = ParagraphStyle("titulo", fontSize=18, textColor=BRANCO,
                               fontName="Helvetica-Bold", alignment=TA_CENTER)
    s_sub    = ParagraphStyle("sub",    fontSize=10, textColor=AZUL_C,
                               fontName="Helvetica",     alignment=TA_CENTER)
    s_campo  = ParagraphStyle("campo",  fontSize=9,  textColor=CINZA,
                               fontName="Helvetica-Bold")
    s_valor  = ParagraphStyle("valor",  fontSize=11, textColor=AZUL,
                               fontName="Helvetica")
    s_rodape = ParagraphStyle("rodape", fontSize=8,  textColor=CINZA,
                               fontName="Helvetica",     alignment=TA_CENTER)
    s_sec    = ParagraphStyle("sec",    fontSize=12, textColor=AZUL_M,
                               fontName="Helvetica-Bold", spaceAfter=6)

    id_, nome, email, tel, sexo, data_nasc, endereco, curso = dados_aluno[:8]
    foto_path = dados_aluno[8] if len(dados_aluno) > 8 else None

    story = []

    # Cabeçalho
    cab = Table([[Paragraph("🎓 Sistema Acadêmico", s_titulo),
                  Paragraph("Ficha de Matrícula", s_sub)]],
                colWidths=["60%", "40%"])
    cab.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), AZUL),
        ("ROWPADDING", (0,0), (-1,-1), 14),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ]))
    story += [cab, Spacer(1, 0.5*cm)]

    # Foto
    foto_cell = ""
    if foto_path and os.path.exists(foto_path):
        try:   foto_cell = RLImage(foto_path, width=3.5*cm, height=3.5*cm)
        except: foto_cell = Paragraph("Sem foto", s_valor)
    else:
        foto_cell = Paragraph("Sem foto", s_valor)

    # Dados pessoais
    borda_linha = TableStyle([
        ("ROWPADDING",  (0,0), (-1,-1), 5),
        ("LINEBELOW",   (0,0), (-1,-1), 0.3, colors.HexColor("#D3D1C7")),
        ("BACKGROUND",  (0,0), (0,-1),  colors.HexColor("#F1EFE8")),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
    ])
    sexo_ext = {"M": "Masculino", "F": "Feminino"}.get(sexo, sexo)
    info = Table([
        [Paragraph("ID",          s_campo), Paragraph(f"#{id_}",    s_valor)],
        [Paragraph("Nome",        s_campo), Paragraph(nome,         s_valor)],
        [Paragraph("Email",       s_campo), Paragraph(email,        s_valor)],
        [Paragraph("Sexo",        s_campo), Paragraph(sexo_ext,     s_valor)],
        [Paragraph("Nascimento",  s_campo), Paragraph(data_nasc,    s_valor)],
    ], colWidths=[3*cm, 10*cm])
    info.setStyle(borda_linha)

    topo = Table([[foto_cell, info]], colWidths=[4*cm, 13*cm])
    topo.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP")]))
    story += [topo, Spacer(1, 0.4*cm),
              HRFlowable(width="100%", thickness=1, color=colors.HexColor("#B5D4F4")),
              Spacer(1, 0.3*cm)]

    # Dados acadêmicos
    story.append(Paragraph("Informações Acadêmicas", s_sec))
    acad = Table([
        [Paragraph("Curso",    s_campo), Paragraph(curso,    s_valor)],
        [Paragraph("Endereço", s_campo), Paragraph(endereco, s_valor)],
        [Paragraph("Telefone", s_campo), Paragraph(tel,      s_valor)],
    ], colWidths=[3*cm, 14*cm])
    acad.setStyle(borda_linha)
    story += [acad, Spacer(1, 1*cm)]

    # Assinatura
    story.append(Table(
        [[Paragraph("_______________________________", s_rodape),
          Paragraph("_______________________________", s_rodape)],
         [Paragraph("Assinatura do Aluno", s_rodape),
          Paragraph("Assinatura da Instituição", s_rodape)]],
        colWidths=["50%", "50%"]))
    story.append(Spacer(1, 0.5*cm))

    # Rodapé
    story += [
        HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#D3D1C7")),
        Spacer(1, 0.2*cm),
        Paragraph(
            f"Gerado em {datetime.datetime.now().strftime('%d/%m/%Y às %H:%M')} "
            "— Sistema Acadêmico de Registro de Alunos", s_rodape)
    ]

    doc.build(story)
    return True


def gerar_relatorio_pdf(dados, output_path, titulo="Relatório de Alunos",
                         filtros_desc=""):
    
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Table, TableStyle, HRFlowable)
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

    AZUL   = colors.HexColor("#042C53")
    AZUL_M = colors.HexColor("#185FA5")
    AZUL_C = colors.HexColor("#E6F1FB")
    CINZA  = colors.HexColor("#5F5E5A")
    CINZA_L = colors.HexColor("#D3D1C7")
    BRANCO = colors.white

    doc = SimpleDocTemplate(output_path, pagesize=landscape(A4),
                            leftMargin=1.5*cm, rightMargin=1.5*cm,
                            topMargin=1.5*cm, bottomMargin=1.5*cm)

    s_titulo  = ParagraphStyle("t",  fontSize=16, textColor=BRANCO,
                                fontName="Helvetica-Bold", alignment=TA_CENTER)
    s_sub     = ParagraphStyle("s",  fontSize=9,  textColor=AZUL_C,
                                fontName="Helvetica", alignment=TA_CENTER)
    s_info    = ParagraphStyle("i",  fontSize=8,  textColor=CINZA,
                                fontName="Helvetica")
    s_rodape  = ParagraphStyle("r",  fontSize=7,  textColor=CINZA,
                                fontName="Helvetica", alignment=TA_CENTER)
    s_cell    = ParagraphStyle("c",  fontSize=8,  textColor=colors.HexColor("#2C2C2A"),
                                fontName="Helvetica", leading=10)
    s_cell_hd = ParagraphStyle("ch", fontSize=8,  textColor=BRANCO,
                                fontName="Helvetica-Bold", leading=10)

    story = []

    # Cabeçalho
    cab = Table([[
        Paragraph("🎓 Sistema Acadêmico", s_titulo),
        Paragraph(titulo, s_sub),
        Paragraph(f"Gerado em {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", s_sub),
    ]], colWidths=["40%", "40%", "20%"])
    cab.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), AZUL),
        ("ROWPADDING", (0,0), (-1,-1), 12),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(cab)
    story.append(Spacer(1, 0.3*cm))

    # Info de filtros e total
    info_txt = f"Total de alunos: {len(dados)}"
    if filtros_desc:
        info_txt += f"   |   Filtros: {filtros_desc}"
    story.append(Paragraph(info_txt, s_info))
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=CINZA_L))
    story.append(Spacer(1, 0.3*cm))

    # Tabela de alunos
    cabecalhos = ["ID", "Nome", "Email", "Telefone", "Sexo", "Nascimento", "Curso"]
    larguras   = [1*cm, 5*cm, 5.5*cm, 3*cm, 1.5*cm, 2.5*cm, 4.5*cm]

    linhas = [[Paragraph(h, s_cell_hd) for h in cabecalhos]]
    for row in dados:
        linhas.append([
            Paragraph(str(row[0]), s_cell),
            Paragraph(str(row[1]), s_cell),
            Paragraph(str(row[2]), s_cell),
            Paragraph(str(row[3]), s_cell),
            Paragraph(str(row[4]), s_cell),
            Paragraph(str(row[5]), s_cell),
            Paragraph(str(row[7]), s_cell),
        ])

    tabela = Table(linhas, colWidths=larguras, repeatRows=1)
    tabela.setStyle(TableStyle([
        # Cabeçalho
        ("BACKGROUND",  (0,0), (-1,0),  AZUL_M),
        ("ROWPADDING",  (0,0), (-1,-1), 5),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        # Linhas alternadas
        *[("BACKGROUND", (0,i), (-1,i),
           colors.HexColor("#F1EFE8") if i % 2 == 0 else BRANCO)
          for i in range(1, len(linhas))],
        # Bordas
        ("LINEBELOW",   (0,0), (-1,-1), 0.3, CINZA_L),
        ("LINEAFTER",   (0,0), (-1,-1), 0.3, CINZA_L),
    ]))
    story.append(tabela)
    story.append(Spacer(1, 0.5*cm))

    # Rodapé
    story.append(HRFlowable(width="100%", thickness=0.5, color=CINZA_L))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "Sistema Acadêmico de Registro de Alunos — Documento gerado automaticamente",
        s_rodape))

    doc.build(story)
    return True