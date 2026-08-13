import streamlit as st
import requests

from PIL import Image
from io import BytesIO

from config import BACKEND_URL


# =========================================================
# API URL
# =========================================================

API_URL = f"{BACKEND_URL.rstrip('/')}/emergency/predict"


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
    # OPEN IMAGE
    # =====================================================

    try:

        original_image = Image.open(
            uploaded_file
        ).convert("RGB")

    except Exception as e:

        st.error(
            f"❌ Could not read image: {e}"
        )

        return

    # =====================================================
    # PREVIEW
    # =====================================================

    st.image(
        original_image,
        caption="Uploaded Image",
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

        try:

            # =================================================
            # RESIZE IMAGE FOR RENDER
            # =================================================

            image = original_image.copy()

            max_size = 1280

            if max(image.size) > max_size:

                image.thumbnail(
                    (max_size, max_size),
                    Image.Resampling.LANCZOS
                )

            # =================================================
            # COMPRESS IMAGE
            # =================================================

            image_buffer = BytesIO()

            image.save(
                image_buffer,
                format="JPEG",
                quality=80,
                optimize=True
            )

            image_bytes = (
                image_buffer.getvalue()
            )

            st.info(
                "🚨 Sending optimized image to Emergency AI..."
            )

            # =================================================
            # FILE PAYLOAD
            # =================================================

            files = {
                "file": (
                    "emergency.jpg",
                    image_bytes,
                    "image/jpeg"
                )
            }

            # =================================================
            # CALL FASTAPI
            # =================================================

            with st.spinner(
                "🚨 Running AI Detection..."
            ):

                response = requests.post(
                    API_URL,
                    files=files,
                    timeout=300
                )

            # =================================================
            # RESPONSE STATUS
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
            # JSON
            # =================================================

            data = response.json()

            st.success(
                "✅ Emergency Detection Completed!"
            )

            # =================================================
            # DETECTIONS
            # =================================================

            detections = data.get(
                "detections",
                []
            )

            # =================================================
            # RESULT IMAGE
            # =================================================

            image_url = data.get(
                "image_url"
            )

            if image_url:

                # Convert local backend URL
                # to Render backend URL

                if "127.0.0.1:8000" in image_url:

                    image_url = image_url.replace(
                        "http://127.0.0.1:8000",
                        BACKEND_URL.rstrip("/")
                    )

                elif "localhost:8000" in image_url:

                    image_url = image_url.replace(
                        "http://localhost:8000",
                        BACKEND_URL.rstrip("/")
                    )

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

                    else:

                        st.warning(
                            "Detection completed, "
                            "but the result image could not be loaded."
                        )

                        st.code(
                            f"Image URL: {image_url}"
                        )

                except Exception as e:

                    st.warning(
                        "Detection completed, "
                        "but the result image could not be displayed."
                    )

                    st.code(
                        str(e)
                    )

            # =================================================
            # SUMMARY
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
            # EMERGENCY DETECTED
            # =================================================

            else:

                st.session_state.alert_status = (
                    str(len(detections))
                )

                first = detections[0]

                st.session_state.alert_value = (
                    first["class"].title()
                )

                c1, c2, c3 = st.columns(3)

                with c1:

                    st.metric(
                        "Detected Object",
                        first["class"].title()
                    )

                with c2:

                    st.metric(
                        "Confidence",
                        f"{first['confidence'] * 100:.2f}%"
                    )

                with c3:

                    st.metric(
                        "Total Detections",
                        len(detections)
                    )

                st.error(
                    "🚨 Emergency Detected"
                )

                st.markdown(
                    "### 🔥 Detected Objects"
                )

                for item in detections:

                    st.write(
                        f"🔥 **{item['class'].title()}** "
                        f"— "
                        f"{item['confidence'] * 100:.2f}%"
                    )

        # =====================================================
        # TIMEOUT
        # =====================================================

        except requests.exceptions.Timeout:

            st.error(
                "⏱️ Emergency detection timed out."
            )

            st.info(
                "The Render backend took too long to process the image."
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
                f"❌ Request failed: {e}"
            )

        # =====================================================
        # OTHER ERROR
        # =====================================================

        except Exception as e:

            st.error(
                f"❌ Unexpected error: {e}"
            )