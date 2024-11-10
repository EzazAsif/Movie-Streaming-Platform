import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from django.conf import settings
import json
from sklearn.metrics.pairwise import linear_kernel
from collections import Counter


csv_file_path = os.path.join(settings.BASE_DIR, 'moviepage', 'static', 'tmdb_5000_movies.csv')
# Check if the file is open
if os.access(csv_file_path, os.R_OK):
    df = pd.read_csv(csv_file_path)
df = pd.read_csv(csv_file_path)

df['overview'] = df['overview'].fillna(' ')
df['tagline'] = df['tagline'].fillna(' ')
df['runtime'] = df['runtime'].fillna(df['runtime'].median())





    
def transform( column):
    array2 = []
    for index, row in df.iterrows():
        keywords = row[column]
        if not keywords or pd.isna(keywords):
            array2.append("")
            continue
        try:
            array = json.loads(keywords.replace("'", '"'))
            str_values = ", ".join(i["name"] for i in array)
            array2.append(str_values)
        except json.JSONDecodeError:
            array2.append("")
    df[column] = array2
    


transform( "keywords")
transform( "genres")
transform( "spoken_languages")



arr = ['genres', 'keywords', 'spoken_languages', 'overview']
tfidfArr = []
tfidf = TfidfVectorizer(stop_words='english')

for i in arr:
    tfidf_matrix = tfidf.fit_transform(df[i])
    tfidfArr.append(tfidf_matrix)



cosine_simArr = []
for i in tfidfArr:
    cosine_sim = linear_kernel(i, i)
  
    cosine_simArr.append(cosine_sim)



indices = pd.Series(df.index, index=df['title']).drop_duplicates()


def getRecommendation(title, cosine_sim, count):
    # Get the index of the movie that matches the title
    idx = indices[title]
    # Get the pairwise similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]
    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]
    # Get the movie titles of the top 10 most similar movies
    recommended_movies = df['title'].iloc[movie_indices]
    # Store movie titles in an array (list or numpy array)
    movie_titles_array = recommended_movies.tolist()  # Using list
    # movie_titles_array = np.array(recommended_movies)  # Using numpy array
    
    return movie_titles_array


# Combining the predictions
def combinePredictions(title):
    PrimaryArray = []
    SecendoryArray = []
    count = 0
    primaryGenre = ['keywords', 'genres']
    for i in primaryGenre:
        PrimaryArray+=getRecommendation(title, cosine_simArr[count], 10)
        count+=1
    
    secondaryGenre = ['overview', 'spoken_languages']
    for i in secondaryGenre:
        SecendoryArray+=getRecommendation(title, cosine_simArr[count], 100)
        count+=1
    
    SecendoryArray = [item for item in SecendoryArray if item in PrimaryArray]
    PrimaryArray+=SecendoryArray
    return PrimaryArray



from collections import Counter

def finalPrediction(title):
    # Count the occurrences of each movie title
    movie_counts = Counter(combinePredictions(title))

    # Get the top 10 most common movie titles
    top_10_movies = movie_counts.most_common(10)

    # Extract only the movie titles
    top_10_titles = [movie[0] for movie in top_10_movies]

    return top_10_titles