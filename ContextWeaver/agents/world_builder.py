# agents/world_builder.py

import requests

WORLD_STATE = {
    "lore": "The world of Eldoria is filled with magic, ancient forests, and hidden kingdoms.",
    "rules": [
        "Magic is rare and requires great skill.",
        "Dragons are majestic and rarely seen.",
        "The forest spirits protect nature from harm."
    ],
    "tone": "mystical and poetic"
}

def world_agent(user_input: str) -> str:
    """
    Updates world context based on user input and ensures story adheres to lore and tone.

    Args:
        user_input (str): Latest user interaction.

    Returns:
        str: Updated world context summary.
    """

    prompt = f"""
You are a world builder agent maintaining the story's lore, tone, and rules.

Current lore:
{WORLD_STATE['lore']}

Rules:
- {"\n- ".join(WORLD_STATE['rules'])}

Tone:
{WORLD_STATE['tone']}

User input:
"{user_input}"

Provide an updated summary of the world context that respects these constraints.
"""

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })

    if response.status_code != 200:
        return WORLD_STATE["lore"]

    updated_context = response.json().get("response", WORLD_STATE["lore"]).strip()

    # Optional: update lore or tone if needed (here we keep it simple)
    return updated_context
