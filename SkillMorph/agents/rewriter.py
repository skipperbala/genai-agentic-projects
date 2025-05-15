def run_rewriter(resume_text: str, jd_text: str, llm_model) -> dict:
    """
    Rewrite resume bullet points to better align with job description.
    """
    prompt = f"""
You are an expert in resume optimization.

Rewrite the bullet points in the RESUME below to make them:
- Aligned with the JOB DESCRIPTION
- More action-oriented (using strong verbs)
- Results-focused (mention outcomes when possible)
- More tailored to the desired job role

Ensure the new bullet points include relevant keywords and inferred missing skills.

RESUME:
\"\"\"
{resume_text}
\"\"\"

JOB DESCRIPTION:
\"\"\"
{jd_text}
\"\"\"

Return a JSON object:
{{
    "rewritten_bullets": ["...bullet point 1...", "...bullet point 2...", "...etc..."]
}}
"""

    return llm_model.invoke(prompt)
