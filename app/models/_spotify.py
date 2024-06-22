from sqlmodel import Field, SQLModel


class SpotifyTrack(SQLModel, table=True):
    """Spotify track model"""

    id: str = Field(primary_key=True)
    song_id: int | None = Field(default=None, foreign_key="song.id")
