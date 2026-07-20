# ==========================================================
# 📄 templates/minimal.py — left-aligned, quiet, monochrome
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

INK = "#222222"
RULE = "#CCCCCC"


def build(candidate_data: dict, sections: dict, output_pdf_path: str):
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)

    doc = SimpleDocTemplate(
        output_pdf_path, pagesize=A4,
        topMargin=0.75 * inch, bottomMargin=0.75 * inch,
        leftMargin=0.9 * inch, rightMargin=0.9 * inch,
    )

    styles = getSampleStyleSheet()
    header_style = ParagraphStyle(
        "Header", parent=styles["Heading1"],
        fontName="Helvetica", fontSize=20, leading=24, alignment=0,
        textColor=colors.HexColor(INK), spaceAfter=2,
    )
    contact_style = ParagraphStyle(
        "Contact", parent=styles["Normal"],
        fontName="Helvetica", fontSize=9.5, leading=13,
        textColor=colors.HexColor("#666666"), spaceAfter=14,
    )
    section_title = ParagraphStyle(
        "SectionTitle", parent=styles["Heading2"],
        fontName="Helvetica-Bold", fontSize=10, leading=13,
        spaceBefore=14, spaceAfter=6,
        textColor=colors.HexColor(INK),
        # simulate letter-spacing via explicit uppercase text
    )
    body_style = ParagraphStyle(
        "BodyText", parent=styles["Normal"],
        fontName="Helvetica", fontSize=10.5, leading=15, spaceAfter=3,
        textColor=colors.HexColor(INK),
    )

    story = []

    story.append(Paragraph(candidate_name(candidate_data), header_style))
    contact = contact_line(candidate_data)
    if contact:
        story.append(Paragraph(contact, contact_style))
    story.append(HRFlowable(width="100%", color=colors.HexColor(RULE), thickness=0.75))

    for sec in SECTION_ORDER:
        content = sections.get(sec, "").strip()
        if not content:
            continue

        # spaced-out uppercase label, minimal style signature
        label = " ".join(list(sec.upper()))  # "S U M M A R Y" style letter-spacing
        story.append(Paragraph(label, section_title))

        if sec == "SKILLS":
            story.append(Paragraph(skills_text(content), body_style))
        elif sec in ("PROJECTS", "EXPERIENCE"):
            items = [ListItem(Paragraph(ln, body_style), leftIndent=8, bulletFontSize=6)
                     for ln in bullet_lines(content)]
            story.append(ListFlowable(items, bulletType="bullet", leftIndent=10,
                                       bulletFontSize=6, bulletColor=colors.HexColor("#999999")))
        else:
            story.append(Paragraph(content.replace("\n", "<br/>"), body_style))

    doc.build(story)
    return output_pdf_path
