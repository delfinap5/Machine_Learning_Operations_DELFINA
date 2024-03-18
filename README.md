# **Proyecto Individual N°1 (MLOps)**
---

<details>
<summary><strong>Índice</strong></summary>

1. [Introducción](#Introducción)
2. [Diccionario](#Diccionario-de-Datos)
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

## **APIS**

---

Se disponibilizó los datos utilizando FastAPI. Los endpoints propuestos para consumir la API son:

#### **play_time_genre(genero: str):**
Devuelve el año con más horas jugadas para un género específico.

#### **user_for_genre(genero: str):**
Proporciona el usuario con más horas jugadas para un género y una lista de la acumulación de horas jugadas por año.

#### **users_recommend(año: int):**
Retorna el top 3 de juegos más recomendados por usuarios para el año especificado.

#### **users_worst_developer(año: int):** 
Obtiene el top 3 de desarrolladoras con juegos menos recomendados por usuarios para el año dado.

#### **sentiment_analysis(empresa_desarrolladora: str):**
Según la empresa desarrolladora, devuelve un diccionario con la cantidad total de registros de reseñas categorizados por análisis de sentimiento.


### **Deployment**

Se realizó un desploy de la api. Aqui el link: [api steam delfina](https://apisteamdelfina.onrender.com/docs)


## Stack Tecnológico

---

Utilicé las siguientes Tecnologías:

#### **Visual Studio Code**
[![Visual Studio Code](https://img.shields.io/badge/Visual-Studio-Code-7B68E?style=for-the-badge&logo=lock&logoColor=white)](https://code.visualstudio.com/)

- *Descripción:* Visual Studio Code es un editor de código fuente desarrollado por Microsoft que ofrece una variedad de características útiles para la programación, incluyendo resaltado de sintaxis, finalización de código, depuración integrada y control de versiones.

- *Utilidad:* Fue utilizado para escribir, editar y depurar código en lenguajes de Python. Con él conecté el repositorio a GitHub.

#### **FastApi**
[![FastApi](https://img.shields.io/badge/FastApi-FFA500?style=for-the-badge&logo=lock&logoColor=white)](https://fastapi.tiangolo.com/)

- *Descripción:* FastAPI es un marco web moderno y de alto rendimiento para construir APIs con Python. Está diseñado para ser fácil de usar, rápido de aprender y muy rápido de ejecutar. Se basa en Python 3.7+ y proporciona una sintaxis declarativa para definir endpoints, validación de datos, documentación automática y soporte para tipos de datos Python nativos.
- 
- *Utilidad:* Con FastAPI construí APIs rápidas y eficientes con Python. Además, su integración con bibliotecas como Pydantic y Starlette proporciona características poderosas como la validación automática de datos y el manejo de solicitudes asíncronas, lo que lo convierte en una excelente opción para proyectos de API web modernos.

#### **Python**
[![Python](https://img.shields.io/badge/Python-007ACC?style=for-the-badge&logo=lock&logoColor=white)](https://www.python.org/)

- *Descripción:* Python es un lenguaje de programación de alto nivel, interpretado y generalmente utilizado para el desarrollo de aplicaciones web, análisis de datos, inteligencia artificial, scripting y muchas otras áreas. Es conocido por su sintaxis clara y legible, así como por su amplia gama de bibliotecas y marcos de trabajo que facilitan el desarrollo rápido y eficiente de software.

- *Utilidad:* Python lo utilicé ya que su ecosistema de bibliotecas y herramientas en constante crecimiento lo hace ideal para realizar trabajo de Data Enggenier y Machine Learning.

#### **Excel**
[![Excel](https://img.shields.io/badge/Excel-FF5733?style=for-the-badge&logo=lucidchart&logoColor=white)](https://www.microsoft.com/es-es/microsoft-365/excel)

- *Descripción:* Microsoft Excel es una aplicación de hojas de cálculo desarrollada por Microsoft que permite a los usuarios realizar cálculos, organizar datos y crear gráficos. Es ampliamente utilizado en entornos empresariales, académicos y personales para realizar análisis, seguimiento de datos y presentaciones.

- *Utilidad:* Sus funciones avanzadas, como tablas dinámicas, me permitieron crear el diccionario de datos. También se pueden visualizar los datasets.

#### **Zoom**
[![Loocker](https://img.shields.io/badge/Zoom-333333?style=for-the-badge&logo=lock&logoColor=white)](https://zoom.us/es)

- *Descripción:* Zoom es una plataforma de comunicación en línea que ofrece servicios de videoconferencia, reuniones en línea, mensajería y colaboración en grupo. Es ampliamente utilizado para reuniones virtuales, webinars, clases en línea y comunicación remota.

- *Utilidad:* Lo utilicé para realizar la presentacion del proyecto, me permitio compartir pantalla, grabar la reunión y así realizar el video.


## **Video**

---

Este video es explicativo y desarrolla todo el contenido del proyecto
[Link del desarrollo del proyecto](https://drive.google.com/drive/folders/1P68YjR5G0JpGXKHdHUULH8FPbCD85dsF?usp=sharing)

## **Contacto**

---

- Gmail: delfinapena55@gmail.com
- LinkedIn: [Delfina Longo Peña](www.linkedin.com/in/delfina-longo-peña-44b4b623b)
- Github: [delfinap5](https://github.com/delfinap5)
