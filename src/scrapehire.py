from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@dataclass(frozen=True)
class Job:
    title: str
    company: str
    link: str


class FakeJobsPage:
    URL = "https://realpython.github.io/fake-jobs/"

    def __init__(self, driver: webdriver.Chrome, timeout_seconds: int = 10) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout_seconds)

    def open(self) -> None:
        """Navigate to the fake jobs site and wait for job cards to load."""
        self.driver.get(self.URL)
        # Wait until at least one job card is present (stable alternative to sleep)
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.card-content")))

    def _parse_cards(self) -> List[BeautifulSoup]:
        """Return all job card content blocks parsed from the current page."""
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        return soup.select("div.card-content")

    @staticmethod
    def _extract_job(card_content_div) -> Job:
        """Extract a single job from a card-content div."""
        title_elem = card_content_div.select_one("h2.title")
        company_elem = card_content_div.select_one("h3.company")

        # The link is not inside card-content; it's in the parent card/footer area.
        card = card_content_div.parent  # parent 'div.card' in this page structure
        link_elem = card.select_one("a.card-footer-item")

        title = title_elem.get_text(strip=True) if title_elem else ""
        company = company_elem.get_text(strip=True) if company_elem else ""
        link = link_elem.get("href", "") if link_elem else ""

        return Job(title=title, company=company, link=link)

    @staticmethod
    def validate_jobs(jobs: List[Job]) -> None:
        """Basic validation: each job should have title, company, and link."""
        if not jobs:
            raise AssertionError("No jobs found on the page.")

        for idx, job in enumerate(jobs, start=1):
            assert job.title, f"Job #{idx}: Missing title"
            assert job.company, f"Job #{idx}: Missing company"
            assert job.link, f"Job #{idx}: Missing link"

    def get_all_jobs(self) -> List[Job]:
        """Scrape, validate, and return all jobs."""
        cards = self._parse_cards()
        jobs = [self._extract_job(card) for card in cards]
        self.validate_jobs(jobs)
        return jobs


def project_root() -> Path:
    """Return the project root folder (ScrapHire/)."""
    return Path(__file__).resolve().parents[1]


def output_csv_path() -> Path:
    """Return the output CSV path in data/."""
    return project_root() / "data" / "scrapehire_jobs.csv"


def save_jobs_to_csv(jobs: List[Job], path: Path) -> None:
    """Save job list to CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)  # ensure data/ exists
    df = pd.DataFrame([job.__dict__ for job in jobs])
    df.to_csv(path, index=False)


def main() -> None:
    # Selenium Manager will automatically handle the driver in Selenium 4+
    driver = webdriver.Chrome()

    try:
        page = FakeJobsPage(driver)
        page.open()

        jobs = page.get_all_jobs()

        # Print a small sample so the user knows it worked
        print(f"Scraped {len(jobs)} jobs.")
        for job in jobs[:5]:
            print(f"- {job.title} | {job.company} | {job.link}")
        if len(jobs) > 5:
            print("...")

        csv_path = output_csv_path()
        save_jobs_to_csv(jobs, csv_path)
        print(f"Saved CSV to: {csv_path}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()