from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import Ollama
from agent.memory import save_memory
from config.settings import MODEL_NAME

# Template for generating reflection
reflection_template = """
You are a reflective assistant reviewing the user's day.

Here are the inputs:
- Date: {date}
- Feedback from user: {feedback}
- Mood: {mood}
- What was planned: {plan}
- What was completed: {completed}

Write a short reflective summary:
- What went well?
- What could be improved?
- How should we adjust future plans?

--- Reflection ---
"""

prompt = PromptTemplate(
    input_variables=["date", "feedback", "mood", "plan", "completed"],
    template=reflection_template
)

llm = Ollama(model=MODEL_NAME)
reflection_chain = LLMChain(llm=llm, prompt=prompt)

def reflect_on_day(memory, date: str, feedback: str, mood: str, plan: str, completed: str):
    summary = reflection_chain.run(
        date=date,
        feedback=feedback,
        mood=mood,
        plan=plan,
        completed=completed
    )

    # Save reflection to memory
    save_memory(memory, summary, metadata={"type": "reflection", "date": date})
    return summary
