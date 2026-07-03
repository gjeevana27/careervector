# CareerVector 
### AI-Powered Resume Intelligence Platform

CareerVector is an end-to-end AI career assistant that analyzes your resume,
finds semantically matched jobs in real time, scores your ATS compatibility,
builds a personalized growth roadmap, rewrites your resume for specific roles,
and simulates live job interviews — all in one platform.

---

## Live Demo
🚀 Coming Soon

---

## Features

### 📄 Vector Analysis
Upload your resume (PDF or DOCX) and CareerVector extracts and structures
every section — contact info, summary, skills, experience, projects, and
certifications — using Groq's Llama 3.3 70B model.

### 💼 Career Matches
Your resume is embedded using HuggingFace sentence-transformers and matched
against 100+ real-time job listings stored in Pinecone via cosine similarity.
Each match shows a percentage score, required skills, and a one-click gap analysis.

### 🎯 ATS Radar
Scores your resume against Applicant Tracking Systems — both generally and
against a specific job description. Shows section scores, matched and missing
keywords, action verb strength, quantification quality, and formatting issues.

### 🚀 Growth Path
Selects a job from your Career Matches and builds a personalized roadmap:
skills to learn with free and paid resources, projects to build, certifications
to get, career trajectory at 3 months / 6 months / 1 year, and quick wins
you can do this week.

### ⚡ Vector Boost
Rewrites your resume for a specific role — headline options, summary rewrite,
bullet point rewrites in STAR format, power word upgrades, JD language mirroring,
and tone analysis. Before and after comparison for every change.

### 🎤 Interview Launchpad
Live AI interview with Alex, your AI interviewer. Questions are tailored to
your actual resume experience and the specific JD. Natural back-and-forth
conversation with follow-up questions. Full feedback report at the end:
score per answer, what was good, what was weak, and a stronger answer suggestion.

---

## Architecture

```
Resume PDF / DOCX
        ↓
PyMuPDF / python-docx  →  raw text
        ↓
Groq API (Llama 3.3 70B)  →  structured JSON
        ↓
HuggingFace sentence-transformers (all-MiniLM-L6-v2)  →  384-dim vector
        ↓
Pinecone serverless  ←  JSearch API (real-time job listings)
        ↓
cosine similarity matching  →  top job matches
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
| Job Data | JSearch API via RapidAPI (LinkedIn + Indeed) |
| Resume Parsing | PyMuPDF (PDF) + python-docx (DOCX) |
| Frontend | Streamlit |
| Language | Python 3.11 |

---

## Project Structure

```
careervector/
├── app.py                              ← entry point
├── scripts/
│   ├── fetch_jobs.py                   ← fetch real-time jobs from JSearch
│   └── ingest_jobs.py                  ← embed + push jobs to Pinecone
├── src/
│   ├── ai/                             ← Groq client, prompt manager, parser
│   ├── core/                           ← config, settings
│   ├── embeddings/                     ← HuggingFace embedding service
│   ├── matching/                       ← Pinecone matcher, similarity scorer
│   ├── prompts/                        ← all LLM prompts
│   ├── resume/                         ← PDF/DOCX parser, analyzer
│   ├── services/groq/                  ← ATS, career, interview, optimizer
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

### 6 — Fetch jobs and populate Pinecone
```bash
python scripts/fetch_jobs.py
python scripts/ingest_jobs.py
```

### 7 — Run the app
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## API Keys

| Service | Free Tier | Sign Up |
|---|---|---|
| Groq | 100,000 tokens / day | console.groq.com |
| Pinecone | 2GB storage, 1M vectors | pinecone.io |
| JSearch (RapidAPI) | 200 requests / month | rapidapi.com |

---

## How to Use

```
1. Vector Analysis      →  upload your resume PDF or DOCX
2. Career Matches       →  see real matched jobs from Pinecone
3. ATS Radar            →  score your resume against a specific job
4. Growth Path          →  get your personalized skill roadmap
5. Vector Boost         →  rewrite your resume for a specific role
6. Interview Launchpad  →  practice a live interview with Alex
```

---

## Author

**Jeevana Sai Gogineni**
MS Data Science · University of Maryland, College Park ·

[LinkedIn](https://linkedin.com/in/jeevana-gogineni) · [GitHub](https://github.com/gjeevana27)

---

## License

MIT License — free to use, modify, and distribute.