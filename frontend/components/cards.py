import streamlit as st

def metric_card(title, value, subtitle, icon):

    st.markdown(
        f"""
<div class="metric-card">

<div class="metric-icon">
{icon}
</div>

<div class="metric-title">
{title}
</div>

<div class="metric-value">
{value}
</div>

<div class="metric-subtitle">
{subtitle}
</div>

</div>
""",
        unsafe_allow_html=True,
    )