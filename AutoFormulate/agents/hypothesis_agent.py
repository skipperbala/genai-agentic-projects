import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def fetch_graph_context():
    query = """
    MATCH (p:Paper)-[:PROPOSES]->(c:Concept),
          (p)-[:LIMITED_BY]->(l:Limitation),
          (p)-[:SUGGESTS]->(f:FutureWork)
    RETURN p.title AS title, c.text AS problem, l.text AS limitation, f.text AS future
    LIMIT 5
    """
    with driver.session() as session:
        result = session.run(query)
        examples = []
        for record in result:
            examples.append({
                "title": record["title"],
                "problem": record["problem"],
                "limitation": record["limitation"],
                "future": record["future"]
            })
    return examples


def generate_hypothesis(context_data):
    context = "\n\n".join([
        f"Title: {item['title']}\nProblem: {item['problem']}\nLimitation: {item['limitation']}\nFuture Work: {item['future']}"
        for item in context_data
    ])

    prompt = f"""
You are an AI research scientist. Based on the following papers and their problems, limitations, and future directions, propose 3 new research hypotheses that push the boundary of current AI research. Make them specific, feasible, and novel.

Context:
{context}

Respond in this format:
1. Hypothesis 1: ...
2. Hypothesis 2: ...
3. Hypothesis 3: ...
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],# ✅ Entry point
        temperature=0.7
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    graph_data = fetch_graph_context()
    output = generate_hypothesis(graph_data)
    print("Proposed Hypotheses:\n", output)
