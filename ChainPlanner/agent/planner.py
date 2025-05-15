from langchain.agents import initialize_agent, Tool
from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from agent.tools import get_calendar_events, get_todo_list
from config.settings import MODEL_NAME

# ReAct-style prompt template
react_template = """
You are an intelligent personal planner agent using the ReAct paradigm.
Your task is to generate a plan for the user based on the following:

- Today's date: {date}
- Calendar events: {calendar}
- To-Do list: {todos}
- User feedback: {feedback}
- Mood: {mood}

Reason step-by-step and generate a time-blocked task plan.
If there is a conflict, suggest an alternative.

---

Final Plan (with time slots):
"""

prompt = PromptTemplate(
    input_variables=["date", "calendar", "todos", "feedback", "mood"],
    template=react_template
)

# Initialize Ollama LLM
llm = Ollama(model=MODEL_NAME) 

planner_chain = LLMChain(llm=llm, prompt=prompt)

def generate_daily_plan(date: str, feedback: str, mood: str) -> str:
    # Fetch tools (simulated or real)
    calendar = get_calendar_events(date)
    todos = get_todo_list(date)

    # Run ReAct chain
    result = planner_chain.run(
        date=date,
        calendar=calendar,
        todos=todos,
        feedback=feedback,
        mood=mood
    )
    return result
