import streamlit as st
from datetime import datetime
from components.cards import metric_card


def dashboard():

    # ==========================================
    # HEADER
    # ==========================================

    current_time = datetime.now().strftime("%d %b %Y | %I:%M %p")

    col1, col2 = st.columns([4, 1])

    with col1:

        st.markdown(
            """
            <div class="dashboard-title">
                🏙️ Smart City AI Platform
            </div>

            <div class="dashboard-subtitle">
                AI-Powered Urban Intelligence Dashboard
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.metric(
            "Today",
            current_time
        )

    st.write("")

    # ==========================================
    # METRIC CARDS
    # ==========================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Traffic",
            st.session_state.traffic_status,
            st.session_state.traffic_value,
            "🚦"
        )

    with c2:
        metric_card(
            "Energy",
           st.session_state.energy_status,
           st.session_state.energy_value,
           "⚡"
       )


    with c3:
         metric_card(
               "Pollution",
             st.session_state.pollution_status,
             st.session_state.pollution_value,
             "🌫️"
         )


    with c4:
       metric_card(
             "Alerts",
        st.session_state.alert_status,
        st.session_state.alert_value,
        "🚨"
    )

    st.write("")
    st.write("")

    # ==========================================
    # AI MODULES
    # ==========================================

    st.markdown(
        """
        <div class="section-title">
            AI Modules
        </div>
        """,
        unsafe_allow_html=True,
    )

    modules = [
        ("🚦", "Traffic Prediction", "Traffic Intelligence"),
        ("⚡", "Power Consumption", "Energy Analytics"),
        ("🌫️", "Pollution Prediction", "Environmental Monitoring"),
        ("🚨", "Emergency Detection", "Emergency Detection"),
        ("🗑️", "Waste Classification", "Waste Management"),
        ("👤", "Citizen Assistant", "Citizen Services"),
        ("📚", "Knowledge Base", "Knowledge Base"),
        ("🤖", "AI Agents", "AI Agents"),
    ]

    cols = st.columns(4)

    for i, (icon, title, page) in enumerate(modules):

        with cols[i % 4]:

            if st.button(
                f"{icon}\n\n{title}",
                key=f"module_{i}",
                use_container_width=True,
            ):
                st.session_state.page = page
                st.rerun()