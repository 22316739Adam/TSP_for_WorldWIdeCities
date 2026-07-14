import sqlite3 
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "cities.db")

def get_city_coordinates(city_name, country_code):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            city_name, latitude, longitude, country_code, population
        FROM cities
        WHERE LOWER(city_name) = LOWER(?) AND country_code = UPPER(?)
        LIMIT 1
        """, (city_name, country_code)
    )

    result = cursor.fetchone()
    conn.close()
    if result:
        return {
            "city": result[0], 
            "latitude": result[1], 
            "longitude": result[2], 
            "country": result[3]
        }
    else:
        return None
    
def get_cities_data(city_names=[("Paris", "FR"), ("Madrid", "ES")]):
    cities = []

    for city in city_names:
        result = get_city_coordinates(city[0], city[1])

        if result is None: 
            raise EOFError(f"City: {city_names[0]} not found ")
        cities.append(result)

    return cities

# print(get_cities_data())