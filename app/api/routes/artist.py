from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_current_active_user
from app.crud.artist import get_all_artists, get_artist_by_id, search_artists
from app.models import ArtistPublic


router = APIRouter(
    prefix="/artists",
    tags=["artists"],
    dependencies=[Depends(get_current_active_user)],
)


@router.get("/{artist_id}", response_model=ArtistPublic)
def read_artist(artist_id: int):
    artist = get_artist_by_id(artist_id)
    if artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist


@router.get("/", response_model=list[ArtistPublic])
def read_artists(search: str = None):
    if search:
        return search_artists(search)
    return get_all_artists()
