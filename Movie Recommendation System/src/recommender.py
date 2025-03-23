import pandas as pd

def recommend_movies(movie_id, num_recommendations, movie_similarity, ratings, movies):
    """
    Recommends similar movies based on the given movie ID.

    Parameters:
        movie_id (int): The movie ID for which recommendations are needed.
        num_recommendations (int): Number of recommendations to return.
        movie_similarity (pd.DataFrame): Precomputed movie similarity matrix.
        ratings (pd.DataFrame): User ratings dataset.
        movies (pd.DataFrame): Movie metadata.

    Returns:
        pd.DataFrame: Recommended movies with titles.
    """

    if movie_similarity is None:
        print("❌ Error: Movie similarity matrix is missing!")
        return pd.DataFrame(columns=["movieId", "title"])  # Return empty DataFrame to prevent errors

    if movie_id not in movie_similarity.index:
        print(f"❌ Error: Movie ID {movie_id} not found in similarity matrix!")
        return pd.DataFrame(columns=["movieId", "title"])  # Return empty DataFrame if movie_id not found

    # Get similar movies sorted by similarity score
    similar_movies = movie_similarity.loc[movie_id].sort_values(ascending=False)[1:num_recommendations+1]

    # Map movie IDs to titles
    recommendations = movies[movies["movieId"].isin(similar_movies.index)][["movieId", "title"]]

    return recommendations
