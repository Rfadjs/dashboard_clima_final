import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# CONFIGURACION DE PAGINA
st.set_page_config(
    page_title="Dashboard Climático OpenWeather",
    layout="wide"
)

# TITULO
st.title("🌎 Dashboard Climático OpenWeather")

# CONEXION SQLITE
conn = sqlite3.connect("clima.db")

query = """
SELECT
    c.nombre,
    c.lat,
    c.lon,
    f.temperatura,
    f.sensacion,
    f.humedad,
    f.presion,
    f.viento,
    t.fecha
FROM fact_clima f
JOIN dim_ciudad c
    ON f.id_ciudad = c.id_ciudad
JOIN dim_tiempo t
    ON f.id_tiempo = t.id_tiempo
"""

df = pd.read_sql(query, conn)

conn.close()

# SI NO HAY DATOS
if df.empty:
    st.error("No hay datos en la base de datos.")
    st.stop()

# FILTRO LATERAL
st.sidebar.title("Filtros")

ciudad = st.sidebar.selectbox(
    "Selecciona una ciudad",
    ["Todas"] + list(df["nombre"].unique())
)

if ciudad != "Todas":
    df = df[df["nombre"] == ciudad]

# KPIs
st.subheader("Indicadores Principales")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🌡️ Temperatura Promedio",
    f"{round(df['temperatura'].mean(),1)} °C"
)

col2.metric(
    "💧 Humedad Promedio",
    f"{round(df['humedad'].mean(),1)} %"
)

col3.metric(
    "🌬️ Viento Promedio",
    f"{round(df['viento'].mean(),1)} m/s"
)

col4.metric(
    "📈 Presión Promedio",
    f"{round(df['presion'].mean(),1)} hPa"
)

st.divider()

# FILA 1
colA, colB = st.columns(2)

with colA:

    fig_temp = px.bar(
        df,
        x="nombre",
        y="temperatura",
        color="temperatura",
        title="Temperatura por Ciudad"
    )

    st.plotly_chart(fig_temp, use_container_width=True)

with colB:

    fig_hum = px.pie(
        df,
        names="nombre",
        values="humedad",
        title="Distribución de Humedad"
    )

    st.plotly_chart(fig_hum, use_container_width=True)

# FILA 2
colC, colD = st.columns(2)

with colC:

    fig_viento = px.bar(
        df,
        x="nombre",
        y="viento",
        color="viento",
        title="Velocidad del Viento"
    )

    st.plotly_chart(fig_viento, use_container_width=True)

with colD:

    fig_presion = px.bar(
        df,
        x="nombre",
        y="presion",
        color="presion",
        title="Presión Atmosférica"
    )

    st.plotly_chart(fig_presion, use_container_width=True)

st.divider()

# MAPA
st.subheader("📍 Ubicación de las Ciudades")

mapa = df[["lat", "lon"]].copy()
mapa.columns = ["lat", "lon"]

st.map(mapa)

# TABLA DE DATOS
st.subheader("📊 Datos Climáticos")

st.dataframe(df, use_container_width=True)