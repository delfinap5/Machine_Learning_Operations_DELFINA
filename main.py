from fastapi import FastAPI
from typing import List, Dict
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

## Df para PlayTimeGenre
# Columnas necesarias de df_steam_games
SteamGamesColumns = ['id', 'release_date', 'genres']
SGPlayTimeGenre = df_steam_games[SteamGamesColumns]

# Columnas necesarias de df_users_items
UsersItemsColumns = ['item_id', 'playtime_forever']
UIPlayTimeGenre = df_users_items[UsersItemsColumns]

# Combinar los DataFrames en uno solo usando 'id' y 'item_id' como claves de combinación
CombinedPlayTimeGenre = SGPlayTimeGenre.merge(UIPlayTimeGenre, left_on='id', right_on='item_id')


# Función para obtener el año con más horas jugadas para un género dado
def GetPlayTimeGenre(CombinedPlayTimeGenre, genero: str) -> int:
    '''
    Obtiene el año con más horas jugadas para un género específico en los juegos de Steam.

    Args:
    - CombinedPlayTimeGenre (DataFrame): DataFrame combinado con información sobre juegos y tiempo de juego de usuarios en Steam.
    - genero (str): El género para el cual se quiere obtener el año con más horas jugadas.

    Returns:
    - int: El año con más horas jugadas para el género especificado.
    '''
    # Filtrar los juegos por el género específico
    games_genre = CombinedPlayTimeGenre[CombinedPlayTimeGenre['genres'].str.contains(genero, case=False, na=False)]
    
    if games_genre.empty:
        return None  # Retorna None si no hay juegos del género especificado
    
    # Encontrar el juego con más horas jugadas en el género
    most_played_game_id = games_genre.loc[games_genre['playtime_forever'].idxmax(), 'id']
    most_played_game = CombinedPlayTimeGenre[CombinedPlayTimeGenre['id'] == most_played_game_id]
    
    # Convertir la columna 'release_date' a formato de fecha si no está en ese formato aún
    most_played_game['release_date'] = pd.to_datetime(most_played_game['release_date'], errors='coerce')
    
    # Obtener el año con más horas jugadas
    most_played_year = most_played_game['release_date'].dt.year
    most_played_year_counts = most_played_year.value_counts()
    
    if most_played_year_counts.empty:
        return None  # Retorna None si no hay datos de año
    
    return most_played_year_counts.idxmax()

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
        most_played_year = GetPlayTimeGenre(CombinedPlayTimeGenre, genre)
        return {"Año de lanzamiento con más horas jugadas para " + genre: most_played_year}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



### API UserForGenre
    
## Df para UserForGenre
# Columnas necesarias de df_steam_games
SteamGamesColumns = ['id', 'release_date', 'genres']
SGUserForGenre = df_steam_games[SteamGamesColumns]

# Columnas necesarias de df_users_items
UsersItemsColumns = ['user_id', 'item_id', 'playtime_forever']
UiUserForGenre = df_users_items[UsersItemsColumns]

# Combinar los DataFrames en uno solo usando 'id' y 'item_id' como claves de combinación
CombinedUserForGenre = SGUserForGenre.merge(UiUserForGenre, left_on='id', right_on='item_id')


# Función para obtener el usuario con más horas jugadas para un género dado y una lista de la acumulación de horas jugadas por año para ese género
def GetUserForGenre(CombinedUserForGenre, genero: str):
    '''
    Obtiene el usuario que acumula más horas jugadas para un género dado
    y una lista de la acumulación de horas jugadas por año para ese género.

    Args:
    - CombinedUserForGenre (DataFrame): DataFrame combinado con información de juegos y usuarios en Steam.
    - genero (str): El género para el cual se quiere obtener la información.

    Returns:
    - dict: Un diccionario con el usuario que más horas jugadas tiene para el género dado
            y una lista de la acumulación de horas jugadas por año.
    '''
    # Filtrar los juegos por el género específico en CombinedUserForGenre
    games_genre = CombinedUserForGenre[CombinedUserForGenre['genres'].str.contains(genero, case=False, na=False)]
    genre_user_items = games_genre[['user_id', 'playtime_forever', 'release_date']]
    
    # Convertir la columna 'release_date' a formato de fecha
    genre_user_items['release_date'] = pd.to_datetime(genre_user_items['release_date'], errors='coerce')
    
    # Extraer el año de cada fecha en 'release_date'
    genre_user_items['Año'] = genre_user_items['release_date'].dt.year
    genre_user_items['Horas'] = genre_user_items['playtime_forever'].astype(int)

    hours_played_by_year = genre_user_items.groupby('Año')['Horas'].sum().reset_index()
    most_played_user = genre_user_items.loc[genre_user_items['Horas'].idxmax(), 'user_id']

    return {
        f"Usuario con más horas jugadas para {genero}": most_played_user,
        "Horas jugadas": hours_played_by_year.to_dict(orient='records')
    }

