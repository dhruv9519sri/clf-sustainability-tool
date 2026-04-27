import streamlit as st

st.title("Admin Login")

password = st.text_input("Enter Password", type="password")

if st.button("Login"):
    if password == "admin123":
        st.session_state.logged_in = True
        st.success("Login Successful")
    else:
        st.error("Wrong Password")
