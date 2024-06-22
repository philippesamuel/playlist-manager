from sqlmodel import Field, Relationship, SQLModel

from .artistsong import ArtistSongLink
from .artist import Artist, ArtistCreate, ArtistPublic


class SongBase(SQLModel):
    name: str
    ccli_number: int | None = None


class Song(SongBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    artists: list["Artist"] = Relationship(
        back_populates="songs",
        link_model=ArtistSongLink,
        sa_relationship_kwargs={"lazy": "joined"},
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
