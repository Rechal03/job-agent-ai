from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from pydantic import BaseModel
import json
import re


class TailorResult(BaseModel):
    improved_summary: str
    suggested_bullets: list[str]
    keywords_to_add: list[str]


llm = OllamaLLM(
    model="llama3",
    temperature=0
)


tailor_prompt = ChatPromptTemplate.from_template("""
You are an expert resume writer helping a candidate target a specific job.

Candidate's current resume summary:
{resume_summary}

Missing skills for this job:
{missing_skills}

Recommended skills to learn/highlight:
{recommended_skills}

Based on this, produce:
1. A rewritten, ATS-friendly 2-3 sentence professional summary tailored to this job.
2. 3-5 suggested resume bullet points the candidate could add or rewrite to better target this job (based on their real experience, not invented experience).
3. A list of keywords they should make sure appear somewhere in their resume for this job.

Return ONLY valid JSON in this exact format:

{{
"improved_summary": "",
"suggested_bullets": [],
"keywords_to_add": []
}}

Do not invent skills or experience the candidate doesn't have. Only rephrase and emphasize what's already there, and suggest keywords to learn/add honestly.
""")


def tailor_resume(resume_summary, missing_skills, recommended_skills):

    chain = tailor_prompt | llm

    response = chain.invoke({
        "resume_summary": resume_summary,
        "missing_skills": ", ".join(missing_skills),
        "recommended_skills": ", ".join(recommended_skills)
    })

    match = re.search(r"\{.*\}", response, re.DOTALL)

    if not match:
        raise ValueError("No JSON found from LLM response")

    clean_json = match.group()

    clean_json = re.sub(r",\s*}", "}", clean_json)
    clean_json = re.sub(r",\s*]", "]", clean_json)

    data = json.loads(clean_json)

    return TailorResult(**data)
