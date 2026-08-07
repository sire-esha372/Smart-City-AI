import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/rag/ask"


def show():

    st.title("📚 Knowledge Base")
    st.markdown("### Government RAG Module")
    st.write("")
    st.write("Ask questions about the uploaded government documents.")

    question = st.text_area(
        "Enter your question",
        placeholder="Example: What is a smart city?"
    )

    if st.button("🤖 Ask AI", use_container_width=True):

        if question.strip() == "":
            st.warning("Please enter a question.")
            return

        with st.spinner("Searching the knowledge base..."):

            try:

                response = requests.post(
                    API_URL,
                    json={
                        "question": question
                    },
                    timeout=60
                )

                if response.status_code == 200:

                    answer = response.json()["answer"]

                    st.success("Answer")

                    st.markdown(
                        f"""
<div style='
background:#1E293B;
padding:20px;
border-radius:10px;
border:1px solid #334155;
color:white;
font-size:16px;
'>
{answer}
</div>
""",
                        unsafe_allow_html=True
                    )

                else:

                    st.error("Backend Error")
                    st.code(response.text)

            except Exception as e:

                st.error("Cannot connect to FastAPI backend.")
                st.code(str(e))