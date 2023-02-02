import streamlit as st
import pickle
import pandas as pd
import numpy as np
import requests

st.set_page_config(layout="wide")


def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://wallpapercave.com/wp/wp11201620.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=ae08cd58d40ecfa2f6b65ae30dfbfa2b&language=en-US'.format(movie_id))
    data = response.json()
    try:
        return "https://image.tmdb.org/t/p/w500/"+ data['poster_path']
    except TypeError:
        st.write("This movie might take some time due to error")


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    actor_index = actor[actor['title'] == movie].index[0]
    genre_index = genre[genre['title'] == movie].index[0]

    distances = similarity[movie_index]
    # movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[0:8]
    # similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[0:8]

    #actor
    distances_actor = similar[actor_index]
    distances_genre = similar_genre[genre_index]
    actors_list = sorted(list(enumerate(distances_actor)), reverse=True, key=lambda x: x[1])[1:9]
    genre_list =  sorted(list(enumerate(distances_genre)), reverse=True, key=lambda x: x[1])[1:9]

    selected_id = movies.loc[movies['title'] == movie, 'movie_id'].iloc[0]
    index = np.where(pt.index == selected_movie_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores_vt[index])), key=lambda x: x[1], reverse=True)[1:10]
    # similar_item = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:9]
    #popular_items = sorted(list(enumerate(popular_df['id'].count())), key=lambda x: x[1], reverse=True)[0:8]
    recommended_movies = []
    recommended_movies_posters = []
    #content
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        #fetch poster from API
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    #collaborative
    for i in similar_items:
        try:
            movies_id = movies.loc[movies['title'] == pt.index[i[0]], 'movie_id'].iloc[0]
        except IndexError:
            print()
        recommended_movies.append(pt.index[i[0]])
        recommended_movies_posters.append(fetch_poster(movies_id))

    #popular
    for i in range (0,12):
            popular_id = popularity_df.iloc[i].id
            recommended_movies.append(popularity_df.iloc[i].title)
            recommended_movies_posters.append(fetch_poster(popular_id))

    # actor-based
    for i in actors_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    #genre
    for i in genre_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters



movie_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movie_dict)

similar = pickle.load(open('similar.pkl','rb'))
similar_genre = pickle.load(open('similar_genre.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))
similarity_scores_vt = pickle.load(open('similarity_scores_vt.pkl','rb'))
popularity_df = pickle.load(open('popular_df.pkl','rb'))

#actor
actor = pickle.load(open('actor_df.pkl','rb'))
genre = pickle.load(open('genre_df.pkl','rb'))
#collaborative
pt = pickle.load(open('pt.pkl','rb'))
pt_file = pd.DataFrame(pt)
vt = pickle.load(open('vt.pkl','rb'))
vt_file = pd.DataFrame(vt)
st.markdown("<h1 style='text-align: center; color: Yellow; font-size:75px;'>Movie Recommender</h1>", unsafe_allow_html=True)


selected_movie_name = st.selectbox(
    'Search any movie to get recommendations! ',
    movies['title'].values)


names, posters = recommend(selected_movie_name)

container = st.container()
container.header("What you were looking for and related movies ")
col1, col2, col3,col4= st.columns(4)
col1,col2,col3,col4 = st.columns(4)


with col1:
   st.text(names[0])
   st.image(posters[0])

with col2:
    st.text(names[1])
    st.image(posters[1])

with col3:
    st.text(names[2])
    st.image(posters[2])

with col4:
    st.text(names[3])
    st.image(posters[3])


with col1:
    st.text(names[5])
    st.image(posters[5])
with col2:
    st.text(names[6])
    st.image(posters[6])
with col3:
    st.text(names[7])
    st.image(posters[7])
with col4:
    st.text(names[8])
    st.image(posters[8])

#Collaborative filtering

container = st.container()
container.header("What other users like to watch")
col1,col2,col3,col4 = st.columns(4)
col1,col2,col3,col4 = st.columns(4)
with col1:
    st.text(names[9])
    st.image(posters[9])
with col2:
    st.text(names[10])
    st.image(posters[10])
with col3:
    st.text(names[11])
    st.image(posters[11])
with col4:
    st.text(names[12])
    st.image(posters[12])


with col1:
    st.text(names[13])
    st.image(posters[13])
with col2:
    st.text(names[14])
    st.image(posters[14])
with col3:
    st.text(names[15])
    st.image(posters[15])
with col4:
    st.text(names[16])
    st.image(posters[16])


#actor_based
container = st.container()
container.header("If you want to watch movies of these actors")
col1,col2,col3,col4 = st.columns(4)
col1,col2,col3,col4 = st.columns(4)
with col1:
    st.text(names[29])
    st.image(posters[29])
with col2:
    st.text(names[30])
    st.image(posters[30])
with col3:
    st.text(names[31])
    st.image(posters[31])
with col4:
    st.text(names[32])
    st.image(posters[32])


with col1:
    st.text(names[33])
    st.image(posters[33])
with col2:
    st.text(names[34])
    st.image(posters[34])
with col3:
    st.text(names[35])
    st.image(posters[35])
with col4:
    st.text(names[36])
    st.image(posters[36])

#genre_based
container = st.container()
container.header("If you want to watch movies of this genre")
col1,col2,col3,col4 = st.columns(4)
col1,col2,col3,col4 = st.columns(4)
with col1:
    st.text(names[37])
    st.image(posters[37])
with col2:
    st.text(names[38])
    st.image(posters[38])
with col3:
    st.text(names[39])
    st.image(posters[39])
with col4:
    st.text(names[40])
    st.image(posters[40])


with col1:
    st.text(names[41])
    st.image(posters[41])
with col2:
    st.text(names[42])
    st.image(posters[42])
with col3:
    st.text(names[43])
    st.image(posters[43])
with col4:
    st.text(names[44])
    st.image(posters[44])


#Popular movies
container = st.container()
container.header("Some of the most rated films on our app")
col1,col2,col3,col4 = st.columns(4)
col1,col2,col3,col4 = st.columns(4)
col1,col2,col3,col4 = st.columns(4)
with col1:
    st.text(names[17])
    st.image(posters[17])
with col2:
    st.text(names[18])
    st.image(posters[18])
with col3:
    st.text(names[19])
    st.image(posters[19])
with col4:
    st.text(names[20])
    st.image(posters[20])


with col1:
    st.text(names[21])
    st.image(posters[21])
with col2:
    st.text(names[22])
    st.image(posters[22])
with col3:
    st.text(names[23])
    st.image(posters[23])
with col4:
    st.text(names[24])
    st.image(posters[24])

with col1:
    st.text(names[25])
    st.image(posters[25])
with col2:
    st.text(names[26])
    st.image(posters[26])
with col3:
    st.text(names[27])
    st.image(posters[27])
with col4:
    st.text(names[28])
    st.image(posters[28])
#
# with col1:
#     st.text(names[29])
#     st.image(posters[29])
# with col2:
#     st.text(names[30])
#     st.image(posters[30])
# with col3:
#     st.text(names[31])
#     st.image(posters[31])
# with col4:
#     st.text(names[32])
#     st.image(posters[32])
#






