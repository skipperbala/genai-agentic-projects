import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def evaluate_hypotheses(hypotheses_text: str, context_summary: str = ""):
    prompt = f"""
You are a scientific reviewer evaluating AI research hypotheses. Given the following context and proposed hypotheses, rate each on:

1. Novelty (0-10)
2. Feasibility (0-10)
3. Relevance to current problems (0-10)

Provide a short justification for each rating.

Context Summary (optional):
{context_summary}

Hypotheses:
{hypotheses_text}

Respond in this format:
- Hypothesis 1:
  - Novelty: X/10 - reason
  - Feasibility: Y/10 - reason
  - Relevance: Z/10 - reason
"""
    response = client.chat.completions.create(model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.3)
    return response.choices[0].message.content

if __name__ == "__main__":
    # Example input (replace with actual hypotheses file or variable)
    hypotheses = """
1. Hypothesis 1: Combining GNNs and symbolic logic will improve explainability in LLMs.
2. Hypothesis 2: Adversarial fine-tuning with meta-learning boosts robustness in vision transformers.
3. Hypothesis 3: A benchmark to evaluate predicted future work leads to better alignment models.
"""
    output = evaluate_hypotheses(hypotheses)
    print("🔍 Hypothesis Evaluation:\n", output)
