import pickle

import numpy as np
import pandas as pd
import requests
import streamlit as st

API_KEY = "f3448ffb322872ba34f7e004c3618d2e"


def Fetch_Poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get("poster_path"):
            return "https://image.tmdb.org/t/p/w500" + data["poster_path"]
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"

    except requests.exceptions.RequestException as e:
        print("TMDB Error:", e)
        return "https://via.placeholder.com/500x750?text=No+Poster"


url = Fetch_Poster(500)
print(url)


def Recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[
        1:6
    ]
    recommended_movies = []
    recommended_movie_poster = []
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_poster.append(Fetch_Poster(movies.iloc[i[0]].id))
    return recommended_movies, recommended_movie_poster


movie_dict = pickle.load(
    open(
        "C:\\Data Science\\Machine Learning\\Project\\Movie_recommendation_system\\pickle\\movie_dict.pkl",
        "rb",
    )
)
similarity = pickle.load(
    open(
        "C:\\Data Science\\Machine Learning\\Project\\Movie_recommendation_system\\pickle\\similarity.pkl",
        "rb",
    )
)
movies = pd.DataFrame(movie_dict)


st.title("Movie Recommendation System")

option = st.selectbox("Select a movie you like:", movies["title"].values)
if st.button("Show Recommendation"):
    recommended_movie_names, recommended_movie_posters = Recommend(option)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
