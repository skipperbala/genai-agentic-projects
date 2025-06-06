import pdfkit
from pathlib import Path

def generate_pdf(resume_text: str, learning_plan: dict, output_path: Path):
    """
    Generate a professional PDF document with the rewritten resume and learning plan.
    """
    # Prepare the HTML content for PDF generation
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }}
            h1 {{ color: #2C3E50; }}
            h2 {{ color: #16A085; }}
            p {{ margin: 10px 0; }}
            .learning-plan {{ margin-top: 30px; }}
            .learning-plan li {{ margin-bottom: 10px; }}
        </style>
    </head># app/ui.py

    <body>
        <h1>Optimized Resume</h1>
        <p>{resume_text}</p>
        
        <h2>Career Improvement Plan</h2>
        <p>Here are some personalized suggestions to help you align better with your desired career:</p>
        <div class="learning-plan">
            <ul>
    """

    # Add learning plan suggestions
    for item in learning_plan.get("learning_plan", []):
        skill_name = item.get("skill") or item.get("tool") or item.get("soft_skill")
        html_content += f"<li><strong>{skill_name}</strong>: <ul>"
        for rec in item.get("recommendations", []):
            html_content += f"<li><a href='{rec}'>{rec}</a></li>"
        html_content += "</ul></li>"

    html_content += f"""
            </ul>
        </div>
        
        <h2>General Career Advice</h2>
        <p>{learning_plan.get('career_advice', 'No advice available.')}</p>
    </body>
    </html>
    """

    # Generate the PDF
    pdfkit.from_string(html_content, str(output_path))

    return output_path
