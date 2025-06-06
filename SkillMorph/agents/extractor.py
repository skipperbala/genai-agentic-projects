import fitz  # PyMuPDF
from pathlib import Path
import pdfplumber
from utils.logger import get_logger
logger = get_logger()

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception as e:
        logger.error(f"Error reading PDF {file_path}: {e}")
        raise RuntimeError("Failed to extract text from PDF.")
    return text

def extract_text_from_txt(txt_path: Path) -> str:
    return Path(txt_path).read_text()

def run_extractor(resume_path: Path, jd_path: Path, llm_model) -> dict:
    resume_text = extract_text_from_pdf(resume_path)
    if jd_path.suffix.lower() == ".txt":
        jd_text = jd_path.read_text(encoding="utf-8", errors="ignore")
    else:
        jd_text = extract_text_from_pdf(jd_path)
    prompt = f"""
You are an expert resume and job analyzer.

Given the following RESUME and JOB DESCRIPTION, extract:
- Relevant Skills
- Job Titles
- Tools/Technologies
- Soft Skills
- Industry Keywords

RESUME:
\"\"\"
{resume_text}
\"\"\"

JOB DESCRIPTION:
\"\"\"
{jd_text}
\"\"\"

Return output as a structured JSON with fields:
{{"resume_skills": [...], "jd_skills": [...], "resume_roles": [...], "jd_roles": [...], "tools": [...], "soft_skills": [...]}}
"""

    response = llm_model.invoke(prompt)
    return response
