import os
import json
import sys
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

#   Following a youtube tutorial: https://www.youtube.com/watch?v=tmt5SdvTqUI

#   The following code will be used to authentication user accounts and authorize them for this code's use.

#       1. To run the python code in terminal, do:
#           python3 <insert file directory here> <insert Spotify user ID here>
#       2. A web page will open up to ask for permission. Hit 'Okay'.
#       3. Google.com should open up. Copy the URL link of that page. Go back into the terminal. Paste the URL. Hit Enter.

#   User IDs for Spotify:
#       Troy: 12178698036
#       William:
#       Stephen:

#   Get user's ID from the terminal
userID = sys.argv[1]
scope = 'user-read-private user-read-playback-state user-modify-playback-state'

#   Erase cache and prompt for user permission:
try:
    token = util.prompt_for_user_token(userID, scope)
except:
    os.remove(f".cache-{userID}")
    token = util.prompt_for_user_token(userID, scope)

# ===============================================================================================

#   Creatng a spotifyObject and a user variable
spotifyObject = spotipy.Spotify(auth=token)
user = spotifyObject.current_user()
displayName = user['display_name']

# Get device
# devices = spotifyObject.devices()
# print(json.dumps(devices, sort_keys=True, indent=4))
# print()
# deviceID = devices['devices'][0]['id']

# Current track playing
# currentPlaying = spotifyObject.current_user_playing_track()
# print(json.dumps(devices, sort_keys=True, indent=4))
# print()
# artist = currentPlaying['item']['artists'][0]['name']
# currentPlaying = currentPlaying['item']['name']

# if artist != "":
#     print("Now Playing: " + artist + " - " + currentPlaying)

print("========================================")
print("======= Spotify Control Platform =======")
print("========================================")
print()
print("Welcome, " + str(displayName) + "!")
print()

while True:
    print("- - - - - - - -")
    print()
    print("What would you like to do?")
    print("1. Serach for an artist")
    print("2. Search for a song")
    print("3. ")
    print("4. Exit")
    print()
    userInput = input(">>> Enter a number: ")

    # Serach for an artist
    if userInput == "1":
        print()
        search = input(">>> Enter the artist's alias: ")
        print()

        # Grabbing artist data from index 0 (the first result)
        result = spotifyObject.search(search,1,0,"artist")
        artist = result['artists']['items'][0]
        artistID = artist['id']
        album = spotifyObject.artist_albums(artistID)
        album = artist['id']

        # Opening image in browser
        webbrowser.open(artist['images'][0]['url'])

        # Album details
        trackURI = []
        trackArt = []
        i = 0
        album = spotifyObject.artist_albums(artistID)
        album = album['items']

        print("Now accessing: " + artist['name'])
        print()

        for item in album:
            print("[ ALBUM ] " + item['name'])
            albumID = item['id']
            albumArt = item['images'][0]['url']
            tracks = spotifyObject.album_tracks(albumID)
            tracks = tracks['items']

            for item in tracks:
                print(str(i) + ": " + item['name'])
                trackURI.append(item['uri'])
                trackArt.append(albumArt)
                i+=1
            print()

        while True:
            # Artist menu
            print()
            print("What would you like to do for this artist?")
            print("1. Play a song")
            print("1. List top 10 songs (by play count)")
            print("2. List all albums")
            print("3. Exit")
            print()
            userInput = input(">>> Enter a number: ")

            # Play a song
            if userInput == "1":
                print()

            # List top 10 songs (by play count)
            if userInput == "1":
                print()

            elif userInput == "4":
                print()
                break
        
        

    elif userInput == "2":
        print()
        
    elif userInput == "3":
        print()

    elif userInput == "4":
        print("Thank you! Have a nice day! c:")
        sys.exit(1)
    
    else:
        print("Sorry! That input is not recognized. Please try again.")
        print()

#   Used to print json data when needed:
#       print(json.dumps(<insert VARABLE here>, sort_keys=True, indent=4))