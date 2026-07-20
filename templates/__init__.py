# ==========================================================
# 📚 templates/__init__.py — registry of available resume templates
# ==========================================================

from . import classic, minimal, compact

TEMPLATES = {
    "classic": {
        "name": "Classic",
        "description": "Centered header, navy accent rule, clear section dividers.",
        "build": classic.build,
    },
    "minimal": {
        "name": "Minimal",
        "description": "Left-aligned, monochrome, generous whitespace, spaced-out headings.",
        "build": minimal.build,
    },
    "compact": {
        "name": "Compact",
        "description": "Tighter spacing and smaller type — fits more on one page.",
        "build": compact.build,
    },
}

DEFAULT_TEMPLATE = "classic"


def build_resume(template_id: str, candidate_data: dict, sections: dict, output_pdf_path: str) -> str:
    """Look up a template by id and build the PDF, falling back to the default
    template for an unrecognized id rather than failing the whole request."""
    entry = TEMPLATES.get(template_id) or TEMPLATES[DEFAULT_TEMPLATE]
    return entry["build"](candidate_data, sections, output_pdf_path)


def list_templates() -> list:
    """Metadata for the frontend template picker — no callables included."""
    return [
        {"id": tid, "name": t["name"], "description": t["description"]}
        for tid, t in TEMPLATES.items()
    ]
