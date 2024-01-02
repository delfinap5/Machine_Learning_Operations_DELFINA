import datetime as dt
import pandas as pd
from typing import List, Dict, Any
from fastapi import FastAPI



# Cargar los datos de los archivos csv eligiendo unicamente las columnas que usaré
steam_games = pd.read_csv('../datasets/csv/steam_games.csv', usecols=['id', 'release_date', 'genres', 'title', 'developer'])
df_steam_games = pd.DataFrame(steam_games)

user_reviews = pd.read_csv('../datasets/csv/user_reviews.csv', usecols=['item_id', 'review', 'sentiment_analysis', 'posted'])
df_user_reviews = pd.DataFrame(user_reviews)

users_items = pd.read_csv('../datasets/csv/users_items.csv', usecols=['item_id', 'playtime_forever', 'user_id', 'release_date'])
df_users_items = pd.DataFrame(users_items)



### API play_time_genre

## Df para play_time_genre
# Combinar los DataFrames en uno solo usando 'id' y 'item_id' como claves de combinación
combined_play_time_genre = df_steam_games.merge(df_users_items, left_on='id', right_on='item_id')

# Función para obtener el año con más horas jugadas para un género dado
def get_play_time_genre(combined_play_time_genre, genero: str) -> int:
    '''
    Obtiene el año con más horas jugadas para un género específico en los juegos de Steam.

    Args:
    - combined_play_time_genre (DataFrame): DataFrame combinado con información sobre juegos y tiempo de juego de usuarios en Steam.
    - genero (str): El género para el cual se quiere obtener el año con más horas jugadas.

    Returns:
    - int: El año con más horas jugadas para el género especificado.
    '''
    # Filtrar los juegos por el género específico
    games_genre = combined_play_time_genre[combined_play_time_genre['genres'].str.contains(genero, case=False, na=False)]
    
    # Retorna un message si no hay juegos del género especificado
    if games_genre.empty:
        return [{'message': 'No hay datos disponibles para el género proporcionado'}]  
    
    # Encontrar el juego con más horas jugadas en el género
    most_played_game_id = games_genre.loc[games_genre['playtime_forever'].idxmax(), 'id']
    most_played_game = combined_play_time_genre[combined_play_time_genre['id'] == most_played_game_id]
    
    # Convertir la columna 'release_date' a formato de fecha si no está en ese formato aún
    most_played_game['release_date'] = pd.to_datetime(most_played_game['release_date'], errors='coerce')
    
    # Obtener el año con más horas jugadas
    most_played_game.loc[:, 'release_date'] = pd.to_datetime(most_played_game['release_date'], errors='coerce')
    most_played_year = most_played_game['release_date'].dt.year
    most_played_year_counts = most_played_year.value_counts()
    most_played_year_counts = int(most_played_year_counts.idxmax())

    return most_played_year_counts


### API user_for_genre
    
## Df para user_for_genre
# Combinar los DataFrames en uno solo usando 'id' y 'item_id' como claves de combinación
combined_user_for_genre = df_steam_games.merge(df_users_items, left_on='id', right_on='item_id')

# Función para obtener el usuario con más horas jugadas para un género dado y una lista de la acumulación de horas jugadas por año para ese género
def get_user_for_genre(combined_user_for_genre, genero: str):
    '''
    Obtiene el usuario que acumula más horas jugadas para un género dado
    y una lista de la acumulación de horas jugadas por año para ese género.

    Args:
    - combined_user_for_genre (DataFrame): DataFrame combinado con información de juegos y usuarios en Steam.
    - genero (str): El género para el cual se quiere obtener la información.

    Returns:
    - dict: Un diccionario con el usuario que más horas jugadas tiene para el género dado
            y una lista de la acumulación de horas jugadas por año.
    '''
    # Filtrar los juegos por el género específico en combined_user_for_genre
    games_genre = combined_user_for_genre[combined_user_for_genre['genres'].str.contains(genero, case=False, na=False)]

    # Retorna un message si no hay juegos del género especificado
    if games_genre.empty:
        return [{'message': 'No hay datos disponibles para el género proporcionado'}]
    
    genre_user_items = games_genre[['user_id', 'playtime_forever', 'release_date']]
    
    # Convertir la columna 'release_date' a formato de fecha
    genre_user_items['release_date'] = pd.to_datetime(genre_user_items['release_date'], errors='coerce')
    
    # Extraer el año de cada fecha en 'release_date'
    genre_user_items['Año'] = genre_user_items['release_date'].dt.year
    genre_user_items['Horas'] = genre_user_items['playtime_forever'].astype(int)

    hours_played_by_year = genre_user_items.groupby('Año')['Horas'].sum().reset_index()
    most_played_user = genre_user_items.loc[genre_user_items['Horas'].idxmax(), 'user_id']

    return {
        'Usuario con más horas jugadas para {genero}': most_played_user,
        'Horas jugadas': hours_played_by_year.to_dict(orient='records')
    }


### users_recommend

## Df para users_recommend
# Combinar los DataFrames usando 'item_id' como clave de combinación
combined_users_recommend = df_user_reviews.merge(df_steam_games, left_on='item_id', right_on='id')

