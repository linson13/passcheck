<div align="center">

# passcheck

<p align="center">Upload your resume and a job description — Passcheck tailors your resume to match the role using an LLM, then scores it against ATS keyword matching before and after. Get back a clean, ATS-friendly PDF, generated in seconds.</p>

**🔗 Live demo: [passcheck-xpbc.onrender.com](https://passcheck-xpbc.onrender.com)**

[![Stars](https://img.shields.io/github/stars/linson13/passcheck?style=flat-square)](https://github.com/linson13/passcheck/stargazers) [![Forks](https://img.shields.io/github/forks/linson13/passcheck?style=flat-square)](https://github.com/linson13/passcheck/network) [![Issues](https://img.shields.io/github/issues/linson13/passcheck?style=flat-square)](https://github.com/linson13/passcheck/issues) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT)

![Python](https://img.shields.io/badge/-Python-555?style=flat-square&logo=python) ![FastAPI](https://img.shields.io/badge/-FastAPI-555?style=flat-square&logo=fastapi) ![JavaScript](https://img.shields.io/badge/-JavaScript-555?style=flat-square&logo=javascript) ![HTML](https://img.shields.io/badge/-HTML-555?style=flat-square&logo=html5) ![CSS](https://img.shields.io/badge/-CSS-555?style=flat-square&logo=css3)

[🐛 Report Bug](https://github.com/linson13/passcheck/issues) · [✨ Request Feature](https://github.com/linson13/passcheck/issues)

</div>

---

## 📋 Table of Contents

- [How it works](#-how-it-works)
- [Features](#-features)
- [Prerequisites](#️-prerequisites)
- [Local setup](#-local-setup)
- [Deploying (Render, free tier)](#-deploying-render-free-tier)
- [Limits worth knowing](#-limits-worth-knowing)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

## 🧩 How it works

1. **Extraction** — the uploaded resume (`.pdf`/`.docx`/`.txt`) is parsed into structured JSON (skills, experience, projects, etc.) via a Groq LLM call.
2. **JD parsing** — the pasted job description is parsed with rule-based regex (no LLM needed for this step).
3. **Tailoring** — candidate + JD data go to Groq, which returns tailored resume sections. These are rendered into a one-page ATS-friendly PDF (ReportLab), and a keyword-match ATS score is computed before/after.

Each request runs in its own isolated job folder (`output/jobs/<uuid>/`), so multiple people can use the app at the same time without their data colliding.

## ✨ Features

- ✅ Drag-and-drop resume upload (`.pdf`, `.docx`, `.txt`)
- ✅ LLM-powered resume tailoring matched to the job description (via Groq)
- ✅ Before/after ATS keyword-match scoring
- ✅ Three selectable PDF templates: Classic, Minimal, Compact
- ✅ Isolated per-request job folders — safe for concurrent users
- ✅ Free-tier deployable (Render)

## ⚙️ Prerequisites

- Python 3.9+
- A free Groq API key ([console.groq.com/keys](https://console.groq.com/keys))

## 🚀 Local setup

```bash
git clone https://github.com/linson13/passcheck.git
cd passcheck
pip install -r requirements.txt
cp .env.example .env
# edit .env and add your GROQ_API_KEY

uvicorn app:app --reload
```

The app will run locally at the URL printed in your terminal.

## 🌐 Deploying (Render, free tier)

1. Push this project to a GitHub repo.
2. On [Render](https://render.com), click **New → Web Service**, connect the repo. Render will detect `render.yaml` automatically — or set manually:
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
3. In the service's **Environment** tab, add `GROQ_API_KEY` with your real key. **Never commit your real key** — `.env` is gitignored for this reason.
4. Deploy. Render gives you a public URL that anyone can use.

> **Free tier note:** Render's free web services spin down after inactivity and take ~30–60s to wake up on the next request — fine for personal/demo use, worth upgrading to a paid instance if you expect steady traffic.

## ⚠️ Limits worth knowing

- 5MB max resume upload size (adjustable in `app.py`, `MAX_UPLOAD_BYTES`)
- Generated PDFs/JSON in `output/jobs/` aren't automatically cleaned up — fine for light use, but worth adding a cleanup cron or TTL if this gets real traffic
- The ATS score is a simple keyword-match heuristic, not a real ATS system's actual scoring — treat it as directional, not exact

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👤 Contact

**linson13**

- GitHub: [@linson13](https://github.com/linson13)
- Email: [linsonthomas1234@gmail.com](mailto:linsonthomas1234@gmail.com)
- Project: [github.com/linson13/passcheck](https://github.com/linson13/passcheck)

---

<div align="center">Made with ❤️ by linson13</div>
