from fastapi import FastAPI
from typing import Dict
import pandas as pd
import datetime as dt


# Cargar los datos de los archivos csv

user_reviews = pd.read_csv('C:\Users\delfi\Downloads\delfina local\PI MLOps - STEAM - DELFINA\Datasets\user_reviews.csv')
users_items = pd.read_csv('C:\Users\delfi\Downloads\delfina local\PI MLOps - STEAM - DELFINA\Datasets\users_items.csv')
steam_games = pd.read_csv('C:\Users\delfi\Downloads\delfina local\PI MLOps - STEAM - DELFINA\Datasets\steam_games.csv')

# Función para obtener el año con más horas jugadas para un género dado
def get_most_played_year_for_genre(genero: str) -> int:
    '''
    Obtiene el año con más horas jugadas para un género específico en los juegos de Steam.

    Parámetros:
    - genero (str): El género para el cual se quiere obtener el año con más horas jugadas.

    Retorna:
    - int: El año con más horas jugadas para el género especificado.
    '''
    # Filtrar por el género específico y encontrar el año con más horas jugadas
    games_genre = steam_games[steam_games['genres'] == genero]
    
    # Convertir la columna 'release_date' a formato de fecha si no está en ese formato aún
    games_genre['release_date'] = pd.to_datetime(games_genre['release_date'])
    
    # Obtener el año con más horas jugadas
    most_played_game = games_genre.loc[games_genre['playtime_forever'].idxmax(), 'release_date']
    most_played_year = most_played_game.year
    return most_played_year


# Crear la instancia de FastAPI
app = FastAPI()

# Definir el endpoint
@app.get("/PlayTimeGenre/{genre}")
def PlayTimeGenre( genre : str ):
    '''
    Obtiene el año con más horas jugadas para un género específico.

    Parámetros:
    - genre (str): El género para el cual se quiere obtener el año con más horas jugadas.

    Retorna:
    - dict: Un diccionario que contiene el año con más horas jugadas para el género especificado.
    '''
    most_played_year = get_most_played_year_for_genre(genre)
    return {"Año de lanzamiento con más horas jugadas para " + genre: most_played_year}
