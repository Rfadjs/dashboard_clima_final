import requests
import sqlite3
from datetime import datetime

API_KEY = "b9438af1d9c26c9dc3518db4021323af"

ciudades = [
    "Santiago",
    "La Serena",
    "Coquimbo",
    "Ovalle",
    "Combarbala"
]

conn = sqlite3.connect("clima.db")
cursor = conn.cursor()

for ciudad in ciudades:

    url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad},CL&appid={API_KEY}&units=metric"

    r = requests.get(url)
    data = r.json()

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO dim_ciudad(nombre,pais,lat,lon)
        VALUES (?,?,?,?)
    """,
    (
        data["name"],
        data["sys"]["country"],
        data["coord"]["lat"],
        data["coord"]["lon"]
    ))

    id_ciudad = cursor.lastrowid

    cursor.execute("""
        INSERT INTO dim_tiempo(fecha)
        VALUES (?)
    """,(fecha,))

    id_tiempo = cursor.lastrowid

    cursor.execute("""
        INSERT INTO fact_clima(
            id_ciudad,
            id_tiempo,
            temperatura,
            sensacion,
            humedad,
            presion,
            viento
        )
        VALUES (?,?,?,?,?,?,?)
    """,
    (
        id_ciudad,
        id_tiempo,
        data["main"]["temp"],
        data["main"]["feels_like"],
        data["main"]["humidity"],
        data["main"]["pressure"],
        data["wind"]["speed"]
    ))

conn.commit()
conn.close()

print("Datos insertados")