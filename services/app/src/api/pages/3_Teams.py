import src.api.commons as commons
import streamlit as st
from awesome_table import AwesomeTable
from awesome_table.column import (Column, ColumnDType)


def get_team(team_name):
    df = commons.get_df_from_api(f"{commons.BACKEND_API_URL}/team/{team_name}")
    return df


def get_teams():
    df = commons.get_df_from_api(f"{commons.BACKEND_API_URL}/teams")
    return df


for team_name in get_teams()["team_name"].to_list():
    st.subheader(f"{team_name}")
    df = get_team(team_name)
    AwesomeTable(
        df,
        columns=[
            commons.get_front_end_column("player_name"),
            commons.get_front_end_column("ppg"),
            commons.get_front_end_column("draft_player"),
            commons.get_front_end_column("is_drafted"),
        ],
        show_search=False,
        key=f"{team_name}"
    )
    #st.write(df)


# AwesomeTable(df, columns=[
#     Column(name='team_name', label='Team Name'),
#     Column(name='name', label='Name'),
#     Column(name='ppg', label='PPG'),
#     Column(name='is_drafted', label='Is Drafted'),
# ], show_search=True)