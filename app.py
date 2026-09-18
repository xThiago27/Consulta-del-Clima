import streamlit as st
import requests


st.set_page_config(
    page_title="Clima",
    page_icon="🌤️",
    layout="centered"
)

st.title("🌤️ Consulta del clima")
st.write("Consulta el clima actual de cualquier ciudad usando una API pública.")


def buscar_ciudad(nombre):
    url = "https://geocoding-api.open-meteo.com/v1/search"

    parametros = {
        "name": nombre,
        "count": 1,
        "language": "es",
        "format": "json"
    }

    respuesta = requests.get(url, params=parametros, timeout=10)
    respuesta.raise_for_status()

    datos = respuesta.json()

    if "results" not in datos or not datos["results"]:
        return None

    return datos["results"][0]


def obtener_clima(latitud, longitud):
    url = "https://api.open-meteo.com/v1/forecast"

    parametros = {
        "latitude": latitud,
        "longitude": longitud,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "wind_speed_10m",
            "weather_code"
        ],
        "timezone": "auto"
    }

    respuesta = requests.get(url, params=parametros, timeout=10)
    respuesta.raise_for_status()

    return respuesta.json()


def descripcion_clima(codigo):
    estados = {
        0: "Despejado",
        1: "Principalmente despejado",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Niebla",
        48: "Niebla",
        51: "Llovizna",
        53: "Llovizna",
        55: "Llovizna intensa",
        61: "Lluvia",
        63: "Lluvia moderada",
        65: "Lluvia intensa",
        71: "Nieve",
        73: "Nieve moderada",
        75: "Nieve intensa",
        80: "Chaparrones",
        81: "Chaparrones moderados",
        82: "Chaparrones intensos",
        95: "Tormenta",
        96: "Tormenta con granizo",
        99: "Tormenta con granizo"
    }

    return estados.get(codigo, "Condición desconocida")


ciudad = st.text_input(
    "Escribe una ciudad",
    placeholder="Ejemplo: Buenos Aires"
)

if st.button("Consultar clima"):

    if not ciudad.strip():
        st.warning("Escribe una ciudad primero.")
    else:
        with st.spinner("Buscando información..."):
            try:
                ubicacion = buscar_ciudad(ciudad)

                if ubicacion is None:
                    st.error("No se encontró la ciudad.")
                    st.stop()

                clima = obtener_clima(
                    ubicacion["latitude"],
                    ubicacion["longitude"]
                )

                actual = clima["current"]

                nombre = ubicacion["name"]
                pais = ubicacion.get("country", "")

                st.success(f"Información encontrada para {nombre}, {pais}")

                st.subheader("🌡️ Clima actual")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Temperatura",
                        f"{actual['temperature_2m']} °C"
                    )

                with col2:
                    st.metric(
                        "Sensación térmica",
                        f"{actual['apparent_temperature']} °C"
                    )

                with col3:
                    st.metric(
                        "Humedad",
                        f"{actual['relative_humidity_2m']} %"
                    )

                st.write(
                    f"**Condición:** "
                    f"{descripcion_clima(actual['weather_code'])}"
                )

                st.write(
                    f"**Viento:** {actual['wind_speed_10m']} km/h"
                )

                st.write(
                    f"**Hora de actualización:** {actual['time']}"
                )

                st.caption(
                    "Datos meteorológicos proporcionados por Open-Meteo."
                )

            except requests.exceptions.RequestException:
                st.error(
                    "No se pudo conectar con la API. "
                    "Comprueba tu conexión a Internet."
                )

            except Exception as error:
                st.error(f"Ocurrió un error: {error}")
