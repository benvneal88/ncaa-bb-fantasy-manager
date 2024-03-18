import src.api.commons as commons
import streamlit as st


def get_team(team_name):
    df = commons.get_df_from_api(f"{commons.API_URL}/team/{team_name}")
    return df


def get_teams():
    df = commons.get_df_from_api(f"{commons.API_URL}/teams")
    return df


for team_name in get_teams()["team_name"].to_list():
    df = get_team(team_name)
    st.subheader(f"{team_name}")
    st.write(df)



# AwesomeTable(df, columns=[
#     Column(name='team_name', label='Team Name'),
#     Column(name='name', label='Name'),
#     Column(name='ppg', label='PPG'),
#     Column(name='is_drafted', label='Is Drafted'),
# ], show_search=True)