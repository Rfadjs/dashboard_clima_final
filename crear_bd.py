import sqlite3

conn = sqlite3.connect("clima.db")

cursor = conn.cursor()

# DIMENSION CIUDAD
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_ciudad (
    id_ciudad INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    pais TEXT,
    lat REAL,
    lon REAL
)
""")

# DIMENSION TIEMPO
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_tiempo (
    id_tiempo INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT
)
""")

# TABLA HECHOS
cursor.execute("""
CREATE TABLE IF NOT EXISTS fact_clima (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_ciudad INTEGER,
    id_tiempo INTEGER,
    temperatura REAL,
    sensacion REAL,
    humedad INTEGER,
    presion INTEGER,
    viento REAL,
    FOREIGN KEY(id_ciudad) REFERENCES dim_ciudad(id_ciudad),
    FOREIGN KEY(id_tiempo) REFERENCES dim_tiempo(id_tiempo)
)
""")

conn.commit()
conn.close()

print("Base creada correctamente")