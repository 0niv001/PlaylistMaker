import bs4
import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Ask user for input and take year out of date
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")
year = date[0:4]

# Billboard url
URL = "https://www.billboard.com/charts/hot-100/"

# Spotify Authentication info
id = os.environ["CLIENT_ID"]
secret = os.environ["SECRET"]
uri = "http://example.com"
user_id = "nirvesh_99"
scope = "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=id, client_secret=secret, redirect_uri=uri,
                                               cache_path=".cache", username=user_id))

results = sp.current_user()

song_uri = []

# Scraper taking list of charting song from date given in input
response = requests.get(f"{URL}{date}/")
songs = response.text
soup = bs4.BeautifulSoup(songs, "html.parser")
titles = soup.select(selector="li ul li h3")
s_list = [item.getText().strip() for item in titles]

# search spotify for songs in billboard list and find their URIs
for song in s_list:
    s = sp.search(q=song, type="track", market="GB", limit=10)
    release = s["tracks"]["items"][0]["album"]["release_date"]
    if date in release:
        song_uri.append(s["tracks"]["items"][0]["uri"])


# Create a spotify playlist and adds tracks from list based on the URI list
create_playlist = sp.user_playlist_create(user=user_id, name="Billboard 100- Python test", public=False,
                                          description="Create a playlist using Spotify API")
playlist_id = create_playlist["id"]
add_track = sp.playlist_add_items(playlist_id=playlist_id, items=song_uri, )
