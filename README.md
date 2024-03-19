<p align=center><img src=./Imagenes/data_im.jpg width="400px"></p>

# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>

# <h1 align=center>**`Machine Learning Operations (MLOps)`**</h1>

---

<details>
<summary><strong>Índice</strong></summary>

1. [Introducción](#Introducción)
2. [Objetivo](#Objetivo)
3. [Diccionario](#Diccionario-de-Datos)
4. [Extracción, Transformación y Carga](#Extracción,-Transformación-y-Carga)
5. [Análisis Exploratorio de Datos](#Análisis-Exploratorio-de-Datos)
6. [API](#API)
   - [Desployment](#Deployment)
7. [Machine Learning](#Machine-Learning)
8. [Stack Tecnológico](#Stack-Tecnológico)
9. [Video Explicativo](#Video)
10. [Contacto](#Contacto)

</details>

## **Introducción**

---

Este proyecto se enfoca en la creación de una API para gestionar y analizar datos de juegos proporcionados por Steam. Steam es una plataforma de distribución digital de videojuegos ampliamente utilizada por jugadores de todo el mundo. Los datos recopilados de esta plataforma contienen información valiosa sobre los juegos, sus usuarios y sus interacciones.

## **Objetivo**

---

El objetivo principal de este proyecto es desarrollar una API que permita realizar consultas, análisis y recomendaciones específicas utilizando los conjuntos de datos de Steam. Esto incluye la capacidad de buscar información detallada sobre juegos, usuarios, transacciones, así como realizar análisis de tendencias y patrones de comportamiento. Además, se pretende implementar funcionalidades de recomendación de juegos basadas en el análisis de datos. Mi rol en este proyecto abarcó el diseño y desarrollo de la infraestructura de datos, la implementación de algoritmos de aprendizaje automático y la gestión del proceso de entrega y despliegue del proyecto.

## **Diccionario de Datos**

---

<img src=./Imagenes/Diccionario.jpg width="450px"></p>

## **Extracción, Transformación y Carga**

---

Se realizó la lectura de los dataset con el formato correcto, incluyendo su limpieza, organización y preparación para optimizar las  consultas que se realicen, el rendimiento de la API, el entrenamiento del modelo de aprendizaje automático.

### User Reviews

- Se lee el archivo user_reviews.json y se carga en un DataFrame.
- Se expanden los diccionarios en las listas de la columna 'reviews' en nuevas columnas.
- Se realiza la limpieza de los datos, eliminando emojis, símbolos no ASCII y filas duplicadas.
- Se realiza el análisis de sentimiento utilizando VADER de NLTK.
- Se realiza la limpieza adicional en la columna 'posted', convirtiendo los nombres de los meses a números y cambiando el formato de fecha.
- Se guarda el DataFrame resultante en un archivo CSV.

### Steam Games

- Se lee el archivo steam_games.json y se carga en un DataFrame.
- Se realizan transformaciones para limpiar los datos, convirtiendo las columnas que son listas a cadenas de texto y convirtiendo la columna 'release_date' al formato de fecha.
- Se eliminan filas donde todos los valores son nulos, se reemplazan los valores NaN con None y se eliminan filas duplicadas.
- Se guarda el DataFrame resultante en un archivo CSV.

### Users Items

- Se lee el archivo users_items.json y se carga en un DataFrame.
- Se expanden los diccionarios en las listas de la columna 'items' en nuevas columnas.
- Se realiza la limpieza de los datos, eliminando filas duplicadas y valores nulos.
- Se guarda el DataFrame resultante en un archivo CSV.

En este archivo se puede ver cómo se realizó y desarrolló el código: [ETL](https://github.com/delfinap5/PI-MLOps_STEAM_DELFINA/blob/main/ETL%20y%20EDA/ETL.ipynb)

## **Análisis Exploratorio de Datos**

---

### Steam Games

- Información General:

  El conjunto de datos contiene información sobre juegos de Steam, con un total de 32,135 entradas y 13 características.
  Algunas características tienen valores nulos, como el editor, el género, la fecha de lanzamiento y el precio.

- Estadísticas Descriptivas:

  El ID de juego varía desde 10 hasta 2,028,850.
  El precio de los juegos varía, con un mínimo de 0 y un máximo de 74.76.

- Valores Únicos y Frecuencias:

  Se observa una amplia variedad de editores, géneros y títulos de juegos.
  Algunos juegos tienen múltiples etiquetas y especificaciones asociadas.

### User Reviews

- Información General:

  El conjunto de datos contiene revisiones de usuarios de Steam, con 25,791 entradas y 10 características.
  Algunas características tienen valores nulos, como la columna 'funny' (gracioso) y 'posted' (publicado).

- Estadísticas Descriptivas:

  El análisis de sentimientos muestra que la mayoría de las revisiones tienen un sentimiento positivo.

- Valores Únicos y Frecuencias:

  Se observan múltiples revisiones de diferentes usuarios para un mismo juego.
  Las revisiones varían en su tono y longitud, desde revisiones cortas hasta revisiones más detalladas.

### Users Items

- Información General:

  El conjunto de datos contiene información sobre los ítems que los usuarios tienen en Steam, con 88,176 entradas y 8 características.
  No se observan valores nulos en este conjunto de datos.

- Estadísticas Descriptivas:

  Los usuarios tienen una cantidad variable de ítems en sus cuentas, con un promedio de aproximadamente 58 ítems por usuario.

- Valores Únicos y Frecuencias:

  Hay una amplia variedad de ítems en el conjunto de datos, desde juegos populares como Counter-Strike: Global Offensive hasta juegos menos conocidos.

En este archivo se puede ver cómo se realizó y desarrolló el código: [EDA](https://github.com/delfinap5/PI-MLOps_STEAM_DELFINA/blob/main/ETL%20y%20EDA/EDA.ipynb)

## **API**

---

<img src=./Imagenes/API.jpeg width="450px"></p>

Se disponibilizó los datos utilizando FastAPI. Los *endpoints* propuestos para consumir la API son:

- *play_time_genre(genero: str):*
  Devuelve el año con más horas jugadas para un género específico.

  Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}

- *user_for_genre(genero: str):*
  Proporciona el usuario con más horas jugadas para un género y una lista de la acumulación de horas jugadas por año.

  Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}

- *users_recommend(año: int):*
  Retorna el top 3 de juegos más recomendados por usuarios para el año especificado.

  Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

- *users_worst_developer(año: int):*
  Obtiene el top 3 de desarrolladoras con juegos menos recomendados por usuarios para el año dado.

  Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

- *sentiment_analysis(empresa_desarrolladora: str):*
  Según la empresa desarrolladora, devuelve un diccionario con la cantidad total de registros de reseñas categorizados por análisis de sentimiento.

  Ejemplo de retorno: {'Valve' : [Negative = 182, Neutral = 120, Positive = 278]}

### **Deployment**

Con el fin de garantizar una creación y despliegue efectivos de las APIs, organicé el trabajo en dos archivos. En el archivo [funciones.py](https://github.com/delfinap5/PI-MLOps_STEAM_DELFINA/blob/main/funciones.py), se encuentran funciones adicionales necesarias para complementar cada API. Estas están diseñadas para obtener y preparar los datos específicamente para cada endpoint definido en 'main.py'.
Por otro lado, en el archivo [main.py](https://github.com/delfinap5/PI-MLOps_STEAM_DELFINA/blob/main/main.py), se encuentran las funciones finales de los endpoints, listas para ser utilizadas en FastAPI y desplegadas en Render.

Puedes acceder a la API desplegada a través de este enlace: [API Steam](https://apisteamdelfina.onrender.com/docs)

En el archivo [requirements.txt](https://github.com/delfinap5/PI-MLOps_STEAM_DELFINA/blob/main/requirements.txt) están las versiones de librerías utilizadas y necesarias para el desploy de la api

## **Machine Learning**

---

Se implementó un enfoque de recomendación de ítem a ítem, lo que implica sugerir elementos similares a un ítem dado. Este método se basa en medir la similitud entre los distintos ítems para realizar recomendaciones. En este caso, se recomiendan juegos similares a uno específico evaluando su grado de similitud con otros juegos. Al ingresar un juego en particular, el sistema devuelve una lista de juegos recomendados que comparten características similares. Para calcular esta similitud, se empleó la medida del coseno, la cual evalúa la similitud entre dos juegos basándose en sus atributos o características.

- *def recomendacion_juego( id de producto)*: Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.

En este archivo se puede ver como se crea y desarrolla: [ML](https://github.com/delfinap5/PI-MLOps_STEAM_DELFINA/blob/main/ML/recommend%20games.ipynb)


## **Stack Tecnológico**

---

Utilicé las siguientes Tecnologías:

### **Editor de código:**

- [![Visual Studio Code](https://img.shields.io/badge/VisualStudioCode-FF5733?style=for-the-badge&logo=lucidchart&logoColor=white)](https://code.visualstudio.com/)
  
  Para escribir, depurar y administrar tu código.

### **Lenguaje de Programación:**

- [![Python](https://img.shields.io/badge/Python-FF5733?style=for-the-badge&logo=lucidchart&logoColor=white)](https://www.python.org/)
  
  Para el desarrollo de la lógica y la funcionalidad de tu aplicación.

### **Bibliotecas de Análisis de Datos:**

- [![NumPy](https://img.shields.io/badge/NumPy-FF5733?style=for-the-badge&logo=lucidchart&logoColor=white)](https://numpy.org/)

  Para operaciones numéricas eficientes.

- [![Pandas](https://img.shields.io/badge/Pandas-FF5733?style=for-the-badge&logo=lucidchart&logoColor=white)](https://pandas.pydata.org/)
  
  Para manipulación y análisis de datos estructurados.

### **Framework Web:**

- [![FastApi](https://img.shields.io/badge/FastApi-FF5733?style=for-the-badge&logo=lucidchart&logoColor=white)](https://fastapi.tiangolo.com/)
  
  Para crear APIs rápidas y modernas.

### **Aplicaciones de Productividad:**

- [![Excel](https://img.shields.io/badge/Excel-FF5733?style=for-the-badge&logo=lucidchart&logoColor=white)](https://www.microsoft.com/es-es/microsoft-365/excel)
  
  Para procesamiento de datos y análisis.

- [![Zoom](https://img.shields.io/badge/Zoom-FF5733?style=for-the-badge&logo=lucidchart&logoColor=white)](https://zoom.us/es)
  
  Para comunicación en línea y videoconferencias.

### **Renderización y Compresión de Datos:**

- [![Render](https://img.shields.io/badge/Render-FF5733?style=for-the-badge&logo=lucidchart&logoColor=white)](https://render.com/)
  
  Para renderización de datos (no estoy seguro si te refieres a alguna biblioteca específica).

- [![Gzip](https://img.shields.io/badge/Gzip-FF5733?style=for-the-badge&logo=lucidchart&logoColor=white)](https://docs.python.org/es/3/library/gzip.html)
  
  Para compresión de archivos y datos.

### **Manipulación de Datos y Texto:**

- [![JSON](https://img.shields.io/badge/JSON-FF5733?style=for-the-badge&logo=lucidchart&logoColor=white)](https://docs.python.org/es/3/library/json.html)
  
  Para manejar datos en formato JSON.
  
- [![ast](https://img.shields.io/badge/ast-FF5733?style=for-the-badge&logo=lucidchart&logoColor=white)](https://docs.python.org/es/3.8/library/ast.html)
  
  Para análisis de árboles sintácticos abstractos.
  
- [![shutil](https://img.shields.io/badge/shutil-FF5733?style=for-the-badge&logo=lucidchart&logoColor=white)](https://docs.python.org/es/3/library/shutil.html)
  
  Para operaciones de archivos y directorios.
  
- [![re](https://img.shields.io/badge/re-FF5733?style=for-the-badge&logo=lucidchart&logoColor=white)](https://docs.python.org/es/3/library/re.html)
  
  Para expresiones regulares.
  
- [![NLTK](https://img.shields.io/badge/nltk-FF5733?style=for-the-badge&logo=lucidchart&logoColor=white)](https://www.nltk.org/)
  
  Para procesamiento de lenguaje natural, específicamente para análisis de sentimientos con SentimentIntensityAnalyzer.
  
- [![sklearn.feature_extraction.text](https://img.shields.io/badge/sklearn.feature_extraction.text-FF5733?style=for-the-badge&logo=lucidchart&logoColor=white)](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html)
  
  Para extracción de características de texto con TfidfVectorizer.

### **Operaciones de Fecha y Hora:**

- [![Datetime](https://img.shields.io/badge/Datetime-FF5733?style=for-the-badge&logo=lucidchart&logoColor=white)](https://docs.python.org/es/3/library/datetime.html)

  Para manipulación de objetos de fecha y hora.

### **Servidor Web y Despliegue:**

- [![Uvicorn](https://img.shields.io/badge/Uvicorn-FF5733?style=for-the-badge&logo=lucidchart&logoColor=white)](https://www.uvicorn.org/)

  Para ejecutar el servidor web ASGI que sirve tu aplicación FastAPI.


## **Video**

---

Este video es explicativo y desarrolla el contenido del proyecto
[Link del desarrollo del proyecto](https://drive.google.com/drive/folders/1P68YjR5G0JpGXKHdHUULH8FPbCD85dsF?usp=sharing)


## **Contacto**

---

- Gmail: delfinapena55@gmail.com
- LinkedIn: [LinkedIn](www.linkedin.com/in/delfina-longo-peña-44b4b623b)
- Github: [delfinap5](https://github.com/delfinap5)
- Curriculum: [CV](https://drive.google.com/drive/folders/1W83x9TqqUa2tFrnDEkXd3ZCLhew8pJ-R?usp=drive_link)
