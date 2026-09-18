# 🌤️ Consulta del Clima con Python y Streamlit

Aplicación web desarrollada en Python y Streamlit que permite consultar el clima actual de una ciudad utilizando la API pública de **Open-Meteo**.

## 🚀 Características

* Buscar ciudades por nombre.
* Obtener automáticamente las coordenadas de la ciudad.
* Consultar el clima actual.
* Mostrar:

  * Temperatura.
  * Sensación térmica.
  * Humedad.
  * Velocidad del viento.
  * Condición meteorológica.
  * Hora de actualización.
* Interfaz web realizada con Streamlit.
* No requiere API key para uso no comercial.

## 🛠️ Tecnologías utilizadas

* Python
* Streamlit
* Requests
* Pandas
* Open-Meteo API

## 📁 Estructura del proyecto

```text
clima-streamlit/
│
├── app.py
└── README.md
```

## ⚙️ Instalación

Primero hay que tener Python instalado.

Luego instalar las dependencias:

```bash
pip install streamlit requests pandas
```

## ▶️ Ejecutar el proyecto

Desde la carpeta del proyecto:

```bash
streamlit run app.py
```

Streamlit abrirá la aplicación en el navegador.

## 🌐 API utilizada

El proyecto utiliza Open-Meteo:

* API meteorológica: `https://api.open-meteo.com`
* API de geocodificación: `https://geocoding-api.open-meteo.com`

Open-Meteo proporciona datos meteorológicos mediante una API JSON y su servicio gratuito no requiere API key para uso no comercial.

## 📌 Funcionamiento

La aplicación realiza dos consultas:

### 1. Buscar la ciudad

Primero se consulta la API de geocodificación utilizando el nombre introducido por el usuario.

La API devuelve información como:

* Nombre de la ciudad.
* País.
* Latitud.
* Longitud.

### 2. Consultar el clima

Después se utilizan la latitud y longitud obtenidas para consultar la API meteorológica.

La aplicación recibe los datos en formato JSON y muestra la información mediante Streamlit.

## 📚 Ejemplo

Si el usuario introduce:

```text
Buenos Aires
```

la aplicación busca la ubicación correspondiente y posteriormente obtiene los datos meteorológicos de esa ubicación.

## 📄 Licencia y atribución

Los datos de Open-Meteo están disponibles bajo la licencia CC BY 4.0, por lo que el proyecto incluye la correspondiente atribución.

Open-Meteo permite el uso gratuito del servicio para aplicaciones no comerciales dentro de sus límites establecidos.

## 👨‍💻 Autor

Proyecto realizado como práctica de programación con Python, APIs y Streamlit.
