import json
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from src.schemas.graph_state import AuditorState
from src.config import OLLAMA_BASE_URL, DEFAULT_MODEL

JUDGE_PROMPT = """You are an AI Auditor. Compare the original CLAIM to the retrieved EVIDENCE.
Decide if the claim is 'Verified', 'Refuted', or 'Unsupported'. Provide a 1-sentence reason.

CLAIM: {claim}
EVIDENCE: {evidence}

Respond in strict JSON format: {{"status": "Verified", "reason": "..."}} (Status must be Verified, Refuted, or Unsupported)"""

def judge_claims(state: AuditorState) -> dict:
    sql_ev = state.get("sql_evidence", [])
    rag_ev = state.get("rag_evidence", [])
    all_evidence = sql_ev + rag_ev
    
    llm = ChatOllama(base_url=OLLAMA_BASE_URL, model=DEFAULT_MODEL, format="json", temperature=0)
    prompt = ChatPromptTemplate.from_template(JUDGE_PROMPT)
    chain = prompt | llm
    
    verdicts = []
    for item in all_evidence:
        response = chain.invoke({"claim": item["claim"], "evidence": item["evidence"]})
        try:
            result = json.loads(response.content)
            result["claim"] = item["claim"]
            verdicts.append(result)
        except:
            verdicts.append({"claim": item["claim"], "status": "Unsupported", "reason": "Judge failed to process evidence."})
            
    return {"verdicts": verdicts}