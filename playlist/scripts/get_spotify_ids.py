from dataclasses import dataclass
from pprint import pprint
from typing import Iterator

import requests
from loguru import logger

from playlist.config import settings
from db.db import get_db, insert_spotify

API_SEARCH_URL = "https://api.spotify.com/v1/search"


@dataclass
class TrackData:
    __slots__ = ["track_id", "track_name", "artist_names"]
    track_id: str
    track_name: str
    artist_names: list[str]


def main() -> None:
    # track_name = "Almighty"
    # artist_name = "Simon Brading"

    for song_id, name, artists in get_db_songs():
        if not artists:
            continue
        artist_name = artists[0]
        for track_data in fetch_track_data(track_name=name, artist_name=artist_name):
            pprint(track_data)
            uinsert = input(f"Insert Spotify ID for {name} by {artist_name} [y/n]: ")
            if uinsert.lower() != "y":
                continue
            try:
                insert_spotify(song_id=song_id, spotify_id=track_data.track_id)
            except Exception as e:
                logger.error(f"Error inserting Spotify ID for {name} by {artist_name}: {e}")
            else:
                logger.info(f"Inserted Spotify ID for {name} by {artist_name}")

    # pprint(list(fetch_track_data(track_name=track_name, artist_name=artist_name)))


def get_db_songs() -> Iterator[tuple[int, str, list[str]]]:
    with get_db() as db:
        q = db.execute("SELECT id, name, artists FROM songs")
        yield from q.fetchall()


def fetch_track_data(
    track_name: str,
    artist_name: str | None = None,
    limit: int = 2,
    offset: int = 0,
    market: str = "DE",
) -> Iterator[TrackData]:
    url = API_SEARCH_URL
    params = get_query_params(
        track_name=track_name,
        artist_name=artist_name,
        limit=limit,
        offset=offset,
        market=market,
    )
    res = requests.get(url, headers=get_headers(), params=params)
    if res.status_code != 200:
        logger.error(f"Failed to fetch track data: {res.text}")
        return
    res_data = res.json()
    track_data_generator = map(get_track_data_from_item, res_data["tracks"]["items"])
    yield from track_data_generator


def get_headers() -> dict:
    return {
        "Authorization": f"Bearer {settings.spotify_auth_token}",
        "Content-Type": "application/json",
    }


def get_query_params(
    track_name: str,
    artist_name: str | None = None,
    limit: int = 2,
    offset: int = 0,
    market: str = "DE",
) -> dict:
    return {
        "q": get_search_query(track_name=track_name, artist_name=artist_name),
        "type": "track",
        "market": market,
        "limit": limit,
        "offset": offset,
    }


def get_search_query(track_name: str, artist_name: str | None = None) -> str:
    search_query = f"track='{track_name}'"
    if artist_name:
        search_query += f"&artist='{artist_name}'"
    return search_query


def get_track_data_from_item(item: dict) -> TrackData:
    return TrackData(
        track_id=item["id"],
        track_name=item["name"],
        artist_names=[a["name"] for a in item["artists"]],
    )


if __name__ == "__main__":
    main()
