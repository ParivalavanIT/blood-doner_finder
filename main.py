import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


st.set_page_config(
    page_title="Blood doner finder",
    page_icon="🩸"
)


@st.cache_data
def load_data():

    return pd.read_excel("blood_data.xlsx")


data = load_data()

st.sidebar.title("Search Parameters")
blood_groups = data['Blood Group'].unique()
selected_blood_group = st.sidebar.selectbox(
    "Select Blood Group", [""] + list(blood_groups))

locations = data['Current Location'].unique()
selected_location = st.sidebar.text_input("Search Location", "")

name = st.sidebar.text_input("Search Name", "")

willing_to_donate = st.sidebar.checkbox("Willing to Donate for Any Emergency")


def fuzzy_search_location(input_location, locations):
    matches = process.extract(input_location, locations, limit=5)

    similar_locations = [match[0] for match in matches if match[1] >= 70]
    return similar_locations


filtered_data = data
if selected_blood_group:
    filtered_data = filtered_data[filtered_data['Blood Group']
                                  == selected_blood_group]
if selected_location:
    similar_locations = fuzzy_search_location(selected_location, locations)
    if similar_locations:
        filtered_data = filtered_data[filtered_data['Current Location'].isin(
            similar_locations)]
if name:
    filtered_data = filtered_data[filtered_data['Name'].str.contains(
        name, case=False, na=False)]

if willing_to_donate:
    filtered_data = filtered_data[filtered_data['Are you willing to donate blood for any emergency?'] == 'Yes']


st.title("Blood Donation Information")
if len(filtered_data) == 0:
    st.write("No matching records found.")
else:
    st.subheader("Blood Donation Recipients")
    for index, row in filtered_data.iterrows():
        st.write(f"**Name:** {row['Name']}")
        st.write(f"**Mobile Number:** {row['Mobile number']}")
        st.write(f"**Blood Group:** {row['Blood Group']}")
        st.write(f"**Location:** {row['Current Location']}")
        st.write("---")

st.write("""
    This app is created by the volunteers of Paavai YRC to find blood donors inside the Paavai campus.
""")
