import csv
import os
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class CSVManager:
    def __init__(self, filename="output.csv"):
        self.filename = filename
        self.filepath = os.path.join(os.getcwd(), self.filename)

    def save_data(self, data, headers=None):
        """Save data to a CSV file, from a list"""
        try:
            with open(self.filepath, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if headers:
                    writer.writerow(headers)
                writer.writerows(data)
            logging.info("Data successfully saved to %s", self.filepath)
        except Exception as e:
            logging.error("An error occurred while saving data: %s", e)

    def save_data_dictionary(self, data, headers=None):
        """Save data to a CSV file, from a double dictionary"""
        try:
            with open(self.filepath, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if headers:
                    writer.writerow(headers)
                for keys, values in data.items():
                    for k, v in values:
                        writer.writerow([keys, k, v])
            logging.info("Data successfully saved to %s", self.filepath)
        except Exception as e:
            logging.error("An error occurred while saving data: %s", e)

    def get_filepath(self):
        return self.filepath
