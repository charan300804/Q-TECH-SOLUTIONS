import streamlit as st
import sys
import os
import pandas as pd


# Get the root directory of the project
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Ensure `src` is in Python's module search path
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)


# Try importing modules
try:
    from data_loader import load_data
    from similarity import compute_movie_similarity
    from recommender import recommend_movies
except ModuleNotFoundError as e:
    st.error(f"❌ Module import error: {e}")
    st.stop()

# Load data
df_movies, df_ratings = load_data()

# Compute similarity matrix
movie_similarity = compute_movie_similarity(df_ratings)

# Streamlit UI
st.title("🎬 Movie Recommendation System")
st.write("Get personalized movie recommendations!")

# Movie selection
movie_list = df_movies["title"].tolist()
selected_movie = st.selectbox("Select a movie you liked:", movie_list)

# Number of recommendations
num_recommendations = st.slider("Number of recommendations:", 1, 10, 5)

# Get recommendations
if st.button("Get Recommendations"):
    movie_row = df_movies[df_movies["title"] == selected_movie]

    if movie_row.empty:
        st.warning("⚠️ Movie not found. Try selecting another movie.")
    else:
        movie_id = int(movie_row["movieId"].values[0])
        recommendations = recommend_movies(movie_id, num_recommendations, movie_similarity, df_ratings, df_movies)

        if recommendations.empty:
            st.warning("No recommendations found. Try another movie.")
        else:
            st.subheader("🎥 Recommended Movies:")
            for _, row in recommendations.iterrows():
                st.write(f"- {row['title']}")
