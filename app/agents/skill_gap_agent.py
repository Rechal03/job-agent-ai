from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from pydantic import BaseModel
import json
import re


class SkillGapResult(BaseModel):
    matched_skills: list[str]
    missing_skills: list[str]
    recommended_skills: list[str]
    match_score: int
    explanation: str


llm = OllamaLLM(
    model="llama3",
    temperature=0
)


skill_gap_prompt = ChatPromptTemplate.from_template("""
You are an expert AI technical recruiter.

Analyze the candidate resume against the job description.

Consider:

1. Direct skill matches.
2. Related technologies.
3. Project experience.
4. AI/ML transferable knowledge.
5. Industry relevance.

Do not only compare exact keywords.


Resume:

{resume_summary}


Job Description:

{job_description}


Return ONLY valid JSON.

Do not include:
- Markdown
- ```json
- Extra text
- Fractions
- Comments


JSON format:

{{
"matched_skills": [],
"missing_skills": [],
"recommended_skills": [],
"match_score": 0,
"explanation": ""
}}


Rules:

matched_skills:
- Skills already present or strongly related.

missing_skills:
- Important job requirements missing from resume.

recommended_skills:
- Technical skills the candidate should learn.

match_score:
- Integer between 0 and 100.


Example:

{{
"matched_skills": [
"Python",
"Machine Learning"
],
"missing_skills": [
"AWS",
"Kubernetes"
],
"recommended_skills": [
"AWS",
"Kubernetes"
],
"match_score": 60,
"explanation": "Candidate has ML experience but needs cloud deployment skills."
}}

Generate JSON only.
""")


def analyze_skill_gap(resume_summary, job_description):

    chain = skill_gap_prompt | llm


    response = chain.invoke(
        {
            "resume_summary": resume_summary,
            "job_description": job_description
        }
    )


    print("\nLLM RAW RESPONSE:")
    print(response)


    # Extract JSON only
    match = re.search(
        r"\{.*\}",
        response,
        re.DOTALL
    )


    if not match:
        raise ValueError(
            "No JSON found from LLM response"
        )


    clean_json = match.group()


    # Fix common Llama formatting issues

    clean_json = re.sub(
        r",\s*}",
        "}",
        clean_json
    )


    clean_json = re.sub(
        r",\s*]",
        "]",
        clean_json
    )


    data = json.loads(clean_json)


    if "explanation" not in data:
        data["explanation"] = (
            "Skill comparison generated successfully."
        )


    return SkillGapResult(**data)