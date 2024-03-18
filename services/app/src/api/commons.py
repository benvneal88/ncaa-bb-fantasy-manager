import requests
import json
import pandas as pd

API_URL = "http://127.0.0.1:5001/api/v1"

FRONT_END_URL = "http://localhost:8512"

def get_df_from_api(api_url):
    response = requests.get(api_url)
    response.raise_for_status()
    df = pd.DataFrame.from_records(json.loads(response.content))
    return df