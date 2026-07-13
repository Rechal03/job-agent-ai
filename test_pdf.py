from app.utils.pdf_reader import extract_pdf_text


pdf_path = "data/resumes/resume.pdf"


text = extract_pdf_text(pdf_path)


print(text)