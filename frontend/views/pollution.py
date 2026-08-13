import streamlit as st
import requests

from config import BACKEND_URL


def pollution():

    # ==========================================
    # PAGE HEADER
    # ==========================================

    st.markdown(
        """
        <h1 style="color:white;font-size:48px;font-weight:800;">
        🌍 Environmental Monitoring
        </h1>

        <p style="
        color:#CBD5E1;
        font-size:20px;
        margin-top:-10px;
        margin-bottom:25px;
        ">
        Predict Air Quality Index (AQI) using live air quality data.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # ==========================================
    # CITY INPUT
    # ==========================================

    st.markdown(
        "<h3 style='color:white;'>📍 Enter City</h3>",
        unsafe_allow_html=True
    )

    city = st.text_input(
        "",
        value="Hyderabad",
        label_visibility="collapsed"
    )

    st.divider()

    # ==========================================
    # BUTTON
    # ==========================================

    if st.button(
        "🌍 Predict Air Quality",
        use_container_width=True
    ):

        if not city.strip():

            st.error(
                "❌ Please enter a city."
            )

            return

        payload = {
            "city": city.strip()
        }

        try:

            # ==========================================
            # CALL RENDER BACKEND
            # ==========================================

            with st.spinner(
                "🌍 Fetching live air quality and predicting AQI..."
            ):

                response = requests.post(
                    f"{BACKEND_URL}/predict/pollution/",
                    json=payload,
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
            # SUCCESS CHECK
            # ==========================================

            if not result.get("success", False):

                st.error(
                    "❌ Pollution prediction failed."
                )

                st.json(result)

                return

            # ==========================================
            # SUCCESS
            # ==========================================

            st.success(
                "✅ Prediction Completed"
            )

            st.divider()

            # ==========================================
            # LOCATION
            # ==========================================

            st.markdown(
                "## 📍 Location"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "City",
                    result["location"]["city"]
                )

            with col2:

                st.metric(
                    "Country",
                    result["location"]["country"]
                )

            st.divider()

            # ==========================================
            # AIR QUALITY
            # ==========================================

            st.markdown(
                "## 🌫 Current Air Quality"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "PM2.5",
                    f"{result['air_quality']['PM2.5']:.2f}"
                )

            with col2:

                st.metric(
                    "PM10",
                    f"{result['air_quality']['PM10']:.2f}"
                )

            with col3:

                st.metric(
                    "NO₂",
                    f"{result['air_quality']['NO2']:.2f}"
                )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "CO",
                    f"{result['air_quality']['CO']:.2f}"
                )

            with col2:

                st.metric(
                    "SO₂",
                    f"{result['air_quality']['SO2']:.2f}"
                )

            with col3:

                st.metric(
                    "O₃",
                    f"{result['air_quality']['O3']:.2f}"
                )

            st.divider()

            # ==========================================
            # AQI RESULT
            # ==========================================

            st.markdown(
                "## 🌍 AQI Prediction"
            )

            col1, col2 = st.columns(2)

            with col1:

                aqi = round(
                    result["prediction"]["aqi"]
                )

                st.metric(
                    "Predicted AQI",
                    aqi
                )

            level = result["prediction"]["level"]

            # ==========================================
            # UPDATE DASHBOARD
            # ==========================================

            st.session_state.pollution_status = (
                f"AQI {aqi}"
            )

            st.session_state.pollution_value = (
                level
            )

            with col2:

                if level == "Good":

                    st.success(
                        "🟢 Good"
                    )

                elif level == "Satisfactory":

                    st.info(
                        "🟢 Satisfactory"
                    )

                elif level == "Moderate":

                    st.warning(
                        "🟡 Moderate"
                    )

                elif level == "Poor":

                    st.warning(
                        "🟠 Poor"
                    )

                elif level == "Very Poor":

                    st.error(
                        "🔴 Very Poor"
                    )

                else:

                    st.error(
                        "⚫ Severe"
                    )

            st.divider()

            # ==========================================
            # AI RECOMMENDATION
            # ==========================================

            st.markdown(
                "## 💡 AI Recommendation"
            )

            if level in [
                "Good",
                "Satisfactory"
            ]:

                st.success(
                    "Air quality is healthy. "
                    "Outdoor activities are safe."
                )

            elif level == "Moderate":

                st.warning(
                    "Sensitive individuals should reduce "
                    "prolonged outdoor exposure."
                )

            elif level == "Poor":

                st.warning(
                    "Reduce outdoor activities and "
                    "consider wearing a mask."
                )

            else:

                st.error(
                    "Air quality is hazardous. "
                    "Stay indoors whenever possible."
                )

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