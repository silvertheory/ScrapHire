from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up Selenium.
service = Service('./chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Open jobs site.
url = "https://realpython.github.io/fake-jobs/"
driver.get(url)

# Wait for page to load.
time.sleep(2)

# Getting page source and parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find all job cards.
job_cards = soup.find_all('div', class_='card-content')

# Prepare list to store job cards.
jobs = []

# Extract details from each job card.
for card in job_cards:
    title_elem = card.find('h2', class_='title')
    company_elem = card.find('h3', class_='company')
    link_elem = card.find_parent().find('a', class_='card-footer-item')

    title = title_elem.text.strip() if title_elem else 'N/A'
    company = company_elem.text.strip() if company_elem else 'N/A'
    link = link_elem['href'] if link_elem else 'N/A'

    print(f"Title: {title}\nCompany: {company}\nLink: {link}\n---")
    jobs.append({'Title': title, 'Company': company, 'Link': link})

# Save to a CSV
df = pd.DataFrame(jobs)
df.to_csv('scrapehire_jobs.csv', index=False)
print("Jobs saved to scrapehire_jobs.csv")

# Close browser.
driver.quit()