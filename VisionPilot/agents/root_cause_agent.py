from langgraph.graph import StateGraph
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from retriever.vector_store import query_documents

class RootCauseAgent:
    def __init__(self, openai_key):
        self.llm = ChatOpenAI(openai_api_key=openai_key, temperature=0.2)

    def analyze_fault(self, caption: str, detections: list, top_docs: list) -> str:
        doc_text = "\n".join([doc.page_content for doc in top_docs])
        prompt = f"""
You are an expert in industrial fault diagnosis.

Image Caption: {caption}
Detected Faults: {', '.join(detections)}
Relevant Docs: {doc_text}

Analyze the root cause of the fault and output a clear diagnosis.
"""

        messages = [
            SystemMessage(content="You are a root cause analysis expert for manufacturing."),
            HumanMessage(content=prompt)
        ]
        result = self.llm(messages)
        return result.content
