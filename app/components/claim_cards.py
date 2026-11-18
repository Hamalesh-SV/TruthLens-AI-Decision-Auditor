import streamlit as st

def render_verdicts(verdicts: list):
    """Iterates through the list of audit verdicts and renders color-coded cards."""
    if not verdicts:
        st.info("No claims processed yet.")
        return
        
    st.markdown("### Claim Verdicts")
    for verdict in verdicts:
        status = verdict.get("status", "Unknown")
        reason = verdict.get("reason", "No reason provided.")
        claim = verdict.get("claim", "Extracted claim text missing.")
        
        with st.container():
            if status == "Refuted":
                st.error(f"❌ **REFUTED:** {claim}\n\n*Evidence:* {reason}")
            elif status == "Verified":
                st.success(f"✅ **VERIFIED:** {claim}\n\n*Evidence:* {reason}")
            else:
                st.warning(f"⚠️ **UNSUPPORTED/CAUTION:** {claim}\n\n*Evidence:* {reason}")