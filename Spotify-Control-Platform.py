import os
import json
import sys
import spotipy
import webbrowser
import random
import spotipy.util as util
import pprint
import subprocess
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

# SelectionSort
def SelSort(A):
    for i in range(len(A)):
        min_index = i
        for j in range(i + 1, len(A)):
            if A[min_index] > A[j]:
                min_index = j
        A[i], A[min_index] = A[min_index], A[i]
    return A

# MergeSort
def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m
    L = [0] * (n1)
    R = [0] * (n2)

    for i in range(0 , n1):
        L[i] = arr[l + i]

    for j in range (0, n2):
        R[i] = arr[m + 1 + j]

    i = 0
    j = 0
    k = l

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def mergeSort(arr, l, r):
    if l < r:
        m = (l + (r - 1)) / 2

        mergeSort(arr, l, m)
        mergeSort(arr, m + 1, r)
        merge(arr, l, m, r)

# Heapify
def heapify(arr, n, root):
    largest = root
    l = 2 * root + 1
    r = 2 * root + 2

    if l < n and arr[root] < arr[l]:
        largest = l

    if r < n and arr[root] < arr[r]:
        largest = r

    if largest != root:
        arr[root], arr[largest] = arr[largest], arr[root]
        heapify(arr, n, largest)

# Heapsort
def heapSort(arr):
    n = len(arr)

    for i in range(n, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

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
scope = 'user-read-private user-read-playback-state user-modify-playback-state playlist-modify-public'

#   Erase cache and prompt for user permission:
# try:
token = util.prompt_for_user_token(userID, scope)
# except:
    # os.remove(f".cache-{userID}")
    # token = util.prompt_for_user_token(userID, scope)

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

masterPlaylist = []

while True:
    print("- - - - - - - -")
    print()
    print("What would you like to do?")
    print("1. Serach for an artist and song to store in a playlist")
    print("2. Show all of your public playlists")
    print("3. Sort/Shuffle your buffer playlist")
    print("4. Create a playlist with the selected songs")
    print("5. Exit")
    print()
    userInput = input(">>> Enter a number: ")

    # Serach for an artist and song
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
            print("2. Select a song")
            print("3. Exit")
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

            # Select a song
            elif userInput == "2":
                print()
                trackNumber = input(">>> Which song would you like to select? Choose a song by number: ")
                inspect = spotifyObject.track(trackURI[int(trackNumber)])
                
                while True:
                    # Artist menu
                    print()
                    print("What would you like to do with " + inspect['name'] + "?")
                    print("1. Preview song")
                    print("2. Add song to playlist")
                    print("3. Exit")
                    print()
                    userInput = input(">>> Enter a number: ")

                    if userInput == '1':
                        print()
                        print("Now Previewing: " + inspect['album']['name'])
                        webbrowser.open(inspect['preview_url'])

                    elif userInput == "2":
                        print()
                        print("Adding song to the buffer playlist...")
                        masterPlaylist.append(inspect['id'])

                    elif userInput == "3":
                        print()
                        break

            elif userInput == "3":
                print()
                break
        
    # Show all of your public playlists        
    elif userInput == "2":
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

    # Sort your buffer playlist
    elif userInput == "3":
        print()
        print("What would you like to do with your buffer playlist?")
        print("1. Sort alphabetically through Quicksort")
        print("2. Sort alphabetically through Selection Sort")
        print("3. Sort alphabetically through Heap Sort")
        print("4. Sort alphabetically through Merge Sort")
        print("5. Shuffle the song order")
        print("6. Exit")
        print()
        userInput = input(">>> Enter a number: ")
        i=0

        # Quicksort
        if userInput == "1":
            print()
            print("Sorting using Quicksort...")
            masterPlaylist = QS(masterPlaylist)
            print("Sorted!")

        # Selection Sort
        elif userInput == "2":
            print()
            print("Sorting using Selection Sort...")
            masterPlaylist = SelSort(masterPlaylist)
            print("Sorted!")

        # Heap Sort
        elif userInput == "3":
            print()
            print("Sorting using Quicksort...")
            # masterPlaylist = heapSort(masterPlaylist)
            print("Sorted!")
            
        # Merge Sort
        elif userInput == "4":
            print()
            print("Sorting using Merge Sort...")
            # masterPlaylist = mergeSort(masterPlaylist, 0, len(masterPlaylist))
            print("Sorted!")

        # Shuffle
        elif userInput == "5":
            print()
            print("Shuffling buffer playlist...")
            masterPlaylist = shuffle(masterPlaylist)
            print("Shuffled!")

        # Exit
        elif userInput == "6":
            print()

    # Create a playlist
    elif userInput == "4":
        print()
        print("Creating playlist...")

        # Ask for user input for playlist name and description
        playlistName = input(">>> What do you want to name the playlist? ")
        playlistDescription = input(">>> Write a description for the playlist: ")

        # Create playlist and enter the songs
        spotifyObject.trace = False
        playlists = spotifyObject.user_playlist_create(userID, playlistName, description=playlistDescription)

        # Fill playlist with the songs chosen
        playlistURI = playlists['uri']
        if masterPlaylist:
            results = spotifyObject.user_playlist_add_tracks(userID, playlistURI, masterPlaylist)

        print()
        print("=== PLAYLIST [" + playlistName + "] CREATED ===")
        print()

    # Exit
    elif userInput == "5":
        print()
        print("Thank you! Have a nice day! c:")
        print()
        sys.exit(1)
    
    else:
        print("Sorry! That input is not recognized. Please try again.")
        print()

#   Used to print json data when needed:
#       print(json.dumps(<insert VARABLE here>, sort_keys=True, indent=4))