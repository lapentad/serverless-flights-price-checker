import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class GoogleFlightsScraper:
    def __init__(self, url="https://www.google.com/travel/flights"):
        self.url = url
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(800, 800)
        self.actions = ActionChains(self.driver)
        logging.info("Initialized WebDriver and set window size.")

    def click_from_xpath(self, xpath):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.click()
        except Exception as e:
            logging.error("Button not found. %s", e)

    def open_page(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        self.click_from_xpath("//button[@aria-label='Reject all']")
        logging.info("Rejected cookies.")

    def enter_location(self, xpath, location):
        logging.info("Entering location: %s", location)
        search_box = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        search_box.clear()
        search_box.send_keys(location)
        time.sleep(1)
        self.actions.send_keys(Keys.ENTER).perform()

    def search_flights(self, origin, destination):
        logging.info("Searching flights from %s to %s.", origin, destination)
        self.enter_location("//input[@aria-label='Where from?']", origin)
        self.enter_location("//input[contains(@aria-label, 'Where to')]", destination)
        self.click_from_xpath("//button[@jsname='vLv7Lb' and @aria-label='Search']")

    def click_next_button(self):
        source = self.driver.page_source
        soup = BeautifulSoup(source, "html.parser")

        months = [
            div.get_text()
            for div in soup.find_all("div", class_="BgYkof B5dqIf qZwLKe")
        ]
        clicks = len(months) - 2
        logging.info(
            "Detected %s months, clicking 'Next' button %s times.", len(months), clicks
        )

        time.sleep(2)
        for i in range(clicks):
            self.click_from_xpath("//button[@jsname='KpyLEe' and @aria-label='Next']")
            logging.info("Finding prices for: %s", months[i])
            time.sleep(3)
        return months

    def extract_data(self):
        logging.info("Extracting flight data.")
        months = self.click_next_button()
        month_data = {month: [] for month in months}

        source = self.driver.page_source
        soup = BeautifulSoup(source, "html.parser")
        all_dates = soup.find_all("div", class_="p1BRgf KQqAEc")
        month_index = 0
        prev_date = None

        for cell in all_dates:
            date_div = cell.find("div", class_="eoY5cb CylAxb sLG56c yCya5")
            price_div = cell.find("div", class_="CylAxb n3qw7 UNMzKf julK3b")

            if date_div:
                date = int(date_div.text.strip())
                price = price_div.text.strip() if price_div else "N/A"

                if prev_date is not None and date < prev_date:
                    month_index += 1

                if month_index < len(months):
                    month_data[months[month_index]].append((date, price))
                prev_date = date
        logging.info("Data extraction complete.")
        return month_data

    def display_results(self, data):
        for month, dates in data.items():
            print(f"\n{month}:")
            for date, price in dates:
                print(f"  Date: {date}, Price: {price}")

    def close_browser(self):
        logging.info("Closing browser.")
        self.driver.quit()


if __name__ == "__main__":
    start = time.time()
    scraper = GoogleFlightsScraper()
    scraper.open_page()
    scraper.search_flights("dub", "bari")
    flight_data = scraper.extract_data()
    scraper.display_results(flight_data)
    scraper.close_browser()
    end = time.time()
    elapsed = end - start
    print(f"Time taken: {elapsed:.6f} seconds")
