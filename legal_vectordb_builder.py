# legal_vectordb_builder.py

import json
import os
from dotenv import load_dotenv
from langchain_community.docstore.document import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

def load_json_data(file_path: str) -> list[dict]:
    """Load legal data from a JSON file."""
    if not os.path.exists(file_path):
        print(f"⚠️ Warning: File not found at {file_path}. Skipping.")
        return []
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def prepare_documents(legal_data: list[dict], law_name: str) -> list[Document]:
    """Convert JSON entries to LangChain Document objects with metadata."""
    return [
        Document(
            page_content=f"[{law_name}] Section {entry['Section']}: {entry['section_title']}\n\n{entry['section_desc']}",
            metadata={
                "law_name": law_name,
                "chapter": entry.get("chapter"),
                "chapter_title": entry.get("chapter_title"),
                "section": entry["Section"],
                "section_title": entry["section_title"],
                "punishment": entry.get("punishment", "As per court discretion"),
                "fine": entry.get("fine", "Applicable"),
                "bailability": entry.get("bailability", "Non-Bailable"),
                "cognizability": entry.get("cognizability", "Cognizable"),
                "state": entry.get("state", "Central")
            }
        )
        for entry in legal_data
    ]

def build_collection(file_path, collection_name, law_name, persist_dir, embeddings):
    """Build and persist a specific collection for a law."""
    data = load_json_data(file_path)
    if not data:
        return
    
    documents = prepare_documents(data, law_name)
    
    Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_dir,
        collection_name=collection_name
    )
    print(f"✅ Collection '{collection_name}' ({law_name}) created successfully.")

def build_all_vectordbs():
    """Build all legal vector databases."""
    persist_dir = os.getenv("PERSIST_DIRECTORY_PATH", "./chroma_vectordb")
    embeddings = HuggingFaceEmbeddings()

    # Define the Acts to process
    acts = [
        {"file": "ipc.json", "collection": "ipc_collection", "name": "IPC"},
        {"file": "crpc.json", "collection": "crpc_collection", "name": "CrPC"},
        {"file": "iea.json", "collection": "iea_collection", "name": "Evidence Act"},
        {"file": "it_act.json", "collection": "it_act_collection", "name": "IT Act"},
        {"file": "pocso.json", "collection": "pocso_collection", "name": "POCSO"},
        {"file": "consumer_act.json", "collection": "consumer_collection", "name": "Consumer Act"},
    ]

    for act in acts:
        # Use path from env if available, else relative path
        env_path = os.getenv(f"{act['name']}_JSON_PATH")
        file_path = env_path if env_path else act['file']
        
        build_collection(file_path, act['collection'], act['name'], persist_dir, embeddings)

if __name__ == "__main__":
    build_all_vectordbs()
