from fastapi import APIRouter, UploadFile, File, Form
import shutil
import os

from app.utils.pdf_reader import extract_pdf_text
from app.agents.workflow import workflow

router = APIRouter()


@router.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    os.makedirs("data/resumes", exist_ok=True)

    file_path = f"data/resumes/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume_text = extract_pdf_text(file_path)

    state = {
        "resume_text": resume_text,
        "summary": "",
        "job_description": job_description,
        "skill_gap": "",
        "tailored_resume": "",
        "interview_prep": ""
    }

    result = workflow.invoke(state)

    return {
        "summary": result["summary"],
        "skill_gap": result["skill_gap"],
        "tailored_resume": result["tailored_resume"],
        "interview_prep": result["interview_prep"]
    }