"""Pandas Data Processor Module for CSV dataset"""

import os
import pandas as pd


class PandasDataProcessor:
    """PandasDataProcessor Class for CSV dataset read and query"""

    def __init__(self, file_path):
        self.file_path = os.path.join(os.path.dirname((__file__)), file_path)
        self.data_frame = pd.DataFrame()

    def read_csv(self):
        """Reads a CSV file and stores keys (header) and data (rows)."""
        self.data_frame = pd.read_csv(self.file_path)

    def clean_df(self):
        """Replace empty values with EMPTY, checks dates, removes duplicates."""
        self.data_frame.fillna("EMPTY", inplace=True)
        self.data_frame["date"] = pd.to_datetime(self.data_frame["date"])
        self.data_frame.dropna(subset=["date"])
