import requests
import sqlite3
import random
from datetime import datetime

# Configuración
API_KEY = "b9438af1d9c26c9dc3518db4021323af"
ciudades = ["Santiago", "La Serena", "Coquimbo", "Ovalle", "Combarbala"]

# Conexión a la base de datos
conn = sqlite3.connect("clima.db")
cursor = conn.cursor()

# 1. Limpiar datos anteriores para que el Dashboard siempre tenga la "foto" más reciente
cursor.execute("DELETE FROM fact_clima")
cursor.execute("DELETE FROM dim_ciudad")
cursor.execute("DELETE FROM dim_tiempo")
conn.commit()

for ciudad in ciudades:
    # Petición a la API
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad},CL&appid={API_KEY}&units=metric"
    r = requests.get(url)
    data = r.json()

    # 2. Generar variación aleatoria para un resultado más realista y dinámico
    temp_final = round(data["main"]["temp"] + random.uniform(-2.0, 2.0), 1)
    humedad_final = max(0, min(100, data["main"]["humidity"] + random.randint(-5, 5)))
    
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Inserción en dimensiones
    cursor.execute("""
        INSERT INTO dim_ciudad(nombre, pais, lat, lon)
        VALUES (?, ?, ?, ?)
    """, (data["name"], data["sys"]["country"], data["coord"]["lat"], data["coord"]["lon"]))
    id_ciudad = cursor.lastrowid

    cursor.execute("INSERT INTO dim_tiempo(fecha) VALUES (?)", (fecha,))
    id_tiempo = cursor.lastrowid

    # Inserción en tabla de hechos
    cursor.execute("""
        INSERT INTO fact_clima(
            id_ciudad, id_tiempo, temperatura, sensacion, humedad, presion, viento
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        id_ciudad,
        id_tiempo,
        temp_final,
        data["main"]["feels_like"],
        humedad_final,
        data["main"]["pressure"],
        data["wind"]["speed"]
    ))

conn.commit()
conn.close()

print("Proceso completado: Datos limpios y actualizados insertados con variación.")