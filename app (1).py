import base64
import requests
import streamlit as st


# ---------------------------------------------------------
# Configuración
# ---------------------------------------------------------

st.set_page_config(
    page_title="Clima",
    page_icon="🌤️",
    layout="centered"
)

CIUDADES_SUGERIDAS = [
    "Buenos Aires",
    "Córdoba",
    "Rosario",
    "Mendoza",
    "La Plata",
    "Mar del Plata",
    "Madrid",
    "Londres",
    "Nueva York",
    "Tokio",
]


# ---------------------------------------------------------
# Estilos
# ---------------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #eaf6ff 0%, #f8fbff 100%);
    }

    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0;
        color: #17324d;
    }

    .subtitle {
        text-align: center;
        color: #607d94;
        margin-top: 0;
        margin-bottom: 2rem;
    }

    .weather-card {
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid rgba(255, 255, 255, 0.9);
        border-radius: 24px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(45, 84, 110, 0.12);
        margin: 20px 0;
    }

    .location {
        text-align: center;
        color: #29485f;
        font-size: 1.35rem;
        font-weight: 700;
    }

    .condition {
        text-align: center;
        color: #607d94;
        font-size: 1.1rem;
        margin-bottom: 10px;
    }

    .temperature {
        text-align: center;
        font-size: 4.5rem;
        font-weight: 800;
        color: #17324d;
        line-height: 1;
        margin: 10px 0;
    }

    .detail-card {
        background: white;
        border-radius: 18px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 5px 18px rgba(45, 84, 110, 0.08);
        min-height: 105px;
    }

    .detail-title {
        color: #78909c;
        font-size: 0.9rem;
    }

    .detail-value {
        color: #17324d;
        font-size: 1.35rem;
        font-weight: 700;
        margin-top: 5px;
    }

    div.stButton > button {
        border-radius: 14px;
        font-weight: 700;
        height: 3rem;
    }

    div[data-testid="stFormSubmitButton"] button {
        border-radius: 14px;
        font-weight: 700;
        height: 3rem;
    }

    .footer {
        text-align: center;
        color: #78909c;
        font-size: 0.8rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Imágenes SVG según el clima
# ---------------------------------------------------------

def imagen_clima(tipo):
    imagenes = {
        "despejado": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450">
            <defs>
                <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0" stop-color="#70c9ff"/>
                    <stop offset="1" stop-color="#dff5ff"/>
                </linearGradient>
            </defs>
            <rect width="800" height="450" rx="30" fill="url(#sky)"/>
            <circle cx="400" cy="215" r="105" fill="#FFD54F"/>
            <g stroke="#FFD54F" stroke-width="15" stroke-linecap="round">
                <line x1="400" y1="65" x2="400" y2="25"/>
                <line x1="400" y1="365" x2="400" y2="405"/>
                <line x1="250" y1="215" x2="210" y2="215"/>
                <line x1="550" y1="215" x2="590" y2="215"/>
                <line x1="295" y1="110" x2="265" y2="80"/>
                <line x1="505" y1="110" x2="535" y2="80"/>
                <line x1="295" y1="320" x2="265" y2="350"/>
                <line x1="505" y1="320" x2="535" y2="350"/>
            </g>
        </svg>
        """,

        "nublado": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450">
            <defs>
                <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0" stop-color="#a9c7d8"/>
                    <stop offset="1" stop-color="#e7eef2"/>
                </linearGradient>
            </defs>
            <rect width="800" height="450" rx="30" fill="url(#sky)"/>
            <circle cx="315" cy="190" r="85" fill="#FFD866"/>
            <path d="M190 310 C170 240 225 190 290 200
                     C315 135 410 125 450 195
                     C525 165 610 215 600 290
                     C660 295 680 360 610 380
                     L230 380 C160 375 145 325 190 310Z"
                  fill="#F5F8FA"/>
        </svg>
        """,

        "lluvia": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450">
            <defs>
                <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0" stop-color="#667f91"/>
                    <stop offset="1" stop-color="#c4d5df"/>
                </linearGradient>
            </defs>
            <rect width="800" height="450" rx="30" fill="url(#sky)"/>
            <path d="M170 285 C155 215 215 165 280 175
                     C305 110 405 95 445 175
                     C520 145 600 195 590 270
                     C655 275 675 340 610 360
                     L205 360 C140 355 125 300 170 285Z"
                  fill="#EEF3F6"/>
            <g stroke="#42A5F5" stroke-width="14" stroke-linecap="round">
                <line x1="245" y1="385" x2="220" y2="425"/>
                <line x1="345" y1="385" x2="320" y2="425"/>
                <line x1="445" y1="385" x2="420" y2="425"/>
                <line x1="545" y1="385" x2="520" y2="425"/>
            </g>
        </svg>
        """,

        "tormenta": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450">
            <defs>
                <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0" stop-color="#263746"/>
                    <stop offset="1" stop-color="#66788a"/>
                </linearGradient>
            </defs>
            <rect width="800" height="450" rx="30" fill="url(#sky)"/>
            <path d="M165 275 C150 205 210 155 275 165
                     C300 100 400 85 440 165
                     C515 135 595 185 585 255
                     C650 260 670 325 605 350
                     L200 350 C135 345 120 290 165 275Z"
                  fill="#D8E0E5"/>
            <polygon points="400,285 345,365 390,365 355,435 465,335 415,335"
                     fill="#FFD54F"/>
        </svg>
        """,

        "nieve": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450">
            <defs>
                <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0" stop-color="#78b7e6"/>
                    <stop offset="1" stop-color="#e6f4ff"/>
                </linearGradient>
            </defs>
            <rect width="800" height="450" rx="30" fill="url(#sky)"/>
            <path d="M175 275 C160 205 220 155 285 165
                     C310 100 410 85 450 165
                     C525 135 600 185 590 255
                     C655 260 675 325 610 350
                     L210 350 C145 345 130 290 175 275Z"
                  fill="#F5F8FA"/>
            <g fill="#FFFFFF">
                <circle cx="245" cy="395" r="13"/>
                <circle cx="335" cy="370" r="11"/>
                <circle cx="430" cy="400" r="13"/>
                <circle cx="525" cy="375" r="11"/>
                <circle cx="600" cy="405" r="12"/>
            </g>
        </svg>
        """
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

st.markdown(
    '<div class="main-title">🌤️ Clima</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Información meteorológica actual de cualquier ciudad</div>',
    unsafe_allow_html=True
)

with st.form("formulario_clima"):

    st.markdown("### 📍 ¿Qué ciudad querés consultar?")

    ciudad_sugerida = st.selectbox(
        "Elegí una sugerencia o seleccioná "Escribir otra ciudad"",
        ["Escribir otra ciudad"] + CIUDADES_SUGERIDAS,
        key="ciudad_sugerida"
    )

    if ciudad_sugerida == "Escribir otra ciudad":
        st.text_input(
            "Ciudad",
            placeholder="Ejemplo: Buenos Aires",
            label_visibility="collapsed",
            key="ciudad"
        )
    else:
        st.text_input(
            "Ciudad",
            value=ciudad_sugerida,
            disabled=True,
            label_visibility="collapsed",
            key="ciudad"
        )

    consultar = st.form_submit_button(
        "🔎 Consultar clima",
        use_container_width=True
    )


if consultar:

    ciudad_busqueda = st.session_state.ciudad.strip()

    if not ciudad_busqueda:
        if st.session_state.ciudad_sugerida != "Escribir otra ciudad":
            ciudad_busqueda = st.session_state.ciudad_sugerida

    if not ciudad_busqueda:
        st.warning("Escribí una ciudad o seleccioná una sugerencia.")
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

            st.markdown(
                '<div class="weather-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="location">📍 {nombre}, {pais}</div>',
                unsafe_allow_html=True
            )

            st.image(
                imagen_clima(tipo_imagen),
                use_container_width=True
            )

            st.markdown(
                f'<div class="condition">{descripcion}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="temperature">{actual["temperature_2m"]}°C</div>',
                unsafe_allow_html=True
            )

            st.markdown("</div>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(
                    f"""
                    <div class="detail-card">
                        <div class="detail-title">Sensación térmica</div>
                        <div class="detail-value">
                            {actual["apparent_temperature"]} °C
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    f"""
                    <div class="detail-card">
                        <div class="detail-title">Humedad</div>
                        <div class="detail-value">
                            {actual["relative_humidity_2m"]} %
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col3:
                st.markdown(
                    f"""
                    <div class="detail-card">
                        <div class="detail-title">Viento</div>
                        <div class="detail-value">
                            {actual["wind_speed_10m"]} km/h
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown(
                f'<div class="footer">🕐 Actualizado: {actual["time"]} · Datos: Open-Meteo</div>',
                unsafe_allow_html=True
            )

        except requests.exceptions.RequestException:
            st.error(
                "No se pudo conectar con la API. "
                "Comprueba tu conexión a Internet."
            )

        except Exception as error:
            st.error(f"Ocurrió un error: {error}")