app = FastAPI()

@app.get("/UserForGenre/{genre}")
def UserForGenre(genre: str):
    try:
        result = GetUserForGenre(CombinedUserForGenre, genre)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



### API UsersRecommend

## Df para UsersRecommend
# Columnas necesarias de df_user_reviews
UserReviewsColumns = ['item_id', 'posted', 'recommend']
URUsersRecommend = df_user_reviews[UserReviewsColumns]

# Columnas necesarias de df_steam_games
SteamGamesColumns = ['id', 'title']
SGUsersRecommend = df_steam_games[SteamGamesColumns]

# Combinar los DataFrames usando 'item_id' como clave de combinación
CombinedUsersRecommend = URUsersRecommend.merge(SGUsersRecommend, left_on='item_id', right_on='id')


# Funcion para devolver los tres juegos más recomendados por usuarios en un año especifico
def GetUsersRecommend(CombinedUsersRecommend, año):
    """
    Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado.

    Args:
    - CombinedUsersRecommend (DataFrame): DataFrame combinado de reseñas de usuarios y juegos de Steam.
    - año (int): Año para el cual se busca obtener los juegos más recomendados.

    Returns:
    - list: Lista de diccionarios con el top 3 de juegos más recomendados en el formato deseado.
      Ejemplo de retorno: [{"Puesto 1": "Nombre Juego 1"}, {"Puesto 2": "Nombre Juego 2"}, {"Puesto 3": "Nombre Juego 3"}]
    """
    # Filtrar las reseñas para el año dado y con recomendaciones positivas
    reviews_for_year = CombinedUsersRecommend[pd.to_datetime(CombinedUsersRecommend['posted']).dt.year == año]
    positive_reviews = reviews_for_year[reviews_for_year['recommend']]

    # Contar la cantidad de recomendaciones por juego
    top_games = positive_reviews['title'].value_counts().head(3)

    # Crear la estructura de retorno en el formato deseado
    return [{"Puesto {}".format(i + 1): game} for i, game in enumerate(top_games.index)]

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
        result = GetUsersRecommend(CombinedUsersRecommend, year)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



### API UsersWorstDeveloper
    
## Df para UsersWorstDeveloper
# Columnas necesarias de df_user_reviews para obtener recomendaciones de usuarios
UserReviewsColumns = ['recommend', 'item_id', 'posted']
URUsersWorstDeveloper = df_user_reviews[UserReviewsColumns]

# Columnas necesarias de df_steam_games para obtener información del desarrollador
SteamGamesColumns = ['id', 'developer']
SGUsersWorstDeveloper = df_steam_games[SteamGamesColumns]

# Combinar los DataFrames usando 'item_id' como clave de combinación
CombinedUsersWorstDeveloper= URUsersWorstDeveloper.merge(SGUsersWorstDeveloper, left_on='item_id', right_on='id')


