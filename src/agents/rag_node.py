from src.schemas.graph_state import AuditorState
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from src.config import CHROMA_PATH, OLLAMA_BASE_URL

def retrieve_rag_context(state: AuditorState) -> dict:
    claims = state.get("extracted_claims", [])
    rag_evidence = []
    
    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    
    for claim in claims:
        if claim.get("type") in ["policy", "meeting_decision"]:
            docs = db.similarity_search(claim["claim"], k=1)
            context = docs[0].page_content if docs else "No internal documents found regarding this claim."
            rag_evidence.append({"claim": claim["claim"], "evidence": context})
            
    return {"rag_evidence": rag_evidence}