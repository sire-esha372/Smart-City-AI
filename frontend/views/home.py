import streamlit as st


def home_page():
    st.title("🏙️ Smart City AI Platform")

    st.write("Welcome to Smart City AI Platform")

    st.subheader("AI Modules")

    st.write("""
    🚦 Traffic Prediction

    ⚡ Power Consumption Prediction

    🌫️ Pollution Prediction

    🚨 Accident Detection

    🗑️ Waste Classification
    """)

    st.success("Select a module from the sidebar.")