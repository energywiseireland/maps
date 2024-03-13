import pandas as pd
import requests
import folium
from folium.plugins import TagFilterButton
import tkinter as tk
from tkinter import messagebox

column_name = ["Job/No", "Job Name", "Post code" , "Customer" , "Category" , "Job Status" , "Ready to uplaod" , "Number" , "Last Updated" , "Date" ]
file_path = "C://Users//rwalia//Documents//map for dave//Book1.xlsx"

data = pd.read_excel(file_path , header= None , names = column_name)
df = data.loc[data['Job Status'].isin(['Complete Waiting Payment - Callbacks', 'Final Payment Received', 'PV - Waiting for Roof'])]


df['latitude'] = None
df['longitude'] = None

for index, row in df.iterrows():

    url = "https://maps-data.p.rapidapi.com/geocoding.php"
    print(row['Post code'])

    querystring = {"query": row['Post code'],"lang":"en","country":"ie"}

    headers = {
        "X-RapidAPI-Key": "8c500f1ad1mshb3e4f6d52177ab5p12f556jsnf347e4a5fb08",
        "X-RapidAPI-Host": "maps-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    address_data = response.json()

    df.at[index, 'latitude'] = address_data['data']['lat']  # Update with actual latitude value
    df.at[index, 'longitude'] = address_data['data']['lng']

print(df)

categories  = ['Complete Waiting Payment - Callbacks', 'Final Payment Received', 'PV - Waiting for Roof']
df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')


def get_marker_color(job_status):
    if job_status == 'Complete Waiting Payment - Callbacks':
        return 'blue'
    elif job_status == 'Final Payment Received':
        return 'green'
    elif job_status == 'PV - Waiting for Roof':
        return 'red'
    else:
        return 'gray'  # Default color


m = folium.Map([51., 1.], zoom_start=7)

# Unique job statuses for filtering
unique_job_statuses = df['Job Status'].unique().tolist()

# Add markers to the map with tags for filtering
for index, row in df.iterrows():
    if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"{row['Job Name']} - {row['Job Status']}",
            tags=[row['Job Status']] ,
            icon=folium.Icon(color = get_marker_color(row['Job Status'])) # Add job status as a tag for filtering
        ).add_to(m)

# Add TagFilterButton for job status filtering
TagFilterButton(unique_job_statuses).add_to(m)

m.save('maptry.html') 


