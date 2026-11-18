from src.agents.sql_node import execute_sql_queries
from src.schemas.graph_state import AuditorState

def test_sql_agent_fetches_metrics():
    """Validates that the SQL Node correctly queries the SQLite database for metric claims."""
    mock_state = AuditorState(
        original_memo="Test memo",
        extracted_claims=[{"claim": "Q3 Revenue is $5M", "type": "metric"}],
        sql_evidence=[],
        rag_evidence=[],
        verdicts=[],
        assurance_score=0.0,
        audit_summary="",
        errors=[]
    )
    
    result = execute_sql_queries(mock_state)
    
    assert "sql_evidence" in result
    assert len(result["sql_evidence"]) == 1
    assert "Database records show:" in result["sql_evidence"][0]["evidence"]