# Funcion para devolver los tres juegos menos recomendados por usuarios en un año especifico
def GetUsersWorstDeveloper(CombinedUsersWorstDeveloper, año):
    """
    Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado.

    Args:
    - CombinedUsersWorstDeveloper (DataFrame): DataFrame combinado de reseñas de usuarios y juegos de Steam.
    - año (int): Año para el cual se busca obtener las desarrolladoras menos recomendadas.

    Returns:
    - list: Lista de diccionarios con el top 3 de desarrolladoras menos recomendadas.
    """
    # Filtrar las reseñas para el año dado con recomendaciones negativas
    negative_reviews = CombinedUsersWorstDeveloper[(pd.to_datetime(CombinedUsersWorstDeveloper['posted']).dt.year == año) & (CombinedUsersWorstDeveloper['recommend'])]
    # Obtener los IDs de los juegos con menos recomendaciones
    worst_games_ids = negative_reviews['item_id']

    # Obtener los IDs de la desarrolladora de los juegos menos recomendados
    worst_developers = CombinedUsersWorstDeveloper[CombinedUsersWorstDeveloper['item_id'].isin(worst_games_ids)]['developer'].value_counts().tail(3)

    # Crear la estructura de retorno
    return [{"Puesto {}".format(i + 1): developer} for i, developer in enumerate(worst_developers.index)]

app = FastAPI()

@app.get("/UsersWorstDeveloper/{year}", response_model = List[Dict[str, str]])
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
        result = GetUsersWorstDeveloper(CombinedUsersWorstDeveloper, year)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



## Api sentiment_analysis

## Df para SentimentAnalysis
# Columnas necesarias de df_user_reviews 
UserReviewsColumns = ['item_id','sentiment_analysis']
URSentimentAnalysis = df_user_reviews[UserReviewsColumns]

# Columnas necesarias de df_steam_games
SteamGamesColumns = ['developer', 'id']
SGSentimentAnalysis = df_steam_games[SteamGamesColumns]

# Combinar los DataFrames usando 'item_id' como clave de combinación
CombinedSentimentAnalysis= URSentimentAnalysis.merge(SGSentimentAnalysis, left_on='item_id', right_on='id')


#  Esta funcion devuelve un diccionario con el nombre de la desarrolladora selecionada
# y una lista con la cantidad total de registros de reseñas de usuarios categorizados por 0 (Negative), 1 (Neutral) y 2 (Positive).
def GetSentimentAnalysis(CombinedSentimentAnalysis, desarrolladora):
    """
    Según la empresa desarrolladora, devuelve un diccionario con el nombre de la desarrolladora
    como llave y una lista con la cantidad total de registros de reseñas de usuarios que se 
    encuentren categorizados con un análisis de sentimiento como valor.

    Args:
    - CombinedSentimentAnalysis (DataFrame): DataFrame combinado de reseñas de usuarios y juegos de Steam.
    - desarrolladora (str): Nombre de la empresa desarrolladora para la cual se busca el análisis de sentimiento.

    Returns:
    - dict: Diccionario con el nombre de la desarrolladora como llave y la cantidad de registros
            categorizados por sentimiento como valor.
    """
    # Filtrar las reseñas por la empresa desarrolladora
    developer_games = CombinedSentimentAnalysis[CombinedSentimentAnalysis['developer'] == desarrolladora]
    reviews_by_developer = developer_games[developer_games['sentiment_analysis'].notnull()]  # Filtrar por reseñas con análisis de sentimiento válido

    # Verificar si hay datos para la desarrolladora seleccionada
    if len(reviews_by_developer) == 0:
        return {desarrolladora: {"No hay datos de la desarrolladora seleccionada": 0}}  # Asumiendo que el valor debe ser 0

    # Contar la cantidad de reseñas por sentimiento
    sentiment_counts = reviews_by_developer['sentiment_analysis'].value_counts()

    # Crear el diccionario de retorno
    sentiment_dict = {
        desarrolladora: 
            {
            'Negative': sentiment_counts.get(0, 0),
            'Neutral': sentiment_counts.get(1, 0),
            'Positive': sentiment_counts.get(2, 0)
            }
    }
    return sentiment_dict

app = FastAPI()

@app.get("/SentimentAnalysis/{desarrolladora}")
def SentimentAnalysis(desarrolladora: str) -> Dict:
    """
    Endpoint para obtener el análisis de sentimiento por desarrolladora.

    Parámetros:
    - desarrolladora (str): Nombre de la empresa desarrolladora.

    Retorna:
    - dict: Diccionario con el análisis de sentimiento por desarrolladora.
    """
    try:
        result = GetSentimentAnalysis(CombinedSentimentAnalysis, desarrolladora)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))