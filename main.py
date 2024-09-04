import yt_dlp as youtube_dl

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from youtube_search import YoutubeSearch

import os
import time

SPOTIPY_CLIENT_ID = "d21033b5995f4abb9cbf6dfc224947aa"
SPOTIPY_CLIENT_SECRET = "021e09d38959443f99b7076b5f3bacff"
SPOTIPY_REDIRECT_URL = "http://localhost:8888/callback"

scope = "user-library-read"

auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URL, scope=scope)

 

options = ["youtube", "soundcloud", "spotify"]


url = input("Enter the URL of the file you'd like to download: ")


def get_choice():
    for i, option in enumerate(options):
        print(f"{i+1}: {option}")
    
    
    looping = True
    
    while looping:
        choice = input("Enter the number of your choice: ")
    
        try: 
            choice = int(choice)
        
        except ValueError:
            print("Incorrect value type. Please enter a number between 1 and 3.")
            continue
        
        if int(choice) < 1 or int(choice) > 3:
            print("Incorrect value. Please enter a number between 1 and 3.")
            continue
        else:
            looping = False
            
    choice = options[choice-1]
    return choice
       
        
        
user_choice = get_choice()

def downloader(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.realpath('downloaded_Files') + '/%(title)s.%(ext)s',
        'ffmpeg_location': os.path.realpath('C:\\Users\\mason\\OneDrive\\Documents\\Desktop\\pythonProjects\\mp3downloader\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])



if user_choice == "youtube":
    downloader(url)


elif user_choice == "soundcloud":
    downloader(url)
    
    
    
else:
    parts = url.split('/')
    track_id = parts[4].split('?')[0]
    
    url = f"spotify:track:{track_id}"
    
    try:
        sp = spotipy.Spotify(auth_manager=auth_manager)
    
    
        track_info = sp.track(url)
    
        artist_name = track_info['artists'][0]['name']
        track_name = track_info['name']
        print("[1]: Finding song information on spotify...")
        time.sleep(2)
        
        
    except:
        print("[2]: Song not found. Program is exiting...")
        exit()
    
    
    text_to_search = artist_name + " - " + track_name
    if text_to_search:
        print("[2]: Song found! -> " + text_to_search)


    time.sleep(1)
    
    print("[3] Extracting results from youtube. This could take a while.")
    results = YoutubeSearch(text_to_search, max_results=1).to_dict()
    
    
    time.sleep(1)
    
    
    url = "https://www.youtube.com" + results[0]['url_suffix']
    print("[4] Found the song on youtube! -> " + url)
    
    
    print("[5] Downloading...")
    downloader(url)
    