# ==========================================================
# 📄 templates/classic.py — centered header, navy rules
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

ACCENT = "#0B3D91"


def build(candidate_data: dict, sections: dict, output_pdf_path: str):
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)

    doc = SimpleDocTemplate(
        output_pdf_path, pagesize=A4,
        topMargin=0.6 * inch, bottomMargin=0.6 * inch,
        leftMargin=0.8 * inch, rightMargin=0.8 * inch,
    )

    styles = getSampleStyleSheet()
    header_style = ParagraphStyle(
        "Header", parent=styles["Heading1"],
        fontSize=22, leading=26, alignment=1,
        textColor=colors.HexColor(ACCENT), spaceAfter=6,
    )
    section_title = ParagraphStyle(
        "SectionTitle", parent=styles["Heading2"],
        fontSize=13, leading=16, spaceBefore=10, spaceAfter=4,
        textColor=colors.HexColor("#1A1A1A"),
    )
    body_style = ParagraphStyle(
        "BodyText", parent=styles["Normal"],
        fontSize=11, leading=15, spaceAfter=4,
    )

    story = []

    story.append(Paragraph(f"<b>{candidate_name(candidate_data)}</b>", header_style))
    story.append(HRFlowable(width="100%", color=colors.HexColor(ACCENT), thickness=1))
    story.append(Spacer(1, 6))

    contact = contact_line(candidate_data)
    if contact:
        story.append(Paragraph(contact, body_style))
        story.append(Spacer(1, 10))

    for sec in SECTION_ORDER:
        content = sections.get(sec, "").strip()
        if not content:
            continue

        story.append(Paragraph(f"<b>{sec.title()}</b>", section_title))

        if sec == "SKILLS":
            story.append(Paragraph(skills_text(content), body_style))
            story.append(Spacer(1, 6))
        elif sec in ("PROJECTS", "EXPERIENCE"):
            items = [ListItem(Paragraph(ln, body_style), leftIndent=10) for ln in bullet_lines(content)]
            story.append(ListFlowable(items, bulletType="bullet", leftIndent=12, bulletFontSize=8))
            story.append(Spacer(1, 6))
        else:
            story.append(Paragraph(content.replace("\n", "<br/>"), body_style))
            story.append(Spacer(1, 6))

        story.append(HRFlowable(width="90%", color=colors.lightgrey, thickness=0.4))
        story.append(Spacer(1, 6))

    doc.build(story)
    return output_pdf_path
