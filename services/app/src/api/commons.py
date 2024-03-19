import requests
import json
import pandas as pd
from awesome_table.column import (Column, ColumnDType)

BACKEND_API_URL = "http://127.0.0.1:5001/api/v1"

FRONT_END_URL = "http://localhost:8512"

def get_df_from_api(BACKEND_API_URL):
    response = requests.get(BACKEND_API_URL)
    response.raise_for_status()
    df = pd.DataFrame.from_records(json.loads(response.content))
    return df


def get_front_end_column(column_name):
    if column_name == "player_name":
        return Column(name='name', label='Name')
    if column_name == "ppg":
        return Column(name='ppg', label='PPG')
    if column_name == "draft_player":
        return Column(name='draft_player', label='Draft', dtype=ColumnDType.ICONBUTTON, icon='fa-solid fa-share-nodes')
    if column_name == "is_drafted":
        return Column(name='is_drafted', label='Drafted?')
    if column_name == "team":
        return Column(name='team', label='Team')
    if column_name == "region":
        return Column(name='region', label='Region')
    if column_name == "seed":
        return Column(name='seed', label='Seed')






