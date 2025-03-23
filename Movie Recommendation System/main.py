from src.data_loader import load_data
from src.similarity import build_user_similarity, build_movie_similarity
from src.recommender import recommend_movies
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import load_data 

# Load Data
movies, ratings = load_data()

# Build Similarity Matrices
user_similarity = build_user_similarity(ratings)
movie_similarity = build_movie_similarity(ratings)

# User input
user_id_to_recommend = int(input("Enter user ID for recommendations: "))

# Generate recommendations
recommended_movies = recommend_movies(user_id_to_recommend, user_similarity, movie_similarity, ratings, movies)

print("\nRecommended Movies:")
print(recommended_movies)
