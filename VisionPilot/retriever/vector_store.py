import os
import pickle
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from retriever.doc_parser import load_documents, split_documents

EMBED_PATH = "data/outputs/faiss_index"

def create_vector_store(openai_key):
    os.environ["OPENAI_API_KEY"] = openai_key
    raw_docs = load_documents()
    split_docs = split_documents(raw_docs)

    embed_model = OpenAIEmbeddings()
    vectordb = FAISS.from_documents(split_docs, embed_model)
    
    # Save index
    vectordb.save_local(EMBED_PATH)
    print("✅ FAISS vector store created.")

def load_vector_store(openai_key):
    os.environ["OPENAI_API_KEY"] = openai_key
    embed_model = OpenAIEmbeddings()
    return FAISS.load_local(EMBED_PATH, embed_model)

def query_documents(query, k=3):
    vectordb = load_vector_store(openai_key=os.getenv("OPENAI_API_KEY"))
    return vectordb.similarity_search(query, k=k)
