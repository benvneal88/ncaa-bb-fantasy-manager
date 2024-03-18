import streamlit as st
import src.api.commons as commons
from awesome_table import AwesomeTable
from awesome_table.column import (Column, ColumnDType)

st.title("Settings")
settings = ["Logs"]
selected_page = st.sidebar.radio("Select a setting...", settings)

if selected_page == "Logs":
    st.write(f"{selected_page}")
    df = commons.get_df_from_api(f"{commons.BACKEND_API_URL}/logs")
    AwesomeTable(
        df,
        columns=[
            Column(name='timestamp', label='Timestamp'),
            Column(name='message', label='Message'),
        ],
        show_search=False
    )

elif selected_page == "Console":
    st.write(f"{selected_page}")