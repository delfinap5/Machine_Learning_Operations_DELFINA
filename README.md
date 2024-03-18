# **Proyecto Individual N°1 (MLOps)**
---

<details>
<summary><strong>Índice</strong></summary>

1. [INtroducción](#Introducción)
2. [FDiccionario](#Diccionario-de-Datos)
3. [Transformaciones (ETL)](#Transformaciones-de-Datos-(ETL))
4. [Analisis (EDA)](#Análisis-Exploratorio-de-Datos-(EDA))
5. [API](#Desarrollo-de-las-API)
   - [Desployment](#Deployment)
7. [Stack Tecnológico](#Stack-Tecnologico)
   - [Visual Studio Code](#Visual-Studio-Code)
   - [Fast Api](#Fast-Api)
   - [Excel](#Excel)
   - [Zoom](#Zoom)
8. [Video Explicativo](#Video)
9. [Contacto](#Datos-de-Contacto)

</details>

## **Introducción**

---

Este es un proyecto enfocado en la creación de una API para la gestión y análisis de datos de juegos proporcionados por Steam. El objetivo es generar funcionalidades específicas para realizar consultas, análisis y recomendaciones a partir de los datasets brindados.

## **Diccionario de Datos**

---

<img src="./Imagenes/Diccionario.jpg"></p>

## **Transformaciones de Datos (ETL)**

---

Se realizó la lectura de los dataset con el formato correcto, incluyendo su limpieza, organización y preparación para optimizar las  consultas que se realicen, el rendimiento de la API, el entrenamiento del modelo de aprendizaje automático.
Se creó la columna 'sentiment_analysis' aplicando análisis de sentimiento a las reseñas de juegos en el dataset 'user_reviews'. Esta columna representa la polaridad del sentimiento en una escala de 0 a 2 (0 malo, 1 neutral o falta de reseña, 2 positivo).

## **Modelo de Aprendizaje Automático**

---

Se utilizó el enfoque para el sistema de recomendación de ítem-ítem para recibir recomendaciones de juegos similares a un producto.
def recomendacion_juego( id de producto ): Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.

## **Análisis Exploratorio de Datos (EDA)**

---

Se realizó un análisis exploratorio de los datos, ayuda a comprender la naturaleza y distribución de los datos.

## **Desarrollo de las API**

---

Se disponibilizó los datos utilizando FastAPI. Los endpoints propuestos para consumir la API son:

- play_time_genre(genero: str): Devuelve el año con más horas jugadas para un género específico.
- user_for_genre(genero: str): Proporciona el usuario con más horas jugadas para un género y una lista de la acumulación de horas jugadas por año.
- users_recommend(año: int): Retorna el top 3 de juegos más recomendados por usuarios para el año especificado.
- users_worst_developer(año: int): Obtiene el top 3 de desarrolladoras con juegos menos recomendados por usuarios para el año dado.
- sentiment_analysis(empresa_desarrolladora: str): Según la empresa desarrolladora, devuelve un diccionario con la cantidad total de registros de reseñas categorizados por análisis de sentimiento.

### **Deployment**

Se realizó un desploy de la api. Aqui el link: [api steam delfina](https://apisteamdelfina.onrender.com/docs)


## Stack Tecnológico

---

Utilicé las siguientes Tecnologías:

- Visual Studio Code
- Fast Api
- 
- Excel
- Zoom

## **Video**

---

Este video es explicativo y desarrolla todo el contenido del proyecto
[Link del desarrollo del proyecto](https://drive.google.com/drive/folders/1P68YjR5G0JpGXKHdHUULH8FPbCD85dsF?usp=sharing)

## **Contacto**
- Gmail: delfinapena55@gmail.com
- LinkedIn: [Delfina Longo Peña](www.linkedin.com/in/delfina-longo-peña-44b4b623b)
- Github: [delfinap5](https://github.com/delfinap5)
