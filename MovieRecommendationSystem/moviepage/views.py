from django.shortcuts import render,redirect
from moviepage.MovieRecommendationSystem import df as movies_df,finalPrediction
import pandas as pd
import json,random
from moviepage.definations import createlist

def is_action_or_adventure(genre_str):
        genres = genre_str.split(", ")
        return "Action" in genres or "Adventure" in genres
        
# Create your views here.
def home(request):
    
    
    # Filter the DataFrame for Action or Adventure movies
    action_adventure_movies_df = movies_df[movies_df['genres'].apply(is_action_or_adventure)]

    # Extract the first 12 titles of Action or Adventure movies
    random_12_action_adventure_movies = action_adventure_movies_df['title'].sample(12).tolist()
    biglistt=movies_df['title'].sample(12).tolist()
    biglist=createlist(biglistt)
    

    popular=random.sample(biglist, 12)
    originals=random.sample(biglist, 12)
    shows=random.sample(biglist, 12)
    trending=random.sample(biglist, 12)
    topm=createlist(random_12_action_adventure_movies)
   
    return render(request,'index.html',context={'topm':topm,'popular':popular,'originals':originals,'shows':shows,'trending':trending})
    



