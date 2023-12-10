#trending movies call written by Nikolas

import streamlit as st
import pandas as pd
import json
import requests
import copy
from IPython.display import HTML
from PIL import Image, ImageEnhance
from datetime import datetime
import streamlit.components.v1 as components
import matplotlib.pyplot as plt ########Chiara hinzufügen

#Variable as a placeholder since the imported data contains some variables where booleans are written as 'false' 
#instead of the correct python spelling 'False' and python cant parse this
false = False
true = True

api_key = '45dcf73ab776e5f887de1aee202d50e7'
##threw in the API key for the convenience of using it as a parameter in making API requests


#imported json_data contains information on movie genre only as id numbers, > this function is mapping the genre ids to the correct names
def movies_genre_id_match(json_data):
    genre_list = {
        "genres": [
            {"id": 28, "name": "Action"},
            {"id": 12, "name": "Adventure"},
            {"id": 16, "name": "Animation"},
            {"id": 35, "name": "Comedy"},
            {"id": 80, "name": "Crime"},
            {"id": 99, "name": "Documentary"},
            {"id": 18, "name": "Drama"},
            {"id": 10751, "name": "Family"},
            {"id": 14, "name": "Fantasy"},
            {"id": 36, "name": "History"},
            {"id": 27, "name": "Horror"},
            {"id": 10402, "name": "Music"},
            {"id": 9648, "name": "Mystery"},
            {"id": 10749, "name": "Romance"},
            {"id": 878, "name": "Science Fiction"},
            {"id": 10770, "name": "TV Movie"},
            {"id": 53, "name": "Thriller"},
            {"id": 10752, "name": "War"},
            {"id": 37, "name": "Western"}
        ]
    }

    genre_mapping = {genre['id']: genre['name'] for genre in genre_list.get('genres', [])}

    for result in json_data.get('results', []):
        result['genres'] = ', '.join([genre_mapping.get(genre_id, 'no information') for genre_id in result.get('genre_ids', [])])


# API Call begin:
api_urls = {
        "Trending today - new discoveries": "https://api.themoviedb.org/3/trending/movie/day?language=en-US", # Trending
        "Currently popular": "https://api.themoviedb.org/3/movie/popular",  # Trending
        #"Now playing in cinemas": "https://developer.themoviedb.org/reference/movie-now-playing-list",  # Now playing 
        # ^? throws an error, need to fix
    }

