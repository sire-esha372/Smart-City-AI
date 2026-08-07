import streamlit as st


def load_css():

    st.markdown("""
<style>

/* =====================================================
   GOOGLE FONT
===================================================== */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* =====================================================
   GLOBAL
===================================================== */

html,body,[class*="css"]{
    font-family:'Inter',sans-serif;
}

.stApp{
    background:#0B1220;
}

#MainMenu,
header,
footer{
    visibility:hidden;
}

.block-container{
    padding:2rem;
}

/* =====================================================
   SIDEBAR
===================================================== */

[data-testid="stSidebar"]{
    background:#111827;
    border-right:1px solid #26364F;
}

[data-testid="stSidebarContent"]{
    padding-top:20px;
}

/* =====================================================
   TITLES
===================================================== */

.dashboard-title{

    font-size:42px;

    font-weight:800;

    color:#FFFFFF;

    margin-bottom:5px;

}

.dashboard-subtitle{

    font-size:18px;

    color:#94A3B8;

    margin-bottom:35px;

}

.section-title{

    font-size:28px;

    font-weight:700;

    color:white;

    margin-bottom:20px;

}

/* =====================================================
   METRIC CARDS
===================================================== */

.metric-card{

    background:#162235;

    border:1px solid #2C4158;

    border-radius:18px;

    padding:25px;

    min-height:190px;

    text-align:center;

    transition:.3s;

    margin-bottom:20px;

    box-shadow:0 8px 20px rgba(0,0,0,.25);

}

.metric-card:hover{

    transform:translateY(-6px);

    border-color:#38BDF8;

    box-shadow:0 15px 35px rgba(56,189,248,.15);

}

.metric-icon{

    font-size:40px;

    margin-bottom:15px;

}

.metric-title{

    color:#CBD5E1;

    font-size:18px;

    font-weight:600;

}

.metric-value{

    color:white;

    font-size:38px;

    font-weight:800;

    margin-top:12px;

}

.metric-subtitle{

    color:#94A3B8;

    margin-top:12px;

    font-size:15px;

}

/* =====================================================
   MODULE CARDS
===================================================== */

.module-card{

    background:#162235;

    border:1px solid #2C4158;

    border-radius:18px;

    padding:28px;

    text-align:center;

    min-height:150px;

    margin-bottom:20px;

    transition:.3s;

    cursor:pointer;

}

.module-card:hover{

    transform:translateY(-6px);

    border-color:#38BDF8;

    box-shadow:0 15px 30px rgba(56,189,248,.18);

}

.module-icon{

    font-size:42px;

    margin-bottom:18px;

}

.module-title{

    color:white;

    font-size:17px;

    font-weight:600;

}

/* =====================================================
   BUTTONS
===================================================== */

.stButton>button{

    width:100%;

    height:56px;

    background:#162235;

    color:white;

    border-radius:12px;

    border:1px solid #334155;

    font-weight:600;

}

.stButton>button:hover{

    background:#2563EB;

    border-color:#38BDF8;

    color:white;

}

/* =====================================================
   INPUTS
===================================================== */

.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stTimeInput input,
textarea{

    background:#162235 !important;

    color:#F8FAFC !important;

    border:1px solid #334155 !important;

    border-radius:10px !important;

    -webkit-text-fill-color:#F8FAFC !important;

}

textarea::placeholder{

    color:#94A3B8 !important;

}

</style>
""", unsafe_allow_html=True)