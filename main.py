from fastapi import FastAPI
from typing import Dict
from fastapi import HTTPException
import pandas as pd
import datetime as dt



# Cargar los datos de los archivos csv
steam_games = pd.read_csv('C:/Users/delfi/Downloads/delfina local/PI MLOps - STEAM - DELFINA/Datasets/steam_games.csv')
df_steam_games = pd.DataFrame(steam_games)

user_reviews = pd.read_csv('C:/Users/delfi/Downloads/delfina local/PI MLOps - STEAM - DELFINA/Datasets/user_reviews.csv')
df_user_reviews = pd.DataFrame(user_reviews)

users_items = pd.read_csv('C:/Users/delfi/Downloads/delfina local/PI MLOps - STEAM - DELFINA/Datasets/users_items.csv')
df_users_items = pd.DataFrame(users_items)



### API PlayTimeGenre

# Función para obtener el año con más horas jugadas para un género dado
def GetPlayTimeGenre(df_steam_games, df_users_items, genero: str) -> int:
    '''
    Obtiene el año con más horas jugadas para un género específico en los juegos de Steam.

    Parámetros:
    - steam_games (DataFrame): DataFrame que contiene información sobre juegos de Steam.
    - users_items (DataFrame): DataFrame que contiene información sobre los ítems de usuarios en Steam.
    - genero (str): El género para el cual se quiere obtener el año con más horas jugadas.

    Retorna:
    - int: El año con más horas jugadas para el género especificado.
    '''
    # Filtrar los juegos por el género específico
    games_genre = df_steam_games[df_steam_games['genres'].str.contains(genero, case=False, na=False)]
    
    # Obtener los IDs de los juegos del género específico
    genre_game_ids = games_genre['id'].tolist()
    
    # Filtrar los datos de usuarios por los juegos del género específico
    genre_user_items = df_users_items[df_users_items['item_id'].isin(genre_game_ids)]
    
    # Obtener la información de los juegos más jugados del género específico
    most_played_game_id = genre_user_items.loc[genre_user_items['playtime_forever'].idxmax(), 'item_id']
    most_played_game = df_steam_games[df_steam_games['id'] == most_played_game_id]
    
    # Convertir la columna 'release_date' a formato de fecha si no está en ese formato aún
    most_played_game['release_date'] = pd.to_datetime(most_played_game['release_date'], errors='coerce')
    
    # Obtener el año con más horas jugadas
    most_played_year = most_played_game['release_date'].dt.year.item()
    return most_played_year

app = FastAPI()

@app.get("/PlayTimeGenre/{genre}")

def PlayTimeGenre(genre: str):
    '''
    Obtiene el año con más horas jugadas para un género específico.

    Parámetros:
    - genre (str): El género para el cual se quiere obtener el año con más horas jugadas.

    Retorna:
    - dict: Un diccionario que contiene el año con más horas jugadas para el género especificado.
    '''
    try:
        most_played_year = GetPlayTimeGenre(df_steam_games, df_users_items, genre)
        return {"Año de lanzamiento con más horas jugadas para " + genre: most_played_year}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


### API UserForGenre

# Función para obtener el año con más horas jugadas para un género dado
def GetUserForGenre(df_steam_games, df_users_items, genero: str) -> int:
    '''
    Obtiene el año con más horas jugadas para un género específico en los juegos de Steam.

    Parámetros:
    - steam_games (DataFrame): DataFrame que contiene información sobre juegos de Steam.
    - users_items (DataFrame): DataFrame que contiene información sobre los ítems de usuarios en Steam.
    - genero (str): El género para el cual se quiere obtener el año con más horas jugadas.

    Retorna:
    - int: El año con más horas jugadas para el género especificado.
    '''
    # Filtrar por el género específico en los juegos de Steam
    games_genre = df_steam_games[df_steam_games['genres'].str.contains(genero, case=False, na=False)]
    
    # Obtener los IDs de los juegos del género específico
    genre_game_ids = games_genre['id'].tolist()
    
    # Filtrar los datos de usuarios por los juegos del género específico
    genre_user_items = df_users_items[df_users_items['item_id'].isin(genre_game_ids)]
    
    # Obtener el ID del juego más jugado del género específico
    most_played_game_id = genre_user_items.loc[genre_user_items['playtime_forever'].idxmax(), 'item_id']
    
    # Encontrar el juego más jugado del género específico en los datos de juegos de Steam
    most_played_game = df_steam_games[df_steam_games['id'] == most_played_game_id]
    
    # Convertir la columna 'release_date' a formato de fecha si no está en ese formato aún
    most_played_game['release_date'] = pd.to_datetime(most_played_game['release_date'], errors='coerce')
    
    # Obtener el año con más horas jugadas del juego más jugado del género específico
    most_played_year = most_played_game['release_date'].dt.year.item()
    
    return most_played_year

app = FastAPI()

@app.get("/UserForGenre/{genre}")
def UserForGenre(genre: str):
    try:
        year = GetUserForGenre(df_steam_games, df_users_items, genre)
        return {"genre": genre, "most_played_year": year}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


## API UsersRecommend

# Funcion para devolver los tres juegos más recomendados por usuarios en un año especifico
def GetUsersRecommend(df_user_reviews, df_steam_games, año):
    """
    Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado.

    Args:
    - df_user_reviews (DataFrame): DataFrame de reseñas de usuarios.
    - df_steam_games (DataFrame): DataFrame de juegos de Steam.
    - año (int): Año para el cual se busca obtener los juegos más recomendados.

    Returns:
    - list: Lista de diccionarios con el top 3 de juegos más recomendados.
    """
    # Filtrar las reseñas para el año dado y con recomendaciones positivas
    reviews_for_year = df_user_reviews[pd.to_datetime(df_user_reviews['posted']).dt.year == año]
    positive_reviews = reviews_for_year[(reviews_for_year['recommend'])]

    # Contar la cantidad de recomendaciones por juego
    top_games = positive_reviews['item_id'].value_counts().head(3)

    # Obtener los nombres de los juegos con más recomendaciones
    top_game_names = [df_steam_games[df_steam_games['id'] == game_id]['title'].values[0] for game_id in top_games.index]

    # Crear la estructura de retorno
    return [{"Puesto {}".format(i + 1): game} for i, game in enumerate(top_game_names)]

