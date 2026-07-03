---
title: CareerVector
emoji: 🎯
colorFrom: red
colorTo: gray
sdk: docker
python_version: "3.11"
app_file: app.py
pinned: false
---

# CareerVector 🎯
### AI-Powered Resume Intelligence Platform

CareerVector is an end-to-end AI career assistant that analyzes your resume,
fetches real-time tailored job listings, scores your ATS compatibility,
builds a personalized growth roadmap, rewrites your resume for specific roles,
and simulates live job interviews — all in one platform.

---

## Live Demo
🚀 [Try CareerVector Live](https://huggingface.co/spaces/gjeevana/CareerVector)

---

## Features

### 📄 Vector Analysis
Upload your resume (PDF or DOCX) and CareerVector extracts and structures
every section — contact info, summary, skills, experience, projects, and
certifications — using Groq's Llama 3.3 70B model. Immediately after
analysis, real-time jobs are fetched from JSearch based on your specific
skills and experience titles, and indexed into Pinecone automatically.

### 💼 Career Matches
Your resume is embedded using HuggingFace sentence-transformers with
section-weighted matching (skills 40%, experience 40%, full text 20%)
and matched against freshly fetched job listings stored in Pinecone via
cosine similarity. Each match shows a percentage score, required skills,
and a one-click gap analysis powered by Groq.

### 🎯 ATS Radar
Scores your resume against Applicant Tracking Systems — both generally and
against a specific job description from your matches. Shows section scores,
matched and missing keywords, action verb strength, quantification quality,
and formatting issues.

### 🚀 Growth Path
Select a job from your Career Matches and get a personalized roadmap:
skills to learn with free and paid resource links, projects to build,
certifications to get, career trajectory at 3 months / 6 months / 1 year,
and quick wins you can do this week.

### ⚡ Vector Boost
Rewrites your resume for a specific role — headline options, summary
rewrite, bullet point rewrites in STAR format, power word upgrades,
JD language mirroring, and tone analysis. Before and after comparison
for every change.

### 🎤 Interview Launchpad
Live AI interview with Alex, your AI interviewer. Questions are tailored
to your actual resume experience and the specific JD. Natural
back-and-forth conversation with follow-up questions if answers need
more depth. Full feedback report at the end: score per answer, what was
good, what was weak, and a stronger answer suggestion per question.

---

## Architecture

```
Resume PDF / DOCX
        ↓
PyMuPDF / python-docx  →  raw text
        ↓
Groq API (Llama 3.3 70B)  →  structured resume JSON
        ↓
JobFetchService builds queries from resume skills + titles
        ↓
JSearch API  →  real-time tailored job listings
        ↓
HuggingFace sentence-transformers (all-MiniLM-L6-v2)  →  384-dim vectors
        ↓
Pinecone serverless  ←  fresh jobs indexed automatically
        ↓
Section-weighted cosine similarity matching  →  top job matches
        ↓
Groq API  →  gap analysis / ATS scoring / interview / resume rewrite
        ↓
Streamlit UI
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM (heavy tasks) | Groq — Llama 3.3 70B Versatile |
| LLM (interview chat) | Groq — Llama 3.1 8B Instant |
| Embeddings | HuggingFace sentence-transformers / all-MiniLM-L6-v2 |
| Vector Database | Pinecone Serverless |
| Job Data | JSearch API via RapidAPI (real-time LinkedIn + Indeed) |
| Resume Parsing | PyMuPDF (PDF) + python-docx (DOCX) |
| Frontend | Streamlit |
| Language | Python 3.11 |

---

## Project Structure

```
careervector/
├── app.py                              ← entry point
├── src/
│   ├── ai/                             ← Groq client, prompt manager, parser
│   ├── core/                           ← config, settings
│   ├── embeddings/                     ← HuggingFace embedding service
│   ├── matching/                       ← Pinecone matcher + job ingestion
│   ├── prompts/                        ← all LLM prompts
│   ├── resume/                         ← PDF/DOCX parser, analyzer
│   ├── services/groq/                  ← all AI services
│   │   ├── ats_service.py
│   │   ├── career_service.py
│   │   ├── interview_service.py
│   │   ├── job_fetch_service.py        ← dynamic job fetching per resume
│   │   ├── optimizer_service.py
│   │   ├── resume_service.py
│   │   └── skill_service.py
│   └── ui/
│       ├── components/
│       │   ├── cards/                  ← resume section cards
│       │   ├── _ATS_Score.py
│       │   ├── _Interview_Prep.py
│       │   ├── _Job_Matches.py
│       │   ├── _Resume_Analysis.py
│       │   ├── _Resume_Optimizer.py
│       │   └── _Skill_Gap.py
│       ├── sidebar.py
│       └── theme.py
├── assets/
│   ├── css/styles.css
│   └── images/logo_cv.svg
├── Dockerfile
├── .streamlit/config.toml
├── requirements.txt
└── .env                                ← never committed
```

---

## Local Setup

### Prerequisites
- Python 3.11
- Git

### 1 — Clone the repo
```bash
git clone https://github.com/gjeevana27/careervector.git
cd careervector
```

### 2 — Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python -m venv venv
source venv/bin/activate
```

### 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### 4 — Create `.env` file
```
GROQ_API_KEY=your_groq_key_here
PINECONE_API_KEY=your_pinecone_key_here
JSEARCH_API_KEY=your_rapidapi_key_here
```

### 5 — Create Pinecone index
Go to pinecone.io and create an index with:
- Name: `jd-matcher`
- Dimensions: `384`
- Metric: `cosine`
- Cloud: AWS / us-east-1

### 6 — Run the app
```bash
streamlit run app.py
```

Open `http://localhost:8501` — upload your resume and jobs are
fetched automatically based on your skills.

---

## How It Works

```
1. Vector Analysis      →  upload resume → jobs fetched automatically
2. Career Matches       →  see real matched jobs tailored to your resume
3. ATS Radar            →  score your resume against a specific job
4. Growth Path          →  get your personalized skill roadmap
5. Vector Boost         →  rewrite your resume for a specific role
6. Interview Launchpad  →  practice a live interview with Alex
```

---

## API Keys

| Service | Free Tier | Sign Up |
|---|---|---|
| Groq | 100,000 tokens / day | console.groq.com |
| Pinecone | 2GB storage, 1M vectors | pinecone.io |
| JSearch (RapidAPI) | 200 requests / month | rapidapi.com |

---

## What Makes It Different

- **Resume-tailored job search** — jobs are fetched in real time based
  on your specific skills and experience, not a hardcoded list
- **Section-weighted matching** — skills and experience are weighted
  more heavily than generic resume text for better match accuracy
- **End-to-end pipeline** — upload once, get job matches, ATS score,
  skill roadmap, resume rewrite, and interview prep all from one resume
- **Live interview simulator** — natural conversation with follow-up
  questions, scored per answer with better answer suggestions

---

## Author

**Jeevana Sai Gogineni**
MS Data Science · University of Maryland, College Park ·

[LinkedIn](https://linkedin.com/in/jeevana-gogineni) ·
[GitHub](https://github.com/gjeevana27)

---

## License

MIT License — free to use, modify, and distribute.