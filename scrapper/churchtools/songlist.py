"""Functions to extract songlists/agenda information"""

from typing import Iterator
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

from scrapper.churchtools.auth import login


URL = "https://mosaikberlin.church.tools/?q=churchservice"


def login_and_yield_songlist_data(
    browser: webdriver.Chrome,
) -> Iterator[tuple[str, list[str], int | None]]:
    """Log into the ChurchTools website and yield songlist data."""

    login(browser, url=URL)

    for node in get_agenda_data_nodes(browser):
        # click anchor tag with service info
        node.click()

        # scroll to songs

        # click a song

        # get html list with songs information

        # go back to previous page

        # list[{song-id:, song-name: }]
        songlist_name, songlist_songs = get_songlist_data(browser, node)
        yield songlist_name, songlist_songs



def get_agenda_data_nodes(browser):
    wait = WebDriverWait(browser, 2)

    # Wait until the song data nodes are loaded
    anchor_nodes = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a"))
    )
    return filter(lambda n: n.get_attribute('id').startswith("detail"), anchor_nodes)


def get_songlist_data():
    pass
