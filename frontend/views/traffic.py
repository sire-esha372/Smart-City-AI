import streamlit as st
import requests
from datetime import date, datetime, timedelta


def traffic_page():

    st.title("🚦 Traffic Intelligence")

    st.write("Predict city traffic using AI and live weather data.")

    # -----------------------------
    # City
    # -----------------------------

    city = st.text_input(
        "📍 City",
        "Hyderabad"
    )

    # -----------------------------
    # Date Selection
    # -----------------------------

    option = st.selectbox(
        "📅 Date",
        ["Today", "Tomorrow", "Custom"]
    )

    if option == "Today":

        selected_date = date.today()

    elif option == "Tomorrow":

        selected_date = date.today() + timedelta(days=1)

    else:

        st.markdown("#### 📅 Select Custom Date")

        col1, col2, col3 = st.columns(3)

        with col1:
            year = st.selectbox(
                "Year",
                [2025, 2026, 2027],
                index=1
            )

        with col2:
            month = st.selectbox(
                "Month",
                list(range(1, 13)),
                index=date.today().month - 1
            )

        with col3:
            day = st.selectbox(
                "Day",
                list(range(1, 32)),
                index=date.today().day - 1
            )

        selected_date = date(year, month, day)

    # -----------------------------
    # Time
    # -----------------------------

    selected_time = st.time_input(
        "🕒 Time",
        value=datetime.now().time()
    )

    # -----------------------------
    # Predict Button
    # -----------------------------

    if st.button("🚀 Predict Traffic", use_container_width=True):

        payload = {
            "city": city,
            "date": str(selected_date),
            "time": selected_time.strftime("%H:%M")
        }

        try:

            response = requests.post(
                "http://127.0.0.1:8000/predict/traffic",
                json=payload
            )

            if response.status_code != 200:
                st.error(response.text)
                return

            result = response.json()

            if result["success"]:

                st.success("✅ Prediction Completed")

                # -----------------------------
                # Location
                # -----------------------------

                st.markdown("## 📍 Location")

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

                # -----------------------------
                # Weather
                # -----------------------------

                st.markdown("## 🌤 Current Weather")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Temperature",
                        f"{result['weather']['temperature']} °C"
                    )

                with col2:
                    st.metric(
                        "Clouds",
                        f"{result['weather']['clouds']} %"
                    )

                with col3:
                    st.metric(
                        "Rain",
                        f"{result['weather']['rain']} mm"
                    )

                st.info(
                    f"{result['weather']['weather']} • "
                    f"{result['weather']['description']}"
                )

                st.divider()

                # -----------------------------
                # Prediction
                # -----------------------------

                st.markdown("## 🚦 Traffic Prediction")

                col1, col2 = st.columns(2)

                with col1:

                    traffic_volume = round(
                        result["prediction"]["traffic_volume"]
                    )

                    st.metric(
                        "Traffic Volume",
                        traffic_volume
                    )

                with col2:

                    level = result["prediction"]["traffic_level"]

                    # ==========================================
                    # UPDATE DASHBOARD CARD
                    # ==========================================

                    st.session_state.traffic_status = level
                    st.session_state.traffic_value = f"{traffic_volume} Vehicles/hr"

                    if level == "Low":
                        st.success(level)

                    elif level == "Medium":
                        st.warning(level)

                    else:
                        st.error(level)

            else:
                st.error("Prediction Failed")

        except Exception as e:
            st.error(f"Error: {e}")