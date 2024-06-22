from loguru import logger

from churchtools import login_and_yield_song_data
from app.crud.song import insert_song, update_song
from scrapper.browser import get_browser


def main() -> None:
    browser = get_browser()
    for song_name, song_artists, ccli_number in login_and_yield_song_data(browser):
        if song_artists:
            split = map(str.split, song_artists)
            split = (names for names in split if len(names) >= 2)
            song_artists_clean = [(first_name, last_name) for first_name, *_, last_name in split]
        # insert_song(song_name, song_artists_clean, ccli_number)
        update_song(song_name, song_artists_clean, ccli_number)


if __name__ == "__main__":
    main()
