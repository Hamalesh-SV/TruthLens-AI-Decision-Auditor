"""
TruthLens UI Entry Point
Author: Hamalesh S.V.
"""
import sys
import os
# Add the parent directory (truthlens root) to Python's import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from app.components.sidebar import render_sidebar
from app.components.claim_cards import render_verdicts
from app.components.metrics_dashboard import render_metrics
from src.graph.workflow import auditor_app

st.set_page_config(page_title="TruthLens | AI Business Decision Auditor", layout="wide")

# Render modular sidebar
inference_mode, ollama_model = render_sidebar()

# Main Content
st.title("TruthLens — AI Business Decision Auditor")
st.write("Audits proposed management decisions against structured financial tables (SQL), quarterly policy manuals, and executive meeting records (RAG) to flag unsupported claims, conflicting figures, and missing evidence.")

# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Decision Auditor", 
    "2. Source Data & RAG Explorer", 
    "3. Reliability & Benchmark Evaluation", 
    "4. Architecture & Audit Logs"
])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("Select a Sample Business Decision Memo or Write Your Own:")
        memo_selection = st.selectbox(
            "Memo Selection", 
            options=["DEC-002: East Region SMB Reliability & Churn Response Plan"],
            label_visibility="collapsed"
        )
        
    with col2:
        st.info("**Memo ID:** DEC-002\n\n**Author:** Director of Customer Success\n\n**Date:** 2025-11-02")
        
    memo_text = st.text_area(
        "Business Decision Memo to Audit:",
        value="In Q3 2025, East region SMB Solutions customer churn reached 6.8% while SLA uptime dropped to 98.7%. In accordance with the October 15 meeting decision, we are deploying a 3-engineer Customer Reliability Tiger Team with a $45,000 budget starting November 1, 2025. We are also authorizing account executives to give automatic 25% renewal discounts to all East region clients without CFO review.",
        height=150
    ) 

    st.markdown(
        """<style>
        div.stButton > button:first-child {
            background-color: #ff4b4b;
            color: white;
            width: 100%;
            border-radius: 6px;
        }
        </style>""", unsafe_allow_html=True
    )
    
    if st.button("Run TruthLens Decision Audit"):
        with st.spinner(f"Initializing LangGraph orchestrator & querying {ollama_model}..."):
            
            # 1. Feed the memo text into the LangGraph state
            initial_state = {"original_memo": memo_text}
            
            # 2. Execute the graph workflow
            result = auditor_app.invoke(initial_state)
            
            st.success("Audit Complete. Rendering Claim Cards...")
            st.divider()
            
            # 3. Display the Output summary
            score = result.get('assurance_score', 0)
            st.subheader(f"Assurance Score: {score}/100")
            st.write(f"**Executive Summary:** {result.get('audit_summary', 'No summary generated.')}")
            
            # 4. Render color-coded verdict cards using the component
            render_verdicts(result.get("verdicts", []))

with tab2:
    st.header("Source Data & RAG Explorer")
    st.write("Inspect the ground-truth databases and vector stores the Auditor uses to verify claims.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Structured Data (SQL)")
        st.caption("Active DB: `company_metrics.db`")
        
        sql_data = pd.DataFrame({
            "Metric": ["Q3 Churn Rate", "SLA Uptime", "Customer Reliability Budget", "Q3 Revenue"],
            "Recorded Value": ["7.2%", "99.1%", "$40,000", "$4.2M"],
            "Last Updated": ["2025-10-31", "2025-10-31", "2025-10-16", "2025-10-15"]
        })
        st.dataframe(sql_data, use_container_width=True, hide_index=True)

    with col2:
        st.subheader("Unstructured Data (RAG)")
        st.caption("Active Vector Store: `chroma_db`")
        
        with st.expander("Q4 Corporate Policy Manual.pdf (Policy Guidelines)"):
            st.write("**Section 4.1: Discount Authorization**")
            st.write("Account Executives are authorized to provide automatic renewal discounts up to a maximum of **15%**. Any discount exceeding 15% requires explicit written approval from the Chief Financial Officer (CFO).")
            
        with st.expander("Oct 15 Sprint Planning Meeting.txt (Meeting Transcripts)"):
            st.write("**Agenda Item: East Region SLA Drop**")
            st.write("Decision Log: The board approved a **$40,000** budget to deploy a **2-engineer** Customer Reliability Tiger Team starting in November.")

with tab3:
    # Render the metrics dashboard component
    render_metrics()

with tab4:
    st.header("Architecture & Audit Logs")
    st.write("Trace the LangGraph orchestration flow and inspect the raw JSON state payload.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ### LangGraph Pipeline
        The TruthLens engine routes the decision memo through five specialized agents:
        
        1. **Extractor Node:** Decomposes the raw memo into atomic, testable claims.
        2. **SQL Node:** Translates quantitative claims into queries against `company_metrics.db`.
        3. **RAG Node:** Retrieves semantic context from `chroma_db` for qualitative claims.
        4. **Judge Node:** Cross-checks the original claims against the retrieved evidence.
        5. **Synthesizer Node:** Computes the Assurance Score and formats the final summary.
        """)
        
    with col2:
        st.subheader("Raw Audit State Output (JSON)")
        st.caption("Latest `AuditorState` memory payload")
        
        # Displaying the hardcoded raw graph state for demonstration
        st.json({
            "assurance_score": 42.5,
            "extracted_claims": [
                {"claim": "Churn reached 6.8%", "type": "metric"},
                {"claim": "SLA uptime dropped to 98.7%", "type": "metric"},
                {"claim": "Deploying 3-engineer Tiger Team", "type": "meeting_decision"},
                {"claim": "$45,000 budget for Tiger Team", "type": "meeting_decision"},
                {"claim": "25% renewal discount without CFO review", "type": "policy"}
            ],
            "verdicts": [
                {"status": "Refuted", "reason": "Database shows churn at 7.2%, not 6.8%."},
                {"status": "Refuted", "reason": "Policy limits unreviewed discounts to 15%."},
                {"status": "Refuted", "reason": "Oct 15 meeting approved a 2-engineer team with a $40,000 budget."}
            ]
        })  