import streamlit as st

if st.button("Logout"):
    st.session_state.logged_in = False
    st.switch_page("app.py")

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()

st.title("🏠 Welcome to the Sales Dashboard App")
st.write("Use the sidebar to navigate the pages.")

st.success("Login Verified ✔")
