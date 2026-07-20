# Passcheck — ATS Resume Tailor

A small web app: upload a resume, paste a job description, get back a
tailored, ATS-scored PDF. Built with FastAPI (backend + API) and a
vanilla HTML/CSS/JS frontend — no build step required.

## How it works

1. **Extraction** — the uploaded resume (.pdf/.docx/.txt) is parsed into
   structured JSON (skills, experience, projects, etc.) via a Groq LLM call.
2. **JD parsing** — the pasted job description is parsed with rule-based
   regex (no LLM needed for this step).
3. **Tailoring** — candidate + JD data go to Groq, which returns tailored
   resume sections. These are rendered into a one-page ATS-friendly PDF
   (ReportLab), and a keyword-match ATS score is computed before/after.

Each request runs in its own isolated job folder (`output/jobs/<uuid>/`),
so multiple people can use the app at the same time without their data
colliding.

## Local setup

```bash
pip install -r requirements.txt
cp .env.example .env
# edit .env and add your GROQ_API_KEY (free at https://console.groq.com/keys)

uvicorn app:app --reload
```

Then open http://127.0.0.1:8000

## Deploying (Render, free tier)

1. Push this project to a GitHub repo.
2. On [Render](https://render.com), click **New → Web Service**, connect the repo.
   Render will detect `render.yaml` automatically — or set manually:
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
3. In the service's **Environment** tab, add `GROQ_API_KEY` with your real key.
   **Never commit your real key** — `.env` is gitignored for this reason.
4. Deploy. Render gives you a public URL (`https://passcheck.onrender.com`-style)
   that anyone can use.

Free tier note: Render's free web services spin down after inactivity and take
~30–60s to wake up on the next request — fine for personal/demo use, worth
upgrading to a paid instance if you expect steady traffic.

## Limits worth knowing

- 5MB max resume upload size (adjustable in `app.py`, `MAX_UPLOAD_BYTES`)
- Generated PDFs/JSON in `output/jobs/` aren't automatically cleaned up —
  fine for light use, but worth adding a cleanup cron or TTL if this gets
  real traffic
- The ATS score is a simple keyword-match heuristic, not a real ATS
  system's actual scoring — treat it as directional, not exact
