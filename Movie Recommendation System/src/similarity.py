import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def compute_movie_similarity(ratings):
    """
    Computes movie similarity matrix using cosine similarity.

    Parameters:
        ratings (pd.DataFrame): User ratings dataset with columns ["userId", "movieId", "rating"].

    Returns:
        pd.DataFrame: Movie similarity matrix.
    """
    if ratings is None or ratings.empty:
        print("❌ Error: Ratings data is empty or missing!")
        return None

    # Create a pivot table: users as rows, movies as columns
    movie_ratings = ratings.pivot(index="movieId", columns="userId", values="rating").fillna(0)

    # Compute cosine similarity between movies
    similarity_matrix = pd.DataFrame(
        cosine_similarity(movie_ratings),
        index=movie_ratings.index,
        columns=movie_ratings.index
    )

    return similarity_matrix
