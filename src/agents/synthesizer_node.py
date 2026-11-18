from src.schemas.graph_state import AuditorState

def synthesize_report(state: AuditorState) -> dict:
    verdicts = state.get("verdicts", [])
    if not verdicts:
        return {"assurance_score": 0, "audit_summary": "No testable claims were found in the memo."}
        
    verified_count = sum(1 for v in verdicts if v.get("status") == "Verified")
    score = (verified_count / len(verdicts)) * 100
    
    summary = f"The auditor extracted and tested {len(verdicts)} claims. {verified_count} claims were successfully verified against internal data."
    return {"assurance_score": round(score, 1), "audit_summary": summary}