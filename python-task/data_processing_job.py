from typing import List

import pandas as pd

from utils.data_utils import *
from utils.request_utils import *

OUTER_MERGE = "outer"
SUFFIXES = ("", "_drop")

HU_COLUMN = "hu"
GRUPPE_COLUMN = "gruppe"
KURZNAME_COLUMN = "kurzname"


class DataProcessingJob:
    _LOCAL_DATA_PATH = "resources/vehicles.csv"

    _TOKEN_REQUEST_ULR = "https://api.baubuddy.de/index.php/login"
    _TOKEN_REQUEST_PAYLOAD = payload = {
        "username": "365",
        "password": "1"
    }
    _TOKEN_REQUEST_HEADERS = headers = {
        "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
        "Content-Type": "application/json"
    }

    _RESOURCE_REQUEST_URL = "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active"
    _RESOURCE_REQUEST_HEADERS = {
        "Authorization": f"Bearer {get_access_token(_TOKEN_REQUEST_ULR, _TOKEN_REQUEST_PAYLOAD, _TOKEN_REQUEST_HEADERS)}",
        "Content-Type": "application/json"
    }

    _COLOR_REQUEST_URL = "https://api.baubuddy.de/dev/index.php/v1/labels/"

    def __init__(self, columns: List[str], to_color_rows: bool):
        self.columns = columns
        self.to_color_rows = to_color_rows

    def run(self):
        data = self._extract()
        final_data = self._transform(data)
        self._load(final_data)

    def _extract(self):
        # Read local data into DataFrame
        local_data_df = pd.read_csv(self._LOCAL_DATA_PATH, sep=";")
        # Download resource data
        resource_data = get_request_resource(self._RESOURCE_REQUEST_URL, self._RESOURCE_REQUEST_HEADERS)
        # Create DataFrame from the resource data
        request_data_df = pd.DataFrame(resource_data)

        return local_data_df, request_data_df

    def _transform(self, data):
        local_data_df, request_data_df = data

        # Get the common columns from both DataFrames
        common_columns = get_common_columns(request_data_df, local_data_df)
        # Remove the merge column from the common columns list
        common_columns.remove(KURZNAME_COLUMN)
        # Merge both DataFrames
        merged_df = merge_dataframes(local_data_df, request_data_df, OUTER_MERGE, KURZNAME_COLUMN, SUFFIXES)
        # Filter rows where "hu" column is None
        filtered_df = filter_rows_with_none_values(merged_df, HU_COLUMN)
        # Replace None values from the duplicate column
        clean_df = replace_none_values(filtered_df, common_columns)
        # Drop the duplicate columns
        clean_df = drop_duplicate_columns(clean_df, common_columns)
        # Sort DataFrame by "gruppe" column
        sorted_df = sort_dataframe(clean_df, GRUPPE_COLUMN, True)

        # for rnr in clean_df["rnr"]:
        #     URL_2 = f'https://api.baubuddy.de/dev/index.php/v1/labels/{rnr}'
        #     labelid_data_as_json = get_request_resource(URL_2, self._RESOURCE_REQUEST_HEADERS)
        #     print(labelid_data_as_json)

        sorted_df.to_excel('C:/Users/Stefan/Desktop/sorted_file.xlsx')

    def _load(self, final_data):
        pass
