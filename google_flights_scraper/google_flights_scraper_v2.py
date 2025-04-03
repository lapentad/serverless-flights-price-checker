import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class GoogleFlightsScraperv2:
    def __init__(self, url="https://www.google.com/travel/flights"):
        self.url = url
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(800, 800)
        self.actions = ActionChains(self.driver)
        logging.info("Initialized WebDriver and set window size.")

    def __click_from_xpath(self, xpath):
        try:
            element = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            self.driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            logging.error("Button not found: %s", e)

    def __open_page(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        self.__click_from_xpath("//button[@aria-label='Reject all']")
        logging.info("Opened page and rejected cookies.")

    def __enter_location(self, xpath, location):
        logging.info("Entering location: %s", location)
        try:
            search_box = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            search_box.clear()
            search_box.send_keys(location)
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "DFGgtd"))
            )
            self.actions.send_keys(Keys.ENTER).perform()
        except Exception as e:
            logging.error("Failed to enter location: %s", e)
            logging.error("Page source: %s", self.driver.page_source)

    def __click_next_button(self):
        logging.info("Navigating through months for flight prices.")
        months = [
            div.text for div in self.driver.find_elements(By.CLASS_NAME, "BgYkof")
        ]

        clicks = len(months) - 2
        for i in range(clicks):
            try:
                next_button = WebDriverWait(self.driver, 2).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@jsname='KpyLEe']"))
                )
                self.driver.execute_script("arguments[0].click();", next_button)
                time.sleep(2)
                logging.info("Navigated to %s", months[i])
            except Exception:
                break
        return months

    def __close_browser(self):
        logging.info("Closing browser.")
        self.driver.quit()

    def __extract_data(self):
        logging.info("Extracting flight data.")
        months = self.__click_next_button()
        month_data = {month: [] for month in months}

        all_dates = self.driver.find_elements(By.CLASS_NAME, "p1BRgf")

        month_index = 0
        prev_date = None

        for cell in all_dates:
            try:
                date_div = cell.find_element(By.CLASS_NAME, "eoY5cb")
                price_div = cell.find_element(By.CLASS_NAME, "n3qw7")

                date = int(date_div.text.strip())
                price = price_div.text.strip() if price_div.text else "N/A"

                if prev_date is not None and date < prev_date:
                    month_index += 1

                if month_index < len(months):
                    month_data[months[month_index]].append((date, price))
                prev_date = date
            except Exception:
                continue

        logging.info("Data extraction complete.")
        self.__close_browser()
        return month_data


    def search_flights(self, origin, destination):
        logging.info("Searching flights from %s to %s.", origin, destination)
        self.__open_page()
        self.__enter_location("//input[@aria-label='Where from?']", origin)
        self.__enter_location("//input[contains(@aria-label, 'Where to')]", destination)
        self.__click_from_xpath("//button[@jsname='vLv7Lb' and @aria-label='Search']")
        return self.__extract_data()

    def display_results(self, data):
        for month, dates in data.items():
            print(f"\n{month}:")
            for date, price in dates:
                print(f"  Date: {date}, Price: {price}")

if __name__ == "__main__":
    start = time.time()
    scraper = GoogleFlightsScraperv2()
    flight_data = scraper.search_flights("dub", "bari")
    scraper.display_results(flight_data)
    end = time.time()
    elapsed = end - start
    print(f"Time taken: {elapsed:.6f} seconds")
