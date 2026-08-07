import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/citizen/summarize"

def citizen_ai():

    st.title("📝 Citizen Services")
    st.caption("AI-powered complaint analysis")

    complaint = st.text_area(
        "Enter Complaint",
        placeholder="Example: Garbage has not been collected for five days and there is a bad smell.",
        height=180,
        key="complaint_box"
    )

    if st.button("🔍 Analyze Complaint", use_container_width=True):

        if not complaint.strip():
            st.warning("Please enter a complaint.")
            return

        try:

            with st.spinner("Analyzing complaint..."):

                response = requests.post(
                    API_URL,
                    json={"complaint": complaint},
                    timeout=30
                )

            response.raise_for_status()

            result = response.json()

            st.success("Complaint analyzed successfully!")

            c1, c2 = st.columns(2)

            with c1:
                st.metric("📂 Category", result["category"])
                st.metric("🏢 Department", result["department"])

            with c2:
                st.metric("😊 Sentiment", result["sentiment"])
                st.metric("⚠️ Priority", result["priority"])

            st.markdown("### 📄 Complaint Summary")

            st.success(result["summary"])

        except requests.exceptions.ConnectionError:
            st.error("Unable to connect to the FastAPI server.")

        except Exception as e:
            st.error(f"Error: {e}")