# ==========================================================
# 📄 templates/compact.py — dense layout for longer resumes
# ==========================================================

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    ListFlowable, ListItem
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from .common import SECTION_ORDER, contact_line, candidate_name, bullet_lines, skills_text

ACCENT = "#2F5D50"


def build(candidate_data: dict, sections: dict, output_pdf_path: str):
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)

    doc = SimpleDocTemplate(
        output_pdf_path, pagesize=A4,
        topMargin=0.5 * inch, bottomMargin=0.5 * inch,
        leftMargin=0.65 * inch, rightMargin=0.65 * inch,
    )

    styles = getSampleStyleSheet()
    header_style = ParagraphStyle(
        "Header", parent=styles["Heading1"],
        fontName="Helvetica-Bold", fontSize=17, leading=20, alignment=0,
        textColor=colors.HexColor("#111111"), spaceAfter=1,
    )
    contact_style = ParagraphStyle(
        "Contact", parent=styles["Normal"],
        fontName="Helvetica", fontSize=9, leading=12,
        textColor=colors.HexColor("#444444"), spaceAfter=6,
    )
    section_title = ParagraphStyle(
        "SectionTitle", parent=styles["Heading2"],
        fontName="Helvetica-Bold", fontSize=10.5, leading=13,
        spaceBefore=7, spaceAfter=2,
        textColor=colors.HexColor(ACCENT),
    )
    body_style = ParagraphStyle(
        "BodyText", parent=styles["Normal"],
        fontName="Helvetica", fontSize=9.5, leading=12.5, spaceAfter=1,
    )

    story = []

    story.append(Paragraph(candidate_name(candidate_data), header_style))
    contact = contact_line(candidate_data)
    if contact:
        story.append(Paragraph(contact, contact_style))
    story.append(HRFlowable(width="100%", color=colors.HexColor(ACCENT), thickness=1.2))
    story.append(Spacer(1, 4))

    for sec in SECTION_ORDER:
        content = sections.get(sec, "").strip()
        if not content:
            continue

        story.append(Paragraph(sec.upper(), section_title))

        if sec == "SKILLS":
            story.append(Paragraph(skills_text(content), body_style))
        elif sec in ("PROJECTS", "EXPERIENCE"):
            items = [ListItem(Paragraph(ln, body_style), leftIndent=6, spaceAfter=0)
                     for ln in bullet_lines(content)]
            story.append(ListFlowable(items, bulletType="bullet", leftIndent=8, bulletFontSize=6))
        else:
            story.append(Paragraph(content.replace("\n", "<br/>"), body_style))

    doc.build(story)
    return output_pdf_path
