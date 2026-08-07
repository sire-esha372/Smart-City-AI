import streamlit as st

def load_css():
    st.markdown("""
<style>

/* =========================
   GOOGLE FONT
========================= */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body{
    font-family: 'Inter', sans-serif;
}

/* =========================
   APP
========================= */

.stApp{
    background:#0B1220;
    
}

/* Hide Streamlit Header & Footer */

header{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

#MainMenu{
    visibility:hidden;
}

/* Main container */

.block-container{
    padding-top:2rem;
    padding-left:2rem;
    padding-right:2rem;
    padding-bottom:2rem;
}

/* =========================
   SIDEBAR
========================= */

[data-testid="stSidebar"]{
    background:#111827;
    border-right:1px solid #26364F;
}

[data-testid="stSidebar"]{
    color:white;
}

[data-testid="stSidebarContent"]{
    padding-top:20px;
}

/* Sidebar Navigation */

.stRadio > div{
    gap:10px;
}

.stRadio label{
    color:#E2E8F0 !important;
    font-size:15px !important;
    font-weight:500 !important;
}

.stRadio [role="radiogroup"]{
    gap:8px;
}

/* =========================
   HEADER
========================= */

.dashboard-title{
    font-size:42px;
    font-weight:800;
    color:white;
    margin-bottom:0px;
}

.dashboard-subtitle{
    color:#94A3B8;
    font-size:18px;
    margin-bottom:40px;
}

/* =========================
   SECTION TITLE
========================= */

.section-title{
    font-size:28px;
    font-weight:700;
    color:white;
    margin-top:20px;
    margin-bottom:20px;
}

/* =========================
   METRIC CARDS
========================= */

.metric-card{

    background:#162235;

    border:1px solid #26364F;

    border-radius:18px;

    padding:25px;

    text-align:center;

    transition:0.3s ease;

    min-height:190px;

    box-shadow:0 10px 25px rgba(0,0,0,.35);

}

.metric-card:hover{

    transform:translateY(-6px);

    border-color:#38BDF8;

}

.metric-icon{

    font-size:34px;

}

.metric-title{

    color:#CBD5E1;

    font-size:18px;

    margin-top:12px;

    font-weight:600;

}

.metric-value{

    font-size:40px;

    font-weight:800;

    color:white;

    margin-top:10px;

}

.metric-subtitle{

    color:#94A3B8;

    margin-top:10px;

}

/* =========================
   BUTTONS
========================= */

.stButton>button{

    width:100%;

    height:58px;

    background:#162235;

    border:1px solid #2F415A;

    color:white;

    border-radius:12px;

    font-size:15px;

    font-weight:600;

    transition:0.3s;

}

.stButton>button:hover{

    background:#1E3A5F;

    border:1px solid #38BDF8;

    color:white;

}

/* =========================
   INFO / SUCCESS
========================= */

.stAlert{

    border-radius:12px;

}

/* =========================
   SCROLLBAR
========================= */

::-webkit-scrollbar{
    width:8px;
}

::-webkit-scrollbar-thumb{
    background:#334155;
    border-radius:20px;
}

::-webkit-scrollbar-track{
    background:#111827;
}

/* ==========================================
   AI MODULE CARDS
========================================== */

.module-card{
    background:#162235;
    border:1px solid #2C4158;
    border-radius:18px;
    padding:25px;
    min-height:150px;

    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;

    margin-bottom:20px;

    transition:all .3s ease;
    cursor:pointer;

    box-shadow:0 8px 20px rgba(0,0,0,.25);
}

.module-card:hover{
    transform:translateY(-6px);
    border-color:#38BDF8;
    box-shadow:0 15px 30px rgba(56,189,248,.20);
}

.module-icon{
    font-size:40px;
    margin-bottom:18px;
}

.module-title{
    font-size:17px;
    font-weight:600;
    color:white;
    text-align:center;
}

.metric-card hr{
    border:none;
    border-top:1px solid #334155;
    margin:15px 0;
}


/* ==========================================
   STREAMLIT METRIC FIX
========================================== */

[data-testid="stMetric"]{
    background:#162235 !important;
    border:1px solid #334155 !important;
    border-radius:16px !important;
    padding:18px !important;
}

[data-testid="stMetricLabel"]{
    color:#E2E8F0 !important;
    font-size:16px !important;
    font-weight:600 !important;
}

[data-testid="stMetricValue"]{
    color:#FFFFFF !important;
    font-size:34px !important;
    font-weight:800 !important;
}

[data-testid="stMetricDelta"]{
    color:#38BDF8 !important;
}

h1,h2,h3,h4,h5,h6{
    color:#FFFFFF !important;
}
/* ==========================================
   INPUT LABELS
========================================== */

/* Labels above inputs */
label,
.stTextInput label,
.stNumberInput label,
.stDateInput label,
.stTimeInput label,
.stSelectbox label,
.stTextArea label{
    color:#F8FAFC !important;
    font-weight:600 !important;
    font-size:16px !important;
}

/* Input boxes */
.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stTimeInput input{
    background:#162235 !important;
    color:#FFFFFF !important;
    border:1px solid #334155 !important;
    border-radius:10px !important;
}

/* Placeholder text */
.stTextInput input::placeholder{
    color:#94A3B8 !important;
}

/* ==========================================
   GENERAL TEXT
========================================== */

p{
    color:#F8FAFC !important;
}

span{
    color:#F8FAFC !important;
}

li{
    color:#F8FAFC !important;
}

/* ==========================================
   MARKDOWN
========================================== */

[data-testid="stMarkdownContainer"]{
    color:#F8FAFC !important;
}

[data-testid="stMarkdownContainer"] *{
    color:#F8FAFC !important;
}

[data-testid="stMarkdownContainer"] p{
    color:#F8FAFC !important;
}

[data-testid="stMarkdownContainer"] li{
    color:#F8FAFC !important;
}

[data-testid="stMarkdownContainer"] strong{
    color:#38BDF8 !important;
}

[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4{
    color:#38BDF8 !important;
}

/* ==========================================
   AGENT RESPONSE CARD
========================================== */

.agent-response{
    background:#162235;
    border:1px solid #334155;
    border-radius:16px;
    padding:25px;
    color:#F8FAFC !important;
}

.agent-response *{
    color:#F8FAFC !important;
}
/* ==========================================
   STREAMLIT TEXTAREA FIX
========================================== */

[data-testid="stTextArea"] textarea {
    background-color: #162235 !important;
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
    caret-color: #38BDF8 !important;
    border: 1px solid #334155 !important;
}

[data-testid="stTextArea"] textarea::placeholder {
    color: #94A3B8 !important;
    opacity: 1 !important;
}

/* Force the inner editable area */
textarea,
textarea:focus,
textarea:active {
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
    caret-color: #38BDF8 !important;
}
/* ==========================================
   FILE UPLOADER FIX
========================================== */

[data-testid="stFileUploader"]{
    color:#F8FAFC !important;
}

[data-testid="stFileUploader"] *{
    color:#F8FAFC !important;
}

[data-testid="stFileUploaderDropzone"]{
    background:#162235 !important;
    border:2px dashed #334155 !important;
    border-radius:12px !important;
}

[data-testid="stFileUploaderDropzone"] button{
    color:#F8FAFC !important;
    background:#1E293B !important;
    border:1px solid #334155 !important;
}

[data-testid="stFileUploaderDropzone"] small{
    color:#CBD5E1 !important;
}
/* ==========================================
   FILE UPLOADER - COMPLETE FIX
========================================== */

[data-testid="stFileUploader"] *{
    color:#F8FAFC !important;
}

[data-testid="stFileUploaderDropzone"]{
    background:#162235 !important;
    border:2px dashed #334155 !important;
}

[data-testid="stFileUploaderDropzone"] section{
    background:#162235 !important;
}

[data-testid="stFileUploaderDropzone"] small{
    color:#CBD5E1 !important;
}

[data-testid="stFileUploaderDropzone"] button{
    background:#1E293B !important;
    color:#FFFFFF !important;
    border:1px solid #334155 !important;
}

/* Upload icon */
[data-testid="stFileUploaderDropzone"] svg{
    fill:#38BDF8 !important;
}
/* ==========================================
   TIME INPUT FIX
========================================== */

[data-testid="stTimeInput"] input{
    background:#162235 !important;
    color:#FFFFFF !important;
    -webkit-text-fill-color:#FFFFFF !important;
    border:1px solid #334155 !important;
    border-radius:10px !important;
}

[data-testid="stTimeInput"] svg{
    fill:#FFFFFF !important;
}

[data-testid="stTimeInput"] button{
    color:#FFFFFF !important;
}

[data-testid="stTimeInput"] *{
    color:#FFFFFF !important;
}
/* ==========================================
   STREAMLIT 1.60 TIME INPUT FIX
========================================== */

/* Outer container */
[data-testid="stTimeInput"]{
    background:#162235 !important;
    border:1px solid #334155 !important;
    border-radius:12px !important;
}

/* Time text */
[data-testid="stTimeInputTimeDisplay"]{
    background:#162235 !important;
    color:#FFFFFF !important;
    -webkit-text-fill-color:#FFFFFF !important;
    font-weight:500 !important;
}

/* Actual input */
[data-testid="stTimeInput"] input{
    background:#162235 !important;
    color:#FFFFFF !important;
    -webkit-text-fill-color:#FFFFFF !important;
}

/* Dropdown arrow */
[data-testid="stTimeInput"] svg{
    fill:#FFFFFF !important;
}

/* Every child */
[data-testid="stTimeInput"] *{
    color:#FFFFFF !important;
}
/* ==========================================
   TIME PICKER POPUP FIX
========================================== */

[data-baseweb="popover"]{
    background:#162235 !important;
}

[data-baseweb="menu"]{
    background:#162235 !important;
}

[data-baseweb="menu"] *{
    color:#FFFFFF !important;
}

[data-baseweb="select"] *{
    color:#FFFFFF !important;
}

[data-baseweb="popover"] *{
    color:#FFFFFF !important;
}

[data-testid="stTimeInputTimeDisplay"]{
    color:#FFFFFF !important;
}

[role="listbox"]{
    background:#162235 !important;
}

[role="option"]{
    background:#162235 !important;
    color:#FFFFFF !important;
}

[role="option"]:hover{
    background:#2563EB !important;
}
/* ===== Streamlit 1.60 Time Input ===== */

[data-testid="stTimeInput"] input{
    background:#162235 !important;
    color:#FFFFFF !important;
    -webkit-text-fill-color:#FFFFFF !important;
    caret-color:#38BDF8 !important;
}

[data-testid="stTimeInput"]{
    background:#162235 !important;
}

[data-testid="stTimeInput"] input:focus{
    background:#162235 !important;
    color:#FFFFFF !important;
}

[data-testid="stTimeInput"] input::selection{
    background:#2563EB;
    color:#FFFFFF;
}
/* ==========================================
   DASHBOARD MODULE BUTTONS
========================================== */

div.stButton > button {

    height: 150px !important;

    border-radius: 18px !important;

    background: #162235 !important;

    border: 1px solid #334155 !important;

    color: #FFFFFF !important;

    font-size: 18px !important;

    font-weight: 600 !important;

    white-space: pre-line !important;

    transition: all .3s ease !important;

    box-shadow: 0 8px 20px rgba(0,0,0,.25);

}

div.stButton > button:hover{

    transform: translateY(-6px);

    border:1px solid #38BDF8 !important;

    box-shadow:0 15px 30px rgba(56,189,248,.20);

}
/* ==========================================
   DASHBOARD MODULE CARDS
========================================== */

div.stButton > button {

    min-height:150px !important;

    border-radius:18px !important;

    background:#162235 !important;

    border:1px solid #334155 !important;

    color:#FFFFFF !important;

    font-size:20px !important;

    font-weight:600 !important;

    white-space:pre-line !important;

    transition:all .3s ease !important;

    box-shadow:0 8px 20px rgba(0,0,0,.25);

}

div.stButton > button:hover{

    transform:translateY(-6px);

    border:1px solid #38BDF8 !important;

    box-shadow:0 15px 30px rgba(56,189,248,.20);

}

div.stButton > button p{

    color:#FFFFFF !important;

    text-align:center !important;

    line-height:1.7 !important;

}
/* Time input field */
[data-testid="stTimeInput"] input {
    background-color: #162235 !important;
    color: #FFFFFF !important;
    border: 1px solid #334155 !important;
}

/* Displayed selected time */
[data-testid="stTimeInputTimeDisplay"] {
    background-color: #162235 !important;
    color: #FFFFFF !important;
}
/* ==========================================
   TIME INPUT (STREAMLIT 1.60)
========================================== */

[data-testid="stTimeInput"]{
    background:#162235 !important;
}

[data-testid="stTimeInput"] > div{
    background:#162235 !important;
}

[data-testid="stTimeInput"] input{
    background:#162235 !important;
    color:#FFFFFF !important;
    -webkit-text-fill-color:#FFFFFF !important;
    caret-color:#38BDF8 !important;
}

[data-testid="stTimeInputTimeDisplay"]{
    background:#162235 !important;
    color:#FFFFFF !important;
    -webkit-text-fill-color:#FFFFFF !important;
}

[data-testid="stTimeInput"] svg{
    fill:#FFFFFF !important;
}

</style>
""", unsafe_allow_html=True)
