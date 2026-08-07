import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/agents/chat"


def agents_page():

    st.title("🤖 AI Agents")
    st.caption("Interact with specialized AI agents for Smart City decision support.")

    st.divider()

    result = None
    error = None

    col1, col2 = st.columns([1, 2])

    # ==========================================
    # LEFT PANEL
    # ==========================================

    with col1:

        st.subheader("⚙️ Select Agent")

        agent = st.selectbox(
            "Choose Agent",
            ["Traffic", "Energy", "Waste", "Emergency"],
            label_visibility="collapsed"
        )

        st.info(f"### {agent} Agent")

        if agent == "Traffic":

            st.markdown("""
- 🚦 Traffic Congestion
- 🛣 Route Optimization
- 🚥 Signal Management
- 🚗 Smart Mobility
""")

        elif agent == "Energy":

            st.markdown("""
- ⚡ Power Consumption
- 🌞 Renewable Energy
- 🔋 Smart Grid
- 💡 Energy Saving
""")

        elif agent == "Waste":

            st.markdown("""
- ♻️ Waste Collection
- 🗑 Smart Bins
- 🚛 Recycling
- 🧹 Sanitation
""")

        elif agent == "Emergency":

            st.markdown("""
- 🚨 Fire Detection
- 🌫 Smoke Detection
- 🚑 Emergency Response
- 🏥 Disaster Management
""")

    # ==========================================
    # RIGHT PANEL
    # ==========================================

    with col2:

        st.subheader("💬 Ask AI Agent")

        query = st.text_area(
            "Question",
            placeholder="Example: Heavy traffic near the railway station during office hours.",
            height=180,
            label_visibility="collapsed"
        )
        st.write("You typed:", query)

        if st.button(
            "🚀 Ask AI Agent",
            use_container_width=True,
            type="primary"
        ):

            if not query.strip():

                st.warning("Please enter your question.")

            else:

                payload = {
                    "agent": agent.lower(),
                    "query": query
                }

                with st.spinner("🤖 Thinking..."):

                    try:

                        response = requests.post(
                            API_URL,
                            json=payload,
                            timeout=60
                        )

                        response.raise_for_status()

                        result = response.json()

                    except requests.exceptions.ConnectionError:

                        error = "Cannot connect to FastAPI backend."

                    except Exception as e:

                        error = str(e)

    # ==========================================
# RESPONSE
# ==========================================

    if error:

        st.error(error)

    elif result:

        st.divider()

        st.success(f"✅ {agent} Agent Response")

        st.markdown(f"## 🤖 {agent} AI Agent")

        with st.container(border=True):

            st.markdown(result["response"])

    st.divider()

    st.subheader("📌 Available AI Agents")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("🚦", "Traffic")

    with c2:
        st.metric("⚡", "Energy")

    with c3:
        st.metric("♻️", "Waste")

    with c4:
        st.metric("🚨", "Emergency")