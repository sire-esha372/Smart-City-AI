import streamlit as st


def sidebar():

    # ===========================
    # LOGO
    # ===========================

    st.sidebar.markdown("# 🏙️")
    st.sidebar.markdown("## Smart City AI")
    st.sidebar.caption("AI-Powered Urban Intelligence")

    st.sidebar.divider()

    # ===========================
    # NAVIGATION
    # ===========================

    pages = [
        "Dashboard",
        "Traffic Intelligence",
        "Energy Analytics",
        "Environmental Monitoring",
        "Emergency Detection",
        "Waste Management",
        "Citizen Services",
        "Knowledge Base",
        "AI Agents",
        "Prediction History"
    ]

    # Create session state if it doesn't exist
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    # Get current index
    current_index = pages.index(st.session_state.page)

    # Sidebar radio
    selected = st.sidebar.radio(
        "",
        pages,
        index=current_index,
        label_visibility="collapsed",
    )

    # Update session state
    st.session_state.page = selected

    st.sidebar.divider()

    # ===========================
    # SYSTEM STATUS
    # ===========================

    st.sidebar.success("🟢 System Online")
    st.sidebar.caption(
        "All Smart City services are operational."
    )