"""Main module mainly used for testing"""

from google_flights_scraper_v2 import GoogleFlightsScraperv2
from csv_manager import CSVManager

if __name__ == "__main__":
    scraper = GoogleFlightsScraperv2()
    flight_data = scraper.search_flights("dub", "bari")
    #scraper.display_results(flight_data)

    csv_manager = CSVManager("flight_prices.csv")
    csv_manager.save_data_dictionary(flight_data, headers=["Month", "Date", "Price"])
