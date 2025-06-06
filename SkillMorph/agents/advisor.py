def run_advisor(comparison_results: dict, llm_model) -> dict:
    """
    Generate personalized career improvement and learning recommendations based on skill gaps.
    """
    missing_skills = comparison_results.get("missing_skills", [])
    missing_tools = comparison_results.get("missing_tools", [])
    misaligned_roles = comparison_results.get("misaligned_roles", [])
    missing_soft_skills = comparison_results.get("missing_soft_skills", [])

    # Construct the prompt for the LLM to generate career advice
    prompt = f"""
You are a career advisor for professionals looking to enhance their resumes and align better with job market demands.

Given the following analysis results, suggest:
- Relevant online courses, certifications, or resources for missing skills and tools
- Career advice on how to align the candidate with desired roles
- Soft skill improvements

Missing Skills: {missing_skills}
Missing Tools: {missing_tools}
Misaligned Roles: {misaligned_roles}
Missing Soft Skills: {missing_soft_skills}

Return output as a structured JSON:
{{
    "learning_plan": [
        {{ "skill": "skill_name", "recommendations": ["course_link_1", "course_link_2"] }},
        {{ "tool": "tool_name", "recommendations": ["course_link_1", "course_link_2"] }},
        {{ "soft_skill": "soft_skill_name", "recommendations": ["soft_skill_improvement_link"] }}
    ],
    "career_advice": "Here is the general career advice..."
}}
"""
    
    return llm_model.invoke(prompt)
