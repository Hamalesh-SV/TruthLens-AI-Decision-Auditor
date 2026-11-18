from langgraph.graph import StateGraph, END
from src.schemas.graph_state import AuditorState

# Import the active AI nodes
from src.agents.extractor_node import extract_claims
from src.agents.sql_node import execute_sql_queries
from src.agents.rag_node import retrieve_rag_context
from src.agents.judge_node import judge_claims
from src.agents.synthesizer_node import synthesize_report

# Build the Graph
workflow = StateGraph(AuditorState)

workflow.add_node("extractor", extract_claims)
workflow.add_node("sql_agent", execute_sql_queries)
workflow.add_node("rag_agent", retrieve_rag_context)
workflow.add_node("judge", judge_claims)
workflow.add_node("synthesizer", synthesize_report)

# Define the flow
workflow.set_entry_point("extractor")
workflow.add_edge("extractor", "sql_agent")
workflow.add_edge("extractor", "rag_agent")
workflow.add_edge("sql_agent", "judge")
workflow.add_edge("rag_agent", "judge")
workflow.add_edge("judge", "synthesizer")
workflow.add_edge("synthesizer", END)

auditor_app = workflow.compile()