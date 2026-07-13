from app.agents.resume_agent import analyze_resume

sample_resume = """
Rechal Reddy Chamakura
M.S. Computer Science, Texas Tech University

Skills: Python, FastAPI, React, LangChain, FAISS, Docker, AWS, PostgreSQL
Experience: Built RAG applications using FAISS and Hugging Face embeddings.
Built full-stack applications with React, Node.js, and PostgreSQL.
"""

result = analyze_resume(sample_resume)
print(result)