def call_api(selected_url):
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0NWRjZjczYWI3NzZlNWY4ODdkZTFhZWUyMDJkNTBlNyIsInN1YiI6IjY1NGY1ZmQ5ZDQ2NTM3MDEzODYxOGM4OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.8VjNzn4qL3MQZUUxaUrsxCdxmYXsR_OIl7q3kAaUXXA"
}
    response = requests.get(selected_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error calling API. Status Code: {response.status_code}")
        return None
    
############################################################################################################################
#With  Help from https://discuss.streamlit.io/t/how-to-change-the-backgorund-color-of-button-widget/12103/37?page=2
    
def ChangeButtonColour(wgt_txt, wch_hex_colour = '12px'):
    htmlstr = """<script>var elements = window.parent.document.querySelectorAll('*'), i;
                for (i = 0; i < elements.length; ++i) 
                    { if (elements[i].innerText == |wgt_txt|) 
                        { elements[i].style.color ='""" + wch_hex_colour + """'; } }</script>  """

    htmlstr = htmlstr.replace('|wgt_txt|', "'" + wgt_txt + "'")
    components.html(f"{htmlstr}", height=0, width=0)

############################################################################################################################

#page title
st.title("Movie Selection")

# defining variables, making them stateful, to persist past the unfortunateness that is streamlit persistently reloading the entire script
player_number = 1
if 'player_number' not in st.session_state:
    st.session_state.player_number = 1
if 'liked_movies_list_player1' not in st.session_state:
    st.session_state.liked_movies_list_player1 = []
if 'liked_movies_list_player2' not in st.session_state:
    st.session_state.liked_movies_list_player2 = []
if 'liked_movies_list_matches' not in st.session_state:
    st.session_state.liked_movies_list_matches = []

movie_list_to_request = st.selectbox("**Which category would you like to choose from?**", list(api_urls.keys()))
#if st.button("Start Game"):
        #st.text(f"Calling API for {movie_list_to_request}...")

selected_url = api_urls[movie_list_to_request]
json_data = call_api(selected_url)
# API Call end

#page header and description
if movie_list_to_request == 'Currently popular':
    st.header("Currently Popular Movies")
    st.write("""
             **The following content presents up to 10 currently popular movies together with a short description, 
             the genre they belong to, and user scores on TheMovieDB on a scale of 1-10. 
             Please make a choice between like (if you would like to watch the movie) and not interested 
             (if not interested). The app will tally the votes and present the two players with the ideal 
             match for their movie night. Enjoy!**
             """)
if movie_list_to_request == 'Trending today - new discoveries':
    st.header("Trending")
    st.write("""
             **The following content presents up to 10 current trending movies together with a short description, 
             the genre they belong to, and user scores on TheMovieDB on a scale of 1-10. 
             Please make a choice between like (if you would like to watch the movie), and not interested 
             (if not interested). The app will tally the votes and present the two players with the ideal 
             match for their movie night. Enjoy!** 
             """)
    



#Correcting inputted data, genre_ids > genre_names
movies_genre_id_match(json_data)

##creating a selectbox to choose between different genres available with TMDB
def get_genres(api_key):
    url = "https://api.themoviedb.org/3/genre/movie/list"
    params = {"api_key": api_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()['genres']
    else:
        return []

genres = get_genres(api_key)

##adding the option for not applying a genre filter
all_genres = {"id": "All", "name": "All genres"}
genres.insert(0, all_genres)

selected_genre = st.selectbox(
    "**Choose a Genre**",
    genres,
    format_func=lambda genre: genre['name'])

##comparing the release date of a movie with today's date
today = datetime.today().date()

def release_date_in_past(release_date_str):
    if release_date_str:
        release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date() ##converts 'release_date'-object (returned as str by API) to datetime.date object as '<=' between instances of str and datetime.date is not supported
        return release_date <= today
    else:
        return False

##extraction of the genre-id and enabling the filtering of the films respective to the selected genre, also sorting out movies which aren't yet released
def filter_movies_by_genre_and_release_date(movies, genre_id):
    filtered_movies = []
    for movie in movies:
        if (genre_id == "All" or genre_id in movie.get('genre_ids')) and release_date_in_past(movie.get('release_date')):
            filtered_movies.append(movie)
    return filtered_movies

#limiting the amount of movies in any selection to 10 to improve performance
filtered_movies_full_list = filter_movies_by_genre_and_release_date(json_data.get("results", []), selected_genre['id'])
#filtered_movies_full_list = []
filtered_movies = []


##listing the genre-ids and assign them to a variable for specific information output
ACTION_GENRE_ID = 28
ADVENTURE_GENRE_ID = 12
ANIMATION_GENRE_ID = 16
COMEDY_GENRE_ID = 35
CRIME_GENRE_ID = 80
DOCUMENTARY_GENRE_ID = 99
DRAMA_GENRE_ID = 18
FAMILY_GENRE_ID = 10751
FANTASY_GENRE_ID = 14
HISTORY_GENRE_ID = 36
HORROR_GENRE_ID = 27
MUSIC_GENRE_ID = 10402
MYSTERY_GENRE_ID = 9648
ROMANCE_GENRE_ID = 10749
SCIENCEFICTION_GENRE_ID = 878
TVMOVIE_GENRE_ID = 10770
THRILLER_GENRE_ID = 53
WAR_GENRE_ID = 10752
WESTERN_GENRE_ID = 37

if selected_genre:
    #movies = filter_movies_by_genre_and_release_date(json_data.get("results", []), selected_genre['id'])
    #filtered_movies_full_list = filter_movies_by_genre_and_release_date(json_data.get("results", []), selected_genre['id'])
    ##outputs the specific information for the genres
    if selected_genre['id'] == 'All':
        st.write("Unsure what kind of movie enthusiast you are? Get started today with exploring the vast universe of cinematography!")
    elif selected_genre['id'] == ACTION_GENRE_ID:
        st.write("Shootouts, explosions, car chases. If you like the rush of adrenaline going thorugh your body, this is the genre you are looking for!")
    elif selected_genre['id'] == ADVENTURE_GENRE_ID:
        st.write("You are looking for an escape to far away lands and exotic locations? With this genre you're getting exactly that!")
    elif selected_genre['id'] == ANIMATION_GENRE_ID:
        st.write("Who says animated movies are for kids, huh? Ignore them haters and watch lovely animated movies or take a trip down memory lane and reminisce about your childhood.")
    elif selected_genre['id'] == COMEDY_GENRE_ID:
        st.write("You're fun at parties and always try to get a laugh? Why not try to switch the roles? With this genre laughter is almost guarateed!")
    elif selected_genre['id'] == CRIME_GENRE_ID:
        st.write("Crime and its detection is nomrally reserved for professionals only. But if you feel sharpminded enough, unleash your inner Sherlock Holmes with this genre!")
    elif selected_genre['id'] == DOCUMENTARY_GENRE_ID:
        st.write("You'd like to discover the world but are to lazy to go outside? No problemo! Treat yourself to the beauty of the universe within your own four walls with this genre!")
    elif selected_genre['id'] == DRAMA_GENRE_ID:
        st.write("Emotions and transitive feelings are what you're seeking for? Prepare for a ride on the rollercoaster of emotions with this genre!")
    elif selected_genre['id'] == FAMILY_GENRE_ID:
        st.write("A family gathering is coming up and you don't feel like talking to your boring family members about the growth of the kids? Let these movies do the talking instead!")
    elif selected_genre['id'] == FANTASY_GENRE_ID:
        st.write("Are you a supernatural being or do you have a talking cat? Probably not. With this genre you can at least imagine what it would be like.")
    elif selected_genre['id'] == HISTORY_GENRE_ID:
        st.write("You'd love to have had witnessed Omaha Beach on D-Day or the beheading of Louis XVI? Since time travel hasn't been invented yet, this genre is probably the closest you can get to that.")
    elif selected_genre['id'] == HORROR_GENRE_ID:
        st.write("You feel tough and aren't afraid of anything? Then this genre will teach you what real fear is!")
    elif selected_genre['id'] == MUSIC_GENRE_ID:
        st.write("You have rhythm in your blood and love the beauty of music? Search no further! With this genre you'll get the full experience of the art of sound.")
    elif selected_genre['id'] == MYSTERY_GENRE_ID:
        st.write("Dark storylines and crushing atmospheres is what you like? This genre provides all that and catapults you into a world full of mysteries.")
    elif selected_genre['id'] == ROMANCE_GENRE_ID:
        st.write("Instead of crying in your bed watching romance movies, go see your loved ones and try to get past your trauma! XOXO")
    elif selected_genre['id'] == SCIENCEFICTION_GENRE_ID:
        st.write("You are bored of mainstream science and fascinated by talking robots or superhumans? Give a f*ck about the laws of science and and watch this genre then!")
    elif selected_genre['id'] == TVMOVIE_GENRE_ID:
        st.write("No idea what kind of genres this is. Feel free to explore for yourself.")
    elif selected_genre['id'] == THRILLER_GENRE_ID:
        st.write("If suspense, plot-twists and a climatic experiences are the things you have a wekaness for, this genre is exactly what you are looking for. Keep in mind to hold on to your seat, beacause this genre keeps you on the edge of it!")
    elif selected_genre['id'] == WAR_GENRE_ID:
        st.write("In the midst of chaos, there is also opportunity. And yours may be this genre.")
    elif selected_genre['id'] == WESTERN_GENRE_ID:
        st.write("Howdy partner! You like horses and the call of the wild? Then what are you waiting for? Buckle up and ride into the sunset with this genre!")

    if len(filtered_movies_full_list) > 10:
        filtered_movies = filtered_movies_full_list[:10]
    else: 
        filtered_movies = filtered_movies_full_list




#output is variable
desired_output_per_movie = ["title", "overview", "genres", "vote_average"]
#dont ask me streamlit wants a key for buttons
button_key_counter = 0


# Backdrop from API: Retrieve the URL for the backdrop image of a movie using its ID
def get_backdrop_url(movie_id):
    # API endpoint for movie images
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/images"

    # API headers including the authorization token
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0NWRjZjczYWI3NzZlNWY4ODdkZTFhZWUyMDJkNTBlNyIsInN1YiI6IjY1NGY1ZmQ5ZDQ2NTM3MDEzODYxOGM4OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.8VjNzn4qL3MQZUUxaUrsxCdxmYXsR_OIl7q3kAaUXXA"
    }

    # Make API request to get movie image data
    response = requests.get(url, headers=headers)
    data = response.json()

    # Assuming the first image in the backdrop list is used
    # Could also access to more different images by changing the number in the [ ]. 
    # Multiple Backdrops for the same movie but after considering, #0 was always the best one...
    # Here until to the ### Line, ChatGPT helped me with the order and generally the stuff to get...
    backdrop_path = data.get('backdrops', [{}])[0].get('file_path', '')

    if backdrop_path:
        # Construct the full URL for the image
        base_url = "https://image.tmdb.org/t/p/original"
        return f"{base_url}{backdrop_path}"
    else:
        # Return None if no backdrop image is available, until now there was never the case where a backdrop missed
        #could be deleted actually...
        return None


#pandas df index hide method # needs to be revisited
def hide_index_function(styler):
    styler.hide(axis="index")
    return styler

#function that outputs movies as a panda dataframe
#st.cache supposed to cache the results of a function and output them if function is called again with the same parameters, should improve performance
@st.cache_data
def movie_output(movie, desired_output_per_movie):
    filter_to_list = {key: movie[key] for key in desired_output_per_movie}
    output = pd.DataFrame(list(filter_to_list.items()), columns=["Key", "Value"])
    
    
 # Get backdrop image URL from def
    backdrop_url = get_backdrop_url(movie.get('id'))

    if backdrop_url:
        # Display the backdrop image
        backdrop_image = Image.open(requests.get(backdrop_url, stream=True).raw)
        st.image(backdrop_image, use_column_width=True)

        # Create a two-column layout with adjusted widths
        col1, col2 = st.columns([1, 3])

        # Display the poster image in the left column so that in the right, there is place for the text from col2
        poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
        col1.image(poster_url, width=175)

        # Display other information for each movie in the right column (two-thirds width)
        # changed the Layout and presentation of the data, as before it was in a Dataframe
        # much nicer to look at... 
        # also here with the content of the indent "with col2:", ChatGPT helped me to reorganize 
        # the part that Nikolas previosly wrote as a Dataframe
        with col2:
            st.write(f"**Title:** {movie['title']}")
            st.write(f"**Overview:** {movie['overview']}")
            st.write(f"**Genres:** {movie['genres']}")
            st.write(f"**Release Date:** {movie['release_date']}")
            st.write(f"**Rating:** {movie['vote_average']}")
        
    return HTML(output.to_html(index=False))

#creating global variables according to the amount of movies > movie1, movie2, movie3, movie4
for i, movie in enumerate(filtered_movies, start=1):
    variable_name = f"movie{i}"
    globals()[variable_name] = movie

##displaying information about movie availabilty in selected genre and category as warning labels
if 1 < len(filtered_movies) and selected_genre['id'] == 'All':
    st.warning(f"There are currently {len(filtered_movies)} movies available in total within the category '{movie_list_to_request}'.")
    st.write("**It is now player ", player_number , "'s turn.**") 

if len(filtered_movies) == 1 and selected_genre['id'] == 'All':
    st.warning(f"There is currently {len(filtered_movies)} movie available within the category '{movie_list_to_request}'.")
    st.write("**It is now player ", player_number , "'s turn.**") 

if 1 < len(filtered_movies) and selected_genre['id'] != 'All':
    st.warning(f"There are currently {len(filtered_movies)} movies available in the genre '{selected_genre['name']}'.")
    st.write("**It is now player ", player_number , "'s turn.**") 

if len(filtered_movies) == 1 and selected_genre['id'] != 'All':
    st.warning(f"There is currently {len(filtered_movies)} movie available in the genre '{selected_genre['name']}'.")
    st.write("**It is now player ", player_number , "'s turn.**") 
        
if len(filtered_movies) == 0 and selected_genre['id'] != 'All':
    st.warning(f"There are currently no movies in the genre '{selected_genre['name']}' within the category '{movie_list_to_request}' available. Please try another genre or category.")
    
if len(filtered_movies) == 0 and selected_genre['id'] == 'All':
    st.warning(f"Unlucky you! There are currently no movies in the category '{movie_list_to_request}' available. Please try another category.")
    

#defining variables, making them stateful, to persist past the unfortunateness that is streamlit persistently reloading the entire script
player_number = 1
if 'player_number' not in st.session_state:
    st.session_state.player_number = 1
if 'liked_movies_list_player1' not in st.session_state:
    st.session_state.liked_movies_list_player1 = []
if 'liked_movies_list_player2' not in st.session_state:
    st.session_state.liked_movies_list_player2 = []
if 'liked_movies_list_matches' not in st.session_state:
    st.session_state.liked_movies_list_matches = []

# Loop for Player 1
button_key_counter = 0
for i in range(1, len(filtered_movies) + 1):
    variable_name = f"movie{i}"
    movie = globals()[variable_name]

    st.write("Movie Suggestion ", i, ": ")

    output = movie_output(movie, desired_output_per_movie)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button('Like', key=button_key_counter):
            st.session_state.liked_movies_list_player1.append(i)
    with col2:
        st.button('Not interested', key=button_key_counter + 1)
        # Handle 'Not interested' action

    st.write("------")
    st.write("\n\n")
    button_key_counter += 2

##removing the button if no choices are available
if len(filtered_movies) > 0: 
    st.button('Done with choosing, Player 2s Turn')
    st.write("------")



button_key_counter = 50  # Reset button_key_counter for Player 2
for i in range(1, len(filtered_movies) + 1):
    variable_name = f"movie{i}"
    movie = globals()[variable_name]

    st.write("Movie Suggestion ", i, ": ")

    output = movie_output(movie, desired_output_per_movie)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button('Like', key=button_key_counter):
            st.session_state.liked_movies_list_player2.append(i)
    with col2:
        st.button('Not interested', key=button_key_counter + 1)
        # Handle 'Not interested' action

    st.write("------")
    st.write("\n\n")
    button_key_counter += 2


for item in st.session_state.liked_movies_list_player1:
    if item in st.session_state.liked_movies_list_player2:
        st.session_state.liked_movies_list_matches.append(item)

####################################################################################### chiara create genre chart
def collect_genre_data(liked_movies_list, movies):
    genre_counts = {}
    for movie_index in liked_movies_list:
        movie = movies[movie_index - 1]  # Adjusting index for zero-based indexing
        genres = movie['genres'].split(', ')
        for genre in genres:
            genre_counts[genre] = genre_counts.get(genre, 0) + 1
    return genre_counts

def plot_genre_pie_chart(genre_data, title):
    # Extracting labels and sizes for the pie chart
    labels = genre_data.keys()
    sizes = genre_data.values()
    fig, ax = plt.subplots()# Creating the pie chart
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    plt.title(title) # Adding a title
    st.pyplot(fig) # Displaying the chart
####################################################################################### chiara create genre chart



if len(filtered_movies) > 0: ##removing the button if no choices are available
    if st.button('Done with choosing, display matches:'):
        i = 1
        st.title("Your Movie Matches Are:")
        for liked_movies in set(st.session_state.liked_movies_list_matches):
            
            variable_name = f"movie{liked_movies}"
            # Use globals() to access the variable by name
            movie = globals()[variable_name]
            # Output the movie
            st.write("------")
            output = movie_output(movie, desired_output_per_movie)        

        if len(set(st.session_state.liked_movies_list_matches)) == 0:
            st.write("\n\n")
            st.info("**There were no matches. Find a better friend.**")    

####################################################################################### chiara display genre chart
        st.title("Your Favorite Genres Are:")
        genre_data_player1 = collect_genre_data(st.session_state.liked_movies_list_player1, filtered_movies)# Collect genre data for both players
        genre_data_player2 = collect_genre_data(st.session_state.liked_movies_list_player2, filtered_movies)
        col1, col2 = st.columns(2)# Create columns for pie charts
        with col1:
            plot_genre_pie_chart(genre_data_player1, "Player 1's Favorite Movie Genres:")# Plot pie chart for Player 1 in the first column
        with col2:
            plot_genre_pie_chart(genre_data_player2, "Player 2's Favorite Movie Genres:") # Plot pie chart for Player 2 in the second column
####################################################################################### chiara display genre chart

        # Resetting the liked movies lists
        st.session_state.liked_movies_list_player1 = []
        st.session_state.liked_movies_list_player2 = []
        st.session_state.liked_movies_list_matches = []
    

st.write("------")

############################################################################################################################
#With  Help from https://discuss.streamlit.io/t/how-to-change-the-backgorund-color-of-button-widget/12103/37?page=2

ChangeButtonColour('Like', '#00AA00')
ChangeButtonColour('Not interested', '#FF0000')

##############################################################################################################################
