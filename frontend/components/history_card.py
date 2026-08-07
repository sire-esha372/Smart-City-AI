import streamlit as st


def history_card(module, status, value, timestamp):

    icons = {
        "Traffic": "🚦",
        "Energy": "⚡",
        "Pollution": "🌍",
        "Emergency": "🚨",
        "Waste": "🗑️"
    }

    icon = icons.get(module, "📌")

    st.markdown(
        f"""
        <div style="
            background:#162235;
            border:1px solid #334155;
            border-radius:18px;
            padding:20px;
            margin-bottom:18px;
            box-shadow:0 8px 18px rgba(0,0,0,.25);
        ">

        <h3>{icon} {module}</h3>

        <p><b>Status:</b> {status}</p>

        <p><b>Value:</b> {value}</p>

        <p style="color:#94A3B8;">
        🕒 {timestamp}
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )