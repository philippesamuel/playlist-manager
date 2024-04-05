import requests
from loguru import logger
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route
from starlette.responses import PlainTextResponse, JSONResponse

from config import settings

# Client info
CLIENT_ID = settings.client_id
CLIENT_SECRET = settings.client_secret
REDIRECT_URI = settings.redirect_uri

# Spotify API endpoints
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://127.0.0.1:8000/token"


app = Starlette(debug=True)


@app.route("/callback", methods=["GET"])
async def callback(request: Request):
    error = request.query_params.get("error")
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    stored_state = request.cookies.get("spotify_auth_state")

    # Check state
    if state is None or state != stored_state:
        logger.error(f"Error message: {repr(error)}")
        logger.error(f"State mismatch: {stored_state} != {state}")
        return PlainTextResponse("Error: state mismatch", status_code=400)

    # Request tokens with code we obtained
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    # `auth=(CLIENT_ID, SECRET)` basically wraps an 'Authorization'
    # header with value:
    # b'Basic ' + b64encode((CLIENT_ID + ':' + SECRET).encode())
    res = requests.get(TOKEN_URL, verify=False)
    # res = await requests.post(TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload, verify=False)
    print(res.json())
    return PlainTextResponse("Callback received")
    res_data = res.json()

    if res_data.get("error") or res.status_code != 200:
        error_message = res_data.get("error", "No error information received.")
        logger.error(f"Failed to receive token: `{error_message}`")
        return PlainTextResponse(
            "Error: failed to receive token", status_code=res.status_code
        )

    # Load tokens into session
    requests.session["tokens"] = {
        "access_token": res_data.get("access_token"),
        "refresh_token": res_data.get("refresh_token"),
    }

    return PlainTextResponse("Callback received")
