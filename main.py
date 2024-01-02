from fastapi import FastAPI
import datetime as dt
import pandas as pd
from typing import List, Dict, Any
from funciones import *

app = FastAPI()

### API play_time_genre

@app.get('/play_time_genre/{genre}')
def play_time_genre(genre: str):
    '''
    Obtiene el año con más horas jugadas para un género específico.

    Parámetros:
    - genre (str): El género para el cual se quiere obtener el año con más horas jugadas.

    Retorna:
    - dict: Un diccionario que contiene el año con más horas jugadas para el género especificado.
    '''
    most_played_year = get_play_time_genre (combined_play_time_genre, genre)
    return {'Año de lanzamiento con más horas jugadas para ' + genre: most_played_year}


### API user_for_genre

@app.get('/user_for_genre/{genre}')
def user_for_genre(genre: str):
    '''
    Endpoint para obtener los usuarios que más han interactuado con un género de juego específico.

    Parámetros:
    - genre (str): Género de juego para el cual se busca obtener los usuarios más activos.

    Retorna:
    - List[Dict[str, str]]: Lista de diccionarios con los usuarios más activos en el género proporcionado.
                            Cada diccionario tiene el formato {'Usuario': 'Nombre del usuario', 'Interacciones': 'Número de interacciones'}.
    '''
    result = get_user_for_genre(combined_user_for_genre, genre)
    return result


### API users_recommend

@app.get('/users_recommend/{year}', response_model=List[Dict[str, str]])
def users_recommend(year: int):
    '''
        Endpoint para obtener el top 3 de juegos recomendados para un año dado.

        Parámetros:
        - year (int): Año para el cual se busca el top de juegos recomendados.

        Retorna:
        - List[Dict[str, str]]: Lista de diccionarios con los top 3 juegos recomendados.
                    Cada diccionario tiene el formato {'Puesto X': 'Nombre del juego'}.
    '''
    result = get_users_recommend(combined_users_recommend, year)
    return result


### API users_worst_developer

@app.get('/users_worst_developer/{year}')
def users_worst_developer(year: int):
    '''
    Endpoint para obtener el top 3 de desarrolladoras menos recomendadas para un año dado.

    Parámetros:
    - year (int): Año para el cual se busca el top de desarrolladoras menos recomendadas.

    Retorna:
    - List[Dict[str, str]]: Lista de diccionarios con los top 3 desarrolladoras menos recomendadas.
                            Cada diccionario tiene el formato {"Puesto X": "Nombre de la desarrolladora"}.
    '''
    result = get_users_worst_developer(combined_users_worst_developer, year)
    return result


## Api sentiment_analysis

@app.get('/sentiment_analysis/{desarrolladora}')
def sentiment_analysis(desarrolladora: str) -> Dict:
    '''
    Endpoint para obtener el análisis de sentimiento por desarrolladora.

    Parámetros:
    - desarrolladora (str): Nombre de la empresa desarrolladora.

    Retorna:
    - dict: Diccionario con el análisis de sentimiento por desarrolladora.
    '''
    result = get_sentiment_analysis(combined_sentiment_analysis, desarrolladora)
    return result
