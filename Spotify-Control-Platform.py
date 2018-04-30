import os
import json
import sys
import spotipy
import webbrowser
import random
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
#       William: 1225039212
#       Stephen:

#   Get user's ID from the terminal
userID = sys.argv[1]

#   Erase cache and prompt for user permission:
try:
    token = util.prompt_for_user_token(userID)
except:
    os.remove(f".cache-{userID}")
    token = util.prompt_for_user_token(userID)

# ===============================================================================================

#   Creatng a spotifyObject and a user variable
spotifyObject = spotipy.Spotify(auth=token)
user = spotifyObject.current_user()
displayName = user['display_name']

print("========================================")
print("======= Spotify Control Platform =======")
print("========================================")
print()
print(">>> Welcome, " + str(displayName) + "!")
print()

while True:
    print("- - - - - - - -")
    print()
    print(">>> What would you like to do?")
    print(">>> 1.")
    print(">>> 2.")
    print(">>> 3.")
    print(">>> 4. Exit")
    print()
    userInput = input(">>> Enter a number: ")

    if userInput == "1":
        print()

    elif userInput == "2":
        print()
        
    elif userInput == "3":
        print()

    elif userInput == "4":
        print("Thank you! Have a nice day! c:")
        exit
    
    else:
        print("Sorry! That input is not recognized. Please try again.")
        print()

#   Used to print json data when needed:
#       print(json.dumps(<insert VARABLE here>, sort_keys=True, indent=4))

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

def shuffle(array):
    n = len(array)
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        array[i], array[j] = array[j], array[i]
    return array