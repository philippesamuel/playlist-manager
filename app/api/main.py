import os
from datetime import timedelta
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlmodel import Session

from ..crud.artist import get_all_artists, get_artist_by_id, search_artists
from ..crud.song import get_all_songs, get_song_by_id, search_songs
from ..database.db import get_session
from ..models.auth import Token
from ..models.user import User
from ..models.song import SongPublic
from ..models.artist import ArtistPublic
from .dependencies import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
)
from .dependencies import fake_users_db


SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://localhost:5500/frontend",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/songs/{song_id}", response_model=SongPublic)
def read_song(
    song_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session),
):
    song = get_song_by_id(song_id, session)
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return song


@app.get("/artists/{artist_id}", response_model=ArtistPublic)
def read_artist(
    artist_id: int, current_user: Annotated[User, Depends(get_current_active_user)]
):
    artist = get_artist_by_id(artist_id)
    if artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist


@app.get("/songs", response_model=list[SongPublic])
def read_songs(
    search: str = None,
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
):
    if search:
        return search_songs(search)
    return get_all_songs()


@app.get("/artists", response_model=list[ArtistPublic])
def read_artists(
    search: str = None,
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
):
    if search:
        return search_artists(search)
    return get_all_artists()
