from src.graph.workflow import auditor_app

def test_full_langgraph_pipeline():
    """Validates that the full pipeline executes from Extractor to Synthesizer without crashing."""
    initial_state = {
        "original_memo": "The customer churn rate is currently 7.2%."
    }
    
    result = auditor_app.invoke(initial_state)
    
    assert "assurance_score" in result
    assert "verdicts" in result
    assert "extracted_claims" in result
    assert isinstance(result["assurance_score"], float)