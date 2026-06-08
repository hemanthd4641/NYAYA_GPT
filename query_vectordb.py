# query_vectordb.py

import os
import logging
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

def main():
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX_NAME", "nyaya-gpt")
    namespace = "ipc"

    if not pinecone_api_key:
        logger.error("PINECONE_API_KEY is not set in environment.")
        return

    query = "What is the IPC section for Theft?"
    logger.info(f"Querying Pinecone index '{index_name}' under namespace '{namespace}' for: '{query}'...")

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    db = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings,
        pinecone_api_key=pinecone_api_key,
        namespace=namespace
    )

    docs = db.similarity_search(query, k=3)

    result = []
    for doc in docs:
        result.append({
            "section": doc.metadata.get("section"),
            "section_title": doc.metadata.get("section_title"),
            "chapter": doc.metadata.get("chapter"),
            "chapter_title": doc.metadata.get("chapter_title"),
            "content": doc.page_content
        })

    logger.info("Results:")
    for r in result:
        print(r)

if __name__ == "__main__":
    main()
