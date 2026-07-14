import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import streamlit as st
from coo_db.retrieval_fromdb import get_cities_data
from bEnd.comp_distance import build_mtx
from bEnd.tsp import tsp_for

st.title("Travelling Salesman algorithm for shortest distance between cities")

st.write("Enter the number of cities wanted: ")

# Computing number of cities
num_cities = st.number_input(
    "Number of cities:",
    min_value=2,
    max_value=100, #theoretical limit
    step=1
)

cities = []
cities_with_cc = []

# dynamic city inputs
for i in range(num_cities):
    # textfield for city_name
    city = st.text_input(
        f"City {i + 1}"
    )

    cities.append(city)

    # textfield for country code
    country = st.text_input(
        f"Country Code for City {i + 1}"
    )

    cities_with_cc.append((city, country))

# solve button
if st.button("Solve TSP"):
    st.write("Cities entered:")

    c_idxs = [i for i in range(num_cities)]

    for city in cities_with_cc:
        st.write(city)

    cities_data = get_cities_data(cities_with_cc)
    distance_matrix = build_mtx(cities_data)
    best_route, best_distance = tsp_for(c_idxs, distance_matrix)

    solution = [cities[i] for i in c_idxs]

    st.write(f"Best route found: {solution} with total distance of {best_distance}")
    
