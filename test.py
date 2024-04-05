import time
import requests
import secrets
import string
from urllib.parse import urlencode

from config import settings
import webbrowser

# Client info
CLIENT_ID = settings.client_id
CLIENT_SECRET = settings.client_secret
REDIRECT_URI = settings.redirect_uri
ACCESS_TOKEN = "..."

# Spotify API endpoints
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"

# base URL of all Spotify API endpoints
BASE_URL = "https://api.spotify.com/v1/"
ME_URL = f"{BASE_URL}/me"


def get_authorization_code():
    # Generate a random state string to prevent CSRF forgery
    state = "".join(
        secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16)
    )

    # Define the authorization URL
    auth_params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "state": state,
        "scope": "user-read-private user-read-email",
        "show_dialog": True,
    }
    auth_url = AUTH_URL + "?" + urlencode(auth_params)

    # Open the authorization URL in the user's browser
    webbrowser.open(auth_url)

    # Wait for the user to authorize the application and retrieve the authorization code
    authorization_code = input("Enter the authorization code: ")

    return authorization_code


def get_access_token(authorization_code):
    # Exchange the authorization code for an access token
    token_params = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(TOKEN_URL, data=token_params)
    response_data = response.json()

    # Extract the access token from the response
    access_token = response_data.get("access_token")

    return access_token


def create_playlist(access_token):
    # Create a new playlist using the access token
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
    }
    playlist_data = {
        "name": "2024-04-07 Worship @ Mosaik Church Berlin",
        "description": "Worship setlist for April 7th, 2024 at Mosaik Church Berlin",
        "public": True,
        "collaborative": True,
    }
    response = requests.post(ME_URL + "/playlists", headers=headers, json=playlist_data)
    response_data = response.json()

    # Extract the playlist ID from the response
    playlist_id = response_data.get("id")

    return playlist_id

def main():
    # authorization_code = get_authorization_code()
    # print("Authorization code:", authorization_code)
    # access_token = get_access_token(authorization_code)
    # playlist_id = create_playlist(access_token)
    # print("Playlist created with ID:", playlist_id)

    # Search for tracks
    track_names = [
        "Great Things",
        "The blood will never loose",
        "God you're so good",
        "Who you say I am",
    ]

    for track_name in track_names:
        time.sleep(2)
        track_id = search_track(
            access_token=ACCESS_TOKEN, 
            query=f"track='{track_name}'")
        print(f"Track ID for {track_name}:", track_id)

    # track_id = search_track(
    #     access_token=ACCESS_TOKEN, 
    #     query="track='Grosse Wunder'")
    # print("Track ID:", track_id)


def search_track(access_token, query):
    # Search for a track using the access token
    headers = {"Authorization": "Bearer " + access_token}
    params = {"q": query, "type": "track", "limit": 1}
    response = requests.get(BASE_URL + "search", headers=headers, params=params)
    response_data = response.json()
    if response.status_code != 200:
        print("Error:", response_data)
        return None
    return response_data["tracks"]["items"][0]["id"]


if __name__ == "__main__":
    main()
