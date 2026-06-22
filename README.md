# Dashboard Climático - Big Data

## Justificación del Entorno
Se eligió el despliegue en la nube (Streamlit Cloud) por su facilidad de acceso y disponibilidad inmediata para las partes interesadas.

## Fuentes de Datos
- **API:** OpenWeatherMap.
- **Datos:** Indicadores meteorológicos (Temperatura, Humedad, Viento, Presión).
- **Objetivo:** Analizar variaciones climáticas territoriales para apoyar la toma de decisiones.

## Modelo de Datos
Se utilizó un modelo multidimensional simplificado (esquema estrella) con:
- **Hechos:** Métricas climáticas capturadas.
- **Dimensiones:** Ubicación geográfica y tiempo.

## Tecnologías
- **Python (Pandas):** Ingesta y normalización de datos.
- **Plotly:** Visualizaciones interactivas.
- **Streamlit:** Interfaz y despliegue web.

