from datetime import datetime
from logger import logger
from typing import List

import pandas as pd
import openpyxl

from utils.data_utils import *
from utils.request_utils import get_access_token

OUTER_MERGE = "outer"
SUFFIX = "_drop"
TODAY = datetime.now()


class DataProcessingJob:
    _HU_COLUMN = "hu"
    _RNR_COLUMN = "rnr"
    _GRUPPE_COLUMN = "gruppe"
    _KURZNAME_COLUMN = "kurzname"
    _LABEL_IDS_COLUMN = "labelIds"

    _LOCAL_DATA_PATH = "resources/vehicles.csv"

    _OUTPUT_DATA_PATH = f"output_data/vehicles_{TODAY.isoformat()}.xlsx".replace(":", ".")

    _TOKEN_REQUEST_ULR = "https://api.baubuddy.de/index.php/login"
    _TOKEN_REQUEST_PAYLOAD = {
        "username": "365",
        "password": "1"
    }
    _TOKEN_REQUEST_HEADERS = {
        "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
        "Content-Type": "application/json"
    }

    _ACCESS_TOKEN = get_access_token(_TOKEN_REQUEST_ULR, _TOKEN_REQUEST_PAYLOAD, _TOKEN_REQUEST_HEADERS)

    _RESOURCE_REQUEST_URL = "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active"
    _RESOURCE_REQUEST_HEADERS = {
        "Authorization": f"Bearer {_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    _COLOR_REQUEST_URL = "https://api.baubuddy.de/dev/index.php/v1/labels/"

    def __init__(self, columns: List[str], add_background_color: bool):
        self.columns = columns
        self.to_color_rows = add_background_color

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value):
        for column in [self._RNR_COLUMN, self._GRUPPE_COLUMN]:
            if column not in value:
                value.append(column)

        self._columns = value

    def run(self):
        logger.info("Running job...")

        data = self._extract()
        result_wb = self._transform(data)
        self._load(result_wb)

    def _extract(self):
        logger.info("Extracting data...")

        # Read local data into DataFrame
        local_data_df = pd.read_csv(self._LOCAL_DATA_PATH, sep=";")
        # Download resource data
        resource_data = get_request_resource_as_json(self._RESOURCE_REQUEST_URL, self._RESOURCE_REQUEST_HEADERS)
        # Create DataFrame from the resource data
        request_data_df = pd.DataFrame(resource_data)

        logger.info("Data extracted successfully!")

        return local_data_df, request_data_df

    def _transform(self, data):
        logger.info("Transforming data...")

        local_data_df, request_data_df = data
        # Get the common columns from both DataFrames
        common_columns = get_common_columns_from_dfs(request_data_df, local_data_df)
        # Remove the merge column from the common columns list
        common_columns.remove(self._KURZNAME_COLUMN)
        # Merge both DataFrames
        merged_df = merge_dataframes(local_data_df, request_data_df, OUTER_MERGE, self._KURZNAME_COLUMN, ("", SUFFIX))
        # Filter rows where "hu" column is Null
        filtered_df = filter_rows_with_null_values_from_df(merged_df, self._HU_COLUMN)
        # Replace Null values from the duplicate column
        clean_df = replace_null_values_in_df(filtered_df, common_columns, SUFFIX)
        # Drop the duplicate columns
        clean_df = drop_suffix_columns_from_df(clean_df, common_columns, SUFFIX)
        # Sort DataFrame by "gruppe" column
        sorted_df = sort_dataframe(clean_df, self._GRUPPE_COLUMN, True)
        sorted_df = sorted_df.reset_index(drop=True)
        # Drop columns from the DataFrame that are not in the input
        clean_df = drop_mismatch_columns(sorted_df, self.columns)

        # Create workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        # Write the data from pandas Dataframe to openpyxl workbook
        write_data_from_pandas_dataframe_to_worksheet(clean_df, ws)

        # Tint the cell's text in workbook if "labelIds" is given in the input
        if self._LABEL_IDS_COLUMN in self.columns:
            add_font_color_to_worksheet_cells(
                clean_df[self._LABEL_IDS_COLUMN],
                ws,
                self._COLOR_REQUEST_URL,
                self._RESOURCE_REQUEST_HEADERS
            )

        # Color rows by date in workbook if add_background_color is True
        if self.to_color_rows:
            add_background_color_to_worksheet_cells(ws, self._HU_COLUMN, TODAY)

        logger.info("Data transformations ended!")

        return wb

    def _load(self, result_wb):
        logger.info("Saving data...")

        # Save the data after the transformations as xlsx file
        result_wb.save(self._OUTPUT_DATA_PATH)
        result_wb.close()

        logger.info("Data saved successfully!")
