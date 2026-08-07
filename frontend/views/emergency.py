import streamlit as st
import requests
from PIL import Image
from io import BytesIO

API_URL = "http://127.0.0.1:8000/emergency/predict"


def emergency():

    st.title("🚨 Emergency Detection")
    st.markdown(
        "Detect **Fire** and **Smoke** using the YOLOv8 AI model."
    )

    st.divider()

    st.subheader("📤 Upload Image")
    st.caption("Supported formats: JPG, JPEG, PNG (Maximum 200 MB)")

    uploaded_file = st.file_uploader(
        "",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )

    if uploaded_file is not None:

        if st.button("🔥 Detect Emergency", use_container_width=True):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type,
                )
            }

            with st.spinner("Running AI Detection..."):
                response = requests.post(API_URL, files=files)

            if response.status_code == 200:

                data = response.json()

                st.success("Detection Completed Successfully!")

                # =====================================
                # Images
                # =====================================

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("📷 Original Image")
                    st.image(uploaded_file, use_container_width=True)

                with col2:
                    st.subheader("🎯 Detection Result")

                    try:
                        image_response = requests.get(data["image_url"])

                        if image_response.status_code == 200:

                            image = Image.open(
                                BytesIO(image_response.content)
                            )

                            st.image(
                                image,
                                use_container_width=True
                            )

                        else:
                            st.error("Unable to load detection image.")

                    except Exception as e:
                        st.error(f"Image Error: {e}")

                st.divider()

                # =====================================
                # Detection Summary
                # =====================================

                st.subheader("📊 Detection Summary")

                if len(data["detections"]) == 0:

                    # ----------------------------
                    # UPDATE DASHBOARD
                    # ----------------------------

                    st.session_state.alert_status = "0"
                    st.session_state.alert_value = "No Alerts"

                    st.success("🟢 No Fire or Smoke Detected")

                else:

                    first = data["detections"][0]

                    # ----------------------------
                    # UPDATE DASHBOARD
                    # ----------------------------

                    st.session_state.alert_status = str(len(data["detections"]))
                    st.session_state.alert_value = first["class"].title()

                    c1, c2, c3 = st.columns(3)

                    with c1:
                        st.metric(
                            "Detected Object",
                            first["class"].title(),
                        )

                    with c2:
                        st.metric(
                            "Confidence",
                            f"{first['confidence']*100:.2f}%"
                        )

                    with c3:
                        st.metric(
                            "Total Detections",
                            len(data["detections"])
                        )

                    st.error("🚨 Emergency Detected")

                    st.markdown("### Detected Objects")

                    for item in data["detections"]:

                        st.write(
                            f"🔥 **{item['class'].title()}** — {item['confidence']*100:.2f}%"
                        )

            else:

                st.error("Unable to connect to the FastAPI server.")