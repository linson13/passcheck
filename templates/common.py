# ==========================================================
# 🧰 templates/common.py
# Shared constants and content-processing helpers used by all
# resume templates. Every template here follows the same ATS
# safety rules: single column, no tables-for-layout, no text
# boxes, no headers/footers, no images/icons, standard fonts.
# ==========================================================

SECTION_ORDER = ["CONTACT", "SUMMARY", "SKILLS", "PROJECTS", "EXPERIENCE", "EDUCATION"]


def contact_line(candidate_data: dict) -> str:
    parts = []
    for field in ("email", "phone", "location"):
        value = candidate_data.get(field)
        if value:
            parts.append(str(value))
    return " | ".join(parts)


def candidate_name(candidate_data: dict) -> str:
    return candidate_data.get("name") or candidate_data.get("full_name") or "Candidate Name"


def bullet_lines(content: str) -> list:
    """Split a PROJECTS/EXPERIENCE section into clean bullet lines."""
    lines = [ln.strip(" -•\t") for ln in content.splitlines() if ln.strip()]
    if len(lines) == 1:
        lines = [s.strip() for s in content.split(";") if s.strip()]
    return lines


def skills_text(content: str) -> str:
    return content.replace("\n", ", ").replace("•", "").strip()
