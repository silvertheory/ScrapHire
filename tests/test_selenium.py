import pytest
from selenium import webdriver


@pytest.mark.smoke
def test_chrome_opens_and_has_title():
    """
    Simple smoke test to prove Selenium can launch Chrome using Selenium Manager.
    """
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.example.com")
        assert driver.title != ""
    finally:
        driver.quit()