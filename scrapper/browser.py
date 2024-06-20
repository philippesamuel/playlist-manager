from selenium import webdriver


def get_browser() -> webdriver.Chrome:
    """Get a Chrome browser instance."""
    return webdriver.Chrome()