from random import random
import random
from sqlalchemy import over
import sys
import streamlit as st
import pandas as pd
import numpy as np 
import pickle
import requests


def fetch_poster(movie_id):
    response= requests.get('https://api.themoviedb.org/3/movie/{}?api_key=9a4694ad681cfb458407b8a48073561b&language=en-US'.format(movie_id))
    data=response.json()
    posters=data['poster_path']
    if(not posters):
        return "img.jpg"
    else:

        return "https://image.tmdb.org/t/p/w500/"+ posters


def fetch_video(movie_id):
    video=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=9a4694ad681cfb458407b8a48073561b&append_to_response=videos'.format(movie_id))
    data1=video.json()
    result=data1['videos']['results']
    a=[]
    for i in result:
        a.append(i['key'])
    
    if(len(a)!=0):
        return "https://www.youtube.com/watch?v={} ".format(a[0])
    else:
        return " video link not available"
    

movies=pickle.load(open('movies.pkl','rb'))
movies_list=movies['title'].values
similarity=pickle.load(open("similarity.pkl","rb"))
dataset=pickle.load(open("dataset.pkl","rb"))
st.sidebar.image("img.jpg")






def recommend(movie):  
  
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movie_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:11]
    recommended_movies=[]
    recommended_movie_poster=[]
    recommended_genres=[]
    recommended_cast=[]
    recommended_overview=[]
    recommended_video=[]
    for i in movie_list:
        movie_id=movies.iloc[i[0]].movie_id
        movie_genres=movies.iloc[i[0]].genres
        movie_cast=dataset.iloc[i[0]].cast
        movie_overview=dataset.iloc[i[0]].overview
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_poster.append(fetch_poster(movie_id))
        recommended_genres.append(movie_genres)
        recommended_cast.append(movie_cast)
        recommended_overview.append(movie_overview)
        recommended_video.append(fetch_video(movie_id))
    return recommended_movies,recommended_movie_poster,recommended_genres ,recommended_cast,recommended_overview ,recommended_video

st.title("Movie Recommender System")

with st.sidebar:
    category=["select from movie list","random movie"]
    select_category=st.selectbox("select category",category)

    
    if(select_category=="select from movie list"):
        select_item=st.selectbox("Select a movie that you want to watch",movies_list)
       
    if(select_category=="random movie"):
        st.markdown("**For random recommendation click only recommended button**")
        select_item=random.choice(movies_list)
       

st.subheader("Recommendations for you")



if st.sidebar.button("Recommended "):
    st.markdown("**Recommendations of {}**".format(select_item))

        
    for i in range(10):
        names,poster,genres,cast,overview,video =recommend(select_item)
        col1,col2=st.columns([1,3])
        with col1:
            st.image(poster[i])
        with col2:
            o=' '.join(overview[i])
            g=' , '.join(genres[i])
            c=' , '.join(cast[i])
            st.markdown("_**Title**_ :=> {}".format(names[i]))
            st.markdown("_**Genres of movie**_:=> {}".format(g))
            st.markdown("_**Cast**_:=> {}".format(c))
            st.markdown("_**overview**_:=> {}".format(o))
            st.markdown("_**video trailer link**_ :=> {}".format(video[i]))
            st.markdown("------------------------------------------------------\n\n")
   


