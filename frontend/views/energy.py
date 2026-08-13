import streamlit as st
import requests
from datetime import date, datetime

from config import BACKEND_URL


def energy():

    # ==========================================
    # PAGE HEADER
    # ==========================================

    st.markdown(
        """
        <h1 style="color:white;font-size:48px;font-weight:800;">
        ⚡ Energy Analytics
        </h1>

        <p style="
        color:#CBD5E1;
        font-size:20px;
        margin-top:-10px;
        margin-bottom:30px;
        ">
        Predict city power consumption using Artificial Intelligence.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # ==========================================
    # INPUT SECTION
    # ==========================================

    st.markdown(
        "<h3 style='color:white;'>📅 Prediction Details</h3>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "<p style='color:#E2E8F0;font-weight:600;'>📅 Select Date</p>",
            unsafe_allow_html=True,
        )

        selected_date = st.date_input(
            "",
            value=date.today(),
            label_visibility="collapsed",
        )

    with col2:

        st.markdown(
            "<p style='color:#E2E8F0;font-weight:600;'>🕒 Select Time</p>",
            unsafe_allow_html=True,
        )

        selected_time = st.time_input(
            "",
            value=datetime.now().time(),
            label_visibility="collapsed",
        )

    st.divider()

    # ==========================================
    # BUTTON
    # ==========================================

    if st.button(
        "⚡ Predict Power Consumption",
        use_container_width=True,
    ):

        payload = {
            "date": str(selected_date),
            "time": selected_time.strftime("%H:%M"),
        }

        try:

            # ==========================================
            # CALL RENDER BACKEND
            # ==========================================

            with st.spinner(
                "⚡ Predicting power consumption... Please wait."
            ):

                response = requests.post(
                    f"{BACKEND_URL}/predict/power",
                    json=payload,
                    timeout=120,
                )

            # ==========================================
            # BACKEND STATUS
            # ==========================================

            if response.status_code != 200:

                st.error(
                    f"❌ Backend Error {response.status_code}"
                )

                st.code(response.text)

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

                st.code(response.text)

                return

            # ==========================================
            # SUCCESS CHECK
            # ==========================================

            if not result.get("success", False):

                st.error("❌ Power prediction failed.")

                st.json(result)

                return

            # ==========================================
            # SUCCESS
            # ==========================================

            st.success(
                "✅ Prediction Completed Successfully"
            )

            st.divider()

            # ==========================================
            # RESULTS
            # ==========================================

            st.markdown(
                "<h2 style='color:white;'>⚡ Power Prediction</h2>",
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns(2)

            with col1:

                power = round(
                    result["prediction"]["power_consumption"]
                )

                st.metric(
                    "Estimated Power Consumption",
                    f"{power} MW",
                )

            with col2:

                level = result["prediction"]["level"]

                # ==========================================
                # UPDATE DASHBOARD
                # ==========================================

                st.session_state.energy_status = level

                st.session_state.energy_value = (
                    f"{power} MW"
                )

                if level == "Low":

                    st.success(
                        "🟢 Low Demand"
                    )

                elif level == "Medium":

                    st.warning(
                        "🟠 Medium Demand"
                    )

                else:

                    st.error(
                        "🔴 High Demand"
                    )

            st.divider()

            # ==========================================
            # AI RECOMMENDATION
            # ==========================================

            if level == "Low":

                recommendation = """
✅ Electricity demand is expected to remain low.

No special grid management actions are required.
"""

            elif level == "Medium":

                recommendation = """
⚠ Moderate electricity demand expected.

Monitor the power distribution network and prepare for increasing load.
"""

            else:

                recommendation = """
🚨 High electricity demand predicted.

Consider load balancing, backup generation, and peak-hour monitoring.
"""

            st.info(recommendation)

        # ==========================================
        # TIMEOUT
        # ==========================================

        except requests.exceptions.Timeout:

            st.error(
                "⏱️ The backend took too long to respond."
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
                "🔌 Could not connect to the backend."
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
        # UNEXPECTED ERROR
        # ==========================================

        except Exception as e:

            st.error(
                f"❌ Unexpected error: {e}"
            )