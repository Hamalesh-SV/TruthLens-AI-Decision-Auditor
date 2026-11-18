import streamlit as st

def render_sidebar():
    """Renders the sidebar controls and returns the selected settings."""
    st.sidebar.title("Evidence-Backed Reporting")
    st.sidebar.markdown("### Execution Engine")
    st.sidebar.success("Ollama Online (3 models)")

    inference_mode = st.sidebar.radio(
        "Select Inference Mode:",
        options=["Deterministic Hybrid Engine\n(Instant & Exact)", "Ollama Local LLM + LangGraph"],
        index=0
    )

    ollama_model = st.sidebar.selectbox(
        "Ollama Model:", 
        options=["llama3.1:8b", "mistral", "phi3"]
    )

    st.sidebar.markdown("### Active Controls")
    st.sidebar.markdown("- **Orchestration:** LangGraph StateGraph")
    
    return inference_mode, ollama_model