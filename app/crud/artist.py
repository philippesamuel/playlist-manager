from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlmodel import Session, text

from ..database.db import engine
from ..models.artist import Artist


def get_artist(
    first_name: str | None = None, last_name: str | None = None
) -> Artist | None:
    """Get an artist from the database"""
    with Session(engine) as session:
        if first_name and last_name:
            statement = select(Artist).where(
                Artist.first_name == first_name, Artist.last_name == last_name
            )
        elif first_name:
            statement = select(Artist).where(Artist.first_name == first_name)
        elif last_name:
            statement = select(Artist).where(Artist.last_name == last_name)
        else:
            return None

        if result := session.exec(statement).one_or_none():
            return result[0]


def create_artist_if_not_exists(first_name: str, last_name: str) -> Artist:
    artist = get_artist(first_name, last_name)
    if not artist:
        artist = Artist(first_name=first_name, last_name=last_name)
    return artist


def insert_artist(first_name: str, last_name: str) -> None:
    """Insert an artist into the database"""
    if get_artist(first_name, last_name):
        logger.info(f"Artist '{first_name} {last_name}' already exists in the database")
        return

    with Session(engine) as session:
        artist = Artist(first_name=first_name, last_name=last_name)
        session.add(artist)
        session.commit()


def get_artist_by_id(artist_id: int) -> Artist | None:
    """Get an artist from the database by ID"""
    with Session(engine) as session:
        artist = session.get(Artist, artist_id, options=(selectinload(Artist.songs),))
        return artist


def get_all_artists() -> list[Artist]:
    """Get all artists"""
    with Session(engine) as session:
        statement = select(Artist).options(selectinload(Artist.songs))
        result = session.exec(statement)
        return [a[0] for a in result.all()]


def search_artists(search: str = '') -> list[Artist]:
    """Search for artists in the database"""
    with Session(engine) as session:
        artists = session.exec(
            select(Artist)
            .where(
                text(f"lower(first_name ||' '|| last_name) like '%{search}%'")
                ).options(selectinload(Artist.songs)))
        return [a[0] for a in artists.all()]
    