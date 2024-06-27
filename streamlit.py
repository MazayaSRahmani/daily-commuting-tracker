import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd


# Display Title and Description
st.title("Daily Commuting Tracker")
st.markdown("Enter your time of leaving and arrival below.")

# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing data
existing_data = conn.read(worksheet='tracker', usecols=list(range(12)), ttl=5)
existing_data = existing_data.dropna(how='all')

# list of stations
stations = [
    'Bogor Station','Cilebut Station',
    'Bojonggede Station','Citayam Station',
    'Depok Station','Depok Baru Station', 
    'Cawang Station','Tebet Station', 
    'Durian Kalibata Station'
    ]

transportation = [
    'Grab Bike',
    'Grab Car',
    'Gojek Bike',
    'Gojek Car',
    'Ojek Pangkalan',
    'Bis Kita Bogor',
    'Busway (BRT)',
    'Light Rapid Transit (LRT)',
    'Mass Rapid Transit (MRT)',
    'Personal Vechicle'
]

trip = [
    'Go to work',
    'Go home',
    'Go to other place',
    'Other'
]

# Data entry
with st.form(key='commuting_form'):
    commuting_date = st.date_input(label="Date*")
    commuting_trip = st.selectbox("Trip type", options=trip, index=None)
    departure_transportation = st.selectbox("Mode of transportation for departure", options=transportation, index=None)
    departure_to_station_time = st.time_input(label="Time of departure with transportation to station")
    departure_station = st.selectbox("Departure Station", options=stations,index=None)
    arrival_to_station_time = st.time_input(label="Time arrived to station")
    train_departure_time = st.time_input(label="Time of train departure")
    train_arrival_time = st.time_input(label="Time of train arrival")
    arrival_transportation = st.selectbox("Mode of transportation for arrival", options=transportation, index=None)
    arrival_station = st.selectbox("Arrival Station", options=stations,index=None)
    departure_from_station_time = st.time_input(label="Time of departure with transportation from station")
    time_of_arrival = st.time_input(label="Time of arrival")
    
    st.markdown("All field must be filled.")
    
    submit_button = st.form_submit_button(label="Submit records")
    
            

    commuting_records = pd.DataFrame(
        [
            {
                "DATE":commuting_date.strftime("%Y-%m-%d"),
                "TRIP":commuting_trip,
                "TRANSPORTATION_FOR_DEPARTURE":departure_transportation,
                "TIME_OF_DEPARTURE":departure_to_station_time,
                "DEPARTURE_STATION":departure_station,
                "TIME_ARRIVED_TO_STATION":arrival_to_station_time,
                "TIME_DEPARTURE_BY_TRAIN":train_departure_time,
                "TIME_ARRIVED_BY_TRAIN":train_arrival_time,
                "TRANSPORTATION_FOR_ARRIVAL":arrival_transportation,
                "ARRIVAL_STATION":arrival_station,
                "TIME_DEPARTURE_FROM_STATION":departure_from_station_time,
                "TIME_OF_ARRIVAL":time_of_arrival
            }
        ]
    )
    
    updated_records = pd.concat([existing_data,commuting_records], ignore_index=True)
    
    # update google sheets
    conn.update(worksheet="tracker", data=updated_records)
    
    st.success("Commuting data successfully recorded!")


