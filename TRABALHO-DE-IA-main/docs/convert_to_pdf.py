import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

def create_pdf(md_file, pdf_file):
    doc = SimpleDocTemplate(pdf_file, pagesize=letter,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)
    Story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], alignment=TA_CENTER, fontSize=16, spaceAfter=14)
    h2_style = ParagraphStyle('H2Style', parent=styles['Heading2'], fontSize=14, spaceBefore=12, spaceAfter=8)
    h3_style = ParagraphStyle('H3Style', parent=styles['Heading3'], fontSize=12, spaceBefore=10, spaceAfter=6)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=11, spaceAfter=6, alignment=TA_JUSTIFY)
    bullet_style = ParagraphStyle('BulletStyle', parent=styles['Normal'], fontSize=11, spaceAfter=4, leftIndent=20)

    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            Story.append(Spacer(1, 6))
            continue
            
        if line.startswith('---'):
            Story.append(Spacer(1, 12))
            continue
            
        # Proper bold toggle
        parts = line.split('**')
        new_text = ''
        for i, part in enumerate(parts):
            if i % 2 == 1:
                new_text += f'<b>{part}</b>'
            else:
                new_text += part
        text = new_text

        if text.startswith('# '):
            Story.append(Paragraph(text[2:], title_style))
        elif text.startswith('## '):
            Story.append(Paragraph(text[3:], h2_style))
        elif text.startswith('### '):
            Story.append(Paragraph(text[4:], h3_style))
        elif text.startswith('- [ ]'):
            Story.append(Paragraph('• [ ] ' + text[5:], bullet_style))
        elif text.startswith('- '):
            Story.append(Paragraph('• ' + text[2:], bullet_style))
        else:
            Story.append(Paragraph(text, body_style))

    doc.build(Story)

if __name__ == '__main__':
    create_pdf('docs/planejamento_trabalho_ia.md', 'docs/planejamento_trabalho_ia.pdf')
