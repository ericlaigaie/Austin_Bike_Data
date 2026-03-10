# Import libraries/packages
import pandas as pd
import warnings
import numpy as np
import random
import folium
import branca.colormap as cm
import streamlit as st

from streamlit_folium import st_folium

# Get rid of warnings
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

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
station_map = folium.Map(location=(vs_lat, vs_lon), zoom_start=14)

df.apply(lambda row: folium.CircleMarker(
                        location=[row['Latitude'],row['Longitude']], 
                        tooltip=str(row['Kiosk ID'])+": "+row['Kiosk Name'],
                        fill=True,
                        fill_opacity=0.6
                        )
                    .add_to(station_map),
                axis=1)

st_map = st_folium(station_map, width=725)