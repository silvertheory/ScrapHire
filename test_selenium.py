from selenium import webdriver
from selenium.webdriver.chrome.service import Service


# Point to chromedriver.exe.
service = Service('./chromedriver.exe')

# Launch Chrome
driver = webdriver.Chrome(service=service)

# Open web page
driver.get('https://www.google.com')

# Wait for a few seconds so you can see it open.
import time
time.sleep(3)

# Close the browser

driver.quit()