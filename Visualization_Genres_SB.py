import streamlit as st
import matplotlib.pyplot as plt

# Counting the amount of genres from the liked_movies_list 
def count_genres(liked_movies_list, movies):
    genre_counts = {}
    for movie_index in liked_movies_list:
        genres = movies[movie_index]['genre_ids']  #'genre_ids' counts the amount of genre IDs -> Just insert the actual list instead of using the fictional 'genre_ids' list
        for genre_id in genres:
            genre_name = genre_id_to_name(genre_id)  # 'genre_id_to_name' will alter the IDs to names in order that we can add them by 1 through an if-statement
            if genre_name in genre_counts:           # -> Assuming that we use a function that converts IDs to names
                genre_counts[genre_name] += 1
            else:
                genre_counts[genre_name] = 1  # The bar chart depicts the amount of liked genres in absolute numbers
    return genre_counts

# Funktion, um ein Balkendiagramm der Genre-Zählung zu erstellen 
# Depicting a barchart that showcases the overall amount of genre matches
def plot_genre_bar_chart(genre_counts):
    genres = list(genre_counts.keys())
    counts = list(genre_counts.values()) 

    fig, ax = plt.subplots()
    ax.bar(genres, counts)
    ax.set_xlabel('Genres')
    ax.set_ylabel('Anzahl der Likes')
    ax.set_title('Beliebte Genres')
    st.pyplot(fig)

# Annahme: 'movies' ist eine Liste von Filmen, welche die Informationen von den Genres enthält
# Beispiel: movies = [{'genre_ids': [28, 12]}, {'genre_ids': [16, 35]}]

# Hauptseite
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Link zum Wechseln zur Statistikseite
if st.session_state.page == 'home':
    if st.button('Zur Statistikseite'): 
        st.session_state.page = 'stats'

# Statistikseite
if st.session_state.page == 'stats':
    # Annahme: 'liked_movies_list_player1' und 'liked_movies_list_player2' sind bereits in st.session_state definiert
    player1_genre_counts = count_genres(st.session_state.liked_movies_list_player1, movies)
    player2_genre_counts = count_genres(st.session_state.liked_movies_list_player2, movies)
    
    st.title('Statistikseite')
    st.write('Visualisierung der bevorzugten Genres basierend auf Likes')

    plot_genre_bar_chart(player1_genre_counts)
    plot_genre_bar_chart(player2_genre_counts)
    
    if st.button('Zurück zur Hauptseite'):
        st.session_state.page = 'home'



# Was ist nun genau der Zweck von diesem Code?
# 1. Interaktion zwischen Nutzern: 
# Benutzer können zwischen einer Hauptseite und gleichzeitig zu einer Statistikseite wechseln.
# Auf der Hautpseite matchen die Nutzer. Auf der Statistikseite werden die gesammelten Daten der Likes visualisiert

# 2. Visualisierung der Daten: 
# Auf der Statistikseite wird nun für jeden Spieler ein Balkendiagramm angezeigt, das die Anzahl der Likes PRO Genre darstellt. 
# Das soll den Benutzern ermöglichen, welche Genres am beliebtesten sind, basierend auf den Filmen, die die Spieler ausgewählt haben.

# 3. Unklar: Session_state
# Session_state Funktion, um die Benutzerpräferenzen über die Seitenaktualisierungen hinweg beizubehalten




def plot_genre_bar_chart(liked_movie_list, title):
    # Extracting labels and counts for the bar chart
    labels = list(genre_data.keys())
    counts = list(genre_data.values())

    fig, ax = plt.subplots()
    ax.bar(labels, counts)
    ax.set_xlabel('Genres')
    ax.set_ylabel('Anzahl der Likes')
    ax.set_title(title)
    plt.xticks(rotation=45, ha='right') # Rotate labels to prevent overlap
    plt.tight_layout() # Adjust layout to prevent clipping of tick-labels
    st.pyplot(fig) # Displaying the chart

# Likes addieren, um die Mengen später darzustellen
genre_data_player1 = collect_genre_data(st.session_state.liked_movies_list_player1, filtered_movies)
genre_data_player2 = collect_genre_data(st.session_state.liked_movies_list_player2, filtered_movies)

# Spalten erstellen
col1, col2 = st.columns(2)

# Balkendiagramm für Benutzer 1
with col1:
    st.subheader("Player 1's Favorite Movie Genres:")
    plot_genre_bar_chart(genre_data_player1, "Player 1's Favorite Genres")

# Balkendiagramm für Benutzer 2
with col2:
    st.subheader("Player 2's Favorite Movie Genres:")
    plot_genre_bar_chart(genre_data_player2, "Player 2's Favorite Genres")



# Beachte allerdings, dass die Session state Funktion noch fehlt. Diese ist wichtig, um die Benutzerpräferenzen über die Seitenaktualisierungen hinweg beizubehalten.