import streamlit as st
import requests
import time

from config import BACKEND_URL


API_URL = f"{BACKEND_URL}/rag/ask"
HEALTH_URL = f"{BACKEND_URL}/"


def show():

    st.title("📚 Knowledge Base")

    st.markdown("### Government RAG Module")

    st.write(
        "Ask questions about the uploaded government documents."
    )

    question = st.text_area(
        "Enter your question",
        placeholder="Example: What is a smart city?",
        height=150
    )

    if st.button(
        "🤖 Ask AI",
        use_container_width=True
    ):

        if not question.strip():

            st.warning("Please enter a question.")
            return

        # ==========================================
        # STEP 1 — WAKE / CHECK RENDER
        # ==========================================

        try:

            with st.spinner(
                "🔄 Connecting to Smart City AI backend..."
            ):

                health_response = requests.get(
                    HEALTH_URL,
                    timeout=60
                )

            if health_response.status_code != 200:

                st.error(
                    f"❌ Backend health check failed: "
                    f"{health_response.status_code}"
                )

                st.code(
                    health_response.text
                )

                return

        except requests.exceptions.Timeout:

            st.error(
                "⏱️ Render backend did not wake up in time."
            )

            return

        except requests.exceptions.RequestException as e:

            st.error(
                "🔌 Could not connect to Render backend."
            )

            st.code(str(e))

            return

        # ==========================================
        # STEP 2 — RAG REQUEST
        # ==========================================

        payload = {
            "question": question.strip()
        }

        start_time = time.time()

        try:

            with st.spinner(
                "📚 Searching the knowledge base..."
            ):

                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=120
                )

            elapsed = round(
                time.time() - start_time,
                2
            )

            st.caption(
                f"RAG response time: {elapsed} seconds"
            )

            # ==========================================
            # SUCCESS
            # ==========================================

            if response.status_code == 200:

                try:

                    data = response.json()

                except ValueError:

                    st.error(
                        "❌ Backend returned invalid JSON."
                    )

                    st.code(
                        response.text
                    )

                    return

                answer = data.get("answer")

                if answer:

                    st.success("✅ Answer")

                    st.markdown(
                        f"""
                        <div style="
                            background:#1E293B;
                            padding:20px;
                            border-radius:10px;
                            border:1px solid #334155;
                            color:white;
                            font-size:16px;
                            line-height:1.6;
                        ">
                        {answer}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.warning(
                        "Backend responded, but no answer was returned."
                    )

                    st.json(data)

                return

            # ==========================================
            # BACKEND ERROR
            # ==========================================

            st.error(
                f"❌ RAG Backend Error {response.status_code}"
            )

            st.code(
                response.text
            )

        # ==========================================
        # RAG TIMEOUT
        # ==========================================

        except requests.exceptions.Timeout:

            elapsed = round(
                time.time() - start_time,
                2
            )

            st.error(
                f"⏱️ RAG request timed out after "
                f"{elapsed} seconds."
            )

            st.info(
                "The backend is reachable, but the RAG "
                "operation is taking too long."
            )

        # ==========================================
        # CONNECTION ERROR
        # ==========================================

        except requests.exceptions.ConnectionError as e:

            st.error(
                "🔌 Connection to the RAG backend failed."
            )

            st.code(
                str(e)
            )

        # ==========================================
        # OTHER REQUEST ERROR
        # ==========================================

        except requests.exceptions.RequestException as e:

            st.error(
                "❌ RAG request failed."
            )

            st.code(
                str(e)
            )

        # ==========================================
        # UNKNOWN ERROR
        # ==========================================

        except Exception as e:

            st.error(
                "❌ Unexpected error."
            )

            st.code(
                str(e)
            )