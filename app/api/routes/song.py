from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.api.dependencies import get_current_active_user
from app.crud.song import get_all_songs, get_song_by_id, search_songs
from app.database.db import get_session
from app.models import SongPublic


router = APIRouter(
    prefix="/songs",
    tags=["songs"],
    dependencies=[Depends(get_current_active_user)],
)


@router.get("/{song_id}", response_model=SongPublic)
def read_song(
    song_id: int,
    session: Session = Depends(get_session),
):
    song = get_song_by_id(song_id, session)
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return song


@router.get("/", response_model=list[SongPublic])
def read_songs(
    search: str = None,
):
    if search:
        return search_songs(search)
    return get_all_songs()
