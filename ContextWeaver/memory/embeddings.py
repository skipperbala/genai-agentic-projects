# memory/embeddings.py

import requests
import numpy as np

OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL_NAME = "llama3"

def get_embedding(text: str) -> np.ndarray:
    response = requests.post(OLLAMA_URL, json={"model": MODEL_NAME, "prompt": text})
    if response.status_code == 200:
        vector = response.json()["embedding"]
        return np.array(vector, dtype=np.float32)
    else:
        raise Exception(f"Embedding failed: {response.text}")

