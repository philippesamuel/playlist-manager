from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db.db import (
    Song,
    Artist,
    get_song_by_id,
    get_artist_by_id,
    get_all_songs,
    get_all_artists,
    search_artists,
    search_songs,
)

app = FastAPI()


class SongArtistModel(BaseModel):
    id: int
    first_name: str
    last_name: str


class SongModel(BaseModel):
    id: int
    name: str
    ccli_number: int | None
    artists: list[SongArtistModel]


class ArtistSongModel(BaseModel):
    id: int
    name: str
    ccli_number: int | None


class ArtistModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    songs: list[ArtistSongModel]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/songs/{song_id}", response_model=SongModel)
def read_song(song_id: int) -> SongModel:
    song = get_song_by_id(song_id)
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return song


@app.get("/artists/{artist_id}", response_model=ArtistModel)
def read_artist(artist_id: int) -> ArtistModel:
    artist = get_artist_by_id(artist_id)
    if artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist


@app.get("/songs/")
def read_songs(search: str = None) -> list[SongModel]:
    if search:
        return search_songs(search)
    return get_all_songs()


@app.get("/artists/")
def read_artists(search: str = None) -> list[ArtistModel]:
    if search:
        return search_artists(search)
    return get_all_artists()
