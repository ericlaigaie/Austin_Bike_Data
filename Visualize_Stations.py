import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.write("Hello - Testing a Simple Map in Streamlit")

# Load in kiosks and trips data
url = 'https://raw.githubusercontent.com/ericlaigaie/Austin_Bike_Data/refs/heads/main/Austin_MetroBike_Kiosk_Locations_20260308.csv'
kiosks = pd.read_csv(url)

#kiosks = pd.read_csv("C:/Users/ericl/Austin Bike Data - Streamlit App/Austin_MetroBike_Kiosk_Locations_20260308.csv")

# Process kiosk data into usable format
open_docks = kiosks[kiosks['Kiosk Status'] == 'active']
df = open_docks[['Kiosk ID','Kiosk Name','Location','Address','Number of Docks','Power Type']]
df['Coords'] = df['Location'].str.replace("(","").str.replace(")","").str.split(",")
df['Latitude'] = pd.to_numeric(df['Coords'].str[0])
df['Longitude'] = pd.to_numeric(df['Coords'].str[1])
df['Number of Docks'] = pd.to_numeric(df['Number of Docks'])
df = df.drop(['Location', 'Coords'], axis=1)

# Find average lat/lon to set as initial view state
vs_lat = df['Latitude'].mean()
vs_lon = df['Longitude'].mean()

# Create a scatterplot layer on pydeck
st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(latitude=vs_lat, longitude=vs_lon, zoom=13, bearing=0, pitch=0),
    layers=pdk.Layer(
        "ScatterplotLayer",
        df,
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
        radius_scale=30,
        radius_min_pixels=1,
        radius_max_pixels=100,
        get_position=['Longitude','Latitude'],
        get_radius=['Number of Docks'],
        get_fill_color=[255,140,0],
        get_line_color=[0,0,0],
    )
))