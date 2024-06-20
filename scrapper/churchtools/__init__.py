import re
from typing import Iterator

from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

from scrapper.browser import get_browser
from .auth import login
from .navigate import get_next_page

DELIMITERS = [" | ", ", "]
DELIMITERS_STR = "|".join(map(re.escape, DELIMITERS))
DELIMITERS_PATTERN = re.compile(DELIMITERS_STR)


def main() -> None:
    browser = get_browser()
    for song_name, song_artists, ccli_number in login_and_yield_song_data(browser):
        print(song_name, song_artists, ccli_number)
    input("Press Enter to close browser")


def login_and_yield_song_data(
    browser: webdriver.Chrome,
) -> Iterator[tuple[str, list[str], int | None]]:
    """Log into the ChurchTools website and yield song data."""

    login(browser)
    for node in get_song_data_nodes(browser):
        song_name, song_artists, ccli_number = get_song_data(browser, node)
        yield song_name, song_artists, ccli_number

    while next_page := get_next_page(browser):
        next_page.click()
        for node in get_song_data_nodes(browser):
            song_name, song_artists, ccli_number = get_song_data(browser, node)
            yield song_name, song_artists, ccli_number


def get_song_data_nodes(browser: webdriver.Chrome) -> Iterator[WebElement]:
    """Get the song data nodes from the ChurchTools website."""
    wait = WebDriverWait(browser, 2)

    # Wait until the song data nodes are loaded
    song_data_nodes = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr[class=data]"))
    )

    for node in song_data_nodes:
        yield node


def get_song_data(
    browser: webdriver.Chrome, node: WebElement
) -> tuple[str, list[str], int | None]:
    """Get the song data from the provided node."""
    song_anchor = node.find_elements(By.CSS_SELECTOR, "td>a")[1]

    ActionChains(browser).move_to_element(song_anchor).click().perform()
    song_name = song_anchor.text
    ARTISTS_CSS_SELECTOR = ".entrydetail > div:nth-child(1) > small:nth-child(4)"
    CCLI_ID = "songselect-link"
    wait = WebDriverWait(browser, 2)

    song_artists_node = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ARTISTS_CSS_SELECTOR))
    )
    ActionChains(browser).move_to_element(song_artists_node).perform()
    song_artists_raw_string = song_artists_node.text
    song_artists_raw_string = (
        song_artists_raw_string.replace("Author", "").replace(":", "").strip()
    )
    song_artists = DELIMITERS_PATTERN.split(song_artists_raw_string)
    try:
        ccli_number_raw = browser.find_element(By.ID, CCLI_ID).text
        ccli_number_str = re.search(r"\d{7}", ccli_number_raw).group()
        ccli_number = int(ccli_number_str)
    except NoSuchElementException:
        ccli_number = None
    except Exception as e:
        logger.error(f"Error while processing ccli_number: {e}")
        logger.info(f"{ccli_number_raw}=")
        ccli_number = None

    song_anchor.click()
    return song_name, song_artists, ccli_number


if __name__ == "__main__":
    main()
