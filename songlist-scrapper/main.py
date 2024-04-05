from loguru import logger

from churchtools import get_browser, login_and_yield_song_data
from db import get_db, insert_song


def main() -> None:
    browser = get_browser()
    with get_db() as db:
        for song_name, song_artists in login_and_yield_song_data(browser):
            q = db.execute("SELECT name FROM songs WHERE name = ?", [song_name])
            if q.fetchone():
                logger.info(f"Song '{song_name}' already exists in the database")
                continue
            insert_song(song_name, song_artists)


if __name__ == "__main__":
    main()
