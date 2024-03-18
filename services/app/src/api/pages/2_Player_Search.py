import json

import pandas as pd
from awesome_table import AwesomeTable
from awesome_table.column import (Column, ColumnDType)
import streamlit as st
import requests

import src.api.commons as commons
st.title("Player Search")


@st.cache_data
def fetch_player_data():
    url = f"{commons.BACKEND_API_URL}/players/"
    df = commons.get_df_from_api(url)
    return df

AwesomeTable(fetch_player_data(), columns=[
    Column(name='Team', label='Team'),
    Column(name='Region', label='Region'),
    Column(name='Name', label='Name'),
    Column(name='PPG', label='PPG'),
], show_search=True)


# data_schema = {
#     "team": "select",
#     "seed": "multiselect",
#     "region": "multiselect",
#     "name": "text",
# }
#
# all_widgets = sp.create_widgets(fetch_data(), data_schema)
# res = sp.filter_df(fetch_data(), all_widgets)
#st.write(res)




#
# st.dataframe(
#     fetch_data(),
#     column_config={
#         "ball_team_name": "Team",
#         "seed": st.column_config.NumberColumn(
#             "Seed",
#         ),
#         "region": "Region",
#         "ppg": st.column_config.NumberColumn(
#             "PPG",
#         ),
#     },
#     hide_index=True,
# )