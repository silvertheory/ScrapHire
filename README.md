# ScrapHire – Selenium Job Scraper

ScrapHire is a Python automation project that demonstrates browser automation, web scraping, data validation, and automated testing. The application uses Selenium to open a job listing website, extracts job information, and exports the results into a structured CSV file.

The project is organized similarly to a small automation framework to demonstrate good project structure and testing practices.

---

# What This Project Demonstrates

- Python automation and scripting
- Selenium browser automation
- HTML parsing and data extraction
- Data transformation into structured CSV output
- Automated testing with pytest
- Clean project organization

---

# Tech Stack

| Technology | Purpose |
|-----------|--------|
| Python | Core programming language |
| Selenium | Browser automation |
| BeautifulSoup | HTML parsing |
| Pandas | Data processing and CSV export |
| pytest | Automated testing framework |

---

# Project Structure

```
ScrapHire
│
├── src/
│   └── scrapehire.py
│
├── tests/
│   ├── test_selenium.py
│   └── test_output_csv.py
│
├── data/
│   └── scrapehire_jobs.csv
│
├── requirements.txt
├── pytest.ini
└── README.md
```

---

# How It Works

1. Selenium launches a Chrome browser.
2. The script navigates to the Fake Jobs website.
3. Job listings are extracted from the page.
4. The data is validated.
5. Results are exported into a CSV file.

---

# Setup

Create and activate a virtual environment, then install dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the Scraper

```bash
python src/scrapehire.py
```

This will generate:

```
data/scrapehire_jobs.csv
```

---

# Running Tests

The project includes automated tests using pytest.

```bash
pytest
```

Expected output:

```
2 passed
```

---

# Example Output

```
Title                  Company        Link
--------------------------------------------------------------
Software Developer     Adams-Brewer   https://www.realpython.com
(Python)
```

---

# Future Improvements

- Parallel test execution
- Continuous Integration (CI) with GitHub Actions
- Dockerized environment
- Additional scraping targets
- Logging and error handling improvements

---

# Author

David Pacheco  
Automation QA Portfolio Project