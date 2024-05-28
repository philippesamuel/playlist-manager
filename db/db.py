from contextlib import contextmanager

from loguru import logger
from pydantic import computed_field
from sqlalchemy import create_engine, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import selectinload
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, text


def get_session():
    with Session(engine) as session:
        yield session
    

class ArtistSongLink(SQLModel, table=True):
    """Link table between Artist and Song"""

    artist_id: int | None = Field(
        default=None, foreign_key="artist.id", primary_key=True
    )
    song_id: int | None = Field(default=None, foreign_key="song.id", primary_key=True)


class ArtistBase(SQLModel):
    first_name: str
    last_name: str


class Artist(ArtistBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    songs: list["Song"] = Relationship(
        back_populates="artists", link_model=ArtistSongLink, sa_relationship_kwargs={"lazy": "joined"}
    )

    @computed_field
    @hybrid_property
    def full_name(self) -> str:
        return self.first_name + " " + self.last_name


class ArtistCreate(ArtistBase):
    pass


class ArtistPublic(ArtistBase):
    id: int
    songs: list["Song"]


class ArtistUpdate(SQLModel):
    first_name: str | None = None
    last_name: str | None = None


class SongBase(SQLModel):
    name: str
    ccli_number: int | None = None


class Song(SongBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    artists: list["Artist"] = Relationship(
        back_populates="songs", link_model=ArtistSongLink, sa_relationship_kwargs={"lazy": "joined"}
    )


class SongCreate(SongBase):
    artists: list[ArtistCreate] | None = None


class SongPublic(SongBase):
    id: int
    artists: list[ArtistPublic]


class SongUpdate(SQLModel):
    name: str | None = None
    ccli_number: int | None = None
    artists: list[ArtistCreate] | None = None


class SpotifyTrack(SQLModel, table=True):
    """Spotify track model"""

    id: str = Field(primary_key=True)
    song_id: int | None = Field(default=None, foreign_key="song.id")


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


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


def insert_spotify_track_by_song_id(song_id: int, spotify_id: str) -> None:
    """Insert a Spotify track into the database"""
    with Session(engine) as session:
        spotify_track = SpotifyTrack(id=spotify_id, song_id=song_id)
        session.add(spotify_track)
        session.commit()


def get_song_by_id(song_id: int, session: Session) -> Song | None:
    """Get a song from the database by ID"""
    song = session.get(Song, song_id, options=(selectinload(Song.artists),))
    return song


def get_song(song_name: str) -> Song | None:
    """Get a song from the database"""
    with Session(engine) as session:
        statement = select(Song).where(Song.name == song_name)
        if result := session.exec(statement).one_or_none():
            return result[0]
        

def search_songs(search: str = '') -> list[Song]:
    """Search for songs in the database"""
    with Session(engine) as session:
        songs = session.exec(
            select(Song)
            .where(
                text(f"lower(name) like '%{search}%'")
                ).options(selectinload(Song.artists)))
        return [s[0] for s in songs.all()]
    

def search_artists(search: str = '') -> list[Artist]:
    """Search for artists in the database"""
    with Session(engine) as session:
        artists = session.exec(
            select(Artist)
            .where(
                text(f"lower(first_name ||' '|| last_name) like '%{search}%'")
                ).options(selectinload(Artist.songs)))
        return [a[0] for a in artists.all()]
        

def get_artist_by_id(artist_id: int) -> Artist | None:
    """Get an artist from the database by ID"""
    with Session(engine) as session:
        artist = session.get(Artist, artist_id, options=(selectinload(Artist.songs),))
        return artist


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


def get_all_songs() -> list[Song]:
    """Get all songs"""
    with Session(engine) as session:
        statement = select(Song).options(selectinload(Song.artists))
        result = session.exec(statement)
        return [s[0] for s in result.all()]


def get_all_artists() -> list[Artist]:
    """Get all artists"""
    with Session(engine) as session:
        statement = select(Artist).options(selectinload(Artist.songs))
        result = session.exec(statement)
        return [a[0] for a in result.all()]


def main() -> None:
    create_db_and_tables()


if __name__ == "__main__":
    main()
