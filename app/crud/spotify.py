from sqlmodel import Session

from ..database.db import engine
from ..models import SpotifyTrack


def insert_spotify_track_by_song_id(song_id: int, spotify_id: str) -> None:
    """Insert a Spotify track into the database"""
    with Session(engine) as session:
        spotify_track = SpotifyTrack(id=spotify_id, song_id=song_id)
        session.add(spotify_track)
        session.commit()
