import streamlit as st
import requests
import pandas as pd
from components.history_card import history_card


def history_page():

    st.title("📜 Prediction History")

    st.write(
        "View all predictions stored in the Smart City database."
    )

    try:

        response = requests.get(
            "http://127.0.0.1:8000/history/"
        )

        if response.status_code != 200:
            st.error("Unable to fetch history.")
            return

        data = response.json()

        if len(data) == 0:

            st.info("No predictions available.")
            return

        df = pd.DataFrame(data)

        # --------------------------------------
        # FILTER
        # --------------------------------------

        module = st.selectbox(
            "Filter by Module",
            ["All"] + sorted(df["module"].unique().tolist())
        )

        if module != "All":
            df = df[df["module"] == module]

        # --------------------------------------
        # SEARCH
        # --------------------------------------

        search = st.text_input(
            "Search"
        )

        if search:

            df = df[
                df.astype(str)
                .apply(
                    lambda x: x.str.contains(
                        search,
                        case=False
                    )
                )
                .any(axis=1)
            ]

        st.write(f"Total Records : {len(df)}")

        for _, row in df.iterrows():

         history_card(
           row["module"],
           row["status"],
           row["value"],
           row["timestamp"],
         )

    

    except Exception as e:

        st.error(e)