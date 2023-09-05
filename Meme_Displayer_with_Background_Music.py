import tkinter as tk
import requests
import yt_dlp as youtube_dl
import random
import time
import vlc
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

# Create the main window
root = tk.Tk()

# Title of the main window
root.title("Meme Displayer with Background Music")

# Initialize the VLC player instance
instance = vlc.Instance()
player = instance.media_player_new()

# Function for playing a song based on artist and title input
def song_player(artist, title):
    
    # Create a query to search from the song on YouTube
    query = f"{artist} - {title} official audio"
    
    # Define yt-dlp options for extracting audio information
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }
    # Use yt-dlp to extract video information
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch1:{query}", download=False)
        # Check if the song exist in the YouTube
        if 'entries' in result:
            first_video = result['entries'][0]
            video_url = first_video['url']
           
            media = instance.media_new(video_url)
            player.set_media(media)
            player.play()
            print(f"Now playing: {first_video['title']}")
        else:
            print("No matching song found on YouTube.")
            
# Function to stop the music from playing
def stop_song():
    player.stop()

# Function to fetch memes based on user input
def fetch_memes(keyword, num_of_display):
    
    # Loop through the input number of display value 
    for _ in range(num_of_display):
        
        # Search the user input keywork in google  
        search_url = f"https://www.google.com/search?q={keyword}+meme&tbm=isch"
        response = requests.get(search_url)
       
        # When the earch is successful 
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract image tags from the HTML
            img_tags = soup.find_all('img')
            
            # Extract meme image URLs
            meme_urls = [img['src'] for img in img_tags if 'src' in img.attrs]
            
            # If the meme exists, choose randomly and display meme
            if meme_urls:
                random_mem_url = random.choice(meme_urls)
                print(f"Displaying a meme for you..:")
                response = requests.get(random_mem_url)
                img = Image.open(BytesIO(response.content))
                img.show()
               
            else:
                print("No memes found for the keyword.")
               
        else:
            print("Failed to fetch memes.")
        
        # wait 5 second before displaying the next meme  
        time.sleep(5)

# Function to start displaying memes    
def start_display():
    keyword = keyword_entry.get()
    num_of_display = int(num_of_display_entry.get())
    fetch_memes(keyword, num_of_display)

# Create labels and entries for the GUI
welcome_label = tk.Label(root, text="Welcome to the Meme Searcher!")
welcome_label.pack()
   
keyword_label = tk.Label(root, text="What kind of memes are you looking for? ")
keyword_label.pack()
   
keyword_entry = tk.Entry(root)
keyword_entry.pack()
   
num_of_display_label = tk.Label(root, text="How many times do you want to display: ")
num_of_display_label.pack()
   
num_of_display_entry = tk.Entry(root)
num_of_display_entry.pack()

artist_label = tk.Label(root, text="Artist")
artist_label.pack()

artist_entry = tk.Entry(root)
artist_entry.pack()

title_label = tk.Label(root, text="Title")
title_label.pack()

title_entry = tk.Entry(root)
title_entry.pack()

play_button = tk.Button(root, text='Play Song', command=lambda:song_player(artist_entry.get(), title_entry.get()))
play_button.pack()

stop_button = tk.Button(root, text='Stop', command=stop_song)
stop_button.pack()
   
start_button = tk.Button(root, text="Start Display", command=start_display)
start_button.pack()

root.mainloop()
