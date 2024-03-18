from awesome_table import AwesomeTable
import src.api.commons as commons
import streamlit as st

from awesome_table.column import (Column, ColumnDType)


import api.utils.logger as log_util

logger = log_util.get_logger(__name__, 'INFO')

st.title("Player Stats")
regions = ["East", "West", "Midwest", "South"]
selected_page = st.radio("Select a region...", regions, horizontal=True)


def get_player_stats_by_region_seed(region, seed, play_in_game=False):
    df = commons.get_df_from_api(f"{commons.BACKEND_API_URL}/player_stats_by_seed_region/{region}/{seed}")
    team_name = ""
    if not df.empty:
        if play_in_game:
            team_name = df["team_name"].iloc[1]
        else:
            team_name = df["team_name"].iloc[0]
        #df = df.set_index('name')
        df = df.drop(columns=["team_name"])
    return team_name, df


def write_dataframes(region):
    first_round_matchups_dict = {
        "east": [(1, 16), (2, 15), (3, 14), (4, 13), (5, 12), (6, 11), (7, 10), (8, 9)],
        "west": [(1, 16, 16), (2, 15), (3, 14), (4, 13), (5, 12), (6, 11), (7, 10), (8, 9)],
        "midwest": [(1, 16, 16), (2, 15), (3, 14), (4, 13), (5, 12), (6, 11), (7, 10, 10), (8, 9)],
        "south": [(1, 16), (2, 15), (3, 14), (4, 13), (5, 12), (6, 11), (7, 10, 10), (8, 9)],
    }
    region = region.lower()
    matchups = first_round_matchups_dict.get(region)

    for row in range(0, 8):
        matchup_set = matchups[row]
        cols = st.columns(len(matchup_set))
        for col_index, col in enumerate(cols):
            with col:
                seed = matchup_set[col_index]
                if col_index == 3:
                    play_in_game = True
                else:
                    play_in_game = False

                team_name, df = get_player_stats_by_region_seed(region, seed, play_in_game=play_in_game)
                team_name_anchor = team_name.lower().replace(" ", "-")
                title = f"### [{seed} - {team_name}]({commons.FRONT_END_URL}/Teams#{team_name_anchor})"
                st.markdown(title, unsafe_allow_html=True)
                if not df.empty:
                    AwesomeTable(
                        df,
                        columns=[
                            Column(name='name', label='Name'),
                            Column(name='ppg', label='PPG'),
                            Column(name='draft_player', label='Draft', dtype=ColumnDType.ICONBUTTON, icon='fa-solid fa-share-nodes'),
                            Column(name='is_drafted', label='Is Drafted'),
                        ],
                        show_search=False,
                        key=f"{str(row)}-{str(col_index)}"
                    )
                    #st.write(df, unsafe_allow_html=True)


if selected_page == "East":
    st.write(f"{selected_page} Region")
    write_dataframes(selected_page)

elif selected_page == "West":
    st.write(f"{selected_page} Region")
    write_dataframes(selected_page)

elif selected_page == "MidWest":
    st.write(f"{selected_page} Region")
    write_dataframes(selected_page)

elif selected_page == "South":
    st.write(f"{selected_page} Region")
    write_dataframes(selected_page)