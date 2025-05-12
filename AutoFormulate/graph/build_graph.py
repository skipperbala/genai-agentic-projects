import os
import json
import glob
from neo4j import GraphDatabase

import os
from dotenv import load_dotenv
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

print("Neo4j URI:", os.getenv("NEO4J_USER"))


driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def create_graph(tx, paper):
    paper_id = paper.get("id", paper.get("title", "")[:30])
    tx.run("""
        MERGE (p:Paper {id: $id, title: $title, abstract: $abstract})
        MERGE (prob:Concept {text: $problem})
        MERGE (meth:Method {text: $methodology})
        MERGE (lim:Limitation {text: $limitations})
        MERGE (fut:FutureWork {text: $future_work})
        MERGE (p)-[:PROPOSES]->(prob)
        MERGE (p)-[:USES]->(meth)
        MERGE (p)-[:LIMITED_BY]->(lim)
        MERGE (p)-[:SUGGESTS]->(fut)
    """, {
        "id": paper_id,
        "title": paper.get("title", ""),
        "abstract": paper.get("abstract", ""),
        "problem": paper.get("problem", ""),
        "methodology": paper.get("methodology", ""),
        "limitations": paper.get("limitations", ""),
        "future_work": paper.get("future_work", "")
    })

def process_all_papers():
    extracted_files = glob.glob("data/parsed_papers/*_extracted.json")
    with driver.session() as session:
        for file_path in extracted_files:
            with open(file_path) as f:
                paper_data = json.load(f)
                print(f"Ingesting paper: {paper_data.get('title', '')[:50]}")
                session.write_transaction(create_graph, paper_data)

if __name__ == "__main__":
    process_all_papers()
    print("Knowledge graph populated.")
