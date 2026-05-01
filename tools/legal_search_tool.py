# tools/legal_search_tool.py

import os
from functools import lru_cache
from dotenv import load_dotenv
from crewai.tools import tool
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

@lru_cache(maxsize=1)
def _get_embeddings():
    """Cache embeddings model so it's only loaded once per session."""
    return HuggingFaceEmbeddings()

def _search_collection(query: str, collection_name: str, persist_dir: str, embeddings: HuggingFaceEmbeddings, top_k=2):
    """Internal helper to search a specific collection."""
    try:
        vector_db = Chroma(
            collection_name=collection_name,
            persist_directory=persist_dir,
            embedding_function=embeddings
        )
        docs = vector_db.similarity_search(query, k=top_k)
        return [
            {
                "law": doc.metadata.get("law_name"),
                "section": doc.metadata.get("section"),
                "title": doc.metadata.get("section_title"),
                "punishment": doc.metadata.get("punishment"),
                "fine": doc.metadata.get("fine"),
                "bailability": doc.metadata.get("bailability"),
                "cognizability": doc.metadata.get("cognizability"),
                "state": doc.metadata.get("state", "Central"),
                "content": doc.page_content
            }
            for doc in docs
        ]
    except Exception as e:
        # If collection doesn't exist yet, just skip it
        return []

@tool("Multi-Act Legal Search Tool")
def search_all_laws(query: str) -> list[dict]:
    """
    Search across multiple Indian legal Acts (IPC, CrPC, IT Act, Evidence Act, POCSO, Consumer Law)
    to find relevant sections for a given query.
    """
    persist_dir = os.getenv("PERSIST_DIRECTORY_PATH", "./chroma_vectordb")
    embeddings = _get_embeddings()

    collections = [
        "ipc_collection", 
        "crpc_collection", 
        "iea_collection", 
        "it_act_collection", 
        "pocso_collection", 
        "consumer_collection"
    ]

    all_results = []
    for col in collections:
        results = _search_collection(query, col, persist_dir, embeddings)
        all_results.extend(results)

    return all_results
