# agents/comparator.py

def run_comparator(extracted_data: dict, llm_model) -> dict:
    """
    Compare extracted resume and JD data to identify gaps.
    """

    prompt = f"""
You are an AI career agent helping identify gaps in a resume based on a job description.

Given the following extracted data:

RESUME SKILLS: {extracted_data.get('resume_skills', [])}
JD SKILLS: {extracted_data.get('jd_skills', [])}

RESUME ROLES: {extracted_data.get('resume_roles', [])}
JD ROLES: {extracted_data.get('jd_roles', [])}

TOOLS: {extracted_data.get('tools', [])}
SOFT SKILLS: {extracted_data.get('soft_skills', [])}

Analyze and return:
- Missing skills
- Missing tools or technologies
- Misaligned roles (if any)
- Soft skills that are expected but missing
- Summary of what the candidate should improve to be a better fit

Return output in JSON:
{{
    "missing_skills": [...],
    "missing_tools": [...],
    "misaligned_roles": [...],
    "missing_soft_skills": [...],
    "summary": "..."
}}
"""
    return llm_model.invoke(prompt)

def run_comparator(extracted_data, llm_model):
    resume_text = extracted_data["resume_text"]
    jd_text = extracted_data["jd_text"]

    prompt = f"""
Compare the candidate's resume and job description below.

Resume:
{resume_text}

Job Description:
{jd_text}

List the missing hard skills, soft skills, and any technical mismatches in JSON format like:
{{
  "missing_skills": [...],
  "soft_skills": [...],
  "tools_or_frameworks": [...]
}}
"""

    response = llm_model(prompt)
    
    try:
        import json
        return json.loads(response)
    except:
        return {
            "missing_skills": [response]  # fallback
        }
