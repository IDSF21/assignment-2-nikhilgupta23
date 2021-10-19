# A Journey through time with Music

We present a small preview into the history of the music industry, using data collected from a popular music streaming service, Spotify. Music is an essential part of every individual's life; we try to capture the trends and shifts of influence, of different genres, and different artists, through the years, to answer some compelling questions.

## Brief Introduction: Data Collection

For this project, we applied the principles and concepts learnt earlier in this class, to source and curate our own dataset (Notebook to collect data attached). Spotify exposes a set of Web API endpoints for Developers to use (https://developer.spotify.com/documentation/web-api/). We used this to do the following tasks:
* Create a list of playlists of Top 100 songs of each year, using Spotify search API. *Note: We have only used Spotify curated playlists to prevent bias*
* Obtain the list of Song IDs from each playlist, and store them according to year
* Obtain metadata for each song (audio-features), genre and artist-based information
* Combine into a single dataframe and export to CSV

## Motivation and Goals

With both of us being audiophiles (streaming music on Spotify almost 7-8 hours everyday), we believed the ideal choice of data to work on would be something we both appreciate. Spotify exposes a lot of information, from individual track based data, to artist data, to albums and playlists. We leveraged this data, to make some important observations, and furthermore, point out trends and inferences that are not very obvious

We look at answering interesting questions around:
1. How have listener preferences changed through the decades? Did the Golden Era of Hip-Hop (the 90's for those wondering) actually give enough chart toppers? Was it able to compete with Rock and Pop from the top?
1. Which artists have contributed to top songs through the years? Are they able to maintain their top spots through the years? Do bands perform better than single artists?
1. What features contribute to the success of a track? An investigation into understanding most influential features contributing to success
1. Do trends in music run in parallel to social trends? Do women artists have enough representation at the top of the charts? Has consumption of explicit content been normalized over the years?

## Design Thinking: Process and Visualizations

Questions we look to answer through our visualizations:
* Trend-based analysis:
    1. We move through the years to understand and analyse how different audio-features contribute to the success of a track. We do this in a fluid fashion, with a slider, and individual line graphs with tooltips for *each* audio feature.
    1. We again incorporate a slider to understand how each genre stacks up, in its composition of the top 100 songs each year. Here we use bar graphs, to understand differences in values effectively. 
    1. To add some pizzazz to our visualizations, we select the best performing artists, and showcase them on our *Artist Highlight!*. We are able to make some interesting inferences based on these visualizations
* To be updated after some more Visualizations

## Development Process Overview

We split the tasks equally between us through all processes of the assignment. Our tasks can be bucketed into 3 main bins:
* Data Curation: Curating the list of playlists, and getting the playlist IDs, using Web APIs to obtain different types of data
* Visualizations + Code: We collaborated on Github to create visualizations, and include post-processing
* Making inferences and observations based on the questions we asked

### Time Analysis
* ~6 hours on Data Curation
* ~7 hours on Learning Streamlit, Creating Visualizations + Code
* ~4 hours on Inferences, Writeup, Deployment
