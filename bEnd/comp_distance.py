<<<<<<< HEAD
#Haversine formula would be used in order to compute accurate distance between two cities on Earth

from math import radians, cos, sin, sqrt, atan2

EARTH_RADIUS = 6371

def haversine_distance(lat1, lon1, lat2, lon2):
    lat1 = radians(lat1)
    lon1 = radians(lat2)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    d_lat = lat2 - lat1
    d_lon = lon2 - lon1

    a = (sin(d_lat/2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon/2) ** 2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    distance = EARTH_RADIUS * c
    return distance

#After computing the distance between each two cities, distance matrix could be created
def build_mtx(cities):
    n = len(cities)

    mtx = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i==j: continue

            city1 = cities[i]
            city2 = cities[j]

            distance = haversine_distance(city1["latitude"], city1["longitude"], city2["latitude"], city2["longitude"])
            mtx[i][j] = round(distance, 5) #At 5 points of precision

    return mtx 
=======
#Haversine formula would be used in order to compute accurate distance between two cities on Earth

from math import radians, cos, sin, sqrt, atan2

EARTH_RADIUS = 6371

def haversine_distance(lat1, lon1, lat2, lon2):
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    d_lat = lat2 - lat1
    d_lon = lon2 - lon1

    a = (sin(d_lat/2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon/2) ** 2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    distance = EARTH_RADIUS * c
    return distance


def build_mtx(cities):
    n = len(cities)

    mtx = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i==j: continue

            city1 = cities[i]
            city2 = cities[j]

            #After computing the distance between each two cities, distance matrix could be created
            distance = haversine_distance(city1["latitude"], city1["longitude"], city2["latitude"], city2["longitude"])
            mtx[i][j] = round(distance, 5) #At 5 points of precision

    return mtx 
>>>>>>> master
