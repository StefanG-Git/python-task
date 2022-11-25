from typing import List

import pandas as pd

from utils.data_utils import *
from utils.request_utils import *

OUTER_MERGE = "outer"
SUFFIX = "_drop"


class DataProcessingJob:
    _HU_COLUMN = "hu"
    _RNR_COLUMN = "rnr"
    _GRUPPE_COLUMN = "gruppe"
    _KURZNAME_COLUMN = "kurzname"
    _LABEL_IDS_COLUMN = "labelIds"
    _COLOR_CODE_COLUMN = "colorCode"

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

    _ACCESS_TOKEN = get_access_token(_TOKEN_REQUEST_ULR, _TOKEN_REQUEST_PAYLOAD, _TOKEN_REQUEST_HEADERS)

    _RESOURCE_REQUEST_URL = "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active"
    _RESOURCE_REQUEST_HEADERS = {
        "Authorization": f"Bearer {_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    _COLOR_REQUEST_URL = "https://api.baubuddy.de/dev/index.php/v1/labels/"

    def __init__(self, columns: List[str], to_color_rows: bool):
        self.columns = columns + [self._RNR_COLUMN]
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
        common_columns.remove(self._KURZNAME_COLUMN)
        # Merge both DataFrames
        merged_df = merge_dataframes(local_data_df, request_data_df, OUTER_MERGE, self._KURZNAME_COLUMN, ("", SUFFIX))
        # Filter rows where "hu" column is None
        filtered_df = filter_rows_with_none_values(merged_df, self._HU_COLUMN)
        # Replace Null values from the duplicate column
        clean_df = replace_null_values(filtered_df, common_columns)
        # Drop the duplicate columns
        clean_df = drop_suffix_columns(clean_df, common_columns, SUFFIX)
        # Sort DataFrame by "gruppe" column
        sorted_df = sort_dataframe(clean_df, self._GRUPPE_COLUMN, True)
        sorted_df = sorted_df.reset_index(drop=True)
        # Drop columns from the DataFrame that are not in the input
        clean_df = drop_mismatch_columns(sorted_df, self.columns)

        if self._LABEL_IDS_COLUMN in self.columns:
            clean_df = add_new_column(clean_df, self._COLOR_CODE_COLUMN)
            clean_df = None

        if self.to_color_rows:
            pass


    def _load(self, final_data):
        pass
