import subprocess

steps = [
    {
        "step": "Scraping recent arXiv papers...",
        "command": ["python", "data/arxiv_scraper.py"]
    },
    {
        "step": "Extracting structured insights from papers...",
        "command": ["python", "agents/tools.py"]
    },
    {
        "step": "Building scientific knowledge graph...",
        "command": ["python", "graph/build_graph.py"]
    },
    {
        "step": "Generating new hypotheses...",
        "command": ["python", "agents/hypothesis_agent.py"]
    }
]

def run_pipeline():
    for step in steps:
        print(f"\n=== {step['step']} ===")
        result = subprocess.run(step["command"])
        if result.returncode != 0:
            print(f"Step failed: {step['step']}")
            break
    else:
        print("\n✅ All steps completed successfully.")

if __name__ == "__main__":
    run_pipeline()