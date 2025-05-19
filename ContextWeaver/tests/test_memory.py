import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from memory.vector_store import VectorStore
from memory.embeddings import get_embedding

def test_memory():
    store = VectorStore()
    embedding = get_embedding("This is a memory about the dragon king.")
    store.add(embedding, {"text": "Memory about the dragon king."})

    results = store.search(embedding, top_k=1)
    assert results[0]["text"] == "Memory about the dragon king."
    print("✅ Memory system works!")

if __name__ == "__main__":
    test_memory()

