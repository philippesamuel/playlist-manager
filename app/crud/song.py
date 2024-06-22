from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlmodel import Session, text

from ..database.db import engine
from ..models.song import Song
from .artist import create_artist_if_not_exists


def get_song(song_name: str) -> Song | None:
    """Get a song from the database"""
    with Session(engine) as session:
        statement = select(Song).where(Song.name == song_name)
        if result := session.exec(statement).one_or_none():
            return result[0]


def insert_song(
    song_name: str,
    artists_names: list[tuple[str, str]] | None = None,
    ccli_number: int | None = None,
) -> None:
    """Insert a song into the database"""
    if get_song(song_name):
        logger.info(f"Song {song_name} already exists in the database")
        return

    with Session(engine) as session:
        song = Song(name=song_name, ccli_number=ccli_number)

        if artists_names:
            artists = [
                create_artist_if_not_exists(fn, ln) for fn, *_, ln in artists_names
            ]
            song.artists = artists
        session.add(song)
        session.commit()


def update_song(
    song_name: str,
    artists_names: list[tuple[str, str]] | None = None,
    ccli_number: int | None = None,
) -> None:
    """Update a song in the database"""
    with Session(engine) as session:
        statement = select(Song).where(Song.name == song_name)
        if not (result := session.exec(statement).one_or_none()):
            logger.info(f"Song {song_name} does not exist in the database")
            return

        song = result[0]
        if ccli_number:
            song.ccli_number = ccli_number

        if artists_names:
            artists = [
                create_artist_if_not_exists(fn, ln) for fn, *_, ln in artists_names
            ]
            artists = [artist for artist in artists if artist not in song.artists]
            song.artists.extend(artists)
        session.add(song)
        session.commit()


def get_song_by_id(song_id: int, session: Session) -> Song | None:
    """Get a song from the database by ID"""
    song = session.get(Song, song_id, options=(selectinload(Song.artists),))
    return song


def search_songs(search: str = '') -> list[Song]:
    """Search for songs in the database"""
    with Session(engine) as session:
        songs = session.exec(
            select(Song)
            .where(
                text(f"lower(name) like '%{search}%'")
                ).options(selectinload(Song.artists)))
        return [s[0] for s in songs.all()]


def get_all_songs() -> list[Song]:
    """Get all songs"""
    with Session(engine) as session:
        statement = select(Song).options(selectinload(Song.artists))
        result = session.exec(statement)
        return [s[0] for s in result.all()]