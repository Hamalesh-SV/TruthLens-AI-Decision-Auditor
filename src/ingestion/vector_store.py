import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DOCS_DIR = os.path.join(BASE_DIR, "data", "raw_documents")
CHROMA_PATH = os.path.join(BASE_DIR, "data", "chroma_db")
OLLAMA_BASE_URL = "http://localhost:11434"

def seed_vector_db():
    print(f"Loading documents from {DOCS_DIR}...")
    loader = DirectoryLoader(DOCS_DIR, glob="**/*.txt", loader_cls=TextLoader)
    docs = loader.load()
    
    if not docs:
        print("No text files found! Please ensure you created the .txt files in the raw_documents folders.")
        return

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(docs)
    
    print(f"Split into {len(chunks)} chunks. Generating embeddings...")
    
    # Using a specialized embedding model for vector math
    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)
    
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    db.persist()
    print(f"Successfully seeded ChromaDB at {CHROMA_PATH}")

if __name__ == "__main__":
    seed_vector_db()