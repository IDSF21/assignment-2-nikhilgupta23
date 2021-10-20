import pandas as pd
import streamlit as st
from collections import Counter
import ast
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectKBest, chi2
import plotly.express as px

st.set_page_config(  # Alternate names: setup_page, page, layout
	layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
	page_title="A Journey through time with Music",  # String or None. Strings get appended with "• Streamlit". 
	page_icon="🎵",  # String, anything supported by st.image, or None.
)

"""
# Spotify Trends
"""
factors = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'normalized_tempo']
major_genres = ["Pop", "House", "Dance", "Electronic", "Country", "Rap", "Hip Hop", "Rock", "Metal", "Contemporary", "R&B", "Jazz", "Folk", "Funk", "Disco"]

spotify_data = pd.read_csv('spotify_data.csv')
# spotify_data = spotify_data[spotify_data['rank_year'] < 21]]
spotify_data['normalized_tempo'] = (spotify_data['tempo'] - spotify_data['tempo'].min()) / (spotify_data['tempo'].max() - spotify_data['tempo'].min())
grouped = spotify_data.groupby('year').mean()

st.header("Music Trends through the years!")

grouped = grouped.reset_index()
grouped_melted = grouped.melt(id_vars = ["year"], value_vars = factors, var_name = "attribute", value_name = "value")

fig = px.line(grouped_melted, x='year', y='value', color='attribute', markers=True)
st.plotly_chart(fig, use_container_width=True)

st.write("""

Here is a brief description of the features, to help make sense of the above graph

* Danceability: Danceability describes how suitable a track is for dancing based on a combination of musical elements
* Energy: Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy.
* Instrumentalness: Predicts whether a track contains no vocals.
* Liveness: Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. 
* Loudness: The overall loudness of a track in decibels (dB). 
* Speechiness: Speechiness detects the presence of spoken words in a track. 
* Tempo: The overall estimated tempo of a track in beats per minute (BPM)
* Valence: A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).

(Source: https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features)

---

""")

option = st.slider('Year', min(grouped["year"].to_list()), max(grouped["year"].to_list()), step=1)
st.header('Year in Focus: ' + str(option))

# Genres Distribution
st.subheader("Genres in Top 100")

def normalize(d, target=1.0):
   raw = sum(d.values())
   factor = (target/raw) * 100
   return {key:value*factor for key,value in d.items()}

def get_genres_dist(sub_df: pd.DataFrame):
    genres = sub_df['artist_genres'].to_list()
    genres = [ast.literal_eval(genre) for genre in genres]
    flat_genre = [item for sublist in genres for item in sublist]
    genre_freq = {major_genre: 0 for major_genre in major_genres}
    for song_genre in flat_genre:
        for major_genre in major_genres:
            if major_genre.casefold() in song_genre.casefold():
                genre_freq[major_genre] = genre_freq[major_genre] + 1
    genre_freq = normalize(genre_freq)
    return genre_freq

genres_dict = get_genres_dist(spotify_data[spotify_data['year']==option])
col1, col2 = st.columns([3,1])

with col1:
    df_genre = pd.DataFrame({
        'Genre': genres_dict.keys(),
        'Percentage of Top 100': genres_dict.values()
    }, columns=['Genre', 'Percentage of Top 100'])
    px_bar = px.bar(df_genre, x='Genre', y='Percentage of Top 100', color='Genre', color_discrete_sequence = px.colors.qualitative.G10, range_y=[0,50])
    st.plotly_chart(px_bar, use_container_width=True)


with col2:
    st.subheader("Top Genres")
    yearly_top_genres = sorted(genres_dict, key=genres_dict.get, reverse=True)[:5]
    for genre in yearly_top_genres:
        st.write('##### ' + genre)


