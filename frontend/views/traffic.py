import streamlit as st
import requests

from config import BACKEND_URL
from datetime import date, datetime, timedelta


def traffic_page():

    st.title("🚦 Traffic Intelligence")

    st.write(
        "Predict city traffic using AI and live weather data."
    )

    st.divider()

    # =====================================================
    # CITY
    # =====================================================

    city = st.text_input(
        "📍 City",
        value="Hyderabad"
    )

    # =====================================================
    # DATE
    # =====================================================

    option = st.selectbox(
        "📅 Date",
        [
            "Today",
            "Tomorrow",
            "Custom"
        ]
    )

    if option == "Today":

        selected_date = date.today()

    elif option == "Tomorrow":

        selected_date = (
            date.today() + timedelta(days=1)
        )

    else:

        selected_date = st.date_input(
            "📅 Select Date",
            value=date.today()
        )

    # =====================================================
    # TIME
    # =====================================================

    selected_time = st.time_input(
        "🕒 Time",
        value=datetime.now().time()
    )

    st.divider()

    # =====================================================
    # PREDICT BUTTON
    # =====================================================

    if st.button(
        "🚀 Predict Traffic",
        use_container_width=True
    ):

        # =================================================
        # VALIDATE CITY
        # =================================================

        if not city.strip():

            st.warning(
                "⚠️ Please enter a city."
            )

            return

        # =================================================
        # PAYLOAD
        # =================================================

        payload = {
            "city": city.strip(),
            "date": selected_date.strftime(
                "%Y-%m-%d"
            ),
            "time": selected_time.strftime(
                "%H:%M"
            )
        }

        st.caption(
            "Connecting to Smart City AI backend..."
        )

        # =================================================
        # API REQUEST
        # =================================================

        try:

            with st.spinner(
                "🚦 Predicting traffic..."
            ):

                response = requests.post(
                    f"{BACKEND_URL.rstrip('/')}/predict/traffic",
                    json=payload,
                    timeout=300
                )

            # =================================================
            # HTTP ERROR
            # =================================================

            if response.status_code != 200:

                st.error(
                    f"❌ Backend Error: "
                    f"{response.status_code}"
                )

                st.code(
                    response.text
                )

                return

            # =================================================
            # JSON RESPONSE
            # =================================================

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

            # =================================================
            # SUCCESS CHECK
            # =================================================

            if not result.get(
                "success",
                False
            ):

                st.error(
                    "❌ Traffic prediction failed."
                )

                st.json(result)

                return

            # =================================================
            # SUCCESS
            # =================================================

            st.success(
                "✅ Traffic Prediction Completed!"
            )

            # =================================================
            # LOCATION
            # =================================================

            location = result.get(
                "location",
                {}
            )

            st.subheader(
                "📍 Location"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "City",
                    location.get(
                        "city",
                        city
                    )
                )

            with col2:

                st.metric(
                    "Country",
                    location.get(
                        "country",
                        "-"
                    )
                )

            # =================================================
            # WEATHER
            # =================================================

            weather = result.get(
                "weather",
                {}
            )

            st.subheader(
                "🌤 Current Weather"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Temperature",
                    f"{weather.get('temperature', 0)} °C"
                )

            with col2:

                st.metric(
                    "Clouds",
                    f"{weather.get('clouds', 0)} %"
                )

            with col3:

                st.metric(
                    "Rain",
                    f"{weather.get('rain', 0)} mm"
                )

            st.info(
                f"{weather.get('weather', '-')}"
                f" • "
                f"{weather.get('description', '-')}"
            )

            # =================================================
            # TRAFFIC PREDICTION
            # =================================================

            prediction = result.get(
                "prediction",
                {}
            )

            st.subheader(
                "🚦 Traffic Prediction"
            )

            traffic_volume = round(
                prediction.get(
                    "traffic_volume",
                    0
                )
            )

            traffic_level = prediction.get(
                "traffic_level",
                "Unknown"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Traffic Volume",
                    f"{traffic_volume} Vehicles/hr"
                )

            with col2:

                st.metric(
                    "Traffic Level",
                    traffic_level
                )

            # =================================================
            # SAVE FOR DASHBOARD
            # =================================================

            st.session_state.traffic_status = (
                traffic_level
            )

            st.session_state.traffic_value = (
                f"{traffic_volume} Vehicles/hr"
            )

            # =================================================
            # TRAFFIC STATUS
            # =================================================

            if traffic_level == "Low":

                st.success(
                    "🟢 Low Traffic"
                )

            elif traffic_level == "Medium":

                st.warning(
                    "🟠 Medium Traffic"
                )

            elif traffic_level == "High":

                st.error(
                    "🔴 High Traffic"
                )

            else:

                st.info(
                    f"Traffic Level: {traffic_level}"
                )

    # =====================================================
    # TIMEOUT
    # =====================================================

        except requests.exceptions.Timeout:

            st.error(
                "⏱️ The traffic request took too long."
            )

            st.info(
                "The backend may be waking up. "
                "Please try again."
            )

    # =====================================================
    # CONNECTION ERROR
    # =====================================================

        except requests.exceptions.ConnectionError as e:

            st.error(
                "🔌 Could not connect to the backend."
            )

            st.code(
                str(e)
            )

    # =====================================================
    # REQUEST ERROR
    # =====================================================

        except requests.exceptions.RequestException as e:

            st.error(
                "❌ Traffic request failed."
            )

            st.code(
                str(e)
            )

    # =====================================================
    # OTHER ERROR
    # =====================================================

        except Exception as e:

            st.error(
                "❌ Unexpected error."
            )

            st.code(
                str(e)
            )