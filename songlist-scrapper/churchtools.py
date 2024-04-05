import re
from typing import Iterator

from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import settings

URL = "https://mosaikberlin.church.tools/?q=churchservice#SongView/"

DELIMITERS = [" | ", ", "]
DELIMITERS_STR = "|".join(map(re.escape, DELIMITERS))
DELIMITERS_PATTERN = re.compile(DELIMITERS_STR)


def main() -> None:
    browser = get_browser()
    for song_name, song_artists in login_and_yield_song_data(browser):
        print(song_name, song_artists)
    input("Press Enter to close browser")


def get_browser() -> webdriver.Chrome:
    """Get a Chrome browser instance."""
    return webdriver.Chrome()


def login_and_yield_song_data(browser: webdriver.Chrome) -> Iterator[tuple[str, list[str]]]:
    """Log into the ChurchTools website and yield song data."""

    login(browser)
    for node in get_song_data_nodes(browser):
        song_name, song_artists = get_song_data(node)
        yield song_name, song_artists

    while next_page := get_next_page(browser):
        next_page.click()
        for node in get_song_data_nodes(browser):
            song_name, song_artists = get_song_data(node)
            yield song_name, song_artists


def get_next_page(browser: webdriver.Chrome) -> WebElement | None:
    wait = WebDriverWait(browser, 2)
    try:
        return wait.until(EC.presence_of_element_located((By.ID, "offsetPlus")))
    except TimeoutException:
        logger.info("No more pages to scrape")
        return None


def login(browser: webdriver.Chrome, url: str = URL) -> None:
    """Log into the ChurchTools website using the provided browser instance."""
    browser.maximize_window()
    browser.get(url)

    username_input = browser.find_element(By.ID, "username")
    pw_input = browser.find_element(By.ID, "password")

    username_input.send_keys(settings.churchtools_user.get_secret_value())
    pw_input.send_keys(settings.churchtools_pw.get_secret_value())

    login_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()


def get_song_data_nodes(browser: webdriver.Chrome) -> Iterator[WebElement]:
    """Get the song data nodes from the ChurchTools website."""
    wait = WebDriverWait(browser, 2)

    # Wait until the song data nodes are loaded
    song_data_nodes = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr[class=data]"))
    )

    for node in song_data_nodes:
        yield node


def get_song_data(node: WebElement) -> tuple[str, list[str]]:
    """Get the song data from the provided node."""
    song_name = node.find_elements(By.CSS_SELECTOR, "td>a")[1].text
    song_artists_raw_string = node.find_elements(By.CSS_SELECTOR, "td>i")[0].text
    song_artists = DELIMITERS_PATTERN.split(song_artists_raw_string)
    return song_name, song_artists


if __name__ == "__main__":
    main()
