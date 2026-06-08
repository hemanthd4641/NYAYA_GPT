# tools/legal_search_tool.py

import os
import logging
from functools import lru_cache
from dotenv import load_dotenv
from crewai.tools import tool
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

@lru_cache(maxsize=1)
def _get_embeddings():
    """Cache embeddings model so it's only loaded once per session."""
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

def _search_namespace(query: str, namespace: str, index_name: str, api_key: str, embeddings: HuggingFaceEmbeddings, top_k=2) -> list[dict]:
    """Internal helper to search a specific Pinecone namespace."""
    try:
        vector_db = PineconeVectorStore(
            index_name=index_name,
            embedding=embeddings,
            pinecone_api_key=api_key,
            namespace=namespace
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
        logger.error(f"Error searching namespace '{namespace}' in Pinecone: {e}")
        return []

@tool("Multi-Act Legal Search Tool")
def search_all_laws(query: str) -> list[dict]:
    """
    Search across multiple Indian legal Acts (IPC, CrPC, IT Act, Evidence Act, POCSO, Consumer Law)
    to find relevant sections for a given query in Pinecone namespaces.
    """
    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX_NAME", "nyaya-gpt")

    if not api_key:
        logger.error("PINECONE_API_KEY environment variable is not set.")
        return []

    embeddings = _get_embeddings()

    namespaces = [
        "ipc", 
        "crpc", 
        "iea", 
        "it_act", 
        "pocso", 
        "consumer_act"
    ]

    all_results = []
    for ns in namespaces:
        logger.info(f"Querying Pinecone namespace '{ns}' for: '{query}'...")
        results = _search_namespace(
            query=query, 
            namespace=ns, 
            index_name=index_name, 
            api_key=api_key, 
            embeddings=embeddings
        )
        all_results.extend(results)

    return all_results
