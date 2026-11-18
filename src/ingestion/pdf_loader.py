import os
from langchain_community.document_loaders import PyPDFLoader

def load_policy_pdf(file_path: str):
    """Loads and paginates formal PDF reports."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF document not found at: {file_path}")
    
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages from {file_path}")
    return documents