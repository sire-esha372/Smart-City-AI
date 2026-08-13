import streamlit as st
import requests

from PIL import Image
from io import BytesIO

from config import BACKEND_URL


# =========================================================
# API URL
# =========================================================

API_URL = (
    f"{BACKEND_URL.rstrip('/')}/emergency/predict"
)

st.info(f"Emergency API: {API_URL}")


# =========================================================
# EMERGENCY PAGE
# =========================================================

def emergency():

    st.title("🚨 Emergency Detection")

    st.markdown(
        "Detect **Fire** and **Smoke** using the YOLOv8 AI model."
    )

    st.divider()

    # =====================================================
    # UPLOAD
    # =====================================================

    st.subheader("📤 Upload Image")

    st.caption(
        "Supported formats: JPG, JPEG, PNG"
    )

    uploaded_file = st.file_uploader(
        "Upload emergency image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    if uploaded_file is None:

        st.info(
            "📷 Upload an image to detect fire or smoke."
        )

        return

    # =====================================================
    # ORIGINAL IMAGE
    # =====================================================

    st.subheader("📷 Original Image")

    st.image(
        uploaded_file,
        use_container_width=True
    )

    st.divider()

    # =====================================================
    # DETECT BUTTON
    # =====================================================

    if st.button(
        "🔥 Detect Emergency",
        use_container_width=True
    ):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type
            )
        }

        # =================================================
        # CALL BACKEND
        # =================================================

        try:

            with st.spinner(
                "🚨 Running AI Detection... "
                "The first request may take a little longer."
            ):

                response = requests.post(
                    API_URL,
                    files=files,
                    timeout=300
                )

            # =================================================
            # BACKEND ERROR
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

                data = response.json()

            except ValueError:

                st.error(
                    "❌ Backend returned an invalid response."
                )

                st.code(
                    response.text
                )

                return

            # =================================================
            # SUCCESS
            # =================================================

            st.success(
                "✅ Emergency Detection Completed!"
            )

            # =================================================
            # GET DETECTIONS
            # =================================================

            detections = data.get(
                "detections",
                []
            )

            # =================================================
            # RESULT IMAGE URL
            # =================================================

            image_url = data.get(
                "image_url"
            )

            # =================================================
            # FIX LOCALHOST URL
            # =================================================

            if image_url:

                image_url = image_url.replace(
                    "http://127.0.0.1:8000",
                    BACKEND_URL.rstrip("/")
                )

                image_url = image_url.replace(
                    "http://localhost:8000",
                    BACKEND_URL.rstrip("/")
                )

            # =================================================
            # DETECTION RESULT IMAGE
            # =================================================

            if image_url:

                st.divider()

                st.subheader(
                    "🎯 Detection Result"
                )

                try:

                    with st.spinner(
                        "Loading detection result..."
                    ):

                        image_response = requests.get(
                            image_url,
                            timeout=60
                        )

                    # -----------------------------------------
                    # IMAGE SUCCESS
                    # -----------------------------------------

                    if image_response.status_code == 200:

                        result_image = Image.open(
                            BytesIO(
                                image_response.content
                            )
                        )

                        st.image(
                            result_image,
                            caption="YOLO Detection Result",
                            use_container_width=True
                        )

                    # -----------------------------------------
                    # IMAGE ERROR
                    # -----------------------------------------

                    else:

                        st.warning(
                            "⚠️ Detection completed, "
                            "but the detection image could not be loaded."
                        )

                        st.caption(
                            f"Image server returned: "
                            f"{image_response.status_code}"
                        )

                        st.code(
                            image_url
                        )

                except requests.exceptions.Timeout:

                    st.warning(
                        "⏱️ Detection completed, "
                        "but the result image took too long to load."
                    )

                except Exception as e:

                    st.warning(
                        "⚠️ Detection completed, "
                        "but the result image could not be displayed."
                    )

                    st.code(
                        str(e)
                    )

            else:

                st.warning(
                    "⚠️ Backend did not return a detection image."
                )

            # =================================================
            # DETECTION SUMMARY
            # =================================================

            st.divider()

            st.subheader(
                "📊 Detection Summary"
            )

            # =================================================
            # NO DETECTION
            # =================================================

            if len(detections) == 0:

                st.session_state.alert_status = "0"

                st.session_state.alert_value = (
                    "No Alerts"
                )

                st.success(
                    "🟢 No Fire or Smoke Detected"
                )

            # =================================================
            # DETECTION FOUND
            # =================================================

            else:

                first = detections[0]

                # ---------------------------------------------
                # DASHBOARD STATE
                # ---------------------------------------------

                st.session_state.alert_status = (
                    str(len(detections))
                )

                st.session_state.alert_value = (
                    first["class"].title()
                )

                # ---------------------------------------------
                # METRICS
                # ---------------------------------------------

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Detected Object",
                        first["class"].title()
                    )

                with col2:

                    st.metric(
                        "Confidence",
                        f"{first['confidence'] * 100:.2f}%"
                    )

                with col3:

                    st.metric(
                        "Total Detections",
                        len(detections)
                    )

                # ---------------------------------------------
                # ALERT
                # ---------------------------------------------

                st.error(
                    "🚨 Emergency Detected"
                )

                # ---------------------------------------------
                # OBJECT LIST
                # ---------------------------------------------

                st.markdown(
                    "### 🔥 Detected Objects"
                )

                for item in detections:

                    class_name = item.get(
                        "class",
                        "Unknown"
                    )

                    confidence = float(
                        item.get(
                            "confidence",
                            0
                        )
                    )

                    st.write(
                        f"🔥 **{class_name.title()}** "
                        f"— "
                        f"{confidence * 100:.2f}%"
                    )

        # =====================================================
        # TIMEOUT
        # =====================================================

        except requests.exceptions.Timeout:

            st.error(
                "⏱️ Emergency detection timed out."
            )

            st.info(
                "The Render backend may be loading the "
                "YOLO model. Please try again."
            )

        # =====================================================
        # CONNECTION ERROR
        # =====================================================

        except requests.exceptions.ConnectionError as e:

            st.error(
                "🔌 Could not connect to the backend."
            )

            st.info(
                f"Backend URL: {BACKEND_URL}"
            )

            st.code(
                str(e)
            )

        # =====================================================
        # REQUEST ERROR
        # =====================================================

        except requests.exceptions.RequestException as e:

            st.error(
                "❌ Emergency request failed."
            )

            st.code(
                str(e)
            )

        # =====================================================
        # UNEXPECTED ERROR
        # =====================================================

        except Exception as e:

            st.error(
                "❌ Unexpected error."
            )

            st.code(
                str(e)
            )