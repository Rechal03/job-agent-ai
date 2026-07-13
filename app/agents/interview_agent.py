from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from pydantic import BaseModel
import json
import re


class InterviewResult(BaseModel):
    technical_questions: list[str]
    behavioral_questions: list[str]
    topics_to_study: list[str]


llm = OllamaLLM(
    model="llama3",
    temperature=0
)


interview_prompt = ChatPromptTemplate.from_template("""
You are an experienced technical interviewer preparing a candidate for a job interview.

Candidate's background:
{resume_summary}

Job description:
{job_description}

Missing skills the candidate should expect to be probed on:
{missing_skills}

Generate:
1. 4-5 technical interview questions likely to be asked for this role, mixing questions about the candidate's existing skills and the missing/required skills.
2. 3 behavioral interview questions relevant to this type of role.
3. A list of specific topics the candidate should study before the interview, based on their skill gaps.

Return ONLY valid JSON in this exact format:

{{
"technical_questions": [],
"behavioral_questions": [],
"topics_to_study": []
}}
""")


def generate_interview_prep(resume_summary, job_description, missing_skills):

    chain = interview_prompt | llm

    response = chain.invoke({
        "resume_summary": resume_summary,
        "job_description": job_description,
        "missing_skills": ", ".join(missing_skills)
    })

    match = re.search(r"\{.*\}", response, re.DOTALL)

    if not match:
        raise ValueError("No JSON found from LLM response")

    clean_json = match.group()

    clean_json = re.sub(r",\s*}", "}", clean_json)
    clean_json = re.sub(r",\s*]", "]", clean_json)

    data = json.loads(clean_json)

    def flatten_to_strings(items):
        cleaned = []
        for item in items:
            if isinstance(item, dict):
                # If it's a dict, grab the first text-like value
                cleaned.append(item.get("question") or item.get("topic") or str(item))
            else:
                cleaned.append(str(item))
        return cleaned

    data["technical_questions"] = flatten_to_strings(data.get("technical_questions", []))
    data["behavioral_questions"] = flatten_to_strings(data.get("behavioral_questions", []))
    data["topics_to_study"] = flatten_to_strings(data.get("topics_to_study", []))

    return InterviewResult(**data)