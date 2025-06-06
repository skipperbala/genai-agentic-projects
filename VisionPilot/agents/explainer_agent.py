from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

class ExplanationAgent:
    def __init__(self, openai_key):
        self.llm = ChatOpenAI(openai_api_key=openai_key, temperature=0.5)

    def explain_fix(self, caption: str, diagnosis: str) -> str:
        prompt = f"""
You are an AI technician assistant.

Given this fault description: {caption}
And this root cause diagnosis: {diagnosis}

Explain in simple terms what the fault is and how to fix it.
Output should be suitable for a factory technician.
"""
        messages = [
            SystemMessage(content="You are a helpful AI assistant for industrial repair."),
            HumanMessage(content=prompt)
        ]
        result = self.llm(messages)
        return result.content
