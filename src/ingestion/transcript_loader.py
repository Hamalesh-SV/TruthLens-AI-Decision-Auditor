import os
from langchain_community.document_loaders import TextLoader

def load_meeting_transcript(file_path: str):
    """Loads raw text meeting logs and board transcripts."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Transcript not found at: {file_path}")
    
    loader = TextLoader(file_path)
    documents = loader.load()
    print(f"Loaded transcript from {file_path}")
    return documents