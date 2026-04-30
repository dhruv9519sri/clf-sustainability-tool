import streamlit as st
from database import create_database

st.set_page_config(page_title="CLF Assessment", layout="wide")

st.title("CLF Sustainability Assessment Tool")

st.write("Welcome to the REAP CLF Sustainability Assessment")

st.page_link("pages/Survey.py", label="Start Survey / सर्वे शुरू करें")
st.page_link("pages/Admin_Login.py", label="Admin Login / प्रशासक लॉगिन")
