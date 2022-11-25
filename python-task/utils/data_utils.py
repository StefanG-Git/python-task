from typing import List, Dict, Any

import pandas as pd

from utils.request_utils import get_request_resource


def merge_dataframes(left_df: pd.DataFrame, right_df: pd.DataFrame,
                     merge_type: str, merge_column: str, suffixes: tuple) -> pd.DataFrame:
    new_df = left_df.merge(right_df, how=merge_type, on=merge_column, suffixes=suffixes)

    return new_df


def filter_rows_with_none_values(df: pd.DataFrame, column: str) -> pd.DataFrame:
    new_df = df[df[column].notnull()]

    return new_df


def get_common_columns(first_df: pd.DataFrame, second_df: pd.DataFrame) -> list:
    common_columns = first_df.columns.intersection(second_df.columns).tolist()

    return common_columns


def replace_null_values(df: pd.DataFrame, common_columns: List[str]) -> pd.DataFrame:
    for column in common_columns:
        df[column] = df[column].where(df[column].notnull(), df[column + "_drop"])

    return df


def drop_suffix_columns(df: pd.DataFrame, columns: List[str], suffix: str) -> pd.DataFrame:
    new_df = df.drop([f"{c}{suffix}" for c in columns], axis=1)

    return new_df


def drop_mismatch_columns(df: pd.DataFrame, columns: List[str]):
    new_df = df.drop(df.columns.difference(columns, sort=False), axis=1)

    return new_df


def sort_dataframe(df: pd.DataFrame, sort_columns: str | List[str], ascending: bool | List[bool]) -> pd.DataFrame:
    new_df = df.sort_values(by=sort_columns, ascending=ascending)

    return new_df


def add_new_column(df: pd.DataFrame, column_name: str, value: Any = None):
    df[column_name] = value

    return df
