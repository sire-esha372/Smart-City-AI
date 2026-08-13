import streamlit as st
import requests

from config import BACKEND_URL


API_URL = f"{BACKEND_URL}/predict/waste"


def waste_page():

    st.title("🗑️ Waste Management")

    st.caption(
        "AI Powered Waste Classification using Computer Vision"
    )

    st.divider()

    col1, col2 = st.columns([1, 1])

    # ==========================================
    # UPLOAD SECTION
    # ==========================================

    with col1:

        st.subheader("📤 Upload Waste Image")

        uploaded_file = st.file_uploader(
            "Upload Waste Image",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )

        if uploaded_file:

            st.image(
                uploaded_file,
                use_container_width=True
            )

    # ==========================================
    # SUPPORTED CATEGORIES
    # ==========================================

    with col2:

        st.subheader("♻️ Supported Categories")

        st.info(
            """
- 📦 Cardboard

- 🍾 Glass

- 🥫 Metal

- 📄 Paper

- 🧴 Plastic

- 🗑️ Trash
            """
        )

    st.divider()

    # ==========================================
    # AI PREDICTION
    # ==========================================

    st.subheader("🤖 AI Prediction")

    if uploaded_file:

        if st.button(
            "🚀 Predict Waste",
            use_container_width=True
        ):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            try:

                # ==========================================
                # CALL RENDER BACKEND
                # ==========================================

                with st.spinner(
                    "♻️ Analyzing Waste Image... Please wait."
                ):

                    response = requests.post(
                        API_URL,
                        files=files,
                        timeout=180
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
                # GET RESULT
                # ==========================================

                prediction = result["prediction"]

                confidence = float(
                    result["confidence"]
                )

                st.success(
                    "✅ Prediction Completed!"
                )

                st.divider()

                # ==========================================
                # RESULTS
                # ==========================================

                c1, c2 = st.columns(2)

                with c1:

                    st.metric(
                        "🗑️ Waste Type",
                        prediction
                    )

                with c2:

                    st.metric(
                        "🎯 Confidence",
                        f"{confidence:.2f}%"
                    )

                st.progress(
                    min(confidence / 100, 1.0)
                )

                # ==========================================
                # CONFIDENCE MESSAGE
                # ==========================================

                if confidence >= 90:

                    st.success(
                        "Excellent confidence."
                    )

                elif confidence >= 75:

                    st.info(
                        "Good confidence."
                    )

                else:

                    st.warning(
                        "Low confidence."
                    )

            # ==========================================
            # TIMEOUT
            # ==========================================

            except requests.exceptions.Timeout:

                st.error(
                    "⏱️ The waste prediction request "
                    "took too long."
                )

                st.info(
                    "The Render backend may be waking up "
                    "or loading the waste model. "
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
            # OTHER ERROR
            # ==========================================

            except Exception as e:

                st.error(
                    f"❌ Unexpected error: {e}"
                )

    else:

        st.warning(
            "Upload an image first."
        )

    st.divider()

    # ==========================================
    # ABOUT
    # ==========================================

    st.subheader("ℹ️ About")

    st.write(
        """
This AI model classifies waste into six categories:

- 📦 Cardboard

- 🍾 Glass

- 🥫 Metal

- 📄 Paper

- 🧴 Plastic

- 🗑️ Trash

The model is trained on the TrashNet dataset using MobileNetV2.
"""
    )