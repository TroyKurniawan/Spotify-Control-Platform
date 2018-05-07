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
class masterstorage():
    def ref(self):
        return self.values
    def names(self):
        return self.listofnames
    def __init__(self, A, B:
        self.values = A
        self.listofnames = B

# Quicksort
def QS(array, name):
    less = []
    equal = []
    greater = []

    l = []
    e = []
    g = []

    if len(array) > 1 and len(name) > 1:
        pivot = name[0]
        i=0
        for x in name:
            if x < pivot:
                less.append(array[i])
                l.append(x)
            if x == pivot:
                equal.append(array[i])
                e.append(x)
            if x > pivot:
                greater.append(array[i])
                g.append(x)
            i+=1
        return QS(less, l) + equal + QS(greater, g)
    else:
        return array

# SelectionSort
def SelSort(A, B):
    for i in range(len(B)):
        min_index = i
        for j in range(i + 1, len(B)):
            if B[min_index] >= B[j]:
                min_index = j
        A[i], A[min_index] = A[min_index], A[i]
        B[i], B[min_index] = B[min_index], B[i]
        print(B[min_index])
    return A

# MergeSort

def mergefunc(left, right):
    i = 0
    j = 0
    hold = []

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            hold.append(left[i])
            i += 1
        else:
            hold.append(right[j])
            j += 1
    while i < len(left):
        hold.append(left[i])
        i += 1
    while j < len(right):
        hold.append(right[j])
        j += 1
    return hold


def mergeSort(A):
    n = len(A)
    if n <= 1:
        return A
    left = mergeSort(A[:round(n / 2)])
    right = mergeSort(A[round(n / 2):n])
    return mergefunc(left, right)

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
        print("    %s - %s" % (track['artists'][0]['name'], track['name']))

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
# token = util.prompt_for_user_token(userID, scope)
token = util.prompt_for_user_token( userID,
                                    scope,
                                    client_id='05856e0782d0460ea1319ef2cbc98167',
                                    client_secret='ffb65ee2ca7c44d4a7e7f4411f3d0b7b',
                                    redirect_uri='http://google.com/'
                                    )


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

isSorted = False
masterPlaylist = []
masterPlaylistName = []
masterDuration = []

while True:
    print("- - - - - - - - - - - - - - - - - - - - - -")
    print()
    print("What would you like to do?")
    print("1. Search for an artist and song to store in a playlist")
    print("2. Show all of your public playlists")
    print("3. Sort/Shuffle your buffer playlist")
    print("4. Create a playlist with the selected songs")
    print("5. Clear the buffer playlist")
    print("0. Exit")
    print()
    userInput = input(">>> Enter a number: ")

    # Search for an artist and song
    if userInput == "1":
        print()
        search = input("    >>> Enter the artist's alias: ")
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

        print("    Now accessing: " + artist['name'])
        print()

        for item in album:
            print("    [ ALBUM ] " + item['name'])
            albumID = item['id']
            albumArt = item['images'][0]['url']
            tracks = spotifyObject.album_tracks(albumID)
            tracks = tracks['items']

            for item in tracks:
                print("    " + str(i) + ": " + item['name'])
                trackName.append(item['name'])
                trackURI.append(item['uri'])
                trackArt.append(albumArt)
                i+=1
            print()

        while True:
            # Artist menu
            print()
            print("    What would you like to do with " + search + "?")
            print("    1. Select a song")
            print("    0. Exit")
            print()
            userInput = input("    >>> Enter a number: ")
            i=0

            # Select a song
            if userInput == "1":
                print()
                trackNumber = input("        >>> Which song would you like to select? Choose a song by number: ")
                inspect = spotifyObject.track(trackURI[int(trackNumber)])
                
                while True:
                    # Artist menu
                    print()
                    print("        What would you like to do with " + inspect['name'] + "?")
                    print("        1. Preview song")
                    print("        2. View artwork")
                    print("        3. Add song to playlist")
                    print("        0. Exit")
                    print()
                    userInput = input("        >>> Enter a number: ")

                    if userInput == '1':
                        print()
                        print("             Now Previewing: " + inspect['name'])
                        webbrowser.open(inspect['preview_url'])

                    elif userInput == "2":
                        print()
                        print("            Now viewing artwork for " + inspect['name'])
                        webbrowser.open(inspect['album']['images'][0]['url'])

                    elif userInput == "3":
                        print()
                        print("            Adding " + inspect['name'] + " to the buffer playlist...")
                        masterPlaylist.append(inspect['id'])
                        masterPlaylistName.append(inspect['name'])
                        masterDuration.append(inspect['duration_ms'])

                    elif userInput == "0":
                        print()
                        break

            # Exit
            elif userInput == "0":
                print()
                break
        
    # Show all of your public playlists        
    elif userInput == "2":
        print()
        print("    Now printing out all of " + str(displayName) + "'s playlists")

        # If the token is found
        if token:
            playlists = spotifyObject.user_playlists(userID)
            for playlist in playlists['items']:

                if playlist['owner']['id'] == userID:
                    print()
                    print("    [PLAYLIST] " + playlist['name'] + "\n    ----------------------------------")
                    print('    Number of tracks in playlist: ', playlist['tracks']['total'])
                    print("    ----------------------------------")
                    results = spotifyObject.user_playlist(userID, playlist['id'], fields="tracks,next")
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

        # if isSorted:
        #     print()
        #     print("    Note: You have already sorted the buffer playlist. You may not sort it again until you've cleared the buffer playlist.")
        #     continue

        while True:
            print()
            print("    What would you like to do with your buffer playlist?")
            print("    1. Sort alphabetically through Quicksort")
            print("    2. Sort alphabetically through Selection Sort")
            print("    3. Sort alphabetically through Merge Sort")
            print("    4. Sort by songs duration (Quicksort)")
            print("    5. Shuffle the song order")
            print("    0. Exit")
            print()
            userInput = input("    >>> Enter a number: ")
            i=0

            # Quicksort
            if userInput == "1":
                print()
                print("        Sorting using Quicksort...")
                masterPlaylist = QS(masterPlaylist, masterPlaylistName)
                masterPlaylistName = QS(masterPlaylistName, masterPlaylistName)
                print("        Sorted!\n")

            # Selection Sort
            elif userInput == "2":
                print()
                print("        Sorting using Selection Sort...")
                masterPlaylist = SelSort(masterPlaylist, masterPlaylistName)
               # print(masterPlaylistName)
                masterPlaylistName = SelSort(masterPlaylistName, masterPlaylistName)
                #print(masterPlaylistName)
                print("        Sorted!\n")
                
            # Merge Sort
            elif userInput == "3":
                print()
                print("        Sorting using Merge Sort...")
                #masterPlaylist = mergeSortpair(masterPlaylist, masterPlaylistName)
                #need to store pairing in a new array
                master = masterstorage(masterPlaylist, masterPlaylistName)
                master.names = masterPlaylistName
                master.ref = masterPlaylist
                master = mergeSort(master.names)

                masterPlaylist = master.ref
                masterPlaylistName = master.names
                print("        Sorted!\n")

            # Sort by songs duration (Quicksort)
            elif userInput == "4":
                print()
                print("        Sorting by song duration...")
                masterPlaylist = QS(masterPlaylist, masterDuration)
                masterPlaylistName = QS(masterPlaylistName, masterDuration)
                masterDuration = QS(masterDuration, masterDuration)
                print("        Sorted!\n")

            # Shuffle
            elif userInput == "5":
                print()
                print("        Shuffling buffer playlist...")
                masterPlaylist = shuffle(masterPlaylist)
                print("        Shuffled!\n")

            # Exit
            elif userInput == "0":
                print()
                break

            else:
                print("Sorry! That input is not recognized. Please try again.")
                print()

    # Create a playlist
    elif userInput == "4":
        print()
        
        if len(masterPlaylist) == 0:
            print("    WARNING! Your buffer playlist is currently empty. Do you wish to proceed anyways?")
            YoN = input("    >>> 1 (Yes) | 2 (No): ")
            if YoN == "1":
                print("    Continuing...")
            elif YoN == "2":
                print()
                continue

        print("    Creating playlist...")

        # Ask for user input for playlist name and description
        playlistName = input("    >>> What do you want to name the playlist? ")
        playlistDescription = input("    >>> Write a description for the playlist: ")

        # Create playlist and enter the songs
        spotifyObject.trace = False
        playlists = spotifyObject.user_playlist_create(userID, playlistName)#, description=playlistDescription)

        # Fill playlist with the songs chosen
        playlistURI = playlists['uri']
        if masterPlaylist:
            results = spotifyObject.user_playlist_add_tracks(userID, playlistURI, masterPlaylist)

        print()
        print("    === PLAYLIST [" + playlistName + "] CREATED ===")
        print()

    # Clear the buffer playlist
    elif userInput == "5":
        print()
        print("    Clearing buffer playlist...")
        masterPlaylist[:] = []
        masterPlaylistName[:] = []
        isSorted = False
        print("    Cleared!")
        print()

    # Exit
    elif userInput == "0":
        print()
        print("Thank you! Have a nice day! c:")
        print()
        sys.exit(1)
    
    else:
        print("Sorry! That input is not recognized. Please try again.")
        print()

#   Used to print json data when needed:
#       print(json.dumps(<insert VARABLE here>, sort_keys=True, indent=4))