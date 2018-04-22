import os
import json
import sys
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

# The following code will be used to authentication user accounts and authorize them for this code's use.

#       1. To run the python code in terminal, do:
#           python3 <insert file directory here> <insert Spotify user ID here>
#       2. A web page will open up to ask for permission. Accept.
#       3. Google.com should open up. Copy the URL link. Go back into the terminal. Paste the URL. Hit Enter.

# User IDs for Spotify:
#     Troy: 12178698036
#     William:
#     Stephen:

# Get username from the terminal
username = sys.argv[1]

# Erase cache and prompt for user permission:
try:
    token = util.prompt_for_user_token(username)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)

# Creatng a spotifyObject
spotifyObject = spotipy.Spotify(auth=token)

# ======================================================================