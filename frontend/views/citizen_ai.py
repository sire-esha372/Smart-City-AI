import streamlit as st
import requests

from config import BACKEND_URL


API_URL = f"{BACKEND_URL}/citizen/summarize"


def citizen_ai():

    st.title("📝 Citizen Services")
    st.caption("AI-powered complaint analysis")

    complaint = st.text_area(
        "Enter Complaint",
        placeholder="Example: Garbage has not been collected for five days and there is a bad smell.",
        height=180,
        key="complaint_box"
    )

    if st.button(
        "🔍 Analyze Complaint",
        use_container_width=True
    ):

        if not complaint.strip():

            st.warning(
                "Please enter a complaint."
            )

            return

        try:

            # ==========================================
            # CALL RENDER BACKEND
            # ==========================================

            with st.spinner(
                "📝 Analyzing complaint... Please wait."
            ):

                response = requests.post(
                    API_URL,
                    json={
                        "complaint": complaint
                    },
                    timeout=120
                )

            # ==========================================
            # BACKEND STATUS
            # ==========================================

            if response.status_code != 200:

                st.error(
                    f"❌ Backend Error {response.status_code}"
                )

                st.code(
                    response.text
                )

                return

            # ==========================================
            # JSON RESPONSE
            # ==========================================

            try:

                result = response.json()

            except ValueError:

                st.error(
                    "❌ Backend returned an invalid response."
                )

                st.code(
                    response.text
                )

                return

            # ==========================================
            # SUCCESS
            # ==========================================

            st.success(
                "✅ Complaint analyzed successfully!"
            )

            c1, c2 = st.columns(2)

            with c1:

                st.metric(
                    "📂 Category",
                    result["category"]
                )

                st.metric(
                    "🏢 Department",
                    result["department"]
                )

            with c2:

                st.metric(
                    "😊 Sentiment",
                    result["sentiment"]
                )

                st.metric(
                    "⚠️ Priority",
                    result["priority"]
                )

            st.markdown(
                "### 📄 Complaint Summary"
            )

            st.success(
                result["summary"]
            )

        # ==========================================
        # TIMEOUT
        # ==========================================

        except requests.exceptions.Timeout:

            st.error(
                "⏱️ The complaint analysis took too long."
            )

            st.info(
                "The Render backend may be waking up. "
                "Please try again."
            )

        # ==========================================
        # CONNECTION ERROR
        # ==========================================

        except requests.exceptions.ConnectionError:

            st.error(
                "🔌 Unable to connect to the backend."
            )

            st.info(
                f"Backend URL: {BACKEND_URL}"
            )

        # ==========================================
        # REQUEST ERROR
        # ==========================================

        except requests.exceptions.RequestException as e:

            st.error(
                f"❌ Backend request failed: {e}"
            )

        # ==========================================
        # OTHER ERROR
        # ==========================================

        except Exception as e:

            st.error(
                f"❌ Unexpected error: {e}"
            )