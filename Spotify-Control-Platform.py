import os
import json
import sys
import spotipy
import webbrowser
import random
import spotipy.util as util
import pprint
from json.decoder import JSONDecodeError

# == FUNCTIONS ================

# Quicksort
def QS(array):
    less = []
    equal = []
    greater = []
    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if x < pivot:
                less.append(x)
            if x == pivot:
                equal.append(x)
            if x > pivot:
                greater.append(x)
        return QS(less) + equal + QS(greater)
    else:
        return array

# Shuffle
def shuffle(array):
    n = len(array)
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        array[i], array[j] = array[j], array[i]
    return array

# Show tracks from the user
def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("%d. %s - %s" % (i, track['artists'][0]['name'], track['name']))

# =============================

#   Following a youtube tutorial: https://www.youtube.com/watch?v=tmt5SdvTqUI

#   The following code will be used to authentication user accounts and authorize them for this code's use.

#       1. To run the python code in terminal, do:
#           python3 <insert file directory here> <insert Spotify user ID here>
#       2. A web page will open up to ask for permission. Hit 'Okay'.
#       3. Google.com should open up. Copy the URL link of that page. Go back into the terminal. Paste the URL. Hit Enter.

#   User IDs for Spotify:
#       Troy: 12178698036
#       William: 1225039212
#       Stephen:

# =============================

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

print()
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
    print("3. Show all of your playlists")
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
        

        # Opening image in browser if it exists
        if artist['images']:
            webbrowser.open(artist['images'][0]['url'])

        # Album details
        trackURI = []
        trackArt = []
        trackName = []
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
                trackName.append(item['name'])
                trackURI.append(item['uri'])
                trackArt.append(albumArt)
                i+=1
            print()

        while True:
            # Artist menu
            print()
            print("What would you like to do with " + search + "?")
            print("1. List all songs alphabetically")
            print("2. Shuffle the song order")
            print("3. Inspect a song")
            print("4. Exit")
            print()
            userInput = input(">>> Enter a number: ")
            i=0

            # List all songs alphabetically
            if userInput == "1":
                print()
                print("Now printing out all songs in alphabetical order:\n")
                trackName = QS(trackName)
                for item in trackName:
                    print(str(i) + ": " + item)
                    i+=1
                print()


            # Shuffle the song order
            elif userInput == "2":
                print()
                print("Now shuffling all of " + search + "'s songs:")
                trackName = shuffle(trackName)
                for item in trackName:
                    print(str(i) + ": " + item)
                    i+=1
                print()

            # Inspect a song
            elif userInput == "3":
                print()
                trackNumber = input(">>> Which song would you like to inspect? Select a song by number: ")
                inspect = spotifyObject.track(trackURI[int(trackNumber)])
                
                # Artist menu
                print()
                print("What would you like to do with " + inspect['album']['name'] + "?")
                print("1. Preview song")
                print("2. Add song to playlist")
                print("3. ")
                print("4. Exit")
                print()
                userInput = input(">>> Enter a number: ")

                if userInput == '1':
                    print()
                    print("Now Previewing: " + inspect['album']['name'])
                    webbrowser.open(inspect['preview_url'])

            elif userInput == "4":
                print()
                break
        
        

    elif userInput == "2":
        print()
        
    elif userInput == "3":
        print()
        print("Now printing out all of " + str(displayName) + "'s playlists")

        # If the token is found
        if token:
            playlists = spotifyObject.user_playlists(userID)
            for playlist in playlists['items']:

                if playlist['owner']['id'] == userID:
                    print()
                    print("[PLAYLIST] " + playlist['name'] + "\n----------------------------------")
                    print('Number of tracks in playlist: ', playlist['tracks']['total'])
                    results = spotifyObject.user_playlist(userID, playlist['id'],
                        fields="tracks,next")
                    tracks = results['tracks']
                    show_tracks(tracks)
                    while tracks['next']:
                        tracks = spotifyObject.next(tracks)
                        show_tracks(tracks)
        
        # If the token cannot be found
        else:
            print("Error! Token not found!")
        
        print()

    elif userInput == "4":
        print("Thank you! Have a nice day! c:")
        sys.exit(1)
    
    else:
        print("Sorry! That input is not recognized. Please try again.")
        print()

#   Used to print json data when needed:
#       print(json.dumps(<insert VARABLE here>, sort_keys=True, indent=4))