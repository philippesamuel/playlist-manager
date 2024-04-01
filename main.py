import requests

from config import settings

# print(settings.model_dump())

# base URL of all Spotify API endpoints
base_url = "https://api.spotify.com/v1/"

# Spotify API endpoints
auth_url = "https://accounts.spotify.com/api/token"


def main() -> None:
    user_id = settings.user_id

    # # Replace these with your app's credentials
    # client_id = 'your_client_id'
    # client_secret = 'your_client_secret'

    # Request based on Client Credentials Flow from https://developer.spotify.com/web-api/authorization-guide/
    auth_response = requests.post(
        auth_url,
        {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
    )

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data["access_token"]

    headers = {"Authorization": "Bearer {token}".format(token=access_token)}

    # Track ID from the URI
    # track_id = '6y0igZArWVi6Iz0rj35c1Y'

    # actual GET request with proper header
    # r = requests.get(base_url + 'audio-features/' + track_id, headers=headers)

    r = requests.post(
        base_url + f"users/{user_id}/playlists",
        headers=headers,
        json={
            "name": "2024-04-07 Worship @ Mosaik Church Berlin",
            "description": "Worship setlist for April 7th, 2024 at Mosaik Church Berlin",
            "public": True,
            "collaborative": True,
        },
    )

    r = r.json()
    print(r)


if __name__ == "__main__":
    main()
