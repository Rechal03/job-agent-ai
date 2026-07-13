from app.agents.workflow import workflow

state = {
    "resume_text": """
Rechal Reddy Chamakura

Skills:
Python
FastAPI
Docker
LangChain
PostgreSQL
Hugging Face
""",

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

    "skill_gap": ""
}

result = workflow.invoke(state)

print(result["summary"])

print("\n=====================\n")

print(result["skill_gap"])