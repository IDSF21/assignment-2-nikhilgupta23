import altair as alt
import pandas as pd
import streamlit as st
from collections import Counter
import ast
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(  # Alternate names: setup_page, page, layout
	layout="centered",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
	page_title="Spotify Trends",  # String or None. Strings get appended with "• Streamlit". 
	page_icon="🎵",  # String, anything supported by st.image, or None.
)

"""
# Spotify Trends
"""
factors = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence']
major_genres = ["Pop", "House", "Dance", "Electronic", "Country", "Rap", "Hip Hop", "Rock", "Metal", "Contemporary", "R&B", "Jazz", "Folk", "Funk", "Disco"]

spotify_data = pd.read_csv('spotify_data.csv')
# spotify_data = spotify_data[spotify_data['rank_year'] < 21]]
grouped = spotify_data.groupby('year').mean()

##########################################################################################################
# Global Stuff

st.header("Music Trends across the Years")
grouped = grouped.reset_index()
grouped_melted = grouped.melt(id_vars = ["year"], value_vars = factors, var_name = "attribute", value_name = "value")
import plotly.express as px
fig = px.line(grouped_melted, x='year', y='value', color='attribute', markers=True)
st.plotly_chart(fig, use_container_width=True)

# Feature Correlation
st.header("Music Feature Correlation")
corr = spotify_data[factors + ['popularity']].corr()
# corr.style.background_gradient(cmap='coolwarm')
fig, ax = plt.subplots()
sns.heatmap(corr, ax=ax)
st.write(fig)

##########################################################################################################
# Yearly Stuff

option = st.slider('Year', min(grouped["year"].to_list()), max(grouped["year"].to_list()), step=1)
st.title('The Year ' + str(option))

# Genres Distribution
st.header("Genres in Top 100")

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
    c = alt.Chart(pd.DataFrame(genres_dict.items(), columns=['Genres', 'Percentage'])).mark_bar().encode(
        x='Genres',
        y='Percentage'
    )
    st.altair_chart(c, use_container_width=True)
with col2:
    st.subheader("Top 3 Genres")
    yearly_top_genres = sorted(genres_dict, key=genres_dict.get, reverse=True)[:3]
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
                out[top_artist] = artist_images[artists.index(top_song_artist_list)]
                break

    return out

top_artist_image_dict = get_top_artists(spotify_data[spotify_data['year']==option])
cols = st.columns(len(top_artist_image_dict))
for col, top_artist in zip(cols, top_artist_image_dict.keys()):
    with col:
        # st.header(top_artist)
        st.image(top_artist_image_dict[top_artist], use_column_width='auto', caption=top_artist)

##########################################################################################################
