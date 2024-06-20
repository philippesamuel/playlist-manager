from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_next_page(browser: webdriver.Chrome) -> WebElement | None:
    wait = WebDriverWait(browser, 2)
    try:
        return wait.until(EC.presence_of_element_located((By.ID, "offsetPlus")))
    except TimeoutException:
        logger.info("No more pages to scrape")
        return None
