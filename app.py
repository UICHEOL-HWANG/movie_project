import pickle
import streamlit as st 
import json 

from tmdbv3api import Movie,TMDb 



movie = Movie()
tmdb = TMDb()
tmdb.api_key = 'API KEY'
# 코사인 영화 데이터와 영화 파일을 임포트 
tmdb.language = 'ko-KR'

def get_recommendations(title):
   
   idx = movies[movies['title']== title].index[0]
   sim_scores = list(enumerate(cosine_sim[idx]))
   #코사인 유사도 매트릭스에서 idx에 해당하는 데이터를 (idx 유사도) 형태로 얻기 
   sim_scores = sorted(sim_scores, key = lambda x : x[1],reverse=True) # 코사인 유사도 정렬 내림 차순 
   sim_scores = sim_scores[1:11] # 자기자신을 제외한 10개의 추천 영화를 슬라이싱
   movie_indices = [i[0] for i in sim_scores] 
   images = []
   titles = []

   for i in movie_indices:
       id = movies['id'].iloc[i]
       details = movie.details(id) 
       image_path = details['poster_path']
      
       if image_path:
        image_path = 'https://image.tmdb.org/t/p/w500' + image_path
       else: 
        image_path = 'no_image.jpg' # 영화를 직접 검색 했을 때 추천 영화에는 있으나 포스터가 없을 경우 
        
       images.append(image_path)
       titles.append(details['title'])
    
   return images,titles 

movies = pickle.load(open('movies.pickle','rb'))
cosine_sim = pickle.load(open('cosine_sim.pickle','rb'))

st.set_page_config(layout='wide')

# 헤더 
st.header('CheolFlix')
movie_list = movies['title'].values 
title = st.selectbox('Choose a movie you like',movie_list) #

if st.button('Recommend'):
    with st.spinner('Please wait...'):
        images, titles = get_recommendations(title)

        idx = 0 # 
        for i in range(0,2):
            cols = st.columns(5) # 5개 컬럼 생성 
            for col in cols:
                col.image(images[idx])
                col.write(titles[idx])
                idx += 1 
