from pydantic import computed_field
from sqlalchemy.ext.hybrid import hybrid_property
from sqlmodel import Field, Relationship, SQLModel

from .artistsong import ArtistSongLink
from . import song as song_model


class ArtistBase(SQLModel):
    first_name: str
    last_name: str


class Artist(ArtistBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    songs: list["song_model.Song"] = Relationship(
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
    songs: list["song_model.Song"]


class ArtistUpdate(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
