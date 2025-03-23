import os
import pandas as pd

def load_data():
    """
    Load movie and ratings data from CSV files.
    Returns:
        df_movies (pd.DataFrame): Movie metadata.
        df_ratings (pd.DataFrame): User-movie ratings.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

    movies_path = os.path.join(base_dir, "movies.csv")
    ratings_path = os.path.join(base_dir, "ratings.csv")

    if not os.path.exists(movies_path) or not os.path.exists(ratings_path):
        raise FileNotFoundError("❌ Data files not found! Please check the 'data' folder.")

    df_movies = pd.read_csv(movies_path)
    df_ratings = pd.read_csv(ratings_path)

    return df_movies, df_ratings
