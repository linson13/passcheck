# ==========================================================
# 🧩 STAGE 1: Resume Extraction (Groq LLM)
# ==========================================================

import os
import config
import utils
import llm_client

SYSTEM_PROMPT = """You are an expert ATS resume parser.
Read the resume text and extract structured candidate data.
Respond ONLY with a JSON object using exactly these keys:
name, email, phone, location, education, skills, experience, projects.
- "skills" must be a list of strings.
- "education" must be a list of strings (one entry per degree/institution).
- "experience" and "projects" must be lists of strings, ONE STRING PER ROLE OR PROJECT.
  Each string must include the title/name, dates if present, AND the full description or
  bullet points underneath it exactly as detail-rich as the original resume — do not
  reduce a project or role to just its title and dates. Join multiple bullet points
  within one entry using "; " so each list item stays a single string.
- Fill missing fields with null (for strings) or [] (for lists).
- Do not include any commentary outside the JSON object."""


def extract_resume_data(resume_input, client=None, out_path=None):
    """
    Extract structured information from a raw resume using an LLM.

    Parameters
    ----------
    resume_input : str
        Either raw text (string) or a file path to .txt/.pdf/.docx.
    client : groq.Groq, optional
        Reuse an existing client; a new one is created if not passed.
    out_path : str, optional
        Where to save the structured JSON. Defaults to config.CANDIDATE_JSON
        (fine for single-user CLI use, NOT safe for concurrent web requests —
        the webapp always passes a per-job path).

    Returns
    -------
    tuple(dict, str)
        (parsed_data, output_json_path)
    """
    client = client or llm_client.get_client()

    # Step 1 – Load text from file or raw string
    if os.path.exists(resume_input):
        resume_text = utils.read_file_text(resume_input)
    else:
        resume_text = resume_input

    # Step 2 – Ask the LLM for structured JSON directly (no regex scraping)
    utils.log_status("🔍 Extracting candidate data with Groq...")
    parsed = llm_client.generate_json(
        client,
        SYSTEM_PROMPT,
        f"Resume:\n{resume_text}",
        max_tokens=2500,
    )

    # Step 3 – Save structured JSON output
    out_path = out_path or config.CANDIDATE_JSON
    utils.save_json(parsed, out_path)
    utils.log_status(f"✅ Candidate JSON saved at: {out_path}")

    return parsed, out_path
