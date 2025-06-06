# llm/model_config.py

from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def load_llm(model_name: str = "mistral"):
    """Load local LLM from Ollama"""
    return Ollama(model=model_name)

def get_json_parser():
    """Get LangChain JSON parser"""
    return JsonOutputParser()


