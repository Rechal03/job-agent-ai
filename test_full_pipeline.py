from app.utils.pdf_reader import extract_pdf_text
from app.agents.workflow import workflow


pdf_path = "data/resumes/resume.pdf"


resume_text = extract_pdf_text(pdf_path)


state = {
    "resume_text": resume_text,
    "summary": "",
    "job_description": """
Looking for an AI Engineer with experience in:

Python
FastAPI
AWS
Docker
Kubernetes
Redis
LangGraph
LLMs
""",
    "skill_gap": "",
    "tailored_resume": "",
    "interview_prep": ""
}


result = workflow.invoke(state)


print("\n================ RESUME SUMMARY ================\n")
print(result["summary"])


print("\n================ SKILL GAP ================\n")
print(result["skill_gap"])

print("\n================ TAILORED RESUME ================\n")
print(result["tailored_resume"])
print("\n================ INTERVIEW PREP ================\n")
print(result["interview_prep"])