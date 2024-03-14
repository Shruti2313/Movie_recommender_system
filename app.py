import streamlit as st
import pickle
import pandas as pd
import requests
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

movies_dict=pickle.load(open('movie_dict.pkl', 'rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl', 'rb'))
# Custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background-color: #121212; /* Dark background color */
        color: #FFFFFF; /* Text color */
        font-family: 'Arial', sans-serif; /* Font */
    }
    h1 {
        color: #E50914; /* Red color for main header */
        font-family: 'fantasy'; /* Fantasy font for main header */
        font-size: 44px; /* Font size for main header */
    }
 h3 {
        color: #FFCC22; /* Golden color for select a movie header */
    }
    p {
        color: #AAAAAA; /* Grey color for "Type or select a movie from the dropdown" text */
    }
    .selectbox {
        color: #4CAF50 !important; /* Green color for selectbox */
    }
    .stButton>button {
        color: #FFFFFF;
        background-color: #E50914; /* Netflix red for button background */
        border-radius: 5px; /* Rounded corners for button */
        padding: 10px 20px; /* Padding for button */
        font-size: 16px;
        font-weight: bold;
        border: none; /* Remove border */
        cursor: pointer; /* Cursor style */
    }
    .stButton>button:hover {
        background-color: #FF0000; /* Darker red on hover */
    }
    .stImage {
        border-radius: 5px; /* Rounded corners for images */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3); /* Add shadow effect to images */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎬 Movie Recommender System 🍿")
st.markdown("---")
st.markdown("### Select a movie from the dropdown below:")
movie_list = movies['title'].values
option = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('🔍 Recommend'):
    names, posters = recommend(option)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        col.text(names[i])
        col.image(posters[i], use_column_width='auto')








