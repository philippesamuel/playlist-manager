from pydantic import computed_field
from sqlalchemy.ext.hybrid import hybrid_property
from sqlmodel import Field, Relationship, SQLModel



class SongBase(SQLModel):
    name: str
    ccli_number: int | None = None


class ArtistSongLink(SQLModel, table=True):
    """Link table between Artist and Song"""

    artist_id: int | None = Field(
        default=None, foreign_key="artist.id", primary_key=True
    )
    song_id: int | None = Field(default=None, foreign_key="song.id", primary_key=True)


class Song(SongBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    artists: list["Artist"] = Relationship(
        back_populates="songs",
        link_model=ArtistSongLink,
        sa_relationship_kwargs={"lazy": "joined"},
    )


class SongCreate(SongBase):
    artists: list["ArtistCreate"] | None = None


class SongPublic(SongBase):
    id: int
    artists: list["ArtistPublic"]


class SongUpdate(SQLModel):
    name: str | None = None
    ccli_number: int | None = None
    artists: list["ArtistCreate"] | None = None


class ArtistBase(SQLModel):
    first_name: str
    last_name: str


class Artist(ArtistBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    songs: list["Song"] = Relationship(
        back_populates="artists",
        link_model=ArtistSongLink,
        sa_relationship_kwargs={"lazy": "joined"},
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
