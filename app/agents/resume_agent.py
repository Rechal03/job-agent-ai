from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM


llm = OllamaLLM(
    model="llama3",
    temperature=0
)


resume_prompt = ChatPromptTemplate.from_template("""
You are an expert technical recruiter and resume parser.

Extract technical information from this resume.

IMPORTANT:
- Do not remove technical keywords.
- Do not summarize too much.
- Preserve every programming language, framework, library, AI/ML technology, database, and cloud technology.
- Include technologies mentioned inside projects and internships.

Resume:

{resume_text}


Return a structured technical profile:


TECHNICAL SKILLS:
(List all technical skills)

PROGRAMMING LANGUAGES:
(List languages only)

FRAMEWORKS AND LIBRARIES:
(List frameworks, libraries, tools)

AI / MACHINE LEARNING SKILLS:
(List ML, DL, NLP, LLM related skills)

DATABASES:
(List databases)

CLOUD / DEVOPS:
(List cloud, deployment, container tools)

PROJECT EXPERIENCE:
(List projects and technologies used)

WORK EXPERIENCE:
(List roles and technical responsibilities)

CERTIFICATIONS:
(List certifications)


Do not include:
- Personal information
- Availability
- Soft skills
- Generic statements

Keep technical details exactly.
""")


def analyze_resume(resume_text):

    chain = resume_prompt | llm

    result = chain.invoke(
        {
            "resume_text": resume_text
        }
    )

    return result