# Top Artists
st.header("Top Artists of the Year")
def get_top_artists(sub_df: pd.DataFrame):
    out = {}    
    artist_images = sub_df['artist_image'].to_list()
    artists = sub_df['artists'].to_list()
    artists = [ast.literal_eval(artist) for artist in artists]
    flat_artists = [item for sublist in artists for item in sublist]

    most_common_artists = Counter(flat_artists).most_common(3)
    # st.write(most_common_artists)
    top_artists = [common[0] for common in most_common_artists]
    for top_artist in top_artists:
        for top_song_artist_list in artists:
            if top_artist in top_song_artist_list:
                artist_images_list = ast.literal_eval(artist_images[artists.index(top_song_artist_list)])                
                out[top_artist] = artist_images_list[top_song_artist_list.index(top_artist)]
                break

    return out

top_artist_image_dict = get_top_artists(spotify_data[spotify_data['year']==option])
cols = st.columns(len(top_artist_image_dict))
for col, top_artist in zip(cols, top_artist_image_dict.keys()):
    with col:
        # st.header(top_artist)
        st.image(top_artist_image_dict[top_artist], use_column_width='auto', caption=top_artist)



st.write("---")

# Feature Correlation
st.header("Music Feature Correlation")

st.write("""

In this section, we look at how different audio-features correlate with each other. Primarily we look at the highly positively/negatively correlated features, and we are particularly interested in the correlation of features with **Popularity**

""")

corr = spotify_data[factors + ['popularity']].corr()
# corr.style.background_gradient(cmap='coolwarm')
fig, ax = plt.subplots()
sns.heatmap(corr, ax=ax)
st.write(fig)

st.write("""

1. The first most striking correlation is negative, between acousticness and energy. This is *highly intuitive* from the definitions of both features. As the acousticness of the song increases, the song loses energy, becomes slower, and more mellow.
1. Which leads to our next inference, which is the negative correlation between valence and acousticness. Again our argument is similar.
1. Moving on to positive correlations, we see that the triad of features: **Danceability, Energy, and Valence**, are all tightly correlated. As we know and understand music, more the energy and happiness conveyed through the song, the more 'danceable' it becomes
1. An interesting observation is the relationship between tempo and danceability. Danceable songs are typically not very fast nor slow. However, tempo is not the only contributing factor, hence we can not make strong arguments in this case.

---
""")

st.header("Features affecting Popularity")
st.write("""We now look at features of songs that affect popularity the most. For this we select features which have the highest values for the test chi-squared statistic, relative to the popularity metric.
Note that the popularity metric of a song tells us about how popular the song is at the present time, so we only included songs from the last decade because songs before that may not be listened as frequently as more recent ones.
""")

spotify_data_without_na = spotify_data.dropna(how='any')
spotify_data_without_na = spotify_data_without_na[spotify_data_without_na['year'] >= 2010]
X = spotify_data_without_na[factors]
y = spotify_data_without_na[['popularity']]
k = 3
k_best = SelectKBest(chi2, k=k)
k_best.fit_transform(X, y)

top_factors = spotify_data_without_na[factors].columns[k_best.get_support()].to_list()
corr = spotify_data[top_factors + ['popularity']].corr()
cols = st.columns(k)
for col, top_factor in zip(cols,top_factors):
    with col:
        delta = "Popularity" if corr['popularity'][top_factor] > 0 else "- Popularity"
        st.metric(label="", value=top_factor, delta=delta)


st.header("Explicitness through the Years")
year_explicit = spotify_data[["year","explicit"]].copy()
year_explicit["explicit"] = year_explicit['explicit'].astype('int64')
year_explicit = year_explicit.groupby("year").sum().reset_index()
fig = px.line(year_explicit, x='year', y='explicit', markers=True)
st.plotly_chart(fig, use_container_width=True)

# year_explicit['decade'] = ((year_explicit["year"] / 10).astype('int64')*10).astype(str) + 's'
# st.plotly_chart(px.sunburst(year_explicit, names='year', parents='decade', values='explicit', branchvalues="total"))
