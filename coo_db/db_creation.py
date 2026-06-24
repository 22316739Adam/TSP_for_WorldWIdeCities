import sqlite3

DB_NAME = "cities.db"
TXT_FILE = "allcountries/allcountries.txt"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        geonameid VARCHAR(20),
        city_name VARCHAR(20),
        asci VARCHAR(20), 
        latitude REAL,
        longitude REAL, 
        country_code VARCHAR(5), 
        population INTEGER
        )
    """
)

with open(TXT_FILE, "r", encoding="UTF-8") as file:
    count = 0

    for line in file:
        parts = line.strip().split("\t") #Removing white spaces and creating the array based on the gap-in-between
        
        if len(parts) < 15:
            continue

        try: 
            geonameid = int(parts[0])
            city_name = parts[1]
            asci = parts[2]
            latitude = float(parts[4])
            longitude = float(parts[5])
            country_code = parts[8]
            population = int(parts[14]) if parts[14] else 0 #Using ternary for citizenless cities

            cursor.execute(
                """
                INSERT INTO cities (
                    geonameid, city_name, asci, latitude, longitude, country_code, population
                    )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    geonameid, city_name, asci, latitude, longitude, country_code, population
                )
            )

            count+=1 #Auto increasing after successful insertion
        except ValueError as e:
            print("Failure at row due ", e)

cursor.execute(
    """
    CREATE INDEX city_idx ON cities(city_name)
    """
)
cursor.execute(
    """
    CREATE INDEX asci_idx ON cities(asci)
    """
)

conn.commit()
print(f"Successful creation with total of {count}")
conn.close()
