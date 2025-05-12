import os
import feedparser
import requests
import time
import json

ARXIV_API = "http://export.arxiv.org/api/query"

def fetch_arxiv_papers(query="cs.AI", max_results=10):
    print(f"🔍 Fetching arXiv papers for query: {query}")
    params = {
        "search_query": f"cat:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    response = requests.get(ARXIV_API, params=params)
    feed = feedparser.parse(response.text)

    papers = []
    for entry in feed.entries:
        paper = {
            "id": entry.id.split("/")[-1],
            "title": entry.title,
            "summary": entry.summary,
            "authors": [author.name for author in entry.authors],
            "published": entry.published,
            "link": entry.link,
            "pdf_url": next((l.href for l in entry.links if l.type == "application/pdf"), None)
        }
        papers.append(paper)
    return papers

def save_papers(papers, output_dir="data/parsed_papers"):
    os.makedirs(output_dir, exist_ok=True)
    for paper in papers:
        filename = f"{paper['id'].replace('/', '_')}.json"
        path = os.path.join(output_dir, filename)
        with open(path, "w") as f:
            json.dump(paper, f, indent=2)
    print(f"✅ Saved {len(papers)} papers to {output_dir}")

if __name__ == "__main__":
    papers = fetch_arxiv_papers(query="cs.AI", max_results=5)
    save_papers(papers)