app = FastAPI()

@app.get("/UsersRecommend/{year}", response_model=List[Dict[str, str]])
def UsersRecommend(year: int):
    """
    Endpoint para obtener el top 3 de juegos recomendados para un año dado.

    Parámetros:
    - year (int): Año para el cual se busca el top de juegos recomendados.

    Retorna:
    - List[Dict[str, str]]: Lista de diccionarios con los top 3 juegos recomendados.
                            Cada diccionario tiene el formato {"Puesto X": "Nombre del juego"}.
    """
    try:
        result = GetUsersRecommend(df_user_reviews, df_steam_games, year)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



## API UsersWorstDeveloper

# Funcion para devolver los tres juegos menos recomendados por usuarios en un año especifico
def GetUsersWorstDeveloper(df_user_reviews, df_steam_games, año):
    """
    Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado.

    Args:
    - df_user_reviews (DataFrame): DataFrame de reseñas de usuarios.
    - df_steam_games (DataFrame): DataFrame de juegos de Steam.
    - año (int): Año para el cual se busca obtener las desarrolladoras menos recomendadas.

    Returns:
    - list: Lista de diccionarios con el top 3 de desarrolladoras menos recomendadas.
    """
    # Filtrar las reseñas para el año dado con recomendaciones negativas
    negative_reviews = df_user_reviews[(pd.to_datetime(df_user_reviews['posted']).dt.year == año) & (df_user_reviews['recommend'])]

    # Obtener los IDs de los juegos con menos recomendaciones
    worst_games_ids = negative_reviews['item_id']

    # Obtener los IDs de la desarrolladora de los juegos menos recomendados
    worst_developers = df_steam_games[df_steam_games['id'].isin(worst_games_ids)]['developer'].value_counts().tail(3)

    # Crear la estructura de retorno
    return [{"Puesto {}".format(i + 1): developer} for i, developer in enumerate(worst_developers.index)]

app = FastAPI()

# Endpoint para obtener las desarrolladoras menos recomendadas para un año dado
@app.get("/UsersWorstDeveloper/{year}", response_model = list[Dict[str, str]])
def UsersWorstDeveloper(year: int):
    """
    Endpoint para obtener el top 3 de desarrolladoras menos recomendadas para un año dado.

    Parámetros:
    - year (int): Año para el cual se busca el top de desarrolladoras menos recomendadas.

    Retorna:
    - List[Dict[str, str]]: Lista de diccionarios con los top 3 desarrolladoras menos recomendadas.
                            Cada diccionario tiene el formato {"Puesto X": "Nombre de la desarrolladora"}.
    """
    try:
        result = GetUsersWorstDeveloper(df_user_reviews, df_steam_games, year)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


## Api sentiment_analysis
    
#  Esta funcion devuelve un diccionario con el nombre de la desarrolladora selecionada
# y una lista con la cantidad total de registros de reseñas de usuarios categorizados por 0 (Negative), 1 (Neutral) y 2 (Positive).
def GetSentimentAnalysis(df_user_reviews, df_steam_games, desarrolladora):
    """
    Según la empresa desarrolladora, devuelve un diccionario con el nombre de la desarrolladora
    como llave y una lista con la cantidad total de registros de reseñas de usuarios que se 
    encuentren categorizados con un análisis de sentimiento como valor.

    Args:
    - df_user_reviews (DataFrame): DataFrame de reseñas de usuarios.
    - df_steam_games (DataFrame): DataFrame de juegos de Steam.
    - desarrolladora (str): Nombre de la empresa desarrolladora para la cual se busca el análisis de sentimiento.

    Returns:
    - dict: Diccionario con el nombre de la desarrolladora como llave y la cantidad de registros
            categorizados por sentimiento como valor.
    """
    # Filtrar las reseñas por la empresa desarrolladora
    developer_games = df_steam_games[df_steam_games['developer'] == desarrolladora]
    reviews_by_developer = df_user_reviews[df_user_reviews['item_id'].isin(developer_games['id'])]

    # Verificar si hay datos para la desarrolladora seleccionada
    if len(reviews_by_developer) == 0:
        return {"No hay datos de la desarrolladora seleccionada"}

    # Contar la cantidad de reseñas por sentimiento
    sentiment_counts = reviews_by_developer['sentiment_analysis'].value_counts()

    # Crear el diccionario de retorno
    sentiment_dict = {
        desarrolladora: {
            'Negative': sentiment_counts.get(0, 0),
            'Neutral': sentiment_counts.get(1, 0),
            'Positive': sentiment_counts.get(2, 0)
        }
    }

    return sentiment_dict

app = FastAPI()

# Definir el endpoint para obtener el análisis de sentimiento por desarrolladora
@app.get("/sentiment_analysis/{desarrolladora}")
def SentimentAnalysis(desarrolladora: str) -> Dict:
    """
    Endpoint para obtener el análisis de sentimiento por desarrolladora.

    Parámetros:
    - desarrolladora (str): Nombre de la empresa desarrolladora.

    Retorna:
    - dict: Diccionario con el análisis de sentimiento por desarrolladora.
    """
    try:
        result = GetSentimentAnalysis(df_user_reviews, df_steam_games, desarrolladora)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
