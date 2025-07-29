from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

# PAGE OBJECT CLASS -
class FakeJobsPage:
    URL = "https://realpython.github.io/fake-jobs/"

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        """Navigate to the fake jobs site."""
        self.driver.get(self.URL)
        time.sleep(2)  # Allow the page to load

    def get_job_cards(self):
        """Parse all job cards using BeautifulSoup."""
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        return soup.find_all('div', class_='card-content')

    def extract_job_details(self, card):
        """Extracts job data (title, company, link) from a single job card."""
        title_elem = card.find('h2', class_='title')
        company_elem = card.find('h3', class_='company')
        link_elem = card.find_parent().find('a', class_='card-footer-item')

        title = title_elem.text.strip() if title_elem else 'N/A'
        company = company_elem.text.strip() if company_elem else 'N/A'
        link = link_elem['href'] if link_elem else 'N/A'
        return {'Title': title, 'Company': company, 'Link': link}

    def validate_jobs(self, jobs):
        """
        Validates that each job has all fields.
        You could add more advanced checks here later.
        """
        for job in jobs:
            assert job['Title'] and job['Title'] != 'N/A', "Missing job title"
            assert job['Company'] and job['Company'] != 'N/A', "Missing company name"
            assert job['Link'] and job['Link'] != 'N/A', "Missing job link"

    def get_all_jobs(self):
        """Returns a validated list of all jobs as dicts."""
        cards = self.get_job_cards()
        jobs = []
        for card in cards:
            job = self.extract_job_details(card)
            jobs.append(job)
        self.validate_jobs(jobs)
        return jobs

# MAIN SCRIPT -

def main():
    # Setup Selenium Chrome driver
    service = Service('./chromedriver.exe')
    driver = webdriver.Chrome(service=service)

    try:
        # Create Page Object and open the page
        jobs_page = FakeJobsPage(driver)
        jobs_page.open()

        # Extract and validate jobs
        jobs = jobs_page.get_all_jobs()

        # Print all jobs (for user feedback)
        for job in jobs:
            print(f"Title: {job['Title']}\nCompany: {job['Company']}\nLink: {job['Link']}\n---")

        # Save results to CSV
        df = pd.DataFrame(jobs)
        df.to_csv('scrapehire_jobs.csv', index=False)
        print("Jobs saved to scrapehire_jobs.csv")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
