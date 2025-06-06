# agents/character_agent.py

import json
from memory.embeddings import get_embedding
from memory.vector_store import VectorStore
import requests

# Load persona config (simplified)
with open("./data/personas.json", "r") as f:
    PERSONAS = json.load(f)

# Character Agent using Ollama + memory
def character_agent(user_input: str, plot_context: str, world_context: str) -> str:
    character_name = "Elaria"  # example character
    persona = PERSONAS.get(character_name, {})

    # Retrieve memories
    embed = get_embedding(user_input)
    store = VectorStore()
    memories = store.search(embed, top_k=3)
    memory_texts = "\n".join([m["text"] for m in memories])

    # Build the prompt
    prompt = f"""
You are {character_name}, a {persona.get('role', 'fantasy character')}.

Backstory:
{persona.get('backstory', 'No backstory available.')}

Memories:
{memory_texts}

World Context:
{world_context}

Plot Context:
{plot_context}

User says: {user_input}

Respond in character.
    """.strip()

    # Generate response
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })

    if response.status_code != 200:
        return "I'm having trouble responding."

    result = response.json()["response"]

    # Store new memory
    memory_data = {"text": f"{character_name} responded to '{user_input}': {result}"}
    memory_embed = get_embedding(result)
    store.add(memory_embed, memory_data)
    store.save()

    return result.strip()
