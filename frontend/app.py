import streamlit as st

from components.styles import load_css
from components.sidebar import sidebar

from views.dashboard import dashboard
from views.traffic import traffic_page
from views.energy import energy
from views.pollution import pollution
from views.emergency import emergency
from views.waste import waste_page
from views.citizen_ai import citizen_ai
from views.rag import show as rag_page
from views.agents import agents_page
from views.history import history_page


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Smart City AI Platform",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()

# ==========================================
# SESSION STATE
# ==========================================

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# ==========================================
# DASHBOARD STATE
# ==========================================

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

# ==========================================
# SIDEBAR
# ==========================================

sidebar()

page = st.session_state.page

# ==========================================
# ROUTING
# ==========================================

if page == "Dashboard":
    dashboard()

elif page == "Traffic Intelligence":
    traffic_page()

elif page == "Energy Analytics":
    energy()

elif page == "Environmental Monitoring":
    pollution()

elif page == "Emergency Detection":
    emergency()

elif page == "Waste Management":
    waste_page()

elif page == "Citizen Services":
    citizen_ai()

elif page == "Knowledge Base":
    rag_page()

elif page == "AI Agents":
    agents_page()
elif page == "Prediction History":
    history_page()    