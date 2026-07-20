# ==========================================================
# 🌐 app.py — ATS Resume Tailor web app
# FastAPI backend: upload a resume, paste a JD, get a tailored,
# ATS-scored PDF back. Each request runs in its own isolated
# job folder so concurrent users never collide.
# ==========================================================

import os
import shutil
import uuid

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import config
import utils
import stage1_resume
import stage2_jd
import stage3_tailor
import llm_client
from templates import list_templates, TEMPLATES, DEFAULT_TEMPLATE

app = FastAPI(title="ATS Resume Tailor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # same-origin frontend; loosened for simplicity
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_UPLOAD_BYTES = 5 * 1024 * 1024  # 5 MB


@app.post("/api/tailor")
async def tailor_resume(resume: UploadFile = File(...), jd_text: str = Form(...),
                         template: str = Form(DEFAULT_TEMPLATE)):
    ext = os.path.splitext(resume.filename or "")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Please upload a .pdf, .docx, or .txt resume.")

    if not jd_text or not jd_text.strip():
        raise HTTPException(400, "Please paste the job description.")

    if template not in TEMPLATES:
        template = DEFAULT_TEMPLATE

    job_id = uuid.uuid4().hex
    job_path = config.job_dir(job_id)

    # Save the upload
    resume_path = os.path.join(job_path, f"resume{ext}")
    content = await resume.read()
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(400, "Resume file is too large (max 5MB).")
    with open(resume_path, "wb") as f:
        f.write(content)

    try:
        client = llm_client.get_client()

        candidate_data, _ = stage1_resume.extract_resume_data(
            resume_path, client, out_path=os.path.join(job_path, "candidate.json")
        )
        jd_data, _ = stage2_jd.extract_jd_data_rulebased(
            jd_text, out_path=os.path.join(job_path, "jd.json")
        )
        tailored_text, pdf_path, ats_report = stage3_tailor.tailor_resume_with_llama(
            candidate_data, jd_data, client,
            output_pdf_path=os.path.join(job_path, "tailored_resume.pdf"),
            template_id=template,
        )
    except RuntimeError as e:
        # e.g. missing GROQ_API_KEY server-side
        raise HTTPException(500, str(e))
    except Exception as e:
        utils.log_status(f"❌ Pipeline error: {e}")
        raise HTTPException(500, "Something went wrong while tailoring the resume. Please try again.")

    return JSONResponse({
        "job_id": job_id,
        "ats_report": ats_report,
        "download_url": f"/api/download/{job_id}",
    })


@app.get("/api/download/{job_id}")
async def download_resume(job_id: str):
    # job_id is a uuid4 hex string — validate to prevent path traversal
    if not all(c in "0123456789abcdef" for c in job_id) or len(job_id) != 32:
        raise HTTPException(400, "Invalid job id.")

    pdf_path = os.path.join(config.job_dir(job_id), "tailored_resume.pdf")
    if not os.path.exists(pdf_path):
        raise HTTPException(404, "Resume not found or has expired.")
    return FileResponse(pdf_path, media_type="application/pdf", filename="tailored_resume.pdf")


@app.get("/api/templates")
async def get_templates():
    return {"templates": list_templates(), "default": DEFAULT_TEMPLATE}


@app.get("/api/health")
async def health():
    return {"status": "ok", "groq_key_configured": bool(config.GROQ_API_KEY)}


# Serve the frontend last so /api/* routes above take priority
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
