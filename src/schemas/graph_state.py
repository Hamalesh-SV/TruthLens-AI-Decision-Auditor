from typing import TypedDict, List, Dict, Any

class AuditorState(TypedDict):
    original_memo: str
    extracted_claims: List[Dict[str, Any]]
    sql_evidence: List[Dict[str, Any]]
    rag_evidence: List[Dict[str, Any]]
    verdicts: List[Dict[str, Any]]
    assurance_score: float
    audit_summary: str
    errors: List[str]
