# agents/plot_manager.py

import requests

PLOT_STATE = {
    "arc": "The story begins in a peaceful village.",
    "key_events": []
}

def plot_agent(user_input: str) -> str:
    """
    Updates the plot context based on user input.

    Args:
        user_input (str): Latest user interaction.

    Returns:
        str: Updated plot context summary.
    """

    prompt = f"""
You are a story plot manager.

Current arc: {PLOT_STATE['arc']}
Key events so far: {', '.join(PLOT_STATE['key_events']) if PLOT_STATE['key_events'] else 'None'}

Based on the user's input: "{user_input}",

Suggest how the story's plot should evolve. Update key events if needed, keeping the narrative coherent and engaging.
Respond with a concise summary of the updated plot arc.
"""

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })

    if response.status_code != 200:
        return PLOT_STATE["arc"]

    updated_arc = response.json().get("response", PLOT_STATE["arc"]).strip()

    # Optional: Add the user input as a key event (simplified)
    PLOT_STATE["key_events"].append(user_input)
    PLOT_STATE["arc"] = updated_arc

    return updated_arc
