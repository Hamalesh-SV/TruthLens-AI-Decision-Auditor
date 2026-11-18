import sqlite3
from src.schemas.graph_state import AuditorState
from src.config import DB_PATH

def execute_sql_queries(state: AuditorState) -> dict:
    claims = state.get("extracted_claims", [])
    sql_evidence = []
    
    # Strip sqlite:/// for the sqlite3 module
    db_file = DB_PATH.replace("sqlite:///", "")
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    for claim in claims:
        if claim.get("type") == "metric":
            # Fetches all metrics as context for the judge
            c.execute("SELECT metric_name, recorded_value FROM metrics")
            rows = c.fetchall()
            evidence_found = f"Database records show: {rows}"
            sql_evidence.append({"claim": claim["claim"], "evidence": evidence_found})
            
    conn.close()
    return {"sql_evidence": sql_evidence}