import streamlit as st

st.title("Settings")
settings = ["Console"]
selected_page = st.sidebar.radio("Select a setting...", settings)

if selected_page == "Console":
    st.write(f"{selected_page}")