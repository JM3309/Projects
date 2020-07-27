# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 22:09:13 2020

@author: Lenovo
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import  pydeck as pdk
import plotly.express as px



#DATA_URL ="https://data.cityofnewyork.us/api/views/h9gi-nx95/rows.csv?accessType=DOWNLOAD"
DATA_URL = "C:\\Users\\Lenovo\\Desktop\\datasets.csv"

st.title("Motor Vehicle Collisions in New York City")
st.markdown("## INTRODUCTION")
            
st.markdown("""This is a data analysis project by using streamlit dashboard to analysis motor vehicle collisions in New York city.
            \n The data comes from this [link](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95).It includes all police reported motor vehicles in NYC.
            \n 
            \n
            \n
            \n
            """)
##############################################################################
st.markdown("#### Define a function to load data and repoccessing data")
"""

\n
\n 1. First load data and since the datasets is kind of big,randomly select datapoint
\n 2. Drop the rows where the data is missing
\n 3. Turn the column name uppercase to lowercase


"""
##############################################################################
@st.cache(persist=True)

def load_data(nrows):
    row_length = 877182
    rows = sorted(random.sample(range(1, row_length+1), row_length- nrows))
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['CRASH_DATE', 'CRASH_TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    mask = data.isna().sum() / len(data) < 0.34
    data = data.loc[:, mask]
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data.rename(columns={"crash_date_crash_time": "date/time"}, inplace=True)
    #data = data[['date/time', 'latitude', 'longitude']]
    return data


data = load_data(nrows=100000)
original_data = data

if st.checkbox("show Raw data",False):
    st.subheader('Raw data')
    st.write(data)

"""
Data Analysis Part:
    \n
 \n 1. Where are the most people injured in NYC?
 \n 2. How many collisions occur during a given time of day?
 \n 3. Top 5 dangerous streets by affected class.


"""
st.header("Where are the most people injured in NYC?")
injured_people = st.slider("Number of persons injured in vehicle collisions", 0, 19)
st.map(data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how="any"))

st.header("How many collisions occur during a given time of day?")
hour = st.slider("Hour to look at", 0, 23)
original_data = data
data = data[data['date/time'].dt.hour == hour]

st.markdown("Vehicle collisions between %i:00 and %i:00" % (hour, (hour + 1) % 24))

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": np.average(data["latitude"]),
        "longitude": np.average(data["longitude"]),
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
        "HexagonLayer",
        data=data[['date/time', 'latitude', 'longitude']],
        get_position=["longitude", "latitude"],
        auto_highlight=True,
        radius=100,
        extruded=True,
        pickable=True,
        elevation_scale=3,
        elevation_range=[0, 1000],
        ),
    ],
))

st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
filtered = data[
    (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour + 1))
]
hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({"minute": range(60), "crashes": hist})
fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400)
st.write(fig)

st.header("Top 5 dangerous streets by affected class")
select = st.selectbox('Affected class', ['Pedestrians', 'Cyclists', 'Motorists'])

if select == 'Pedestrians':
    st.write(original_data.query("injured_pedestrians >= 1")[["on_street_name", "injured_pedestrians"]].sort_values(by=['injured_pedestrians'], ascending=False).dropna(how="any")[:5])

elif select == 'Cyclists':
    st.write(original_data.query("injured_cyclists >= 1")[["on_street_name", "injured_cyclists"]].sort_values(by=['injured_cyclists'], ascending=False).dropna(how="any")[:5])

else:
    st.write(original_data.query("injured_motorists >= 1")[["on_street_name", "injured_motorists"]].sort_values(by=['injured_motorists'], ascending=False).dropna(how="any")[:5])

 