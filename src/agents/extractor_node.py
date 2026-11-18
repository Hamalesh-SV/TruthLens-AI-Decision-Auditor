import json
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from src.schemas.graph_state import AuditorState
from src.config import OLLAMA_BASE_URL, DEFAULT_MODEL
from src.agents.prompts import EXTRACTOR_PROMPT

def extract_claims(state: AuditorState) -> dict:
    memo = state["original_memo"]
    
    # Initialize local LLM and force JSON output
    llm = ChatOllama(base_url=OLLAMA_BASE_URL, model=DEFAULT_MODEL, format="json")
    prompt = ChatPromptTemplate.from_template(EXTRACTOR_PROMPT)
    
    chain = prompt | llm
    response = chain.invoke({"memo": memo})
    
    try:
        parsed_data = json.loads(response.content)
        claims = parsed_data.get("claims", [])
    except json.JSONDecodeError:
        claims = []
        
    return {"extracted_claims": claims}