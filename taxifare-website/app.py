import datetime
import streamlit as st
import requests
'''
# TaxiFare
'''
base_url = "https://taxifare-ydlcssklqq-ew.a.run.app/predict"

st.markdown('''
            Provide the details of your desired trip.
            ''')

with st.form("my_form"):
   st.write("Date and time")
   pickup_date = st.date_input("Pickup date")
   pickup_time = st.time_input("Pickup time")
   pickup_long = st.number_input("Pickup longitude")
   pickup_lat = st.number_input("Pickup latitude")
   dropoff_long = st.number_input("Dro-poff longitude")
   dropoff_lat = st.number_input("Drop-off latitude")
   passenger_count = st.number_input("Passenger count")

   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")

   pickup_dt = datetime.datetime.combine(pickup_date, pickup_time)

   if submitted:
       params = {
           "pickup_latitude": pickup_lat,
           "pickup_longitude": pickup_long,
           "dropoff_latitude": dropoff_lat,
           "dropoff_longitude": dropoff_long,
           "passenger_count": passenger_count,
           "pickup_datetime": pickup_dt,
           }

       st.write("Calculating the fare....")

       res = requests.get(url=base_url, params=params)
       st.write("Fare:", str(round(res.json()["fare_amount"], 2)))
