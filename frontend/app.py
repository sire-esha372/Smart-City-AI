import streamlit as st

from components.styles import load_css
from components.sidebar import sidebar


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Smart City AI Platform",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# LOAD CSS
# =========================================================

load_css()


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# =========================================================
# DASHBOARD STATE
# =========================================================

defaults = {
    "traffic_status": "N/A",
    "traffic_value": "--",

    "energy_status": "N/A",
    "energy_value": "--",

    "pollution_status": "N/A",
    "pollution_value": "--",

    "alert_status": "0",
    "alert_value": "No Alerts",
}


for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# SIDEBAR
# =========================================================

sidebar()


# =========================================================
# MOBILE / QUICK NAVIGATION
# =========================================================

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
    "Prediction History",
]


with st.expander("☰ Navigate", expanded=False):

    selected_page = st.selectbox(
        "Go to",
        pages,
        index=pages.index(
            st.session_state.page
        ),
        label_visibility="collapsed",
    )

    if selected_page != st.session_state.page:

        st.session_state.page = selected_page

        st.rerun()


# =========================================================
# CURRENT PAGE
# =========================================================

page = st.session_state.page


# =========================================================
# ROUTING
# =========================================================

if page == "Dashboard":

    from views.dashboard import dashboard

    dashboard()


elif page == "Traffic Intelligence":

    from views.traffic import traffic_page

    traffic_page()


elif page == "Energy Analytics":

    from views.energy import energy

    energy()


elif page == "Environmental Monitoring":

    from views.pollution import pollution

    pollution()


elif page == "Emergency Detection":

    from views.emergency import emergency

    emergency()


elif page == "Waste Management":

    from views.waste import waste_page

    waste_page()


elif page == "Citizen Services":

    from views.citizen_ai import citizen_ai

    citizen_ai()


elif page == "Knowledge Base":

    from views.rag import show

    show()


elif page == "AI Agents":

    from views.agents import agents_page

    agents_page()


elif page == "Prediction History":

    from views.history import history_page

    history_page()


else:

    st.error(
        f"Unknown page: {page}"
    )