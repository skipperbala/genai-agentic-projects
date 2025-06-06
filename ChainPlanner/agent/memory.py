from langchain.vectorstores import FAISS
from langchain.embeddings import OllamaEmbeddings
from langchain.docstore import InMemoryDocstore
from langchain.schema import Document
import os
import faiss


embedding = OllamaEmbeddings(model="nomic-embed-text")
embedding_dim = 768

def create_memory_store(memory_path: str = "data/memory_index") -> FAISS:
    if os.path.exists(memory_path):
        return FAISS.load_local(memory_path, embedding, allow_dangerous_deserialization=True)
    else:
        index = faiss.IndexFlatL2(embedding_dim)
        return FAISS(embedding.embed_query, index, InMemoryDocstore({}), {})


# Save text to memory
def save_memory(vector_store: FAISS, content: str, metadata: dict = {}):
    doc = Document(page_content=content, metadata=metadata)
    vector_store.add_documents([doc])

# Search memory with a query
def recall_memory(vector_store: FAISS, query: str, k: int = 3):
    return vector_store.similarity_search(query, k=k)

# Save memory to disk
def persist_memory(vector_store: FAISS, path: str = "data/memory_index"):
    vector_store.save_local(path)
