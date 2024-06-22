from sqlmodel import Field, SQLModel


class ArtistSongLink(SQLModel, table=True):
    """Link table between Artist and Song"""

    artist_id: int | None = Field(
        default=None, foreign_key="artist.id", primary_key=True
    )
    song_id: int | None = Field(default=None, foreign_key="song.id", primary_key=True)