# Funcion para devolver los tres juegos más recomendados por usuarios en un año especifico
def get_users_recommend(combined_users_recommend, año):
    '''
    Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado.

    Args:
    - combined_users_recommend (DataFrame): DataFrame combinado de reseñas de usuarios y juegos de Steam.
    - año (int): Año para el cual se busca obtener los juegos más recomendados.

    Returns:
    - list: Lista de diccionarios con el top 3 de juegos más recomendados en el formato deseado.
    '''
    # Filtrar las reseñas para el año dado y con sentimiento positivo
    combined_users_recommend['posted'] = pd.to_datetime(combined_users_recommend['posted'], format='%Y-%m-%d')
    reviews_for_year = combined_users_recommend[combined_users_recommend['posted'].dt.year == año]

    if reviews_for_year.empty:
        return [{'message': 'No hay datos disponibles para el año proporcionado'}]
    
    positive_reviews = reviews_for_year[reviews_for_year['sentiment_analysis'] == 2]

    # Contar la cantidad de recomendaciones por juego
    top_games = positive_reviews['title'].value_counts().head(3)

    # Crear la estructura de retorno en el formato deseado
    return [{'puesto {}'.format(i + 1): game} for i, game in enumerate(top_games.index)]


### users_worst_developer

## Df para users_worst_developer
# Combinar los DataFrames usando 'item_id' como clave de combinación
combined_users_worst_developer= df_user_reviews.merge(df_steam_games, left_on='item_id', right_on='id')

# Funcion para devolver los tres juegos menos recomendados por usuarios en un año especifico
def get_users_worst_developer(combined_users_worst_developer, año):
    '''
    Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado.

    Args:
    - combined_users_worst_developer (DataFrame): DataFrame combinado de reseñas de usuarios y juegos de Steam.
    - año (int): Año para el cual se busca obtener las desarrolladoras menos recomendadas.

    Returns:
    - list: Lista de diccionarios con el top 3 de desarrolladoras menos recomendadas.
    '''
    # Convertir la columna 'posted' a datetime con el formato deseado
    combined_users_worst_developer['posted'] = pd.to_datetime(combined_users_worst_developer['posted'], format='%Y-%m-%d')

    # Filtrar las reseñas para el año dado con sentimiento negativo (0)
    reviews_for_year = combined_users_worst_developer[combined_users_worst_developer['posted'].dt.year == año]

    # Verificar si no hay datos para el año proporcionado
    if reviews_for_year.empty:
        return [{'message': 'No hay datos disponibles para el año proporcionado'}]

    # Filtrar las reseñas con sentimiento negativo (0)
    negative_reviews = reviews_for_year[reviews_for_year['sentiment_analysis'] == 0]
    worst_games_ids = negative_reviews['item_id']

    # Obtener las desarrolladoras de los juegos menos recomendados
    worst_developers = combined_users_worst_developer[combined_users_worst_developer['item_id'].isin(worst_games_ids)]['developer'].value_counts().tail(3)

    # Crear la estructura de retorno
    return [{'puesto {}'.format(i + 1): developer} for i, developer in enumerate(worst_developers.index)]


## sentiment_analysis

## Df para sentiment_analysis
# Combinar los DataFrames usando 'item_id' como clave de combinación
combined_sentiment_analysis = df_user_reviews.merge(df_steam_games, left_on='item_id', right_on='id')

# Eliminar valores nulos, Nan o faltantes
combined_sentiment_analysis = combined_sentiment_analysis.dropna(subset=['item_id','review' , 'sentiment_analysis', 'developer', 'id'])

#  Funcion que devuelve un diccionario con el nombre de la desarrolladora selecionada
# y una lista con la cantidad total de registros de reseñas de usuarios categorizados por 0 (Negative), 1 (Neutral) y 2 (Positive).
def get_sentiment_analysis(combined_sentiment_analysis, desarrolladora: str) -> Dict:
    '''
    Según la empresa desarrolladora, devuelve un diccionario con el nombre de la desarrolladora
    como llave y una lista con la cantidad total de registros de reseñas de usuarios que se 
    encuentren categorizados con un análisis de sentimiento como valor.

    Args:
    - combined_sentiment_analysis (DataFrame): DataFrame combinado de reseñas de usuarios y juegos de Steam.
    - desarrolladora (str): Nombre de la empresa desarrolladora para la cual se busca el análisis de sentimiento.

    Returns:
    - dict: Diccionario con el nombre de la desarrolladora como llave y la cantidad de registros
            categorizados por sentimiento como valor.
    '''
    # Filtrar las reseñas por la empresa desarrolladora
    developer_games = combined_sentiment_analysis[combined_sentiment_analysis['developer'] == desarrolladora]

    # Filtrar por reseñas con análisis de sentimiento válido
    reviews_by_developer = developer_games.dropna(subset=['sentiment_analysis'])

    # Filtrar por reseñas con análisis de sentimiento válido
    reviews_by_developer['sentiment_analysis'] = reviews_by_developer['sentiment_analysis'].astype(int)

    # Verificar si hay datos para la desarrolladora seleccionada
    if len(reviews_by_developer) == 0:
        return {'message': 'No hay datos disponibles para la desarrolladora proporcionada'}
    
    # Contar la cantidad de reseñas por sentimiento
    sentiment_counts = reviews_by_developer['sentiment_analysis'].value_counts()

    # Crear el diccionario de retorno
    sentiment_dict = {
        desarrolladora: 
            {
            'Negative': int(sentiment_counts.get(0, 0)),
            'Neutral': int(sentiment_counts.get(1, 0)),
            'Positive': int(sentiment_counts.get(2, 0))
            }
    }
    return sentiment_dict