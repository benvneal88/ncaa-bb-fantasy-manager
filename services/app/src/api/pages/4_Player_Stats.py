import streamlit as st

import pandas as pd
import numpy as np

st.title("Player Stats")
regions = ["East", "West", "MidWest", "South"]
selected_page = st.sidebar.radio("Select a region...", regions)

def generate_fake_data():
    # Generate some fake data for demonstration
    dataframes = []
    for i in range(4*16):
        data = {
            'Column1': np.random.rand(5),
            'Column2': np.random.rand(5),
        }
        df = pd.DataFrame(data)
        dataframes.append(df)
    return dataframes


dataframes = generate_fake_data()

def get_region_stats(region):
    for row in range(0, 8):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            with col:
                st.subheader(f"Container {row + 1}-{j + 1}")
                st.write(dataframes[row + j])


if selected_page == "East":
    st.write("Welcome to the main page!")
    get_region_stats(selected_page)

elif selected_page == "West":
    st.write("Player Search page")
    get_region_stats(selected_page)

elif selected_page == "MidWest":
    st.write("Draft Night page")
    get_region_stats(selected_page)

elif selected_page == "South":
    st.write(f"Region: {selected_page}")
    get_region_stats(selected_page)


elif selected_page == "Setting":
    st.write("Setting page")
    # Add your code for Setting page here