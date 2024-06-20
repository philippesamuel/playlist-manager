from scrapper.config import settings


from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://mosaikberlin.church.tools/?q=churchservice#SongView/"


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
