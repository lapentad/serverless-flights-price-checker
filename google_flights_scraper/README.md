# Web Scraping Google Flights with Selenium

This project demonstrates how to use Selenium to scrape data from Google Flights. Google Flights dynamically loads its content using JavaScript and requires user interaction to display flight information. Traditional web scraping tools like `requests` and `BeautifulSoup` are insufficient for this task, as they cannot handle JavaScript-rendered content or simulate user interactions.

## Why Selenium?

Selenium is a tool for web automation used mainly for testing but also it can:

- Interact with web pages as a real user would (e.g., clicking buttons, filling forms).
- Wait for JavaScript-rendered content to load.
- Extract data from dynamic web pages.

## Use Case

Google Flights does not display flight data unless there is user interaction, such as selecting dates or destinations. This project uses Selenium to automate these interactions and retrieve the required data.

## Prerequisites

- Python installed on your system.
- Libraries `pip install -r requirements.txt`
- A compatible web driver (e.g., ChromeDriver for Google Chrome).

## In Action
```bash
python google_flights_scraper.py
```
Time taken: 37.649263 seconds

```bash
python main.py
```
Generates *flight_prices.csv* with Month Date and Price for Dublin-Bari flights.

```bash
python google_flights_scraper_v2.py
```
Time taken: 35.923318 seconds