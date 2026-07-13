# Job Agent AI

Job Agent AI is a multi-agent AI system that analyzes a candidate's resume against a job description and produces a complete application-readiness report — skill gap analysis, tailored resume suggestions, and interview preparation — using a sequential LangGraph agent pipeline powered by a locally-hosted LLM.

Unlike a single-prompt chatbot, this project is built as four specialized agents that pass structured state to one another, each responsible for one part of the analysis.

## Features

- **Resume parsing** — extracts a structured technical profile from an uploaded PDF resume, preserving skills, frameworks, AI/ML technologies, and project details
- **Skill gap analysis** — compares the resume against a job description and returns matched skills, missing skills, recommended skills to learn, and a match score
- **Resume tailoring** — generates a rewritten, ATS-friendly summary and suggested bullet points based on the candidate's real experience (never invents skills or experience)
- **Interview preparation** — generates likely technical and behavioral interview questions, plus specific topics to study, based on the candidate's actual skill gaps
- **Web UI** — upload a resume and paste a job description to get a full visual report

## Tech Stack

- **Backend:** FastAPI, Uvicorn
- **Agent Orchestration:** LangGraph, LangChain
- **LLM:** Llama 3, served locally via Ollama — fully private, no API costs
- **PDF Parsing:** pypdf
- **Structured Output:** Pydantic
- **Frontend:** HTML/CSS/JavaScript
- **Language:** Python

## Architecture

```
Resume PDF
    │
    ▼
PDF Text Extraction (pypdf)
    │
    ▼
┌─────────────────────────────────────────┐
│           LangGraph Pipeline             │
│                                           │
│  Resume Analyzer Agent                   │
│  → extracts structured technical profile │
│              │                           │
│              ▼                           │
│  Skill Gap Agent                         │
│  → compares resume vs. job description   │
│  → matched / missing / recommended       │
│              │                           │
│              ▼                           │
│  Resume Tailor Agent                     │
│  → rewritten summary, suggested bullets  │
│              │                           │
│              ▼                           │
│  Interview Prep Agent                    │
│  → technical & behavioral questions      │
│  → topics to study                       │
└─────────────────────────────────────────┘
    │
    ▼
Full JSON Report → Web UI
```

Each agent is a separate node in a LangGraph `StateGraph`. State (resume text, job description, and each agent's output) flows through the graph via a shared `TypedDict`, so later agents can build on earlier agents' structured output rather than re-parsing raw text.

## Project Structure

```
job-agent-ai/
│
├── app/
│   ├── agents/
│   │   ├── resume_agent.py         # Extracts structured resume profile
│   │   ├── skill_gap_agent.py      # Compares resume vs. job description
│   │   ├── resume_tailor_agent.py  # Generates tailored resume suggestions
│   │   ├── interview_agent.py      # Generates interview prep
│   │   └── workflow.py             # LangGraph pipeline definition
│   │
│   ├── api/
│   │   └── analyze.py              # POST /analyze endpoint
│   │
│   └── utils/
│       └── pdf_reader.py           # PDF text extraction
│
├── frontend/
│   └── index.html                  # Web UI
│
├── data/
│   └── resumes/                    # Uploaded resumes (gitignored)
│
├── main.py                         # FastAPI app entrypoint
└── requirements.txt
```

## Setup

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com) installed, with the `llama3` model pulled:
  ```bash
  ollama pull llama3
  ```

### Installation
```bash
git clone https://github.com/Rechal03/job-agent-ai.git
cd job-agent-ai
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
```

### Running
```bash
uvicorn main:app --reload
```

- API docs: `http://127.0.0.1:8000/docs`
- Web UI: open `frontend/index.html` directly in a browser

## API

| Endpoint | Method | Description |
|---|---|---|
| `/analyze` | POST | Upload a resume PDF and job description text; returns full 4-agent analysis |

**Request:** `multipart/form-data`
- `file` — resume PDF
- `job_description` — job posting text

**Response:**
```json
{
  "summary": "...",
  "skill_gap": {
    "matched_skills": [...],
    "missing_skills": [...],
    "recommended_skills": [...],
    "match_score": 70,
    "explanation": "..."
  },
  "tailored_resume": {
    "improved_summary": "...",
    "suggested_bullets": [...],
    "keywords_to_add": [...]
  },
  "interview_prep": {
    "technical_questions": [...],
    "behavioral_questions": [...],
    "topics_to_study": [...]
  }
}
```

## Notes on LLM Reliability

Local LLMs don't always follow structured-output instructions exactly. This project handles that with:
- Regex-based JSON extraction from responses that include extra text
- Trailing comma and malformed-fraction cleanup before parsing
- Pydantic schema validation with normalization for inconsistent field shapes (e.g., flattening nested objects back into plain strings when the model over-structures its output)

## Future Improvements

- Job posting URL ingestion (fetch and parse directly from a link)
- Multi-resume comparison against the same job
- Export tailored resume as a downloadable PDF
- Streaming responses for faster perceived latency
- Docker deployment