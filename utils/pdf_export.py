from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Preformatted
from io import BytesIO
from datetime import datetime

def export_session_pdf(history: list) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )

    title_style = ParagraphStyle('T', fontSize=22,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1D9E75'), spaceAfter=6)
    sub_style = ParagraphStyle('S', fontSize=11,
        fontName='Helvetica',
        textColor=colors.HexColor('#666666'), spaceAfter=20)
    q_style = ParagraphStyle('Q', fontSize=13,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1A1A1A'),
        spaceAfter=6, spaceBefore=16)
    a_style = ParagraphStyle('A', fontSize=11,
        fontName='Helvetica',
        textColor=colors.HexColor('#333333'),
        spaceAfter=8, leading=16)
    code_style = ParagraphStyle('C', fontSize=9,
        fontName='Courier',
        textColor=colors.HexColor('#1A2F45'),
        backColor=colors.HexColor('#F0F4F8'),
        spaceAfter=8, leftIndent=10, rightIndent=10,
        borderPadding=6)

    story = []
    story.append(Paragraph('AI SQL Agent — Session Report', title_style))
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    story.append(Paragraph(
        'Generated: ' + now + ' | Queries: ' + str(len(history)),
        sub_style
    ))
    story.append(HRFlowable(width='100%',
        color=colors.HexColor('#1D9E75')))
    story.append(Spacer(1, 0.4*cm))

    for i, item in enumerate(history, 1):
        story.append(Paragraph('Q' + str(i) + ': ' + item["q"], q_style))
        clean_answer = item['a'].replace('<', '&lt;').replace('>', '&gt;')
        story.append(Paragraph(clean_answer, a_style))
        if item.get('sql'):
            story.append(Paragraph('SQL:', ParagraphStyle('L',
                fontSize=10, fontName='Helvetica-Bold',
                textColor=colors.HexColor('#534AB7'), spaceAfter=4)))
            story.append(Preformatted(item['sql'], code_style))
        story.append(HRFlowable(width='100%',
            color=colors.HexColor('#EEEEEE'), spaceAfter=8))

    doc.build(story)
    return buffer.getvalue()