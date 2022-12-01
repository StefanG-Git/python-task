from unittest import TestCase

import numpy as np
import pandas as pd

from utils.data_utils import *


class DataUtilsTests(TestCase):
    _SUFFIX = "_drop"
    _OUTER_MERGE = "outer"
    _INNER_MERGE = "inner"
    _LEFT_MERGE = "left"
    _RIGHT_MERGE = "right"

    _MERGE_COLUMN = "merge_colum"
    _FIRST_DF_MERGE_COLUMN_DATA = [1, 2, 3, 4]
    _SECOND_DF_MERGE_COLUMN_DATA = [1, 2, 3, 4]

    _COLUMN_1 = "col1"
    _FIRST_DF_COLUMN_1_DATA = [np.nan, np.nan, np.nan, "D"]
    _SECOND_DF_COLUMN_1_DATA = ["A", np.nan, "C", np.nan]

    _DATE_COLUMN = "date_column"
    _DATE_COLUMN_DATA = ["2022-11-15", "2021-11-15", "2022-05-15", "2022-11-15"]

    _FIRST_DF_DATA = {
        _MERGE_COLUMN: _FIRST_DF_MERGE_COLUMN_DATA,
        _COLUMN_1: _FIRST_DF_COLUMN_1_DATA,
        _DATE_COLUMN: _DATE_COLUMN_DATA
    }

    _SECOND_DF_DATA = {
        _MERGE_COLUMN: _SECOND_DF_MERGE_COLUMN_DATA,
        _COLUMN_1: _SECOND_DF_COLUMN_1_DATA,
    }

    def setUp(self):
        self.first_df = pd.DataFrame(self._FIRST_DF_DATA)
        self.second_df = pd.DataFrame(self._SECOND_DF_DATA)

    def test_merge_dataframes__when_outer_merge_and_same_keys_count__expect_same_keys_and_new_columns(self):
        # Arrange
        expected_keys = [1, 2, 3, 4]
        expected_rows_count = 4
        expected_columns = [self._MERGE_COLUMN, self._COLUMN_1, self._DATE_COLUMN, self._COLUMN_1 + self._SUFFIX]
        expected_columns_count = 4

        # Act
        new_df = merge_dataframes(
            self.first_df,
            self.second_df,
            self._OUTER_MERGE,
            self._MERGE_COLUMN,
            ("", self._SUFFIX)
        )
        actual_keys = new_df[self._MERGE_COLUMN].tolist()
        actual_rows_count = len(new_df.index)
        actual_columns = list(new_df.columns)
        actual_columns_count = len(actual_columns)

        # Assert
        self.assertListEqual(expected_keys, actual_keys)
        self.assertEqual(expected_rows_count, actual_rows_count)
        self.assertListEqual(expected_columns, actual_columns)
        self.assertEqual(expected_columns_count, actual_columns_count)

    def test_merge_dataframes__when_outer_merge_and_diff_keys_count__expect_keys_from_both_dfs_and_new_columns(self):
        # Arrange
        expected_keys = [1, 2, 3, 4, 5]
        expected_rows_count = 5
        expected_columns = [self._MERGE_COLUMN, self._COLUMN_1, self._DATE_COLUMN, self._COLUMN_1 + self._SUFFIX]
        expected_columns_count = 4

        # Act
        row = pd.DataFrame([{
            self._MERGE_COLUMN: 5,
            self._COLUMN_1: "E",
            self._DATE_COLUMN: "2022-11-15"
        }])

        df = pd.concat([self.first_df, row])

        new_df = merge_dataframes(
            df,
            self.second_df,
            self._OUTER_MERGE,
            self._MERGE_COLUMN,
            ("", self._SUFFIX)
        )
        actual_keys = new_df[self._MERGE_COLUMN].tolist()
        actual_rows_count = len(new_df.index)
        actual_columns = list(new_df.columns)
        actual_columns_count = len(actual_columns)

        # Assert
        self.assertListEqual(expected_keys, actual_keys)
        self.assertEqual(expected_rows_count, actual_rows_count)
        self.assertListEqual(expected_columns, actual_columns)
        self.assertEqual(expected_columns_count, actual_columns_count)

    def test_merge_dataframes__when_inner_merge_and_same_keys__expect_same_keys_and_new_columns(self):
        # Arrange
        expected_keys = [1, 2, 3, 4]
        expected_rows_count = 4
        expected_columns = [self._MERGE_COLUMN, self._COLUMN_1, self._DATE_COLUMN, self._COLUMN_1 + self._SUFFIX]
        expected_columns_count = 4

        # Act
        new_df = merge_dataframes(
            self.first_df,
            self.second_df,
            self._INNER_MERGE,
            self._MERGE_COLUMN,
            ("", self._SUFFIX)
        )
        actual_keys = new_df[self._MERGE_COLUMN].tolist()
        actual_rows_count = len(new_df.index)
        actual_columns = list(new_df.columns)
        actual_columns_count = len(actual_columns)

        # Assert
        self.assertListEqual(expected_keys, actual_keys)
        self.assertEqual(expected_rows_count, actual_rows_count)
        self.assertListEqual(expected_columns, actual_columns)
        self.assertEqual(expected_columns_count, actual_columns_count)

    def test_merge_dataframes__when_inner_merge_and_diff_keys__expect_match_keys_only_and_new_columns(self):
        # Arrange
        expected_keys = [1, 2, 3, 4]
        expected_rows_count = 4
        expected_columns = [self._MERGE_COLUMN, self._COLUMN_1, self._DATE_COLUMN, self._COLUMN_1 + self._SUFFIX]
        expected_columns_count = 4

        # Act
        row = pd.DataFrame([{
            self._MERGE_COLUMN: 5,
            self._COLUMN_1: "E",
            self._DATE_COLUMN: "2022-11-15"
        }])

        df = pd.concat([self.first_df, row])

        new_df = merge_dataframes(
            df,
            self.second_df,
            self._INNER_MERGE,
            self._MERGE_COLUMN,
            ("", self._SUFFIX)
        )
        actual_keys = new_df[self._MERGE_COLUMN].tolist()
        actual_rows_count = len(new_df.index)
        actual_columns = list(new_df.columns)
        actual_columns_count = len(actual_columns)

        # Assert
        self.assertListEqual(expected_keys, actual_keys)
        self.assertEqual(expected_rows_count, actual_rows_count)
        self.assertListEqual(expected_columns, actual_columns)
        self.assertEqual(expected_columns_count, actual_columns_count)

    def test_merge_dataframes__when_left_merge_and_same_keys__expect_same_keys_and_new_columns(self):
        # Arrange
        expected_keys = [1, 2, 3, 4]
        expected_rows_count = 4
        expected_columns = [self._MERGE_COLUMN, self._COLUMN_1, self._DATE_COLUMN, self._COLUMN_1 + self._SUFFIX]
        expected_columns_count = 4

        # Act
        new_df = merge_dataframes(
            self.first_df,
            self.second_df,
            self._LEFT_MERGE,
            self._MERGE_COLUMN,
            ("", self._SUFFIX)
        )
        actual_keys = new_df[self._MERGE_COLUMN].tolist()
        actual_rows_count = len(new_df.index)
        actual_columns = list(new_df.columns)
        actual_columns_count = len(actual_columns)

        # Assert
        self.assertListEqual(expected_keys, actual_keys)
        self.assertEqual(expected_rows_count, actual_rows_count)
        self.assertListEqual(expected_columns, actual_columns)
        self.assertEqual(expected_columns_count, actual_columns_count)

    def test_merge_dataframes__when_left_merge_and_diff_keys__expect_keys_from_left_df_and_new_columns(self):
        # Arrange
        expected_keys = [1, 2, 3, 4, 5]
        expected_rows_count = 5
        expected_columns = [self._MERGE_COLUMN, self._COLUMN_1, self._DATE_COLUMN, self._COLUMN_1 + self._SUFFIX]
        expected_columns_count = 4

        # Act
        row = pd.DataFrame([{
            self._MERGE_COLUMN: 5,
            self._COLUMN_1: "E",
            self._DATE_COLUMN: "2022-11-15"
        }])

        df = pd.concat([self.first_df, row])

        new_df = merge_dataframes(
            df,
            self.second_df,
            self._LEFT_MERGE,
            self._MERGE_COLUMN,
            ("", self._SUFFIX)
        )
        actual_keys = new_df[self._MERGE_COLUMN].tolist()
        actual_rows_count = len(new_df.index)
        actual_columns = list(new_df.columns)
        actual_columns_count = len(actual_columns)

        # Assert
        self.assertListEqual(expected_keys, actual_keys)
        self.assertEqual(expected_rows_count, actual_rows_count)
        self.assertListEqual(expected_columns, actual_columns)
        self.assertEqual(expected_columns_count, actual_columns_count)

    def test_merge_dataframes__when_right_merge_and_same_keys__expect_same_keys_and_new_columns(self):
        # Arrange
        expected_keys = [1, 2, 3, 4]
        expected_rows_count = 4
        expected_columns = [self._MERGE_COLUMN, self._COLUMN_1, self._DATE_COLUMN, self._COLUMN_1 + self._SUFFIX]
        expected_columns_count = 4

        # Act
        new_df = merge_dataframes(
            self.first_df,
            self.second_df,
            self._RIGHT_MERGE,
            self._MERGE_COLUMN,
            ("", self._SUFFIX)
        )
        actual_keys = new_df[self._MERGE_COLUMN].tolist()
        actual_rows_count = len(new_df.index)
        actual_columns = list(new_df.columns)
        actual_columns_count = len(actual_columns)

        # Assert
        self.assertListEqual(expected_keys, actual_keys)
        self.assertEqual(expected_rows_count, actual_rows_count)
        self.assertListEqual(expected_columns, actual_columns)
        self.assertEqual(expected_columns_count, actual_columns_count)

    def test_merge_dataframes__when_right_merge_and_diff_keys__expect_keys_from_right_df_and_new_columns(self):
        # Arrange
        expected_keys = [1, 2, 3, 4]
        expected_rows_count = 4
        expected_columns = [self._MERGE_COLUMN, self._COLUMN_1, self._DATE_COLUMN, self._COLUMN_1 + self._SUFFIX]
        expected_columns_count = 4

        # Act
        row = pd.DataFrame([{
            self._MERGE_COLUMN: 5,
            self._COLUMN_1: "E",
            self._DATE_COLUMN: "2022-11-15"
        }])

        df = pd.concat([self.first_df, row])

        new_df = merge_dataframes(
            df,
            self.second_df,
            self._RIGHT_MERGE,
            self._MERGE_COLUMN,
            ("", self._SUFFIX)
        )
        actual_keys = new_df[self._MERGE_COLUMN].tolist()
        actual_rows_count = len(new_df.index)
        actual_columns = list(new_df.columns)
        actual_columns_count = len(actual_columns)

        # Assert
        self.assertListEqual(expected_keys, actual_keys)
        self.assertEqual(expected_rows_count, actual_rows_count)
        self.assertListEqual(expected_columns, actual_columns)
        self.assertEqual(expected_columns_count, actual_columns_count)

    def test_filter_rows_with_null_values_from_df__when_column_contains_null_values__expect_rows_to_be_removed(self):
        # Arrange
        expected_rows_count = 2
        expected_col_1_values = ["A", "C"]

        # Act
        new_df = filter_rows_with_null_values_from_df(self.second_df, self._COLUMN_1)
        actual_rows_count = len(new_df.index)
        actual_col_1_values = new_df[self._COLUMN_1].tolist()
        contains_null_values = new_df[self._COLUMN_1].isnull().values.any()

        # Assert
        self.assertEqual(expected_rows_count, actual_rows_count)
        self.assertListEqual(expected_col_1_values, actual_col_1_values)
        self.assertFalse(contains_null_values)

    def test_filter_rows_with_null_values_from_df__when_no_null_values_in_column__expect_no_change(self):
        # Arrange
        expected_rows_count = 4
        expected_col_1_values = ["A", "Some value", "C", "Some value"]

        # Act
        self.second_df[self._COLUMN_1].fillna("Some value", inplace=True)
        new_df = filter_rows_with_null_values_from_df(self.second_df, self._COLUMN_1)
        actual_rows_count = len(new_df.index)
        actual_col_1_values = new_df[self._COLUMN_1].tolist()

        # Assert
        self.assertEqual(expected_rows_count, actual_rows_count)
        self.assertListEqual(expected_col_1_values, actual_col_1_values)

    def test_get_common_columns_from_dfs__when_dfs_have_common_columns__expect_list_with_the_common_columns(self):
        # Arrange
        expected_common_columns = [self._MERGE_COLUMN, self._COLUMN_1]

        # Act
        actual_common_columns = get_common_columns_from_dfs(self.first_df, self.second_df)

        # Assert
        self.assertListEqual(expected_common_columns, actual_common_columns)

    def test_get_common_columns_from_dfs__when_no_common_columns__expect_empty_list(self):
        # Arrange
        expected_common_columns = []

        # Act
        new_df = self.first_df.drop([self._MERGE_COLUMN, self._COLUMN_1], axis=1)
        actual_common_columns = get_common_columns_from_dfs(new_df, self.second_df)

        # Assert
        self.assertListEqual(expected_common_columns, actual_common_columns)

    def test_replace_null_values_in_df__when_they_are_replacement_values__expect_to_replace_null_values(self):
        # Arrange
        expected_values_col_1 = ["A", np.nan, "C", "D"]

        # Act
        df = merge_dataframes(
            self.first_df,
            self.second_df,
            self._OUTER_MERGE,
            self._MERGE_COLUMN,
            ("", self._SUFFIX)
        )
        new_df = replace_null_values_in_df(df, [self._COLUMN_1], self._SUFFIX)
        actual_values_col_1 = new_df[self._COLUMN_1].tolist()

        # Assert
        self.assertListEqual(expected_values_col_1, actual_values_col_1)

    def test_drop_suffix_columns_from_df__when_they_are_suffix_columns__expect_to_be_removed(self):
        # Arrange
        expected_columns_count = 3
        expected_columns = [self._MERGE_COLUMN, self._COLUMN_1, self._DATE_COLUMN]

        # Act
        df = merge_dataframes(
            self.first_df,
            self.second_df,
            self._OUTER_MERGE,
            self._MERGE_COLUMN,
            ("", self._SUFFIX)
        )
        new_df = drop_suffix_columns_from_df(df, [self._COLUMN_1], self._SUFFIX)
        actual_columns_count = len(new_df.columns)
        actual_columns = new_df.columns.tolist()

        # Assert
        self.assertEqual(expected_columns_count, actual_columns_count)
        self.assertEqual(expected_columns, actual_columns)

    def test_drop_suffix_columns_from_df__when_they_are_no_suffix_columns__expect_no_change(self):
        # Arrange
        expected_columns_count = 3
        expected_columns = [self._MERGE_COLUMN, self._COLUMN_1, self._DATE_COLUMN]

        # Act
        new_df = drop_suffix_columns_from_df(self.first_df, expected_columns, self._SUFFIX)
        actual_columns_count = len(new_df.columns)
        actual_columns = new_df.columns.tolist()

        # Assert
        self.assertEqual(expected_columns_count, actual_columns_count)
        self.assertEqual(expected_columns, actual_columns)

    def test_drop_mismatch_columns__when_they_are_mismatch_columns__expect_to_be_removed(self):
        # Arrange
        expected_columns_count = 2
        expected_columns = [self._MERGE_COLUMN, self._COLUMN_1]

        # Act
        new_df = drop_mismatch_columns(self.first_df, self.second_df.columns.tolist())
        actual_columns_count = len(new_df.columns)
        actual_columns = new_df.columns.tolist()

        # Assert
        self.assertEqual(expected_columns_count, actual_columns_count)
        self.assertListEqual(expected_columns, actual_columns)
        self.assertTrue(self._DATE_COLUMN not in new_df.columns)

    def test_drop_mismatch_columns__when_they_are_no_mismatch_columns__expect_no_change(self):
        # Arrange
        expected_columns_count = 3
        expected_columns = self.first_df.columns.tolist()

        # Act
        new_df = drop_mismatch_columns(self.first_df, expected_columns)
        actual_columns_count = len(new_df.columns)
        actual_columns = new_df.columns.tolist()

        # Assert
        self.assertEqual(expected_columns_count, actual_columns_count)
        self.assertListEqual(expected_columns, actual_columns)

    def test_sort_dataframe__when_ascending_is_true__expect_df_to_be_sorted_in_ascending_order(self):
        # Arrange
        expected_first_row_values = [2, np.nan, '2021-11-15']
        expected_last_row_values = [4, 'D', '2022-11-15']

        # Act
        new_df = sort_dataframe(self.first_df, self._DATE_COLUMN, True)
        actual_first_row_values = new_df.iloc[0].tolist()
        actual_last_row_values = new_df.iloc[-1].tolist()

        # Assert
        self.assertListEqual(expected_first_row_values, actual_first_row_values)
        self.assertListEqual(expected_last_row_values, actual_last_row_values)

    def test_sort_dataframe__when_ascending_is_false__expect_df_to_be_sorted_in_descending_order(self):
        # Arrange
        expected_first_row_values = [1, np.nan, '2022-11-15']
        expected_last_row_values = [2, np.nan, '2021-11-15']

        # Act
        new_df = sort_dataframe(self.first_df, self._DATE_COLUMN, False)
        actual_first_row_values = new_df.iloc[0].tolist()
        actual_last_row_values = new_df.iloc[-1].tolist()

        # Assert
        self.assertListEqual(expected_first_row_values, actual_first_row_values)
        self.assertListEqual(expected_last_row_values, actual_last_row_values)
