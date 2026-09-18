import base64
import html
import requests
import streamlit as st


st.set_page_config(
    page_title="Clima",
    page_icon="🌤️",
    layout="centered"
)


# ---------------------------------------------------------
# Configuración
# ---------------------------------------------------------

CIUDADES_SUGERIDAS = [
    "Buenos Aires",
    "Córdoba",
    "Rosario",
    "Mendoza",
    "La Plata",
    "Mar del Plata",
    "Bariloche",
    "Salta",
    "Puerto Iguazú",
    "Ushuaia",
]


# Imágenes SVG embebidas dentro del propio archivo.
# De esta manera no hace falta guardar imágenes adicionales.
def imagen_clima(tipo):
    imagenes = {
        "despejado": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450">
            <rect width="800" height="450" rx="30" fill="#87CEEB"/>
            <circle cx="400" cy="220" r="105" fill="#FFD54F"/>
            <g stroke="#FFD54F" stroke-width="16" stroke-linecap="round">
                <line x1="400" y1="65" x2="400" y2="25"/>
                <line x1="400" y1="375" x2="400" y2="415"/>
                <line x1="245" y1="220" x2="205" y2="220"/>
                <line x1="555" y1="220" x2="595" y2="220"/>
                <line x1="290" y1="110" x2="262" y2="82"/>
                <line x1="510" y1="110" x2="538" y2="82"/>
                <line x1="290" y1="330" x2="262" y2="358"/>
                <line x1="510" y1="330" x2="538" y2="358"/>
            </g>
        </svg>
        """,

        "nublado": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450">
            <rect width="800" height="450" rx="30" fill="#B0BEC5"/>
            <circle cx="330" cy="220" r="100" fill="#FFD54F"/>
            <path d="M210 315 C190 245 245 195 305 205
                     C325 135 430 125 465 205
                     C540 175 615 225 605 300
                     C680 305 690 375 625 390
                     L245 390 C180 385 165 330 210 315Z"
                  fill="#ECEFF1"/>
        </svg>
        """,

        "lluvia": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450">
            <rect width="800" height="450" rx="30" fill="#78909C"/>
            <path d="M180 275 C165 205 225 155 285 165
                     C305 95 410 85 445 165
                     C520 135 595 185 585 260
                     C660 265 670 335 605 350
                     L215 350 C150 345 135 290 180 275Z"
                  fill="#ECEFF1"/>
            <g stroke="#42A5F5" stroke-width="15" stroke-linecap="round">
                <line x1="250" y1="370" x2="225" y2="415"/>
                <line x1="350" y1="370" x2="325" y2="415"/>
                <line x1="450" y1="370" x2="425" y2="415"/>
                <line x1="550" y1="370" x2="525" y2="415"/>
            </g>
        </svg>
        """,

        "tormenta": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450">
            <rect width="800" height="450" rx="30" fill="#37474F"/>
            <path d="M170 260 C155 190 215 140 275 150
                     C295 80 400 70 435 150
                     C510 120 585 170 575 245
                     C650 250 660 320 595 335
                     L205 335 C140 330 125 275 170 260Z"
                  fill="#CFD8DC"/>
            <polygon points="400,285 345,365 390,365 355,430 465,335 415,335"
                     fill="#FFD54F"/>
        </svg>
        """,

        "nieve": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450">
            <rect width="800" height="450" rx="30" fill="#90CAF9"/>
            <path d="M180 275 C165 205 225 155 285 165
                     C305 95 410 85 445 165
                     C520 135 595 185 585 260
                     C660 265 670 335 605 350
                     L215 350 C150 345 135 290 180 275Z"
                  fill="#ECEFF1"/>
            <g fill="#FFFFFF">
                <circle cx="250" cy="390" r="12"/>
                <circle cx="330" cy="365" r="10"/>
                <circle cx="430" cy="395" r="12"/>
                <circle cx="520" cy="370" r="10"/>
                <circle cx="590" cy="400" r="11"/>
            </g>
        </svg>
        """,
    }

    svg = imagenes.get(tipo, imagenes["nublado"])
    return "data:image/svg+xml;base64," + base64.b64encode(
        svg.encode("utf-8")
    ).decode("utf-8")


# ---------------------------------------------------------
# API
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# Descripción e imagen según código meteorológico
# ---------------------------------------------------------

def informacion_clima(codigo):
    if codigo == 0:
        return "Despejado", "despejado"

    if codigo in [1, 2, 3]:
        return "Parcialmente nublado / Nublado", "nublado"

    if codigo in [45, 48]:
        return "Niebla", "nublado"

    if codigo in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82]:
        return "Lluvia / Llovizna", "lluvia"

    if codigo in [71, 73, 75, 77, 85, 86]:
        return "Nieve", "nieve"

    if codigo in [95, 96, 99]:
        return "Tormenta", "tormenta"

    return "Condición desconocida", "nublado"


# ---------------------------------------------------------
# Interfaz
# ---------------------------------------------------------

st.title("🌤️ Consulta del clima")
st.write("Busca una ciudad y consulta su clima actual.")

st.subheader("📍 Elegí una ciudad")

# Form permite que Enter en el campo de texto envíe la consulta.
with st.form("formulario_clima"):
    
    ciudad = st.text_input(
        "Escribe una ciudad",
        placeholder="Ejemplo: Buenos Aires"

    ciudad_sugerida = st.selectbox(
        "Opciones predeterminadas",
        ["— Seleccionar una ciudad —"] + CIUDADES_SUGERIDAS
    )
    )

    consultar = st.form_submit_button(
        "🔎 Consultar clima",
        use_container_width=True
    )


if consultar:

    # Si el usuario escribió una ciudad, se utiliza esa.
    # Si no, se utiliza la ciudad seleccionada.
    ciudad_busqueda = ciudad.strip()

    if not ciudad_busqueda:
        if ciudad_sugerida != "— Seleccionar una ciudad —":
            ciudad_busqueda = ciudad_sugerida

    if not ciudad_busqueda:
        st.warning("Escribí una ciudad o seleccioná una opción.")
        st.stop()

    with st.spinner("Consultando el clima..."):

        try:
            ubicacion = buscar_ciudad(ciudad_busqueda)

            if ubicacion is None:
                st.error("No se encontró esa ciudad.")
                st.stop()

            clima = obtener_clima(
                ubicacion["latitude"],
                ubicacion["longitude"]
            )

            actual = clima["current"]

            nombre = ubicacion["name"]
            pais = ubicacion.get("country", "")
            codigo = actual["weather_code"]

            descripcion, tipo_imagen = informacion_clima(codigo)

            st.success(f"📍 {nombre}, {pais}")

            # Imagen dependiendo del clima
            st.image(
                imagen_clima(tipo_imagen),
                use_container_width=True
            )

            st.subheader(f"🌡️ {descripcion}")

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
                f"💨 **Viento:** {actual['wind_speed_10m']} km/h"
            )

            st.write(
                f"🕐 **Hora de actualización:** {actual['time']}"
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
