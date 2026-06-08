# legal_vectordb_builder.py

import json
import os
import time
import logging
from dotenv import load_dotenv
from langchain_community.docstore.document import Document
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

def load_json_data(file_path: str) -> list[dict]:
    """Load legal data from a JSON file."""
    if not os.path.exists(file_path):
        logger.warning(f"File not found at {file_path}. Skipping.")
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Error loading {file_path}: {e}")
        return []

def prepare_documents(legal_data: list[dict], law_name: str) -> list[Document]:
    """Convert JSON entries to LangChain Document objects with metadata."""
    documents = []
    for entry in legal_data:
        try:
            # Ensure section and titles are clean strings
            section = str(entry.get("Section", ""))
            section_title = str(entry.get("section_title", ""))
            section_desc = str(entry.get("section_desc", ""))
            
            # Construct metadata, cleaning potential None/null values
            doc = Document(
                page_content=f"[{law_name}] Section {section}: {section_title}\n\n{section_desc}",
                metadata={
                    "law_name": str(law_name),
                    "chapter": str(entry.get("chapter", "")),
                    "chapter_title": str(entry.get("chapter_title", "")),
                    "section": section,
                    "section_title": section_title,
                    "punishment": str(entry.get("punishment", "As per court discretion")),
                    "fine": str(entry.get("fine", "Applicable")),
                    "bailability": str(entry.get("bailability", "Non-Bailable")),
                    "cognizability": str(entry.get("cognizability", "Cognizable")),
                    "state": str(entry.get("state", "Central"))
                }
            )
            documents.append(doc)
        except Exception as e:
            logger.error(f"Error parsing entry in {law_name}: {entry}. Error: {e}")
    return documents

def build_collection(file_path, namespace, law_name, index_name, embeddings, pinecone_api_key):
    """Build and upload a specific namespace for a law in Pinecone."""
    data = load_json_data(file_path)
    if not data:
        return
    
    documents = prepare_documents(data, law_name)
    if not documents:
        logger.warning(f"No valid documents found for {law_name}.")
        return

    logger.info(f"Upserting {len(documents)} documents for '{law_name}' to Pinecone namespace '{namespace}'...")
    
    # Upsert in batches of 100 documents to avoid timeouts or API limits
    batch_size = 100
    for i in range(0, len(documents), batch_size):
        batch_docs = documents[i : i + batch_size]
        retries = 3
        while retries > 0:
            try:
                PineconeVectorStore.from_documents(
                    documents=batch_docs,
                    embedding=embeddings,
                    index_name=index_name,
                    namespace=namespace,
                    pinecone_api_key=pinecone_api_key
                )
                logger.info(f"Successfully upserted batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1} for '{law_name}'")
                break
            except Exception as e:
                retries -= 1
                logger.error(f"Error upserting batch to Pinecone (Retries left: {retries}): {e}")
                if retries == 0:
                    raise e
                time.sleep(2)

def build_all_vectordbs():
    """Build all legal vector databases in Pinecone."""
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX_NAME", "nyaya-gpt")

    if not pinecone_api_key:
        logger.error("PINECONE_API_KEY is not set in environment.")
        raise ValueError("❌ PINECONE_API_KEY environment variable is required.")

    # Initialize Pinecone Client
    logger.info("Initializing Pinecone client...")
    pc = Pinecone(api_key=pinecone_api_key)

    # Instantiate HuggingFace embeddings
    logger.info("Loading HuggingFace embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    # Get expected embedding dimension dynamically
    logger.info("Determining embedding dimensions...")
    test_emb = embeddings.embed_query("test query")
    dimension = len(test_emb)
    logger.info(f"Embedding dimension resolved: {dimension}")

    # Create Pinecone index if it doesn't exist
    existing_indexes = [idx.name for idx in pc.list_indexes()]
    if index_name not in existing_indexes:
        logger.info(f"Pinecone index '{index_name}' not found. Creating serverless index...")
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        # Wait for index initialization
        while not pc.describe_index(index_name).status.ready:
            logger.info("Waiting for Pinecone index to be ready...")
            time.sleep(2)
        logger.info("Pinecone index created and ready.")
    else:
        logger.info(f"Pinecone index '{index_name}' already exists.")

    # Define the Acts to process with Pinecone Namespaces
    acts = [
        {"file": "ipc.json", "namespace": "ipc", "name": "IPC"},
        {"file": "crpc.json", "namespace": "crpc", "name": "CrPC"},
        {"file": "iea.json", "namespace": "iea", "name": "Evidence Act"},
        {"file": "it_act.json", "namespace": "it_act", "name": "IT Act"},
        {"file": "pocso.json", "namespace": "pocso", "name": "POCSO"},
        {"file": "consumer_act.json", "namespace": "consumer_act", "name": "Consumer Act"},
    ]

    for act in acts:
        # Use path from env if available, else relative path
        env_key = f"{act['name'].upper().replace(' ', '_')}_JSON_PATH"
        env_path = os.getenv(env_key)
        file_path = env_path if env_path else act['file']
        
        build_collection(
            file_path=file_path, 
            namespace=act['namespace'], 
            law_name=act['name'], 
            index_name=index_name, 
            embeddings=embeddings, 
            pinecone_api_key=pinecone_api_key
        )
        
    logger.info("🎉 All legal databases have been successfully indexed in Pinecone.")

if __name__ == "__main__":
    build_all_vectordbs()
