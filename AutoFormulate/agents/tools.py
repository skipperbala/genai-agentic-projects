import os
import json
import glob
from typing import Dict
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EXTRACTION_PROMPT_TEMPLATE = """
You are an expert scientific research assistant. Extract the following elements from the research paper content provided:

1. Title
2. Abstract
3. Core Research Problem
4. Methodology
5. Limitations
6. Suggested Future Work

Respond in the following JSON format:
{{
  "title": "...",
  "abstract": "...",
  "problem": "...",
  "methodology": "...",
  "limitations": "...",
  "future_work": "..."
}}

Paper Content:
\"\"\"
{content}
\"\"\"
"""

def extract_scientific_info(text: str) -> Dict:
    prompt = EXTRACTION_PROMPT_TEMPLATE.format(content=text[:5000])  # Safe truncation for long input
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        output = response.choices[0].message.content
        return json.loads(output)
    except Exception as e:
        print(f"Error parsing response: {e}")
        return {}

if __name__ == "__main__":
    paper_files = glob.glob("data/parsed_papers/*.json")

    for file_path in paper_files:
        with open(file_path) as f:
            paper = json.load(f)
            title = paper.get("title", "Untitled Paper")
            summary = paper.get("summary", "")

            print(f"🔍 Extracting from: {title[:60]}...")

            info = extract_scientific_info(summary)
            output_path = file_path.replace(".json", "_extracted.json")

            with open(output_path, "w") as out:
                json.dump(info, out, indent=2)

            print(f"Saved extracted info to {output_path}")
