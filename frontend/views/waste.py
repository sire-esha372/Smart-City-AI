import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict/waste"


def waste_page():

    st.title("🗑️ Waste Management")
    st.caption("AI Powered Waste Classification using Computer Vision")

    st.divider()

    col1, col2 = st.columns([1, 1])

    with col1:

        st.subheader("📤 Upload Waste Image")

        uploaded_file = st.file_uploader(
            "Upload Waste Image",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )

        if uploaded_file:
            st.image(uploaded_file, use_container_width=True)

    with col2:

        st.subheader("♻️ Supported Categories")

        st.info("""
- 📦 Cardboard
- 🍾 Glass
- 🥫 Metal
- 📄 Paper
- 🧴 Plastic
- 🗑️ Trash
""")

        st.subheader("🤖 AI Prediction")

        if uploaded_file:

            if st.button("🚀 Predict Waste", use_container_width=True):

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                with st.spinner("Analyzing Image..."):

                    response = requests.post(
                        API_URL,
                        files=files
                    )

                if response.status_code == 200:

                    result = response.json()

                    prediction = result["prediction"]
                    confidence = result["confidence"]

                    st.success("Prediction Completed!")

                    st.divider()

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

                    st.progress(confidence / 100)

                    if confidence >= 90:
                        st.success("Excellent confidence.")

                    elif confidence >= 75:
                        st.info("Good confidence.")

                    else:
                        st.warning("Low confidence.")

                else:
                    st.error(response.text)

        else:
            st.warning("Upload an image first.")

    st.divider()

    st.subheader("ℹ️ About")

    st.write("""
This AI model classifies waste into six categories:

- 📦 Cardboard
- 🍾 Glass
- 🥫 Metal
- 📄 Paper
- 🧴 Plastic
- 🗑️ Trash

The model is trained on the TrashNet dataset using MobileNetV2.
""")