from loguru import logger

from scrapper.browser import get_browser
from scrapper.churchtools.songlist import login_and_yield_songlist_data


def main() -> None:
    browser = get_browser()
    next(login_and_yield_songlist_data(browser))

    print("hahaha")


if __name__ == "__main__":
    main()
